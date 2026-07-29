import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class RunSkillTests(unittest.TestCase):
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
        self.assertIn("0.1.0", completed.stdout)


if __name__ == "__main__":
    unittest.main()
