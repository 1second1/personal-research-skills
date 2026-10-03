import unittest
from pathlib import Path

from research_skills.evaluation import evaluate, load_rubric, report_for


ROOT = Path(__file__).resolve().parents[1]


class EvaluationTests(unittest.TestCase):
    def test_all_public_rubrics_accept_their_expected_outputs(self) -> None:
        cases = (
            ("paper-reading", "paper-reading"),
            ("research-question", "research-question"),
            ("argument-analysis", "argument-analysis"),
        )

        for skill_name, rubric_name in cases:
            with self.subTest(skill=skill_name):
                candidate = (ROOT / f"skills/{skill_name}/examples/expected-output.md").read_text(
                    encoding="utf-8"
                )
                rubric = (ROOT / f"evals/rubrics/{rubric_name}.yaml").read_text(
                    encoding="utf-8"
                )
                self.assertEqual(evaluate(candidate, rubric), [])

    def test_empty_claim_headings_disable_source_claim_checks(self) -> None:
        rubric = """required_headings: [\"## Result\"]
required_markers: [\"bounded\"]
claim_headings: []
"""

        self.assertEqual(evaluate("## Result\nA bounded answer.", rubric), [])

    def test_report_is_versioned_and_explicit_about_semantic_quality(self) -> None:
        report = report_for(["Missing marker: Evidence:"], source_checked=False)

        self.assertEqual(report["schema_version"], "1.0")
        self.assertFalse(report["check_passed"])
        self.assertEqual(report["semantic_quality"], "not_evaluated")
        self.assertEqual(report["errors"], ["Missing marker: Evidence:"])

    def test_rubric_rejects_unknown_fields(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown rubric fields"):
            load_rubric("required_headings: [\"## Result\"]\nscore: 10\n")

    def test_fenced_examples_cannot_satisfy_output_requirements(self) -> None:
        rubric = 'required_headings: ["## Result"]\nrequired_markers: ["bounded"]\nclaim_headings: []\n'
        examples = (
            "```markdown\n## Result\nbounded\n```\n",
            "~~~markdown\n## Result\nbounded\n~~~\n",
            "````markdown\n```\n## Result\nbounded\n````\n",
            "~~~markdown\n```\n## Result\nbounded\n~~~\n",
            "```markdown\n## Result\nbounded\n",
            "~~~markdown\n## Result\nbounded\n",
            "   ~~~markdown\n## Result\nbounded\n   ~~~~\n",
            "~~~markdown\n~~\n## Result\nbounded\n~~~\n",
            "```markdown\n``` not a closing fence\n## Result\nbounded\n```\n",
        )
        for candidate in examples:
            with self.subTest(candidate=candidate):
                errors = evaluate(candidate, rubric)
                self.assertIn("Missing or empty section: ## Result", errors)
                self.assertIn("Missing marker: bounded", errors)

    def test_fences_do_not_hide_real_sections_after_the_block(self) -> None:
        rubric = 'required_headings: ["## Result"]\nrequired_markers: ["bounded"]\nclaim_headings: []\n'
        for fence in ("```", "~~~"):
            with self.subTest(fence=fence):
                candidate = f"{fence}\nexample\n{fence}\n## Result\nA bounded answer.\n"
                self.assertEqual(evaluate(candidate, rubric), [])

    def test_four_space_indentation_is_not_a_fence(self) -> None:
        rubric = 'required_headings: ["## Result"]\nclaim_headings: []\n'
        candidate = "    ```\n## Result\nAn actual heading outside indented code.\n    ```\n"
        self.assertEqual(evaluate(candidate, rubric), [])


if __name__ == "__main__":
    unittest.main()
