---
layout: default
title: Pretrain ESM1nv with custom data
nav_order: 3
parent: ESM1
grand_parent: Recipes
---

# Pretraining ESM1nv with custom data


## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


{: .note }
{% include template/protein_mlm_objective.md %}

## Prerequisites
Complete Step 1. Make sure you have Jupyter notebook launched. 


## Step 1. Prepare clean training data

1. In a directory inside the container, create the following folder structure: 
```
|-- data
    |-- train
        |-- x000.csv
        |-- x001.csv
        |-- ...
    |-- val
        |-- x000.csv
        |-- x001.csv
        |-- ...
    |-- test
        |-- x000.csv
        |-- x001.csv
        |-- ...
```
- the folder names must be exactly `train`, `val`, and `test`
- the file names must be exactly `x000.csv`, `x001.csv`, etc. You can have just 1 CSV file or split into multiple CSVs if it's too large. 
- the CSV file must contain the following column: `record_id`, `sequence`. It's OK to have other columns which won't be used in training.  Download the [template CSV file]({{ "/assets/files/esm1nv_pretrain_input/x000.csv" | prepend: site.baseurl }}).
    ![esm1-pretrain-input]({{ "/assets/images/esm1-pretrain-input.jpg" | prepend: site.baseurl }})

2. Go to `examples/protein/esm1nv/conf/pretrain_small.yaml`, update the following: 
![esm1-pretrain-custom-yaml]({{"/assets/images/esm1-pretrain-custom-yaml.jpg" | prepend: site.baseurl}})
- `dataset_path`: set to the folder that contains train/val/test folder. E.g. the `path/to/data` in the above example
- `dataset.train`, `dataset.val`, `dataset.test`: set to the CSV name or ranges. 
- `csv_mmap.data_col`: set 3 the index of the column containing the sequence. E.g. `3` in the above example
- `downstr_task_validation.enabled`: set to `True` to enable validation-in-the-loop in Step 2. 

## Step 2. (Optional) prepare clean validation-in-the-loop data

{: .note }
{% include template/validation_in_the_loop_protein.md %}


### Scenario 1: Downstream task is per-token classification
An example is 3-state structure prediction. Specifically, for each amino acid in the sequence, we want to predict whether it's in helix, sheet, or coil.

1. In a directory inside the container, create the following folder structure: 
```
|-- downstream
    |-- train
        |-- x000.csv
    |-- test
        |-- x000.csv
```
2. Each CSV file needs to contain `id`, `sequence`, and `target` column. For example: 
![esm1-pretrain-custom-downstream]({{"/assets/images/esm1-pretrain-custom-downstream.jpg" | prepend: site.baseurl}})
- the `target` column can be either `3state` or `8state`. Column name doesn't matter
- the `resolved` column is a used as mask. This is optional. If teh structure of some residue is not resolved, you can put `0` in the sequence corresponding to that residue.
- Download a [template CSV file]({{ "/assets/files/flip_3state/x000.csv" | prepend: site.baseurl }})
3. Go to `examples/protein/esm1nv/conf/pretrain_small.yaml`, make sure `dwnstr_task_validation.enabled = True` 
4. Go to `examples/protein/esm1nv/conf/base_config.yaml`, under `dwnstr_task_validation`, modify the following columns:
![esm1-pretrain-custom-downstream-yaml]({{"/assets/images/esm1-pretrain-custom-downstream-yaml.jpg" | prepend: site.baseurl}})
Specifically: 
   - `task_class`: set to the `PerTokenPredictionCallBack`class
   - `task_type`: set to `token-level-classification`
   - `task_name`: change to whatever you want
   - `dataset_path`: set to the folder that contains train/test folder. E.g. the `path/to/downstream` in the above example
   - `dataset.train`, `dataset.test`: set to the file name. E.g. `x000` in the above example
   - `sequence_column`: set to name of the column that contains the sequence. E.g. `sequence` in the above example
   - `target_column`: set to name of the column that contains the target. E.g. `3state` in the above example/ 
   - `target_size`: set to number of classes. E.g. `3` in the above example
   - `mask_column`: set to name of the column that contains the mask. E.g. `resolved` in the above example. If no mask, set to `mask_column: [null]`. 

### Scenario 2: Downstream task is sequence-level classification
In this example, the downstream task is subcellular location (classification of the protein sequences belonging to one of the 10 subcellular compartments)
1. In a directory inside the container, create the following folder structure: 
```
|-- downstream
    |-- train
        |-- x000.csv
    |-- test
        |-- x000.csv
```
2. Each CSV file needs to contain `id`, `sequence`, and `target` column. For example: 
![esm1-pretrain-custom-downstream-classification]({{"/assets/images/esm1-pretrain-custom-downstream-classification.jpg" | prepend: site.baseurl}})
- the `target` column is `scl_label`. Column name doesn't matter
- Download a [template CSV file]({{ "/assets/files/flip_scl/x000.csv" | prepend: site.baseurl }})
3. Go to `examples/protein/esm1nv/conf/pretrain_small.yaml`, make sure `dwnstr_task_validation.enabled = True` 
4. Go to `examples/protein/esm1nv/conf/base_config.yaml`, under `dwnstr_task_validation`, modify the following columns:
![esm1-pretrain-custom-downstream-yaml-classification]({{"/assets/images/esm1-pretrain-custom-downstream-yaml-classification.jpg" | prepend: site.baseurl}})
- `task_class`: set to `SingleValuePredictionCallBack`
- `task_type`: set to `classification`
- `task_name`: change to whatever you want
- `dataset_path`: set to the folder that contains train/test folder. E.g. the `path/to/downstream` in the above example
- `dataset.train`, `dataset.test`: set to the file name. E.g. `x000` in the above example
- `sequence_column`: set to name of the column that contains the sequence. E.g. `sequence` in the above example
- `target_column`: set to name of the column that contains the target. E.g. `scl_label` in the above example/
- `target_size`: set to number of classes. E.g. `10` in the above example
- `mask_column`: comment this out. 

### Scenario 3: Downstream task is sequence-level regression
In this example, the downstream task is predicting the melting temperature of the protein sequences.
1. In a directory inside the container, create the following folder structure: 
```
|-- downstream
    |-- train
        |-- x000.csv
    |-- test
        |-- x000.csv
```
2. Each CSV file needs to contain `id`, `sequence`, and `target` column. For example:
![esm1-pretrain-custom-downstream-regression]({{"/assets/images/esm1-pretrain-custom-downstream-regression.jpg" | prepend: site.baseurl}})
- the `target` column is `target`. Column name doesn't matter
- Download a [template CSV file]({{ "/assets/files/flip_meltome/x000.csv" | prepend: site.baseurl }})
3. Go to `examples/protein/esm1nv/conf/pretrain_small.yaml`, make sure `dwnstr_task_validation.enabled = True`
4. Go to `examples/protein/esm1nv/conf/base_config.yaml`, under `dwnstr_task_validation`, modify the following columns:
![esm1-pretrain-custom-downstream-yaml-regression]({{"/assets/images/esm1-pretrain-custom-downstream-yaml-regression.jpg" | prepend: site.baseurl}})
- `task_class`: set to `SingleValuePredictionCallBack`
- `task_type`: set to `regression`
- `task_name`: change to whatever you want
- `dataset_path`: set to the folder that contains train/test folder. E.g. the `path/to/downstream` in the above example
- `dataset.train`, `dataset.test`: set to the file name. E.g. `x000` in the above example
- `sequence_column`: set to name of the column that contains the sequence. E.g. `sequence` in the above example
- `target_column`: set to name of the column that contains the target. E.g. `target` in the above example/
- `target_size`: set to `1`
- `mask_column`: comment this out. 


## Step 3. Train
1. In the Juptyer notebook terminal, run
```shell
cd /workspace/BioNeMo
```
2. Run the following command to start training. 
```shell
python examples/protein/esm1nv/pretrain.py \
  --config-path=conf \
  --config-name=pretrain_small \
  ++do_training=True \
  ++do_testing=False \
  ++trainer.devices=1 \
  ++model.micro_batch_size=128 \
  ++trainer.max_steps=100 \
  ++trainer.val_check_interval=10 \
  ++exp_manager.create_wandb_logger=False \
  ++exp_manager.checkpoint_callback_params.save_top_k=5
````

## Extras

### An example
In here we have the clean training data in `examples/tests/test_data/protein` and the validation-in-the-loop data in `examples/tests/test_data/protein/downstream` (for the 3-state structure prediction task).
We could simply run the following command to start training. 

```shell
python examples/protein/esm1nv/pretrain.py \
  --config-path=conf \
  --config-name=pretrain_small \
  ++do_training=True \
  ++do_testing=False \
  ++model.data.dataset_path=examples/tests/test_data/protein \
  ++model.data.dataset.train=x000 \
  ++model.data.dataset.val=x000 \
  ++model.data.dataset.test=x000 \
  ++trainer.devices=1 \
  ++model.micro_batch_size=128 \
  ++trainer.max_steps=100 \
  ++trainer.val_check_interval=10 \
  ++exp_manager.create_wandb_logger=False \
  ++exp_manager.checkpoint_callback_params.save_top_k=5 \
  ++model.dwnstr_task_validation.enabled=True \
  ++model.dwnstr_task_validation.dataset.dataset_path=examples/tests/test_data/protein/downstream
```