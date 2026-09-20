"""Repository-shape validation shared by the CLI and compatibility script."""

from __future__ import annotations

from pathlib import Path

from .dna import load_contract, load_profile
from .evaluation import load_rubric
from .run_records import validate_run_record


REQUIRED_PATHS = (
    ".gitattributes",
    "README.md",
    "profiles/reasoning-dna.yaml",
    "evals/rubrics/paper-reading.yaml",
    "evals/rubrics/research-question.yaml",
    "evals/rubrics/argument-analysis.yaml",
    "evals/schemas/run-record-v1.schema.json",
    "evals/schemas/run-record-v1.1.schema.json",
    "evals/fixtures/paper-reading-demo/source.md",
    "evals/fixtures/paper-reading-demo/evidence-card.md",
    "evals/fixtures/run-record-demo/input.md",
    "evals/fixtures/run-record-demo/context.md",
    "evals/fixtures/run-record-demo/output.md",
    "evals/fixtures/run-record-demo/run.yaml",
    "evals/cases/u-mamba-real-paper/README.md",
    "evals/cases/u-mamba-real-paper/case.yaml",
    "evals/cases/u-mamba-real-paper/source-map.md",
    "evals/cases/u-mamba-real-paper/expected-output.md",
    "evals/cases/u-mamba-real-paper/rubric.yaml",
    "evals/cases/2013-text3-pilot/README.md",
    "research_skills/cli.py",
    "research_skills/dna.py",
    "research_skills/compose.py",
    "research_skills/evaluation.py",
    "research_skills/run_records.py",
    "research_skills/blinding.py",
    "research_skills/repository.py",
    "scripts/run_skill.py",
    "scripts/evaluate_paper_reading.py",
    "scripts/evaluate_output.py",
    "scripts/prepare_blind_review.py",
)

SKILL_FRONTMATTER_KEYS = ("name:", "description:")
REQUIRED_DIRECTORIES = ("profiles", "skills")
SKILL_ARTIFACTS = (
    "SKILL.md",
    "contract.yaml",
    "examples/input.md",
    "examples/expected-output.md",
    "evals/pressure-scenarios.md",
)


def validate(root: Path) -> list[str]:
    """Return missing or malformed public repository artifacts."""
    errors: list[str] = []
    for relative_path in REQUIRED_PATHS:
        if not (root / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")
    for relative_path in REQUIRED_DIRECTORIES:
        if not (root / relative_path).is_dir():
            errors.append(f"Missing required directory: {relative_path}")

    profiles_root = root / "profiles"
    if profiles_root.is_dir():
        for profile_path in sorted(profiles_root.glob("*.yaml")):
            try:
                load_profile(profile_path)
            except (OSError, ValueError) as error:
                relative_path = profile_path.relative_to(root).as_posix()
                errors.append(f"Invalid profile {relative_path}: {error}")

    skills_root = root / "skills"
    if skills_root.is_dir():
        for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
            skill_relative = skill_dir.relative_to(root).as_posix()
            for artifact in SKILL_ARTIFACTS:
                if not (skill_dir / artifact).is_file():
                    errors.append(f"Missing Skill artifact: {skill_relative}/{artifact}")
            rubric_relative = f"evals/rubrics/{skill_dir.name}.yaml"
            if not (root / rubric_relative).is_file():
                errors.append(f"Missing Skill rubric: {rubric_relative}")
            skill_path = skill_dir / "SKILL.md"
            if skill_path.is_file():
                skill_text = skill_path.read_text(encoding="utf-8")
                for key in SKILL_FRONTMATTER_KEYS:
                    if key not in skill_text:
                        errors.append(f"Missing Skill frontmatter key in {skill_dir.name}: {key}")
            contract_path = skill_dir / "contract.yaml"
            if contract_path.is_file():
                try:
                    contract = load_contract(contract_path)
                except (OSError, ValueError) as error:
                    errors.append(f"Invalid Skill contract {skill_relative}/contract.yaml: {error}")
                else:
                    if contract["name"] != skill_dir.name:
                        errors.append(
                            f"Invalid Skill contract {skill_relative}/contract.yaml: "
                            "name must match the Skill directory"
                        )

    rubrics_root = root / "evals/rubrics"
    if rubrics_root.is_dir():
        for rubric_path in sorted(rubrics_root.glob("*.yaml")):
            try:
                load_rubric(rubric_path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as error:
                relative_path = rubric_path.relative_to(root).as_posix()
                errors.append(f"Invalid rubric {relative_path}: {error}")

    fixtures_root = root / "evals/fixtures"
    record_paths: list[Path] = []
    if fixtures_root.is_dir():
        record_paths.extend(fixtures_root.rglob("run.yaml"))

    cases_root = root / "evals/cases"
    if cases_root.is_dir():
        for runs_directory in cases_root.rglob("runs"):
            if runs_directory.is_dir():
                record_paths.extend(runs_directory.glob("*.yaml"))
        for path in cases_root.rglob("*"):
            if path.is_file() and path.suffix.casefold() == ".pdf":
                errors.append(f"Do not commit source PDF: {path.relative_to(root).as_posix()}")
    for record_path in sorted(record_paths):
        for error in validate_run_record(record_path, root=root):
            relative_path = record_path.relative_to(root).as_posix()
            errors.append(f"Invalid run record {relative_path}: {error}")
    return errors
