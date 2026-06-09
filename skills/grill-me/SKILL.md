---
name: grill-me
description: Use when the user wants to stress-test a plan or design, asks to be "grilled" on a proposal, says "grill me", or wants relentless interview-style probing of decisions before committing to implementation.
---

# Grill Me

Interview the user relentlessly about every aspect of their plan until reaching shared understanding. Walk down each branch of the design tree, resolving dependencies one-by-one. Each session writes a durable sibling artifact so resolutions outlive the chat.

## The Pattern

- Provide your **recommended answer** with every question — don't just ask, take a position.
- Ask **one question at a time.** Wait for the answer before moving on.
- If a question can be answered by **reading the code**, read instead of asking.
- Walk to the **leaves** — don't stop at the obvious top-level questions.

## Document output

Write to a sibling of the source doc: `<Source Title> - Grilled #N.md`.

- **Source doc.** Scan recent turns for `.md` paths. Multiple candidates → list them and let the user pick. None → ask. Don't silently guess. Don't start Q1 until the source is confirmed.
- **N.** `max` of existing `Grilled #(\d+)` siblings `+ 1`; first run = `1`. Fixed for the session.
- **Structure.**
  - `## Decisions` — ledger table, **appended per resolved Q**, row schema `| # | Question | Recommended | User resolution | Affects § |`. First Q writes file header + table header + row 1.
  - `## Folded sections` — **written once, at session end**: rewritten §sections of the source that the grill touched, citing ledger row numbers.

See `references/document-output.md` for the full template, schema rationale, worked example, and edge cases.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Flat list of questions at once | One at a time; let each answer reshape the next |
| Neutral "what do you think?" | State your position, then ask if they agree |
| Asking what the code already answers | Read first; ask only about genuine ambiguity |
| Stopping at the top-level questions | Walk each answer down to its sub-decisions |
| Starting Q1 before the source doc is confirmed | Resolve the source path first — the first ledger write needs to land somewhere |
| Rewriting folded sections after every Q | Only the ledger writes per-Q; fold once at session end |
| Silently guessing the source from multiple `.md` candidates | List candidates, let the user pick |

## Attribution

Adapted from Matt Pocock's [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md). The document-output behavior is an isoon extension.
