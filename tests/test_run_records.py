import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import yaml

from research_skills.run_records import (
    ARTIFACT_NAMES,
    CONDITIONS,
    REQUIRED_FIELDS,
    validate_run_record,
)


ROOT = Path(__file__).resolve().parents[1]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_record(root: Path, *, condition: str = "skill") -> Path:
    artifacts = root / "artifacts"
    artifacts.mkdir(parents=True)
    for name in ARTIFACT_NAMES:
        (artifacts / f"{name}.md").write_text(f"# {name}\n", encoding="utf-8")
    record = {
        "schema_version": "1.0",
        "run_id": f"RQ-01-{condition}-r1",
        "task_id": "RQ-01",
        "condition": condition,
        "repetition": 1,
        "created_at": "2026-09-19T12:00:00Z",
        "repository_revision": "06a4e609b046698e77d01e0712f59edb973118ae",
        "model": {"provider": "fixture", "name": "deterministic-demo", "version": "1"},
        "generation": {
            "temperature": 0,
            "seed": 42,
            "max_output_tokens": 1024,
            "tools": [],
        },
        "artifacts": {name: f"artifacts/{name}.md" for name in ARTIFACT_NAMES},
        "digests": {
            name: _digest(artifacts / f"{name}.md") for name in ARTIFACT_NAMES
        },
        "review": {"status": "unreviewed"},
    }
    path = root / "run.yaml"
    path.write_text(yaml.safe_dump(record, sort_keys=False), encoding="utf-8")
    return path


class RunRecordTests(unittest.TestCase):
    def test_bundled_demo_run_record_is_valid(self) -> None:
        record = ROOT / "evals/fixtures/run-record-demo/run.yaml"

        self.assertEqual(validate_run_record(record, root=ROOT), [])

    def test_valid_record_checks_files_and_digests(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = _write_record(root)

            errors = validate_run_record(record, root=root)

        self.assertEqual(errors, [])

    def test_bad_digest_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = _write_record(root)
            data = yaml.safe_load(record.read_text(encoding="utf-8"))
            data["digests"]["output"] = "0" * 64
            record.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            errors = validate_run_record(record, root=root)

        self.assertTrue(any("Digest mismatch for output" in error for error in errors))

    def test_path_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = _write_record(root)
            data = yaml.safe_load(record.read_text(encoding="utf-8"))
            data["artifacts"]["output"] = "../private.md"
            record.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            errors = validate_run_record(record, root=root)

        self.assertTrue(any("must stay under the evaluation root" in error for error in errors))

    def test_created_at_requires_a_timezone(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            record = _write_record(root)
            data = yaml.safe_load(record.read_text(encoding="utf-8"))
            data["created_at"] = "2026-09-19T12:00:00"
            record.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            errors = validate_run_record(record, root=root)

        self.assertTrue(any("timezone" in error for error in errors))

    def test_temperature_must_be_finite_and_non_negative(self) -> None:
        for temperature in (float("nan"), float("inf"), -0.1):
            with self.subTest(temperature=temperature):
                with tempfile.TemporaryDirectory() as temporary_directory:
                    root = Path(temporary_directory)
                    record = _write_record(root)
                    data = yaml.safe_load(record.read_text(encoding="utf-8"))
                    data["generation"]["temperature"] = temperature
                    record.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

                    errors = validate_run_record(record, root=root)

                self.assertTrue(any("temperature" in error for error in errors))

    def test_public_json_schema_matches_runtime_constants(self) -> None:
        schema = json.loads(
            (ROOT / "evals/schemas/run-record-v1.schema.json").read_text(encoding="utf-8")
        )

        self.assertEqual(set(schema["required"]), set(REQUIRED_FIELDS))
        self.assertEqual(set(schema["properties"]["condition"]["enum"]), set(CONDITIONS))
        self.assertEqual(schema["properties"]["generation"]["properties"]["temperature"]["minimum"], 0)
        self.assertEqual(
            set(schema["properties"]["artifacts"]["required"]), set(ARTIFACT_NAMES)
        )


if __name__ == "__main__":
    unittest.main()
