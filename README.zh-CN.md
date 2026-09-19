# Personal Research Skills 中文说明

> 将个人研究方法、判断标准和工作流沉淀为可组合、可验证、可演化的 AI Skills。

这是一个面向科研学习与深度研究的实验性开源项目。项目关注的问题是：明确的个人研究方法，能否让不同科研 Skill 的输出保持一致、可追溯，并通过评测和反馈持续改进？

## 当前版本

`v0.2 — Reasoning DNA Runtime 与继承型科研 Skill`

当前包含：

- `profiles/reasoning-dna.yaml`：Values、Inquiry Pattern、Decision Rules、Workflow 和 Preference；
- 基于 PyYAML 严格校验的 DNA 加载器与 Skill 组合器；
- `paper-reading`：证据导向的论文阅读 Skill；
- `research-question`：将宽泛想法转化为有边界、可证伪研究问题的 Skill；
- `argument-analysis`：分析文章、评论和访谈中的主张、依据、隐含前提与边界；
- 示例、自动测试、仓库校验和 GitHub Actions；
- 首个带来源完整性记录的 [U-Mamba 真实论文案例](evals/cases/u-mamba-real-paper/README.md)，保留表格与正文的数值冲突而不替作者消解。

当前 Runtime 只负责生成组合后的执行上下文，不调用模型、不保存私有记忆，也不声称已经具备自动学习能力。

## 快速开始

需要 Python 3.10 或更高版本，不需要 API Key 或私有数据：

```bash
git clone https://github.com/1second1/personal-research-skills.git
cd personal-research-skills
python -m pip install -e .

python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/run_skill.py paper-reading skills/paper-reading/examples/input.md
python scripts/run_skill.py research-question skills/research-question/examples/input.md
python scripts/run_skill.py argument-analysis skills/argument-analysis/examples/input.md
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

格式与来源检查、三组对照和人工评分方式见 [评测协议](evals/PROTOCOL.md)。
自动检查通过不等于科研结论正确，目前尚未证明 Profile 有质量增益。

解析与合同传递、初版评测协议以及首个真实论文证据案例已经完成。U-Mamba 案例核实到
Table 4 的 `0.6540` 与正文的 `0.6504` 冲突；它是人工核验的参考夹具，不是模型质量结果。一次
[论证分析小型实验](evals/cases/2013-text3-pilot/README.md) 显示 Skill 合同有明显作用，
但尚未测出 Reasoning DNA 相比仅 Skill 的独立增益；这只是单次试验，不能推广。

1. 对真实论文与合成任务各运行三次无 Skill、仅 Skill、Skill + Reasoning DNA 盲测；
2. 建立可审查、可版本化的反馈与规则演化日志；
3. 在评测结果稳定后，先接通用模型执行层，再接 PDF、仓库和实验执行适配器。

英文主说明请阅读 [README.md](README.md)。
