"""Validate the public shape of the Personal Research Skills repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_PATHS = (
    "README.md",
    "profiles/reasoning-dna.yaml",
    "skills/paper-reading/SKILL.md",
    "skills/paper-reading/contract.yaml",
    "skills/paper-reading/examples/input.md",
    "skills/paper-reading/examples/expected-output.md",
    "evals/rubrics/paper-reading.yaml",
    "evals/fixtures/paper-reading-demo/source.md",
    "evals/fixtures/paper-reading-demo/evidence-card.md",
    "skills/research-question/SKILL.md",
    "skills/research-question/contract.yaml",
    "skills/research-question/examples/input.md",
   "skills/research-question/examples/expected-output.md",
    "skills/argument-analysis/SKILL.md",
    "skills/argument-analysis/contract.yaml",
    "skills/argument-analysis/examples/input.md",
    "skills/argument-analysis/examples/expected-output.md",
    "skills/argument-analysis/evals/pressure-scenarios.md",
    "evals/cases/2013-text3-pilot/README.md",
    "research_skills/dna.py",
    "research_skills/compose.py",
    "scripts/run_skill.py",
)

SKILL_FRONTMATTER_KEYS = ("name:", "description:")
CONTRACT_KEYS = (
    "paper_text",
    "problem",
    "evidence",
    "inferences",
    "assumptions",
    "boundaries",
    "connections",
    "next_actions",
)


def validate(root: Path) -> list[str]:
    """Return a list of missing or malformed public repository artifacts."""
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")

    for skill_name in ("paper-reading", "research-question", "argument-analysis"):
        skill_path = root / "skills" / skill_name / "SKILL.md"
        if skill_path.is_file():
            skill_text = skill_path.read_text(encoding="utf-8")
            for key in SKILL_FRONTMATTER_KEYS:
                if key not in skill_text:
                    errors.append(f"Missing Skill frontmatter key in {skill_name}: {key}")

    contract_path = root / "skills/paper-reading/contract.yaml"
    if contract_path.is_file():
        contract_text = contract_path.read_text(encoding="utf-8")
        for key in CONTRACT_KEYS:
            if key not in contract_text:
                errors.append(f"Missing contract key: {key}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate")
    arguments = parser.parse_args()

    errors = validate(Path(arguments.root).resolve())
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
