# Reasoning DNA Runtime Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the maintainer's research methodology into a validated profile that can be loaded and composed with individual Skills.

**Architecture:** A dependency-free Python runtime reads a constrained YAML-like profile, validates required sections, and composes the profile with a Skill contract. A CLI exposes the composed result and a research-question Skill demonstrates inheritance. The runtime emits explicit errors for malformed or incomplete profiles.

**Tech Stack:** Python 3.11+, standard library only, Markdown Skill files, YAML-compatible profile syntax.

---

### Task 1: Define the profile and runtime contract

**Files:**
- Create: `profiles/reasoning-dna.yaml`
- Create: `src/research_skills/__init__.py`
- Create: `src/research_skills/dna.py`
- Create: `src/research_skills/compose.py`
- Test: `tests/test_reasoning_dna.py`

- [ ] Write failing tests for required sections, nested values, and composed rules.
- [ ] Run the focused tests and confirm they fail because the runtime does not exist.
- [ ] Implement strict profile parsing and validation with standard-library code.
- [ ] Run the focused tests and confirm they pass.
- [ ] Commit the runtime contract.

### Task 2: Add a DNA-inheriting research-question Skill

**Files:**
- Create: `skills/research-question/SKILL.md`
- Create: `skills/research-question/contract.yaml`
- Create: `skills/research-question/examples/input.md`
- Create: `skills/research-question/examples/expected-output.md`
- Test: `tests/test_research_question.py`

- [ ] Write a failing test for required research-question sections and DNA markers.
- [ ] Run the test and confirm it fails.
- [ ] Add the Skill contract, instructions, and example.
- [ ] Run the test and confirm it passes.
- [ ] Commit the Skill.

### Task 3: Expose the runtime through a CLI

**Files:**
- Create: `scripts/run_skill.py`
- Create: `tests/test_run_skill.py`
- Modify: `pyproject.toml`
- Modify: `README.md`

- [ ] Write a failing subprocess test for `paper-reading` composition.
- [ ] Implement Skill lookup, profile loading, and deterministic Markdown output.
- [ ] Add `research-question` CLI coverage.
- [ ] Run all tests, repository validation, and both fixture evaluations.
- [ ] Commit the runnable demo.

### Task 4: Document and verify the milestone

**Files:**
- Modify: `WEEK-1-CHECKLIST.md`
- Create: `WEEK-2-CHECKLIST.md`
- Modify: `.github/workflows/validate.yml`

- [ ] Add the CLI command and architecture to the README.
- [ ] Add Week 2 evidence and acceptance criteria.
- [ ] Run the exact CI commands locally.
- [ ] Commit the verified milestone.
