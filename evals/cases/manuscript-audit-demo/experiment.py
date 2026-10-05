"""Deterministic synthetic 1-NN example; no model service or third-party library."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path


FEATURES = ("feature_1", "feature_2")


def read_data(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"sample_id", "patient_id", "label", *FEATURES}
        if set(reader.fieldnames or []) != required:
            raise ValueError("CSV must contain sample_id, patient_id, label, and both features")
        rows = []
        for row in reader:
            parsed = {"sample_id": row["sample_id"], "patient_id": row["patient_id"],
                      "label": int(row["label"]), **{name: float(row[name]) for name in FEATURES}}
            if not parsed["sample_id"] or not parsed["patient_id"] or parsed["label"] not in (0, 1):
                raise ValueError("Empty ID or non-binary label")
            if not all(math.isfinite(parsed[name]) for name in FEATURES):
                raise ValueError("Features must be finite")
            rows.append(parsed)
    if not rows or len({row["sample_id"] for row in rows}) != len(rows):
        raise ValueError("Dataset must be nonempty with unique sample IDs")
    return sorted(rows, key=lambda row: row["sample_id"])


def partition(rows: list[dict], config: dict) -> tuple[list[dict], list[dict]]:
    split = config["split"]
    unit = split["unit"]
    if unit not in ("sample", "patient"):
        raise ValueError("split.unit must be sample or patient")
    key = unit + "_id"
    selected = set(split["test_ids"])
    if not selected or not selected.issubset({row[key] for row in rows}):
        raise ValueError("Test IDs must identify existing samples or patients")
    train = [row for row in rows if row[key] not in selected]
    test = [row for row in rows if row[key] in selected]
    if not train or not test:
        raise ValueError("Both partitions must contain samples")
    return train, test


def fit_normalizer(train: list[dict]) -> dict:
    mean = {name: math.fsum(row[name] for row in train) / len(train) for name in FEATURES}
    scale = {name: math.sqrt(math.fsum((row[name] - mean[name]) ** 2 for row in train) / len(train))
             or 1.0 for name in FEATURES}
    return {"mean": mean, "scale": scale, "fit_sample_ids": [row["sample_id"] for row in train]}


def run_experiment(rows: list[dict], config: dict) -> dict:
    if config.get("model") != "1nn" or config.get("normalization") != "train_only":
        raise ValueError("This small example supports 1nn with train_only normalization")
    train, test = partition(rows, config)
    normalizer = fit_normalizer(train)
    scale = normalizer["scale"]
    predictions = []
    for row in test:
        nearest = min(train, key=lambda candidate: (
            math.fsum(((row[name] - candidate[name]) / scale[name]) ** 2 for name in FEATURES),
            candidate["sample_id"],
        ))
        predictions.append({"sample_id": row["sample_id"], "patient_id": row["patient_id"],
                            "truth": row["label"], "prediction": nearest["label"],
                            "nearest_train_sample_id": nearest["sample_id"]})
    correct = sum(row["prediction"] == row["truth"] for row in predictions)
    return {
        "synthetic": True, "model": "1nn",
        "train_sample_ids": [row["sample_id"] for row in train],
        "test_sample_ids": [row["sample_id"] for row in test],
        "train_patient_ids": sorted({row["patient_id"] for row in train}),
        "test_patient_ids": sorted({row["patient_id"] for row in test}),
        "normalizer": normalizer, "predictions": predictions,
        "metrics": {"n_train": len(train), "n_test": len(test), "correct": correct,
                    "accuracy": correct / len(test)},
        "limits": ["generated signals", "one fixed split", "one complete model", "no component ablation"],
    }


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: dict) -> None:
    # Reproduction writes a fresh artifact, never replaces a preserved run.
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = run_experiment(read_data(args.data), json.loads(args.config.read_text(encoding="utf-8")))
        result["input_digests"] = {"data": digest(args.data), "config": digest(args.config),
                                  "experiment": digest(Path(__file__))}
        write_json(args.output, result)
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Experiment input/output error: {error}\n")
    print(json.dumps(result["metrics"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
