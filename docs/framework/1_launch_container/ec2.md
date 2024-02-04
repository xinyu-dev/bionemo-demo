---
layout: default
title: Method 2. On EC2
nav_order: 2
parent: Step 1. Launch container
grand_parent: BioNeMo Framework
---

# Launch container on AWS EC2


## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Prerequisites

{: .note }
Please contact NVIDIA team for NGC access & credentials

1. An AWS account with role permissions to launch EC2 instances and subscribe to the [NVIDIA GPU Optimized VMI](https://aws.amazon.com/marketplace/pp/prodview-7ikjtg3um26wq) through marketplace. 
1. Create an account on [NGC](https://ngc.nvidia.com/signin). No need to access clusters. 
2. Get a NGC API key from [here](https://ngc.nvidia.com/setup/api-key).

## Steps

### Step 1: Launch an EC2 instance
1. In [AWS EC2 console](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1), click on **Launch Instance**. This will open a instance specification page. 
![Launch Instance](/assets/images/ec2-launch-instance.jpg)
2. **Name**: enter a name for your instance
![Name Instance](/assets/images/ec2-name-instance.jpg)
3. Under **Application & OS Images**:
   4. select **Browse more AMIs**.
   ![Browse AMIs](/assets/images/ec2-browse-ami.jpg)
   5. Type `nvidia` in the search bar. Press `Enter`. Then click on **AWS Marketplace AMI**. Then select **NVIDIA GPU Optimized VMI** and click on **Select**.
   ![choose AMI](/assets/images/ec2-choose-ami.jpg)
   7. When prompted, select **Subscribe Now**
8. Under **instance type**, select **p3dn.24xlarge**.See footnote[^1] for more info. 
![choose instance](/assets/images/ec2-choose-instance.jpg)
9. Under **key pair**: Choose an existing key pair or create a new one. If you create a new one, enter a keypair name, then select **RSA** and **.pem**. Download the **.pem** file for later use. 
![choose key pair](/assets/images/ec2-keypairs.jpg)
10. Under **Network settings**: choose the network, subnet, and security group that you want to use. An example is shown below but should be modified according to your organization's policies.
![choose network](/assets/images/ec2-network-settings.jpg)
11. Keep other settings default (or change them as needed). Click on **Launch Instance**. Wait until the `Instance State` becomes `running`.

### Step 2. Connect to a running instance
12. In the EC2 console, wait until the instance state becomes `running`. Then copy the **Public IP4 address** or **Private IP4 address** of the instance, depending on your network settings. 
![copy IP](/assets/images/ec2-copy-ip.jpg)
13. Open a terminal at the local folder where you keep the **.pem** file that was used during instance launch.  Run the following command to change the permissions of the **.pem** file. Replace `your-key-pair.pem` with the name of your **.pem** file.
```shell
chmod 400 your-key-pair.pem
```
14. SSH into the instance.Replace `your-ip4-address` with the public or private IP4 address of your instance. 
```shell
ssh -i your-key-pair.pem -L 8888:127.0.0.1:8888 ubuntu@your-ip4-address
```
15. The first time when you log into the instance, driver installation will start automatically. Wait until the system is ready. 

### Step 3. Pull the BioNeMo container
1. NGC CLI is preinstalled. In the `ubuntu` terminal, type
```shell
ngc config set
```
2. Enter the information as prompted:  
   4. `API key`: enter API key, 
   5. `CLI output`: accept default (ascii) by pressing `Enter`
   6. `org`: Enter the NGC org you're assigned with
   7. `team`: Enter the NGC team you're assigned with
   8. `ace`: Accept default and press `Enter`
9. Pull the BioNeMo container image from NGC. 
```shell
docker pull nvcr.io/nvidia/clara/bionemo-framework:latest
```

### Step 4. Run the BioNeMo container
1. In the ubuntu terminal, make a new folder so we can mount it to docker to persist data. Replace `xyu-workspace1` with your workspace name. See footnote[^2] for more info. 
 ```shell
 cd ~
 mkdir xyu-workspace1
 ```
2. Start the container. Replace `xyu-workspace1` with your workspace name. 
```shell
docker run --rm --privileged --gpus all -p 8888:8888 -v /home/ubuntu/xyu-workspace1:/workspace/bionemo/xyu-workspace1 nvcr.io/nvidia/clara/bionemo-framework:latest "jupyter lab --allow-root --ip=* --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.allow_origin='*' --ContentsManager.allow_hidden=True --notebook-dir=/workspace/bionemo"
```
3. You can now access JupyterLab by visitn `localhost:8888` in your web browser.
![ngc-jupyterlab](/assets/images/ngc-jupyterlab.jpg)






## Footnotes
[^1]: We recommend [A100 (p4 instances)](https://aws.amazon.com/ec2/instance-types/p4/) for training in BioNeMo. However, these instances might be challenging to launch on demand. For this demo we will use [V100 (p3dn.24xlarge)](https://aws.amazon.com/ec2/instance-types/p3/#:~:text=Amazon%20EC2%20P3%20instance%20product%20details) instead. Note that some BioNeMo features might not be supported on V100.  V100 might only be available in some EC2 regions. 
[^2]: This is optional. To persist data you can mount a folder from EBS (in this example), or by mounting [EFS](https://aws.amazon.com/efs/), [Lustre](https://aws.amazon.com/fsx/lustre/) or other file systems. Refer to AWS documentations. 
