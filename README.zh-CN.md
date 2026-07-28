# Personal Research Skills 中文说明

> 将个人研究方法、判断标准和工作流沉淀为可组合、可验证、可演化的 AI Skills。

这是一个面向科研学习与深度研究的实验性开源项目。项目关注的问题是：明确的个人研究方法，能否让不同科研 Skill 的输出保持一致、可追溯，并通过评测和反馈持续改进？

## 当前版本

`v0.2 — Reasoning DNA Runtime 与继承型科研 Skill`

当前包含：

- `profiles/reasoning-dna.yaml`：Values、Inquiry Pattern、Decision Rules、Workflow 和 Preference；
- 标准库实现的 DNA 加载器与 Skill 组合器；
- `paper-reading`：证据导向的论文阅读 Skill；
- `research-question`：将宽泛想法转化为有边界、可证伪研究问题的 Skill；
- 示例、自动测试、仓库校验和 GitHub Actions。

当前 Runtime 只负责生成组合后的执行上下文，不调用模型、不保存私有记忆，也不声称已经具备自动学习能力。

## 快速开始

需要 Python 3.10 或更高版本，不需要 API Key 或私有数据：

```bash
git clone https://github.com/1second1/personal-research-skills.git
cd personal-research-skills

python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/run_skill.py paper-reading skills/paper-reading/examples/input.md
python scripts/run_skill.py research-question skills/research-question/examples/input.md
```

## 核心模型

```text
Identity → Values → Thinking → Workflow → Preferences → Skills
```

第一版 Inquiry Pattern：

```text
What → Why → Assumption → Boundary → Connection → Application → Value
```

项目不把 Skill 当作孤立 Prompt，而是要求每个 Skill 具备输入输出契约、证据规则、示例、评测和适用边界。

## 后续路线

1. 对现有 Skill 做独立 Agent 前向测试；
2. 增加代码库分析或论文到代码追踪 Skill；
3. 对比无 Profile、仅 Skill、Skill + Reasoning DNA 三组输出；
4. 建立可审查的反馈与规则演化日志；
5. 在评测闭环稳定后，再考虑模型、PDF、仓库和实验执行集成。

英文主说明请阅读 [README.md](README.md)。
