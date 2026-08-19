---
name: logic-first-review
description: Use as a sub-skill when another skill (/code-review, self-review-before-complete, security-review) needs the structured review format — Current logic → Why it breaks → What should happen → Suggested change. Pattern reference, not a standalone trigger
---

# Logic-First Code Review

## Core Principle

**Never lead with a suggestion before establishing the current behavior and why it breaks.**

A suggestion without grounded logic is an assertion the reader can't verify. Force every issue through the same four-step explanation so the reader (and you) have to actually understand the code before proposing a change.

## When to Use

- Reviewing a pull request (use with the bundled `/code-review` skill or GitHub MCP for fetching the diff)
- Reviewing a local diff before commit (use with `self-review-before-complete`)
- Reviewing a single file or function someone hands you
- Any time you're producing structured feedback on code you didn't just write

## When NOT to Use

- Pure debugging where you're chasing one specific symptom
- Code generation (you write, not review)
- Style/lint issues that a linter already covers

## The Pattern

For **each issue you flag**, follow this exact order:

**1. Current logic** — explain what the code does today. Be specific: file, function, line behavior. Walk a concrete input through it if non-trivial.

**2. Why it's a problem** — explain what goes wrong, under what conditions. Use a concrete example input that triggers the failure.

**3. What should happen instead** — describe the correct behavior or design in plain terms.

**4. Suggested change** — the concrete code or structural fix.

Use this structure even for minor issues. Skipping step 1 or 2 is the failure mode this skill exists to prevent.

## Publishing Gate (Bug / Medium)

Generate issue candidates aggressively (see Focus Areas and adversarial inputs). Then, before you assign **Bug** or **Medium** to any candidate, it must pass all three checks below. Run them against the code **freshly re-read**, not your memory of it.

1. **Trace.** Write the sequence `input → code path → observable wrong result`, each step pointing at a specific line that does what you claim. If you cannot write the trace, you do not yet understand the failure — it is not a Bug/Medium.
2. **Trigger.** The input in your trace must be reachable with realistic data and callers, not only contrived values. Fires only on contrived input → demote.
3. **No existing guard.** Check for a type, upstream validation, early return, framework guarantee, or surrounding check that already prevents the failure — including guards documented in comments or visible at the call site. If a guard exists, the issue is invalid → drop it.

A candidate that fails any check is **not** a Bug/Medium. Demote it to Low (if it is a real maintainability/style point) or drop it. **Demote, don't inflate.** These are Low at most — they describe hypothetical or unverifiable futures, not a failure you can trace today:

- "Could break if a future caller ignores the validated contract" — the contract holds at every current call site → Low.
- "Duplicated logic might drift" — it is consistent today → Low.
- "Symbol / type is not visible in this diff" — you cannot trace a failure you cannot see → Low or drop; note it as "verify it resolves", not a defect.

**The gate filters false positives; it does not lower the bar for real bugs.** A failure you can trace end-to-end on realistic input stays a **Bug** even if the fix is one line. Detection stays wide — only publishing is gated.

## Output Structure

### Overview
2–3 sentences: what the change does, what problem it solves, overall direction assessment.

### Issues
One block per issue, each following the 4-step pattern above.

### Summary Table

| Severity | Issue |
|----------|-------|
| Bug | ... |
| Medium | ... |
| Low | ... |

Severity levels:
- **Bug** — incorrect behavior, data loss, silent failures, security
- **Medium** — duplication, missing abstraction, regression risk, unhandled edge case
- **Low** — style, naming, consistency

## Focus Areas (in priority order)

1. **Correctness** — logic bugs, edge cases, off-by-one, type/size mismatches, silent invalid output
2. **Regressions & blast radius** — behavior removed or narrowed versus the code being replaced, and the downstream fallout of the change: callers of changed/renamed/removed functions, importers of changed symbols, behavioral-contract shifts (same signature, different return value / thrown error / side-effect), and readers or writers of a changed schema, data shape, config key, or shared state. On a bare pasted diff, at least name the dependents that need checking; with repo access, trace them (see the `self-review-before-complete` blast-radius step)
3. **Duplication** — identical blocks that will drift; extract helpers
4. **Architecture** — business logic leaking into wrong layer, shared utilities missing
5. **Tests** — coverage of edge cases, not just happy path
6. **Consistency** — naming, struct field types diverging from adjacent code

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Leading with "you should..." before tracing what the code does | Always write step 1 (current logic) first, even if obvious |
| Mentally walking through only the inputs the spec lists | Construct adversarial inputs: empty, malformed, boundary, type-confused |
| Assuming the spec's stated examples = the full contract | Treat examples as illustrative, not exhaustive — flag silent invalid output for unstated inputs |
| Flagging style nits as bugs | Use the severity table; nits are Low or omitted |
| Ranking a hypothetical or unverifiable observation as Bug/Medium ("could drift", "might break a future caller", "type not visible here") | Run the Publishing Gate. No traceable failure on realistic input past existing guards → Low or drop, not Medium |
| Restating the PR description | Description is context — review the *code*, not the prose |
| Inventing issues | Only flag what's observable in the diff plus surrounding context |

## What NOT to Do

- Do not suggest a fix before explaining what the current code does.
- Do not flag style nits as bugs.
- Do not restate what the change description already says.
- Do not invent issues.
