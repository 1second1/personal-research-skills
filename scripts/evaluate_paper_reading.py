"""Compatibility wrapper for the original paper-reading evaluator."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from research_skills.evaluation import evaluate, read_rubric_values  # noqa: E402,F401
from scripts.evaluate_output import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
