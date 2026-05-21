---
name: continuous-learning
description: Use at session end or mid-session when something non-trivial has been solved — a debugging technique, a workaround, a project-specific quirk, a multi-prompt resteer pattern — to extract that knowledge into a reusable skill so future sessions don't repeat the work.
---

# Continuous Learning

When you solve something non-trivial, write it down as a skill before you forget. The next session won't have your context; the skill will.

## When to invoke

- **End of session** — the `Stop` hook chain calls `evaluate-session.sh` after `session-end.sh` writes the journal footer. The activator prompts the user (`y/N`) before extracting anything.
- **Mid-session, manually** — after you've just figured out something the rest of the codebase / future-you doesn't yet know.
- **After a resteer** — when you had to fire a second prompt to correct Claude's direction, that's a signal the original prompt lacked a rule. The rule belongs in a skill.

## What counts as worth extracting

| Worth a skill | Not worth a skill |
|---------------|-------------------|
| Debugging technique that took >1 hour to discover | One-off fix; you'll never see it again |
| Workaround for a library/tool bug with a clear trigger | Personal preference / aesthetic choice |
| Project-specific pattern (naming, layering, hooks) | Already documented in CLAUDE.md or the repo wiki |
| A reproducible "do X before Y" rule | A vague intuition you can't articulate |
| Mistake you (or Claude) made twice this session | Knowledge derivable from reading the code |

The threshold: **could a fresh Claude session, six months from now, benefit from this if they hit the same problem?**

## How to write the skill

1. **Name it kebab-case.** Short, action-oriented. `avoid-rtk-stale-cache`, not `rtk-cache-notes`.
2. **Path:** `~/.claude/skills/learned/<name>/SKILL.md`.
3. **Frontmatter description is the trigger condition.** Write it as "Use when …" — that's what semantic matching uses.
4. **Body structure:**
   - **The rule** (one sentence, imperative).
   - **Why** (the past incident — concrete, not abstract).
   - **How to apply** (when to act on the rule).
   - **Anti-example** (the failure mode the rule prevents — optional but helpful).
5. **Keep it short.** A skill is not a doc. If it's >60 lines, you're writing a tutorial — split or trim.

## Example (extracted from a real session)

```markdown
---
name: rtk-gain-not-rust-type-kit
description: Use when running rtk commands and they fail with "command not found" or behave unexpectedly — verify the right rtk binary is installed before debugging the command itself.
---

# Avoid the rtk Name Collision

If `rtk gain` fails or `rtk` outputs unexpected content, **verify the binary** with `which rtk` and `rtk --version` before debugging the command.

**Why:** Two unrelated tools ship under the name `rtk`:
- `reachingforthejack/rtk` — Rust Type Kit
- The intended Rust Token Killer

Installing the wrong one masquerades as a config bug.

**How to apply:** First thing on any rtk-related failure — `which rtk && rtk --version`. Then debug.
```

## Anti-patterns

- **Extracting too much.** A 200-line skill no one will read. Trim aggressively.
- **Skills that re-explain the codebase.** That's what the wiki is for. Skills are *behavioral rules*, not documentation.
- **Skills that fire on everything.** A description like "Use when coding" matches every session and contributes noise. Be specific in the trigger.
- **Silent writes.** Never auto-write to `learned/` without user confirmation — risks polluting the skill namespace with vibes.

## When the evaluator script asks

The `evaluate-session.sh` activator prompts: *"Anything from this session worth turning into a skill? (y/N)"*

- **Default to N.** Most sessions don't produce extractable knowledge. That's fine.
- **If Y,** the script opens `$EDITOR` (or `vi` fallback) on a stub at `~/.claude/skills/learned/draft-$(timestamp).md`. Edit, save, then rename the directory and file to the final skill name.
- **Don't extract speculative rules.** If you're not sure it'll come up again, skip it. False-positive skills are noise; missed skills are recoverable.

## Related

- Journal pattern: `[[wiki/concepts/session-memory-persistence]]` — the session log is the input to this extraction.
- Skill authoring: `[[wiki/concepts/skill-authoring]]` — broader guidance on skill structure beyond this extraction-specific recipe.
- Trigger: ECC's `/learn` command is the slash-command analogue; we use the Stop-hook pathway instead.
