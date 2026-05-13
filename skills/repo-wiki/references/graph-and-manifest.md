# Knowledge Graph & manifest.json

How pages connect inside a repo and across repos.

## Within a repo: typed wikilinks

```markdown
<!-- Standard link -->
[[pages/api/auth-endpoints]]

<!-- Typed relationship -->
[[pages/api/auth-endpoints|implements]] → [[pages/business/login-flow]]
[[pages/data/user-entity|persisted-by]]  → [[pages/database/users-table]]
[[pages/integration/stripe-client|consumed-by]] → [[pages/api/payment-endpoints]]
```

Every page's frontmatter declares its outgoing edges:

```yaml
graph_edges:
  - target: "pages/api/auth-endpoints"
    relation: "implements"
  - target: "pages/data/user-entity"
    relation: "uses"
  - target: "pages/database/users-table"
    relation: "persisted-by"
```

**Rule:** every link expresses a relationship (`implements`, `uses`, `persisted-by`, `calls`, etc.). No untyped edges.

## Across repos: `docs/manifest.json`

Each repo publishes a manifest describing what it exposes and consumes:

```json
{
  "repo": "payment-service",
  "version": "2026-04-14",
  "tech_stack": ["typescript", "nestjs", "postgresql"],
  "dimensions": ["api", "architecture", "data", "database", "integration"],
  "exposes": {
    "api": [
      {
        "id": "POST /payments",
        "page": "pages/api/create-payment",
        "description": "Create a new payment intent"
      }
    ],
    "events": [
      {
        "id": "payment.completed",
        "page": "pages/business/payment-lifecycle",
        "description": "Emitted when payment succeeds"
      }
    ],
    "entities": [
      {
        "id": "Payment",
        "page": "pages/data/payment-entity",
        "description": "Core payment domain model"
      }
    ]
  },
  "consumes": {
    "api": [
      {
        "id": "GET /users/:id",
        "from_repo": "user-service",
        "page": "pages/integration/user-service-client"
      }
    ],
    "events": [
      {
        "id": "user.verified",
        "from_repo": "user-service",
        "page": "pages/business/payment-eligibility"
      }
    ]
  },
  "cross_repo_links": [
    {
      "local_page": "pages/integration/user-service-client",
      "remote_repo": "user-service",
      "remote_page": "pages/api/user-endpoints",
      "relation": "calls"
    }
  ]
}
```

The central `docs-registry` aggregates every repo's manifest into `registry.json` — a complete graph of the ecosystem. See `references/registry-schema.md` for the central-registry layout.

**Rule:** never hard-code paths to other repos. Always reference via manifest entries so links survive repo moves.
