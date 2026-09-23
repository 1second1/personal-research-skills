# What a failed Reasoning DNA experiment taught us

> A nine-run U-Mamba paper-reading pilot improved with an explicit Skill
> contract, but not with an additional personal reasoning profile. The failure
> is more useful than a polished success claim.

## Result at a glance

| Condition | Runs | Mean score | Range | Critical failures |
|---|---:|---:|---:|---:|
| Baseline task | 3 | 6.67 / 10 | 6–8 | 0 |
| `paper-reading` Skill | 3 | 9.67 / 10 | 9–10 | 0 |
| Skill + Reasoning DNA | 3 | 9.00 / 10 | 9–9 | 0 |

In this setup, the Skill contract improved evidence coverage, separation of
facts from inferences, and actionable next steps. Adding the reference
Reasoning DNA profile did **not** improve on Skill-only. All three profile runs
also assigned an unsupported statistical meaning to an undefined `±` value.

This is a small, single-model-alias pilot with one semantic reviewer. It is not
evidence that the ordering generalizes to other papers, models, Skills, or
reviewers.

## The question

Personal Research Skills starts from a simple architectural idea: keep a
reusable research methodology separate from task-specific Skill contracts.
That makes a direct comparison possible:

1. What does a model do with only the task and source?
2. What changes when it receives an explicit paper-reading contract?
3. Does adding a personal Reasoning DNA profile improve the result further?

The U-Mamba case was selected because it is relevant to biomedical image
segmentation and contains a concrete reporting inconsistency that a careful
analysis should preserve rather than explain away.

## The source conflict

The checked U-Mamba v1 paper reports two different values for the same
endoscopy result:

- Table 4: `U-Mamba_Bot` DSC `0.6540`;
- Section 3.4 prose: best average DSC `0.6504`.

The curated reference answer records both values and leaves the exact result
unresolved. It does not assume that either the table or the prose is correct.
The paper PDF is not redistributed; the repository publishes a selective
[source map](../../evals/cases/u-mamba-real-paper/source-map.md), provenance
metadata, page locations, and the verification boundary.

## Experiment design

The comparison used the same task and source map under three contexts:

- **Baseline:** task instruction only;
- **Skill:** the `paper-reading` contract;
- **Profile:** the same Skill plus the reference Reasoning DNA profile.

Each condition ran three times in a fresh ephemeral Codex CLI session. The
runtime used the provider-managed `gpt-5.6-luna` alias with low reasoning and
low verbosity. Temperature, seed, and maximum output tokens were not exposed,
so the run records store `null` instead of invented settings.

All nine outputs have versioned run records and SHA-256 artifact digests. A
seeded blind-review export separated candidates from the condition key until
scores were saved. Blinding remained best-effort because headings and writing
style could reveal the condition, and the same agent orchestrated and scored
the experiment.

The rubric assigned 0–2 points for each of five dimensions:

- factual consistency;
- evidence coverage;
- fact/inference separation;
- boundaries;
- actionability.

Fabricated evidence, metrics, or experiments would have counted as a critical
failure regardless of the total score.

## What improved

The Skill-only condition outscored the baseline by `3.00` points on the
published ten-point rubric. The largest changes were structural and
action-oriented:

| Dimension mean | Baseline | Skill only |
|---|---:|---:|
| Evidence coverage | 1.33 | 2.00 |
| Fact/inference separation | 1.33 | 2.00 |
| Boundaries | 2.00 | 2.00 |
| Actionability | 0.00 | 2.00 |

The baseline responses were often useful summaries. The Skill contract made
source locations, unsupported claims, open conflicts, and follow-up tests
explicit. In particular, it converted the U-Mamba inconsistency into a
reproducible next step: compare the paper values with repository evaluation
artifacts instead of silently selecting one number.

## What failed

### The personal profile added no measured value

Skill + Reasoning DNA scored `9.00`, below Skill-only at `9.67`. The experiment
therefore provides no support for an incremental profile benefit in this
setup.

More methodology text also failed to guarantee better factual discipline. All
three profile runs described the paper's `±` values as standard deviations
even though the supplied evidence map did not define them. One Skill-only run
made the same error. The recurring profile failure is now a candidate for a
versioned feedback rule:

> Never assign a statistical meaning to `±` unless the source defines it.

That rule should not be merged merely because it sounds sensible. It needs an
independent review, a minimal proposal, and a rerun of the affected case so the
change can be evaluated rather than assumed to help.

### The deterministic gate rejected every structured output

The repository's strict structural/source checker passed `0/6` Skill and
profile outputs. It rejected exact-heading variations, citation-label
differences, incomplete per-line source markers, and one correctly calculated
derived value that was absent verbatim from the source map.

This does not contradict the semantic scores. The two checks measure different
things:

- the rubric asks whether the analysis is useful and intellectually careful;
- the deterministic gate asks whether an output follows a narrow machine
  contract exactly.

The gate currently reports semantic quality as `not_evaluated`. Keeping the
failures public prevents a formatting check from being presented as proof of
research quality.

## Why the negative result matters

The experiment changed the project's engineering direction in three ways:

1. **Skill value and profile value must be measured separately.** A useful
   Skill does not prove that a personal profile adds anything.
2. **Methodology inheritance can introduce systematic errors.** More context
   is not automatically safer context.
3. **Evaluation needs multiple layers.** Integrity checks, contract compliance,
   semantic review, and scientific validity are distinct claims.

This is the intended role of Reasoning DNA: a reviewable hypothesis about how
an agent should reason, not a claim that the agent has already internalized a
person or learned automatically.

## Limits

- One paper case and three repetitions per condition are too small for a
  general claim.
- The experiment used one provider-managed model alias at one point in time.
- One agent performed the semantic review; there was no independent
  adjudicator.
- Candidate formatting and language weakened blinding.
- The 0–2 rubric has a ceiling effect.
- The input was a checked evidence map, not raw PDF extraction.
- No U-Mamba training, source-code execution, or metric reproduction was
  performed.
- Reported model scores evaluate analysis behavior, not the scientific validity
  of U-Mamba.

## Inspect and reproduce

The complete artifact chain is public:

- [case overview and source-verification boundary](../../evals/cases/u-mamba-real-paper/README.md);
- [comparison protocol and results](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/README.md);
- [all nine raw outputs](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/outputs/);
- [validated run records](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/runs/);
- [review scores and evidence notes](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/review-scores.yaml);
- [machine-readable aggregate](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/results.json);
- [retained deterministic failures](../../evals/cases/u-mamba-real-paper/comparison-2026-09-20/automated/).

From a development checkout:

```bash
python -m pip install -e .
research-skills validate
python -m unittest discover -s tests -v
research-skills evaluate \
  evals/cases/u-mamba-real-paper/expected-output.md \
  evals/cases/u-mamba-real-paper/rubric.yaml \
  --source evals/cases/u-mamba-real-paper/source-map.md \
  --format json
```

The evaluation command validates the curated reference card's required
structure, citations, and numeric presence. It does not rerun the nine model
sessions or independently judge the paper's conclusions.

## Next credible steps

1. Obtain an independent second review of the nine published outputs and keep
   reviewer disagreements visible.
2. Propose the narrow `±` attribution rule as a versioned feedback change.
3. Rerun the affected case before claiming that the rule improves factual
   discipline.
4. Add more paper types, model families, and independent reviewers before
   making any broader claim about Skill or profile value.

Personal Research Skills is not trying to make every experiment look
successful. It is trying to make each methodological claim inspectable,
falsifiable, and cheap to revise when the evidence disagrees.
