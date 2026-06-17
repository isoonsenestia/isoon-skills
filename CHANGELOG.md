# Changelog

All notable changes to isoon-skills.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] — 2026-06-17

### Added
- Three skills extracted from an obesity-assessment frontend session:
  - `restack-after-amend` — re-stack dependent branches after rewriting a base commit in a stacked-PR chain; `git rebase --onto <new-base> <old-boundary>` to drop the superseded commit (plain rebase for additive changes).
  - `verify-ui-against-design-headless` — pixel-verify a component with no DOM test runner: throwaway preview route + headless-Chrome screenshot + `getBoundingClientRect()` readout; a green build is not a pixel match.
  - `design-feedback-as-oracle` — when a literal design fix is rejected, render side-by-side candidates and let the user pick; decouple visual iteration from the expensive commit/rebase step.
- `README.md`, `skills/_meta/INDEX.md`, and `.claude-plugin/plugin.json` updated to list the three new skills.

## [0.2.0] — 2026-06-11

### Added
- New skills since 0.1.0: `building-concept-explainer-html`, `checking-ready-to-develop`, `continuous-learning`, `grill-me`, `memory-review`, `pr-agent-loop`, `senestia-bug-intake`, `tidy-memory`, `writing-tests`.
- `scripts/sync-cowork.sh` — mirror repo skills into the newest Claude Desktop ("Cowork") session; `install.sh --all` runs it after the CLI sync.
- `skills/grill-me/references/document-output.md` — full output template, decision-row schema rationale, N-detection regex, worked example, and edge-case handling for the grilled-artifact behavior.
- `internal-memo/` (gitignored) as a scratch area.

### Changed
- `grill-me` now produces a durable per-session artifact: a sibling `<Source Title> - Grilled #N.md` next to the source markdown doc. The file has a live `## Decisions` ledger (appended per resolved question, row schema `# | Question | Recommended | User resolution | Affects §`) and a `## Folded sections` block (written once at session end, rewriting only the source §sections the grill touched). N increments from existing `Grilled #M` siblings; behavior is generic across any source doc.
- `grill-me` source-doc discovery: skill scans recent conversation turns for `.md` paths, lists candidates for the user to pick, and asks if none are found — does not silently guess.
- `save-skill` now writes the skill into this repo and symlinks via `install.sh`, instead of writing directly into `~/.claude/skills/`.
- `analyzing-phone-data-quality` aligned with the strict-validity report format.
- `review` gained a validation pass for Bug/Medium issues.
- `README.md`, `skills/_meta/INDEX.md`, and `.claude-plugin/plugin.json` refreshed to list the full current skill catalog.

## [0.1.0] — 2026-05-13

### Added
- Initial release.
- 7 personal skills migrated from `~/.claude/skills/`: `save-skill`, `fe-next`, `repo-wiki`, `review`, `logic-first-review`, `self-review-before-complete`, `analyzing-phone-data-quality`.
- `_meta/` with `BEST_PRACTICES.md`, `TEMPLATE.md`, `INDEX.md`.
- `scripts/install.sh`, `scripts/uninstall.sh`, `scripts/doctor.sh` — idempotent symlink management.
- `.claude-plugin/plugin.json` — installable via `/plugin install`.
