---
name: resplitting-commits
description: Use when a branch's commits are tangled or junk-named ("wip", "stuff", "fixes") and need to be rebuilt as clean atomic commits, or when asked to squash-and-re-split, flatten and recommit, or reorganize a branch's history into one commit per concern.
---

# Re-split a Messy Branch Into Atomic Commits

**Rule:** Anchor first, build **forward** from the base, gate every commit and the endpoint:

```bash
git branch anchor/<name> HEAD           # 1. anchor the original tip
git reset --mixed <base>                # 2. all changes unstaged, tree untouched
rtk proxy git --no-pager diff -U10 --no-color <base> anchor/<name> > /tmp/all.patch
                                        # 3. per concern: copy all.patch, then cut the other
                                        #    concerns out of the copy (see Trimming rules below)
git apply --cached --recount /tmp/concern.patch
rtk proxy git diff --cached             # 4. review what this commit actually contains
git commit -m "feat(x): ..."            #    repeat 3-4 per concern
rtk proxy git diff anchor/<name> HEAD   # 5. MUST be empty
rtk proxy git status --porcelain        #    MUST be empty
```

Keep `anchor/<name>` until the branch is pushed or reviewed, then delete it.

**Why two gates:** nothing in git enforces that the re-split tree matches the original. The endpoint gate (step 5) proves the final tree is faithful; it cannot see a bad intermediate commit, because a later `git add -A` silently restores the correct final tree. Step 4 is the only thing that catches that.

Split by **concern, not by file**: a config key belongs with the feature that reads it, even when that means splitting one file's hunk across two commits. Changes that were added and then removed within the branch net to zero and simply never appear in the new history - do not fabricate a commit to remove them.

**Dependent branches:** if other branches stack on this one, their base SHA just changed. **REQUIRED SUB-SKILL:** use `restack-after-amend` before touching them.

**Trimming rules for step 3:**

- **Diff commit-to-commit.** `git diff anchor/<name> -- <file>` compares the anchor against the worktree, which after `reset --mixed` still holds the anchor's content - it returns 0 bytes every time.
- **Cut a foreign `+` line by deleting it. Cut a foreign `-` line by flipping its `-` to a space**, making it context - deleting it drops that line from this commit's file entirely.
- **A flipped `-` line must move below the `+` lines you kept.** Left in place, it yields an intermediate commit with the code in the wrong order. That patch applies cleanly, passes a syntax check, and still passes the endpoint gate, because the next `git add -A` restores the correct final tree. Only `git diff --cached` catches it.
- `--recount` on `git apply` is mandatory: cutting lines invalidates the hunk header counts.
- `git add -A` is legitimate for the **last** concern only, where the unstaged remainder already *is* that concern.

**Two rtk traps:**

- `rtk git` summarizes `diff` and `status` - it prints `ok` for a non-empty diff and emits patches `git apply` rejects. **Every diff, status, and patch-generating command here must go through `rtk proxy git`**, or the gates pass on output that was never read.
- `rtk proxy git diff <a> <b> -- <paths>` returns 0 bytes; the pathspec form is eaten. Diff without a pathspec and trim the patch instead.

`git add -p` is not an option: it needs a TTY, and it cannot split concerns that interleave inside one contiguous hunk.

**Anti-example:** producing an intermediate state by retyping content - hand-editing the file backwards, or hand-authoring the patch. Deleting lines from a real diff is safe because you never author content; typing lines into one is the drift you are trying to avoid. When you need a file's exact final content back, restore it (`git checkout anchor/<name> -- <file>`), never retype it.
