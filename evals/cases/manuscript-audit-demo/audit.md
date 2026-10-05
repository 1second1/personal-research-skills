## Summary

这是本次实现过程中整理的合成案例参考报告，不是独立评测模型输出。已读取原稿、配置、CSV、分类程序及实际运行结果；执行记录见 [original/execution.json](original/execution.json)。原版本检出患者重叠和报告数值冲突；组件归因证据不足；训练集归一化质疑被实际检查排除。尚未以此证明 Skill 优于其他提示。

## Findings

### MA-001 — 新患者主张与划分冲突

- **Location and claim**：原稿 Abstract 声称对此前未见患者泛化；Methods 按每位患者最后一个样本留出；`original/config.json` 的 `split.unit` 为 `sample`。 [Source: original/manuscript.md — Abstract, Methods] [Source: original/config.json — split]
- **Judgment**：`confirmed_error`，针对“测试患者未见过”的实验前提。
- **Evidence**：`original/result.json` 的 train/test patient-ID 集合交集为 P001 至 P012，共 12 个患者；不是仅由文字推测的泄漏风险。 [Source: original/check.json — checks.patient_disjoint]
- **Impact**：原测试不能验证新患者主张。`Inference:` 身份相关信号可能有利于同患者匹配；本次没有隔离其对成绩的因果贡献。
- **Minimal check**：取训练与测试患者集合交集；空集可排除这条重叠路径，非空则该划分不满足新患者前提。
- **Execution and result**：`executed`；`verify.py` 原版本退出码 1，交集非空。
- **Repair**：改为患者级留出 P003、P006、P009、P012，重新计算预测，并将结论限于这一个合成划分。
- **Resolution and recheck**：初审 `open`；修复后状态见 [recheck.md](recheck.md)。

### MA-002 — 表格与原始预测不一致

- **Location and claim**：原稿 Results 的 Test accuracy 为 0.930000。 [Source: original/manuscript.md — Results]
- **Judgment**：`confirmed_error`，针对该表格与本版本评测输出的对应关系。
- **Evidence**：实际预测 12 项均正确，准确率 12/12 = 1.0。原始运行、CSV 和配置的哈希已写入结果；重新执行得到相同预测。 [Source: original/result.json — metrics, predictions, input_digests] [Source: original/check.json — reported_accuracy_matches, result_matches_rerun]
- **Impact**：影响准确成绩的引用；原版本的 1.0 同时受 MA-001 的实验边界限制。
- **Minimal check**：逐项比较 truth 和 prediction，除以实际评测样本数，再核对 Results 表格。显示保留六位小数，比较容差为 0.0000005。
- **Execution and result**：`executed`；重算为 1.0，表格为 0.93，匹配检查失败。
- **Repair**：修复划分后使用新预测的 4/16 = 0.25，表格及摘要统一报告其范围。
- **Resolution and recheck**：初审 `open`；修复后状态见 [recheck.md](recheck.md)。

### MA-003 — 组件贡献和必要性未被检验

- **Location and claim**：原稿 Component interpretation 称归一化导致提升且不可缺少。 [Source: original/manuscript.md — Component interpretation]
- **Judgment**：`evidence_gap`。
- **Evidence**：给定程序和结果只有一个完整模型、一个划分，没有归一化开关的受控比较，也没有从头不使用该组件的学习实验。此判断只覆盖提供的合成包。 [Source: experiment.py — run_experiment] [Source: original/result.json — limits]
- **Impact**：影响因果贡献和必要性主张，不能据此声称归一化没有用。
- **Minimal check**：已有匹配条件的 with/without 结果若存在，检查其差异；不存在时，撤回归因或再设计受控比较。局部去除不能替代整组干预，推理时可去除不能证明训练时不需要。
- **Execution and result**：`executed`，仅执行材料检查；未运行组件消融或训练。程序检查器明确不评估此类语义判断。
- **Repair**：收窄为完整模型在给定合成划分的观察结果；保留“未隔离归一化贡献”的限制。
- **Resolution and recheck**：初审 `open`；修复通过措辞收窄解决，不证明原因果主张。

### MA-004 — 测试数据参与归一化拟合的质疑被排除

- **Location and claim**：Methods 声称仅以训练集拟合缩放；程序 `run_experiment` 调用 `fit_normalizer(train)`。 [Source: original/manuscript.md — Methods] [Source: experiment.py — run_experiment, fit_normalizer]
- **Judgment**：`excluded`，针对给定程序本次运行的拟合路径。
- **Evidence**：拟合样本列表与 36 个训练样本完全一致；独立重算均值和尺度一致。仅将测试样本 feature_1 加 10000，归一化参数保持不变。 [Source: original/check.json — normalizer_train_only]
- **Impact**：这条拟合泄漏路径被排除，患者重叠问题 MA-001 仍存在。
- **Minimal check**：核对 fit sample IDs、训练集统计量及测试数据扰动前后参数。任一不一致会重新支持质疑。
- **Execution and result**：`executed`；三个条件均通过。
- **Repair**：无需修改该拟合路径。
- **Resolution and recheck**：`not_applicable`；修复版继续核对该排除依据。

## Checks

原版本 `experiment.py` 退出 0；`verify.py` 退出 1，因为 patient_disjoint 和 reported_accuracy_matches 失败。拟合范围、预测重算及输入哈希通过。原始 JSON 保存所有预测，不仅保存汇总成绩。命令、时间、标准输出、标准错误和退出码均见执行记录。

## Repair Plan

用户已授权该教学案例修复。保留 original；修改 revised 的配置与稿件。顺序为：患者级划分 → 实际重算 → 依据新输出修正稿件 → 收窄归因 → 同一程序复查。差异见 [repair.diff](repair.diff)。

## Recheck

见 [修复后复查](recheck.md)。程序通过只覆盖患者交集、数值对应、拟合路径、重算和哈希；组件措辞需要另行核对正文。无模型比较结果，无真实医学或跨数据集有效性结论。
