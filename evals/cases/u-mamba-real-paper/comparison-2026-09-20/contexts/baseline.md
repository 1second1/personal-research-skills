## Controlled execution rules

Do not use tools, web access, shell commands, or files. Analyze only the
supplied context. Return only the final Markdown answer, without meta-commentary
or any mention of the experimental condition.

## Task

Produce an evidence-grounded research evidence card from supplied paper text.

## Input Document

# U-Mamba source map

This is a selective, paraphrased evidence map for arXiv:2401.04722v1. It is not a replacement for the paper and intentionally omits the PDF and full-text extracts.

## Paper metadata

- Title: *U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation*.
- Authors: Jun Ma, Feifei Li, and Bo Wang.
- Version checked: arXiv v1, submitted 9 January 2024; the PDF contains 17 pages.

## p. 5, Section 2.2

- Each U-Mamba building block places two residual blocks before a Mamba block.
- Features shaped `(B, C, H, W, D)` are flattened to `(B, L, C)`, where `L = H x W x D`, before entering the Mamba block.
- `U-Mamba_Bot` applies the U-Mamba block only at the bottleneck; `U-Mamba_Enc` uses it throughout the encoder.
- The decoder uses residual blocks and transposed convolutions, with U-Net-style skip connections.

## pp. 7-8, Sections 3.2-3.3

- The implementation is built in the nnU-Net framework so preprocessing, augmentation, patch size, batch size, and dataset-specific configuration can remain controlled across architectures.
- U-Mamba uses stochastic gradient descent with an unweighted sum of Dice loss and cross-entropy.
- Test-time augmentation is disabled for all reported experiments.
- All compared networks are trained from scratch for 1000 epochs on one NVIDIA A100 GPU using the same batch size for each dataset setting.
- The paper evaluates organ and instrument segmentation with DSC and NSD, and cell instance segmentation with F1.

## p. 8, Table 3

- For 3D abdomen CT, `U-Mamba_Bot` reports DSC `0.8683 +/- 0.0808`; `U-Mamba_Enc` reports `0.8638 +/- 0.0908`; nnU-Net reports `0.8615 +/- 0.0790`.
- For 3D abdomen MRI, `U-Mamba_Enc` reports DSC `0.8501 +/- 0.0732`; `U-Mamba_Bot` reports `0.8453 +/- 0.0673`; nnU-Net reports `0.8309 +/- 0.0769`.

## p. 9, Table 4

- For 2D abdomen MRI, `U-Mamba_Enc` reports DSC `0.7625 +/- 0.1082`.
- For endoscopy instrument segmentation, `U-Mamba_Bot` reports DSC `0.6540 +/- 0.3008` and NSD `0.6692 +/- 0.3050`.
- For microscopy cell segmentation, `U-Mamba_Enc` reports F1 `0.5607 +/- 0.2784`.

## p. 9, Section 3.4

- The narrative says the best average results across the three 2D tasks are DSC `0.7625`, DSC `0.6504`, and F1 `0.5607`, respectively.
- The narrative's endoscopy value `0.6504` conflicts with Table 4's `0.6540`.

## pp. 10-11, Discussion

- The authors attribute the reported gains to combining multi-scale local features with long-range dependency modeling.
- They also state possible explanations for Transformer baselines underperforming, including the one-GPU, train-from-scratch setup and the absence of large-scale pretraining.
- The discussion proposes larger-scale training, stronger augmentation, imbalance-aware losses, region-based training, and extension to classification or detection as future work.

## Official code repository

- The author repository documents Ubuntu 20.04, CUDA 11.8, Python 3.10, PyTorch 2.0.1, `mamba-ssm`, nnU-Net preprocessing, and separate trainers for `U-Mamba_Bot` and `U-Mamba_Enc`.
- The paper's original `wanglab.ai/u-mamba.html` link resolved to a parked domain when checked on 19 September 2026, so this case uses the author repository at `https://github.com/bowang-lab/U-Mamba` as the code reference.
