"""Compose a repository Skill with the default personal reasoning profile."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_skills.compose import compose_skill  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="Skill directory name under skills/")
    parser.add_argument("input", help="Input Markdown path, retained for reproducible invocation")
    parser.add_argument(
        "--profile",
        default="profiles/reasoning-dna.yaml",
        help="Profile path relative to the repository root",
    )
    arguments = parser.parse_args()
    skill_dir = ROOT / "skills" / arguments.skill
    input_path = ROOT / arguments.input
    if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
        print(f"Unknown Skill: {arguments.skill}", file=sys.stderr)
        return 2
    if not input_path.is_file():
        print(f"Input file not found: {arguments.input}", file=sys.stderr)
        return 2
    try:
        input_text = input_path.read_text(encoding="utf-8")
        print(compose_skill(skill_dir, ROOT / arguments.profile, input_text=input_text), end="")
    except (FileNotFoundError, ValueError) as error:
        print(f"Could not compose Skill: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
