"""Check evidence-card structure and optional source consistency, not semantic truth."""
from __future__ import annotations
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_skills.dna import _parse, _strings

def _rubric(text):
    rubric = _parse(text)
    if set(rubric) - {"required_headings", "required_markers", "claim_headings"}:
        raise ValueError("Unknown rubric fields")
    _strings(rubric.get("required_headings"), "required_headings")
    if any(not heading.startswith("## ") for heading in rubric["required_headings"]):
        raise ValueError("Required headings must start with ## ")
    if "required_markers" in rubric:
        _strings(rubric["required_markers"], "required_markers")
    if "claim_headings" in rubric:
        _strings(rubric["claim_headings"], "claim_headings")
        if any(heading not in rubric["required_headings"] for heading in rubric["claim_headings"]):
            raise ValueError("Claim headings must also be required headings")
    return rubric

def read_rubric_values(rubric_text: str) -> list[str]:
    rubric = _rubric(rubric_text)
    return rubric["required_headings"] + rubric.get("required_markers", [])

def evaluate(card_text: str, rubric_text: str, *, source_text: str | None = None) -> list[str]:
    rubric = _rubric(rubric_text)
    # Ignore fenced examples; a quoted sample is not an actual evidence card.
    text = re.sub(r"(?ms)^\s*```[^\n]*\n.*?^\s*```[^\n]*$", "", card_text)
    matches = list(re.finditer(r"(?m)^## ([^\n]+)$", text))
    sections = {}
    errors = []
    for index, match in enumerate(matches):
        heading = "## " + match[1].strip()
        if heading in sections:
            errors.append(f"Duplicate section: {heading}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[heading] = text[match.end():end].strip()
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
    claim_bodies = []
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

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("card", type=Path)
    parser.add_argument("rubric", type=Path)
    parser.add_argument("--source", type=Path, help="Source Markdown; citation labels must match its headings")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable check report")
    args = parser.parse_args()
    try:
        errors = evaluate(args.card.read_text(encoding="utf-8"),
                          args.rubric.read_text(encoding="utf-8"),
                          source_text=args.source.read_text(encoding="utf-8") if args.source else None)
    except (OSError, ValueError) as error:
        print(f"Invalid evaluation input: {error}", file=sys.stderr)
        return 2
    report = {"check_passed": not errors, "source_checked": args.source is not None,
              "semantic_quality": "not_evaluated", "errors": errors}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif errors:
        print("\n".join(errors), file=sys.stderr)
    else:
        print("Evaluation passed (structural/source checks only; semantic quality not evaluated)")
    return int(bool(errors))

if __name__ == "__main__":
    raise SystemExit(main())
