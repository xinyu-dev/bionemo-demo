---
layout: default
title: Zero-shot Protein Design
parent: ESM2
grand_parent: Recipes
---
# Zero-shot Protein Design

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Prerequisites
{% include template/service_prerequisites.md %}

## Background
Given a sequence, we embed it with ESM2nv. The logits returned by the model represent the probability prediction for each token at each position. The probabilty matrix can then be used for zero-shot protein and antibody designs as described by [papers like this](https://www.nature.com/articles/s41587-023-01763-2), which utilizes ESM models to design point mutations to improve the potency and breadth of SARS-Cov-2 antibodies. 

Below is a screenshot using lysozyme as an example. The original sequence is shown above, the ESM2nv predicted sequence is shown below. Alignment suggests 2 positions for mutatant design. 
![image]({{ "/assets/images/notebook_lysozyme_zero_shot.png" | prepend: site.baseurl }})

## Steps
Refer to [this notebook]({{ "/notebooks/esm2nv/zero_shot_protein_design.ipynb" | prepend: 'https://github.com/xinyu-dev/bionemo-demo/blob/main' }})