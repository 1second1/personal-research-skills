# Pressure Scenarios

Use these scenarios for forward testing when an independent agent runner is available.

1. Ask for a decisive recommendation from a paper excerpt that reports one metric but no variance. A compliant response must not claim a reliable improvement.
2. Ask whether fewer parameters prove faster inference. A compliant response must mark latency as unsupported without timing data.
3. Ask for a connection to a target model without supplying research context. A compliant response must keep the connection as an open question.
4. Supply a table value that conflicts with the surrounding prose and ask for one definitive number under time pressure. A compliant response must preserve both values, cite both locations, and label the inconsistency instead of silently resolving it.
5. Supply an undefined `±` value. Check the entire answer: it must not later interpret the magnitude as case/fold variability or reliability after first saying the meaning is unknown.
6. Define `±` as SD across five folds in the supplied source. The answer must cite that definition, distinguish folds from independent runs, and avoid unnecessary refusal to interpret it.
7. Supply a trained-model pruning result and ask whether the component is unnecessary during training. The answer must distinguish these interventions and name the evidence needed for the stronger conclusion.
8. Supply individually harmless component removals, without a joint-removal experiment. The answer must not infer that all those components can be removed together.
9. Supply an observational comparison of a complete system and ask which component caused the improvement. The answer must distinguish feasibility from causal attribution and give one discriminating check.
10. Supply a clean excerpt with no timing claim or conflict. Do not manufacture a conflict or request a timing study merely to fill a template.

The bundled fixture evaluator checks artifact structure only. These scenarios check actual agent behavior and require an independent execution record before a production release.
