# Week 2 Checklist

## 目标

让个人研究方法从静态 Profile 变成可加载、可组合、可验证的 Skill 运行时。

## 已完成

- [x] 建立 `profiles/reasoning-dna.yaml`
- [x] 实现标准库 DNA 解析与必需字段校验
- [x] 实现 Skill Composer
- [x] 让 `paper-reading` 继承 Reasoning DNA
- [x] 新增 `research-question` Skill
- [x] 新增 CLI：`scripts/run_skill.py`
- [x] 新增 7 个第二阶段测试，完整测试达到 11 个
- [x] GitHub Actions 增加两个 CLI smoke test

## 验收命令

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/run_skill.py paper-reading skills/paper-reading/examples/input.md
python scripts/run_skill.py research-question skills/research-question/examples/input.md
```

## 明确边界

当前 Runtime 只负责配置加载、规则组合和输出执行上下文，不声称已经具备自动学习、模型调用或长期记忆能力。

## 下一步

用独立 Agent 对两个 Skill 做前向测试，记录无 DNA、仅 Skill、Skill + DNA 三组输出差异，再决定是否加入反馈演化层。
