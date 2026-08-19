# RFC: Appointment Reminder Service

> **Format Demo C — "RFC-lite" decision doc.** Lightweight and fast to fill. One page of
> problem → proposal → trade-offs. Optimized for quick review and a clear decision, not
> exhaustive documentation. Best for small-to-medium changes.

**Author:** Isoon · **Status:** Proposed · **Date:** 2026-07-10 · **JIRA:** APS-482

## Problem
~18% OPD no-shows. Reminders are sent manually the afternoon before, don't scale past two
branches, skip same-day bookings, and have no delivery tracking.

## Proposal
A small stateless Go service that polls the HIS for confirmed appointments, sends a reminder per
appointment over the patient's preferred channel (SMS/LINE) at configurable lead times, and
records delivery. Runs on the existing K8s cluster with Postgres and the internal queue.

```
HIS ─pull─> scheduler ─> queue ─> workers ─> SMS/LINE ─> vendor
                                     └─> Postgres <─ delivery webhook
```

**Key choices:** pull (HIS can't push reliably) · one record per reminder *attempt* · idempotent
on `(appointment_id, slot)` so re-runs never double-send · channel fallback on failure.

## Alternatives
| Option | Why not |
|---|---|
| Cron inside HIS integration service | Couples to integration release cycle; no clean tracking/scaling. |
| Third-party notification SaaS | PII leaves our environment; ~3x cost at our volume. |
| Event-driven (HIS pushes) | HIS can't commit to reliable webhooks this year; revisit later. |

## Trade-offs / risks
- Polling adds a small latency floor — acceptable (≤5 min).
- LINE may rate-limit the 20:00 burst → spread sends, monitor 429s.
- PII in transit/storage → encrypt at rest, redact logs, purge after 90 days, secrets in vault.

## Rollout
Shadow mode (log-only) at one branch → real sends at one branch → branch-by-branch. Feature-flagged;
manual process stays as fallback until stable.

## Decision
- [ ] Approved  - [ ] Needs changes  - [ ] Rejected

Reviewers: @backend-lead @platform @infosec
