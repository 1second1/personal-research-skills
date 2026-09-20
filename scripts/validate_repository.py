"""Validate the public shape of the Personal Research Skills repository."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from research_skills.dna import load_contract, load_profile


REQUIRED_PATHS = (
    "README.md",
    "profiles/reasoning-dna.yaml",
    "evals/rubrics/paper-reading.yaml",
    "evals/fixtures/paper-reading-demo/source.md",
    "evals/fixtures/paper-reading-demo/evidence-card.md",
    "evals/cases/u-mamba-real-paper/README.md",
    "evals/cases/u-mamba-real-paper/case.yaml",
    "evals/cases/u-mamba-real-paper/source-map.md",
    "evals/cases/u-mamba-real-paper/expected-output.md",
    "evals/cases/u-mamba-real-paper/rubric.yaml",
    "evals/cases/2013-text3-pilot/README.md",
    "research_skills/cli.py",
    "research_skills/dna.py",
    "research_skills/compose.py",
    "scripts/run_skill.py",
)

SKILL_FRONTMATTER_KEYS = ("name:", "description:")
REQUIRED_DIRECTORIES = ("profiles", "skills")
SKILL_ARTIFACTS = (
    "SKILL.md",
    "contract.yaml",
    "examples/input.md",
    "examples/expected-output.md",
    "evals/pressure-scenarios.md",
)


def validate(root: Path) -> list[str]:
    """Return a list of missing or malformed public repository artifacts."""
    errors: list[str] = []

    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")

    for relative_path in REQUIRED_DIRECTORIES:
        if not (root / relative_path).is_dir():
            errors.append(f"Missing required directory: {relative_path}")

    profiles_root = root / "profiles"
    if profiles_root.is_dir():
        for profile_path in sorted(profiles_root.glob("*.yaml")):
            try:
                load_profile(profile_path)
            except (OSError, ValueError) as error:
                relative_path = profile_path.relative_to(root).as_posix()
                errors.append(f"Invalid profile {relative_path}: {error}")

    skills_root = root / "skills"
    if skills_root.is_dir():
        for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
            skill_relative = skill_dir.relative_to(root).as_posix()
            for artifact in SKILL_ARTIFACTS:
                if not (skill_dir / artifact).is_file():
                    errors.append(f"Missing Skill artifact: {skill_relative}/{artifact}")

            skill_path = skill_dir / "SKILL.md"
            if skill_path.is_file():
                skill_text = skill_path.read_text(encoding="utf-8")
                for key in SKILL_FRONTMATTER_KEYS:
                    if key not in skill_text:
                        errors.append(f"Missing Skill frontmatter key in {skill_dir.name}: {key}")

            contract_path = skill_dir / "contract.yaml"
            if contract_path.is_file():
                try:
                    contract = load_contract(contract_path)
                except (OSError, ValueError) as error:
                    errors.append(f"Invalid Skill contract {skill_relative}/contract.yaml: {error}")
                else:
                    if contract["name"] != skill_dir.name:
                        errors.append(
                            f"Invalid Skill contract {skill_relative}/contract.yaml: "
                            "name must match the Skill directory"
                        )

    cases_root = root / "evals/cases"
    if cases_root.is_dir():
        for path in cases_root.rglob("*"):
            if path.is_file() and path.suffix.casefold() == ".pdf":
                errors.append(f"Do not commit source PDF: {path.relative_to(root).as_posix()}")

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
