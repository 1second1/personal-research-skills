# Release Checklist

Before creating a release:

1. Check that `pyproject.toml` version and the proposed Git tag match.
2. In a clean temporary project, list and install all three Skills for Codex
   and Claude Code using the command in each README; inspect the actual target
   files and run the documented example prompt. This is a maintainer smoke
   test, not independent user validation.
3. Run the full Python test suite, repository validation, and the bundled
   paper-reading and real-paper evaluations.
4. Check the README links, example commands, Skill contracts, and the U-Mamba
   claims against the archived source map, raw outputs, and score records.
5. Review the intended diff and tracked files for secrets, private research
   data, or unlicensed paper content; confirm license and contribution links.
6. Push the verified commit and confirm GitHub Actions passes for that SHA.
7. Publish release notes describing scope, the nine-run pilot's one-reviewer
   limit, the negative Reasoning DNA result, and known runtime limitations.
8. Confirm the public Release tag points to the verified commit and its links
   work. Only then describe the release as published.
