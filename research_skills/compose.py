"""Compose a Skill document with a personal reasoning profile."""

from pathlib import Path

from .dna import format_profile_rules, load_profile


def compose_skill(skill_dir: str | Path, profile_path: str | Path) -> str:
    skill_path = Path(skill_dir) / "SKILL.md"
    if not skill_path.is_file():
        raise FileNotFoundError(skill_path)
    skill_text = skill_path.read_text(encoding="utf-8").strip()
    profile = load_profile(profile_path)
    return "\n\n".join((format_profile_rules(profile), "## Skill Contract", skill_text)) + "\n"
