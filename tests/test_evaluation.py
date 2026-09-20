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


if __name__ == "__main__":
    unittest.main()
