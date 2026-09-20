# Contributing

感谢参与 Personal Research Skills。这个项目贡献的重点不是增加 Skill 数量，而是把研究方法写成可理解、可复用、可评估的能力单元。

## 提交一个 Skill

新 Skill 至少需要包含：

```text
skills/<skill-name>/
├── SKILL.md
├── contract.yaml
├── examples/
│   ├── input.md
│   └── expected-output.md
└── evals/
    └── pressure-scenarios.md
```

## 必须说明

- 这个 Skill 解决什么研究问题？
- 什么时候应该使用它？
- 什么情况下不应该使用它？
- 输入和输出是什么？
- 它继承了哪些 Values、Thinking 或 Workflow 规则？
- 哪些结论必须有证据？
- 如何判断输出合格？
- 已知失败模式和风险是什么？

## 评测要求

每个 Skill 需要提供至少一个真实或脱敏的研究样例，并包含：

- 正常输入
- 边界输入
- 信息不足输入
- 事实与推断混淆风险
- 期望行为和失败判据

不要只通过“读起来不错”判断 Skill 质量。优先检查证据覆盖率、事实一致性、边界说明和行动可执行性。

## 修改方法论

如果修改 Values、Inquiry Pattern 或 Workflow，需要同时提交：

1. 修改动机；
2. 真实失败案例；
3. 新增或更新的评测用例；
4. 对现有 Skills 的影响；
5. 是否需要人工批准。

一次性的排版偏好应更新 Preference，不应升级为 Thinking 或 Values。

## 提交前检查

- 文件命名使用小写字母和连字符。
- `SKILL.md` 具有清晰的触发条件和非目标。
- 示例输入可以被其他人理解。
- 评测规则可以被复现。
- 没有把推断写成来源事实。
- 没有把私密对话、私有数据或 API 密钥提交到仓库。
- 根目录 `CHANGELOG.md` 说明了面向用户的版本和行为变化。
