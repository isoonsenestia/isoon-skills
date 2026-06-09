# Changelog

All notable changes to isoon-skills.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- `grill-me` now produces a durable per-session artifact: a sibling `<Source Title> - Grilled #N.md` next to the source markdown doc. The file has a live `## Decisions` ledger (appended per resolved question, row schema `# | Question | Recommended | User resolution | Affects §`) and a `## Folded sections` block (written once at session end, rewriting only the source §sections the grill touched). N increments from existing `Grilled #M` siblings; behavior is generic across any source doc.
- Source-doc discovery: skill scans recent conversation turns for `.md` paths, lists candidates for the user to pick, and asks if none are found — does not silently guess.

### Added
- `skills/grill-me/references/document-output.md` — full output template, decision-row schema rationale, N-detection regex, worked example, and edge-case handling for the new artifact behavior.

## [0.1.0] — 2026-05-13

### Added
- Initial release.
- 7 personal skills migrated from `~/.claude/skills/`: `save-skill`, `fe-next`, `repo-wiki`, `review`, `logic-first-review`, `self-review-before-complete`, `analyzing-phone-data-quality`.
- `_meta/` with `BEST_PRACTICES.md`, `TEMPLATE.md`, `INDEX.md`.
- `scripts/install.sh`, `scripts/uninstall.sh`, `scripts/doctor.sh` — idempotent symlink management.
- `.claude-plugin/plugin.json` — installable via `/plugin install`.
