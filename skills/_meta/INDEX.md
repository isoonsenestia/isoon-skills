# Personal Skills Index

Registry of skills under `~/.claude/skills/`. Keep entries to one line. Update whenever a skill is added, renamed, or removed.

## Skills

- **analyzing-phone-data-quality** — Audit raw phone-number CSVs: detect separators, validate against a national standard, output a cleansing plan.
- **building-concept-explainer-html** — Build a single-file interactive HTML page that teaches a concept; eight beats, seven UI primitives, single-file vanilla-JS baseline.
- **checking-ready-to-develop** — Gate a backlog item against Senestia's Definition of Ready (6 required + 2 optional criteria, owners, deprecated security review) before it enters a sprint.
- **fe-next** — Frontend agent for Senestia Next.js apps; triggers on component/page/hook/style work.
- **grill-me** — Interview the user one question at a time with a recommended answer each round; capture each resolution into a sibling `<doc> - Grilled #N.md` (live decisions ledger + end-of-session folded sections).
- **logic-first-review** — Sub-skill enforcing the *Current logic → Why it breaks → What should happen → Suggested change* review format.
- **memory-review** — Walk the auto-memory directory file-by-file with the user; keep / update / delete each entry and reconcile MEMORY.md.
- **pr-agent-loop** — Trigger, wait for, fetch, and validate the Codium PR-agent (github-actions[bot]) auto-review on a PR.
- **repo-wiki** — Generate and maintain a graph-linked living wiki for a repo across the microservice ecosystem.
- **review** — PR code review using `gh` to fetch the diff and producing a logic-first structured review.
- **save-skill** — Capture a new technique as a properly-formatted SKILL.md and register it here.
- **self-review-before-complete** — Apply logic-first review to your own diff before claiming a task is done.
- **senestia-bug-intake** — Triage a customer-reported bug in Senestia's Atlassian: file the engineering counterpart on the PECS board with sprint/label/link, post a Thai short summary back on the source.
- **tidy-memory** — On-demand audit + tier-by-tier prune of journal, transcripts, and skill drafts (defers auto-memory to memory-review).

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
