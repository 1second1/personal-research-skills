import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import REQUIRED_PATHS, validate


ROOT = Path(__file__).resolve().parents[1]


class ValidateRepositoryTests(unittest.TestCase):
    def test_validator_requires_profile_and_skill_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            errors = validate(Path(temporary_directory))

        self.assertIn("Missing required directory: profiles", errors)
        self.assertIn("Missing required directory: skills", errors)

    def test_validator_rejects_invalid_profile_schema(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            profile_path = root / "profiles/broken.yaml"
            profile_path.parent.mkdir(parents=True)
            profile_path.write_text("profile: broken\n", encoding="utf-8")

            errors = validate(root)

        self.assertTrue(any("Invalid profile" in error for error in errors))

    def test_validator_rejects_invalid_skill_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_root = root / "skills/example"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example Skill.\n---\n",
                encoding="utf-8",
            )
            (skill_root / "contract.yaml").write_text(
                "name: different-name\nversion: invalid\n",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertTrue(any("Invalid Skill contract" in error for error in errors))

    def test_validator_requires_standard_artifacts_for_discovered_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            skill_root = root / "skills/example"
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                "---\nname: example\ndescription: Example Skill.\n---\n",
                encoding="utf-8",
            )
            (skill_root / "contract.yaml").write_text(
                """name: example
version: 0.1.0
purpose: Demonstrate repository validation.
inputs:
  - name: source
    required: true
    type: text
outputs: [result]
constraints: [Do not invent evidence.]
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertTrue(
            any("Missing Skill artifact: skills/example/examples/input.md" in error for error in errors)
        )
        self.assertTrue(
            any("Missing Skill artifact: skills/example/evals/pressure-scenarios.md" in error for error in errors)
        )
        self.assertTrue(
            any("Missing Skill rubric: evals/rubrics/example.yaml" in error for error in errors)
        )

    def test_real_paper_case_is_a_required_public_artifact(self) -> None:
        expected = {
            "evals/cases/u-mamba-real-paper/README.md",
            "evals/cases/u-mamba-real-paper/case.yaml",
            "evals/cases/u-mamba-real-paper/source-map.md",
            "evals/cases/u-mamba-real-paper/expected-output.md",
            "evals/cases/u-mamba-real-paper/rubric.yaml",
        }

        self.assertTrue(expected.issubset(REQUIRED_PATHS))

    def test_latest_run_record_schema_is_a_required_public_artifact(self) -> None:
        self.assertIn("evals/schemas/run-record-v1.1.schema.json", REQUIRED_PATHS)

    def test_validator_rejects_nested_pdf_regardless_of_extension_case(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            pdf_path = root / "evals/cases/example/nested/Source.PDF"
            pdf_path.parent.mkdir(parents=True)
            pdf_path.write_bytes(b"%PDF-test")

            errors = validate(root)

        self.assertTrue(any("source PDF" in error for error in errors))

    def test_validator_rejects_invalid_discovered_run_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = root / "evals/fixtures/example/run.yaml"
            record.parent.mkdir(parents=True)
            record.write_text("schema_version: '1.0'\n", encoding="utf-8")

            errors = validate(root)

        self.assertTrue(any("Invalid run record" in error for error in errors))

    def test_validator_rejects_invalid_case_run_record(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = root / "evals/cases/example/runs/bad.yaml"
            record.parent.mkdir(parents=True)
            record.write_text("schema_version: '1.1'\n", encoding="utf-8")

            errors = validate(root)

        self.assertTrue(any("Invalid run record" in error for error in errors))

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
