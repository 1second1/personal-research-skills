## Controlled execution rules

Do not use tools, web access, shell commands, or files. Analyze only the
supplied context. Return only the final Markdown answer, without meta-commentary
or any mention of the experimental condition.

## Task

Produce an evidence-grounded research evidence card from supplied paper text.

## Skill Contract

```json
{
  "name": "paper-reading",
  "version": "0.2.0",
  "purpose": "Produce an evidence-grounded research evidence card from supplied paper text.",
  "inputs": [
    {
      "name": "paper_text",
      "required": true,
      "type": "markdown_or_text"
    },
    {
      "name": "research_context",
      "required": false,
      "type": "markdown_or_text"
    },
    {
      "name": "source_locations",
      "required": false,
      "type": "mapping"
    }
  ],
  "outputs": [
    "problem",
    "evidence",
    "conflicts_and_anomalies",
    "inferences",
    "assumptions",
    "boundaries",
    "connections",
    "next_actions"
  ],
  "constraints": [
    "Do not present inferences as source facts.",
    "Do not silently reconcile conflicting source claims or values.",
    "Do not invent page, section, or experiment locations.",
    "Mark unsupported conclusions and information gaps explicitly.",
    "Make next_actions falsifiable and measurable."
  ],
  "evaluation": [
    "factual_consistency",
    "evidence_coverage",
    "conflict_detection",
    "fact_inference_separation",
    "boundary_analysis",
    "actionability"
  ]
}
```

## Skill Instructions

---
name: paper-reading
description: Use when analyzing a research paper or excerpt whose claims, evidence, numerical results, limitations, or internal consistency must be assessed.
---

# Paper Reading

Produce a research evidence card, not a persuasive summary. Preserve the boundary between what the source states, what follows from it, and what should be tested next.

## Input

Accept `paper_text`. Optionally accept `research_context` and `source_locations`.

If source locations are unavailable, write `location unavailable`; never invent page or section numbers.

## Output

Use these sections in order:

1. `## Problem`
2. `## Evidence`
3. `## Conflicts and Anomalies`
4. `## Inferences`
5. `## Assumptions`
6. `## Boundaries`
7. `## Connections`
8. `## Next Actions`

## Procedure

1. State the research problem in one sentence.
2. Extract only direct claims into **Evidence**. Attach `[Source: ...]` to each material claim.
3. Compare repeated claims, table values, captions, and prose. If they disagree, write `Conflict:` with every incompatible value and source location. Do not silently reconcile them or choose the convenient value. If none are found, limit that statement to the checked material.
4. Prefix every non-direct conclusion with `Inference:`.
5. Identify assumptions needed for the reported result to hold.
6. State what the source does not establish, including missing baselines, missing uncertainty, missing external validation, or missing implementation detail.
7. Connect the method to `research_context` only when the context supplies a concrete comparison or decision.
8. End with numbered, falsifiable actions that specify what evidence would change the current conclusion.

## Quick Reference

| Write this | When |
|---|---|
| `[Source: section or location]` | Directly supported by the supplied text |
| `Conflict:` | Two checked source claims or values are incompatible |
| `Inference:` | Derived from one or more source facts |
| `Unsupported:` | The source lacks evidence for the claim |
| `Open question:` | A decision needs information absent from the text |

## Common Mistakes

- Do not convert a higher metric into a claim of general superiority.
- Do not treat fewer parameters as measured lower latency.
- Do not call a comparison statistically reliable when variance or repeated runs are absent.
- Do not resolve a table/prose mismatch by silently selecting one value.
- Do not use `research_context` to overwrite or embellish the source.
- Do not give vague actions such as “run more experiments”; name the comparison, metric, and failure condition.

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
