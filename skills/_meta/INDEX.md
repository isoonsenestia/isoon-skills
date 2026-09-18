# Personal Skills Index

Registry of skills under `~/.claude/skills/`. Keep entries to one line. Update whenever a skill is added, renamed, or removed.

## Skills

Model-invoked (the agent may reach for these on its own):

- **logic-first-review** - Sub-skill enforcing the *Current logic, Why it breaks, What should happen, Suggested change* review format.
- **memory-review** - Walk the auto-memory directory file-by-file with the user; keep / update / delete each entry and reconcile MEMORY.md.
- **pr-review** - Review a GitHub PR by number: fetch the diff with `gh`, trace the blast radius, publish a logic-first review with a validated severity table.
- **verify-ui-against-design-headless** - Pixel-verify a UI component with no DOM test runner: throwaway preview route + headless-Chrome screenshot + `getBoundingClientRect()` readout. Reached as the verification step of `ui-image-intake`, not on its own.

User-invoked only (`disable-model-invocation: true`; type the slash command):

- **checking-ready-to-develop** - Gate a backlog item against Senestia's Definition of Ready (6 required + 2 optional criteria, owners, deprecated security review) before it enters a sprint.
- **component-from-figma** - Build one his-design-system component from a Jira ticket plus labelled Figma nodes; worktree + subagent flow over the repo's figma-conformance skill.
- **resplitting-commits** - Rebuild a tangled or junk-named branch as atomic commits: anchor the base, build forward one concern at a time, gate every commit.
- **restack-after-amend** - After amending a base commit in a stacked-branch chain, rebase dependents with `git rebase --onto <new-base> <old-boundary>` to drop the superseded commit (plain rebase for additive changes).
- **senestia-bug-intake** - Triage a customer-reported bug in Senestia's Atlassian: file the engineering counterpart on the PECS board with sprint/label/link, post a Thai short summary back on the source.
- **tidy-memory** - On-demand audit + tier-by-tier prune of journal, transcripts, and skill drafts (defers auto-memory to memory-review).
- **ui-image-intake** - Turn a pasted UI image into a semantic build spec: snap visuals to the repo design system, interview only states/behavior/data, hand the spec off and verify headless.

## Meta

- **_meta/BEST_PRACTICES.md** — skill-authoring rules (frontmatter, naming, CSO, token budget).
- **_meta/TEMPLATE.md** — copy-paste SKILL.md skeleton.
- **_meta/INDEX.md** — this file.

## Conventions

- Skills live directly under `~/.claude/skills/` (flat namespace).
- Names are verb-first, kebab-case, ASCII letters/digits/hyphens only.
- Descriptions follow `Use when ...` and never summarize the workflow.
- A skill only a human should start carries `disable-model-invocation: true`; nothing else can call it.
- Heavy reference (>100 lines) goes under `<skill>/references/`, not inline.
- The full ruleset is `_meta/BEST_PRACTICES.md`.
