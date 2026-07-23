# GitHub-Ready Framework Design

## Goal

Create a public, locally runnable template repository for Personal Research Skills. The first release must demonstrate one real research skill (`paper-reading`) with a clear contract, a sample task, repeatable checks, and GitHub collaboration defaults.

## Scope

### Included

- A Python-based local validator for the repository and Skill contract.
- A `paper-reading` Skill folder with instructions, contract, example input/output, and rubric.
- A reference methodology profile expressing Values, Inquiry Pattern, Workflow, and Preferences.
- A fixture-driven evaluation command that checks the example output against required research-quality markers.
- GitHub Actions that run the validator and evaluation command on pushes and pull requests.
- README, contribution guide, code of conduct, security policy, issue forms, pull request template, license, and release checklist.

### Excluded

- LLM API calls, chat UI, database, vector store, PDF extraction engine, agent planner, automatic Skill mutation, or automatic GitHub publishing.
- Claims that the example analysis was generated from a particular model or paper source.

## Repository Architecture

```text
personal-research-skills/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/validate.yml
│   ├── pull_request_template.md
│   └── dependabot.yml
├── docs/
│   ├── methodology.md
│   ├── compatibility.md
│   ├── contributing.md
│   ├── CODE_OF_CONDUCT.md
│   ├── SECURITY.md
│   ├── RELEASE.md
│   └── superpowers/specs/
├── evals/
│   ├── fixtures/paper-reading-demo/
│   ├── rubrics/paper-reading.yaml
│   └── README.md
├── profiles/researcher-example.yaml
├── scripts/
│   ├── validate_repository.py
│   └── evaluate_paper_reading.py
├── skills/paper-reading/
│   ├── SKILL.md
│   ├── contract.yaml
│   ├── examples/
│   └── evals/
├── tests/
│   ├── test_validate_repository.py
│   └── test_evaluate_paper_reading.py
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── pyproject.toml
└── .gitignore
```

## Components

### Research Methodology Profile

`profiles/researcher-example.yaml` remains the reference implementation for the four-layer model. It must be readable independently from the Skill and must not contain secrets, private conversation logs, or personally identifying material beyond what a contributor explicitly chooses to publish.

### `paper-reading` Skill

The first Skill must provide a repeatable method for converting paper text into a research evidence card. It must require explicit separation between evidence, inference, and recommendation; it must request source locations when available; and it must surface assumptions, boundaries, connections, and next actions.

The Skill does not parse PDFs itself. It accepts source text and optional page/section annotations supplied by the caller.

### Contract

`contract.yaml` defines the public interface:

- required input: `paper_text`
- optional inputs: `research_context`, `source_locations`
- required output sections: `problem`, `evidence`, `inferences`, `assumptions`, `boundaries`, `connections`, `next_actions`
- constraints: do not present inference as source fact; state uncertainty when evidence is missing
- evaluation signals: structure, evidence markers, fact/inference separation, and actionability

### Example and Evaluation Fixture

The repository will use a short synthetic research note, not copyrighted paper text, as its example fixture. This makes the evaluation locally runnable and removes licensing uncertainty. The expected output is a human-readable evidence card.

The evaluator checks format and required content markers only. It does not claim to judge scientific truth automatically.

### Validation Scripts

`validate_repository.py` checks that required repository files exist, the Skill frontmatter is valid, the contract has mandatory fields, and all referenced example/evaluation files are present.

`evaluate_paper_reading.py` checks the example output against the rubric: required headings, source markers in evidence, explicit inference labeling, a boundary statement, and at least one actionable next step.

## Data Flow

```text
source text + optional locations
  → paper-reading/SKILL.md
  → evidence-card output
  → fixture/rubric evaluator
  → pass/fail report
```

The runtime user may execute the Skill in Codex or Claude Code. The repository itself verifies the public artifact shape, not the behavior of a hosted model.

## Error Handling

- If source locations are absent, the output must mark evidence as “location unavailable” rather than inventing page numbers.
- If the source text does not support a requested conclusion, the output must list it as an open question or hypothesis.
- Validator errors must name the missing file or malformed key and exit non-zero.
- Evaluator failures must identify the missing rubric requirement and exit non-zero.

## Testing Strategy

1. Write tests for repository validation before implementing the validator.
2. Run tests and confirm they fail because the scripts do not exist.
3. Implement the smallest validator and rerun tests.
4. Write tests for evaluator success and an explicit missing-inference-label failure.
5. Run the evaluator tests red, then implement the evaluator.
6. Run the full test suite and the direct CLI commands.
7. Configure GitHub Actions to run the same commands.

## Acceptance Criteria

- `python -m unittest discover -s tests -v` exits successfully.
- `python scripts/validate_repository.py` exits successfully.
- `python scripts/evaluate_paper_reading.py` exits successfully on the bundled fixture.
- A deliberately malformed temporary fixture causes the evaluator to exit non-zero.
- The repository contains no API key, model dependency, private paper PDF, or unverified claim of automated scientific correctness.
- A new contributor can identify where to add a Skill, an example, an evaluation, and a GitHub issue from the README.

## Publishing Boundary

The local repository will be initialized and committed. Creating a remote GitHub repository, pushing commits, and opening a pull request require a repository target and separate user authorization.
