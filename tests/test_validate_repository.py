import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import REQUIRED_PATHS, validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateRepositoryTests(unittest.TestCase):
    def test_real_paper_case_is_a_required_public_artifact(self) -> None:
        expected = {
            "evals/cases/u-mamba-real-paper/README.md",
            "evals/cases/u-mamba-real-paper/case.yaml",
            "evals/cases/u-mamba-real-paper/source-map.md",
            "evals/cases/u-mamba-real-paper/expected-output.md",
            "evals/cases/u-mamba-real-paper/rubric.yaml",
        }

        self.assertTrue(expected.issubset(REQUIRED_PATHS))

    def test_validator_rejects_nested_pdf_regardless_of_extension_case(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            pdf_path = root / "evals/cases/example/nested/Source.PDF"
            pdf_path.parent.mkdir(parents=True)
            pdf_path.write_bytes(b"%PDF-test")

            errors = validate(root)

        self.assertTrue(any("source PDF" in error for error in errors))

    def test_validator_reports_missing_required_files(self) -> None:
        incomplete_root = ROOT / "tests/fixtures/incomplete-repository"
        result = subprocess.run(
            [sys.executable, "scripts/validate_repository.py", "--root", str(incomplete_root)],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required file", result.stderr)

    def test_validator_accepts_complete_repository(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_repository.py", "--root", "."],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Repository validation passed", result.stdout)
