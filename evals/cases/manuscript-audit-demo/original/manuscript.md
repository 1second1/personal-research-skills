# Normalized nearest neighbors on repeated synthetic patient signals

**Synthetic teaching manuscript with deliberately planted issues.** The IDs and numerical signals are generated, not patient records. This is not medical evidence or an independent model evaluation.

## Abstract

We evaluate a normalized nearest-neighbor classifier on 48 signals from 12 synthetic patients. Our result demonstrates generalization to previously unseen patients. We attribute the improvement to normalization.

## Methods

Four signals share each generated patient's identity-like feature pattern and binary label. The final sample of each patient is held out; the other three are training samples. The classifier uses both numerical features, population-standard-deviation scaling fitted on training samples, Euclidean distance, and a sample-ID tie breaker. No GPU, optimization loop, or model service is used.

## Results

| Metric | Value |
|---|---|
| Test accuracy | 0.930000 |

The number is the fraction of correctly classified held-out samples.

## Component interpretation

The normalization module causes the accuracy gain and is necessary for this performance. We report one complete-model evaluation; no with/without-normalization or joint-component experiment is included.

## Limitations

One fixed split is reported, with no uncertainty estimate. The signals are synthetic. No real-patient experiment was conducted.
