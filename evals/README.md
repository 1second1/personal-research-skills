# Evaluation

This directory contains the public evaluation entry points. The current evaluator checks repository fixtures and contract-level behavior; it does not claim to measure the quality of model-generated research outputs.

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
