"""Load and verify provider-neutral model-run records."""

from __future__ import annotations

from datetime import datetime
import hashlib
import math
from pathlib import Path
import re

from .dna import _parse


SCHEMA_VERSION = "1.1"
SUPPORTED_SCHEMA_VERSIONS = ("1.0", SCHEMA_VERSION)
CONDITIONS = ("baseline", "skill", "profile")
ARTIFACT_NAMES = ("input", "context", "output")
REQUIRED_FIELDS = (
    "schema_version",
    "run_id",
    "task_id",
    "condition",
    "repetition",
    "created_at",
    "repository_revision",
    "model",
    "generation",
    "artifacts",
    "digests",
    "review",
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_run_record(path: str | Path) -> dict:
    return _parse(Path(path).read_text(encoding="utf-8"))


def _non_empty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _mapping_fields(
    value: object,
    field: str,
    required: set[str],
    errors: list[str],
    *,
    optional: set[str] | None = None,
) -> dict | None:
    if not isinstance(value, dict):
        errors.append(f"{field} must be a mapping")
        return None
    allowed = required | (optional or set())
    missing = required - set(value)
    unknown = set(value) - allowed
    if missing:
        errors.append(f"{field} missing fields: {', '.join(sorted(missing))}")
    if unknown:
        errors.append(f"{field} has unknown fields: {', '.join(sorted(unknown))}")
    return value


def validate_run_record(path: str | Path, *, root: str | Path) -> list[str]:
    """Validate metadata, artifact containment, and SHA-256 integrity."""
    record_path = Path(path)
    root_path = Path(root).resolve()
    try:
        record = load_run_record(record_path)
    except (OSError, ValueError) as error:
        return [f"Invalid run record: {error}"]

    errors: list[str] = []
    missing = set(REQUIRED_FIELDS) - set(record)
    unknown = set(record) - set(REQUIRED_FIELDS)
    if missing:
        errors.append("Missing run-record fields: " + ", ".join(sorted(missing)))
    if unknown:
        errors.append("Unknown run-record fields: " + ", ".join(sorted(unknown)))

    schema_version = record.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(
            "schema_version must be one of: " + ", ".join(SUPPORTED_SCHEMA_VERSIONS)
        )
    for field in ("run_id", "task_id", "created_at", "repository_revision"):
        if not _non_empty_text(record.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if _non_empty_text(record.get("created_at")):
        try:
            created_at = datetime.fromisoformat(record["created_at"].replace("Z", "+00:00"))
        except ValueError:
            errors.append("created_at must be an ISO-8601 timestamp")
        else:
            if "T" not in record["created_at"] or created_at.tzinfo is None:
                errors.append("created_at must include a date, time, and timezone")
    if record.get("condition") not in CONDITIONS:
        errors.append("condition must be one of: " + ", ".join(CONDITIONS))
    repetition = record.get("repetition")
    if isinstance(repetition, bool) or not isinstance(repetition, int) or repetition < 1:
        errors.append("repetition must be a positive integer")

    model = _mapping_fields(record.get("model"), "model", {"provider", "name", "version"}, errors)
    if model is not None:
        for field in ("provider", "name", "version"):
            if not _non_empty_text(model.get(field)):
                errors.append(f"model.{field} must be a non-empty string")

    generation_fields = {"temperature", "seed", "max_output_tokens", "tools"}
    optional_generation_fields = (
        {"reasoning_effort", "verbosity"} if schema_version == "1.1" else set()
    )
    generation = _mapping_fields(
        record.get("generation"),
        "generation",
        generation_fields,
        errors,
        optional=optional_generation_fields,
    )
    if generation is not None:
        temperature = generation.get("temperature")
        temperature_unavailable = schema_version == "1.1" and temperature is None
        if not temperature_unavailable and (
            isinstance(temperature, bool)
            or not isinstance(temperature, (int, float))
            or not math.isfinite(temperature)
            or temperature < 0
        ):
            errors.append("generation.temperature must be finite and non-negative")
        seed = generation.get("seed")
        if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
            errors.append("generation.seed must be an integer or null")
        limit = generation.get("max_output_tokens")
        limit_unavailable = schema_version == "1.1" and limit is None
        if not limit_unavailable and (
            isinstance(limit, bool) or not isinstance(limit, int) or limit < 1
        ):
            errors.append("generation.max_output_tokens must be a positive integer")
        tools = generation.get("tools")
        if not isinstance(tools, list) or any(not _non_empty_text(item) for item in tools):
            errors.append("generation.tools must be a list of non-empty strings")
        if schema_version == "1.1":
            for field in ("reasoning_effort", "verbosity"):
                value = generation.get(field)
                if value is not None and not _non_empty_text(value):
                    errors.append(f"generation.{field} must be a non-empty string or null")

    artifacts = _mapping_fields(record.get("artifacts"), "artifacts", set(ARTIFACT_NAMES), errors)
    digests = _mapping_fields(record.get("digests"), "digests", set(ARTIFACT_NAMES), errors)
    if artifacts is not None and digests is not None:
        for name in ARTIFACT_NAMES:
            relative = artifacts.get(name)
            expected = digests.get(name)
            if not _non_empty_text(relative):
                errors.append(f"artifacts.{name} must be a non-empty relative path")
                continue
            relative_path = Path(relative)
            artifact_path = (root_path / relative_path).resolve()
            if relative_path.is_absolute() or not artifact_path.is_relative_to(root_path):
                errors.append(f"artifacts.{name} must stay under the evaluation root")
                continue
            if not artifact_path.is_file():
                errors.append(f"Artifact not found: {relative}")
                continue
            if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
                errors.append(f"digests.{name} must be a lowercase SHA-256 value")
                continue
            if sha256_file(artifact_path) != expected:
                errors.append(f"Digest mismatch for {name}: {relative}")

    review = _mapping_fields(record.get("review"), "review", {"status"}, errors)
    if review is not None and review.get("status") not in {"unreviewed", "reviewed", "excluded"}:
        errors.append("review.status must be unreviewed, reviewed, or excluded")
    return errors
