# Evaluation protocol

## Automated gate

Install dependencies with `python -m pip install -e .`, then run:

```bash
python -m unittest discover -s tests -v
research-skills validate
research-skills evaluate evals/fixtures/paper-reading-demo/evidence-card.md evals/fixtures/paper-reading-demo/rubric.yaml --source evals/fixtures/paper-reading-demo/source.md --format json
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

The general paper-reading rubric does not force conflict, inference, or timing
topics when they are absent. Case-specific semantic requirements remain in case
rubrics. The manuscript-audit rubric checks its five sections only: no-finding
responses are permitted, and issue-card correctness needs evidence review.

## Author manuscript audit and revision pilot

The [executed synthetic teaching case](cases/manuscript-audit-demo/README.md)
includes originals, revisions, raw predictions, failed/passing checks and logs.
Its reports are authored references, not independently generated model answers.
The [prospective three-arm protocol](cases/manuscript-audit-pilot/preregistration.md)
uses separate sealed materials and a user-approved model/budget. It does not
authorize generation or reuse old uncertainty-v2 experiment materials.

Run-record v1.2 adds `strong_prompt` and `peer_review` conditions, a required
hashed `trace` artifact, and `measurements` for elapsed seconds, actual model
requests, input/output tokens, cost, currency and cost basis. Unknowns are null;
cost basis is `unavailable`, `reported` or `estimated`. Trace preserves receipts
and failures. Native v1.0/v1.1 condition sets and required fields are unchanged.
The blind exporter still exports reports only; traces/usage remain outside the
semantic-review bundle. Separately verify execution claims and disclose any
unblinding. Validation checks integrity/types, not whether a reported execution
or bill is true.

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

## Prospective uncertainty diagnostics

Apply this diagnostic to newly authorized evaluations only. It does not rescore
or rewrite the historical nine-run comparison, alter frozen private evaluation
materials, promote uncertainty-v2, or authorize the paused 36-run study.
Freeze the diagnostic, source scope and decision rules before generating outputs.

Report these findings separately from the five dimension scores:

| Diagnostic | Failure criterion | Correct behavior |
|---|---|---|
| Unsupported SD attribution | Within the supplied source scope, `±` is undefined, but the answer asserts or uses standard deviation as its established meaning | Preserve the value and state that the meaning is unspecified in the supplied material; distinguish any hypothesis from a source fact |
| Unnecessary withholding of a defined meaning | The supplied source explicitly defines `±` as SD, the task requires interpreting it, but the answer denies that definition or refuses to identify it without a source-grounded reason | Attribute SD to the source and preserve its scope, such as five folds rather than five independent runs |

Acknowledging that a reported SD has not been independently reproduced is not
unnecessary withholding. A task that does not require interpreting the notation
is not penalized merely for omitting that interpretation. Missing access to a
required source or a genuine conflict in definitions is unresolved evidence,
not permission to guess. Absence of a definition in an excerpt does not establish
absence throughout the paper or its external materials.

For each response, record `present`, `absent`, `not_applicable` or `unresolved`
for each diagnostic, with the exact output quote, source location and rationale.
Report denominators, individual failures and unresolved cases; do not hide a
failure behind a pooled score. Unsupported SD attribution fails the uncertainty
interpretation diagnostic regardless of the general quality score. Unnecessary
withholding fails the defined-meaning diagnostic. Neither diagnostic replaces
the other factual and critical-failure checks.

Two reviewers assess disputed claims before condition labels are revealed.
Preserve both judgments; an adjudicator resolves disagreements against the
frozen definitions and cited source. If independent adjudication is unavailable,
keep the item unresolved and withhold any success claim that depends on it.
Do not revise labels, thresholds or source scope after learning conditions;
a necessary method change requires a separately identified prospective revision.

## Small harness acceptance tasks

For instruction or workflow changes, start with one simple question, one small
file edit and one fresh-session continuation of an existing handoff. Save the
exact prompts, instruction version/hash, actual outputs, artifacts and execution
traces. Record unnecessary confirmation, artifact discoverability, accurate
completion/publication status and separation of historical from current checks.
A new session reading a prepared handoff tests continuation from that record;
it does not establish recovery from arbitrary interruptions or context loss.

Keep environment/setup failures distinct from agent behavior, retain failed
attempts, and do not switch models silently to obtain a passing result. These
three tasks are acceptance observations, not a causal comparison or evidence
of general reliability. Inspect Skill triggers only when observed steps suggest
avoidable overhead. This acceptance work does not resume the research study.

The repository includes a curated real-paper reference case and a
[nine-run baseline / Skill / profile comparison](cases/u-mamba-real-paper/comparison-2026-09-20/README.md)
on its source map. That comparison used one semantic reviewer and best-effort
blinding; independent review remains pending. Store future run artifacts
outside the public tree until reviewed for private data.
