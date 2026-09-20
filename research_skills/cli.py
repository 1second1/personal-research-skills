"""Compose, inspect, validate, and evaluate Personal Research Skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .blinding import prepare_blind_review
from .compose import compose_skill
from .evaluation import evaluate, report_for
from .repository import validate as validate_repository
from .run_records import validate_run_record


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COMMANDS = {"compose", "list", "validate", "evaluate", "blind"}


def _default_root() -> Path:
    current_directory = Path.cwd()
    if (current_directory / "skills").is_dir() and (current_directory / "profiles").is_dir():
        return current_directory
    return PACKAGE_ROOT


def _normalize_legacy_argv(argv: list[str]) -> list[str]:
    """Insert `compose` for the original `research-skills SKILL INPUT` form."""
    # argparse requires global options before subcommands. The original flat
    # CLI accepted --root after its positionals, so hoist it before dispatch.
    roots: list[str] = []
    remaining: list[str] = []
    scan = 0
    while scan < len(argv):
        argument = argv[scan]
        if argument == "--root" and scan + 1 < len(argv):
            roots.extend((argument, argv[scan + 1]))
            scan += 2
            continue
        if argument.startswith("--root="):
            roots.append(argument)
            scan += 1
            continue
        remaining.append(argument)
        scan += 1
    argv = roots + remaining

    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--root":
            index += 2
            continue
        if argument.startswith("--root="):
            index += 1
            continue
        if argument in {"--version", "-h", "--help"}:
            return argv
        if argument.startswith("-"):
            index += 1
            continue
        if argument not in COMMANDS:
            return argv[:index] + ["compose"] + argv[index:]
        return argv
    return argv


def _path(root: Path, value: Path | None) -> Path | None:
    if value is None:
        return None
    return value if value.is_absolute() else root / value


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=_default_root(),
        help="Repository root containing skills/, profiles/, and evals/",
    )
    parser.add_argument("--version", action="version", version=f"research-skills {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compose = subparsers.add_parser("compose", help="Compose a provider-neutral Skill context")
    compose.add_argument("skill", help="Skill directory name under skills/")
    compose.add_argument(
        "input", help="Input Markdown path relative to the repository, or - for stdin"
    )
    compose.add_argument("--mode", choices=("baseline", "skill", "profile"), default="profile")
    compose.add_argument("--profile", default="profiles/reasoning-dna.yaml")
    compose.add_argument("--output", type=Path, help="Write UTF-8 Markdown to this path")

    listing = subparsers.add_parser("list", help="List available public Skills")
    listing.add_argument("--format", choices=("text", "json"), default="text")

    validation = subparsers.add_parser("validate", help="Validate the repository or one run record")
    validation.add_argument(
        "--run", type=Path, help="Run-record YAML path relative to the repository"
    )

    evaluation = subparsers.add_parser("evaluate", help="Run deterministic output checks")
    evaluation.add_argument("candidate", type=Path)
    evaluation.add_argument("rubric", type=Path)
    evaluation.add_argument("--source", type=Path)
    evaluation.add_argument("--format", choices=("text", "json"), default="text")

    blind = subparsers.add_parser("blind", help="Prepare a reproducible blind-review bundle")
    blind.add_argument("records", nargs="+", type=Path)
    blind.add_argument("--output", type=Path, required=True)
    blind.add_argument("--seed", type=int, required=True)
    return parser


def _compose(arguments: argparse.Namespace, root: Path) -> int:
    skill_dir = root / "skills" / arguments.skill
    if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").is_file():
        print(f"Unknown Skill: {arguments.skill}", file=sys.stderr)
        return 2
    input_path = None if arguments.input == "-" else _path(root, Path(arguments.input))
    if input_path is not None and not input_path.is_file():
        print(f"Input file not found: {arguments.input}", file=sys.stderr)
        return 2
    try:
        input_text = (
            sys.stdin.read() if input_path is None else input_path.read_text(encoding="utf-8")
        )
        context = compose_skill(
            skill_dir,
            _path(root, Path(arguments.profile)),
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


def _list_skills(arguments: argparse.Namespace, root: Path) -> int:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        print(f"Skills directory not found: {skills_root}", file=sys.stderr)
        return 2
    skills = sorted(
        path.name
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if arguments.format == "json":
        print(json.dumps({"schema_version": "1.0", "skills": skills}, ensure_ascii=False, indent=2))
    else:
        print("\n".join(skills))
    return 0


def _validate(arguments: argparse.Namespace, root: Path) -> int:
    if arguments.run:
        errors = validate_run_record(_path(root, arguments.run), root=root)
        success_message = "Run record validation passed"
    else:
        errors = validate_repository(root)
        success_message = "Repository validation passed"
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(success_message)
    return 0


def _evaluate(arguments: argparse.Namespace, root: Path) -> int:
    candidate = _path(root, arguments.candidate)
    rubric = _path(root, arguments.rubric)
    source = _path(root, arguments.source)
    try:
        errors = evaluate(
            candidate.read_text(encoding="utf-8"),
            rubric.read_text(encoding="utf-8"),
            source_text=source.read_text(encoding="utf-8") if source else None,
        )
    except (OSError, ValueError) as error:
        print(f"Invalid evaluation input: {error}", file=sys.stderr)
        return 2
    report = report_for(errors, source_checked=source is not None)
    if arguments.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        print("\n".join(errors), file=sys.stderr)
    else:
        print("Evaluation passed (structural/source checks only; semantic quality not evaluated)")
    return int(bool(errors))


def _blind(arguments: argparse.Namespace, root: Path) -> int:
    records = [_path(root, path) for path in arguments.records]
    output = _path(root, arguments.output)
    try:
        manifest = prepare_blind_review(records, output, root=root, seed=arguments.seed)
    except (OSError, ValueError) as error:
        print(f"Could not prepare blind review: {error}", file=sys.stderr)
        return 2
    print(f"Prepared {len(manifest['candidates'])} blinded candidates in {output}")
    print("Keep private/review-key.json away from reviewers")
    return 0


def main(argv: list[str] | None = None) -> int:
    normalized = _normalize_legacy_argv(list(sys.argv[1:] if argv is None else argv))
    arguments = _build_parser().parse_args(normalized)
    root = arguments.root.resolve()
    if arguments.command == "compose":
        return _compose(arguments, root)
    if arguments.command == "list":
        return _list_skills(arguments, root)
    if arguments.command == "validate":
        return _validate(arguments, root)
    if arguments.command == "evaluate":
        return _evaluate(arguments, root)
    if arguments.command == "blind":
        return _blind(arguments, root)
    raise AssertionError(f"Unhandled command: {arguments.command}")


if __name__ == "__main__":
    raise SystemExit(main())
