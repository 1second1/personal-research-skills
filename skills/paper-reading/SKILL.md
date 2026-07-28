---
name: paper-reading
description: Use when analyzing a research paper or paper excerpt and producing an evidence-grounded research evidence card with explicit facts, inferences, assumptions, boundaries, connections, and next actions.
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
3. `## Inferences`
4. `## Assumptions`
5. `## Boundaries`
6. `## Connections`
7. `## Next Actions`

## Procedure

1. State the research problem in one sentence.
2. Extract only direct claims into **Evidence**. Attach `[Source: ...]` to each material claim.
3. Prefix every non-direct conclusion with `Inference:`.
4. Identify assumptions needed for the reported result to hold.
5. State what the source does not establish, including missing baselines, missing uncertainty, missing external validation, or missing implementation detail.
6. Connect the method to `research_context` only when the context supplies a concrete comparison or decision.
7. End with numbered, falsifiable actions that specify what evidence would change the current conclusion.

## Quick Reference

| Write this | When |
|---|---|
| `[Source: section or location]` | Directly supported by the supplied text |
| `Inference:` | Derived from one or more source facts |
| `Unsupported:` | The source lacks evidence for the claim |
| `Open question:` | A decision needs information absent from the text |

## Common Mistakes

- Do not convert a higher metric into a claim of general superiority.
- Do not treat fewer parameters as measured lower latency.
- Do not call a comparison statistically reliable when variance or repeated runs are absent.
- Do not use `research_context` to overwrite or embellish the source.
- Do not give vague actions such as “run more experiments”; name the comparison, metric, and failure condition.
