# Evidence Card: U-Mamba for Biomedical Image Segmentation

**Citation**  
Ma, Jun, Feifei Li, and Bo Wang. *U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation*. arXiv:2401.04722v1, submitted 9 January 2024.

**Research question**  
Can adding Mamba-based long-range dependency modeling to a U-Net-style architecture improve biomedical image segmentation?

**Intervention**  
U-Mamba inserts a Mamba block after two residual blocks. 3D features are flattened from `(B, C, H, W, D)` to `(B, L, C)`, where `L = H × W × D`.

- `U-Mamba_Bot`: Mamba block at the bottleneck only.
- `U-Mamba_Enc`: Mamba blocks throughout the encoder.
- Decoder: residual blocks, transposed convolutions, and U-Net skip connections.

**Evaluation design**

- Implemented within nnU-Net to control preprocessing, augmentation, patch size, batch size, and dataset-specific configuration.
- Networks trained from scratch for 1000 epochs on one NVIDIA A100 GPU.
- SGD with an unweighted Dice-plus-cross-entropy loss.
- Test-time augmentation disabled.
- Metrics: DSC and NSD for organ/instrument segmentation; F1 for cell instance segmentation.

**Reported results**

| Task | Best reported configuration | Metric |
|---|---|---:|
| 3D abdomen CT | U-Mamba_Bot | DSC 0.8683 ± 0.0808 |
| 3D abdomen MRI | U-Mamba_Enc | DSC 0.8501 ± 0.0732 |
| 2D abdomen MRI | U-Mamba_Enc | DSC 0.7625 ± 0.1082 |
| Endoscopy instruments | U-Mamba_Bot | DSC 0.6540 ± 0.3008; NSD 0.6692 ± 0.3050 |
| Microscopy cells | U-Mamba_Enc | F1 0.5607 ± 0.2784 |

For comparison, nnU-Net achieved DSC 0.8615 ± 0.0790 on 3D abdomen CT and 0.8309 ± 0.0769 on 3D abdomen MRI.

**Main finding**  
Across the reported tasks, the authors associate U-Mamba’s performance with combining multi-scale local features and long-range dependency modeling. The results suggest that the bottleneck-only and encoder-wide variants may be advantageous in different imaging settings.

**Limitations and interpretive cautions**

- All models were trained from scratch on a single GPU, which may disadvantage Transformer baselines that benefit from large-scale pretraining.
- The study disabled test-time augmentation and used a fixed training protocol, limiting conclusions about performance under alternative training regimes.
- The authors identify stronger augmentation, imbalance-aware losses, region-based training, and larger-scale training as future directions.
- The paper’s narrative reports an endoscopy DSC of `0.6504`, whereas Table 4 reports `0.6540`; the table value should be treated as the directly tabulated result.
- The source is a selective paraphrased evidence map, not the complete paper or a substitute for independent reproduction.

**Code reference**  
Author repository: [bowang-lab/U-Mamba](https://github.com/bowang-lab/U-Mamba). The repository documents Ubuntu 20.04, CUDA 11.8, Python 3.10, PyTorch 2.0.1, `mamba-ssm`, nnU-Net preprocessing, and separate trainers for the two U-Mamba variants.