---
layout: default
title: ESM2nv Inference
nav_order: 1
parent: Step 4. Inference
grand_parent: BioNeMo Framework
---

# ESM2nv Inference

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


{: .highlight }
{% include template/fw_inference_warning.md %}



## Prerequisites
1. Complete Step 1. Make sure you have Jupyter notebook launched. 
2. Have a pretrained model checkpoint `.nemo` file. You can either use the pretrained models we provide in Step 1, or use your own trained model from Step 2. 


## Steps
1. Go to `examples/protein/esm2nv/nbs` folder. Click on `inference_interactive.ipynb`. 
![esm2-inference-interactive]({{ "/assets/images/esm2-inference-interactive.jpg" | prepend: site.baseurl }})
2. By default, the default YAML file is located at
```python
config_path = BIONEMO_HOME / "examples" / "protein" / "esm2nv" / "conf" # /workspace/bionemo/examples/protein/esm2nv/conf
cfg = load_model_config(config_path, config_name="infer.yaml") # infer.yaml
```
3. Open the `infer.yaml` file and update the following fields. 
```yaml
downstream_task:
    restore_from_path: "${oc.env:BIONEMO_HOME}/models/protein/esm2nv/esm2nv_650M_converted.nemo" # Path to pretrained checkpoint.
```
   - `restore_from_path`: path to the default `nemo` model checkpoint. If needed, update it to where your checkpoint is located.
   - `dataset_path`: this doesn't matter
4. Go back to the `inference_interactive.ipynb` and run the cells.
   - **Sequence to hidden states**: this generates per token embedding
   - **Sequence to embedding**: this generates per sequence embedding