import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "evals/fixtures/paper-reading-demo/evidence-card.md"
RUBRIC = ROOT / "evals/rubrics/paper-reading.yaml"


class EvaluatePaperReadingTests(unittest.TestCase):
    def test_evaluator_accepts_bundled_evidence_card(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/evaluate_paper_reading.py", str(FIXTURE), str(RUBRIC)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Evaluation passed", result.stdout)

    def test_evaluator_rejects_missing_inference_label(self) -> None:
        text = FIXTURE.read_text(encoding="utf-8").replace("Inference:", "Interpretation:")
        candidate = ROOT / "tests/fixtures/missing-inference-card.md"
        candidate.write_text(text, encoding="utf-8")
        self.addCleanup(candidate.unlink)

        result = subprocess.run(
            [sys.executable, "scripts/evaluate_paper_reading.py", str(candidate), str(RUBRIC)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Inference:", result.stderr)
