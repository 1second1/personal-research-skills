"""Compose a Skill document with a personal reasoning profile."""

from pathlib import Path

from .dna import format_profile_rules, load_contract, load_profile


def _format_metadata(
    skill_dir: Path,
    profile_path: Path,
    profile: dict,
    contract: dict,
) -> str:
    """Render deterministic metadata: versions, source paths, and contract summary."""
    contract_path = skill_dir / "contract.yaml"
    lines = [
        "## Composed Context Metadata",
        "",
        f"- Profile: {profile_path.name} version {profile['identity'].get('version', 'unknown')}",
        f"- Skill: {skill_dir.name}",
        f"- Contract: {contract_path.name} version {contract.get('version', 'unknown')}",
        f"- Contract purpose: {contract.get('purpose', 'not specified')}",
    ]
    return "\n".join(lines)


def compose_skill(
    skill_dir: str | Path,
    profile_path: str | Path,
    input_text: str | None = None,
) -> str:
    skill_path = Path(skill_dir) / "SKILL.md"
    if not skill_path.is_file():
        raise FileNotFoundError(skill_path)

    contract_path = Path(skill_dir) / "contract.yaml"
    if not contract_path.is_file():
        raise FileNotFoundError(contract_path)

    skill_text = skill_path.read_text(encoding="utf-8").strip()
    profile = load_profile(profile_path)
    contract = load_contract(contract_path)

    parts = [
        format_profile_rules(profile),
        _format_metadata(Path(skill_dir), Path(profile_path), profile, contract),
        "## Skill Contract",
        skill_text,
    ]

    if input_text is not None:
        parts.append("## Input Document")
        parts.append(input_text.strip())

    return "\n\n".join(parts) + "\n"
