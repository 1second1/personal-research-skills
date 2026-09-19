import unittest
from pathlib import Path

from research_skills.dna import _parse, load_profile
from research_skills.compose import compose_skill
from scripts.evaluate_paper_reading import evaluate

ROOT = Path(__file__).resolve().parents[1]


class IntegrityTests(unittest.TestCase):
    def test_quoted_hash_and_comma_are_preserved(self):
        self.assertEqual(_parse('name: "Evidence #1"\nitems: ["a,b", c]'),
                         {'name': 'Evidence #1', 'items': ['a,b', 'c']})

    def test_duplicate_keys_rejected(self):
        with self.assertRaises(ValueError):
            _parse('name: first\nname: second')

    def test_invalid_profile_type_rejected_at_load(self):
        with self.assertRaises(ValueError):
            load_profile(ROOT / 'tests/fixtures/invalid-types.yaml')

    def test_workflows_and_full_contract_reach_context(self):
        result = compose_skill(ROOT / 'skills/paper-reading', ROOT / 'profiles/reasoning-dna.yaml')
        self.assertIn('Question → Evidence → Inference → Boundary → Experiment → Review', result)
        self.assertIn('source_locations', result)
        self.assertIn('factual_consistency', result)

    def test_empty_rubric_rejected(self):
        with self.assertRaises(ValueError):
            evaluate('', '')

    def test_empty_sections_rejected(self):
        rubric = 'required_headings:\n  - "## Evidence"\nrequired_markers:\n  - "[Source:"'
        self.assertTrue(evaluate('## Evidence\n[Source:', rubric))

    def test_heading_inside_prose_does_not_count(self):
        self.assertTrue(evaluate('text ## Evidence\nSome result', 'required_headings: ["## Evidence"]'))

    def test_source_checks_accept_known_citation_and_value(self):
        errors = evaluate('## Evidence\n- Dice 0.842. [Source: Note]', 'required_headings: ["## Evidence"]', source_text='# Note\nDice 0.842.')
        self.assertEqual(errors, [])

    def test_source_checks_reject_invented_citation(self):
        errors = evaluate('## Evidence\n- Dice 0.842. [Source: Invented]', 'required_headings: ["## Evidence"]', source_text='# Note\nDice 0.842.')
        self.assertTrue(any('source' in error.lower() for error in errors))

    def test_source_checks_reject_invented_number(self):
        errors = evaluate('## Evidence\n- Dice 0.999. [Source: Note]', 'required_headings: ["## Evidence"]', source_text='# Note\nDice 0.842.')
        self.assertTrue(any('0.999' in error for error in errors))

    def test_source_checks_reject_reversed_numeric_sign(self):
        errors = evaluate(
            '## Evidence\n- Change was 0.5. [Source: Note]',
            'required_headings: ["## Evidence"]',
            source_text='# Note\nChange was -0.5.',
        )
        self.assertTrue(any('0.5' in error for error in errors))

    def test_comparison_modes_isolate_profile_and_skill(self):
        base = ROOT / 'skills/paper-reading'
        profile = ROOT / 'profiles/reasoning-dna.yaml'
        baseline = compose_skill(base, profile, input_text='Unique input', mode='baseline')
        skill = compose_skill(base, profile, input_text='Unique input', mode='skill')
        full = compose_skill(base, profile, input_text='Unique input', mode='profile')
        for context in (baseline, skill, full):
            self.assertIn('Unique input', context)
        self.assertNotIn('## Skill Contract', baseline)
        self.assertIn('## Skill Contract', skill)
        self.assertNotIn('## Personal Reasoning DNA', skill)
        self.assertIn('## Personal Reasoning DNA', full)

    def test_invalid_comparison_mode_rejected(self):
        with self.assertRaises(ValueError):
            compose_skill(ROOT / 'skills/paper-reading', ROOT / 'profiles/reasoning-dna.yaml', mode='unknown')
