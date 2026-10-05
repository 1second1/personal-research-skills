# Personal Research Skills

## Cross-Agent Handoff and Long-Term Engineering Plan

### 当前状态入口 — 2026-10-05

本节是唯一的当前交接入口；下文是按日期保留的历史记录。

1. **当前目标与完成范围**：按已批准的实施计划优化 `paper-reading`，新增
   `manuscript-audit`，完成可复现的合成教学案例，以及三组初审／复查比较的材料和预注册。
   新增运行记录 v1.2 与封存检查器；旧 v1.0／v1.1 验证规则和历史输出、评分保持原样。
   这是程序实现和材料准备；模型行为评测尚未执行。
2. **实际工作位置与 Git 状态**：`C:\personal research skill`，当前分支 `master`。
   本轮从干净的 `796ad3886cfac5776a8a984453daf953937df179` 开始，在临时分支
   `codex/manuscript-audit` 完成实现。实现提交为
   `02921f508609e4223b32ace193c9eb3e7d020e97`，已快进合入 `master` 并推送，远端 SHA
   已核对一致；确认其包含于远端 `master` 后，已删除该本地交付分支，没有创建对应远端分支。
   这是按用户此前授权的常规交付执行。本节是后续完成状态补录，随独立文档提交保存；
   最新 HEAD 与同步状态使用 `git log -1`、`git status --short --branch` 核对。
   新版本发布、技能全局安装和额外模型调用未执行。
3. **交付物绝对路径**：
   - 阅读入口：`C:\personal research skill\skills\paper-reading\SKILL.md`。
   - 作者审查入口：`C:\personal research skill\skills\manuscript-audit\SKILL.md`。
   - 教学案例：`C:\personal research skill\evals\cases\manuscript-audit-demo\README.md`；
     同目录含原稿、修订稿、CSV、配置、纯 Python 实验与检查器、实际原始结果和日志、
     审查／复查参考报告以及 `repair.diff`。这些参考报告是在实现过程中编写整理的，
     不代表模型独立发现或真实科研效果。
   - 公共预注册和预算：`C:\personal research skill\evals\cases\manuscript-audit-pilot`。
   - 私有冻结包：`C:\personal research skill\evals\local\manuscript-audit-prospective-20261005`。
     此目录受现有忽略规则保护，答案、检查依据和模型输入分开保存，不提交或发布。
4. **本轮实际运行的验证**：使用已有 `.venv`、命令范围内 UTF-8 设置运行完整测试，
   114 项通过；仓库校验、旧演示运行记录校验、新 Skill 示例的结构检查和封存检查均通过。
   36 个不同本地 Markdown 链接目标存在，`git diff --check` 通过。
   新增负向验证覆盖旧版本拒绝新条件、计量类型、轨迹路径／哈希、材料封存篡改、
   伪造预处理记录和预测。第一次受限测试的写入失败属于权限问题；在获准环境重跑，
   没有通过修改业务规则掩盖失败。
   教学案例原版实际检出 12 位患者全部跨训练／测试集，实际准确率 `12/12 = 1.0`
   与论文 `0.93` 冲突；修复后按患者划分，准确率 `4/16 = 0.25`，检查全部通过。
   两次测试集不同，不能把数值下降当作泄漏的受控因果效应。训练集统计量预处理的质疑
   由实际记录、独立重算和仅改变测试特征的检查排除；组件归因通过收窄主张解决，未补做消融。
   程序和结构检查均不评估语义正确性或 Skill 的模型效果。
   合并到 `master` 后再次实际运行同一完整测试、仓库／旧记录校验、新 Skill 结构检查及
   封存校验，全部通过。实现提交的 GitHub Actions 运行 `37286598624` 实际完成并成功，
   Ubuntu／Windows × Python 3.10／3.12 四项任务均通过：
   `https://github.com/1second1/personal-research-skills/actions/runs/37286598624`。
5. **材料冻结与对照兼容性**：独立材料在 Skill 指令冻结后创建，未用于模型调试。
   冻结包包含 75 个文件，共 500,082 字节，`seal.json` 的 SHA-256 为
   `18244726547b52446835dfabb967f9433947abba942f02d554e5a67e1667b3c7`。
   公共 `material-lock.json` 与实际封存文件一致；入口检查器为
   `C:\personal research skill\scripts\verify_evaluation_seal.py`。
   K-Dense `peer-review` v2.4 固定在
   `a92663a0214b3b9fa1ba6b958284ffd919c00a0c`；对应入口、参考资料、模板、脚本和许可均保存，
   源文件未改写。实际兼容性预检发现原生 intake 明确禁止外部服务及基准数据复用，返回
   `BLOCKED`；本次使用的是注明假设条件的兼容性输入，不是假造许可或真实投稿记录。
   预算提案因此明确包含仅限自有合成材料的任务适配，待用户批准；不声称原生 gate 已通过，
   不把部署限制当作审查效果差异。
6. **未完成事项与授权边界**：拟定三组条件 × 三次重复 × 初审／复查，共 18 个阶段，
   工具循环可能增加实际调用数。当前额外模型评测调用数为 0，尚无模型输出或语义评分。
   行为压力场景已编写，未运行。候选为官方 API 的 `deepseek-flash`；按照本轮核对的
   官方价格和累计 token 上限，估算 API 成本上限约为人民币 0.864／1.728 元
   （低峰／高峰，未使用缓存折扣），拟申请人民币 3 元硬上限。
   材料、上述对照任务适配、模型和预算尚需确认；另一个 DeepSeek harness 的实际
   计量、思考模式及超限终止能力尚未检查。预算提案不是已批准预算或实际账单。
   用户确认后，先固定 harness 配置和隔离权限，再启动评测；若需修改冻结材料或阈值，
   创建前瞻性版本，不依据生成结果追溯改写。
7. **保留事项**：旧 36 次实验继续暂停，旧九份 U-Mamba 输出／评分及原冻结材料没有改写。
   `codex/uncertainty-v2-candidate` 和其独立工作树仍有未晋升工作，继续保留；
   `.local-project-materials`、`evals/local`、现有 `.venv` 不属于清理目标。

### 历史记录：README、About 与交付分支收束 — 2026-10-04

本节保留 2026-10-04 的历史状态；续做前以开头当前入口和实际文件、Git 状态为准。

1. **当前目标与完成范围**：按用户“先做前两个”，更新 GitHub About 描述，
   并把归档 U-Mamba 来源/基础回答/Skill 回答对照图放入中英文 README；用户随后授权提交、推送和分支收束。
   About 已通过 `gh repo edit` 保存，并回读确认：
   `Research Skills for checking paper claims, surfacing evidence conflicts, and turning ideas into testable questions.`
2. **实际工作位置与 Git 状态**：`C:\personal research skill`，当前分支 `master`。
   README/图工作起点为 `209f4d0ed4b3f83801bc3cde6099a0a56e77e3b3`，合并阶段起点为 `f189dd6`，两阶段开始时工作树均干净。
   README、对照图和交接更新已提交为 `d21b2fa8e420aaaae9f7b32a8f89d35fa45c6533`，
   连同此前的 `7529d36`、`209f4d0` 一并推送至 `origin/codex/delivery-fixes`，远端 SHA 已核对。
   用户澄清常规交付应直接合并。已将四个交付提交快进合入 `master` 并推送至
   `origin/master`，远端 SHA 核对为 `f189dd63652674a35fa2c7fc2458b3645b0a0409`，交付分支已清理。
   本节完成状态补录随后单独提交至 `master`；最新提交和同步状态使用 `git log -1`、
   `git status --short --branch` 核对。默认分支已包含新 README 和对照图；About 已生效。
3. **交付物绝对路径**：
   - `C:\personal research skill\README.md`、`C:\personal research skill\README.zh-CN.md`。
   - 图源：`C:\personal research skill\docs\assets\u-mamba-evidence-comparison.svg`。
   - 实际渲染预览：`C:\Users\34638\AppData\Local\Temp\prs-u-mamba-evidence-comparison-20261004.png`
     （临时预览；正式产物是上述 SVG）。
4. **本轮实际验证**：About 回读一致；SVG XML 可解析，无脚本、外部资源或嵌入页面；
   使用已有 Sharp 渲染为 1200×770 PNG 并实际查看，文字无截断；两个 README 的 19 个不同本地链接目标存在。
   图中数值和基础回答摘录与归档文件匹配，`git diff --check` 通过。
   提交前于 2026-10-04 重新执行项目完整验证：90 项测试、仓库校验和演示运行记录校验均通过。
   首次受限执行的 32 项错误来自临时目录 `WinError 5`；获准环境重跑同一组命令后通过，未据此修改代码。
   推送后的 GitHub Actions 运行 `37196972802`（提交 `d21b2fa`）实际完成并成功：
   Ubuntu/Windows × Python 3.10/3.12 四项任务均通过。
   入口：`https://github.com/1second1/personal-research-skills/actions/runs/37196972802`。
   合并阶段在 `master` 上再次实际重跑：90 项测试、仓库校验、演示运行记录校验和 `git diff --check` 均通过。
5. **事实修正与授权边界**：两份 r1 回答都发现数值冲突。Skill 回答虽然声明 `±` 未定义，
   后文仍推断变异性；原 README 对它的描述过宽，现已修正并在图中展示此问题。
   这里只描述原始文本，没有裁定 R004，也没有改写旧输出、评分或冻结方案。
   图仅概括 2026-09-20 归档的一对回答，不能证明普遍提升。本轮没有启动模型生成。
   用户本次澄清常规交付由 Agent 完成合并、推送和已合并分支清理，无需用户去官网操作。
   本次已按此完成；实验候选未晋升，未启动模型生成，其余推广建议和新版本发布未执行。
6. **分支收束**：`feature/github-ready-framework` 已确认是 `origin/master` 的祖先，独立提交数为 0。
   其工作树没有未保存工作，忽略内容仅为三份 Python 缓存；已删除该本地分支及
   `C:\personal research skill\.worktrees\github-ready-framework` 工作树。
   `codex/delivery-fixes` 已快进合入 `master`；在核对远端 `master` 同步后，已删除该本地和远端分支。
   `codex/uncertainty-v2-candidate` 保留，仍有未晋升的候选改动和一个本地交接提交，不能作为已合并分支删除。
   远端两个 Dependabot PR #1 和 #2 仅更新 `checkout@v7` 与 `setup-python@v7`；
   两个版本已经存在于 `origin/master`，因此已关闭这两个过期重复 PR、删除对应远端分支，并 fetch/prune 核对。
   主目录中的 `.local-project-materials`、`evals/local` 和现有 `.venv` 不属于分支清理目标。

### 历史记录：交付收束与诊断 — 2026-10-03

本节保留 2026-10-03 的工作记录；续做前核对开头当前状态与实际 Git 状态。

1. **当前目标**：收束 delivery-fixes 的交付修复，应用少量全局规则，补齐独立诊断与交接口径。
   本轮完成本地验证和三个小任务验收；没有启动模型效果研究。
2. **实际工作位置与 Git 状态**：`C:\personal research skill`，分支 `codex/delivery-fixes`。
   交付修复单独提交为 `7529d365fbd0358478fcead880e99bb1d857828d`；本节与评测协议随其后的独立文档提交保存。
   本轮只做本地提交，未推送、未发布；远端 CI 未在本轮执行。续做时运行 `git status --short`、
   `git log -2 --oneline` 核对最新状态，不依赖历史 `master` 标签。
3. **交付物绝对路径**：
   - 当前交接：`C:\personal research skill\docs\AGENT-HANDOFF-PLAN.md`。
   - 交付代码：`C:\personal research skill\research_skills`；回归测试：`C:\personal research skill\tests`。
   - 效果诊断规范：`C:\personal research skill\evals\PROTOCOL.md`。
   - Codex 全局规则：`C:\Users\34638\.codex\AGENTS.md`（独立于本仓库，四处定点改写已应用）。
   - 小任务验收：`E:\freedom\harness-acceptance-20261003\README.md`，原始轨迹与精确提示词同目录保存。
4. **本轮实际运行的验证**：使用项目 `.venv`，设置 `PYTHONUTF8=1`、`PYTHONIOENCODING=utf-8`、
   `PYTHONDONTWRITEBYTECODE=1`，重新执行 `python -m unittest discover -s tests -v`，90 项通过；
   `python -m research_skills.cli validate`、`validate --run evals/fixtures/run-record-demo/run.yaml`、
   `git diff --check` 均通过。三类独立 CLI 会话得到正确产物、无需确认且未冒用历史验证；
   这是本轮实际观察，不是普遍可靠性或新旧指令效果对比。新会话续做使用预置交接材料，
   尚未验证任意中断后的恢复。PATH 中旧 CLI 0.145.0 的模型兼容失败已保留，后续使用本机已有的
   0.160.0；没有升级程序、改 PATH 或切换模型。续做会话有一次无关的 `resume|简历` 记忆检索，
   原因未验证，未据此改写全部 Skill。
5. **未完成事项与授权边界**：实际模型效果、独立语义复审和任意中断恢复仍未验证。
   36 次前瞻性研究保持暂停；旧九份输出/评分和封存材料没有改写，uncertainty-v2 没有晋升。
   本轮检查私有包目录未发现 outputs/runs/raw-outputs；这不是重新核验整包 seal 的结果。
   后续先按真实任务观察流程开销；若要恢复研究、修改冻结方案、推送或发布，需要新的明确指示。
   新诊断仅供未来授权评测，不追溯改变历史评分，也不修改现有冻结方案。

### 历史记录：Delivery fixes — 2026-10-03

The user stopped the proposed 36-run model evaluation and requested delivery
fixes and a focused quality review. Do not start that evaluation or create a
model-provider revision from the earlier DeepSeek discussion without a new
request. Its ignored materials remain intact; the candidate uncertainty-v2
branch remains a separate, unpromoted experiment.

Delivery work is on `codex/delivery-fixes`, based on the public release line.
The fixes cover LF context output on Windows, fenced-code false positives,
actual YAML frontmatter validation and preflight rejection of external blind
review records. Regression assertions were observed failing before the
implementation changes. CI is configured for Ubuntu/Windows and Python
3.10/3.12; local verification does not claim those remote jobs have run.
On 2026-10-03 the local Windows Python 3.12 environment passed all 90 tests,
repository validation and the demo run-record check. Use the existing `.venv`
with `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8` and `PYTHONDONTWRITEBYTECODE=1`.

No model-effect claims, Skill contract/version changes or edits to historical
model outputs/scores are part of this work. Publishing, release and external
promotion remain separate actions.

### 历史记录：Implementation status — updated 2026-09-23

The configuration parser now requires PyYAML (install with `python -m pip install -e .`).
Profiles and contracts are validated; full contracts and workflows reach composed
contexts. `run_skill.py --mode baseline|skill|profile` supports controlled comparisons.
The installed `research-skills` command supports stdin and direct UTF-8 file output.
Repository validation discovers all Profile and Skill directories rather than a fixed list.
The CLI now exposes explicit `compose`, `list`, `validate`, `evaluate`, and
`blind` commands while retaining the original compose form. The generic
evaluator covers every public Skill and emits versioned JSON. Run records use a
public schema with SHA-256 integrity checks; blinded exports separate reviewer
files from the private condition key. None of these deterministic checks
establish semantic entailment. See `evals/PROTOCOL.md`.
The historical commit and status below describe the original handoff, not current HEAD.
The first `PR-REAL-01` comparison now contains nine validated model runs and a
best-effort blinded single-agent review. Skill-only outscored baseline, while
the profile did not improve on Skill-only. Next: obtain independent review and
turn the observed `±` attribution failure into a versioned feedback proposal.

> This is the historical design and cross-agent handoff record. The opening update,
> README, CHANGELOG, tests, and current Git state define implementation status.

**Repository:** <https://github.com/1second1/personal-research-skills>

**Historical branch at original handoff:** `master`

**Historical project commit at original handoff:** `442eb62`

**Primary maintainer:** `1second1`

**Document language:** Chinese for project intent and decisions; English for code, public APIs, Skill names, contracts, and provider adapters.

---

## 1. What this project is

Personal Research Skills is a provider-neutral framework for turning a person's research methodology into composable, testable AI Skills.

The project is not intended to clone a person, create a generic chatbot, or become a prompt collection. Its core proposition is:

> A reusable AI Skill should inherit a research methodology, expose an explicit contract, separate evidence from inference, and remain evaluable across agent runtimes.

The repository has two roles:

1. **Framework:** Any researcher should be able to define values, thinking rules, workflows, preferences, and Skills.
2. **Reference implementation:** The maintainer's personal Reasoning DNA is the first complete public example.

This distinction is essential. The project is not “an AI that copies the maintainer.” It is “a framework that lets any user encode and evolve a research methodology,” with the maintainer's profile as the reference implementation.

---

## 2. How the idea evolved

The original project discussion considered several directions:

- a lightweight image-caption generator;
- an AI Research Copilot for papers, formulas, diagrams, experiments, and reproduction plans;
- a GitHub Repository Copilot for architecture, dependencies, README generation, and learning paths;
- an AI Prompt OS combining memory, workflows, reasoning, evaluation, and versioning;
- an AI GitHub Mentor for repository and contribution analysis;
- a Local AI Workspace combining files, PDF, Markdown, GitHub, terminal, browser, notes, and MCP-style tools.

The small image-caption project was rejected as a portfolio flagship because it was too close to a generic AI wrapper and demonstrated limited research or engineering depth.

The long-term product vision remains closest to an **AI Research Copilot**, but the stable implementation order starts lower in the stack:

```text
Personal methodology
        ↓
Reasoning DNA profile
        ↓
Provider-neutral Skill contract
        ↓
Agent adapter
        ↓
Evidence-grounded research workflow
        ↓
Optional PDF / GitHub / model / RAG / experiment integrations
```

The project should not jump directly to a large multi-tool agent. The methodology and evaluation layer must be stable first, otherwise the system will become a collection of integrations without a defensible identity.

---

## 3. The maintainer's methodology model

The central model is a hierarchy, not a single prompt:

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
Skill Runtime
```

### 3.1 Values

The current reference profile prefers:

- long-term value over short-term novelty;
- principles over tricks;
- reusable systems over one-off answers;
- evidence before confidence;
- smaller verifiable claims over broad unsupported conclusions.

Values define what counts as a good decision. They are more stable than formatting preferences and must not be buried in individual Skills.

### 3.2 Thinking: Inquiry Pattern

The most important personal asset identified in the discussion is not a fixed “Reasoning Signature,” but a recurring inquiry pattern:

```text
What
  ↓
Why
  ↓
Assumption
  ↓
Boundary
  ↓
Connection
  ↓
Application
  ↓
Value
```

This pattern explains why the maintainer repeatedly asks:

- What is it?
- Why does it work?
- What assumptions does it make?
- Where does it stop working?
- How is it related to other concepts?
- How can it be applied?
- What long-term value does it create?

`Reasoning DNA` is the preferred project term because it describes an inherited methodology rather than a superficial personality signature. It must remain revisable and versioned; it is not an immutable identity claim.

### 3.3 Workflow

Workflows are actions and sequences, not values:

```text
Research:
Question → Evidence → Inference → Boundary → Experiment → Review

Paper reading:
Problem → Evidence → Inferences → Assumptions → Boundaries → Connections → Next Actions
```

### 3.4 Preferences

Current preferences include:

- Chinese-first explanation with English technical terms when useful;
- structured Markdown;
- YAML or JSON when it improves inspectability;
- Mermaid when it clarifies structure or flow;
- high information density without hiding uncertainty.

Preferences can change more easily than values or thinking rules. They must not be used as the primary definition of the framework.

---

## 4. Current repository state

The current public repository contains:

- `profiles/reasoning-dna.yaml` — the first reference profile;
- `research_skills/dna.py` — a PyYAML-based loader with duplicate-key and type validation;
- `research_skills/compose.py` — profile and Skill text composition;
- `skills/paper-reading/` — evidence-grounded paper reading instructions, contract, examples, and evaluation material;
- `skills/research-question/` — bounded and falsifiable research-question instructions, contract, and examples;
- `skills/argument-analysis/` — genre-aware argument reconstruction for essays, editorials, interviews, and policy prose;
- `scripts/run_skill.py` — a deterministic composition CLI;
- `scripts/validate_repository.py` — repository shape validation;
- `research_skills/evaluation.py` — generic deterministic output evaluation;
- `research_skills/run_records.py` — versioned run-record and artifact-integrity checks;
- `research_skills/blinding.py` — reproducible reviewer export with a private condition key;
- `scripts/evaluate_paper_reading.py` — compatibility wrapper for the original command;
- `tests/` — the regression suite; always use a fresh run rather than a stored count;
- `.github/workflows/validate.yml` — GitHub Actions validation;
- `README.md` — English public entry point;
- `README.zh-CN.md` — Chinese explanation;
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `RELEASE.md`, and MIT License.

The last verified commands were:

```bash
python -m unittest discover -s tests -v
research-skills validate
research-skills evaluate \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml \
  --source evals/fixtures/paper-reading-demo/source.md \
  --format json
research-skills compose paper-reading skills/paper-reading/examples/input.md
research-skills compose research-question skills/research-question/examples/input.md
```

The public GitHub Actions run for the presentation update passed. Do not treat this as evidence that a model's research output is correct; it only proves repository and fixture checks.

---

## 5. Objective quality assessment at handoff

The project is a solid early prototype, not yet a mature AI product or a flagship research system.

### Strengths

- clear distinction between framework and personal reference profile;
- explicit separation of facts, inferences, assumptions, boundaries, and actions;
- reproducible repository structure;
- no required API key or private data;
- working tests and CI;
- provider-neutral Markdown and YAML artifacts;
- English public README plus Chinese project explanation;
- honest non-goals and explicit runtime limitations.

### Current weaknesses

1. `run_skill.py` reads the input and composes a complete execution context, but it still does not execute a model.
2. The evaluator checks structure, source labels, and numeric presence. It is a rejection filter, not a semantic judge.
3. `PR-REAL-01` includes a nine-run three-condition comparison, but it is still analysis of a curated source map rather than an independent reproduction of the paper.
4. The comparison has one semantic reviewer; condition style may have weakened blinding, and independent human review is still pending.
5. PDF ingestion and code execution are still manual; there is no provider-neutral adapter layer.
6. The Reasoning DNA is hand-authored. In the first repeated comparison it did
   not improve on Skill-only; broader benefit has not been established.
7. Feedback-to-rule evolution has not yet been implemented as a versioned, reviewable artifact.

The correct status language is therefore:

```text
GitHub-ready prototype
Methodology framework
Reference implementation
Not yet a model-serving system
Not yet empirically validated as a reasoning improvement
```

---

## 6. Stable engineering path

The project should evolve through additive layers. Avoid a large rewrite, a framework migration, or a model dependency until the lower layer is stable.

### Layer A: Stable public specification

Define a versioned provider-neutral schema for:

```text
Profile
Skill
Contract
Input
Output
Evaluation
Feedback
```

The canonical artifacts remain human-readable Markdown and YAML-compatible files. Every schema change must include a migration note and a backward-compatibility decision.

### Layer B: Pure core runtime

Keep the core runtime dependency-light and deterministic:

```text
load_profile(path)
load_skill(path)
load_contract(path)
compose_context(profile, skill, contract, input)
validate_artifacts(...)
```

The core must not know whether the final agent is Codex, Claude Code, Gemini CLI, a local model, or a hosted API.

### Layer C: Provider adapters

Adapters translate the same composed context into provider-specific files or calls:

```text
core context
   ├── Codex adapter
   ├── Claude Code adapter
   ├── Gemini / other CLI adapter
   └── generic Markdown / stdin adapter
```

The adapter layer may change as external agent products change. The profile, Skill contracts, and evaluations must remain provider-neutral.

Adapter rules:

- never duplicate the Reasoning DNA in multiple provider files;
- generate provider files from the canonical profile and Skill;
- preserve the source version and hash in generated output;
- keep generated files distinguishable from hand-authored files;
- test each adapter with a golden output fixture;
- verify actual provider conventions before implementation because agent software formats can change.

### Layer D: Evaluation harness

The evaluation harness must compare behavior, not just file presence:

```text
same input
  ├── no Skill
  ├── Skill only
  └── Skill + Reasoning DNA
```

It should score at least:

- evidence coverage;
- fact/inference separation;
- unsupported-claim rate;
- boundary quality;
- assumption coverage;
- actionability;
- format compliance;
- stability across repeated runs.

The first evaluation can be human-scored with a small rubric. An automated judge or model-based evaluator must be added only after the rubric is explicit and checked against examples.

### Layer E: Optional integrations

Only after Layers A–D are stable should the project add:

- PDF extraction;
- arXiv or paper metadata;
- GitHub repository inspection;
- local files and notes;
- RAG or vector search;
- model providers;
- experiment execution;
- memory and feedback storage.

Each integration must be an optional adapter. The core Skill should remain usable without network access or API keys.

---

## 7. Recommended implementation sequence

### Phase 0 — Correct the current semantic mismatch

Priority: **P0**

Do not add more Skills before this is complete.

Tasks:

1. Rename the internal concept from “run” to “compose” where it only generates context, or make the CLI actually include the input contents.
2. Load `contract.yaml` together with `SKILL.md`.
3. Include the input document in the composed context with a clear delimiter.
4. Include profile version, Skill version, contract version, and source paths.
5. Add tests proving that changing the input changes the output.
6. Add tests proving that contract fields appear in the output.
7. Keep the old invocation working for backward compatibility.

Acceptance criteria:

```text
The CLI does not silently ignore input content.
The contract is included or explicitly validated.
The old repository examples still pass.
```

### Phase 1 — Establish real forward evaluations

Priority: **P0**

Current status: the source-verified `PR-REAL-01` U-Mamba fixture, generic
rubrics, run-record schemas, integrity validation, blind-review export, nine
model outputs, and a scored single-agent review are complete. The remaining
Phase 1 work is independent second review and adjudication; do not mislabel the
curated reference answer as a model run or this analysis as paper reproduction.

For both existing Skills, create the same prompt scenarios in three modes:

1. no Skill;
2. Skill without personal profile;
3. Skill plus Reasoning DNA.

Use the synthetic fixture and the U-Mamba real-paper source map. Store future
model-run artifacts outside the public tree until reviewed, then publish only
redacted records with this shape:

```text
evals/
├── scenarios/
├── baselines/
├── outputs/
├── rubrics/
└── reports/
```

Do not claim improvement from one anecdotal output. Record the exact input, model/runtime, date, configuration, and evaluator rubric.

### Phase 2 — Add a provider-neutral execution interface

Priority: **P1**

Define a small interface such as:

```python
class AgentAdapter(Protocol):
    def render(self, context: ComposedContext) -> str: ...
```

Start with a `markdown` adapter and a `stdin` adapter. Add Codex and Claude Code adapters only after their target file conventions are verified.

The first interface should render context, not call a model. This keeps tests deterministic and avoids coupling the project to one vendor.

### Phase 3 — Package the core cleanly

Priority: **P1**

Move toward a standard package layout only when the current API is stable:

```text
src/personal_research_skills/
├── profiles.py
├── skills.py
├── contracts.py
├── compose.py
├── adapters/
└── evaluations/
```

Keep compatibility shims for the current `research_skills` import and original
CLI form until the migration is complete. The console entry point and explicit
subcommands now exist; future packaging changes must preserve them or include a
migration note.

### Phase 4 — Add feedback without pretending to learn

Priority: **P1**

Create explicit, reviewable feedback artifacts:

```yaml
feedback_id: ...
target: paper-reading
observed_failure: inference presented as evidence
evidence: evals/reports/...
proposed_rule: ...
status: proposed
```

The system should not automatically rewrite the Reasoning DNA. A human or explicitly authorized agent must review a proposed change, run regression evaluations, and record a version bump.

This is the safe interpretation of “Reasoning Evolution”: evolution of a versioned methodology under evidence, not opaque personality imitation.

### Phase 5 — Build the AI Research Copilot layer

Priority: **P2**

Only after the earlier phases are stable, compose workflows such as:

```text
paper intake
  → evidence extraction
  → formula / method explanation
  → architecture diagram
  → paper-to-code mapping
  → reproduction checklist
  → experiment plan
  → results review
  → research report
```

Each node should be an independently testable Skill or adapter. Do not build one large autonomous agent first.

---

## 8. Future expansion directions

### Research workflows

- `codebase-analysis`: map a repository's modules, dependencies, and execution path;
- `paper-to-code`: connect paper claims to implementation files and configuration;
- `experiment-design`: define variables, controls, metrics, seeds, and stopping conditions;
- `experiment-review`: separate observed results from interpretation;
- `research-writing`: turn verified evidence into a report or README;
- `interview-preparation`: convert research understanding into defensible explanations.

### Tool integrations

- PDF and structured paper extraction;
- arXiv or DOI metadata;
- GitHub repository and issue context;
- local Markdown notes and project files;
- browser or MCP-compatible tools;
- local model or hosted model adapters;
- optional vector retrieval for large personal corpora.

### Evaluation and evolution

- regression corpus of failure cases;
- human rubric plus automated checks;
- model/provider comparison;
- repeated-run stability analysis;
- versioned Reasoning DNA changes;
- explainable feedback proposals;
- per-Skill compatibility matrix.

### Product direction

The eventual product can become a local research workspace combining:

```text
PDF + Markdown + GitHub + Notes + Terminal + Browser
                       ↓
              provider-neutral Agent Runtime
                       ↓
          personal methodology + research Skills
```

This should remain an optional application layer over the stable core, not the foundation of the repository.

---

## 9. Rules for every future Agent

Before changing the project:

1. Read this file, `README.md`, the current `reasoning-dna.yaml`, and the target Skill.
2. Inspect `git status`, recent commits, and current tests.
3. State whether the requested change is framework, profile, Skill, adapter, evaluation, or documentation work.
4. Do not perform a broad rewrite when an additive migration is possible.
5. Use test-first development for code and pressure/evaluation scenarios for Skills.
6. Preserve the distinction between source evidence, inference, assumption, boundary, and recommendation.
7. Do not claim a model result, benchmark, or compatibility that was not actually tested.
8. Keep provider-specific details in adapters.
9. Keep private conversations, private papers, credentials, and personal data out of the public repository.
10. Run the full verification commands before committing.

Before claiming completion:

```bash
python -m unittest discover -s tests -v
research-skills validate
research-skills validate --run evals/fixtures/run-record-demo/run.yaml
research-skills evaluate \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml \
  --source evals/fixtures/paper-reading-demo/source.md \
  --format json
git diff --check
git status --short --branch
```

If the change affects GitHub Actions, run or inspect the resulting remote workflow before claiming CI success.

---

## 10. If context or quota is limited

Use this priority order:

### Must do first

- obtain an independent second review of the nine published `PR-REAL-01` runs and retain disagreements;
- adjudicate the disputed interpretation of undefined `±` values without revealing condition labels during scoring;
- preserve tests and backward compatibility;
- document exact limitations.

### Do next

- add a versioned feedback artifact;
- add a provider-neutral model execution interface and Markdown/stdin adapter;
- add `codebase-analysis` only after the first Skill evaluation is credible.

### Defer safely

- hosted model integration;
- vector database and RAG;
- PDF parsing;
- browser automation;
- large web UI;
- multi-agent orchestration;
- automatic profile rewriting;
- SaaS deployment and authentication.

When time is short, leave a passing test and a precise issue rather than a half-integrated feature.

---

## 11. Suggested first prompt for another Agent

Copy the following prompt when handing this repository to another coding agent:

```text
Read docs/AGENT-HANDOFF-PLAN.md, README.md, profiles/reasoning-dna.yaml,
and the target Skill before making changes.

Current priority: independently review the nine published `PR-REAL-01` outputs
without opening their condition-labeled run records. Score the five documented
dimensions, quote evidence for each deduction, record suspected unblinding,
then compare against `comparison-2026-09-20/review-scores.yaml` and retain every
disagreement. The current result is negative for incremental profile value and
must remain so unless a documented adjudication changes the scores.

Do not treat the curated reference answer as a model run, and do not add a
database, web UI, automatic profile rewriting, or provider-specific product
integration in this task. Use TDD for code changes and pressure scenarios for
Skill changes. Run the full verification commands before committing. Report
exact files changed, test output, remaining limitations, and the commit hash.
```

---

## 12. Final architectural decision

The stable path is:

```text
versioned methodology schema
        ↓
deterministic provider-neutral core
        ↓
independently testable Skills
        ↓
evaluation and feedback records
        ↓
thin provider adapters
        ↓
optional research tools and model integrations
```

Do not reverse this order.

The project's long-term defensibility will not come from having the most integrations. It will come from making a research methodology explicit, testable, portable across agent software, and improvable through evidence.
