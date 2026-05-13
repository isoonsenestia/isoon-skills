---
name: review
description: Use when asked to review a pull request or code changes — fetches PR diff via gh CLI, then produces a structured review with logic-first explanations before each suggestion
---

# PR Code Review

## Workflow

1. If no PR number given, run `gh pr list` and ask which to review.
2. Run `gh pr view <number> --json title,body,files,additions,deletions,commits` to get context.
3. Run `gh pr diff <number>` to get the full diff.
4. For large diffs, read specific changed files to understand surrounding context.
5. Produce a structured review (see format below).

## Output Format

### Overview
2–3 sentences: what the PR does, what problem it solves, overall direction assessment.

### Issues
For **each issue**, follow this exact order:

**1. Current logic** — explain what the code does today (be specific: file, function, line behavior).

**2. Why it's a problem** — explain what goes wrong, under what conditions, with a concrete example if possible.

**3. What should happen instead** — describe the correct behavior or design in plain terms.

**4. Suggested change** — the concrete code or structural fix.

Use this structure even for minor issues. Never lead with a suggestion before establishing the current behavior and why it breaks.

### Summary Table

End with a severity table:

| Severity | Issue |
|----------|-------|
| Bug | ... |
| Medium | ... |
| Low | ... |

Severity levels: **Bug** (incorrect behavior, data loss, silent failures), **Medium** (duplication, missing abstraction, regression risk), **Low** (style, naming, consistency).

## Focus Areas

Evaluate in this order:
1. **Correctness** — logic bugs, edge cases, off-by-one, type/size mismatches
2. **Regressions** — behavior removed or narrowed versus the code it replaces
3. **Duplication** — identical blocks that will drift; extract helpers
4. **Architecture** — business logic leaking into wrong layer, shared utilities missing
5. **Tests** — coverage of edge cases, not just happy path
6. **Consistency** — naming, struct field types that diverge from adjacent code

## What NOT to do

- Do not suggest a fix before explaining what the current code does.
- Do not invent issues — only flag what is observable in the diff plus surrounding context.
- Do not restate what the PR description already says.
- Do not flag style nits as bugs.
