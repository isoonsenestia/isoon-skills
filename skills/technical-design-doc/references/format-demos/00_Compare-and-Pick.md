# Technical Design Doc — format options to pick from

Three demo templates, all filled with the **same** example (Appointment Reminder Service:
a Go microservice that integrates the HIS with SMS/LINE vendors) so you're comparing *format*,
not content. Skim all three, then tell me which one(s) to base the skill on — we can also mix
sections across them.

## At a glance

| | Demo A — Google-style | Demo B — Structured SDD | Demo C — RFC-lite |
|---|---|---|---|
| **Feel** | Narrative memo, argument-driven | Formal, section-numbered, table-heavy | One-pager, decision-driven |
| **Length** | ~3-4 pages | ~4-5 pages | ~1 page |
| **Strong at** | Explaining *why*; alternatives & reasoning | Sign-off, audit, hand-off, NFRs | Fast review, small/medium changes |
| **Weak at** | Formal completeness / audit trail | Speed; can feel heavy for small work | Depth; not enough for complex builds |
| **Best when** | New service, real design debate | Enterprise/regulated, needs approval | A focused change, quick decision |

## How each is organized
- **A (Google-style):** Context → Goals → Non-goals → Proposed design (+ key decisions) → Alternatives → Cross-cutting concerns → Rollout → Open questions.
- **B (Structured SDD):** Doc control + revision history → Overview → Requirements (FR/NFR tables) → Architecture → Interfaces → Data design → NFR notes → Risk table → Rollout/rollback → Open items.
- **C (RFC-lite):** Problem → Proposal → Alternatives → Trade-offs/risks → Rollout → Decision checkbox.

## My take for your context
Given microservices + integrations at standard depth, a solid default is **A or B**, with **C**
kept as a "lite mode" for smaller changes. A common, effective setup is a skill that produces
**B-structure with A's narrative voice**, and can drop to **C** when you say "quick" or "RFC".

## What I need from you
1. Which format(s) do you want the skill to produce — one, or a default + a lite mode?
2. Anything to add/remove (e.g. cost/ROI section like your PRD skill, a capacity table, security review checklist, sequence diagrams)?
3. Should it auto-pull context from Jira (like your other skills) and/or write output to Notion?

Once you pick, I'll note that I can't build the skill file directly in this session — but I'll
prepare the full SKILL.md content and instructions ready for you to add via Settings → Capabilities.
