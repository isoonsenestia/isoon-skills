# isoon-skills

Personal Claude Code skills.

## What's in here

| Skill | Use when |
|---|---|
| `save-skill` | Capturing a new technique as a SKILL.md |
| `fe-next` | Working in a Senestia Next.js codebase |
| `repo-wiki` | Documenting or navigating a repo / microservice ecosystem |
| `review` | Reviewing a pull request |
| `logic-first-review` | Sub-skill for the *Current logic → Why it breaks → What should happen → Suggested change* format |
| `self-review-before-complete` | Before claiming a task done — reviews your own diff |
| `analyzing-phone-data-quality` | Auditing raw phone-number CSVs (Thai context) |

See `skills/_meta/INDEX.md` for the canonical registry and `skills/_meta/BEST_PRACTICES.md` for the authoring rules.

## Install — as a Claude Code plugin (recommended for users)

```
/plugin install https://github.com/isoonsenestia/isoon-skills
```

Claude Code clones the repo into its plugin cache and auto-loads everything in `skills/`. Skill names will appear namespaced as `isoon-skills:save-skill`, etc.

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

- `scripts/install.sh` — idempotent. Creates one symlink per skill in `~/.claude/skills/`. Backs up any pre-existing non-symlink content to `<name>.bak.<timestamp>` before linking. Pass `--all` (or `--cowork`, or `COWORK=1`) to also run `sync-cowork.sh`.
- `scripts/sync-cowork.sh` — mac-only. Detects the newest Claude Desktop Cowork session and symlinks each repo skill into its `skills/` folder. No-ops gracefully when Cowork isn't installed.
- `scripts/uninstall.sh` — removes only symlinks pointing into this repo, from both the CLI destination and the newest Cowork session. Leaves backups and foreign symlinks alone.
- `scripts/doctor.sh` — reports broken symlinks and any directory under `~/.claude/skills/` that isn't a symlink (potential unsaved work). Also scans the newest Cowork session for broken repo-pointing symlinks.

`install.sh`, `sync-cowork.sh`, `uninstall.sh`, and `doctor.sh` all accept `SKILLS_SRC` and `SKILLS_DEST` env vars for testing.

## Authoring a new skill

Run `save-skill` inside Claude Code (say "save this as a skill" or "make this a skill"). It reads `skills/_meta/BEST_PRACTICES.md`, drafts from `skills/_meta/TEMPLATE.md`, writes the new skill, and updates `skills/_meta/INDEX.md`.

## License

MIT. See `LICENSE`.
