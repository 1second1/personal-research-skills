# Evaluation Entry

第一周只建立评估入口和规则，不声称已有自动评测能力。

## 第一阶段指标

| 指标 | 说明 |
|---|---|
| factual-consistency | 是否忠实于论文、代码或实验记录 |
| evidence-coverage | 关键结论是否带可追溯来源 |
| inquiry-pattern-coverage | 是否覆盖必要的 What / Why / Assumption / Boundary 判断 |
| method-consistency | 不同 Skill 是否继承同一方法论 Profile |
| actionability | 输出是否能形成下一步研究任务 |

## 基线任务

后续每个 Skill 至少补充一个基线任务。第一批建议覆盖：

1. 论文方法与假设提取。
2. 论文公式变量解释。
3. 论文到 GitHub 入口文件的对应。
4. 医学图像分割实验方案设计。
5. 训练日志异常与复盘建议。

## 评估原则

评估结果必须保留输入、输出、评分和失败原因。任何方法论或 Skill 更新，都需要重新运行受影响的回归任务。
