# Evaluation protocol

## Automated gate

Install dependencies with `python -m pip install -e .`, then run:

```bash
python -m unittest discover -s tests -v
research-skills validate
research-skills evaluate evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml --source evals/fixtures/paper-reading-demo/source.md --format json
research-skills evaluate evals/cases/u-mamba-real-paper/expected-output.md evals/cases/u-mamba-real-paper/rubric.yaml --source evals/cases/u-mamba-real-paper/source-map.md --format json
research-skills evaluate skills/research-question/examples/expected-output.md evals/rubrics/research-question.yaml --format json
research-skills evaluate skills/argument-analysis/examples/expected-output.md evals/rubrics/argument-analysis.yaml --format json
research-skills validate --run evals/fixtures/run-record-demo/run.yaml
```

Exit codes: 0 = checks passed, 1 = candidate failed checks, 2 = invalid input.
The versioned JSON report always labels semantic quality as `not_evaluated`.
Source labels must exactly match headings in the supplied Markdown source.
Each Evidence claim must occupy one line and contain a complete citation.
Rubrics may use `claim_headings` to apply the same citation and numeric checks to
other factual sections. The paper-reading rubric applies them to both Evidence
and Conflicts and Anomalies.
Numeric checks flag numbers absent from the source; they cannot detect swapped
metric attribution, changed units, reversed comparisons or unsupported prose.
These checks are a rejection filter, not a factual correctness score.

Regression tests include valid evidence, invented citation labels, invented
numbers, conflict claims with bad citations or numbers, empty rubrics, empty
sections, headings hidden inside prose, and the U-Mamba source-verified case.

## Controlled model comparison

Generate each condition for the same input:

```bash
research-skills compose paper-reading skills/paper-reading/examples/input.md --mode baseline
research-skills compose paper-reading skills/paper-reading/examples/input.md --mode skill
research-skills compose paper-reading skills/paper-reading/examples/input.md --mode profile
```

Baseline receives the task purpose and input. Skill adds its complete contract and
instructions. Profile additionally adds the personal methodology. The baseline
is not required to adopt the Skill's output headings: score its meaning, not format.
Use the same model version, sampling parameters, token budget and tools in all
conditions. Start a fresh conversation per run. Save the exact context and raw
output, model/version, parameters, condition, source, task ID and run ID.
Run three repetitions per condition. Store each run with
`evals/schemas/run-record-v1.1.schema.json`; the input, context, and raw output
digests must validate before review. Randomize presentation order and hide the
condition from reviewers. Do not reuse the authored example as a model output.
If the runtime does not expose a generation control, record `null`; never infer
or invent a temperature, seed, or token limit. The original `1.0` schema remains
available for existing records whose numeric settings are known.

Create the reviewer bundle with a fixed seed:

```bash
research-skills blind evals/local/runs/run-a.yaml evals/local/runs/run-b.yaml \
  --seed 20260919 --output evals/local/review-export
```

Give reviewers `review-manifest.json` and `candidates/`, but not
`private/review-key.json`. Keep the key for adjudication and reproducibility.
Because output wording may identify a condition, describe this as best-effort
blinding and record any suspected unblinding.

Start with these fixed tasks:

| Task | Source/input | Required review |
|---|---|---|
| PR-01 | paper-reading/examples/input.md | Correctly attribute Dice values; do not infer measured latency from parameter count |
| PR-02 | PR-01 plus question: Does this establish external-dataset superiority? | Answer that external validation is absent |
| PR-03 | PR-01 plus question: Is the improvement statistically significant? | No significance claim without repeated-run evidence |
| PR-REAL-01 | `evals/cases/u-mamba-real-paper/source-map.md` | Preserve the 0.6540 / 0.6504 conflict with both source locations; do not present paper claims as reproduced results |
| RQ-01 | research-question/examples/input.md | Observable hypothesis, controlled variables and a falsification condition |

Paths without an `evals/` prefix are under `skills/`. These tasks constitute a
small pilot only; do not generalize results to research tasks as a whole.

## Human quality review

Score each dimension 0, 1 or 2, with an output quote and source location:

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Factual consistency | Invented/contradicted material claim | Ambiguous attribution | All material factual claims supported |
| Evidence coverage | Main claim untraceable | Partial traceability | Every main claim linked to supplied evidence |
| Fact/inference separation | Inference stated as fact | Inconsistent labels | Clear separation throughout |
| Boundaries | Unsupported generalization | Some limits named | Relevant limits and missing evidence explicit |
| Actionability | No executable next step | Action without decision criterion | Artifact, metric and stopping/falsification criterion |

Any fabricated citation, metric or experiment is a critical failure regardless of
total score. Unsupported latency and significance claims are critical failures
for PR-01/03. Review semantic meaning: repeating rubric words earns no credit.
Use a second reviewer for disputed claims; retain disagreements and adjudication.
Report per-task scores, critical failures and variation across repetitions, not
just a pooled average. Do not change thresholds after seeing condition labels.

The repository includes a curated real-paper reference case and a
[nine-run baseline / Skill / profile comparison](cases/u-mamba-real-paper/comparison-2026-09-20/README.md)
on its source map. That comparison used one semantic reviewer and best-effort
blinding; independent review remains pending. Store future run artifacts
outside the public tree until reviewed for private data.
