import json
from pathlib import Path
import subprocess
import sys
import unittest

from research_skills.compose import compose_skill
from research_skills.evaluation import evaluate


ROOT = Path(__file__).resolve().parents[1]


class ManuscriptAuditTests(unittest.TestCase):
    def test_new_skill_is_discovered_by_existing_cli(self):
        result = subprocess.run(
            [sys.executable, "-m", "research_skills.cli", "list", "--format", "json"],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("manuscript-audit", json.loads(result.stdout)["skills"])

    def test_new_skill_composes_without_personal_profile(self):
        skill = ROOT / "skills/manuscript-audit"
        self.assertTrue((skill / "SKILL.md").is_file(), "New Skill entrypoint is missing")
        context = compose_skill(skill, ROOT / "profiles/reasoning-dna.yaml",
                                "Audit the supplied draft.", mode="skill")
        self.assertIn("confirmed_error", context)
        self.assertIn("excluded", context)
        self.assertNotIn("## Personal Reasoning DNA", context)

    def test_authored_audit_example_passes_structure_only(self):
        candidate = ROOT / "skills/manuscript-audit/examples/expected-output.md"
        self.assertTrue(candidate.is_file(), "Authored example is missing")
        rubric = (ROOT / "evals/rubrics/manuscript-audit.yaml").read_text(encoding="utf-8")
        self.assertEqual(evaluate(candidate.read_text(encoding="utf-8"), rubric), [])

    def test_clean_audit_needs_no_fabricated_finding(self):
        rubric_path = ROOT / "evals/rubrics/manuscript-audit.yaml"
        self.assertTrue(rubric_path.is_file(), "New structural rubric is missing")
        candidate = """## Summary
No material issue found in the supplied excerpt; implementation not inspected.
## Findings
None in the checked scope.
## Checks
Text inspection only. No executable check was run.
## Repair Plan
No change proposed on the supplied evidence.
## Recheck
Not requested; no previous audit supplied.
"""
        self.assertEqual(evaluate(candidate, rubric_path.read_text(encoding="utf-8")), [])

    def test_general_paper_rubric_does_not_force_case_specific_topics(self):
        candidate = """## Problem
Does the described method solve the stated task?
## Evidence
The abstract reports feasibility. [Source: Abstract]
## Conflicts and Anomalies
No inconsistency was found in the supplied abstract. [Source: Abstract]
## Inferences
No additional mechanism conclusion is justified.
## Assumptions
Implementation matches the description; this was not inspected.
## Boundaries
Only the abstract was supplied.
## Connections
No additional research context was supplied.
## Next Actions
Inspect the method and evaluation sections before making a comparative claim.
"""
        rubric = (ROOT / "evals/rubrics/paper-reading.yaml").read_text(encoding="utf-8")
        self.assertEqual(evaluate(candidate, rubric, source_text="# Abstract\nFeasibility is reported."), [])


if __name__ == "__main__":
    unittest.main()
