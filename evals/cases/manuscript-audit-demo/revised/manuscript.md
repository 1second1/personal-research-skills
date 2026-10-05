# Normalized nearest neighbors on repeated synthetic patient signals

**Synthetic teaching manuscript, revised after executed checks.** The IDs and numerical signals are generated, not patient records. This is not medical evidence or an independent model evaluation.

## Abstract

We evaluate a normalized nearest-neighbor classifier on 48 signals from 12 synthetic patients. Under one fixed patient-disjoint split, 4 of 16 test signals are classified correctly. This documents the complete model's behavior on this generated dataset and does not establish reliable generalization to real or other unseen patients.

## Methods

Four signals share each generated patient's identity-like feature pattern and binary label. Patients P003, P006, P009, and P012 are held out entirely; the other eight patients form the training set. The classifier uses both numerical features, population-standard-deviation scaling fitted on the 32 training samples, Euclidean distance, and a sample-ID tie breaker. No GPU, optimization loop, or model service is used.

## Results

| Metric | Value |
|---|---|
| Test accuracy | 0.250000 |

The number is the fraction of correctly classified held-out samples. It agrees with saved predictions: 4 correct among 16 evaluated samples.

## Component interpretation

We report one complete-model evaluation and no with/without-normalization or joint-component experiment. These results do not isolate normalization's contribution or establish that it is necessary. The original component-attribution claim has been removed.

## Limitations

One fixed split is reported, with no uncertainty estimate. The signals are synthetic and no real-patient experiment was conducted. The original sample-level split produced 12/12 correct predictions while overlapping all 12 patients. The revised split uses a different test set; the difference between 1.0 and 0.25 is not a controlled estimate of the causal effect of overlap. Repaired partitioning and consistent reporting do not establish a useful classifier or a reproducible scientific result across datasets.
