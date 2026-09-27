# Argo Recovery Economic Analysis

This repository contains the code and datasets used to perform the economic analysis of Argo float recovery presented in the associated scientific paper.

The analysis evaluates the economic value of recovering and redeploying Argo floats under uncertainty in recovery costs and recovery success rates. Five float configurations are considered:

- Core
- Deep
- BGC (O₂)
- BGC (O₂, FLBB)
- BGC (+3)

The repository includes the raw datasets used in the analysis, the Python code implementing the sensitivity and Monte Carlo analyses, and the figures generated for the study.

## Repository structure

```text
argo-recovery-economic-analysis/
├── data/
├── code/
├── figures/
└── supplementary/

Reproducibility
The Python scripts can be used to reproduce the sensitivity and Monte Carlo analyses described in the paper and to generate the corresponding figures. The analysis is designed to run without local file paths, allowing the code to be reproduced on other systems.
Associated publication
[Full title of the paper]
Authors: Alberto González Santana et al.
The manuscript has been submitted as a preprint and is currently undergoing moderation.
License
The code in this repository is released under the MIT License.
