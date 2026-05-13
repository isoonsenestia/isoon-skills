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

## Scripts

- `scripts/install.sh` — idempotent. Creates one symlink per skill in `~/.claude/skills/`. Backs up any pre-existing non-symlink content to `<name>.bak.<timestamp>` before linking.
- `scripts/uninstall.sh` — removes only symlinks pointing into this repo. Leaves backups and foreign symlinks alone.
- `scripts/doctor.sh` — reports broken symlinks and any directory under `~/.claude/skills/` that isn't a symlink (potential unsaved work).

All three accept `SKILLS_SRC` and `SKILLS_DEST` env vars for testing.

## Authoring a new skill

Run `save-skill` inside Claude Code (say "save this as a skill" or "make this a skill"). It reads `skills/_meta/BEST_PRACTICES.md`, drafts from `skills/_meta/TEMPLATE.md`, writes the new skill, and updates `skills/_meta/INDEX.md`.

## License

MIT. See `LICENSE`.
