# Week 1 Checklist

## 目标

完成项目公开协作所需的方法论基线、仓库骨架、边界说明和贡献入口。

## 已完成

- [x] 项目 README：一句话定位、当前状态、项目结构、贡献入口、非目标
- [x] `researcher-example.yaml`：Values、Inquiry Pattern、Workflow、Preference
- [x] 方法论说明：四层结构、Evidence/Inferences/Recommendations、演化规则
- [x] 兼容性说明：Codex、Claude Code、普通 Markdown、未实现 Runtime
- [x] 贡献规范：Skill 目录、样例、评测、风险和变更记录
- [x] 评估入口：第一阶段指标和基线任务
- [x] `paper-reading` Skill：契约、合成输入、预期证据卡片与压力场景
- [x] 本地校验器：`scripts/validate_repository.py`
- [x] 证据卡片评测器：`scripts/evaluate_paper_reading.py`
- [x] 自动测试：`tests/test_validate_repository.py` 与 `tests/test_evaluate_paper_reading.py`
- [x] GitHub 协作文件：CI、Issue 表单、PR 模板、贡献与安全政策

## 本周验收标准

- [x] 外部读者可以在 5 分钟内理解项目做什么
- [x] 外部贡献者知道如何提交一个 Skill
- [x] Profile 可以被独立阅读，不依赖聊天上下文
- [x] README 没有把未实现的 Runtime 描述为已经存在
- [x] 第一周没有创建未经测试的生产 Skill
- [x] `python -m unittest discover -s tests -v`：4 个测试通过
- [x] `python scripts/validate_repository.py`：仓库契约通过
- [x] `python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml`：合成 Demo 通过

## 下一周入口

下一周对 `paper-reading` 做独立 Agent 前向测试：运行 `skills/paper-reading/evals/pressure-scenarios.md` 中的三个场景，记录没有 Skill 和加载 Skill 时的原始输出，再决定是否扩展到 `codebase-analysis`。
