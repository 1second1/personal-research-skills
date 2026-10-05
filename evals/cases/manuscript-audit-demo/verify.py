"""Check split, reported accuracy, fit scope, and saved-result reproduction.

This is a teaching-case checker, not a semantic manuscript evaluator.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import re

from experiment import FEATURES, digest, partition, run_experiment, write_json


def verify(rows: list[dict], config: dict, manuscript: str, result: dict) -> dict:
    train, test = partition(rows, config)
    expected = run_experiment(rows, config)
    overlap = sorted({row["patient_id"] for row in train} & {row["patient_id"] for row in test})
    rerun_matches = all(result.get(key) == value for key, value in expected.items())
    match = re.findall(r"(?m)^\| Test accuracy \| (\d+(?:\.\d+)?) \|$", manuscript)
    reported = float(match[0]) if len(match) == 1 else None
    actual = sum(item["prediction"] == item["truth"] for item in expected["predictions"]) / len(test)
    normalizer = result.get("normalizer", {})
    fit_ids = normalizer.get("fit_sample_ids", [])
    expected_ids = [row["sample_id"] for row in train]
    independent_mean = {name: math.fsum(row[name] for row in train) / len(train) for name in FEATURES}
    independent_scale = {
        name: math.sqrt(math.fsum((row[name] - independent_mean[name]) ** 2 for row in train) / len(train)) or 1.0
        for name in FEATURES
    }
    test_ids = {row["sample_id"] for row in test}
    perturbed = [dict(row, feature_1=row["feature_1"] + 10000) if row["sample_id"] in test_ids else row for row in rows]
    unchanged_by_test = run_experiment(perturbed, config)["normalizer"] == expected["normalizer"]
    checks = {
        "patient_disjoint": {"passed": not overlap, "overlap_patient_ids": overlap},
        "reported_accuracy_matches": {"passed": reported is not None and abs(reported - actual) <= 0.0000005,
                                      "reported": reported, "recomputed": actual},
        "normalizer_train_only": {
            "passed": fit_ids == expected_ids and normalizer.get("mean") == independent_mean
                      and normalizer.get("scale") == independent_scale and unchanged_by_test,
            "fit_sample_count": len(fit_ids), "training_sample_count": len(train),
            "test_only_perturbation_preserves_normalizer": unchanged_by_test,
        },
        "result_matches_rerun": {"passed": rerun_matches},
    }
    return {"schema_version": "1.0", "synthetic": True,
            "check_passed": all(item["passed"] for item in checks.values()), "checks": checks,
            "semantic_quality": "not_evaluated",
            "not_checked": ["causal attribution wording requires manual evidence review",
                            "real-patient generalization", "statistical reliability", "training reproducibility"]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("data", "config", "manuscript", "result", "output"):
        parser.add_argument("--" + name, type=Path, required=True)
    args = parser.parse_args()
    try:
        from experiment import read_data
        result = json.loads(args.result.read_text(encoding="utf-8"))
        check = verify(read_data(args.data), json.loads(args.config.read_text(encoding="utf-8")),
                       args.manuscript.read_text(encoding="utf-8"), result)
        expected_digests = {"data": digest(args.data), "config": digest(args.config),
                            "experiment": digest(Path(__file__).with_name("experiment.py"))}
        check["checks"]["input_digests_match"] = {"passed": result.get("input_digests") == expected_digests}
        check["check_passed"] = all(item["passed"] for item in check["checks"].values())
        check["input_digests"] = {**expected_digests, "manuscript": digest(args.manuscript),
                                 "result": digest(args.result), "checker": digest(Path(__file__))}
        write_json(args.output, check)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Check input/output error: {error}\n")
    print(json.dumps({"check_passed": check["check_passed"],
                      "failed_checks": [name for name, item in check["checks"].items() if not item["passed"]]}))
    return 0 if check["check_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
