# Personal Research Skills 中文说明

> 将个人研究方法、判断标准和工作流沉淀为可组合、可验证、可演化的 AI Skills。

这是一个面向科研学习与深度研究的实验性开源项目。项目关注的问题是：明确的个人研究方法，能否让不同科研 Skill 的输出保持一致、可追溯，并通过评测和反馈持续改进？

## 安装到 Codex 和 Claude Code

如果只想使用三个科研 Skill，不需要安装 Python、不需要 API Key，也不需要配置模型服务；
安装器需要 Node.js 和 `npx`，使用开源的
[`skills` CLI](https://github.com/vercel-labs/skills)。请在希望启用这些 Skill 的项目目录中运行：

```bash
npx skills add 1second1/personal-research-skills
```

也可以用一条命令把三个 Skill 同时安装到 Codex 和 Claude Code：

```bash
npx skills add 1second1/personal-research-skills \
  --skill '*' --agent codex --agent claude-code --copy --yes
```

经过实际烟测，项目级安装位置分别是 Codex 的 `.agents/skills/` 和 Claude Code 的
`.claude/skills/`。Skill 会继承宿主 Agent 获得的权限，使用前应检查其内容。
本仓库目前不是 Codex 或 Claude 官方插件，不会把普通 GitHub 仓库包装成官方市场项目来宣传。

### 可用 Skills

| Skill | 适用场景 | 示例请求 |
|---|---|---|
| `paper-reading` | 检查论文主张、证据、数值、局限和内部一致性 | `使用 paper-reading 分析 paper.md，不要把推断写成事实。` |
| `research-question` | 把宽泛研究想法转化为有边界、可证伪的问题 | `使用 research-question 把这个想法收敛成可验证的研究问题。` |
| `argument-analysis` | 拆分论证中的主张、依据、论证桥梁、反方意见和边界 | `使用 argument-analysis 审查 article.md 的论证结构。` |

在 Codex 中还可以通过 `$paper-reading`、`$research-question` 或
`$argument-analysis` 显式调用；当请求与 Skill 描述匹配时，宿主也可能自动选择。

这条安装命令让三个 Skill 可以独立使用，**不会自动加载**
[`profiles/reasoning-dna.yaml`](profiles/reasoning-dna.yaml)。如果要应用个人
Reasoning DNA，需要用下文的 [`research-skills compose`](#框架开发) 生成组合
上下文，再把生成的 Markdown 提供给 Agent。组合器只生成上下文，不调用模型。

## 60 秒 Skill 演示

安装 `paper-reading` 后，把下面的请求和已核对的摘录一起复制到 Codex 或
Claude Code。这个例子使用独立 Skill，不需要克隆仓库或解析 PDF。摘录来自
[U-Mamba 来源映射](evals/cases/u-mamba-real-paper/source-map.md)，其中记录了
这些主张在论文中的位置。

```text
使用 paper-reading Skill，只分析下面这段已核对的摘录。区分来源事实和推断；
列出冲突的数值与各自位置；在证据不足时不要判断哪个数值正确。

U-Mamba，arXiv:2401.04722v1，内镜器械分割：
- 第 9 页 Table 4：U-Mamba_Bot 的 DSC 为 0.6540 +/- 0.3008。
- 第 9 页 Section 3.4：正文称最佳平均 DSC 为 0.6504。
摘录没有定义 +/- 后面的数值代表什么。
```

检查回答是否同时保留两个数值、标注两个来源位置，并保持 `+/-` 的含义
未定；具体措辞可能不同。较长的真实输出见
[归档的仅 Skill 运行](evals/cases/u-mamba-real-paper/comparison-2026-09-20/outputs/skill-r1.md)。

仓库中已发布的实验使用**完整来源映射**，不是上面这段短摘录。在同一模型
别名、每组独立运行三次的条件下，评分结果为：

| 条件 | 平均评分 | 本次结果 |
|---|---:|---|
| 基础任务 | 6.67 / 10 | 能完成总结，但按公开评分标准缺少可执行的后续行动 |
| 仅 `paper-reading` Skill | 9.67 / 10 | 证据覆盖、事实与推断分离、后续行动均更完整 |
| Skill + Reasoning DNA | 9.00 / 10 | 没有额外增益；三次运行都过度解释了来源未定义的 `±` |

Profile 条件使用下文的组合器；只安装 Skill 不会复现这一条件。这只是九次
运行、单一语义评审者的小型实验，不是通用基准。

[阅读完整案例文章](docs/case-studies/u-mamba-negative-result.md) ·
[检查全部原始输出与运行记录](evals/cases/u-mamba-real-paper/comparison-2026-09-20/README.md)

## 当前版本

`v0.2 — 独立科研 Skill 与可选的 Reasoning DNA 组合`

当前包含：

- `profiles/reasoning-dna.yaml`：Values、Inquiry Pattern、Decision Rules、Workflow 和 Preference；
- 基于 PyYAML 严格校验的 DNA 加载器与 Skill 组合器；
- `paper-reading`：证据导向的论文阅读 Skill；
- `research-question`：将宽泛想法转化为有边界、可证伪研究问题的 Skill；
- `argument-analysis`：分析文章、评论和访谈中的主张、依据、隐含前提与边界；
- 示例、自动测试、仓库校验和 GitHub Actions；
- 面向三个 Skill 的通用结构评测器与版本化 JSON 报告；
- 带 SHA-256 完整性校验的 provider-neutral 运行记录 Schema；
- 将盲评候选与 condition 对照表分离的可复现导出工具；
- 首个带来源完整性记录的 [U-Mamba 真实论文案例](evals/cases/u-mamba-real-paper/README.md)，保留表格与正文的数值冲突而不替作者消解。
- 九次运行的 [U-Mamba 三条件对照实验](evals/cases/u-mamba-real-paper/comparison-2026-09-20/README.md)，
  公开上下文、原始输出、完整性记录以及 Profile 未带来增益的负结果。

当前 Runtime 只负责生成组合后的执行上下文，不调用模型、不保存私有记忆，也不声称已经具备自动学习能力。

## 框架开发

下面的命令用于开发组合器、评测器和运行记录工具；如果只使用已经安装的 Skill，
不需要执行这些步骤。框架开发需要 Python 3.10 或更高版本，不需要 API Key 或私有数据：

```bash
git clone https://github.com/1second1/personal-research-skills.git
cd personal-research-skills
python -m pip install -e .

python -m unittest discover -s tests -v
research-skills validate
research-skills compose paper-reading skills/paper-reading/examples/input.md --output context.md
research-skills compose research-question skills/research-question/examples/input.md
research-skills compose argument-analysis skills/argument-analysis/examples/input.md
research-skills evaluate skills/research-question/examples/expected-output.md evals/rubrics/research-question.yaml --format json
research-skills validate --run evals/fixtures/run-record-demo/run.yaml
```

要把 Reasoning DNA 应用到自己的材料，请把上面 `compose` 命令里的示例输入
路径替换为 UTF-8 文本或 Markdown 文件，再将生成的 `context.md` 交给 Agent
作为任务上下文。默认 `profile` 模式同时包含 Skill 和
[`profiles/reasoning-dna.yaml`](profiles/reasoning-dna.yaml)；`--mode skill`
不包含 Profile。两种模式都不会调用模型。

输入路径写成 `-` 时从 stdin 读取；`--output` 会直接写入 UTF-8 Markdown，
避免依赖 PowerShell 管道传递 Unicode 字符。原有无 `compose` 命令形式和
`scripts/run_skill.py` 仍兼容。
若在仓库目录外运行已安装命令，请传入
`--root /path/to/personal-research-skills`；wheel 不复制公开的 Skill 和 Profile 文件。

真实模型输出应按 `evals/schemas/run-record-v1.1.schema.json` 记录输入、组合上下文、
输出、模型设置和 SHA-256。至少准备两个运行记录后，可用 `research-skills blind`
生成盲评包；只把 `review-manifest.json` 和 `candidates/` 交给评审，评分完成前不要
提供 `private/review-key.json`。运行时没有公开的采样参数应记为 `null`，不能猜测；
旧版 `1.0` 记录仍然兼容。仓库中的 demo 仅用于完整性测试，不是模型成绩。

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

解析与合同传递、通用评测器、运行记录 Schema、盲评导出、初版评测协议以及首个真实论文证据案例已经完成。U-Mamba 案例核实到
Table 4 的 `0.6540` 与正文的 `0.6504` 冲突；它是人工核验的参考夹具，不是模型质量结果。
首轮三条件重复实验中，baseline、仅 Skill、Skill + Profile 的平均分分别为
`6.67`、`9.67`、`9.00`。这说明本次设置下 Skill 有明显作用，但 Profile 没有额外增益；
评审只有一个 Agent，仍需独立人工复核。一次
[论证分析小型实验](evals/cases/2013-text3-pilot/README.md) 显示 Skill 合同有明显作用，
但尚未测出 Reasoning DNA 相比仅 Skill 的独立增益；这只是单次试验，不能推广。

1. 对已发布的真实论文运行进行第二位独立评审并保留分歧；
2. 针对 `±` 被错误解释为标准差的问题建立可审查、可版本化反馈，并回归测试；
3. 在反馈回归后接通用模型执行层，再接 PDF、仓库和实验执行适配器。

英文主说明请阅读 [README.md](README.md)。
