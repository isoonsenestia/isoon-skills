---
name: dispatch
description: Use when the user wants work dispatched to dev-squad agents — "/dispatch <goal>", "dispatch this to the squad", "send agents to build X", "run this through dev-squad", or a goal naming repos plus the word harness. Turns one goal into a plan.md and runs the tmux dispatch pipeline.
---

# Dispatch a goal to dev-squad

Turn a one-line goal into a valid `plan.md`, preflight it, get the user's approval, then run the dispatch pipeline. You orchestrate; dispatched agents do the coding. Full toolkit reference: `~/claude-things/dev-squad/CLAUDE.md`.

## Workflow

**1. Decompose.** Split the goal into per-repo tasks. Repo names MUST be keys in `~/claude-things/repos.json` (`jq -r '.repos | keys[]'`). Producer stages before consumer stages (API before the UI that calls it); same stage = parallel. Pick mode: **harness** (TDD, verified commits — default for well-specified changes in repos with runnable test suites) or **simple** (interactive panes — exploratory / hard-to-test work). User said "harness" → harness.

**2. Write the plan** to `~/claude-things/dev-squad/plans/<slug>/plan.md`:

```markdown
# <title>
**Mode:** harness

### Task 1: <full task description — this heading line is the agent's entire ticket: what, where, acceptance criteria>
**Repo:** <repos.json key>
**Stage:** 1
**Agent:** Backend
```

Heading rules: no backticks, quotes, or pipes (parser strips/breaks on them); write testable acceptance criteria — in harness mode this one line drives both the test author and the implementer. Validate: `~/claude-things/dev-squad/parse-plan.sh <plan.md>` must exit 0 and show every task.

**3. Preflight** (report results, fix nothing yet):

| Check | How |
|---|---|
| Repo resolves | task repo/stack/agent present in parse-plan output |
| Clean tree + branch | `git -C <repo> status --porcelain` empty; note current branch |
| Git identity (harness) | `git -C <repo> config user.email` non-empty |
| `.claude/` gitignored (harness) | else ROUTING clean-tree guard aborts after settings.json is written. Zero-footprint fix: `echo '.claude/' >> <repo>/.git/info/exclude` (appending to `.gitignore` dirties the tree it's meant to clean) |
| tmux session | `tmux has-session -t dev-squad` — else run `~/claude-things/dev-squad/setup-dev-squad.sh` |
| Panes idle (simple) | `tmux list-panes -t dev-squad:2 -F '#{pane_current_command}'` → shells, not claude; `/exit` leftovers |

**4. Approval gate — hard stop.** Show the user: the plan, preflight results (including any blockers and the exact fix commands), and the run commands. **Never commit, checkout, or edit anything in a target repo without the user's explicit yes — including "harmless" `.gitignore` fixes.** Wait for approval.

**5. Run.**

```zsh
~/claude-things/dev-squad/generate-dispatch.sh [--harness] <plan.md>   # --harness redundant if plan has Mode:
bash <plan-dir>/dispatch.sh
```

Stage-gate Enter prompts in that terminal belong to the user.

**6. Monitor and close.** Activity: Monitoring pane / `tail -f ~/.dev-squad/monitor.log` (`PASS`/`FAIL`/`ABORT` lines). Harness attempt logs: `~/.dev-squad/logs/<Agent>-<timestamp>/`. Results are local commits — pushing/PRs stay with the user (`git push` is denied to agents). Simple mode: `/exit` the pane sessions afterward so the next dispatch lands in idle shells.

## Common mistakes

- Backticks in a task heading → broken generated script.
- Repo name not a `repos.json` key → task silently skipped (simple) or error (harness).
- Dispatching into panes still running claude → keystrokes land inside the old session.
- Harness on a dirty tree or missing git identity → ABORT in ROUTING.
- "Fixing" preflight blockers in target repos before the user approved.
