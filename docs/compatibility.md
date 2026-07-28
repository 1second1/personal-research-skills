# Compatibility

## 当前支持方式

第一阶段使用 Agent-compatible 的 Markdown 与 YAML 文件，不依赖专用后端。

| 环境 | 当前状态 | 说明 |
|---|---|---|
| Claude Code | 目标环境 | 可将每个 Skill 目录放入项目级 Skills 目录 |
| Codex | 目标环境 | 可通过项目上下文和 Skills 目录加载方法论与 Skill |
| 普通 Markdown 阅读器 | 支持 | 可以阅读全部方法论和契约文件 |
| 自动 Runtime | 未实现 | Planner、Scheduler、Memory 和 Learner 不属于第一周交付 |

## 兼容性原则

- `SKILL.md` 保持自包含，不能依赖只有某一个模型知道的隐式上下文。
- 方法论 Profile 与具体 Skill 分离，便于替换个人 Profile。
- 评估样例使用普通文本和结构化文件，避免绑定付费模型。
- 外部工具、仓库访问和实验执行必须在 Skill 中明确声明前置条件。
- 不把 Codex 或 Claude Code 的专有行为写成通用标准。

## 后续兼容目标

后续会在真实 Skill 完成后验证：

- Claude Code 项目级 Skills
- Codex 项目级 Skills
- 通过脚本运行的离线评测
- 可选的 GitHub、PDF 和实验工具连接

兼容性以实际样例和评测结果为准，不以 README 中的声明为准。
