---
name: checking-ready-to-develop
disable-model-invocation: true
description: Use when checking if a story, task, or backlog item meets the Definition of Ready (DoR) to enter a sprint — "is this card ready to develop?", DoR gate, sprint-planning readiness check.
---

# Checking Definition of Ready to Develop

The Definition of Ready (DoR) gates a backlog item into the Sprint Backlog.
A card failing any **required** criterion is not ready, regardless of pressure to start.
Sign-off authority: SM / Tech Lead. (Distinct from Definition of *Done*.)

## When to Use

- Reviewing a card before sprint planning / before moving it to "Ready to Develop"
- "Is this ticket ready to develop?" / "does this meet DoR?"
- Triaging why a card was rejected from a sprint, or drafting one to pass the gate

## Criteria

All **required** must be met. Report a NOT-ready verdict by naming the failing criterion + its owner (route the gap to them).

| # | Required criterion | Owner |
|---|--------------------|-------|
| 1 | Requirements confirmed — acceptance criteria set, all agreed | PM |
| 2 | UI to Dev ready — designs cover success, error **and** loading states | PD |
| 3 | Timeline set — clear start + rollout | PM / SWE |
| 4 | Ticket priority set | PM |
| 5 | Event tracking defined — key events identified | PD |
| 6 | Technical solution ready — clear approach outlined | SWE |

**Optional, do NOT block readiness:** (8) Story estimation — XFN; (9) Test case covering the story — QA.

**Deprecated, do NOT enforce:** ~~(7) Security Review~~ (struck in source).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Blocking on missing estimation or test case | Those are optional (8, 9) |
| Enforcing Security Review | Item 7 is deprecated |
| Accepting UI that only covers the happy path | Error + loading states required (criterion 2) |
| "Ready" verdict without naming the gap's owner | Each criterion has an owner — route it |
| Confusing DoR with Definition of Done | DoR gates sprint entry; DoD gates completion |

Source: Notion — "Definition of Ready to Develop" (Senestia XFN Sprint Working Process Policy).
