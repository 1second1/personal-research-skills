# Evaluation

This directory contains provider-neutral evaluation contracts, fixtures, and
public case reports. Automated checks reject malformed or source-inconsistent
outputs; they do not claim to measure semantic research quality.

## What is implemented

- `rubrics/`: deterministic structure and marker checks for every public Skill;
- `schemas/run-record-v1.schema.json`: the original `1.0` model-run contract;
- `schemas/run-record-v1.1.schema.json`: the current contract, which can record
  provider controls while representing unavailable sampling parameters as `null`;
- `fixtures/run-record-demo/`: a non-model integrity fixture used by tests;
- `cases/`: reviewed examples and limited pilot reports;
- `PROTOCOL.md`: repeated-run and blinded human-review procedure.

Run the public checks through one CLI:

```bash
research-skills evaluate \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml \
  --source evals/fixtures/paper-reading-demo/source.md \
  --format json

research-skills validate --run evals/fixtures/run-record-demo/run.yaml
```

Evaluation JSON is versioned and always reports
`"semantic_quality": "not_evaluated"`. This prevents a deterministic gate from
being presented as a factual-quality score.

## Run records and blind review

Every real run must preserve the exact input, composed context, raw output,
model identity, generation settings, repository revision, and SHA-256 digests.
Paths are repository-relative and may not escape the evaluation root.
Use schema `1.1` when a runtime does not expose `temperature` or
`max_output_tokens`; record those values as `null` rather than inventing a
setting. `reasoning_effort` and `verbosity` are optional because not every
provider exposes them. Existing `1.0` records remain valid.

Prepare a review bundle only after at least two records validate:

```bash
research-skills blind evals/local/runs/run-a.yaml evals/local/runs/run-b.yaml \
  --seed 20260919 --output evals/local/review-export
```

The public manifest contains only opaque IDs, task IDs, and candidate paths.
The random seed and condition mapping stay in `private/review-key.json`; do not
give that file to reviewers before scoring. Candidate prose may still reveal a
condition indirectly, so report this as best-effort blinding rather than proof
of perfect blindness.

## Metrics

| Metric | Meaning |
|---|---|
| factual-consistency | 是否忠实于论文、代码或实验记录 |
| evidence-coverage | 关键结论是否带可追溯来源 |
| inquiry-pattern-coverage | 是否覆盖必要的 What / Why / Assumption / Boundary 判断 |
| method-consistency | 不同 Skill 是否继承同一方法论 Profile |
| actionability | 输出是否能形成下一步研究任务 |

## Baseline tasks

Each Skill should eventually include at least one baseline task. Recommended coverage:

1. Extracting paper methods and assumptions.
2. Explaining formula variables.
3. Mapping paper claims to repository entry points.
4. Designing medical image segmentation experiments.
5. Reviewing training-log anomalies.

## Evaluation rules

Keep the input, output, score, and failure reason for every evaluation. Re-run affected regression tasks after any methodology or Skill change.

Public case reports live under `evals/cases/`. They must state model settings,
sample count, reviewer blinding, known transport or source limitations, and
negative findings. Do not publish source material without redistribution rights.
