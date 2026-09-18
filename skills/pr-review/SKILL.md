---
name: pr-review
description: Use when asked to review a pull request by number or URL, or to review "the PR" on GitHub — the diff still has to be fetched with `gh`. Not for reviewing a local branch or a range of commits against a base ref.
---

# PR Code Review

## Workflow

1. If no PR number given, run `gh pr list` and ask which to review.
2. Run `gh pr view <number> --json title,body,files,additions,deletions,commits` to get context.
3. Run `gh pr diff <number>` to get the full diff.
4. For large diffs, read specific changed files to understand surrounding context.
5. **Trace the blast radius** (see Blast-Radius Trace below).
6. Draft the Issues section per the format below.
7. **Validate every Bug/Medium issue before publishing** (see Validation Pass).
8. Adjust severity or remove invalidated issues, then publish the structured review.

## Blast-Radius Trace

A diff only shows what changed, not what depended on it. Before drafting issues, map the fallout of the change into the code it does **not** touch.

For every symbol the diff changes, renames, or removes — and any changed schema, DB column, config key, or data shape — find its dependents with `grep` / `gh` / `rg`:

- **Callers** of changed/renamed/removed functions — do they still pass valid args and handle the new return/behavior?
- **Importers** of a changed type, constant, or export — does the new signature or shape still fit?
- **Behavioral-contract shifts** — same signature, changed return value, thrown error, null-handling, or side-effect. The compiler will not catch these; only reading the caller will.
- **Readers/writers of shared state** — a changed schema, config key, or global has consumers beyond direct code callers; find them too.
- **Detail the caller must know** - while each dependent is open, ask what policy, ordering, or implementation detail it has to hold to get its domain outcome. That answer is the raw material for an Architecture finding (see Focus Areas #4).

Open each dependent and decide: real break, or fine. **Report a downstream break only when you have opened the site and can state the observable consequence** (e.g. "unknown id now returns 200 with guest data instead of 404 in `profileHandler`"). An untraced "this may affect callers" fails the Publishing Gate — either trace it to a concrete break or note the site as checked-and-fine. Do not flag a dependent where the changed path is unreachable (e.g. a caller that only passes ids known to exist).

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

For a **design finding** (Architecture, Focus Areas #4) the same four steps apply with two extra requirements:

- Step 2 names one complexity cost verbatim: `Change amplification`, `Cognitive load`, or `Unknown unknowns`.
- Step 4 gives a boundary, contract, or ownership direction, not a patch. Name which module should own the detail and what stays in one place afterwards. See [the design review framework](references/design-review-framework.md) for the comment pattern.

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

**This is the `logic-first-review` Publishing Gate applied at PR scope** — the three checks below (re-read → trace → guard → trigger) are that gate plus PR-specific tagging. Keep the two in sync when editing either.

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

**Design findings (Architecture) substitute evidence for the failure trace.** A complexity cost has no input-to-crash path, so steps 2 and 4 would delete it. Validate it instead by citing evidence for the named cost:

- `Change amplification` - cite at least two `file:line` sites that must change together for one policy change. One site is not amplification.
- `Cognitive load` - cite the detail the caller must hold and the `file:line` where it must hold it. If the API already hides it, the issue is invalid.
- `Unknown unknowns` - cite what a caller can miss and a real call site that misses it or gets it right only by accident. A hypothetical future caller is not evidence.

Steps 1 (re-read at the cited lines) and 3 (look for an existing guard, here: an abstraction that already owns the detail) still apply. At step 5, skip the tags: the named complexity cost is the tag. A design finding without this evidence is Low or deleted, same as an untraceable Bug.

Why this step exists: rigorous-sounding feedback that falls apart on re-reading wastes the author's time and burns trust. Catching it in your head is cheaper than catching it after the author has spent an hour planning the fix. A Medium issue you can't trace is a Low issue at best.

## Focus Areas

Evaluate in this order:
1. **Correctness** — logic bugs, edge cases, off-by-one, type/size mismatches
2. **Regressions** — behavior removed or narrowed versus the code it replaces
3. **Duplication** — identical blocks that will drift; extract helpers
4. **Architecture** - business logic leaking into wrong layer, shared utilities missing, and module boundaries that push complexity onto callers. Judge a boundary by its complexity cost: `Change amplification`, `Cognitive load`, or `Unknown unknowns`. Trace the domain outcome from the entry point the diff touches through the boundaries it crosses, and ask which module has the knowledge and control to own each detail the caller currently holds. Read [the design review framework](references/design-review-framework.md) before writing a design finding. Severity: a material cost the author should fix is **Medium**; an optional improvement is **Low**. Prefer a few high-signal findings over a boundary audit.
5. **Tests** — coverage of edge cases, not just happy path
6. **Consistency** — naming, struct field types that diverge from adjacent code

## What NOT to do

- Do not suggest a fix before explaining what the current code does.
- Do not invent issues — only flag what is observable in the diff plus surrounding context.
- Do not restate what the PR description already says.
- Do not flag style nits as bugs.
- Do not report formatting or naming preferences as design findings.
- Do not prescribe an implementation when the boundary is the real issue.
- Do not publish a Bug/Medium issue you didn't run through the Validation Pass.

## Pointers

- **REQUIRED BACKGROUND:** `logic-first-review` — this skill's Issues format and Validation Pass are that gate at PR scope.
- **REFERENCE:** [`references/design-review-framework.md`](references/design-review-framework.md) - complexity costs, boundary questions, and design checks behind Focus Areas #4.
- **RELATED:** `superpowers:requesting-code-review` - the same discipline on your own diff, before the PR exists.
