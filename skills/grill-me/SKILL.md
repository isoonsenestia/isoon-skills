---
name: grill-me
description: Use when the user wants to stress-test a plan or design, asks to be "grilled" on a proposal, says "grill me", or wants relentless interview-style probing of decisions before committing to implementation.
---

# Grill Me

Interview the user relentlessly about every aspect of their plan until reaching shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one.

## The Pattern

- For each question, provide your **recommended answer** alongside the question — don't just ask, take a position.
- Ask **one question at a time.** Wait for the answer before moving on.
- If a question can be answered by **exploring the codebase**, explore instead of asking.
- Keep going until every branch of the decision tree is resolved — don't stop at the first layer.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Asking a flat list of questions at once | One at a time; let each answer reshape the next question |
| Neutral "what do you think?" questions | State your recommended answer, then ask if they agree |
| Asking the user things the code already answers | Read the code first; ask only about genuine ambiguity |
| Stopping after the obvious top-level questions | Follow each answer down to its sub-decisions until the leaves are concrete |

## Attribution

Adapted from Matt Pocock's [grill-me](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md).
