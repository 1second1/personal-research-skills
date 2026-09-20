# Compatibility

## Current support level

The public release uses provider-neutral Markdown and YAML-compatible files. It does not require a hosted backend.

| Environment | Status | Notes |
|---|---|---|
| Claude Code | Compatible artifacts | Load the self-contained `SKILL.md` files using the project's supported Skill location |
| Codex | Compatible artifacts | Load the profile and Skill files through project context or the supported Skills location |
| Generic agents | Supported | Consume deterministic Markdown from `research-skills compose` or the legacy wrapper |
| Markdown readers | Supported | All profiles, contracts, examples, and rubrics are readable without tooling |
| Model-serving runtime | Not included | This release does not call a model or provide memory, scheduling, or automatic learning |

## 兼容性原则

- `SKILL.md` 保持自包含，不能依赖只有某一个模型知道的隐式上下文。
- 方法论 Profile 与具体 Skill 分离，便于替换个人 Profile。
- 评估样例使用普通文本和结构化文件，避免绑定付费模型。
- 外部工具、仓库访问和实验执行必须在 Skill 中明确声明前置条件。
- 不把 Codex 或 Claude Code 的专有行为写成通用标准。
- Windows 下优先使用 CLI 的 `--output` 写入 UTF-8 文件，避免 shell 管道改变 Unicode 文本。
- CLI 在仓库目录外运行时必须通过 `--root` 指向包含 `skills/` 和 `profiles/` 的 checkout。
- Run records and evaluator reports are versioned provider-neutral YAML/JSON;
  provider-specific metadata must not be added to the canonical schema without a compatibility decision.

## Compatibility policy

Compatibility claims must be backed by an example or evaluation. The repository does not treat a provider name in documentation as proof of runtime compatibility.

Provider-specific adapters may be added later, but the canonical profile, Skill contract, and evaluation files must remain provider-neutral.
