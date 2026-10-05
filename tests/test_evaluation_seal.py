import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def validator():
    path = ROOT / "scripts/verify_evaluation_seal.py"
    assert path.is_file(), "Evaluation seal checker is missing"
    spec = importlib.util.spec_from_file_location("evaluation_seal", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.verify_seal


def fixture(root):
    (root / "materials").mkdir()
    payload = b"synthetic input\n"
    (root / "materials/input.md").write_bytes(payload)
    value = {"schema_version":"1.0", "sealed_directories":["materials"],
             "files":[{"path":"materials/input.md", "size":len(payload),
                       "sha256":hashlib.sha256(payload).hexdigest()}]}
    path = root / "seal.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path, value


class EvaluationSealTests(unittest.TestCase):
    def test_valid_package_is_verified(self):
        verify = validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, _ = fixture(root)
            self.assertEqual(verify(manifest, root), [])

    def test_mutation_and_unlisted_file_are_detected(self):
        verify = validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, _ = fixture(root)
            (root / "materials/input.md").write_text("changed", encoding="utf-8")
            (root / "materials/extra.md").write_text("unsealed", encoding="utf-8")
            errors = verify(manifest, root)
            self.assertTrue(any("Digest mismatch" in e for e in errors))
            self.assertTrue(any("Unsealed file" in e for e in errors))

    def test_external_path_and_duplicate_entry_are_rejected(self):
        verify = validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest, value = fixture(root)
            value["files"].append(value["files"][0])
            value["files"].append({"path":"../outside.md", "size":0, "sha256":"0"*64})
            manifest.write_text(json.dumps(value), encoding="utf-8")
            errors = verify(manifest, root)
            self.assertTrue(any("Duplicate" in e for e in errors))
            self.assertTrue(any("escapes" in e for e in errors))

    def test_empty_manifest_is_not_a_valid_seal(self):
        verify = validator()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "seal.json"
            manifest.write_text('{"schema_version":"1.0","sealed_directories":[],"files":[]}', encoding="utf-8")
            self.assertTrue(verify(manifest, root))


if __name__ == "__main__":
    unittest.main()
