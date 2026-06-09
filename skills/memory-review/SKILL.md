---
name: memory-review
description: Use when the user says "review memory", "audit my memories", "/memory-review", "is this memory still relevant", or wants to walk through entries in ~/.claude/projects/-Users-io-claude-things/memory/ and decide what to keep
---

# Memory Review

## Overview

Walk through each file in the auto-memory directory with the user, ask "still relevant?", and prune stale entries (plus their `MEMORY.md` index line). One file at a time — deletions need human judgment, especially for feedback and project memories that drift in subtle ways.

## When to Use

- User says "review memory", "audit memories", "let's clean up MEMORY.md"
- A memory was just acted on and turned out to be stale
- Periodic hygiene — every few weeks, or when `MEMORY.md` exceeds ~30 entries

**When NOT to use:**
- For journal/transcript bloat → use `tidy-memory` instead.
- For adding a new memory → that happens organically as I detect save-worthy facts.
- For mass deletion ("delete all feedback memories") → refuse and walk through individually.

## The Pattern

### Step 1 — List the memory directory

```bash
ls ~/.claude/projects/-Users-io-claude-things/memory/
cat ~/.claude/projects/-Users-io-claude-things/memory/MEMORY.md
```

Count entries and group by type prefix (`user_`, `feedback_`, `project_`, `reference_`). Project memories decay fastest; user memories rarely.

### Step 2 — Walk each entry, one at a time

For each `*.md` file (skip `MEMORY.md` itself):

1. Read the file. Print the `description:` line and the body (or the first 15 lines if longer).
2. State the **age** (`stat -f '%Sm' -t '%F'` on macOS) and the **type** from frontmatter.
3. Ask one of:
   - For **user** memories: "Still accurate?"
   - For **feedback** memories: "Still want me to follow this rule?"
   - For **project** memories: "Is this project state still current? Date in the entry: X — that's N months old."
   - For **reference** memories: "Does this resource still exist / is it still the right pointer?"
4. Wait for the answer. Do not batch.

### Step 3 — Act on each decision

| Answer | Do this |
|---|---|
| "Keep" / "yes" | Move on. No edit. |
| "Update" | Ask what to change. Edit the body, refresh `description:` if the meaning shifted. |
| "Delete" | Remove the file. Remove its line from `MEMORY.md`. Confirm both happened. |
| "Not sure" | Default to keep — but ask if I should re-verify against current code/files now. |

### Step 4 — Reconcile `MEMORY.md` at the end

After all decisions:
- Read `MEMORY.md` and check every line still points to an existing file.
- Remove orphan lines (file gone but index entry remains).
- Confirm the file count matches: `ls *.md | grep -v MEMORY.md | wc -l` vs index line count.

### Step 5 — Summary

Print: kept N, updated M, deleted K. List the deleted entries by slug for the user's reference.

## Quick Reference

| Memory type | Decay rate | Question to ask |
|---|---|---|
| `user_*` | Slow — preferences and role | "Still accurate?" |
| `feedback_*` | Medium — corrections age as habits form | "Still want me to follow this rule?" |
| `project_*` | Fast — initiatives, deadlines, bugs | "Is this state still current?" (cite the date) |
| `reference_*` | Medium — external systems change names | "Does this pointer still resolve?" |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Batching — showing all 10 files and asking "which to delete" | Walk one at a time. Batching surfaces deletion fatigue. |
| Deleting file but forgetting `MEMORY.md` line | Step 4 reconciliation catches this — don't skip it. |
| Editing a memory's body but not its `description:` frontmatter | Description drives future relevance matching; keep it in sync with the body. |
| Treating "I'm not sure" as deletion | Default to keep when uncertain. The cost of carrying a stale memory is low; the cost of losing a load-bearing one is higher. |
| Reviewing memories I just wrote this session | Skip entries from the current session — they haven't aged. |

## Related

- **RELATED:** tidy-memory (journal + transcript pruning, not memory files)
- **REQUIRED BACKGROUND:** the auto-memory system's frontmatter rules — see the `# auto memory` section of the global system prompt
