"""Evaluate a Skill output with deterministic structure and source checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_skills.evaluation import evaluate, report_for  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("rubric", type=Path)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        errors = evaluate(
            args.candidate.read_text(encoding="utf-8"),
            args.rubric.read_text(encoding="utf-8"),
            source_text=args.source.read_text(encoding="utf-8") if args.source else None,
        )
    except (OSError, ValueError) as error:
        print(f"Invalid evaluation input: {error}", file=sys.stderr)
        return 2
    report = report_for(errors, source_checked=args.source is not None)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        print("\n".join(errors), file=sys.stderr)
    else:
        print("Evaluation passed (structural/source checks only; semantic quality not evaluated)")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
