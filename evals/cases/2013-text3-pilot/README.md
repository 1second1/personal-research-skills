# Argument-analysis pilot: 2013 Text 3

This case records the first same-model comparison of the repository's three
composition modes, followed by one forward test of `argument-analysis`.

## Source handling

The input was a user-supplied image of one English exam passage about humanity's
long-term future. The source image and full transcription are not redistributed
because this repository does not establish publication rights. The public outputs
are model-generated analyses. This limits exact third-party reproduction.

## Conditions

- Date: 2026-09-19
- Model reported by Codex CLI: `gpt-5.6-sol`
- Reasoning effort reported by CLI: `none`
- One fresh ephemeral session per condition
- No browsing or external evidence
- One run per condition
- Scores assigned by the authoring agent with condition labels visible

The first three conditions used `paper-reading`:

1. baseline task and source;
2. Skill contract and source;
3. Skill contract, Reasoning DNA profile, and source.

The fourth output is a later forward test using `argument-analysis` plus the
profile. It is not part of the original three-way score comparison.

## Pilot scores

| Condition | Factual consistency | Evidence coverage | Fact/inference separation | Boundaries | Actionability | Total |
|---|---:|---:|---:|---:|---:|---:|
| Baseline | 2 | 1 | 1 | 2 | 0 | 6/10 |
| Paper-reading Skill | 2 | 2 | 2 | 2 | 1 | 9/10 |
| Paper-reading Skill + profile | 2 | 2 | 2 | 2 | 1 | 9/10 |

No critical fabrication was observed. The Skill-only output proposed arbitrary
future-study thresholds, including a sample count and probability cutoff, which
reduced its actionability score.

## Result

The baseline was concise and independently detected the passage's main logical
gap: a current “Least Concern” classification cannot establish survival over
thousands of years. The paper-reading Skill improved traceability, assumptions,
and boundaries, but overfit a research-paper workflow to an essay. The profile
added useful conceptual distinctions but did not outscore Skill-only.

The argument-analysis forward test better matched the genre. It reconstructed
each claim as support plus implicit warrant, classified the Long Now clock as
an example rather than survival evidence, and gave one decisive internal
counterargument. It avoided arbitrary datasets and numeric thresholds. This
single output motivated the new Skill; it does not establish a general gain.

## Artifacts

- [Baseline](outputs/baseline-output.md)
- [Paper-reading Skill](outputs/skill-output.md)
- [Paper-reading Skill plus profile](outputs/profile-output.md)
- [Argument-analysis forward test](outputs/argument-analysis-output.md)

## Limitations

- One run cannot estimate model variance.
- The initial scoring was not blind and had no second reviewer.
- The source is an argumentative exam excerpt rather than a research paper.
- Some arrows and punctuation were corrupted while the first prompts crossed a
  PowerShell pipeline. The prose remained readable, but the transport must be
  corrected before formal evaluation.
- The rubric rewards research actionability and therefore does not fully measure
  usefulness for reading comprehension.

The defensible conclusion is narrow: the Skill contract changed output structure
and coverage in this case; this pilot did not demonstrate an independent benefit
from Reasoning DNA.
