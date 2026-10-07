# Try one manuscript audit

[中文试用](#中文试用) · [All four Skills](../README.md#available-skills)

Start with `manuscript-audit` in a working Codex or Claude Code project.
Your agent supplies model access and tools; this repository supplies the Skill.
Node.js and `npx` are needed for installation. Python is optional unless you use
the framework or rerun the complete teaching case.

```text
npx skills add 1second1/personal-research-skills --skill manuscript-audit --agent codex --agent claude-code --copy --yes
```

## Copy this request

Paste this request into your agent after installation. It uses a short excerpt
from the [archived synthetic teaching case](../evals/cases/manuscript-audit-demo/README.md).
No private paper, repository clone, or new experiment is needed to inspect it.

```text
Use manuscript-audit to audit only the synthetic excerpt below.
Locate each concern, distinguish source facts from calculations and inference,
and propose the smallest repair. Do not claim you executed code or checked files
that are not attached. Do not edit anything yet.

Synthetic teaching excerpt:
- Manuscript claim: "Our result demonstrates generalization to previously unseen patients."
- Manuscript table: Test accuracy = 0.930000.
- Saved result: correct = 12, n_test = 12, accuracy = 1.0.
- Training patient IDs: P001, P002, P003, P004, P005, P006,
  P007, P008, P009, P010, P011, P012.
- Test patient IDs: P001, P002, P003, P004, P005, P006,
  P007, P008, P009, P010, P011, P012.
- These are generated identifiers and signals, not patient records.
```

## Inspect the answer

Look for a report organized as **Summary → Findings → Checks → Repair Plan → Recheck**.
For this excerpt, the deciding evidence is:

| Concern | Evidence to preserve | Bounded next action |
|---|---|---|
| Previously unseen patients | All 12 listed IDs appear in both sets | Narrow the claim to held-out observations of seen synthetic patients, or obtain a patient-disjoint experiment |
| Reported accuracy | The table says 0.93; the saved counts give 12/12 = 1.0 | Reconcile the manuscript with the deciding run artifact; keep the conflicting values visible until the run is identified |

These are checks for this prepared excerpt, not a recorded model response or a
guarantee about your agent. It must distinguish inspecting supplied text from
executing code. An excluded concern is useful too; an audit does not need a
fixed number of accusations.

## Follow the repair and recheck

The [complete case](../evals/cases/manuscript-audit-demo/README.md) includes
code, configurations, saved failures, a repair diff, and a revised result:

| Check | Original | Revised |
|---|---|---|
| Shared training/test patient IDs | 12 | 0 |
| Saved accuracy | 12/12 = 1.0 | 4/16 = 0.25 |
| Manuscript accuracy | 0.93, inconsistent | 0.25, consistent |

The test sets differ, so the accuracy change is not a controlled estimate of
leakage's effect. The lesson is a traceable repair, not better model performance.
The case reports were authored during implementation; they are not independent
model evaluations.

For your own work, attach the manuscript and available code, configuration and
result files. Ask for an audit first. Authorize edits separately, then provide
the revised material and previous audit for recheck. Missing material remains
an evidence limit, and unavailable checks remain unrun.

[Share a useful result or failure](https://github.com/1second1/personal-research-skills/issues/new?template=usage_feedback.yml)
using public or synthetic excerpts. Keep unpublished drafts and credentials private.

## 中文试用

在已经能正常使用 Codex 或 Claude Code 的项目中，运行上面的单行安装命令，
然后把以下请求复制给 Agent：

```text
使用 manuscript-audit，只审查下面这段合成教学摘录。
定位每项质疑，区分来源事实、计算和推断，并给出最小修复。
不要声称执行了代码或检查了未提供的文件。先不要修改任何内容。

合成教学摘录：
- 稿件主张：“结果证明模型能够泛化到此前未见过的患者。”
- 稿件表格：测试准确率 = 0.930000。
- 保存结果：正确数 = 12，测试数 = 12，准确率 = 1.0。
- 训练患者 ID：P001、P002、P003、P004、P005、P006、
  P007、P008、P009、P010、P011、P012。
- 测试患者 ID：P001、P002、P003、P004、P005、P006、
  P007、P008、P009、P010、P011、P012。
- 这些是生成的标识符和信号，不是真实患者记录。
```

检查回答是否保留两项具体矛盾：12 个 ID 全部重叠，与“未见过患者”不符；
`12/12 = 1.0` 与稿件的 `0.93` 不符。回答应定位来源，提出限定主张或核对结果的
具体修复，并诚实记录执行情况。这是准备好的试用请求与检查标准，不是已经生成的模型回答。

[完整案例](../evals/cases/manuscript-audit-demo/README.md)保留了原始失败、修改差异和复查：
修订后患者交集为空，实际成绩为 `4/16 = 0.25`，稿件也报告 `0.25`。
两个版本测试集合不同，成绩变化不能当作泄漏影响的受控因果估计；教学报告也不能当作独立模型评测。

换成自己的稿件时，提供已有代码、配置和结果，先审查，再授权必要修复，最后带上旧审查报告复查。
可以[用中文反馈帮助或误判](https://github.com/1second1/personal-research-skills/issues/new?template=usage_feedback.yml)，
只分享公开或合成摘录，未发表材料保留在本地。
