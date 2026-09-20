# Research Evidence Card: U-Mamba

**Study**  
Ma, Li, and Wang, *U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation* (arXiv:2401.04722v1, submitted 9 January 2024).

**Research question / contribution**  
U-Mamba integrates Mamba-based long-range dependency modeling with U-Net-style multi-scale convolutional features for biomedical image segmentation. Each building block places two residual blocks before a Mamba block; 3D features are flattened from `(B, C, H, W, D)` to `(B, L, C)`, with `L = H × W × D` (p. 5, §2.2).

**Architectural variants**

- `U-Mamba_Bot`: Mamba block only at the bottleneck.
- `U-Mamba_Enc`: Mamba blocks throughout the encoder.
- Decoder: residual blocks, transposed convolutions, and U-Net skip connections (p. 5, §2.2).

**Evaluation design**

- Implemented within nnU-Net to standardize preprocessing, augmentation, patch size, batch size, and dataset-specific configuration (pp. 7–8, §§3.2–3.3).
- Trained from scratch for 1000 epochs on one NVIDIA A100 GPU.
- Optimizer: stochastic gradient descent.
- Loss: unweighted sum of Dice loss and cross-entropy.
- Test-time augmentation disabled.
- Metrics: DSC and NSD for organ/instrument segmentation; F1 for cell instance segmentation (pp. 7–8).

**Reported evidence**

| Task | Best reported result in supplied text | Comparator / context |
|---|---:|---|
| 3D abdomen CT | `U-Mamba_Bot` DSC `0.8683 ± 0.0808` | `U-Mamba_Enc`: `0.8638 ± 0.0908`; nnU-Net: `0.8615 ± 0.0790` (Table 3) |
| 3D abdomen MRI | `U-Mamba_Enc` DSC `0.8501 ± 0.0732` | `U-Mamba_Bot`: `0.8453 ± 0.0673`; nnU-Net: `0.8309 ± 0.0769` (Table 3) |
| 2D abdomen MRI | `U-Mamba_Enc` DSC `0.7625 ± 0.1082` | Table 4 |
| Endoscopy instruments | `U-Mamba_Bot` DSC `0.6540 ± 0.3008`; NSD `0.6692 ± 0.3050` | Table 4 |
| Microscopy cells | `U-Mamba_Enc` F1 `0.5607 ± 0.2784` | Table 4 |

**Interpretation**  
The authors attribute gains to combining multi-scale local feature extraction with long-range dependency modeling (pp. 10–11). They suggest Transformer baselines may be disadvantaged by the one-GPU, from-scratch training setup and lack of large-scale pretraining.

**Limitations and implementation caveats**

- Results reflect a constrained training regime: one GPU, training from scratch, and no test-time augmentation.
- The paper proposes larger-scale training, stronger augmentation, imbalance-aware losses, and region-based training as future improvements.
- The narrative reports an endoscopy DSC of `0.6504`, whereas Table 4 reports `0.6540`; the table and narrative are inconsistent (p. 9, §3.4 vs. Table 4).
- The supplied evidence map does not include full experimental tables, dataset sizes, statistical testing, or the complete paper text; broader claims should therefore be treated as provisional.

**Code reference**  
The author repository documents Ubuntu 20.04, CUDA 11.8, Python 3.10, PyTorch 2.0.1, `mamba-ssm`, nnU-Net preprocessing, and separate trainers for the two variants: [bowang-lab/U-Mamba](https://github.com/bowang-lab/U-Mamba).