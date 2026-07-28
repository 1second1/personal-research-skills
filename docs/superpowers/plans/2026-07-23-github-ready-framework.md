# GitHub-Ready Framework Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a GitHub-ready Personal Research Skills repository with one testable `paper-reading` Skill, local validation, fixture evaluation, and contribution automation.

**Architecture:** The repository uses a static Skill contract plus synthetic fixtures. Two Python standard-library scripts validate the public repository shape and evaluate the bundled example output. Unit tests exercise both scripts; GitHub Actions executes the same commands on every push and pull request.

**Tech Stack:** Python 3.10+, `unittest`, YAML-compatible hand-written configuration parsed by a minimal local reader, Markdown, GitHub Actions.

---

## File map

| Path | Responsibility |
|---|---|
| `pyproject.toml` | Python version and unittest command metadata |
| `scripts/validate_repository.py` | Verify required files, Skill frontmatter, and contract fields |
| `scripts/evaluate_paper_reading.py` | Score bundled evidence card against required markers |
| `tests/test_validate_repository.py` | Validator behavior tests |
| `tests/test_evaluate_paper_reading.py` | Evaluator success and failure tests |
| `skills/paper-reading/` | First usable Skill, contract, example, and rubric pointer |
| `evals/fixtures/paper-reading-demo/` | Synthetic source note and evidence-card output |
| `evals/rubrics/paper-reading.yaml` | Public evaluation requirements |
| `.github/` | CI, contribution forms, pull request guidance, Dependabot |
| repository root docs | Contributor-facing README, license, conduct, security, release checklist |

### Task 1: Establish Python test harness and repository defaults

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `tests/__init__.py`
- Create: `tests/test_validate_repository.py`

- [ ] **Step 1: Write the validator test before the validator exists**

```python
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ValidateRepositoryTests(unittest.TestCase):
    def test_validator_reports_missing_required_files(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_repository.py", "--root", "."],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required file", result.stderr)
```

- [ ] **Step 2: Run the test and verify it fails because the script is missing**

Run: `python -m unittest tests.test_validate_repository -v`

Expected: `FAIL` or `ERROR` mentioning that `scripts/validate_repository.py` cannot be opened.

- [ ] **Step 3: Add project metadata and ignores**

Create `pyproject.toml`:

```toml
[project]
name = "personal-research-skills"
version = "0.1.0"
requires-python = ">=3.10"

[tool.unittest]
start-directory = "tests"
```

Create `.gitignore`:

```gitignore
__pycache__/
*.py[cod]
.coverage
.venv/
dist/
build/
.DS_Store
```

- [ ] **Step 4: Commit the test harness**

```bash
git add pyproject.toml .gitignore tests/__init__.py tests/test_validate_repository.py
git commit -m "test: add repository validator contract"
```

### Task 2: Implement repository validator

**Files:**
- Create: `scripts/validate_repository.py`
- Modify: `tests/test_validate_repository.py`

- [ ] **Step 1: Extend the failing test for the valid repository case**

```python
    def test_validator_accepts_complete_repository(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_repository.py", "--root", "."],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Repository validation passed", result.stdout)
```

- [ ] **Step 2: Run tests and verify the new valid-repository assertion fails**

Run: `python -m unittest tests.test_validate_repository -v`

Expected: the valid-repository test fails because the repository artifacts do not yet exist.

- [ ] **Step 3: Implement the minimal validator API**

Implement `validate(root: Path) -> list[str]` and CLI `main() -> int`. Require the following paths:

```python
REQUIRED_PATHS = (
    "README.md",
    "profiles/researcher-example.yaml",
    "skills/paper-reading/SKILL.md",
    "skills/paper-reading/contract.yaml",
    "skills/paper-reading/examples/input.md",
    "skills/paper-reading/examples/expected-output.md",
    "evals/rubrics/paper-reading.yaml",
    "evals/fixtures/paper-reading-demo/source.md",
    "evals/fixtures/paper-reading-demo/evidence-card.md",
)
```

The validator must additionally require `name:` and `description:` in `SKILL.md`, and these literal keys in the contract: `paper_text`, `problem`, `evidence`, `inferences`, `assumptions`, `boundaries`, `connections`, and `next_actions`.

- [ ] **Step 4: Run the validator test and verify the expected missing-file failure**

Run: `python -m unittest tests.test_validate_repository -v`

Expected: the first test passes because the validator names missing files; the valid-repository test remains failing until Task 3 adds artifacts.

- [ ] **Step 5: Commit the minimal validator**

```bash
git add scripts/validate_repository.py tests/test_validate_repository.py
git commit -m "feat: add repository contract validator"
```

### Task 3: Add the `paper-reading` Skill and synthetic demonstration

**Files:**
- Create: `skills/paper-reading/SKILL.md`
- Create: `skills/paper-reading/contract.yaml`
- Create: `skills/paper-reading/examples/input.md`
- Create: `skills/paper-reading/examples/expected-output.md`
- Create: `skills/paper-reading/evals/README.md`
- Create: `evals/fixtures/paper-reading-demo/source.md`
- Create: `evals/fixtures/paper-reading-demo/evidence-card.md`
- Create: `evals/rubrics/paper-reading.yaml`

- [ ] **Step 1: Create a synthetic source note**

Use this source text in `evals/fixtures/paper-reading-demo/source.md` and `skills/paper-reading/examples/input.md`:

```markdown
# LiteSeg synthetic research note

LiteSeg is a lightweight encoder-decoder network for 2D medical image segmentation.
It replaces standard convolution blocks with depthwise separable convolutions and adds a
boundary-aware loss. On Dataset-A, LiteSeg reports Dice 0.842 versus 0.831 for U-Net,
with 2.1M versus 7.8M parameters. Experiments use 256×256 images and a fixed 80/20
train-validation split. The note does not report inference latency, repeated-run variance,
or external-dataset results.
```

- [ ] **Step 2: Write a contract that makes evidence and inference separate**

`contract.yaml` must declare required input `paper_text`, optional `research_context` and `source_locations`, required output sections listed by Task 2, and constraints that prohibit invented locations and unsupported claims.

- [ ] **Step 3: Write `SKILL.md` in imperative form**

The Skill must instruct the agent to:

1. Identify the problem and direct source facts.
2. Label inferences and recommendations explicitly.
3. Check assumptions and boundaries.
4. Connect the method to the supplied research context only when the context supports it.
5. End with falsifiable next actions.

The frontmatter must be:

```yaml
---
name: paper-reading
description: Use when analyzing a research paper or paper excerpt and producing an evidence-grounded research evidence card with explicit facts, inferences, assumptions, boundaries, and next actions.
---
```

- [ ] **Step 4: Create expected evidence-card output**

The output fixture must contain headings `## Problem`, `## Evidence`, `## Inferences`, `## Assumptions`, `## Boundaries`, `## Connections`, and `## Next Actions`; cite the synthetic note as `[Source: LiteSeg synthetic research note]`; label at least one `Inference:`; state that latency and external generalization are unsupported; and include an action to measure inference time.

- [ ] **Step 5: Add public rubric**

Use this exact minimum rubric content:

```yaml
required_headings:
  - "## Problem"
  - "## Evidence"
  - "## Inferences"
  - "## Assumptions"
  - "## Boundaries"
  - "## Connections"
  - "## Next Actions"
required_markers:
  - "[Source:"
  - "Inference:"
  - "unsupported"
  - "measure inference time"
```

- [ ] **Step 6: Run the validator and verify it passes**

Run: `python scripts/validate_repository.py`

Expected: `Repository validation passed`.

- [ ] **Step 7: Run validator unit tests and verify both tests pass**

Run: `python -m unittest tests.test_validate_repository -v`

Expected: `OK` with 2 tests.

- [ ] **Step 8: Commit the first Skill and demo**

```bash
git add skills evals scripts/validate_repository.py tests/test_validate_repository.py
git commit -m "feat: add evidence-grounded paper reading skill"
```

### Task 4: Implement fixture evaluator with red-green tests

**Files:**
- Create: `tests/test_evaluate_paper_reading.py`
- Create: `scripts/evaluate_paper_reading.py`

- [ ] **Step 1: Write evaluator tests before the evaluator exists**

```python
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals/fixtures/paper-reading-demo/evidence-card.md"
RUBRIC = ROOT / "evals/rubrics/paper-reading.yaml"


class EvaluatePaperReadingTests(unittest.TestCase):
    def test_evaluator_accepts_bundled_evidence_card(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/evaluate_paper_reading.py", str(FIXTURE), str(RUBRIC)],
            cwd=ROOT, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Evaluation passed", result.stdout)

    def test_evaluator_rejects_missing_inference_label(self) -> None:
        text = FIXTURE.read_text(encoding="utf-8").replace("Inference:", "Interpretation:")
        with tempfile.TemporaryDirectory() as directory:
            candidate = Path(directory) / "bad-card.md"
            candidate.write_text(text, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "scripts/evaluate_paper_reading.py", str(candidate), str(RUBRIC)],
                cwd=ROOT, capture_output=True, text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Inference:", result.stderr)
```

- [ ] **Step 2: Run evaluator tests and verify they fail because the evaluator is absent**

Run: `python -m unittest tests.test_evaluate_paper_reading -v`

Expected: both tests fail because `scripts/evaluate_paper_reading.py` is missing.

- [ ] **Step 3: Implement the evaluator**

Implement a standard-library YAML-list reader that extracts quoted values under `required_headings:` and `required_markers:`. Implement `evaluate(card_text: str, rubric_text: str) -> list[str]`. The CLI must print each missing requirement to stderr and return `1`; print `Evaluation passed` and return `0` when no requirements are missing.

- [ ] **Step 4: Run evaluator tests and verify both pass**

Run: `python -m unittest tests.test_evaluate_paper_reading -v`

Expected: `OK` with 2 tests.

- [ ] **Step 5: Run direct success and failure commands**

Run: `python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml`

Expected: `Evaluation passed`.

Run: `python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/source.md evals/rubrics/paper-reading.yaml`

Expected: non-zero exit and a list of missing headings/markers.

- [ ] **Step 6: Commit evaluator and tests**

```bash
git add scripts/evaluate_paper_reading.py tests/test_evaluate_paper_reading.py
git commit -m "feat: add paper reading fixture evaluator"
```

### Task 5: Add GitHub collaboration and release files

**Files:**
- Create: `.github/workflows/validate.yml`
- Create: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Create: `.github/ISSUE_TEMPLATE/skill_proposal.yml`
- Create: `.github/pull_request_template.md`
- Create: `.github/dependabot.yml`
- Create: `CONTRIBUTING.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `SECURITY.md`
- Create: `RELEASE.md`
- Create: `LICENSE`
- Modify: `README.md`

- [ ] **Step 1: Add GitHub Actions workflow**

Run Python 3.11 on `push` and `pull_request`; execute:

```yaml
- run: python -m unittest discover -s tests -v
- run: python scripts/validate_repository.py
- run: python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml
```

- [ ] **Step 2: Add contribution forms**

The bug form must ask for affected path, command, actual behavior, and expected behavior. The Skill proposal form must ask for trigger, input/output contract, source of evaluation data, failure boundaries, and whether it changes Values, Thinking, Workflow, or Preference.

- [ ] **Step 3: Add project governance documents**

Use Apache License 2.0. The security policy must direct reporters not to publish secrets or private research data in public issues. The release checklist must require the test suite, validator, evaluator, changelog review, and license review.

- [ ] **Step 4: Upgrade README into a runnable entry point**

Add exact Quickstart commands:

```bash
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml
```

Link to the example Skill, fixture, rubric, contribution guide, security policy, code of conduct, and release process.

- [ ] **Step 5: Run full local verification**

Run: `python -m unittest discover -s tests -v`

Expected: all tests pass.

Run: `python scripts/validate_repository.py`

Expected: `Repository validation passed`.

Run: `python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml`

Expected: `Evaluation passed`.

- [ ] **Step 6: Commit GitHub-ready framework**

```bash
git add .github CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md RELEASE.md LICENSE README.md
git commit -m "chore: add GitHub collaboration framework"
```

### Task 6: Final audit and release-ready commit

**Files:**
- Modify: `WEEK-1-CHECKLIST.md`
- Modify: `README.md`

- [ ] **Step 1: Add real completion evidence to the Week 1 checklist**

Replace document-only completion claims with command outputs, test count, Skill artifact locations, and known limitations.

- [ ] **Step 2: Inspect tracked content for safety exclusions**

Run: `git grep -n -E "api[_-]?key|sk-[A-Za-z0-9]|BEGIN PRIVATE|password="`

Expected: no matches.

- [ ] **Step 3: Inspect pending changes and run all checks fresh**

Run:

```bash
git status --short
python -m unittest discover -s tests -v
python scripts/validate_repository.py
python scripts/evaluate_paper_reading.py evals/fixtures/paper-reading-demo/evidence-card.md evals/rubrics/paper-reading.yaml
```

Expected: only intended files are pending before commit; all commands exit `0`.

- [ ] **Step 4: Commit the release-ready first-week artifact**

```bash
git add WEEK-1-CHECKLIST.md README.md
git commit -m "docs: record verified week one milestone"
```

- [ ] **Step 5: Confirm local publication boundary**

Run: `git log --oneline --decorate -5`

Expected: a local commit history exists. Do not add a remote or push without an explicit GitHub repository target and authorization.
