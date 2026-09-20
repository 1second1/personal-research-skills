import importlib.metadata
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RunSkillTests(unittest.TestCase):
    def test_distribution_exposes_console_entry_point(self):
        entry_points = tuple(
            importlib.metadata.entry_points(
                group="console_scripts",
                name="research-skills",
            )
        )

        self.assertEqual(len(entry_points), 1)
        self.assertEqual(entry_points[0].value, "research_skills.cli:main")

    def test_cli_reads_input_from_stdin(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "paper-reading", "-"],
            cwd=ROOT,
            input="A supplied study reports Dice 0.842.",
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("A supplied study reports Dice 0.842.", completed.stdout)

    def test_cli_writes_utf8_output_file(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "context.md"
            completed = subprocess.run(
                [
                    sys.executable,
                    "scripts/run_skill.py",
                    "paper-reading",
                    "skills/paper-reading/examples/input.md",
                    "--output",
                    str(output_path),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            output = output_path.read_text(encoding="utf-8") if output_path.is_file() else ""

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertIn("What → Why → Assumption → Boundary", output)

    def test_cli_reports_invalid_utf8_without_traceback(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "invalid.md"
            input_path.write_bytes(b"\xff")
            completed = subprocess.run(
                [sys.executable, "scripts/run_skill.py", "paper-reading", str(input_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 1)
        self.assertIn("Could not compose Skill", completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_module_cli_accepts_explicit_repository_root(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "research_skills.cli",
                    "--root",
                    str(ROOT),
                    "paper-reading",
                    "skills/paper-reading/examples/input.md",
                ],
                cwd=temporary_directory,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## Skill Contract", completed.stdout)

    def test_legacy_cli_accepts_repository_root_after_positionals(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "research_skills.cli",
                    "paper-reading",
                    "skills/paper-reading/examples/input.md",
                    "--root",
                    str(ROOT),
                ],
                cwd=temporary_directory,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## Skill Contract", completed.stdout)

    def test_cli_composes_paper_reading_with_default_profile(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "paper-reading", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## Personal Reasoning DNA", completed.stdout)
        self.assertIn("## Evidence", completed.stdout)

    def test_cli_rejects_unknown_skill(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "missing", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("Unknown Skill", completed.stderr)

    # --- Phase 0: input content and contract assertions ---

    def test_cli_includes_input_content_in_output(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "paper-reading", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        # Input file content must appear in the output with a clear delimiter.
        self.assertIn("## Input Document", completed.stdout)
        self.assertIn("LiteSeg", completed.stdout)

    def test_cli_includes_contract_version_in_output(self):
        completed = subprocess.run(
            [sys.executable, "scripts/run_skill.py", "paper-reading", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        # Contract name and version must be visible.
        self.assertIn("paper-reading", completed.stdout)
        self.assertIn("Contract: contract.yaml version 0.2.0", completed.stdout)

    def test_cli_exposes_version(self):
        completed = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "--version"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertRegex(completed.stdout, r"research-skills \d+\.\d+\.\d+")

    def test_cli_lists_skills_as_json(self):
        completed = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "list", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(
            set(__import__("json").loads(completed.stdout)["skills"]),
            {"argument-analysis", "paper-reading", "research-question"},
        )

    def test_explicit_compose_subcommand_matches_legacy_form(self):
        legacy = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "paper-reading", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        explicit = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "compose", "paper-reading", "skills/paper-reading/examples/input.md"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(legacy.returncode, 0, legacy.stderr)
        self.assertEqual(explicit.returncode, 0, explicit.stderr)
        self.assertEqual(legacy.stdout, explicit.stdout)

    def test_cli_validate_subcommand_checks_repository(self):
        completed = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "validate"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Repository validation passed", completed.stdout)

    def test_cli_validate_subcommand_checks_run_record(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "research_skills.cli",
                "validate",
                "--run",
                "evals/fixtures/run-record-demo/run.yaml",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Run record validation passed", completed.stdout)

    def test_cli_evaluate_subcommand_emits_versioned_json(self):
        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "research_skills.cli",
                "evaluate",
                "skills/research-question/examples/expected-output.md",
                "evals/rubrics/research-question.yaml",
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = __import__("json").loads(completed.stdout)
        self.assertEqual(report["schema_version"], "1.0")
        self.assertTrue(report["check_passed"])


if __name__ == "__main__":
    unittest.main()
