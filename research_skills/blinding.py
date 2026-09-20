"""Prepare deterministic, condition-hidden output bundles for human review."""

from __future__ import annotations

import json
from pathlib import Path
import random
import shutil

from .run_records import load_run_record, validate_run_record


def prepare_blind_review(
    record_paths: list[str | Path],
    output_dir: str | Path,
    *,
    root: str | Path,
    seed: int,
) -> dict:
    """Validate records, randomize outputs, and separate the private key."""
    if len(record_paths) < 2:
        raise ValueError("Blind review requires at least two run records")

    root_path = Path(root).resolve()
    runs: list[tuple[Path, dict]] = []
    run_ids: set[str] = set()
    for path in record_paths:
        record_path = Path(path)
        errors = validate_run_record(record_path, root=root_path)
        if errors:
            raise ValueError(f"Invalid run record {record_path}: " + "; ".join(errors))
        record = load_run_record(record_path)
        if record["run_id"] in run_ids:
            raise ValueError(f"Duplicate run_id: {record['run_id']}")
        run_ids.add(record["run_id"])
        runs.append((record_path, record))

    random.Random(seed).shuffle(runs)
    export = Path(output_dir)
    export.mkdir(parents=True, exist_ok=False)
    candidates_dir = export / "candidates"
    private_dir = export / "private"
    candidates_dir.mkdir()
    private_dir.mkdir()

    public_entries: list[dict] = []
    private_entries: list[dict] = []
    for index, (record_path, record) in enumerate(runs, start=1):
        blind_id = f"R{index:03d}"
        output_path = (root_path / record["artifacts"]["output"]).resolve()
        candidate_relative = f"candidates/{blind_id}.md"
        shutil.copyfile(output_path, export / candidate_relative)
        public_entries.append(
            {
                "blind_id": blind_id,
                "task_id": record["task_id"],
                "file": candidate_relative,
            }
        )
        private_entries.append(
            {
                "blind_id": blind_id,
                "run_id": record["run_id"],
                "task_id": record["task_id"],
                "condition": record["condition"],
                "repetition": record["repetition"],
                "record": record_path.resolve().relative_to(root_path).as_posix(),
            }
        )

    # The seed stays in the private key: publishing it with a known record order
    # would let a reviewer reconstruct the condition mapping.
    manifest = {"schema_version": "1.0", "candidates": public_entries}
    key = {"schema_version": "1.0", "seed": seed, "candidates": private_entries}
    (export / "review-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (private_dir / "review-key.json").write_text(
        json.dumps(key, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest
