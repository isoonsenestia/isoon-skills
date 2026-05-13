# Docs Registry Schema

The `docs-registry` is a dedicated repository that serves as the central
knowledge graph for all documented services. It aggregates manifests from
individual repos and provides cross-repo navigation.

---

## Registry Repository Structure

```
docs-registry/
├── CLAUDE.md                          ← How to operate as registry agent
├── registry.json                      ← Aggregated graph of all services
├── repos/
│   ├── {service-name}/
│   │   └── manifest.json              ← Synced from each repo
│   └── ...
├── graph/
│   ├── service-map.md                 ← Visual topology
│   ├── api-contracts.md               ← All cross-service API calls
│   ├── data-flow.md                   ← How data moves across services
│   ├── shared-entities.md             ← Entities in multiple repos
│   └── dependency-matrix.md           ← Who depends on whom
└── wiki/
    ├── index.md                       ← Cross-repo knowledge index
    ├── log.md                         ← Registry activity log
    └── pages/
        ├── flows/                     ← End-to-end user flows
        ├── entities/                  ← Org-wide entity catalog
        └── analyses/                  ← Cross-cutting analyses
```

---

## registry.json Schema

The master graph file. Rebuilt by aggregating all repo manifests.

```json
{
  "version": "1.0",
  "generated": "2026-04-14T10:00:00Z",
  "repos": {
    "payment-service": {
      "tech_stack": ["typescript", "nestjs", "postgresql"],
      "dimensions": ["api", "architecture", "data", "database", "integration"],
      "manifest_synced": "2026-04-14T09:30:00Z"
    },
    "user-service": {
      "tech_stack": ["typescript", "express", "mongodb"],
      "dimensions": ["api", "architecture", "data", "business"],
      "manifest_synced": "2026-04-13T15:00:00Z"
    }
  },
  "edges": [
    {
      "source_repo": "payment-service",
      "source_page": "pages/integration/user-service-client",
      "target_repo": "user-service",
      "target_page": "pages/api/user-endpoints",
      "relation": "calls",
      "description": "Payment service fetches user data for eligibility check"
    },
    {
      "source_repo": "order-service",
      "source_page": "pages/integration/payment-client",
      "target_repo": "payment-service",
      "target_page": "pages/api/payment-endpoints",
      "relation": "calls",
      "description": "Order service creates payment intents"
    },
    {
      "source_repo": "notification-service",
      "source_page": "pages/business/payment-notifications",
      "target_repo": "payment-service",
      "target_page": "pages/business/payment-lifecycle",
      "relation": "subscribes-to",
      "description": "Notification service listens for payment.completed events"
    }
  ],
  "shared_entities": [
    {
      "entity": "User",
      "repos": [
        {
          "repo": "user-service",
          "page": "pages/data/user-entity",
          "role": "owner"
        },
        {
          "repo": "payment-service",
          "page": "pages/data/user-reference",
          "role": "consumer"
        },
        {
          "repo": "order-service",
          "page": "pages/data/user-reference",
          "role": "consumer"
        }
      ]
    }
  ],
  "events": [
    {
      "event": "payment.completed",
      "producer_repo": "payment-service",
      "producer_page": "pages/business/payment-lifecycle",
      "consumers": [
        {
          "repo": "notification-service",
          "page": "pages/business/payment-notifications"
        },
        {
          "repo": "order-service",
          "page": "pages/business/order-fulfillment"
        }
      ]
    }
  ]
}
```

---

## Per-Repo manifest.json Schema

Each repo publishes this file at `docs/manifest.json`. It is the contract
between the repo's wiki and the central registry.

```json
{
  "$schema": "repo-wiki-manifest-v1",
  "repo": "string — repo name (must match across all references)",
  "version": "string — ISO date of last update",
  "tech_stack": ["string — languages, frameworks"],
  "dimensions": ["string — active dimension names"],

  "exposes": {
    "api": [
      {
        "id": "string — method + path (e.g., 'POST /payments')",
        "page": "string — wiki page path",
        "description": "string — what it does"
      }
    ],
    "events": [
      {
        "id": "string — event name (e.g., 'payment.completed')",
        "page": "string — wiki page documenting this event",
        "description": "string — when it fires"
      }
    ],
    "entities": [
      {
        "id": "string — entity name (e.g., 'Payment')",
        "page": "string — wiki page for this entity",
        "description": "string — what it represents"
      }
    ]
  },

  "consumes": {
    "api": [
      {
        "id": "string — method + path consumed",
        "from_repo": "string — source repo name",
        "page": "string — local wiki page documenting usage"
      }
    ],
    "events": [
      {
        "id": "string — event name consumed",
        "from_repo": "string — repo that produces this event",
        "page": "string — local wiki page documenting handler"
      }
    ]
  },

  "cross_repo_links": [
    {
      "local_page": "string — wiki page in this repo",
      "remote_repo": "string — target repo name",
      "remote_page": "string — wiki page in target repo",
      "relation": "string — relationship type"
    }
  ]
}
```

### Manifest Rules

1. **repo name is canonical.** Must be the same string everywhere — in
   this manifest, in other repos' `consumes.from_repo`, and in the
   registry. Use the GitHub repo name (e.g., `payment-service`).

2. **exposes is exhaustive.** Every public API endpoint, published event,
   and shared entity should be listed. This is how other repos discover
   what you offer.

3. **consumes is honest.** Every external dependency you rely on should
   be declared. This enables the registry to build the full dependency graph.

4. **cross_repo_links are bidirectional in the registry.** When you declare
   a link from your page to another repo's page, the registry creates both
   the forward and reverse edges. You only need to declare your side.

5. **version tracks freshness.** Bump the version date on every sync.
   The registry uses this to detect stale manifests.

---

## Registry CLAUDE.md Template

```markdown
# CLAUDE.md — Docs Registry

## Purpose

This repository is the central knowledge graph for all documented services
in the organization. It aggregates wiki manifests from individual repos and
provides cross-repo navigation, dependency analysis, and organizational
knowledge synthesis.

## How to Navigate

1. Read `registry.json` for the complete service graph
2. Read `graph/service-map.md` for a visual topology
3. For specific service docs, check `repos/{service-name}/manifest.json`
4. For cross-cutting analysis, browse `wiki/pages/`

## Operations

### Sync (primary operation)
When a repo pushes an updated manifest:
1. Copy to `repos/{service-name}/manifest.json`
2. Rebuild `registry.json` from all manifests
3. Update `graph/` pages if topology changed
4. Update `wiki/index.md`
5. Log in `wiki/log.md`

### Analyze
Generate or update cross-repo synthesis:
- End-to-end user flows that span services
- Shared entity consistency checks
- Dependency health (circular deps, single points of failure)
- Coverage gaps (services not yet documented)

### Lint
Check registry health:
- Stale manifests (version older than 30 days)
- Broken cross-repo links (target repo not in registry)
- Orphan repos (documented but no inbound/outbound edges)
- Inconsistent entity definitions across repos

## Services Tracked
{Auto-generated list from registry.json}
```

---

## Graph Pages

### service-map.md
Visual service topology with relationships:
```markdown
# Service Map

## Topology
{Mermaid diagram or ASCII art showing services and connections}

## Services
| Service | Stack | Dimensions | Dependencies | Dependents |
|---------|-------|------------|--------------|------------|
| payment-service | TS/NestJS/PG | 5 | user-svc | order-svc, notif-svc |

## Communication Patterns
- **Synchronous (REST):** {list of service-to-service API calls}
- **Asynchronous (Events):** {list of event flows}
- **Shared Data:** {list of shared entities}
```

### api-contracts.md
All cross-service API dependencies:
```markdown
# Cross-Service API Contracts

## {Consumer} → {Provider}
| Endpoint | Purpose | Contract Page |
|----------|---------|---------------|
| GET /users/:id | Fetch user for payment eligibility | [[user-service::pages/api/user-endpoints]] |
```

### data-flow.md
How data moves through the system:
```markdown
# Data Flow

## {Flow Name: e.g., Order-to-Payment}
1. Order created in order-service → [[order-service::pages/data/order-entity]]
2. Payment intent created → [[payment-service::pages/api/payment-endpoints]]
3. Stripe webhook received → [[payment-service::pages/integration/stripe-client]]
4. payment.completed event → [[notification-service::pages/business/payment-notifications]]
```

### shared-entities.md
Entities that exist across multiple repos:
```markdown
# Shared Entities

## {Entity Name}
- **Owner:** {repo that owns the canonical definition}
- **Consumers:** {repos that reference this entity}
- **Consistency:** {are definitions aligned or divergent?}
- **Canonical page:** [[{owner-repo}::pages/data/{entity}]]
```

### dependency-matrix.md
Service dependency matrix:
```markdown
# Dependency Matrix

|  | user-svc | payment-svc | order-svc | notif-svc |
|--|----------|-------------|-----------|-----------|
| **user-svc** | — | | | |
| **payment-svc** | REST(3) | — | | Events(1) |
| **order-svc** | REST(1) | REST(2) | — | |
| **notif-svc** | | Events(2) | Events(1) | — |

Rows = consumer, Columns = provider. Numbers = count of dependencies.
```
