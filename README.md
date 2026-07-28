# Personal Research Skills

> 把研究方法、判断标准和工作流沉淀为可组合、可验证、可演化的 AI Skills。

Personal Research Skills 是一个面向科研学习与深度研究的实验性开源项目。
第一阶段以论文阅读、代码分析、实验设计和研究写作为参考场景，探索一个核心问题：

> 明确的个人研究方法，能否让不同科研 Skill 的输出保持一致、可追溯，并且通过反馈持续改进？

## 5 分钟理解

输入一篇论文、一个公开代码仓库和一个研究问题，项目希望输出：

```text
论文证据卡片
  → 论文-代码对应关系
  → 可执行实验计划
  → 研究复盘报告
```

每个关键结论都应尽量回溯到论文页码、代码文件、配置项或实验日志，并明确区分：

- `evidence`：来源中明确出现的事实
- `inference`：基于证据的推断
- `recommendation`：面向下一步行动的建议

## 核心方法

```text
Identity
  ↓
Values
  ↓
Thinking / Inquiry Pattern
  ↓
Workflow
  ↓
Preference
  ↓
Skills
```

Inquiry Pattern 是项目的第一版思维基线：

```text
What → Why → Assumption → Boundary
     → Connection → Generalization → Application → Value
```

Skill 不只是 Prompt，而是继承这套方法的、具有输入输出边界和评估标准的能力单元。

## 当前状态

`v0.1 — Week 1: 方法论基线与仓库骨架`

当前已完成：

- 个人研究方法 Profile
- 项目边界与非目标
- Agent / Skill 职责划分
- 贡献规范
- 评估原则草案

尚未完成：

- 可运行的五个科研 Skill
- 自动评测脚本
- 生产级 Runtime
- 自动 Skill 演化

## 仓库结构

```text
personal-research-skills/
├── README.md
├── profiles/
│   └── researcher-example.yaml
├── docs/
│   ├── methodology.md
│   ├── compatibility.md
│   └── contributing.md
└── evals/
    └── README.md
```

后续 Skill 目录统一采用：

```text
skills/<skill-name>/
├── SKILL.md
├── contract.yaml
├── examples/
├── evals/
└── changelog.md
```

## 第一阶段路线

1. 建立个人研究方法基线。
2. 编写 `paper-reading` 并用真实论文进行基线测试。
3. 编写 `codebase-analysis`，建立论文到代码的追踪样例。
4. 编写实验设计、实验复盘和研究写作 Skills。
5. 建立失败案例、回归评测和可审查的改进提案。

## 运行方式

当前版本以 Markdown、YAML 和 Agent-compatible 文件为主，可以被复制到 Codex 或 Claude Code 的项目级 Skills 目录中使用。

执行具体 Skill 前，请先阅读对应的 `SKILL.md`、`contract.yaml` 和评测说明。需要 API、PDF 解析、仓库访问或实验执行的功能将在后续版本中逐步增加。

## 贡献一个 Skill

一个 Skill 至少需要提交：

- `SKILL.md`
- 能力契约
- 一个真实输入样例
- 一个期望输出样例
- 评估规则
- 已知限制与风险
- 变更记录

详见 [`docs/contributing.md`](docs/contributing.md)。

## 设计文档

- [方法论基线](docs/methodology.md)
- [兼容性说明](docs/compatibility.md)
- [贡献规范](docs/contributing.md)
- [评估入口](evals/README.md)

## 非目标

第一阶段不做通用 Agent 平台、多用户 SaaS、无约束自动改写 Skill、完整人格复制或覆盖所有科研领域的知识库。

## 许可证

当前仍处于实验阶段，许可证将在第一版可运行 Skills 发布前确定。
