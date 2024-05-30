---
layout: default
title: Run BioNeMo as Singularity
nav_order: 1
parent: Singularity
grand_parent: Other Adaptations
---

# Running BioNeMo Framework as Singularity Container


## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## Prerequisites

{: .note }
You will need a ubuntu environment with Singularity, docker, ngc cli, cuda driver, and cuda container toolkit installed. An example Environment I used is shown below. 

### 1. Set up EC2
1. Follow [Step 1 in BioNeMo Framework]({{ "/docs/framework/1_launch_container/ec2" | prepend: site.baseurl }}) to launch a EC2 instance with an instance. Specifically: 
    - Use **NVIDIA GPU Optimized** AMI which has the CUDA driver,  toolkits and NGC CLI installed.
    - Use **g5.16xlarge** instance type (or p3 instance)
    - Optionally, in **security group**, in addition to `SSH`, enable `NFS` port (2049) so that we can mount EFS volume (Skip this step if you're prefer to use the default EC2 EBS volume instead)
    - Use a minimum of 200 GB root volume (container is > 30 GB)
    - The rest are the same as in the EC2 tutorial above. 
2. SSH into the instance. 

### 2. Install Singularity
1. The NVIDIA GPU Optimized AMI does not have Singularity installed. We need to install Singularity from source. First, install dependencies: 
```bash
	sudo apt-get update && sudo apt-get install -y \
	    build-essential \
	    libssl-dev \
	    uuid-dev \
	    libgpgme11-dev \
	    squashfs-tools \
	    libseccomp-dev \
	    pkg-config \
        libglib2.0-dev \
        libfuse3-dev \
        libtool \
        autoconf \
        automake
```
2. Then install Go. Click [here](https://go.dev/dl/) and pick the your version of Go. For example, the latest version is `1.22.3` for me at the time of writing. 
    ```bash
    export VERSION=1.22.3 OS=linux ARCH=amd64 && \
    wget https://dl.google.com/go/go$VERSION.$OS-$ARCH.tar.gz && \
    sudo tar -C /usr/local -xzvf go$VERSION.$OS-$ARCH.tar.gz && \
    rm go$VERSION.$OS-$ARCH.tar.gz
    ```
    Make sure you change the `VERSION=...` to yours
3. Then run
   ```bash
	echo 'export GOPATH=${HOME}/go' >> ~/.bashrc && \
    echo 'export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin' >> ~/.bashrc && \
    source ~/.bashrc
    ```
4. Go to [here](https://github.com/sylabs/singularity/releases) and pick the your version of singularity. For example, the latest version at the time of writing is `4.1.3`. 
5. Run
    ```bash
	export VERSION=4.1.3 && # adjust this as necessary \
	    mkdir -p $GOPATH/src/github.com/sylabs && \
	    cd $GOPATH/src/github.com/sylabs && \
	    wget https://github.com/sylabs/singularity/releases/download/v${VERSION}/singularity-ce-${VERSION}.tar.gz && \
	    tar -xzf singularity-ce-${VERSION}.tar.gz && \
        cd ./singularity-ce-${VERSION}
    ```
    Make sure you change the `VERSION` to yours. 
6. Compile
    ```bash
	./mconfig && \
    make -C ./builddir && \
    sudo make -C ./builddir install
    ```
7. If successful, it will show something like this: 
    ```bash
    DONE
    make: Leaving directory '/home/ubuntu/go/src/github.com/sylabs/singularity-ce-4.1.3/builddir'
    ```
8. Verify installation
    ```bash
    singularity --version
    ```
    You should see the version number. Proceed to next section

## Steps
### Step 1. Pull BioNeMo docker container

{: .note }
Instead of converting local docker image to singularity, it is also possible to directly pull `singularity pull docker://nvcr.io/nvidia/clara/bionemo-framework:<tag>` . However sometimes I encountered issues with the latter approach, so I download a local version of docker image first. 


1. Configure NGC
	```
	cd ~ && ngc config set
	```
2. Pull BioNeMo image from docker
	```
	docker pull nvcr.io/nvidia/clara/bionemo-framework:1.5
	```
3. Build singularity image
	```
	singularity build bionemo-framework.sif docker-daemon:nvcr.io/nvidia/clara/bionemo-framework:1.5
	```
	It will take a while to complete. Once complete, it should say
	```
	INFO:    Build complete: bionemo-framework.sif
	```



### Optional Step 2: Mount EFS volumne

{: .note }
This step is optional but recommended. The container, model weights, and datasets can all take significant amount of space. You can cache the model weights and datasets into a EFS volume and mount it to singularity container. 


1. In the EC2 terminal, create a folder as mounting point. For example `xyu-workspace1`. 
```bash
cd ~ && mkdir xyu-workspace1
```
2. Go to AWS EFS console, create EFS volume. Make sure: 
    - EFS volume is in the same region as the EC2 instance
    - EFS volume uses the same security group as your EC2 instace. 
3. Click on `Attach` in the EFS console, and copy the command provided for the NFS client. It looks like this: 
```bash
sudo mount -t nfs4 -o nfsvers=...,rsize=...,wsize=...,hard,timeo=...,retrans=...,noresvport <some id>.efs.us-west-2.amazonaws.com:/ <name of your folder>
```
3. Go back to the EC2 terminal. Execute the commnad above
4. Change permission from `root` to `ubuntu`. 
	```
	sudo chown -R ubuntu:ubuntu /home/ubuntu/xyu-workspace1
	```

### Step 3: Update singularity config file

1. Find config file
	```
	sudo find / -name singularity.conf
	```
	It should produce path like `/usr/local/etc/singularity/singularity.conf`
5. Open config
	```
	sudo nano /usr/local/etc/singularity/singularity.conf
	```
6. The following items can be update: 
	1. If using overlay, update `sessiondir max size = 51200`. (50 GB). Model weights alone is about 14 GB. Overlay is recommended the first time you use BioNeMo, because you need to use the scripts inside the container to download model weights.
	2. If using `nvccli`: 
		1. Confirm that `nvidia-container-cli` is installed. If you're using the NVIDIA GPU optimized AMI, it should be pre-installed. Confirm by running `which nvidia-container-cli`. It should show a path. 
		2. In the singularity conf file, update `nvidia-container-cli = /path/to/nvidia-container-cli`. If you build the image with `nvidia-container-cli` preinstalled, the correct path should already be there. See [related singularity docs](https://docs.sylabs.io/guides/main/user-guide/gpu.html#nvidia-gpus-cuda-nvidia-container-cli)

### Step 4. Run singularity container (first time)


{: .warning }
> [Singualrity CE containers](https://docs.sylabs.io/guides/main/user-guide/singularity_and_docker.html#read-only-by-default) are read-only by default. You can either use overlay to make the container writable (changes will be lost after the container is destroyed), or you can mount a writable directory to it. The exmaple below mounts `/home/ubuntu/xyu-workspace1` to the container. 


1. Mount EFS volume to `/home/ubuntu/xyu-workspace1`
2. Run
	```bash
	singularity run \
    --nv \
    --writable-tmpfs \
    --bind /home/ubuntu/xyu-workspace1:/workspace/bionemo/xyu-workspace1:rw \
    bionemo-framework.sif \
    "jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.allow_origin='*' --ContentsManager.allow_hidden=True --notebook-dir=/workspace/bionemo"
	```
	- In general, you can use `--nv` + `--writable-tmpfs`, The latter tag makes all directories in the container writable. This creates overlay and the size of the overlay is defined by `sessiondir max size` in the Singularity config file. 
	- Instead of above you can also use `--nv` + `--nvccli` . The latter tag performs GPU container set up sing `nvidia-container-cli`. It also automatically enables `--writable-tmpfs` which is required by `nvidia-container-cli`. Currently `--nvccli` is not compatible with `--fakeroot`
	- `--fakeroot`: some package installations (e.g. in OpenFold inference) will requires this tag. 
	- By default all GPUs are visible 
	- When running `singularity run`, if error pops up: 
		```
		FATAL:   while opening capability config file: open /usr/local/etc/singularity/capability.json: permission denied
		```
		To fix it, try : 
		```bash
		sudo chmod 755 /usr/local/etc/singularity/capability.json
		```
3. This opens up a jupyter lab 

### Step 5. Download model weights
1. To download the pretrained model weights, open a terminal in JupyterLab. 
2. In the terminal, run the `ngc config set` again to set the NGC credentials inside the container. You might need to [install NGC CLI first](https://org.ngc.nvidia.com/setup/installers/cli), before running the command. 
3. Then run
```shell
cd /workspace/bionemo
python download_models.py all --source ngc --download_dir ${BIONEMO_HOME}/models --verbose
```
This will create download the models to `/workspace/bionemo/models` folder. 
4. Optionally, persist the models by copying them to your workspace
```shell
mkdir -p xyu-workspace1/bionemo && cp -r models xyu-workspace1/bionemo/models
```

### Optional Step 6: Run singularity container (with mounted model weights)
If model weights are persisted in the EFS volume, you can mount the model weights to the container and run the container. 

```bash
singularity run \
--nv \
--writable-tmpfs \
--bind /home/ubuntu/xyu-workspace1:/workspace/bionemo/xyu-workspace1:rw \
--bind /home/ubuntu/xyu-workspace1/bionemo/models:/workspace/bionemo/models \
bionemo-framework.sif \
"jupyter lab --allow-root --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.allow_origin='*' --ContentsManager.allow_hidden=True --notebook-dir=/workspace/bionemo"
```
