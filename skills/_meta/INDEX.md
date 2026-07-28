# Personal Skills Index

Registry of skills under `~/.claude/skills/`. Keep entries to one line. Update whenever a skill is added, renamed, or removed.

## Skills

- **adhd** — Parallel divergent ideation (third-party, [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd)): spawn 5 isolated Agent branches under distorted cognitive frames, then score, cluster, prune traps, and deepen the top 3; for open-ended design, naming, API surface, and fuzzy debugging.
- **analyzing-phone-data-quality** — Audit raw phone-number CSVs: detect separators, validate against a national standard, output a cleansing plan.
- **building-concept-explainer-html** — Build a single-file interactive HTML page that teaches a concept; eight beats, seven UI primitives, single-file vanilla-JS baseline.
- **checking-ready-to-develop** — Gate a backlog item against Senestia's Definition of Ready (6 required + 2 optional criteria, owners, deprecated security review) before it enters a sprint.
- **continuous-learning** — Extract a non-trivial solution (debugging technique, workaround, project quirk, resteer pattern) into a reusable skill at session end so future sessions don't repeat the work.
- **design-doc-self-review** — Before handing a design/spec/TDD doc to a reviewer, self-check six defect classes (overclaim, internal contradiction, stale framing, rationale gap, name-hides-intent, claim-scope); surface requirement questions instead of auto-fixing them.
- **design-feedback-as-oracle** — When a literal design fix is rejected, render side-by-side candidate variants and let the user pick; decouple cheap visual iteration from the expensive commit/rebase step.
- **dispatch** — Turn a one-line goal into a dev-squad plan.md (strict format, repos.json keys), preflight the target repos, hard-stop for approval, then run the tmux dispatch pipeline.
- **fe-next** — Frontend agent for Senestia Next.js apps; triggers on component/page/hook/style work.
- **grill-me** — Interview the user one question at a time with a recommended answer each round; capture each resolution into a sibling `<doc> - Grilled #N.md` (live decisions ledger + end-of-session folded sections).
- **logic-first-review** — Sub-skill enforcing the *Current logic → Why it breaks → What should happen → Suggested change* review format.
- **memory-review** — Walk the auto-memory directory file-by-file with the user; keep / update / delete each entry and reconcile MEMORY.md.
- **pr-agent-loop** — Trigger, wait for, fetch, and validate the Codium PR-agent (github-actions[bot]) auto-review on a PR.
- **repo-wiki** — Generate and maintain a graph-linked living wiki for a repo across the microservice ecosystem.
- **restack-after-amend** — After amending a base commit in a stacked-branch chain, rebase dependents with `git rebase --onto <new-base> <old-boundary>` to drop the superseded commit (plain rebase for additive changes).
- **review** — PR code review using `gh` to fetch the diff and producing a logic-first structured review.
- **save-skill** — Capture a new technique as a properly-formatted SKILL.md and register it here.
- **self-review-before-complete** — Apply logic-first review to your own diff before claiming a task is done.
- **senestia-bug-intake** — Triage a customer-reported bug in Senestia's Atlassian: file the engineering counterpart on the PECS board with sprint/label/link, post a Thai short summary back on the source.
- **technical-design-doc** — Draft a technical design doc from house templates: FULL (~3-4 pages, alternatives argued) or LITE (one-page RFC); not for PRDs, charters, or story cards.
- **tidy-memory** — On-demand audit + tier-by-tier prune of journal, transcripts, and skill drafts (defers auto-memory to memory-review).
- **ui-image-intake** — Turn a pasted UI image into a semantic build spec: snap visuals to the repo design system, interview only states/behavior/data, hand the spec to fe-next and verify headless.
- **verify-ui-against-design-headless** — Pixel-verify a UI component with no DOM test runner: throwaway preview route + headless-Chrome screenshot + `getBoundingClientRect()` readout; a green build is not a pixel match.
- **writing-tests** — Pick the smallest test tier (unit/integration/e2e) that exercises a dev-squad TDD task and write assertions that fail for the right reason; per-stack idioms for go and nextjs.

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
