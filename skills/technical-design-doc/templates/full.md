# Technical Design: {Title}

| | |
|---|---|
| **Author** | {author} |
| **Reviewers** | {@reviewers} |
| **Status** | **Draft** · In Review · Approved · Superseded |
| **Last updated** | {date} |
| **Related** | {Jira key} · {PRD / other links} |

---

## 1. Context and problem
{Why does this exist? Describe the current situation and what's broken or missing,
with concrete evidence. 1-2 short paragraphs. End with a one-sentence statement of
what this document proposes.}

## 2. Goals
{2-4 bullets. What must be true for this to succeed? Make them specific and, where
possible, measurable (volume, latency, coverage, delivery rate).}

## 3. Non-goals
{What this explicitly does NOT do. Prevents scope creep and sets reviewer
expectations. 2-4 bullets.}

## 4. Proposed design
{The core of the doc. Explain the approach in prose first, then a diagram.}

```
{ASCII architecture / flow diagram — components and how requests/data move between them}
```

{Describe how the pieces fit: entry points, data stores, external systems, deployment
target. Note what existing platform/infra you reuse.}

### Key decisions
{The 3-5 choices that actually matter, each as a bullet: the decision + one line of
why. e.g. idempotency strategy, sync vs async, pull vs push, data model shape.}

## 5. Alternatives considered
{For each serious alternative: name it, one line on the idea, and why it was rejected
(or deferred). This section is mandatory — it's how reviewers trust the recommendation.}

- **{Alternative 1}.** {What it is.} {Why not.}
- **{Alternative 2}.** {What it is.} {Why not.}

## 6. Cross-cutting concerns
{Address each that applies; delete those that don't.}

**Data & privacy.** {What data is handled, PII, encryption, retention/purge.}

**Reliability.** {Retries, fallback, idempotency, behavior on restart/failure.}

**Observability.** {Key metrics, alerts, how to trace one request end-to-end.}

**Security.** {Secrets handling, authn/authz, signature verification, exposure.}

## 7. Rollout plan
{How this ships safely, in order. Prefer shadow/flagged → single scope → gradual
rollout, with the fallback/rollback path stated.}

## 8. Open questions
{Genuine unknowns and decisions still outstanding. Better here and honest than
hidden. Bullet list.}
