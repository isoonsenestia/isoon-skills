# RFC: {Title}

**Author:** {author} · **Status:** Proposed · **Date:** {date} · **Related:** {Jira key / links}

## Problem
{What's broken or missing, in 1-3 sentences with concrete evidence.}

## Proposal
{The change, in a short paragraph. What gets built/modified and where it runs.}

```
{Small ASCII diagram if it helps — otherwise delete this block}
```

**Key choices:** {the 2-4 decisions that matter, comma-separated: e.g. idempotency
key, sync vs async, reuse existing infra, fallback behavior.}

## Alternatives
| Option | Why not |
|---|---|
| {Alternative 1} | {Reason rejected / deferred} |
| {Alternative 2} | {Reason rejected / deferred} |

## Trade-offs / risks
{Bullet list. State each downside or risk honestly, with its mitigation. Cover
data/PII, reliability, and anything vendor- or scale-related that applies.}

## Rollout
{How it ships safely and how to roll back. Prefer flagged / gradual with a fallback.}

## Decision
- [ ] Approved  - [ ] Needs changes  - [ ] Rejected

Reviewers: {@reviewers}
