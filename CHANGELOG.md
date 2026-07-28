# Changelog

All notable project changes are documented here.

## [0.2.0] - 2026-07-28

### Added

- Versioned reference profile at `profiles/reasoning-dna.yaml`.
- Dependency-free profile loader and Skill composer.
- `paper-reading` and `research-question` Skills with contracts and examples.
- Deterministic CLI composition through `scripts/run_skill.py`.
- Repository validation, fixture evaluation, unit tests, and GitHub Actions.
- English public README with a Chinese companion README.

### Known limitations

- The CLI composes an agent context; it does not call a model.
- Evaluation currently validates contracts and fixtures rather than model quality.
- Provider-specific Codex and Claude Code adapters are not yet implemented.
- The profile parser intentionally supports the repository's constrained YAML subset.

## [0.1.0] - 2026-07-19

### Added

- Initial public repository structure and methodology baseline.
- MIT license, contribution policy, security policy, and community files.
