---
name: pr-agent-loop
description: Use when a PR is backed by Codium PR-agent (github-actions[bot] running pr_agent.yaml) and you need to trigger, wait for, fetch, or validate the bot's auto-review. Triggers on phrases like "check the bot review", "wait for the PR agent", "trigger a re-review", "read the github-actions comments on the PR", or right after pushing follow-up commits to a branch that has a Codium PR-agent workflow.
---

# PR-Agent Loop

## Overview

Codium PR-agent (the `github-actions[bot]`) posts a persistent **PR Reviewer Guide** comment plus a **PR Code Suggestions** comment on PR open. Subsequent pushes do NOT auto-retrigger it — you re-trigger with `/review` / `/improve` PR comments. The bot edits the persistent review in place but sometimes replaces the suggestions comment by deleting + posting a new one. After fetching findings, pipe each through the `review` skill's Validation Pass before accepting or declining.

## When to Use

- A PR you control is backed by Codium PR-agent (`pr_agent.yaml` workflow exists).
- You pushed follow-up commits and need a fresh bot review (auto-trigger only fires on PR open).
- The bot's first run posted placeholder comments ("Preparing review…", "Work in progress…") that you need to wait for.
- You're auditing the bot's findings before accepting / declining.

**When NOT to use:**
- The repo doesn't have `pr_agent.yaml` — the bot won't run, this skill does nothing.
- You're reviewing the diff yourself — use the `review` skill directly.
- You need a one-off Q&A — use `/ask <question>` as a PR comment manually; this skill is for the persistent review/improve cycle.

## The Pattern

### Step 1 — Trigger (only if follow-up commits were pushed)

```
gh pr comment <PR-NUMBER> --body "/review"
gh pr comment <PR-NUMBER> --body "/improve"
```

Record the trigger timestamp in UTC (`date -u +%H:%M:%S`) — you'll filter comments by it.

Other supported commands (use only when relevant):
- `/describe` — regenerates the PR description.
- `/ask <q>` — one-off Q&A; replies inline.

### Step 2 — Wait for content (poll, don't sleep)

The bot first posts placeholders ("Preparing review...", "Work in progress..."), then either edits them in place or deletes-and-replaces. Poll for the real headers rather than the placeholder ids:

```bash
until \
  gh api repos/<owner>/<repo>/issues/<PR>/comments \
    --paginate -q '.[] | select(.user.login=="github-actions[bot]" and (.created_at > "<TRIGGER-UTC>")) | .body' \
  | grep -qE "PR Reviewer Guide|No relevant tests"; do
  sleep 15
done
```

Run polling in the background (`run_in_background: true`) — the system notifies you when the loop exits. Don't chain short `sleep`s in the foreground; that's blocked.

### Step 3 — Fetch and read

```bash
gh api repos/<owner>/<repo>/issues/<PR>/comments --paginate \
  -q '.[] | select(.user.login=="github-actions[bot]" and (.created_at > "<TRIGGER-UTC>"))
       | "===\n\(.created_at) | id=\(.id)\n---\n\(.body)\n"' \
  > /tmp/pr-bot.txt
```

The two top-level comments to read:
- **PR Reviewer Guide** — focus areas, prose findings, severity context.
- **PR Code Suggestions** — concrete diff suggestions with importance ratings.

If a comment 404s when fetched by id, the bot deleted the placeholder and posted a new comment — re-list since the trigger timestamp instead of fetching by id.

### Step 4 — Validate each finding

For every Bug/Medium-impact suggestion, pipe through the `review` skill's Validation Pass:

1. Re-read the cited file at the cited lines.
2. Trace the failure scenario step by step.
3. Look for guards (type narrowing, early returns, framework guarantees) that already prevent it.
4. Tag: **CONFIRMED REAL** / **LATENT** / **THEORETICAL**.
5. Decline THEORETICAL findings with one-line reasoning; apply CONFIRMED REAL as follow-up commits; note LATENT for the human reviewer.

Skip validation for Low / importance ≤ 4 suggestions — they're style nits.

### Step 5 — Report back

Present a table:

| Finding | Source | Validation | Action |
|---|---|---|---|
| <one-line title> | Reviewer Guide / Code Suggestion (importance N) | CONFIRMED REAL / LATENT / THEORETICAL | Apply / Note / Decline |

## Quick Reference

| Need | How |
|---|---|
| Trigger fresh review | `gh pr comment <PR> --body "/review"` |
| Trigger code suggestions | `gh pr comment <PR> --body "/improve"` |
| Bot user filter | `select(.user.login=="github-actions[bot]")` |
| Filter to post-trigger | `.created_at > "<UTC-ISO>"` |
| Wait for completion | Background poll on body containing `"PR Reviewer Guide"` |
| Workflow runs check | `gh api repos/<owner>/<repo>/actions/runs --paginate -q '.workflow_runs[] \| select(.head_branch=="<branch>")'` |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Assuming a new push auto-retriggers the bot | `pr_agent.yaml` typically fires on PR open only — re-trigger with `/review` and `/improve` |
| Polling by comment count | Bot edits in place AND sometimes deletes+replaces; count is unreliable. Poll by body content (header strings) |
| Fetching a placeholder comment by id and getting 404 | The bot deleted that placeholder. Re-list comments since the trigger time |
| Foreground `sleep 165 && fetch` | Long foreground sleeps are blocked. Use `run_in_background: true` and let the harness notify |
| Treating bot suggestions as bugs | Run each through the Validation Pass. THEORETICAL findings should be declined, not applied |
| Forgetting the `[bot]` suffix on user.login | The login is literally `github-actions[bot]` — include the brackets |

## Related

- **REQUIRED BACKGROUND:** `review` — the Validation Pass section is the gate for Step 4.
- **RELATED:** `logic-first-review` — the structured format applies to bot suggestions too.
