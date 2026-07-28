# Personal Research Skills

[![Validate repository](https://github.com/1second1/personal-research-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/1second1/personal-research-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](pyproject.toml)

> A composable, evidence-grounded way to turn research methodology into reusable AI Skills.

Personal Research Skills is an experimental open-source framework for research learning and deep research workflows. It explores one question:

> Can an explicit personal research methodology make different AI Skills more consistent, traceable, and open to improvement?

[中文说明](README.zh-CN.md)

## Why this project exists

Most AI Skills are isolated prompts. This project treats a Skill as a capability with:

- a reasoning profile;
- explicit input and output contracts;
- evidence and uncertainty rules;
- examples and regression evaluations;
- a documented boundary.

The first reference profile models a four-layer system:

```text
Identity → Values → Thinking → Workflow → Preferences → Skills
```

Its inquiry pattern is:

```text
What → Why → Assumption → Boundary → Connection → Application → Value
```

## Current status

`v0.2 — Reasoning DNA runtime and inherited research Skills`

Included today:

- `profiles/reasoning-dna.yaml`: values, inquiry pattern, decision rules, workflows, and preferences;
- a dependency-free Python loader and Skill composer;
- `paper-reading`: evidence-grounded paper analysis;
- `research-question`: conversion of broad ideas into bounded, falsifiable questions;
- deterministic examples, tests, repository validation, and GitHub Actions.

The runtime currently generates a composed execution context. It does not call a model, store private memory, or claim to learn automatically.

## Quickstart

Requirements: Python 3.10 or newer. No API key or private data is required.

```bash
git clone https://github.com/1second1/personal-research-skills.git
cd personal-research-skills

python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml
```

Compose a Skill with the reference Reasoning DNA profile:

```bash
python scripts/run_skill.py paper-reading skills/paper-reading/examples/input.md
python scripts/run_skill.py research-question skills/research-question/examples/input.md
```

The CLI emits a deterministic Markdown context containing the personal profile and the selected Skill contract. It can be inspected or passed to an agent runtime.

## Repository layout

```text
personal-research-skills/
├── profiles/reasoning-dna.yaml
├── research_skills/
│   ├── dna.py
│   └── compose.py
├── scripts/run_skill.py
├── skills/
│   ├── paper-reading/
│   └── research-question/
├── evals/
├── tests/
├── docs/
├── CHANGELOG.md
└── .github/workflows/validate.yml
```

Every Skill should include:

```text
skills/<skill-name>/
├── SKILL.md
├── contract.yaml
├── examples/
├── evals/
└── changelog.md
```

## Design principles

- Evidence is separate from inference.
- Unsupported conclusions are marked instead of invented.
- Every recommendation has a measurable next action.
- A profile is reusable; a Skill remains independently testable.
- Boundaries are part of the output, not an afterthought.

## Roadmap

1. Run independent-agent forward evaluations for `paper-reading` and `research-question`.
2. Add a third Skill for codebase or paper-to-code analysis.
3. Compare outputs from no profile, Skill only, and Skill plus Reasoning DNA.
4. Add a reviewable feedback log for evolving rules.
5. Consider model, PDF, repository, and experiment integrations only after the evaluation loop is reliable.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [the detailed contribution guide](docs/contributing.md), [SECURITY.md](SECURITY.md), [RELEASE.md](RELEASE.md), and [CHANGELOG.md](CHANGELOG.md) before opening a pull request.

Do not commit API keys, private papers, participant data, or unredacted conversation logs.

## License

MIT. See [LICENSE](LICENSE).
