# Personal Research Skills

[![Validate repository](https://github.com/1second1/personal-research-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/1second1/personal-research-skills/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg)](pyproject.toml)

> A composable, evidence-grounded way to turn research methodology into reusable AI Skills.

Personal Research Skills is an experimental open-source framework for research learning and deep research workflows. It explores one question:

> Can an explicit personal research methodology make different AI Skills more consistent, traceable, and open to improvement?

[中文说明](README.zh-CN.md)

## Install as Agent Skills

You do not need Python, an API key, or a model provider to use the packaged
Skills. The installer requires Node.js and `npx`. Run it from the project where
you want the Skills available. Installation uses the open-source
[`skills` CLI](https://github.com/vercel-labs/skills).

Guided installation:

```bash
npx skills add 1second1/personal-research-skills
```

Install all three Skills for both Codex and Claude Code in one command:

```bash
npx skills add 1second1/personal-research-skills \
  --skill '*' --agent codex --agent claude-code --copy --yes
```

The verified project-local targets are `.agents/skills/` for Codex and
`.claude/skills/` for Claude Code. Review installed Skills before use because
they run with the permissions granted to the host agent. This repository is not
currently distributed as an official Codex or Claude plugin.

### Available Skills

| Skill | Use it when you need to | Example request |
|---|---|---|
| `paper-reading` | examine a paper's claims, evidence, numbers, limitations, and internal consistency | `Use paper-reading to analyze paper.md without turning inference into fact.` |
| `research-question` | turn a broad research idea into a bounded, falsifiable question | `Use research-question to refine this idea into a testable study.` |
| `argument-analysis` | separate claims, support, warrants, counterarguments, and boundaries in argumentative prose | `Use argument-analysis to audit the reasoning in article.md.` |

In Codex, you can also invoke a Skill explicitly with `$paper-reading`,
`$research-question`, or `$argument-analysis`. The host may select a Skill
automatically when the request matches its description.

## 60-second evidence demo

After installation, attach or add a paper to your agent's working context and
ask:

```text
Use paper-reading to analyze this paper. Separate source facts from inferences,
surface internal conflicts, and end with falsifiable next actions.
```

The repository's real-paper example shows what that contract is meant to
change. On the same U-Mamba evidence map, with one model alias and three fresh
runs per condition:

| Condition | Mean rubric score | What the result showed |
|---|---:|---|
| Baseline task | 6.67 / 10 | Useful summary, but no actionable follow-up under the published rubric |
| `paper-reading` Skill | 9.67 / 10 | Better evidence coverage, fact/inference separation, and next actions |
| Skill + Reasoning DNA | 9.00 / 10 | No incremental gain; all three runs over-interpreted an undefined `±` value |

The Skill also kept an internal source conflict visible: U-Mamba reports an
endoscopy DSC of `0.6540` in Table 4 but `0.6504` in the surrounding prose.
It did not silently choose a winner. This is a nine-run pilot with one semantic
reviewer, not a general benchmark.

[Read the short case study](docs/case-studies/u-mamba-negative-result.md) ·
[inspect all raw outputs and run records](evals/cases/u-mamba-real-paper/comparison-2026-09-20/README.md)

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
- a validated YAML profile loader and Skill composer (PyYAML);
- `paper-reading`: evidence-grounded paper analysis;
- `research-question`: conversion of broad ideas into bounded, falsifiable questions;
- `argument-analysis`: claim, support, warrant, counterargument, and boundary analysis for argumentative prose;
- deterministic examples, tests, repository validation, and GitHub Actions;
- a generic structural evaluator with versioned JSON reports and rubrics for all three Skills;
- backward-compatible run-record schemas with SHA-256 artifact verification
  and honest `null` values for provider settings a runtime does not expose;
- deterministic blind-review export with the condition key separated from reviewer files;
- a source-verified [U-Mamba real-paper case](evals/cases/u-mamba-real-paper/README.md) that preserves an internal table/prose conflict instead of hiding it.
- a nine-run [U-Mamba controlled comparison](evals/cases/u-mamba-real-paper/comparison-2026-09-20/README.md)
  with published contexts, raw outputs, integrity records, and a negative
  profile result.

The runtime currently generates a composed execution context. It does not call a model, store private memory, or claim to learn automatically.

## Framework development

The commands below are for developing the composer, evaluator, and run-record
tooling. They are not required when you only want to use the installed Skills.
Requirements: Python 3.10 or newer. No API key or private data is required.

```bash
git clone https://github.com/1second1/personal-research-skills.git
cd personal-research-skills
python -m pip install -e .

python -m unittest discover -s tests -v
research-skills validate
research-skills evaluate \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml \
  --source evals/fixtures/paper-reading-demo/source.md \
  --format json
```

Compose a Skill with the reference Reasoning DNA profile:

```bash
research-skills compose paper-reading skills/paper-reading/examples/input.md --output context.md
research-skills compose research-question skills/research-question/examples/input.md
research-skills compose argument-analysis skills/argument-analysis/examples/input.md
research-skills list --format json
```

The original `research-skills paper-reading ...` form and
`python scripts/run_skill.py ...` remain backward compatible. Use `-` as the
input path to read from stdin. The CLI emits a
deterministic Markdown context containing the personal profile and selected
Skill contract; `--output` writes it directly as UTF-8 instead of relying on a
shell pipeline. When invoking an installed command outside the checkout, pass
`--root /path/to/personal-research-skills` so it can find the public Skills and
profiles; the wheel intentionally does not duplicate those repository artifacts.

Validate an evaluation run before review:

```bash
research-skills validate --run evals/fixtures/run-record-demo/run.yaml

# Two or more real run records are required.
research-skills blind evals/local/runs/run-a.yaml evals/local/runs/run-b.yaml \
  --seed 20260919 --output evals/local/review-export
```

Give reviewers only `review-manifest.json` and `candidates/`. Keep
`private/review-key.json` hidden until scoring is complete. The bundled run is a
deterministic integrity fixture, not a model result.

## Repository layout

```text
personal-research-skills/
├── profiles/reasoning-dna.yaml
├── research_skills/
│   ├── cli.py
│   ├── dna.py
│   ├── compose.py
│   ├── evaluation.py
│   ├── run_records.py
│   └── blinding.py
├── scripts/                  # backward-compatible wrappers
├── skills/
│   ├── paper-reading/
│   ├── research-question/
│   └── argument-analysis/
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
│   ├── input.md
│   └── expected-output.md
└── evals/
    └── pressure-scenarios.md
```

## Design principles

- Evidence is separate from inference.
- Unsupported conclusions are marked instead of invented.
- Conflicting source claims remain visible and traceable.
- Every recommendation has a measurable next action.
- A profile is reusable; a Skill remains independently testable.
- Boundaries are part of the output, not an afterthought.

## Roadmap

For source checks and three-condition experiments, see
[the evaluation protocol](evals/PROTOCOL.md). Passing automated checks does not
establish semantic correctness or demonstrate a benefit from the profile.

The parser/contract layer, generic evaluator, versioned run-record schemas,
blind-review exporter, initial evaluation protocol, and first
[source-verified real-paper case](evals/cases/u-mamba-real-paper/README.md) are
implemented. The real-paper case uncovered and retains a `0.6540` table value
versus `0.6504` prose value conflict; it is a curated reference fixture, not a
model-quality result. Its first repeated comparison found Skill-only above the
baseline (`9.67` versus `6.67` mean rubric score), while Skill + profile scored
`9.00`; the profile therefore showed no incremental gain in this setup. This
was a single-agent best-effort blind review, not an independent human study. A
single-run [argument-analysis pilot](evals/cases/2013-text3-pilot/README.md)
showed a clear benefit from the Skill contract but no measured gain from the
profile over Skill-only. This is evidence from one evaluation setup, not a
general result.

1. Obtain an independent second review of the published real-paper runs and retain disagreements.
2. Add a reviewable, versioned feedback proposal for the observed `±` attribution failure, then rerun the affected case.
3. Add provider-neutral model execution, then PDF, repository, and experiment adapters after the feedback regression.

## Contributing

Read [CONTRIBUTING.md](CONTRIBUTING.md), [the detailed contribution guide](docs/contributing.md), [SECURITY.md](SECURITY.md), [RELEASE.md](RELEASE.md), and [CHANGELOG.md](CHANGELOG.md) before opening a pull request.

Do not commit API keys, private papers, participant data, or unredacted conversation logs.

## License

MIT. See [LICENSE](LICENSE).
