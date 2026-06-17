---
name: restack-after-amend
description: Use when you've amended, reworded, or rewritten a commit on a base branch in a stacked-branch / stacked-PR chain and need to rebase the dependent branches onto it without conflicts or duplicate commits.
---

# Re-stack Dependent Branches After Rewriting a Base

**Rule:** Capture each dependent branch's *old base SHA before* you rewrite the base. Then rebase dependents with `git rebase --onto <new-base> <old-boundary-sha> <branch>` when the base commit was **amended/replaced** (drops the superseded commit); use plain `git rebase <new-base> <branch>` only when the base change was **purely additive** (new commits on top).

**Why:** In a `result-ui → result-display → SLA-2720` chain, we amended the ruler-fix commit on `result-ui` (its SHA changed). A plain `git rebase result-ui result-display` replays the *old* ruler-fix commit (still in `result-display`'s history) on top of the new one → conflict on the same file + a duplicate commit. `git rebase --onto result-ui <old-ruler-sha> result-display` dropped the stale commit cleanly. Hit this 3× in one session; the additive case (a new feature commit on top) was the only one where plain rebase was correct.

**How to apply:**
1. *Before* rewriting: `OLD=$(git rev-parse <base-branch>)` for each dependent's current base.
2. Amend/rewrite the base branch.
3. Per dependent: amended base → `--onto <new-base> <OLD>`; additive base → plain `git rebase <new-base>`.
4. Verify every link: `git merge-base --is-ancestor <base> <dep>` (✓ each), and no dup subjects: `git log --oneline <root>..<tip> | sed -E 's/^[0-9a-f]+ //' | sort | uniq -d` (expect empty).

**Anti-example:** `git rebase result-ui result-display` right after amending `result-ui`'s tip → replays the superseded commit → conflict + duplicate in history. The `--onto <old-boundary>` form is what avoids it.
