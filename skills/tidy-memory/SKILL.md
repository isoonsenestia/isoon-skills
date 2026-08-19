---
name: tidy-memory
description: Use when the user says "tidy memory", "clean up memory", "prune journal", "the transcripts are bloated", "/tidy-memory", or when SessionStart context shows transcript/journal counts past the nudge threshold and the user wants to act on it
---

# Tidy Memory

## Overview

On-demand audit of the three persistence tiers (auto-memory, journal, transcripts), with deletion proposals the user must approve. No silent cron — the user stays in the loop because deletions need judgment.

## When to Use

- User says "tidy memory", "clean up memory", "let's prune the journal"
- The SessionStart `memory-counts.sh` nudge fired and the user wants to act on it
- Disk pressure check after `du -sh ~/.claude/`

**When NOT to use:**
- For removing a specific stale memory entry → use `memory-review` instead (per-file walk).
- For *disabling* persistence on a single session → use `claude-nomem` alias instead.
- For project-specific files (worktrees, build artifacts) — out of scope.

## The Pattern

### Step 1 — Report current footprint

Run a single audit pass and present a table. Use `du`, `find`, and `stat` — no fancy tools:

```bash
echo "=== Footprint ==="
du -sh ~/.claude/journal ~/.claude/projects ~/.claude/skills/learned 2>/dev/null

echo "=== Memory ==="
ls ~/.claude/projects/-Users-io-claude-things/memory/*.md 2>/dev/null | grep -v MEMORY.md | wc -l
echo "=== Journal age buckets ==="
for d in 7 30 60 90; do
  n=$(find ~/.claude/journal -name '*.tmp' -mtime +$d 2>/dev/null | wc -l)
  echo "older than ${d}d: $n"
done

echo "=== Transcripts by project (top 10) ==="
du -sh ~/.claude/projects/*/ 2>/dev/null | sort -h | tail -10
```

### Step 2 — Propose deletions per tier

For each tier with prunable content, list candidates and ask for approval. Defaults:

| Tier | Default prune candidates | Rationale |
|---|---|---|
| Journal | Files older than 30d (SessionStart only reads <7d, so >30 is dead weight) | Safe — context layer ignores them already |
| Transcripts | Files older than 60d **AND** in projects not touched in 30d | Conservative — recent resumability matters |
| `skills/learned/` drafts | Anything older than 14d that wasn't turned into a skill | Drafts are ephemeral by intent |
| Auto-memory | **Never** auto-propose — defer to `memory-review` | Each one needs human judgment |

Present each tier as: "Found N candidates totaling X MB. Sample: …. Delete?"

### Step 3 — Execute on approval, file-by-file or batch

- Batch deletions only after explicit user "yes" — never on a vague "looks good".
- Use `find … -print -delete` (or `rm` with the explicit list) so the deleted paths echo to the terminal.
- Skip `~/.claude/projects/-Users-io-claude-things/memory/` entirely — that's `memory-review`'s job.

### Step 4 — Report what was freed

After deletion, re-run `du -sh` on the affected directories and show the delta. One line per tier.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Journal >50 files, all <7d old | Don't prune — daily files are expected; only stale (>30d) are candidates |
| Transcripts >200 MB | Prune by project age, not global age — recent projects might span months |
| `skills/learned/` has drafts | Ask whether to save-as-skill or delete; don't auto-delete drafts the user might still want |
| User says "delete everything" | Refuse. Confirm tier-by-tier. |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Auto-deleting auto-memory files | Defer all `memory/*.md` decisions to `memory-review` |
| Pruning today's journal because it has zero content | Only consider files older than 30d; today's might still get appended |
| Treating "approved tier 1" as approval for tier 2 | Re-confirm per tier — blast radius differs |
| Deleting transcripts in an active project | Cross-check project mtime, not just file mtime |
| Dry-running with `rm -rf` instead of `find -print` | Always preview the file list before deletion |

## Related

- **RELATED:** memory-review (per-file curation of auto-memory entries)
- **RELATED:** your skill-authoring skill (rescue a `skills/learned/draft-*` before tidy deletes it)
