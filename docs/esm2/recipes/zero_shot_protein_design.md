---
layout: default
title: 1. Zero-shot Mutant Design
parent: 4. Recipes
grand_parent: ESM2
nav_order: 1
---
{: .warning}
This site has been deprecated. Please visit the new [demo GitBook site](https://xinyu-dev.gitbook.io/bionemo-gitbook). 

# Zero-shot Mutant Design

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}


## Prerequisites

{: .highlight }
{% include template/service_prerequisites.md %}

## Background
Given a sequence, we embed it with ESM2nv. The logits returned by the model represent the probability prediction for each token at each position. The probabilty matrix can then be used for zero-shot protein and antibody designs as described by [papers like this](https://www.nature.com/articles/s41587-023-01763-2), which utilizes ESM models to design point mutations to improve the potency and breadth of SARS-Cov-2 antibodies. 

Below is a screenshot using lysozyme as an example. The original sequence is shown above, the ESM2nv predicted sequence is shown below. Alignment suggests 2 positions for mutatant design. 
![image]({{ "/assets/images/notebook_lysozyme_zero_shot.png" | prepend: site.baseurl }})

## Steps
Refer to [this notebook]({{ "/notebooks/esm2nv/zero_shot_protein_design.ipynb" | prepend: 'https://github.com/xinyu-dev/bionemo-demo/blob/main' }})