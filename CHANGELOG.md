# Changelog

All notable project changes are documented here.

## Unreleased

- Organize the CLI into `compose`, `list`, `validate`, `evaluate`, and `blind`
  commands while preserving the original compose invocation.
- Generalize deterministic evaluation across all public Skills and version JSON reports.
- Add a versioned provider-neutral run-record schema with path containment,
  timezone, metadata, and SHA-256 integrity checks.
- Add deterministic blind-review export that keeps the random seed and
  condition mapping out of the reviewer manifest.
- Add the installed `research-skills` command with stdin and UTF-8 file output.
- Discover and validate every public Profile and Skill contract instead of
  hard-coding the current Skill names.
- Remove a stale, incompatible example Profile and align the documented Skill
  layout with the repository's actual evaluation artifacts.
- Add evaluation criteria and pressure scenarios for `research-question`.
- Replace the custom YAML parser with safe parsing, duplicate-key rejection,
  and typed profile/contract validation.
- Include workflows and the complete contract in composed contexts.
- Add baseline, Skill-only and profile comparison modes.
- Reject empty rubrics and incomplete evidence cards; add optional source-label
  and numeric consistency checks with machine-readable reports.
- Document a blinded human-review protocol; no model quality gains are claimed.
- Add the `argument-analysis` Skill after a paper-reading prompt overfit an argumentative essay.
- Publish a limited three-condition pilot and its negative result: the profile did not outperform Skill-only in the first run.
- Add a source-verified U-Mamba paper-reading case without redistributing the PDF.
- Add an explicit conflicts-and-anomalies contract section and source checks for configurable claim sections.

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
