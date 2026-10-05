import json
from pathlib import Path
import tempfile
import unittest

import yaml

from research_skills.blinding import prepare_blind_review
from research_skills.run_records import validate_run_record
from tests.test_run_records import ROOT, _digest, _write_record


def write_v1_2(root, condition="strong_prompt"):
    path = _write_record(root, condition=condition, schema_version="1.2")
    trace = root / "artifacts/trace.jsonl"
    trace.write_text('{"event":"fixture_only","model_executed":false}\n', encoding="utf-8", newline="\n")
    record = yaml.safe_load(path.read_text(encoding="utf-8"))
    record["artifacts"]["trace"] = "artifacts/trace.jsonl"
    record["digests"]["trace"] = _digest(trace)
    record["measurements"] = {
        "wall_time_seconds": 1.5, "model_calls": 0,
        "input_tokens": None, "output_tokens": None,
        "cost": None, "currency": None, "cost_basis": "unavailable",
    }
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8", newline="\n")
    return path


def save(path, record):
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8", newline="\n")


class RunRecordsV12Tests(unittest.TestCase):
    def test_malformed_enum_types_report_errors_instead_of_crashing(self):
        for field in ("schema_version", "cost_basis"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = write_v1_2(root)
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                if field == "schema_version":
                    record[field] = []
                else:
                    record["measurements"][field] = {}
                save(path, record)
                self.assertTrue(any(field in e for e in validate_run_record(path, root=root)))

    def test_new_conditions_with_unknown_cost_and_trace_are_valid(self):
        for condition in ("strong_prompt", "skill", "peer_review"):
            with self.subTest(condition=condition), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = write_v1_2(root, condition)
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                record["generation"].update(temperature=None, max_output_tokens=None, reasoning_effort="low")
                save(path, record)
                self.assertEqual(validate_run_record(path, root=root), [])

    def test_old_versions_reject_new_conditions_and_measurements(self):
        for version in ("1.0", "1.1"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = _write_record(root, condition="strong_prompt", schema_version=version)
                self.assertTrue(any("condition" in e for e in validate_run_record(path, root=root)))
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                record["condition"] = "skill"
                record["measurements"] = {}
                save(path, record)
                self.assertTrue(any("Unknown run-record fields" in e for e in validate_run_record(path, root=root)))

    def test_new_record_requires_trace_and_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = _write_record(root, schema_version="1.2")
            errors = validate_run_record(path, root=root)
            self.assertTrue(any("measurements" in e for e in errors))
            self.assertTrue(any("trace" in e for e in errors))

    def test_optional_generation_controls_reject_invalid_types(self):
        for field in ("reasoning_effort", "verbosity"):
            for value in ([], 2, " "):
                with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    path = write_v1_2(root)
                    record = yaml.safe_load(path.read_text(encoding="utf-8"))
                    record["generation"][field] = value
                    save(path, record)
                    self.assertTrue(any(f"generation.{field}" in e for e in validate_run_record(path, root=root)))

    def test_trace_is_subject_to_digest_and_containment_checks(self):
        for bad_value in ("../outside.jsonl", "artifacts/trace.jsonl"):
            with self.subTest(value=bad_value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = write_v1_2(root)
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                record["artifacts"]["trace"] = bad_value
                record["digests"]["trace"] = "0" * 64
                save(path, record)
                errors = validate_run_record(path, root=root)
                self.assertTrue(any("trace" in e for e in errors))

    def test_invalid_measurements_are_rejected(self):
        cases = [("wall_time_seconds", -1), ("wall_time_seconds", float("nan")),
                 ("model_calls", True), ("input_tokens", 1.2), ("output_tokens", -1),
                 ("cost", float("inf")), ("currency", "usd"), ("cost_basis", "guessed")]
        for field, value in cases:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                path = write_v1_2(root)
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                record["measurements"][field] = value
                save(path, record)
                self.assertTrue(any(field in e for e in validate_run_record(path, root=root)))

    def test_available_cost_requires_currency_and_basis(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = write_v1_2(root)
            record = yaml.safe_load(path.read_text(encoding="utf-8"))
            record["measurements"]["cost"] = 0
            save(path, record)
            self.assertTrue(any("cost" in e or "currency" in e for e in validate_run_record(path, root=root)))
            record["measurements"].update(currency="USD", cost_basis="reported")
            save(path, record)
            self.assertEqual(validate_run_record(path, root=root), [])

    def test_blind_export_accepts_new_arms_without_exposing_trace_or_measurements(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            records = [write_v1_2(root / condition, condition) for condition in ("strong_prompt", "peer_review")]
            # Each record's artifact path is relative to its own test subroot.
            for path in records:
                record = yaml.safe_load(path.read_text(encoding="utf-8"))
                record["artifacts"] = {key: path.parent.name + "/" + value for key, value in record["artifacts"].items()}
                save(path, record)
            manifest = prepare_blind_review(records, root / "review", root=root, seed=41)
            text = json.dumps(manifest)
            self.assertNotIn("strong_prompt", text)
            self.assertNotIn("peer_review", text)
            self.assertNotIn("measurements", text)
            self.assertFalse((root / "review/candidates/trace.jsonl").exists())
            key = json.loads((root / "review/private/review-key.json").read_text(encoding="utf-8"))
            self.assertEqual({entry["condition"] for entry in key["candidates"]}, {"strong_prompt", "peer_review"})

    def test_public_v1_2_schema_documents_new_fields(self):
        path = ROOT / "evals/schemas/run-record-v1.2.schema.json"
        self.assertTrue(path.is_file(), "Public v1.2 schema is missing")
        schema = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "1.2")
        self.assertIn("peer_review", schema["properties"]["condition"]["enum"])
        self.assertIn("measurements", schema["required"])
        self.assertIn("trace", schema["properties"]["artifacts"]["required"])


if __name__ == "__main__":
    unittest.main()
