---
name: logic-first-review
description: Use as a sub-skill when another skill (review, self-review-before-complete, security-review) needs the structured review format — Current logic → Why it breaks → What should happen → Suggested change. Pattern reference, not a standalone trigger
---

# Logic-First Code Review

## Core Principle

**Never lead with a suggestion before establishing the current behavior and why it breaks.**

A suggestion without grounded logic is an assertion the reader can't verify. Force every issue through the same four-step explanation so the reader (and you) have to actually understand the code before proposing a change.

## When to Use

- Reviewing a pull request (use with `review` skill or GitHub MCP for fetching the diff)
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
2. **Regressions** — behavior removed or narrowed versus the code being replaced
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
| Restating the PR description | Description is context — review the *code*, not the prose |
| Inventing issues | Only flag what's observable in the diff plus surrounding context |

## What NOT to Do

- Do not suggest a fix before explaining what the current code does.
- Do not flag style nits as bugs.
- Do not restate what the change description already says.
- Do not invent issues.
