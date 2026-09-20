# U-Mamba real-paper case

`PR-REAL-01` is the first source-verified paper-reading case in this repository. It uses [U-Mamba: Enhancing Long-range Dependency for Biomedical Image Segmentation](https://arxiv.org/abs/2401.04722v1) because the architecture and experiments align with medical image segmentation and expose both methodological strengths and a concrete reporting inconsistency.

This directory contains a curated reference answer and a separate repeated
model comparison. The reference answer is not a model output. The comparison is
a small pilot and does not establish that one condition or model is generally
superior.

## What was verified

- The arXiv v1 PDF was downloaded twice from the official PDF URL. Both copies were 13,369,554 bytes and produced the same SHA-256 recorded in `case.yaml`; the server `Content-Length` matched the local size.
- Text extraction was used for navigation. PDF pages 8 and 9 were rendered at 220 DPI and visually checked against Tables 3 and 4 and the surrounding prose.
- The author repository was verified at [bowang-lab/U-Mamba](https://github.com/bowang-lab/U-Mamba). The project URL printed in the paper resolved to a parked domain on the access date, so it was not used as evidence for the current code instructions.
- The PDF is not redistributed. `source-map.md` contains selective paraphrases and result values with page-level locations.

## Negative finding retained

Table 4 reports endoscopy DSC `0.6540` for `U-Mamba_Bot`, while Section 3.4 reports `0.6504` as the best average DSC for that task. The reference card records this as a source conflict rather than silently choosing one value.

## Run the deterministic check

```bash
research-skills evaluate \
  evals/cases/u-mamba-real-paper/expected-output.md \
  evals/cases/u-mamba-real-paper/rubric.yaml \
  --source evals/cases/u-mamba-real-paper/source-map.md \
  --format json
```

The check validates required structure, citations, and numeric presence in the curated source map. It does not judge whether the scientific interpretation is correct.

## Scope limits

- Selected pages and claims were checked; this is not an exhaustive audit of all 17 pages.
- No training run or source-code execution was performed.
- A three-condition, three-repetition comparison is available in
  [`comparison-2026-09-20/`](comparison-2026-09-20/README.md). Skill-only
  outscored the baseline in that setup; the profile did not improve on
  Skill-only. It used one semantic reviewer and still needs independent review.
- The reported metrics are paper claims, not independently reproduced results.
