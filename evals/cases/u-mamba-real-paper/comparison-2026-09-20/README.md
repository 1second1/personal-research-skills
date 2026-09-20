# PR-REAL-01 controlled comparison

This is the first repeated model comparison on the source-verified U-Mamba
case. It compares the same task and input under three contexts:

1. baseline task only;
2. paper-reading Skill contract;
3. paper-reading Skill plus the reference Reasoning DNA profile.

It is a small pilot, not evidence that the reported ordering generalizes to
other models, papers, Skills, or reviewers.

## Setup

| Setting | Value |
|---|---|
| Runtime | OpenAI Codex CLI 0.145.0 |
| Model | `gpt-5.6-luna` provider-managed alias, accessed 2026-09-20 |
| Reasoning effort | `low` |
| Verbosity | `low` |
| Temperature / seed / max output tokens | Not exposed by the runtime; recorded as `null` |
| Tools | Disabled by instruction; no tool calls observed |
| Repetitions | 3 per condition, each in a fresh ephemeral session |
| Input | [`source-map.md`](../source-map.md) |
| Blind-review seed | `20260920` |

All nine outputs have v1.1 run records with SHA-256 digests. The condition key
was not opened until the scores were saved. The same agent orchestrated and
scored the experiment, so this is a single-agent semantic review rather than an
independent human review. Candidate language and headings could also reveal the
condition; blinding was therefore best-effort.

## Rubric

Each output received 0–2 points for factual consistency, evidence coverage,
fact/inference separation, boundaries, and actionability. Fabricated evidence,
metrics, or experiments would be a critical failure regardless of total score.

## Results

| Condition | Run scores | Mean | Range | Critical failures |
|---|---:|---:|---:|---:|
| Baseline | 6, 8, 6 | 6.67 | 6–8 | 0 |
| Skill only | 10, 10, 9 | 9.67 | 9–10 | 0 |
| Skill + profile | 9, 9, 9 | 9.00 | 9–9 | 0 |

| Dimension mean | Baseline | Skill only | Skill + profile |
|---|---:|---:|---:|
| Factual consistency | 2.00 | 1.67 | 1.00 |
| Evidence coverage | 1.33 | 2.00 | 2.00 |
| Fact/inference separation | 1.33 | 2.00 | 2.00 |
| Boundaries | 2.00 | 2.00 | 2.00 |
| Actionability | 0.00 | 2.00 | 2.00 |

The Skill contract improved traceability, explicit reasoning boundaries, and
next-step quality in this setup. The profile did **not** improve on Skill-only.
All three profile runs called the undefined `±` values “standard deviations”
before acknowledging that the supplied source did not define them. One
Skill-only run made the same mistake. This is a useful negative result: more
methodology text did not guarantee better factual discipline.

The deterministic structural/source gate passed `0/6` Skill and profile
outputs. It rejected exact-marker omissions, source-label spelling differences,
incomplete per-line citations, and—in one run—a correctly calculated `0.0068`
difference because that derived number did not appear verbatim in the source.
These failures are retained in [`automated/`](automated/) rather than edited out
of the raw outputs. They show that high semantic scores and strict contract
compliance are different measurements; the gate still reports semantic quality
as `not_evaluated`.

## Limits

- One paper case, one provider-managed model alias, and three repetitions per
  condition are insufficient for a general claim.
- There was one semantic reviewer and no independent adjudication.
- Visible style differences made strict blinding impossible.
- The 0–2 rubric has a ceiling effect and does not measure every aspect of
  research quality.
- The test evaluates analysis of a supplied evidence map, not PDF extraction,
  code reproduction, or the paper's scientific validity.

The next credible step is an independent second review followed by a narrowly
scoped feedback proposal: never assign a statistical meaning to `±` unless the
source defines it.

## Artifacts

- [`results.json`](results.json): machine-readable aggregate and per-run scores;
- [`review-scores.yaml`](review-scores.yaml): review notes and evidence quotes;
- [`automated/`](automated/): deterministic failure reports for the six
  Skill/Profile outputs;
- [`contexts/`](contexts/): exact prompts sent for each condition;
- [`outputs/`](outputs/): all nine raw final responses;
- [`runs/`](runs/): validated v1.1 records and artifact digests.

Validate the repository and every published record with:

```bash
research-skills validate
python -m unittest discover -s tests -v
```
