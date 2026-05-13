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
5. Draft the Issues section per the format below.
6. **Validate every Bug/Medium issue before publishing** (see Validation Pass).
7. Adjust severity or remove invalidated issues, then publish the structured review.

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

## Validation Pass

Before publishing, validate every **Bug** and **Medium** issue. Skip Low (style nits don't earn the cost).

For each Bug/Medium claim:

1. **Re-read the cited file at the cited lines.** Open it fresh — don't trust your earlier reading. If the line numbers shifted in your head, the rest of the analysis is suspect.
2. **Trace the failure scenario step by step.** Write the sequence: input → code path → observable failure. Each step must point at a line that does what you claimed. If you can't write the trace, you don't understand the failure yet.
3. **Look for guards that already prevent it.** Type narrowing, early returns, framework guarantees, surrounding checks. If a guard exists, the issue is invalid — remove it.
4. **Confirm the trigger.** Can this fire with realistic data and timing? Or only with contrived inputs?
5. **Tag each validated issue:**
   - **CONFIRMED REAL** — failure path exists end-to-end, manifests under normal use
   - **LATENT** — failure path exists but requires unusual timing or data; note this in the issue text so the author can judge urgency
   - **THEORETICAL** — only fires under contrived conditions; demote to Low or delete entirely
6. **Edit the review.** Demote, delete, or annotate before publishing.

Why this step exists: rigorous-sounding feedback that falls apart on re-reading wastes the author's time and burns trust. Catching it in your head is cheaper than catching it after the author has spent an hour planning the fix. A Medium issue you can't trace is a Low issue at best.

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
- Do not publish a Bug/Medium issue you didn't run through the Validation Pass.
