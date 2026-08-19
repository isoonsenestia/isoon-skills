# Solution Design Document — Appointment Reminder Service

> **Format Demo B — "Structured Solution Design (SDD)".** Section-numbered, enterprise style.
> Explicit tables for non-functional requirements, interfaces, data, and risks. Optimized for
> completeness, sign-off, and hand-off to implementers or auditors.

## Document control

| Field | Value |
|---|---|
| Document ID | SDD-APS-482 |
| Version | 0.1 (Draft) |
| Author | Isoon Phitiphasit |
| Approvers | Backend Lead, Platform, InfoSec |
| Status | Draft |
| Date | 2026-07-10 |

**Revision history**

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-07-10 | Isoon | Initial draft |

---

## 1. Overview

### 1.1 Purpose
Define the technical design for a service that sends appointment reminders to OPD patients over
SMS and LINE, tracks delivery, and reduces no-shows.

### 1.2 Scope
**In scope:** reminder scheduling, SMS/LINE delivery, channel preference, delivery tracking,
ops-dashboard feed. **Out of scope:** two-way messaging, marketing, rescheduling logic.

### 1.3 Definitions
HIS — Hospital Information System (source of appointments). Reminder slot — a scheduled send
(e.g. "day-before" or "2-hour").

## 2. Requirements

### 2.1 Functional
| ID | Requirement |
|---|---|
| FR-1 | Retrieve confirmed appointments from HIS for a configurable window. |
| FR-2 | Send a reminder per appointment at each configured slot. |
| FR-3 | Route to SMS or LINE by patient preference; fall back on failure. |
| FR-4 | Persist delivery status per reminder attempt. |
| FR-5 | Expose delivery data to the ops dashboard. |

### 2.2 Non-functional
| ID | Category | Target |
|---|---|---|
| NFR-1 | Throughput | 8k reminders/day now; scale to 80k without redesign. |
| NFR-2 | Latency | Reminder sent within 5 min of its slot. |
| NFR-3 | Availability | 99.5% monthly for the send path. |
| NFR-4 | Delivery rate | ≥ 97% of attempts confirmed delivered. |
| NFR-5 | Data retention | Reminder records purged after 90 days. |
| NFR-6 | Security | PII encrypted at rest; secrets in vault; webhook signature-verified. |

## 3. Architecture

### 3.1 Component overview
| Component | Responsibility | Tech |
|---|---|---|
| Scheduler | Poll HIS, create reminder jobs, enforce idempotency | Go, cron |
| Queue | Buffer reminder jobs | Internal MQ |
| Worker pool | Resolve channel, call vendor adapter, persist result | Go |
| SMS adapter | Wrap SMS gateway API | Go |
| LINE adapter | Wrap LINE Messaging API | Go |
| Status webhook | Ingest vendor delivery receipts | Go, HTTP |
| Store | Reminder + status state | Postgres |

### 3.2 Flow
```
HIS ──pull──> Scheduler ──> Queue ──> Worker ──> {SMS|LINE} adapter ──> Vendor
                                        │                                 │
                                        └──> Postgres <──── webhook ──────┘
```

### 3.3 Deployment
Deployed to the shared K8s cluster. Scheduler as a CronJob; workers and webhook as Deployments
with HPA. Postgres via the managed instance.

## 4. Interfaces

### 4.1 Inbound — Status webhook
`POST /v1/delivery-receipts` — vendor delivery callback. Signature-verified. Body: `{ reminder_id, status, vendor_ref, timestamp }`.

### 4.2 Outbound — HIS
`GET /appointments?status=confirmed&from=&to=` — pull confirmed appointments. Read-only.

### 4.3 Outbound — Vendors
| Vendor | Endpoint | Auth |
|---|---|---|
| SMS gateway | `POST /messages` | API key (vault) |
| LINE | `POST /v2/bot/message/push` | Channel token (vault) |

## 5. Data design

| Table | Key fields | Notes |
|---|---|---|
| `reminder` | `id`, `appointment_id`, `reminder_slot`, `channel`, `status`, `created_at` | Unique on `(appointment_id, reminder_slot)` for idempotency. |
| `delivery_event` | `id`, `reminder_id`, `status`, `vendor_ref`, `received_at` | Append-only audit of receipts. |

PII fields (phone, LINE ID, name) encrypted at rest; purge job removes rows > 90 days old.

## 6. Non-functional design notes
- **Idempotency:** unique key `(appointment_id, reminder_slot)`; scheduler re-runs are safe.
- **Retry/fallback:** exponential backoff on the primary channel; switch to secondary after N failures.
- **Observability:** per-channel sent/delivered/failed metrics; alert if delivery rate < NFR-4.

## 7. Risks and mitigations
| Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|
| LINE rate-limit at 20:00 burst | Delayed reminders | Medium | Spread sends over a window; monitor 429s. |
| HIS poll returns stale data | Wrong/missed reminders | Low | Reconcile against HIS at slot time. |
| Vendor outage | Missed reminders | Medium | Channel fallback + retry queue. |
| PII leak in logs | Compliance breach | Low | Redaction + log review in rollout. |

## 8. Rollout & rollback
Shadow mode (log-only) at one branch → real sends at one branch → branch-by-branch rollout.
Feature-flagged; disabling the flag reverts to the manual process (rollback path).

## 9. Open items
LINE burst limits · ownership of channel-preference data · confirm 90-day retention with compliance.
