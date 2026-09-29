"""Guard the archived evidence links for the proposed uncertainty feedback."""

import unittest
from pathlib import Path

import yaml

from research_skills.run_records import load_run_record, validate_run_record


ROOT = Path(__file__).resolve().parents[1]
FEEDBACK = ROOT / "evals/feedback/PR-REAL-01-plus-minus-v1.yaml"
REGRESSION = ROOT / "evals/regressions/PR-REAL-01-plus-minus-v1.yaml"
EXPECTED_RUNS = {
    "PR-REAL-01-skill-r3",
    "PR-REAL-01-profile-r1",
    "PR-REAL-01-profile-r2",
    "PR-REAL-01-profile-r3",
}


class UncertaintyFeedbackTests(unittest.TestCase):
    def test_feedback_links_to_four_integrity_checked_outputs(self) -> None:
        self.assertTrue(FEEDBACK.is_file(), "Missing versioned feedback artifact")
        feedback = yaml.safe_load(FEEDBACK.read_text(encoding="utf-8"))
        self.assertEqual(feedback["schema_version"], "1.0")
        self.assertEqual(feedback["status"], "proposed")
        self.assertEqual(feedback["target"], "paper-reading")
        self.assertTrue((ROOT / feedback["source"]).is_file())
        self.assertEqual(feedback["regression_case"], REGRESSION.relative_to(ROOT).as_posix())

        observations = feedback["observations"]
        self.assertEqual({item["run_id"] for item in observations}, EXPECTED_RUNS)
        self.assertEqual(len(observations), len(EXPECTED_RUNS))
        for item in observations:
            with self.subTest(run_id=item["run_id"]):
                record_path = (ROOT / item["run_record"]).resolve()
                output_path = (ROOT / item["output"]).resolve()
                self.assertTrue(record_path.is_relative_to(ROOT))
                self.assertTrue(output_path.is_relative_to(ROOT))
                self.assertEqual(validate_run_record(record_path, root=ROOT), [])
                record = load_run_record(record_path)
                self.assertEqual(record["run_id"], item["run_id"])
                self.assertEqual(record["artifacts"]["output"], item["output"])
                self.assertIn(item["quote"], output_path.read_text(encoding="utf-8"))

    def test_manual_regression_includes_safe_and_contradictory_examples(self) -> None:
        self.assertTrue(REGRESSION.is_file(), "Missing manual semantic regression case")
        regression = yaml.safe_load(REGRESSION.read_text(encoding="utf-8"))
        self.assertEqual(regression["schema_version"], "1.0")
        self.assertEqual(regression["review_mode"], "human_semantic")
        self.assertTrue((ROOT / regression["source"]).is_file())
        self.assertEqual(
            {item["id"]: item["expected"] for item in regression["examples"]},
            {
                "safe_unknown": "pass",
                "unsupported_sd": "fail",
                "claim_then_caveat": "fail",
            },
        )
        self.assertTrue(all(item["answer"].strip() for item in regression["examples"]))


if __name__ == "__main__":
    unittest.main()
