import importlib.util
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "evals/cases/manuscript-audit-demo"


def load_module(name, filename):
    path = CASE / filename
    assert path.is_file(), f"Teaching-case implementation is missing: {filename}"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def modules():
    experiment = load_module("experiment", "experiment.py")
    checker = load_module("audit_demo_verify", "verify.py")
    return experiment, checker


class ManuscriptDemoTests(unittest.TestCase):
    def test_original_actual_run_reveals_overlap_and_reporting_error(self):
        experiment, checker = modules()
        data = experiment.read_data(CASE / "data.csv")
        config = json.loads((CASE / "original/config.json").read_text(encoding="utf-8"))
        result = experiment.run_experiment(data, config)
        check = checker.verify(data, config, (CASE / "original/manuscript.md").read_text(encoding="utf-8"), result)
        self.assertEqual(result["metrics"]["accuracy"], 1.0)
        self.assertEqual(result["metrics"]["n_test"], 12)
        self.assertFalse(check["check_passed"])
        self.assertFalse(check["checks"]["patient_disjoint"]["passed"])
        self.assertFalse(check["checks"]["reported_accuracy_matches"]["passed"])
        self.assertTrue(check["checks"]["normalizer_train_only"]["passed"])

    def test_revised_material_passes_identical_checks_and_matches_saved_run(self):
        experiment, checker = modules()
        data = experiment.read_data(CASE / "data.csv")
        config = json.loads((CASE / "revised/config.json").read_text(encoding="utf-8"))
        result = experiment.run_experiment(data, config)
        check = checker.verify(data, config, (CASE / "revised/manuscript.md").read_text(encoding="utf-8"), result)
        self.assertTrue(check["check_passed"], check)
        self.assertEqual(result["metrics"]["n_test"], 16)
        stored = json.loads((CASE / "revised/result.json").read_text(encoding="utf-8"))
        self.assertEqual(stored["metrics"], result["metrics"])
        self.assertEqual(stored["predictions"], result["predictions"])

    def test_test_only_perturbation_cannot_change_training_normalizer(self):
        experiment, _ = modules()
        data = experiment.read_data(CASE / "data.csv")
        config = json.loads((CASE / "original/config.json").read_text(encoding="utf-8"))
        result = experiment.run_experiment(data, config)
        test_ids = set(result["test_sample_ids"])
        perturbed = [dict(row, feature_1=row["feature_1"] + 10000) if row["sample_id"] in test_ids else row for row in data]
        self.assertEqual(experiment.run_experiment(perturbed, config)["normalizer"], result["normalizer"])

    def test_checker_detects_forged_fit_scope_or_predictions(self):
        experiment, checker = modules()
        data = experiment.read_data(CASE / "data.csv")
        config = json.loads((CASE / "original/config.json").read_text(encoding="utf-8"))
        manuscript = (CASE / "original/manuscript.md").read_text(encoding="utf-8")
        for mutation in ("fit_scope", "predictions"):
            with self.subTest(mutation=mutation):
                result = experiment.run_experiment(data, config)
                if mutation == "fit_scope":
                    result["normalizer"]["fit_sample_ids"].append(result["test_sample_ids"][0])
                else:
                    result["predictions"][0]["prediction"] ^= 1
                check = checker.verify(data, config, manuscript, result)
                self.assertFalse(check["checks"]["result_matches_rerun"]["passed"])
                if mutation == "fit_scope":
                    self.assertFalse(check["checks"]["normalizer_train_only"]["passed"])

    def test_missing_reported_metric_fails_instead_of_silently_passing(self):
        experiment, checker = modules()
        data = experiment.read_data(CASE / "data.csv")
        config = json.loads((CASE / "original/config.json").read_text(encoding="utf-8"))
        check = checker.verify(data, config, "No table supplied.", experiment.run_experiment(data, config))
        self.assertFalse(check["checks"]["reported_accuracy_matches"]["passed"])


if __name__ == "__main__":
    unittest.main()
