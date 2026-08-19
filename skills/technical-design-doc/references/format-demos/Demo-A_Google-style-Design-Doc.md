# Technical Design: Appointment Reminder Service

> **Format Demo A — "Google-style" Design Doc.** Narrative-first. Reads like a well-argued
> memo. Optimized for reviewers who want to understand *why* before *how*. Diagrams and tables
> are used sparingly, in service of the prose.

| | |
|---|---|
| **Author** | Isoon Phitiphasit |
| **Reviewers** | @backend-lead, @platform, @infosec |
| **Status** | Draft · In Review · **Approved** · Superseded |
| **Last updated** | 2026-07-10 |
| **Related** | JIRA: APS-482 · PRD: "Reduce OPD no-shows" |

---

## 1. Context and problem

Roughly 18% of OPD appointments end in no-shows, and today reminders go out manually from the
front-desk team the afternoon before. The process doesn't scale past two branches, misses
same-day bookings entirely, and gives us no delivery tracking.

We want a service that, given the day's confirmed appointments from the HIS, sends each patient a
reminder over their preferred channel (SMS or LINE) at a configurable lead time, and records
whether it was delivered. This document proposes how we'll build it.

## 2. Goals

- Send reminders for 100% of confirmed appointments at a configurable lead time (default: 20:00 the day before, plus a 2-hour-before nudge).
- Support SMS and LINE, with per-patient channel preference and automatic fallback.
- Record delivery status per reminder and expose it for the ops dashboard.
- Handle 3 branches today, ~8k reminders/day, with headroom for 10x.

## 3. Non-goals

- Two-way conversations / rescheduling by reply (future phase).
- Marketing or non-appointment messaging.
- Replacing the HIS as source of truth for appointments.

## 4. Proposed design

The service is a stateless Go microservice that pulls confirmed appointments from the HIS
integration, enqueues a reminder job per appointment, and hands each job to a channel adapter.

At a high level: a **scheduler** wakes on a cron cadence, queries the HIS adapter for appointments
in the target window, and writes reminder jobs to a queue. A pool of **workers** consumes the
queue, resolves the patient's channel preference, calls the appropriate **vendor adapter**
(SMS gateway or LINE Messaging API), and persists the outcome. A thin **status webhook** receives
delivery receipts from the vendors and updates the record.

```
HIS ──(pull)──> [Scheduler] ──> Queue ──> [Workers] ──> SMS/LINE adapter ──> Vendor
                                              │                                  │
                                              └──────> Postgres <── webhook ─────┘
```

We lean on the existing platform: deploy on the shared K8s cluster, Postgres for reminder state,
and the internal message queue rather than standing up new infrastructure.

### Key decisions

- **Pull from HIS, don't wait for push.** The HIS can't reliably push events to us, so the
  scheduler polls. This adds a small latency floor but avoids a fragile dependency on HIS
  outbound calls.
- **One record per reminder attempt, not per appointment.** Makes retries, fallback, and
  per-channel delivery tracking natural to model and query.
- **Idempotency keyed on `(appointment_id, reminder_slot)`.** A re-run of the scheduler must
  never double-send.

## 5. Alternatives considered

**Cron job inside the HIS integration service.** Simplest to ship, but couples reminder logic to
the HIS adapter's release cycle and gives us no independent scaling or clean delivery tracking.
Rejected — reminders will grow features fast and shouldn't ride the integration's cadence.

**Third-party notification SaaS.** Fastest time-to-value, but patient PII would leave our
environment and per-message cost is ~3x our direct vendor rates at our volume. Rejected on
privacy and cost.

**Event-driven (HIS pushes to us).** Cleanest latency, but the HIS team can't commit to reliable
outbound webhooks this year. Revisit when they can.

## 6. Cross-cutting concerns

**Data & privacy.** Reminders carry patient name, appointment time, and phone/LINE ID — PII.
Store the minimum, encrypt at rest, and purge reminder records after 90 days. Adapter logs must
redact phone numbers and message bodies.

**Reliability.** Vendor calls retry with backoff; after N failures on the primary channel we fall
back to the secondary. Scheduler and workers are idempotent so a pod restart mid-run is safe.

**Observability.** Emit metrics for sent/delivered/failed per channel and alert on delivery rate
dropping below threshold. Trace a reminder end-to-end via the appointment ID.

**Security.** Vendor credentials live in the secrets manager, not config. The status webhook
validates vendor signatures.

## 7. Rollout plan

1. Ship behind a flag to one branch, reminders logged but **not sent** (shadow mode) for 3 days; compare against manual list.
2. Enable real sends for that branch; monitor delivery rate and complaints for a week.
3. Roll out branch by branch. Keep the manual process as fallback until all branches are stable.

## 8. Open questions

- Does LINE OA rate-limiting bite at the 20:00 burst, or do we need to spread sends?
- Who owns the patient channel-preference data — us or the HIS?
- Retention: is 90 days acceptable to compliance, or shorter?
