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
