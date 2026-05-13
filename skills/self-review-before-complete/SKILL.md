---
name: self-review-before-complete
description: Use before claiming an implementation task is "done", "complete", "fixed", or "implemented" — applies logic-first review to your own diff. Complements `superpowers:verification-before-completion` (which runs build/test commands); this one reviews logic that commands cannot catch
---

# Self-Review Before Complete

## Core Principle

**Implementation finished ≠ task complete.** Before declaring done, you review your own diff with the same rigor you'd apply to someone else's PR.

Tests passing prove the cases you wrote. They do not prove the cases you didn't think of. Self-review is where you find the latter.

## Relationship to verification-before-completion

These two skills are complements, not alternatives:

- `superpowers:verification-before-completion` runs **commands** (build, lint, typecheck, tests) and confirms output before success claims. It catches what commands can catch.
- `self-review-before-complete` (this skill) reviews **logic** in your own diff. It catches what commands cannot — silent invalid output, narrow-contract bugs, missed edge cases, regressions in adjacent behavior.

Run both. Commands first (they're cheap and definitive), then self-review (catches what's left).

## The Iron Rule

```
NO "DONE" CLAIM WITHOUT A SELF-REVIEW PASS FIRST
```

"Done", "complete", "fixed", "implemented", "ready", "all set" — all trigger this skill.

## The One Exception — Mechanical, Not Subjective

Skip self-review **only if all three are true**:
- Diff is **<5 lines**, AND
- Touches **1 file**, AND
- Has **no logic change** (typo, comment, rename, formatting, dependency bump)

**Run `git diff --stat` and count.** Don't eyeball it. If line count is fuzzy in your head, it's >5.

The exception is mechanical, not subjective. None of the following are valid reasons to skip:
- "It feels trivial"
- "It's straight-line logic"
- "Only N cases / branches"
- "Skill's overhead exceeds its value here"
- "I'd reach for it on a *real* change"
- "I mentally traced each example as I wrote it"

If you find yourself making any of those arguments, the skill is firing correctly — run the review.

## Workflow

```
1. Get the diff:    git diff HEAD          (default — covers staged + unstaged)
                    git diff --staged      (only if narrowing to staged)
                    git show HEAD          (if work is already committed / amending)
2. Apply pattern:   Use logic-first-review skill on the diff
3. Resolve issues:  Bug/Medium → fix before claiming done
                    Low        → fix or note as known limitation
4. Then claim done — and only then.
```

**REQUIRED SUB-SKILL:** Use `logic-first-review` for the review pattern (Current logic → Why it breaks → What should happen → Suggested change).

## What Self-Review Specifically Catches

The kinds of issues commands and tests miss:

| Class | Example |
|-------|---------|
| Silent invalid output | Function returns `'00812345678'` for a malformed input instead of throwing — tests for valid inputs all pass |
| Narrow contract reading | Spec listed 4 example inputs; you handled exactly those and missed `'00'`-prefixed international format |
| Adjacent regressions | Refactor changed shared util; callers in unrelated modules now behave differently |
| Off-by-one / boundary | Empty input, single-element, max-length, zero — none in the test set |
| Missing length / range / type validation | Function accepts `'12345'` and silently returns `'12345'` |
| Dead branches | `if (x)` where `x` is now never falsy after the change |
| Leaked abstractions | Business logic landed in the wrong layer; works but wrong place |

## Common Rationalizations — STOP and Self-Review

These thoughts mean the gate is firing and you're trying to skip it:

| Rationalization | Reality |
|-----------------|---------|
| "I mentally walked through the examples" | Mental walkthrough ≠ self-review. Run `git diff` and trace adversarial inputs. |
| "The spec only listed these inputs, so that's the contract" | Examples are illustrative, not exhaustive. Silent invalid output for unstated inputs is still a bug. |
| "Tests pass" | Tests pass on the cases you wrote. Self-review is where you find the cases you didn't. |
| "It's a simple function" | Simple functions break in subtle ways — that's how they earn their bugs. Run the review. |
| "I followed the spec exactly" | Following the spec literally while missing edge cases is exactly the failure mode this skill prevents. |
| "I'll review at PR time" | At PR time you've forgotten what you were thinking. Review now, while the change is in your head. |
| "This was a one-line typo fix" | Then check the exception (<5 lines AND 1 file AND no logic). If all three hold, skip. Otherwise review. |
| "User is waiting" | They're waiting for *correct* work, not fast-then-broken work. Self-review takes 60 seconds. |
| "Skill's overhead exceeds its value here" | You don't get to weigh costs against a rule. The rule has one exception (the mechanical 5/1/no-logic gate); apply that and stop. The time spent justifying skipping is longer than the review. |
| "It's straight-line logic" / "Only N cases" | Subjective complexity isn't a skip condition. Off-by-one bugs live in straight-line logic. |
| "I'd reach for the skill on a *real* change" | This is a real change. If it has logic and >5 lines, the skill applies. |

## Red Flags — STOP

If you catch yourself saying any of these, you're about to violate the rule:

- "Done." (and you haven't run `git diff`)
- "Implementation complete." (and you haven't traced an adversarial input)
- "Ready for review." (and you haven't reviewed it yourself first)
- "All set." (and you can't name an edge case you considered)
- "Tests pass, so it's good." (tests ≠ review)

**All of these mean: run `git diff`, apply `logic-first-review`, then resume.**

## What "Adversarial Inputs" Means

When tracing the diff, deliberately construct inputs the spec didn't mention:

- Empty / null / undefined
- Already-formatted vs raw (e.g. input that's already in target format)
- Boundary values (0, 1, max, max+1, negative, very large)
- Type-confused (string where number expected, array where scalar)
- Mixed / partial (some valid, some invalid in the same input)
- Unicode / non-ASCII variants
- Inputs that combine spec'd transformations in unexpected ways (e.g. `+66` AND a leading trunk `0`)

Pick 2–3 that are most relevant to the change. Walk each through the new code. If any produces silently-wrong output, that's a Bug.

## Output of a Self-Review

Either:

**(a) Clean** — "Self-review pass. No Bug/Medium issues. [optional: Low notes]." Then claim done.

**(b) Issues found** — Apply `logic-first-review` format, fix Bug/Medium, then re-review the fix. Then claim done.

Never claim done with unaddressed Bug or Medium issues from your own review.
