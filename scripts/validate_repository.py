"""Backward-compatible repository validation command."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_skills.repository import REQUIRED_PATHS, validate  # noqa: E402


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
