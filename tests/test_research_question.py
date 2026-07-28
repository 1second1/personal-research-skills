import unittest
from pathlib import Path

from research_skills.compose import compose_skill


ROOT = Path(__file__).parents[1]


class ResearchQuestionSkillTests(unittest.TestCase):
    def test_skill_requires_a_falsifiable_question_contract(self):
        contract = (ROOT / "skills" / "research-question" / "contract.yaml").read_text(encoding="utf-8")
        skill = (ROOT / "skills" / "research-question" / "SKILL.md").read_text(encoding="utf-8")

        for marker in ("question", "hypothesis", "variables", "falsification", "next_actions"):
            self.assertIn(marker, contract)
            self.assertIn(marker, skill.lower())

    def test_skill_inherits_the_personal_inquiry_pattern(self):
        result = compose_skill(
            ROOT / "skills" / "research-question",
            ROOT / "profiles" / "reasoning-dna.yaml",
        )
        self.assertIn("What → Why → Assumption → Boundary", result)
        self.assertIn("## Research Question", result)


if __name__ == "__main__":
    unittest.main()
