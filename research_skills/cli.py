"""Command-line interface for composing repository Skills."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .compose import compose_skill


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _default_root() -> Path:
    current_directory = Path.cwd()
    if (current_directory / "skills").is_dir() and (current_directory / "profiles").is_dir():
        return current_directory
    return PACKAGE_ROOT


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="Repository root containing skills/ and profiles/",
    )
    parser.add_argument("skill", help="Skill directory name under skills/")
    parser.add_argument("--mode", choices=("baseline", "skill", "profile"), default="profile")
    parser.add_argument("input", help="Input Markdown path relative to the repository, or - for stdin")
    parser.add_argument(
        "--profile",
        default="profiles/reasoning-dna.yaml",
        help="Profile path relative to the repository root",
    )
    parser.add_argument("--output", type=Path, help="Write UTF-8 Markdown to this path")
    arguments = parser.parse_args(argv)

    root = arguments.root.resolve()
    skill_dir = root / "skills" / arguments.skill
    if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
        print(f"Unknown Skill: {arguments.skill}", file=sys.stderr)
        return 2

    input_path = None
    if arguments.input != "-":
        input_path = root / arguments.input
        if not input_path.is_file():
            print(f"Input file not found: {arguments.input}", file=sys.stderr)
            return 2

    try:
        if input_path is None:
            input_text = sys.stdin.read()
        else:
            input_text = input_path.read_text(encoding="utf-8")
        context = compose_skill(
            skill_dir,
            root / arguments.profile,
            input_text=input_text,
            mode=arguments.mode,
        )
        if arguments.output:
            arguments.output.write_text(context, encoding="utf-8")
        else:
            sys.stdout.write(context)
    except (OSError, ValueError) as error:
        print(f"Could not compose Skill: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
