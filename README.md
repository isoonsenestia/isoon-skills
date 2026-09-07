# isoon-skills

Personal Claude Code skills.

## What's in here

| Skill | Use when |
|---|---|
| `continuous-learning` | Extracting a solved non-trivial problem into a reusable skill at session end |
| `fe-next` | Working in a Senestia Next.js codebase |
| `repo-wiki` | Documenting or navigating a repo / microservice ecosystem |
| `pr-review` | Reviewing a GitHub pull request by number |
| `design-doc-self-review` | Self-checking a design/spec/estimation doc before handing it to a reviewer |
| `technical-design-doc` | Drafting a technical design doc - FULL (~3-4 pages) or LITE one-page RFC |
| `dispatch` | Turning a one-line goal into a dev-squad plan.md and running the tmux dispatch pipeline |
| `logic-first-review` | Sub-skill for the *Current logic → Why it breaks → What should happen → Suggested change* format |
| `self-review-before-complete` | Before claiming a task done — reviews your own diff |
| `writing-tests` | Authoring a unit/integration/e2e test (esp. dev-squad TDD tasks) |
| `checking-ready-to-develop` | Gating a backlog item against the Definition of Ready before a sprint |
| `senestia-bug-intake` | Triaging a customer bug into an engineering ticket on the PECS board |
| `pr-agent-loop` | Driving the Codium PR-agent auto-review on a PR |
| `building-concept-explainer-html` | Building a single-file interactive HTML page that teaches a concept |
| `analyzing-phone-data-quality` | Auditing raw phone-number CSVs (Thai context) |
| `memory-review` | Walking the auto-memory directory entry-by-entry to keep / update / delete |
| `tidy-memory` | Auditing and pruning journal, transcripts, and skill drafts |
| `restack-after-amend` | Re-stacking dependent branches after amending a base commit in a stacked-PR chain (`rebase --onto`) |
| `resplitting-commits` | Rebuilding a tangled or junk-named branch as one atomic commit per concern |
| `component-from-figma` | Building one his-design-system component from a Jira ticket plus labelled Figma nodes |
| `ui-image-intake` | Building/matching UI from a pasted image — snap to the design system, interview semantics, emit a semantic spec + a `design.md` visual reference |
| `verify-ui-against-design-headless` | Pixel-verifying a UI component against a design via headless Chrome (no DOM test runner) |
| `design-feedback-as-oracle` | A literal design fix was rejected — disambiguate with side-by-side candidates, not another guess |

See `skills/_meta/INDEX.md` for the canonical registry and `skills/_meta/BEST_PRACTICES.md` for the authoring rules.

## Install — as a Claude Code plugin (recommended for users)

```
/plugin install https://github.com/isoonsenestia/isoon-skills
```

Claude Code clones the repo into its plugin cache and auto-loads everything in `skills/`. Skill names will appear namespaced as `isoon-skills:pr-review`, etc.

## Install — as a symlinked dev checkout (for the author / contributors)

```bash
git clone https://github.com/isoonsenestia/isoon-skills ~/claude-things/isoon-skills
cd ~/claude-things/isoon-skills
./scripts/install.sh
```

This symlinks each skill from `skills/<name>` into `~/.claude/skills/<name>`. Edits to a SKILL.md in the repo are visible to Claude Code immediately — no commit/push/update cycle needed.

### Three skill homes

A skill is "installed" when its `SKILL.md` lives in a directory that one of the Claude surfaces scans on launch. There are three on macOS:

| # | Surface | Path | Synced by |
|---|---|---|---|
| 1 | **Repo** (canonical source) | `~/claude-things/isoon-skills/skills/<name>/` | git |
| 2 | **Claude Code (CLI)** | `~/.claude/skills/<name>/` | `scripts/install.sh` |
| 3 | **Claude Cowork** (Desktop local-agent-mode) | `~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/<sessionId>/<accountId>/skills/<name>/` | `scripts/sync-cowork.sh` |

Sync everything in one command:

```bash
./scripts/install.sh --all     # CLI + Cowork
```

Or run them separately:

```bash
./scripts/install.sh           # CLI only
./scripts/sync-cowork.sh       # Cowork only
```

**Caveats for the Cowork sync:**

1. The Cowork `skills/` directory is a **server-synced runtime cache**. A future Claude Desktop update may wipe or restructure it — if `sync-cowork.sh` stops working after a desktop update, expect the path or format to have changed.
2. Cowork skills normally have a server-issued `skillId` recorded in `manifest.json`. We don't touch that manifest — we bet on the desktop app picking up directory-scanned `SKILL.md` files at session start. If a synced skill doesn't appear in Cowork's `/` menu after restarting the desktop, the bet failed; fall back to uploading via the Desktop UI.
3. Cowork rotates session UUIDs. The script always targets the **newest** session by mtime. Re-run after a long gap.
4. Names that already exist in Cowork (built-ins like `pdf`, `pptx`, plus any skill you uploaded via the UI) are **skipped, never overwritten**. To override a built-in name, first rename your repo skill.

## Scripts

- `scripts/install.sh` — idempotent. Creates one symlink per skill in `~/.claude/skills/`. Backs up any pre-existing non-symlink content to `<name>.bak.<timestamp>` before linking. Then **reaps** its own stale links, on the same rules as `sync-cowork.sh` below. Pass `--all` (or `--cowork`, or `COWORK=1`) to also run `sync-cowork.sh`.
- `scripts/sync-cowork.sh` — mac-only. Detects the newest Claude Desktop Cowork session and symlinks each repo skill into its `skills/` folder. Then **reaps** its own stale links: a symlink pointing into this repo whose skill no longer exists is removed, so deleting or renaming a skill doesn't leave a dangling link behind. Never touches Cowork built-ins, uploaded skills, or symlinks pointing outside the repo — including broken ones. Skips the reap entirely if the source tree turns up empty. Pass `REAP=0` to disable. No-ops gracefully when Cowork isn't installed.
- `scripts/uninstall.sh` — removes only symlinks pointing into this repo, from both the CLI destination and the newest Cowork session. Leaves backups and foreign symlinks alone.
- `scripts/doctor.sh` — reports broken symlinks and any directory under `~/.claude/skills/` that isn't a symlink (potential unsaved work). Also scans the newest Cowork session for broken repo-pointing symlinks.

`install.sh`, `sync-cowork.sh`, `uninstall.sh`, and `doctor.sh` all accept `SKILLS_SRC`, `SKILLS_DEST`, and `REPO_ROOT` env vars for testing. `install.sh` and `sync-cowork.sh` also accept `REAP=0` to skip the reap pass.

## Authoring a new skill

Use whichever skill-authoring skill is installed (`superpowers:writing-skills`) to draft it, or `continuous-learning` to extract one from a solved problem. Either way the repo's own rules apply: read `skills/_meta/BEST_PRACTICES.md`, start from `skills/_meta/TEMPLATE.md`, and add a one-line entry to `skills/_meta/INDEX.md` plus a row in the table above.

## License

MIT. See `LICENSE`.
