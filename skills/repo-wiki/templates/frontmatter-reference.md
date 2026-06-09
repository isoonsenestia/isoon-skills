# Frontmatter Reference — Repo Wiki Pages

Every wiki page in `/docs/wiki/pages/` must have YAML frontmatter. The schema
varies by dimension and page type.

---

## Common Fields (all pages)

```yaml
---
title: "Human-readable title"
dimension: api | architecture | business | data | database | integration | cross-cutting
type: {dimension-specific type}
source_refs: ["raw/api-reference.md#section-anchor"]
tags: [auth, payment, user, stripe]
graph_edges:
  - "pages/dimension/page-name|relationship-type"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

### Field Rules

- **title**: Plain text, no wikilinks
- **dimension**: Must match the folder the page lives in
- **type**: Dimension-specific (see below)
- **source_refs**: Array of raw doc paths, optionally with `#section` anchors
- **tags**: Lowercase, hyphenated. Used for cross-cutting discovery.
- **graph_edges**: Array of typed connections to other pages. Each entry is a single string in the form `"target|relation"` where:
  - `target`: Relative path from `wiki/` (e.g., `pages/api/auth-endpoints`)
  - `relation`: Describes the nature of the connection (see Relationship Types)
  - String-encoded (not object-encoded) so Obsidian's properties panel renders it as a proper multi-text list rather than collapsed JSON. The `|` separator mirrors the typed-wikilink syntax `[[page|relation]]` used in body prose.
- **created/updated**: ISO dates, updated on every edit

---

## Dimension-Specific Types

### API Dimension
```yaml
dimension: api
type: endpoint-group | middleware | error-handling | versioning
# Additional fields:
methods: [GET, POST, PUT, DELETE]
base_path: "/api/v1/payments"
auth_required: true
```

### Architecture Dimension
```yaml
dimension: architecture
type: layer | pattern | decision | overview
# Additional fields:
pattern: "clean-architecture" | "mvc" | "cqrs" | "event-driven" | etc.
```

### Business Dimension
```yaml
dimension: business
type: use-case | flow | state-machine | domain-event | business-rule
# Additional fields:
actors: ["user", "admin", "system"]
```

### Data Dimension
```yaml
dimension: data
type: entity | value-object | dto | enum | aggregate
# Additional fields:
orm: "typeorm" | "prisma" | "sequelize" | "gorm" | etc.
source_file: "src/entities/payment.entity.ts"
```

### Database Dimension
```yaml
dimension: database
type: table | view | index | migration-summary | query-pattern
# Additional fields:
database_type: "postgresql" | "mongodb" | "mysql" | "redis"
```

### Integration Dimension
```yaml
dimension: integration
type: api-client | sdk | webhook-handler | event-consumer | event-producer
# Additional fields:
provider: "stripe" | "sendgrid" | "aws-s3" | etc.
protocol: "rest" | "grpc" | "graphql" | "websocket" | "event"
```

### Cross-Cutting
```yaml
dimension: cross-cutting
type: theme | comparison | analysis | guide
# Additional fields:
dimensions_spanned: [api, business, integration]
```

---

## Relationship Types

Use these standard relation types in `graph_edges`:

### Structural Relations
| Relation | Meaning | Example |
|----------|---------|---------|
| `contains` | Parent contains child | Layer → module |
| `part-of` | Child belongs to parent | Module → layer |
| `depends-on` | Requires the target to function | Service → database |

### Behavioral Relations
| Relation | Meaning | Example |
|----------|---------|---------|
| `implements` | Realizes a business flow | API endpoint → use case |
| `triggers` | Causes the target to execute | Webhook → event handler |
| `calls` | Makes a synchronous call | API → third-party client |
| `produces` | Emits an event | Service → domain event |
| `consumes` | Handles an event | Handler → domain event |
| `orchestrates` | Coordinates multiple targets | Flow → multiple services |

### Data Relations
| Relation | Meaning | Example |
|----------|---------|---------|
| `accepts` | Takes this as input | Endpoint → DTO |
| `returns` | Outputs this | Endpoint → response DTO |
| `operates-on` | Reads/writes this entity | Use case → entity |
| `persisted-by` | Stored in this table | Entity → database table |
| `transforms` | Converts between representations | Mapper → entity + DTO |
| `validates` | Applies validation rules | Guard → DTO |

### Cross-Repo Relations
| Relation | Meaning | Example |
|----------|---------|---------|
| `calls` | Cross-service API call | Payment → User service |
| `subscribes-to` | Listens to events from | Notification → Payment events |
| `publishes-to` | Sends events consumed by | Payment → event bus |
| `shared-entity` | Same concept in both repos | User in auth-svc and user-svc |

---

## Naming Conventions

- **File names:** lowercase, hyphenated slugs (`auth-endpoints.md`, `payment-entity.md`)
- **No spaces** in filenames
- **Dimension prefix not needed** in filename (the folder provides context)
- **Cross-cutting pages** should describe the theme, not the dimensions
  (e.g., `authentication.md` not `api-business-auth.md`)
