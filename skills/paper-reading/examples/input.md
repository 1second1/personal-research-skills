# LiteSeg synthetic research note

LiteSeg is a lightweight encoder-decoder network for 2D medical image segmentation.
It replaces standard convolution blocks with depthwise separable convolutions and adds a
boundary-aware loss. On Dataset-A, LiteSeg reports Dice 0.842 versus 0.831 for U-Net,
with 2.1M versus 7.8M parameters. Experiments use 256×256 images and a fixed 80/20
train-validation split. The note does not report inference latency, repeated-run variance,
or external-dataset results.

Research context: decide whether LiteSeg is a fair lightweight baseline for a future
comparison with a Vision Mamba segmentation model.
