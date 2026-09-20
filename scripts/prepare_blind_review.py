"""Create a reproducible blind-review export from validated run records."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_skills.blinding import prepare_blind_review  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("records", nargs="+", type=Path)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, required=True)
    args = parser.parse_args()
    try:
        manifest = prepare_blind_review(
            args.records,
            args.output,
            root=args.root,
            seed=args.seed,
        )
    except (OSError, ValueError) as error:
        print(f"Could not prepare blind review: {error}", file=sys.stderr)
        return 2
    print(f"Prepared {len(manifest['candidates'])} blinded candidates in {args.output}")
    print("Keep private/review-key.json away from reviewers")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
