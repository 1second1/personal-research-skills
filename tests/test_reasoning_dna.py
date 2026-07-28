import unittest
from pathlib import Path

from research_skills.compose import compose_skill
from research_skills.dna import load_profile


ROOT = Path(__file__).parents[1]


class ReasoningDnaTests(unittest.TestCase):
    def test_bundled_profile_contains_the_four_layer_model(self):
        profile = load_profile(ROOT / "profiles" / "reasoning-dna.yaml")

        self.assertEqual(profile["identity"]["name"], "personal-researcher")
        self.assertIn("values", profile)
        self.assertIn("thinking", profile)
        self.assertIn("workflows", profile)
        self.assertIn("preferences", profile)
        self.assertIn("assumption_check", profile["thinking"])

    def test_incomplete_profile_reports_missing_sections(self):
        with self.assertRaisesRegex(ValueError, "thinking"):
            load_profile(ROOT / "tests" / "fixtures" / "incomplete-dna.yaml")

    def test_composed_skill_contains_profile_rules_and_skill_contract(self):
        result = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
        )

        self.assertIn("Long-term value over short-term novelty", result)
        self.assertIn("What → Why → Assumption → Boundary", result)
        self.assertIn("## Problem", result)
        self.assertIn("## Evidence", result)


if __name__ == "__main__":
    unittest.main()
