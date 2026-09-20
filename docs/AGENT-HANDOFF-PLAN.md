# Personal Research Skills

## Cross-Agent Handoff and Long-Term Engineering Plan

### Local implementation update — 2026-09-19

The configuration parser now requires PyYAML (install with `python -m pip install -e .`).
Profiles and contracts are validated; full contracts and workflows reach composed
contexts. `run_skill.py --mode baseline|skill|profile` supports controlled comparisons.
The installed `research-skills` command supports stdin and direct UTF-8 file output.
Repository validation discovers all Profile and Skill directories rather than a fixed list.
The evaluator checks structure and, with `--source`, source labels and numeric
presence. It does not establish semantic entailment. See `evals/PROTOCOL.md`.
The historical commit and status below describe the original handoff, not current HEAD.
Next: collect and blindly review actual model outputs; do not report ablation gains
before those runs exist.

> This is the historical design and cross-agent handoff record. The opening update,
> README, CHANGELOG, tests, and current Git state define implementation status.

**Repository:** <https://github.com/1second1/personal-research-skills>

**Current branch:** `master`

**Current project commit at handoff:** `442eb62`

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
- `scripts/evaluate_paper_reading.py` — fixture evaluation;
- `tests/` — the regression suite; always use a fresh run rather than a stored count;
- `.github/workflows/validate.yml` — GitHub Actions validation;
- `README.md` — English public entry point;
- `README.zh-CN.md` — Chinese explanation;
- `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `RELEASE.md`, and MIT License.

The last verified commands were:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml
python scripts/run_skill.py paper-reading skills/paper-reading/examples/input.md
python scripts/run_skill.py research-question skills/research-question/examples/input.md
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
3. `PR-REAL-01` is a manually verified real-paper reference case, not a model output or an independent reproduction; the repeated three-condition comparison is still missing.
4. The Python package is not yet installed through a standard console entry point; the CLI currently adjusts `sys.path` for repository-local execution.
5. PDF ingestion and code execution are still manual; there is no provider-neutral adapter layer.
6. The Reasoning DNA is hand-authored and has not yet been shown to improve research results through blinded or repeated comparisons.
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

Current status: the source-verified `PR-REAL-01` U-Mamba fixture is complete,
including page-level evidence and a retained table/prose metric conflict. The
remaining Phase 1 work is to generate repeated model outputs and conduct blinded
human review; do not mislabel the curated reference answer as a model run.

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

Keep compatibility shims for the current `research_skills` import and CLI until the migration is complete. Add a console entry point only after install-from-clean-checkout is tested.

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
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py \
  evals/fixtures/paper-reading-demo/evidence-card.md \
  evals/rubrics/paper-reading.yaml
git diff --check
git status --short --branch
```

If the change affects GitHub Actions, run or inspect the resulting remote workflow before claiming CI success.

---

## 10. If context or quota is limited

Use this priority order:

### Must do first

- run three repetitions for baseline, Skill-only, and profile conditions on `PR-REAL-01`;
- score the randomized outputs with blinded human review and retain disagreements;
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

Current priority: run the remaining Phase 1 comparison on the source-verified PR-REAL-01 case.
Generate three fresh runs for baseline, Skill-only, and Skill + Reasoning DNA
under identical model settings, then randomize and score them with blinded human
review. Preserve raw outputs, run metadata, reviewer disagreements, and the
negative result if the profile does not outperform Skill-only.

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
