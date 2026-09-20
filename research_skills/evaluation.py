"""Deterministic structure and source checks for research-skill outputs.

These checks are rejection filters. They do not judge semantic correctness.
"""

from __future__ import annotations

import re

from .dna import _parse


RUBRIC_FIELDS = {"required_headings", "required_markers", "claim_headings"}


def _string_list(value: object, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        qualifier = "a list" if allow_empty else "a non-empty list"
        raise ValueError(f"{field} must be {qualifier}")
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field} entries must be non-empty strings")
    return value


def load_rubric(text: str) -> dict:
    """Parse and validate an automated structural-check rubric."""
    rubric = _parse(text)
    unknown = set(rubric) - RUBRIC_FIELDS
    if unknown:
        raise ValueError("Unknown rubric fields: " + ", ".join(sorted(unknown)))

    headings = _string_list(rubric.get("required_headings"), "required_headings")
    if any(not heading.startswith("## ") for heading in headings):
        raise ValueError("Required headings must start with ## ")

    if "required_markers" in rubric:
        _string_list(rubric["required_markers"], "required_markers", allow_empty=True)
    if "claim_headings" in rubric:
        claim_headings = _string_list(
            rubric["claim_headings"], "claim_headings", allow_empty=True
        )
        if any(heading not in headings for heading in claim_headings):
            raise ValueError("Claim headings must also be required headings")
    return rubric


def read_rubric_values(rubric_text: str) -> list[str]:
    """Return required strings for compatibility with the original evaluator."""
    rubric = load_rubric(rubric_text)
    return rubric["required_headings"] + rubric.get("required_markers", [])


def evaluate(
    candidate_text: str,
    rubric_text: str,
    *,
    source_text: str | None = None,
) -> list[str]:
    """Return deterministic rubric failures for one Markdown candidate."""
    rubric = load_rubric(rubric_text)
    # A fenced example is not an actual output section.
    text = re.sub(r"(?ms)^\s*```[^\n]*\n.*?^\s*```[^\n]*$", "", candidate_text)
    matches = list(re.finditer(r"(?m)^## ([^\n]+)$", text))
    sections: dict[str, str] = {}
    errors: list[str] = []
    for index, match in enumerate(matches):
        heading = "## " + match[1].strip()
        if heading in sections:
            errors.append(f"Duplicate section: {heading}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[match.end() : end].strip()

    for heading in rubric["required_headings"]:
        body = sections.get(heading, "")
        cleaned = re.sub(r"\[Source:[^\]\n]*(?:\]|$)", "", body, flags=re.I)
        cleaned = re.sub(r"\b(?:Conflict|Inference|Unsupported):", "", cleaned, flags=re.I)
        if not re.search(r"\w", cleaned):
            errors.append(f"Missing or empty section: {heading}")

    for marker in rubric.get("required_markers", []):
        if marker.casefold() not in text.casefold():
            errors.append(f"Missing marker: {marker}")

    claim_headings = rubric.get("claim_headings", ["## Evidence"])
    claim_bodies: list[str] = []
    for heading in claim_headings:
        body = sections.get(heading, "")
        claim_bodies.append(body)
        for line in body.splitlines():
            if not line.strip():
                continue
            if not re.search(r"\[Source:\s*[^\]\s][^\]]*\]", line, re.I):
                errors.append(f"Claim in {heading} lacks a complete source citation")

    if source_text is not None:
        if not source_text.strip():
            raise ValueError("Source must not be empty")
        titles = set(re.findall(r"(?m)^#{1,6}\s+(.+?)\s*$", source_text))
        claims = "\n".join(claim_bodies)
        for citation in re.findall(r"\[Source:\s*([^\]]+)\]", claims, re.I):
            if citation.strip() not in titles:
                errors.append(f"Unknown source location: {citation}")
        number_pattern = r"(?<![\w.])[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"
        source_numbers = set(re.findall(number_pattern, source_text))
        uncited_claims = re.sub(r"\[Source:[^\]]+\]", "", claims, flags=re.I)
        for number in sorted(set(re.findall(number_pattern, uncited_claims)) - source_numbers):
            errors.append(f"Number absent from source: {number}")
    return errors


def report_for(errors: list[str], *, source_checked: bool) -> dict:
    """Create a stable machine-readable report."""
    return {
        "schema_version": "1.0",
        "check_passed": not errors,
        "source_checked": source_checked,
        "semantic_quality": "not_evaluated",
        "errors": errors,
    }
