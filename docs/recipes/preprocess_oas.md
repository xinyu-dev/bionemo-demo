---
layout: default
title: Preprocess OAS
nav_order: 3
parent: Recipes
---
# Preprocess OAS

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Prerequisites
Complete [Step 1 in BiNeMo Framework]({{ "/docs/framework/1_launch_container" | prepend: site.baseurl }})

## Steps

### Step 1. Download OAS data
1. Go to [OAS](https://opig.stats.ox.ac.uk/webapps/oas/oas_paired/), do not put in any search attributes, just click on Search button. 
2. Download the shell script. 
![oas-download]({{ "/assets/images/oas_download.jpg" | prepend: site.baseurl }})
3. Rename it to `oas_paired_subset_download.sh`. Upload to `/workspace/bionemo/bionemo/data/preprocess/protein` folder. 
4. copy this [oas_preprocess.py]() to `/workspace/bionemo/bionemo/data/preprocess/protein` folder. 