# Methodology Baseline

## 目标

本文件定义参考 Profile 的方法论基线。独立安装的 Skill 不会自动载入该
Profile；需要通过 `research-skills compose` 显式组合。

它不是人格描述，也不是不可修改的系统 Prompt。它是一份可以被评估、被质疑、被版本化的研究工作规则。

## 四层结构

### Values

回答“什么值得做”和“什么样的结果值得保留”。当前基线强调长期价值、原理、复用、证据和可验证性。

### Thinking

以 [`profiles/reasoning-dna.yaml`](../profiles/reasoning-dna.yaml) 中的
`thinking.inquiry_pattern` 为当前思维结构：

```text
What → Why → Assumption → Boundary → Connection → Application → Value
```

该顺序不是要求每个回答机械输出七个标题，而是要求 Agent 在任务允许时完成这些判断。

### Workflow

将研究从问题推进到产物：

```text
发现问题 → 阅读论文 → 分析代码 → 设计实验
        → 记录结果 → 复盘失败 → 形成报告
```

上图是后续研究工作的路线示意；组合器当前实际注入的流程以 Profile
文件中的 `workflows` 字段为准。

### Preference

偏好 Markdown、YAML、JSON、Mermaid、结构化表达和证据标注。偏好属于可变层，不能被误当作核心价值或思维规则。

## 输出分类

所有科研产物尽量使用以下三类标记：

| 类型 | 定义 | 允许的语气 |
|---|---|---|
| Evidence | 来源明确陈述或可直接观察的结果 | “论文第 X 页说明……” |
| Inference | 基于证据的解释或推断 | “这可能意味着……” |
| Recommendation | 面向下一步行动的建议 | “下一步可验证……” |

## 质量检查

提交研究产物前，Agent 至少检查：

- 问题是否被清楚定义？
- 关键结论是否有来源？
- 事实和推断是否分开？
- 假设和失败边界是否被说明？
- 是否存在与当前研究问题的连接？
- 输出是否形成了可执行的下一步？

## 演化规则

一次用户修改不能自动成为永久规则。只有当修改：

1. 能解释一个可复现的失败模式；
2. 不只是一次性的格式偏好；
3. 能写成新的评测用例；
4. 经过人工审查；

才可以进入 Profile 或 Skill 的新版本。
