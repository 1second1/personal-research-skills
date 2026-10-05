# Prospective manuscript-audit pilot — protocol 1.0

Status: **materials preparation; model generation not authorized**. This does not resume the paused uncertainty-v2 study or rescore historical runs. The public teaching case and its authored reports are not model evaluation outputs.

## Question and design

Compare concrete issue detection, verification, repair actionability, and revision recheck on one independent synthetic AI/ML manuscript pair.

- Conditions: `strong_prompt`, `skill` (manuscript-audit, no personal profile), and `peer_review`.
- Three independent repetitions per arm, each with initial audit and recheck: **18 stages**, potentially more model requests.
- Initial audit starts fresh. Recheck starts fresh with that arm/repetition's exact initial report and the revised materials. Source material and stage objectives are identical across arms; condition instructions/resources and each arm's own prior report differ.
- Revised materials are prepared before generation. Agents audit/recheck; they do not create condition-specific revisions or edit common inputs.
- This is a bounded pilot, not evidence across real manuscripts, disciplines, models, or full PDFs.

## Materials and conditions

Prepare the held-out pair after freezing Skill instructions, separately from the public demo. The material author knows the planted issues; this is not an independently authored external benchmark. No model answer is used to debug the Skill.

The pair contains partition/result inconsistencies, a bounded attribution gap, and a negative control excluding a suspected preprocessing path. An uncertainty example tests unspecified versus source-defined notation. The private answer key records exact locations, judgment classes, deciding artifacts, accepted repairs, and revised dispositions.

- Preserve `strong-review-prompt.md` verbatim, rather than a weak task-purpose baseline.
- Preserve manuscript-audit's full contract and entrypoint; use `--mode skill`.
- Pin K-Dense peer-review v2.4 to `a92663a0214b3b9fa1ba6b958284ffd919c00a0c`, with references, assets, scripts, and MIT license. Hash the complete package. Do not truncate the comparator or silently alter its instructions.
- Provide the same local Python/file tools, source files, permissions, and task objective. Comparator-specific helpers are available as part of each package. Preflight any dependency and the legitimate synthetic/author-owned intake path before approval.
- Model-visible workspaces exclude gold answers, reviewer checks, other outputs, the public demo, and unrelated files. No network, expensive training, or dependency installation during evaluation.

**Comparator compatibility:** v2.4's native intake checker rejects external-service use and benchmarking/data reuse even for a declared synthetic fixture. Preserve this restriction and its actual failed preflight in the record; do not set false declarations to obtain `READY_FOR_LOCAL_REVIEW`. The proposed API comparison therefore requires a disclosed common-task adaptation for author-owned synthetic benchmark materials, approved with the model/budget: it overrides the local-only/non-benchmark restrictions for these files, changes no upstream resource, and claims no journal/venue authorization or native gate success. Label the arm `peer_review` with this adaptation in reports, rather than claiming a native journal workflow comparison. A gate/deployment refusal is reported as workflow incompatibility, not a scientific-quality failure. If the adaptation is not approved, revise the comparison prospectively before generation.

Freeze SHA-256 hashes for source files, instructions/resources, stage requests, protocol, score template, private answers, and proposed limits. Verify completeness and isolation. Recheck contexts are hashed later because they include generated prior reports. Model/budget approval is a separately sealed execution addendum, not a retrospective material edit.

## Proposed limits and approval

Per stage propose **8 model requests, 32,000 cumulative input tokens, 4,000 cumulative output tokens, and 300 seconds**. Input includes repeated context, instructions/references, tool returns and prior report; output includes tool-call text and billed reasoning where available. Across 18 stages, nominal ceilings are 576,000 input and 72,000 output tokens. Retries consume the same allowance; unavailable usage is not zero.

The repository does not execute models or enforce these limits. An approved external harness must expose and enforce stage accounting. If a control is unavailable, disclose it and seal a feasible budget revision before generation; a per-response cap is not a total trajectory cap.

Present the material seal, exact provider/model identifier or version visibility limit, sampling settings, request range, token/pricing estimate, tools and hard ceiling to the user. **Do not generate until the user confirms materials, model and budget.** This document alone is not authorization.

## Semantic scoring

Score meaning without requiring our headings. Give each concern a blind finding ID, quote, evidence-based disposition and source location. Deduplicate the same underlying issue; listing consequences does not multiply recall. Keep unexecuted conditional hypotheses separate from asserted defects.

| Measure | Frozen rule |
|---|---|
| True issues | Match predefined issues or independently substantiate unexpected issues; report confirmed errors and evidence gaps separately |
| Recall | Matched predefined issues / applicable predefined issues per class; unexpected issues are listed without changing the frozen denominator |
| Precision / false positives | Supported actionable issues / asserted actionable issues; count contradicted allegations and unnecessary repairs after evidence excludes a path |
| Location | 0 absent/wrong; 1 correct file/broad section; 2 exact table, claim, function, JSON key or sample/group IDs |
| Actionability | 0 generic/wrong; 1 concrete operation missing input/criterion; 2 executable check with supplied inputs, decision criterion and bounded repair |
| Recheck | Correctly closed, incorrectly closed, incorrectly resurrected, unresolved, or not applicable per issue |
| Efficiency | Elapsed time, actual requests, input/output usage and cost/basis per stage and per audit/recheck episode |

Use not applicable when precision or recall has a zero denominator; always report counts. Missing optional artifacts are evidence limits, not proof work was never done. A clearly labeled possible risk is not automatically an asserted error. Record voluntary exclusion of the negative control and correct uncertainty scope.

Fabricated citations, numbers, successful commands, reproduction, or scientific-validation claims are critical failures regardless of scores. Honest failed execution is not fabrication. Claim narrowing can resolve wording without proving original causation.

Use fixed-seed best-effort blinding, recording suspected unblinding. First score blinded reports; separately verify execution claims against original traces, documenting any condition disclosure. Costs come from original receipts. A second reviewer handles disputes; absent adjudication remains unresolved. Do not call the generating model an independent judge.

## Records, failures and reporting

- Use run-record v1.2, distinct audit/recheck task IDs, and the parent initial-run ID/report digest in recheck input. Input contains a full material manifest. Trace preserves every model request and tool command, output, exit status, timeout, usage receipt, and failure.
- Hash input/context/output/trace. Unknown controls, usage, duration or attributable cost are `null`; estimate basis is `estimated`, actual provider figures `reported`.
- Preserve empty, failed and over-limit stages. No rerun to select favorable results. Infrastructure retries are separate attempts after documented fixes; retain original attempts and costs.
- Score sheets retain quotes, matches, disputes, locations and execution evidence. Generate summaries by program after scoring; no hand-typed aggregate counts.
- Report per-arm/per-repetition results, critical failures, excluded concerns, denominators, variation, and resources. Do not hide failures behind a pooled score.

Both Skills also contain prospective pressure scenarios for undefined/defined `±`, absent artifacts, component interactions, source instruction injection, and repaired-issue resurrection. They have not been run. Expanding beyond this pilot requires a separate budget.
