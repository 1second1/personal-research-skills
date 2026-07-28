"""Evaluate a paper-reading evidence card against a small public rubric."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def read_rubric_values(rubric_text: str) -> list[str]:
    """Extract quoted list entries from the repository's minimal YAML rubric format."""
    values: list[str] = []
    for line in rubric_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        value = stripped[2:].strip()
        if len(value) >= 2 and value[0] == value[-1] == '"':
            values.append(value[1:-1])
    return values


def evaluate(card_text: str, rubric_text: str) -> list[str]:
    """Return rubric requirements that are absent from an evidence card."""
    requirements = read_rubric_values(rubric_text)
    normalized_card = card_text.casefold()
    return [
        requirement
        for requirement in requirements
        if requirement.casefold() not in normalized_card
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path, help="Evidence-card Markdown path")
    parser.add_argument("rubric", type=Path, help="Rubric YAML path")
    arguments = parser.parse_args()

    missing = evaluate(
        arguments.card.read_text(encoding="utf-8"),
        arguments.rubric.read_text(encoding="utf-8"),
    )
    if missing:
        print("Missing rubric requirement(s):", file=sys.stderr)
        for requirement in missing:
            print(f"- {requirement}", file=sys.stderr)
        return 1

    print("Evaluation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
