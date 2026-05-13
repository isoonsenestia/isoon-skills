# Skill Authoring — Best Practices

Distilled from Anthropic's official skill-authoring guide and the superpowers `writing-skills` skill. Use this as the checklist when adding or editing any skill under `~/.claude/skills/`.

## 1. What a skill IS / IS NOT

- **IS:** a reusable reference for a proven technique, pattern, or tool.
- **IS NOT:** a narrative about a past session, a project-specific convention (put those in `CLAUDE.md`), or a one-off solution.

If the rule is enforceable by a hook or linter, write the hook — not a skill.

## 2. Directory shape

```
skills/
  skill-name/
    SKILL.md              # required
    references/           # optional, heavy reference (>100 lines)
    scripts/              # optional, reusable code/tools
    examples/             # optional, only if not inlineable
```

Flat namespace — every skill lives directly under `~/.claude/skills/`. Sub-directories inside a skill are for that skill's own assets.

## 3. Frontmatter

```yaml
---
name: verb-first-kebab-case
description: Use when <specific trigger / symptom / situation>
---
```

Rules:
- `name`: letters, digits, hyphens only. No parens, slashes, spaces.
- `description`: third-person, starts with **"Use when..."**, lists triggers and symptoms, **NEVER** summarizes the workflow. Keep under ~500 chars; total frontmatter under 1024 chars.
- Optional fields (when supported): `argument-hint`, `allowed-tools`.

### Why no workflow in the description

If the description says "does X then Y", Claude follows the description and skips the body. Keep the description trigger-only so the body actually gets read. See `superpowers:writing-skills` for the CSO failure case this is patched against.

## 4. Naming

- Verb-first or gerund: `save-skill`, `analyzing-phone-data-quality`, `reviewing-prs`.
- Avoid noun-only names like `skill-management` or `frontend-helpers`.
- Name should describe what you DO, not the artifact.

## 5. Body structure (target order)

1. `# Skill Name` (sentence form OK)
2. **Overview / core principle** — 1-2 sentences.
3. **When to Use / When NOT to Use** — bullet list of symptoms.
4. **The Pattern** — the actual technique. Inline code if < 50 lines.
5. **Quick Reference** — table for scanning.
6. **Common Mistakes** — table of failure mode → fix.
7. **Pointers** — link to `references/heavy-file.md` or `scripts/tool.sh` if needed.

Scale each section to its complexity. A 60-line skill is fine if the technique is small.

## 6. Token efficiency

- Frequently-loaded skills: target < 200 words.
- Other skills: target < 500 words for the SKILL.md; push heavy reference into `references/`.
- Don't restate things Claude already knows (what a PDF is, what HTTP is).
- One excellent example beats five mediocre ones — don't ship the same example in three languages.

## 7. Cross-referencing other skills

Use plain references with a requirement marker:

- `**REQUIRED BACKGROUND:** see superpowers:test-driven-development`
- `**RELATED:** logic-first-review`

Do NOT use `@path/to/SKILL.md` — that force-loads content and burns context.

## 8. Flowcharts

Use a Graphviz `dot` block ONLY when there is a non-obvious decision point or a loop where the agent might stop too early. Reference material → tables. Linear steps → numbered list. Never put runnable code in flowchart node labels.

## 9. Description-field examples

```yaml
# BAD — summarizes workflow
description: Use when reviewing PRs - fetches diff, runs lint, posts comments

# BAD — first person
description: I help review PRs

# BAD — too abstract
description: For code review

# GOOD — trigger-only
description: Use when asked to review a pull request or code changes
```

## 10. The Iron Law

> No skill (and no edit to a skill) ships without first watching it be needed.

For high-stakes / discipline skills: write a pressure scenario, run it without the skill, document what fails, then write the skill against those failures. For low-stakes reference skills: at minimum, exercise it once in a real task before declaring it done.

## 11. Checklist before saving

- [ ] `name` is kebab-case, verb-first, letters/digits/hyphens only.
- [ ] `description` starts with "Use when..." and contains no workflow summary.
- [ ] Frontmatter < 1024 chars total.
- [ ] Body has Overview, When to Use, the technique itself, and Common Mistakes.
- [ ] No `@` force-load links.
- [ ] Heavy reference (>100 lines) lives in `references/`, not inline.
- [ ] Listed in `_meta/INDEX.md`.

## 12. References

- Anthropic official: `~/.claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-skills/anthropic-best-practices.md`
- Superpowers writing-skills: same directory, `SKILL.md`
- Spec: https://agentskills.io/specification
