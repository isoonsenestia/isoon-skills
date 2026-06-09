# Grill-me — Document output reference

Heavy reference for the `## Document output` section of `SKILL.md`. Read when you're about to grill and need the exact template / schema / discovery logic.

## 1. File location and naming

The artifact lives **next to the source doc** (same directory), named:

```
<Source Title> - Grilled #N.md
```

Where `<Source Title>` is the source doc's basename **without** its `.md` extension. Examples:

| Source | Output |
|---|---|
| `Technical Design - Draft 5 (Post-Wiki-Grill).md` | `Technical Design - Draft 5 (Post-Wiki-Grill) - Grilled #1.md` |
| `Plan.md` | `Plan - Grilled #1.md` |
| `RFC-007.md` | `RFC-007 - Grilled #1.md` |

The output filename embeds the source's full name (including any existing `Draft N`, parens, etc.) — do not strip those. They're part of the identity of what was grilled.

## 2. N detection

At the start of the session, list sibling `.md` files in the same directory. For each, match the regex:

```
 - Grilled #(\d+)\.md$
```

`N = max(captured groups) + 1`. If no matches, `N = 1`.

**N is fixed for the duration of the session.** If the user re-engages mid-session ("one more question"), keep writing into the same `Grilled #N.md` — do not bump.

## 3. Source-doc discovery

The skill must know which doc is being grilled before Q1.

1. Scan the most recent ~20 conversation turns for `.md` paths (user messages, tool outputs, `@`-mentions).
2. Deduplicate. Filter out anything in `~/.claude/`, `node_modules/`, `.git/`, build output dirs.
3. **If exactly one candidate:** propose it, ask for confirmation. ("Grilling `<path>` — confirm?")
4. **If multiple candidates:** list them numbered, ask the user to pick. **Do not pick one arbitrarily.**
5. **If none:** ask plainly. ("Which document should I grill against?")

Do not start Q1 until the source is confirmed. Without it, the first ledger write has nowhere to land.

## 4. File structure

### 4.1 Header (written on first Q)

```markdown
# <Source Title> — Grilled #N

**Source:** `<relative or absolute path to source doc>`
**Grill started:** YYYY-MM-DD
**Status:** In progress
```

When the session ends, change `Status:` to `Complete`.

### 4.2 `## Decisions` ledger (appended per-Q)

```markdown
## Decisions

| # | Question | Recommended | User resolution | Affects § |
|---|----------|-------------|-----------------|-----------|
| 1 | <verbatim or compressed Q> | <your position going in> | <what the user landed on, in their words where possible> | §<section ref in source> |
```

Schema rationale (why each column matters):

- **`#`** — stable ID. The folded sections cite these.
- **`Question`** — the resolved question. Keep it short; full detail lives in the chat.
- **`Recommended`** — the position the skill took going in. Important for retrospectives ("we overrode the recommendation in row 3 — did that hold up?").
- **`User resolution`** — what the user actually decided. The single source of truth for the fold.
- **`Affects §`** — which section of the source doc this changes. If unknown, use `?` and resolve at fold time. Without this column the folded rewrite has no anchor.

### 4.3 `## Folded sections` (single write, at session end)

```markdown
## Folded sections

### §<X> (rewritten)

<full rewritten §X of the source doc, with grill decisions folded in>

> **Folds:** rows #2, #5

### §<Y> (rewritten)

...
```

Write once, at session end. The user signals end-of-session with phrases like "we're done", "that's all", or by going quiet on follow-ups. Only the §sections that the ledger touched get rewritten — the rest stays in the source doc untouched.

## 5. Worked example

Source: `Technical Design - Draft 5 (Post-Wiki-Grill).md`. No existing `Grilled #N` siblings, so `N = 1`. Output: `Technical Design - Draft 5 (Post-Wiki-Grill) - Grilled #1.md`.

### After Q1

```markdown
# Technical Design - Draft 5 (Post-Wiki-Grill) — Grilled #1

**Source:** `./Technical Design - Draft 5 (Post-Wiki-Grill).md`
**Grill started:** 2026-05-22
**Status:** In progress

## Decisions

| # | Question | Recommended | User resolution | Affects § |
|---|----------|-------------|-----------------|-----------|
| 1 | Should `bmi_assessment` retention be 180d auto-delete or DPO-request-only? | 180d auto-delete (matches TDD-5 §1.1) | Confirmed: 180d auto-delete via nightly sweep | §1.1 |
```

### After Q2 (only the ledger grows)

```markdown
| 1 | Should `bmi_assessment` retention be 180d auto-delete or DPO-request-only? | 180d auto-delete (matches TDD-5 §1.1) | Confirmed: 180d auto-delete via nightly sweep | §1.1 |
| 2 | Does `actor_email` need allowlist validation before SSO migration? | No — regex shape only is sufficient v1 | Agreed: no allowlist v1; revisit at SSO migration | §3.4 |
```

### End-of-session (Status flipped + folded sections written)

```markdown
**Status:** Complete

## Decisions
...table as above...

## Folded sections

### §1.1 (rewritten)

<TDD §1.1 with the 180d auto-delete decision folded in as locked text>

> **Folds:** row #1

### §3.4 (rewritten)

<TDD §3.4 with the allowlist deferral folded in>

> **Folds:** row #2
```

## 6. Edge cases

| Case | Handling |
|---|---|
| Source doc has no `Grilled #N` siblings | Start at `#1` |
| Source filename contains `#` or `(...)` | Treat as part of the title; the counter regex only matches the trailing ` - Grilled #N.md` suffix |
| User re-grills mid-session ("one more thing") | Continue writing into the same `Grilled #N.md` — do not bump N |
| Session interrupted before folded-sections write | The ledger alone is still a valid artifact; leave `Status: In progress`. A follow-up session can resume by appending to the same file |
| User explicitly asks for a fresh file | Bump N as usual at the new session's start |
| Source doc cannot be located on disk | Ask the user to clarify; do not invent a path |
| Multiple `.md` candidates with very similar names | Show full paths, not just basenames, when listing for the user to pick |

## 7. What NOT to put in the artifact

- Verbatim chat dump — the ledger is a compressed decision record, not a transcript.
- Speculative or unresolved questions — those stay in the chat until resolved, then land as a row.
- Source-doc content that wasn't changed by the grill — the fold only covers touched §sections.
