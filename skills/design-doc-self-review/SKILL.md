---
name: design-doc-self-review
description: Use when finishing or about to hand off edits to a design / spec / technical-design / estimation doc — before posting it for a reviewer, before a grill, or before declaring a doc edit done. Catches the overclaims, internal contradictions, stale framing, and unstated rationale a reviewer would otherwise be the one to flag.
---

# Design-Doc Self-Review

## Overview

Before a design/spec doc goes to a reviewer, run a self-review for the defect classes reviewers reliably catch — so you find them first. Goal: ship docs that survive review on substance. NOT to "fix" things the reviewer hasn't questioned.

## When to Use

- About to hand a TDD / spec / estimation / design doc to a reviewer, or open it for a grill
- Just finished a non-trivial edit to such a doc and are about to call it done
- A decision changed and you edited some sections — sweep the rest for drift

**When NOT to use:**
- Code review → use `logic-first-review` / `self-review-before-complete`
- Pure prose/style polish — this is about claims and consistency, not wording

## The Pattern

Run all six passes. Each is a grep-and-judge over the **whole doc**, not just the section you edited.

| # | Defect class | The check |
|---|---|---|
| 1 | **Overclaim** | Every authority word — *canonical, guaranteed, always, unambiguous, sole source of truth* — does the design deliver it for **every** case, or only the happy path? Scope it down or cut it. |
| 2 | **Internal contradiction** | For each invariant, grep the same concept across sections and confirm they agree (e.g. "never send raw X" in one section vs a section that sends raw X). |
| 3 | **Stale framing after a decision** | After any decision, sweep the doc for the OLD framing's keywords and kill survivors — the decision changed intent; the old words linger elsewhere. |
| 4 | **Rationale gap** | For every non-obvious choice (no FK, generic name, unusual key, retained-after-purge), is the *why* stated inline at the point of definition? If a sharp reviewer would ask "why X?", pre-answer it. |
| 5 | **Name hides intent** | Does each key/column/field name say what it actually is? (an `id` that is really a `submit_id`; a `resource_id` that is really one specific FK.) |
| 6 | **Claim scope** | Does each metric/behavior claim hold for **all** entry paths and states, or is it stated universally but true only for the primary path? State the boundary. |

## The guardrail (most important)

**Surface, don't auto-fix requirements.** Split every finding:
- **Doc-consistency fix** (overclaim, contradiction, stale framing, naming, missing rationale) → fix it.
- **Requirement / scope question** ("do we even use this data?", "is this field needed?") → **do NOT add fields, scope, or schema to pre-empt it.** Flag it for the requirement owner and wait.

Adding a column/scope to satisfy an *imagined* reviewer concern, before the requirement is confirmed, is the classic overreach — it manufactures work the requirement may not want.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Added a field/scope to answer a reviewer's "why not X?" before confirming the requirement | Surface it as a question; only the requirement owner decides scope |
| Reviewed only the section you just edited | Every pass is whole-doc — drift hides in the sections you didn't touch |
| Kept a strong word ("canonical") because it reads well | If it's not true for all cases, it's an overclaim — scope it or cut it |
| Fixed framing in the doc but not in sibling docs (estimation, blueprint, CLAUDE.md) | Sweep all synced artifacts for the same stale framing |

## Related

- **RELATED:** self-review-before-complete, logic-first-review, grill-me
