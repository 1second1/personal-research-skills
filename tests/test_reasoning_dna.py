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

    # --- Phase 0: input content, contract, version, and source path assertions ---

    def test_composed_skill_includes_input_content(self):
        result = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
            input_text="LiteSeg reports Dice 0.842 on Dataset-A.",
        )

        self.assertIn("## Input Document", result)
        self.assertIn("LiteSeg reports Dice 0.842 on Dataset-A.", result)

    def test_changing_input_changes_output(self):
        result_a = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
            input_text="Input alpha: segmentation model X with Dice 0.9.",
        )
        result_b = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
            input_text="Input beta: segmentation model Y with Dice 0.7.",
        )

        self.assertIn("Input alpha", result_a)
        self.assertIn("Input beta", result_b)
        self.assertNotEqual(result_a, result_b)

    def test_composed_skill_includes_contract_fields(self):
        result = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
        )

        self.assertIn("paper-reading", result)
        self.assertIn("version", result.lower())

    def test_composed_skill_includes_version_and_source_info(self):
        result = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
        )

        # Profile version from reasoning-dna.yaml
        self.assertIn("0.1.0", result)
        # Source path markers (profile path and skill directory appear in metadata)
        self.assertIn("reasoning-dna.yaml", result)
        self.assertIn("paper-reading", result)

    def test_backward_compatible_without_input(self):
        """Calling compose_skill without input_text must still work."""
        result = compose_skill(
            ROOT / "skills" / "paper-reading",
            ROOT / "profiles" / "reasoning-dna.yaml",
        )

        self.assertIn("## Personal Reasoning DNA", result)
        self.assertIn("## Skill Contract", result)
        self.assertIn("## Evidence", result)


if __name__ == "__main__":
    unittest.main()
