import subprocess
import sys
import unittest
from pathlib import Path

from research_skills.compose import compose_skill
from research_skills.dna import load_contract


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "argument-analysis"


class ArgumentAnalysisSkillTests(unittest.TestCase):
    def test_contract_exposes_argument_specific_outputs(self):
        contract = load_contract(SKILL / "contract.yaml")

        self.assertEqual(contract["name"], "argument-analysis")
        self.assertEqual(
            contract["outputs"],
            [
                "thesis",
                "argument_map",
                "evidence",
                "assumptions",
                "counterarguments",
                "boundaries",
                "implications",
            ],
        )

    def test_composed_context_targets_argumentative_prose(self):
        result = compose_skill(SKILL, ROOT / "profiles" / "reasoning-dna.yaml")

        self.assertIn("## Argument Map", result)
        self.assertIn("claim → support → warrant", result)
        self.assertIn("reader_goal", result)
        self.assertNotIn("confidence interval", result.lower())

    def test_cli_composes_the_example(self):
        completed = subprocess.run(
            [
                sys.executable,
                "scripts/run_skill.py",
                "argument-analysis",
                "skills/argument-analysis/examples/input.md",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("## Argument Map", completed.stdout)
        self.assertIn("A durable research tool", completed.stdout)


if __name__ == "__main__":
    unittest.main()
