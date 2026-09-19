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

    def test_paper_reading_context_requires_conflict_reporting(self):
        result = compose_skill(ROOT / 'skills/paper-reading', ROOT / 'profiles/reasoning-dna.yaml')
        self.assertIn('conflicts_and_anomalies', result)
        self.assertIn('## Conflicts and Anomalies', result)
        self.assertIn('Do not silently reconcile', result)

    def test_real_case_manifest_pins_source_without_redistributing_pdf(self):
        case_root = ROOT / 'evals/cases/u-mamba-real-paper'
        manifest_path = case_root / 'case.yaml'
        self.assertTrue(manifest_path.is_file(), 'real-paper case manifest is missing')
        manifest = _parse(manifest_path.read_text(encoding='utf-8'))
        self.assertEqual(manifest['paper']['arxiv_id'], '2401.04722')
        self.assertEqual(manifest['paper']['version'], 'v1')
        self.assertEqual(manifest['source_file']['bytes'], 13369554)
        self.assertEqual(
            manifest['source_file']['sha256'],
            '2ffc896ee1fdea0410d5e5608b56a6577f6d3cc30bede40daa7e4c181ecb7709',
        )
        self.assertFalse(manifest['source_file']['redistributed'])
        self.assertEqual(
            [path for path in case_root.rglob('*') if path.suffix.casefold() == '.pdf'],
            [],
        )

    def test_real_case_does_not_claim_reproducibility_without_execution(self):
        output = (ROOT / 'evals/cases/u-mamba-real-paper/expected-output.md').read_text(
            encoding='utf-8'
        )
        self.assertNotIn('reproducible comparison family', output)
        self.assertIn('public implementation', output)

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

    def test_configured_conflict_section_rejects_unknown_citation(self):
        rubric = (
            'required_headings: ["## Conflicts and Anomalies"]\n'
            'claim_headings: ["## Conflicts and Anomalies"]'
        )
        try:
            errors = evaluate(
                '## Conflicts and Anomalies\n'
                '- Conflict: table and prose disagree. [Source: Invented location]',
                rubric,
                source_text='# Verified location\nTable and prose disagree.',
            )
        except ValueError as error:
            self.fail(f'claim_headings should be supported: {error}')
        self.assertTrue(any('source' in error.lower() for error in errors))

    def test_configured_conflict_section_rejects_number_absent_from_source(self):
        rubric = (
            'required_headings: ["## Conflicts and Anomalies"]\n'
            'claim_headings: ["## Conflicts and Anomalies"]'
        )
        try:
            errors = evaluate(
                '## Conflicts and Anomalies\n'
                '- Conflict: narrative reports 0.6504. [Source: Verified location]',
                rubric,
                source_text='# Verified location\nTable reports 0.6540.',
            )
        except ValueError as error:
            self.fail(f'claim_headings should be supported: {error}')
        self.assertTrue(any('0.6504' in error for error in errors))

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
