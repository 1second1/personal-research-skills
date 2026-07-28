import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidateRepositoryTests(unittest.TestCase):
    def test_validator_reports_missing_required_files(self) -> None:
        result = subprocess.run(
            [sys.executable, "scripts/validate_repository.py", "--root", "."],
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
