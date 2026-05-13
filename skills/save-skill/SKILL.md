---
name: save-skill
description: Use when the user says "save this as a skill", "make this a skill", "remember this pattern as a skill", "capture this workflow", or otherwise asks to persist a technique into ~/.claude/skills/
---

# Save Skill

## Overview

Capture a technique that just proved itself in this session into a properly-structured personal skill under `~/.claude/skills/`. Optimize for **getting it saved**; iteration comes later.

## When to Use

- User says "save this as a skill" / "make this a skill" / "let's keep this pattern"
- User describes a workflow they want to reuse in future sessions
- A non-obvious technique just worked and the user wants it persisted

**When NOT to use:**
- The technique is project-specific → put it in that project's `CLAUDE.md` instead.
- The rule is mechanically enforceable → write a hook, not a skill.
- The user wants to remember a *fact* about themselves or the project → use the memory system, not a skill.

## The Pattern

1. **Confirm the four inputs.** Ask only for what isn't already obvious from the conversation:
   - **Name** (verb-first, kebab-case, ASCII letters/digits/hyphens only)
   - **Trigger** — the "Use when..." sentence (no workflow summary)
   - **Technique** — the actual steps, table, or pattern
   - **Failure modes** — at least one mistake → fix entry, if known
2. **Read `~/.claude/skills/_meta/BEST_PRACTICES.md`** before drafting. It has the authoritative frontmatter and structure rules.
3. **Draft from `~/.claude/skills/_meta/TEMPLATE.md`.** Don't invent a new structure.
4. **Validate against the checklist** in `_meta/BEST_PRACTICES.md` §11 before writing.
5. **Write `~/.claude/skills/<name>/SKILL.md`.**
6. **Append a one-line entry to `~/.claude/skills/_meta/INDEX.md`** in the `## Skills` section, alphabetical.
7. **Tell the user**: where it was saved, that the description is trigger-only by design, and that the skill can be refined later (with what to look for — see "Improving later" below).

## Quick Reference

| Step | Tool | What to check |
|------|------|---------------|
| Draft | Read `_meta/TEMPLATE.md` | Frontmatter `name` + `description` only |
| Description | n/a | Starts with "Use when..."; no workflow summary |
| Write | Write tool | Path is `~/.claude/skills/<name>/SKILL.md` |
| Register | Edit `_meta/INDEX.md` | One line, alphabetical |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Description summarizes the workflow ("Use when X — does A then B") | Strip everything after the trigger; the body holds the workflow |
| Name is noun-only (`skill-helpers`) | Rewrite verb-first (`helping-with-skills` or, better, the actual verb you do) |
| Skill is really project-specific | Move to that project's `CLAUDE.md` instead |
| Body restates what Claude already knows | Delete; assume Claude is smart |
| Forgot to update `_meta/INDEX.md` | Add the entry — the index is how the user audits the skill set |
| Used `@path/to/file` to reference another skill | Use plain reference: `**RELATED:** other-skill-name` |

## Improving later

Tell the user the skill is intentionally a v1. Concrete improvement triggers:
- It fired but Claude still missed the technique → tighten the **description** triggers.
- It fired but Claude did the wrong steps → tighten the **body** or add a **flowchart** for the non-obvious decision.
- Same mistake keeps appearing → add a row to the **Common Mistakes** table.
- Body is growing past ~500 words → move heavy material to `<name>/references/`.

## Related

- **REQUIRED BACKGROUND:** see `~/.claude/skills/_meta/BEST_PRACTICES.md`
- **TEMPLATE:** `~/.claude/skills/_meta/TEMPLATE.md`
- **DEEPER METHODOLOGY:** superpowers:writing-skills (RED-GREEN-REFACTOR for skills)
