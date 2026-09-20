# Research Evidence Card: U-Mamba

**Citation**  
Ma, Jun, Feifei Li, and Bo Wang. *U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation*. arXiv:2401.04722v1, submitted 9 January 2024.

**Research question**  
Can adding Mamba-based long-range dependency modeling to a U-Net-style biomedical segmentation architecture improve performance across 2D and 3D medical-image tasks?

**Method and architecture**

- U-Mamba blocks place two residual blocks before a Mamba block.
- Features `(B, C, H, W, D)` are flattened to `(B, L, C)`, with `L = H × W × D`, before Mamba processing.
- `U-Mamba_Bot` uses the block only at the bottleneck; `U-Mamba_Enc` uses it throughout the encoder.
- The decoder uses residual blocks, transposed convolutions, and U-Net-style skip connections.
- Implemented within nnU-Net to control preprocessing, augmentation, patch size, batch size, and dataset-specific configuration.
- Models were trained from scratch for 1000 epochs using SGD and an unweighted Dice-plus-cross-entropy loss. Test-time augmentation was disabled.

**Evidence of performance**

| Task | Reported result |
|---|---:|
| 3D abdomen CT — U-Mamba_Bot DSC | 0.8683 ± 0.0808 |
| 3D abdomen CT — U-Mamba_Enc DSC | 0.8638 ± 0.0908 |
| 3D abdomen CT — nnU-Net DSC | 0.8615 ± 0.0790 |
| 3D abdomen MRI — U-Mamba_Enc DSC | 0.8501 ± 0.0732 |
| 3D abdomen MRI — U-Mamba_Bot DSC | 0.8453 ± 0.0673 |
| 3D abdomen MRI — nnU-Net DSC | 0.8309 ± 0.0769 |
| 2D abdomen MRI — U-Mamba_Enc DSC | 0.7625 ± 0.1082 |
| Endoscopy instruments — U-Mamba_Bot DSC | 0.6540 ± 0.3008 |
| Endoscopy instruments — U-Mamba_Bot NSD | 0.6692 ± 0.3050 |
| Microscopy cells — U-Mamba_Enc F1 | 0.5607 ± 0.2784 |

**Main interpretation**

The reported results support the authors’ claim that combining multi-scale local feature extraction with long-range dependency modeling can improve biomedical image segmentation relative to nnU-Net in the cited 3D comparisons, particularly for abdomen MRI. Performance varies by task and by placement of the Mamba block; encoder-wide integration is not uniformly superior to bottleneck-only integration.

**Limitations and caveats**

- The supplied evidence is a selective paraphrased source map, not the full paper or PDF.
- All models were trained from scratch on one NVIDIA A100 GPU, which may disadvantage Transformer baselines lacking large-scale pretraining.
- The authors identify stronger augmentation, imbalance-aware losses, region-based training, larger-scale training, and extension to classification or detection as future work.
- The narrative reports an endoscopy DSC of `0.6504`, conflicting with Table 4’s `0.6540`; the table value should be treated as the directly tabulated result.
- The original project webpage was unavailable when checked; the author GitHub repository is used as the code reference.