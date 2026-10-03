# Changelog

Notable changes to the research Skills and supporting framework.

## [Unreleased]

### Fixed

- Composed output files now use LF newlines on Windows as required by run-record
  integrity validation.
- Structural evaluation excludes backtick and tilde fenced examples, including
  longer and unclosed fences, without hiding real sections after a closed block.
- Repository validation parses Skill YAML frontmatter and rejects missing,
  malformed or mismatched names/descriptions instead of matching body text.
- Blind-review export rejects records outside the evaluation root before
  creating files, preventing a partial packet on that validation failure.

### Development

- The CI configuration now covers Windows and Ubuntu on Python 3.10 and 3.12,
  with an explicit UTF-8 environment.

## [0.2.0] - 2026-09-27

This version gathers the current research Skills and supporting framework.
The package version was already `0.2.0` before a GitHub Release was created.

### Included

- Three standalone Skills: `paper-reading`, `research-question`, and
  `argument-analysis`, with contracts, examples, and pressure scenarios.
- Optional Reasoning DNA profile, validated YAML loading, and a context
  composer with baseline, Skill-only, and profile modes.
- `research-skills` CLI for composition, listing, validation, deterministic
  evaluation, and blind-review export; legacy script entry points remain.
- Versioned run records with SHA-256 integrity checks, deterministic rubrics,
  repository tests, and GitHub Actions validation.
- Source-verified U-Mamba case and a published nine-run comparison with raw
  contexts, outputs, records, and scores.
- Installation guidance for Codex and Claude Code, a copyable PowerShell/Bash
  command, and a short evidence-grounded demonstration in both READMEs.

### Known limitations

- Installing the Skills does not automatically apply the Reasoning DNA
  profile. The composer generates context; it does not call a model or learn
  from feedback automatically.
- The nine-run U-Mamba pilot used one model alias, one case, and one semantic
  reviewer. Skill-only scored higher than baseline in this setup, but the
  profile showed no incremental gain. Independent review remains pending.
- Deterministic checks reject some semantically useful outputs and are not a
  measure of factual or research quality. PDF extraction and provider adapters
  are not included.

## [0.1.0] - 2026-07-19

- Initial public repository structure and methodology baseline.
- MIT license, contribution policy, security policy, and community files.
