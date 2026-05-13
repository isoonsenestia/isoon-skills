# Document Dimensions

The knowledge base organizes content across six dimensions. Each has its own page subdirectory, frontmatter schema, and scanning strategy.

## Core dimensions (always generated)

### 1. API — `pages/api/`

What the service exposes and consumes. Endpoints, request/response schemas, authentication, rate limits, error codes, versioning.

### 2. Architecture — `pages/architecture/`

How the service is built. Layers, patterns, key abstractions, control flow, design decisions, trade-offs.

## Detected dimensions (generated only when content is found)

### 3. Business Logic — `pages/business/`

What the service does from a product perspective. Use cases, user flows, domain rules, state machines, business events.

**Detect:** service handlers, controllers with business logic, domain models, workflow definitions.

### 4. Data Entities — `pages/data/`

The domain model. Entities, value objects, DTOs, relationships, validations, transformations.

**Detect:** model/entity definitions, TypeORM / Prisma / Sequelize schemas, Pydantic models, protobuf, GraphQL types.

### 5. Database — `pages/database/`

Persistence layer. Schema design, migrations, indexes, queries, connection config, caching strategy.

**Detect:** migration files, schema definitions, ORM config, SQL files.

### 6. Third-Party Integrations — `pages/integration/`

External dependencies. API clients, SDKs, webhooks, OAuth flows, retry policies, circuit breakers.

**Detect:** HTTP client configurations, SDK imports, webhook handlers, external API calls.

## Rule

**Dimensions are earned.** Only generate a dimension folder when meaningful content exists. An empty dimension is worse than no dimension — it clutters the knowledge graph.
