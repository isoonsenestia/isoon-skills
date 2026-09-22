---
name: ask-pm
description: Use when unsure what to work on next, which workspace application or project to work in, or which process to follow.
disable-model-invocation: true
---

# Ask PM

Use this as a router when the user is unsure what to do next, which application to work in, or which process to follow.

Start by identifying the decision, not by proposing work. Inspect only enough current workspace context to distinguish the likely destinations: top-level directories and the relevant `MISSION.md`, `NOTES.md`, `AGENTS.md`, issue, or task document. Prefer the user's latest stated goal over stale notes.

## Recommend one path

Give one primary recommendation. State it in this format:

```text
Work on: <application, project, or learning track>
Why now: <one concrete reason>
First move: <smallest useful next action>
Process: <short workflow>
```

Include one alternative only when it is genuinely viable and explain the condition that would make it preferable. Ask one focused question only when the answer would change the recommendation materially.

## Routing

### Learn a capability

Continue the relevant stateful learning track in the workspace. Read its `MISSION.md` and `NOTES.md`, find the latest lesson or learning record, and offer the next focused practice. Use a real active project only when it helps apply that single concept.

### Build or change an existing application

Choose the application directory that owns the user-facing outcome. Read its local agent guidance and task documents before proposing a change. Route a small, clear change to implementation; route a multi-session or unclear feature through requirements, decision-making, and a concise implementation plan first.

### Something is broken or unclear in an application

Route to diagnosis. First establish the observed behavior, expected behavior, and a reproducible feedback loop. Do not recommend fixes until there is evidence for the cause.

### Evaluate a plan, design, or decision

Route to a structured review. Separate the decision to make, constraints, options, trade-offs, and decision owner. Recommend a prototype when behavior or UI must be observed before the decision can be trusted.

### Research before acting

Route to focused research when the answer depends on external, current, or authoritative facts. Define the decision the research must unlock and stop after it is supported by sufficient primary sources.

### Improve an engineering system

Choose the owning codebase, then distinguish between architecture/design work, quality/review work, operational hygiene, and feature work. Recommend the narrowest process that can create a durable improvement.

### Create or improve a reusable agent skill

Route to skill creation. Define the repeated situation, the decision the skill should improve, and its invocation boundary before writing instructions. Keep the skill user-invoked unless autonomous discovery is clearly valuable.

## Application choice

When more than one workspace application could fit, compare them on:

- Directness: does it own the desired user or business outcome?
- Readiness: is there a concrete next artifact, issue, or lesson?
- Leverage: will this unblock or improve other work?
- Risk: can the next action be validated safely?

Choose the highest-leverage ready option. If none is ready, recommend the smallest action that makes one option ready rather than starting speculative work.

## Process choice

Use the lightest process that preserves quality:

- A single, testable change: inspect, implement, verify.
- A behavior or failure not yet understood: diagnose, reproduce, explain, then fix if requested.
- A decision with material trade-offs: frame, compare, decide, record.
- A large or cross-functional effort: establish outcome, scope, owners, dependencies, milestones, risks, and decision path.
- A portfolio conflict: compare outcome, deadline, cost of delay, capacity, and bottleneck; make the deferred work visible.

End with an actionable next step. Do not begin unrelated work unless the user asks to proceed.
