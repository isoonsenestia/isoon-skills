# Personal Skills Index

Registry of skills under `~/.claude/skills/`. Keep entries to one line. Update whenever a skill is added, renamed, or removed.

## Skills

- **analyzing-phone-data-quality** — Audit raw phone-number CSVs: detect separators, validate against a national standard, output a cleansing plan.
- **fe-next** — Frontend agent for Senestia Next.js apps; triggers on component/page/hook/style work.
- **logic-first-review** — Sub-skill enforcing the *Current logic → Why it breaks → What should happen → Suggested change* review format.
- **repo-wiki** — Generate and maintain a graph-linked living wiki for a repo across the microservice ecosystem.
- **review** — PR code review using `gh` to fetch the diff and producing a logic-first structured review.
- **save-skill** — Capture a new technique as a properly-formatted SKILL.md and register it here.
- **self-review-before-complete** — Apply logic-first review to your own diff before claiming a task is done.

## Meta

- **_meta/BEST_PRACTICES.md** — skill-authoring rules (frontmatter, naming, CSO, token budget).
- **_meta/TEMPLATE.md** — copy-paste SKILL.md skeleton.
- **_meta/INDEX.md** — this file.

## Conventions

- Skills live directly under `~/.claude/skills/` (flat namespace).
- Names are verb-first, kebab-case, ASCII letters/digits/hyphens only.
- Descriptions follow `Use when ...` and never summarize the workflow.
- Heavy reference (>100 lines) goes under `<skill>/references/`, not inline.
- The full ruleset is `_meta/BEST_PRACTICES.md`.
