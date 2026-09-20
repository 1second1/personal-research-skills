import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

from research_skills.blinding import prepare_blind_review
from research_skills.run_records import ARTIFACT_NAMES


ROOT = Path(__file__).resolve().parents[1]


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record(root: Path, condition: str, text: str) -> Path:
    run_root = root / condition
    run_root.mkdir(parents=True)
    for name in ARTIFACT_NAMES:
        content = text if name == "output" else f"# {name}\n"
        (run_root / f"{name}.md").write_text(content, encoding="utf-8")
    data = {
        "schema_version": "1.0",
        "run_id": f"RQ-01-{condition}-r1",
        "task_id": "RQ-01",
        "condition": condition,
        "repetition": 1,
        "created_at": "2026-09-19T12:00:00Z",
        "repository_revision": "06a4e609b046698e77d01e0712f59edb973118ae",
        "model": {"provider": "fixture", "name": "deterministic-demo", "version": "1"},
        "generation": {"temperature": 0, "seed": 7, "max_output_tokens": 256, "tools": []},
        "artifacts": {name: f"{condition}/{name}.md" for name in ARTIFACT_NAMES},
        "digests": {name: _digest(run_root / f"{name}.md") for name in ARTIFACT_NAMES},
        "review": {"status": "unreviewed"},
    }
    path = root / f"{condition}.yaml"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    return path


class BlindingTests(unittest.TestCase):
    def test_blind_manifest_hides_conditions_and_key_retains_them(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            records = [
                _record(root, "baseline", "baseline output"),
                _record(root, "profile", "profile output"),
            ]
            export = root / "review"

            prepare_blind_review(records, export, root=root, seed=23)

            manifest_text = (export / "review-manifest.json").read_text(encoding="utf-8")
            key = json.loads((export / "private/review-key.json").read_text(encoding="utf-8"))
            manifest = json.loads(manifest_text)

            self.assertNotIn("baseline", manifest_text)
            self.assertNotIn("profile", manifest_text)
            self.assertNotIn("seed", manifest)
            self.assertEqual(
                {entry["condition"] for entry in key["candidates"]}, {"baseline", "profile"}
            )
            self.assertEqual(
                [item["blind_id"] for item in manifest["candidates"]], ["R001", "R002"]
            )
            for item in manifest["candidates"]:
                self.assertTrue((export / item["file"]).is_file())

    def test_same_seed_produces_same_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            records = [
                _record(root, "baseline", "baseline output"),
                _record(root, "skill", "skill output"),
                _record(root, "profile", "profile output"),
            ]

            prepare_blind_review(records, root / "one", root=root, seed=91)
            prepare_blind_review(records, root / "two", root=root, seed=91)

            one = (root / "one/private/review-key.json").read_text(encoding="utf-8")
            two = (root / "two/private/review-key.json").read_text(encoding="utf-8")

        self.assertEqual(one, two)

    def test_cli_creates_blind_review_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            records = [
                _record(root, "baseline", "baseline output"),
                _record(root, "skill", "skill output"),
            ]
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "research_skills.cli",
                    "--root",
                    str(root),
                    "blind",
                    str(records[0]),
                    str(records[1]),
                    "--seed",
                    "17",
                    "--output",
                    "review",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            key_exists = (root / "review/private/review-key.json").is_file()

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertTrue(key_exists)

    def test_duplicate_run_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            baseline = _record(root, "baseline", "baseline output")
            skill = _record(root, "skill", "skill output")
            data = yaml.safe_load(skill.read_text(encoding="utf-8"))
            data["run_id"] = "RQ-01-baseline-r1"
            skill.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Duplicate run_id"):
                prepare_blind_review([baseline, skill], root / "review", root=root, seed=3)


if __name__ == "__main__":
    unittest.main()
