# Project instructions

This project composes research methodology profiles and Skill contracts into
portable Markdown contexts. It does not execute a model or learn automatically.

- Core: research_skills/dna.py and research_skills/compose.py.
- CLI: scripts/run_skill.py. Evaluation: scripts/evaluate_paper_reading.py.
- Install: python -m pip install -e .
- Verify: python -m unittest discover -s tests -v, then
  python scripts/validate_repository.py.
- Keep source facts, inferences, and unsupported claims distinct.
- A deterministic format check is not proof of factual or research quality.
- Keep handoff context in docs/AGENT-HANDOFF-PLAN.md; do not add weekly logs.
