---
title: "Clean Architecture Layers"
dimension: architecture
type: layer
source_refs: ["raw/architecture.md#layers"]
tags: [clean-architecture, layers, dependency-rule]
pattern: "clean-architecture"
graph_edges:
  - target: "pages/architecture/cqrs-pattern"
    relation: "contains"
  - target: "pages/architecture/dependency-injection"
    relation: "depends-on"
  - target: "pages/api/auth-endpoints"
    relation: "contains"
  - target: "pages/api/payment-endpoints"
    relation: "contains"
  - target: "pages/data/payment-entity"
    relation: "contains"
  - target: "pages/database/typeorm-config"
    relation: "contains"
created: 2026-04-14
updated: 2026-04-14
---

# Clean Architecture Layers

The service follows Clean Architecture with four layers. Dependencies point
inward — outer layers depend on inner layers, never the reverse.

```
┌─────────────────────────────────────────────┐
│  Infrastructure (src/infrastructure/)        │
│  ├── Controllers, Guards, Interceptors       │
│  ├── TypeORM repositories                    │
│  ├── External API clients                    │
│  └── Config, logging, middleware             │
├─────────────────────────────────────────────┤
│  Application (src/application/)              │
│  ├── Command handlers (CQRS)                 │
│  ├── Query handlers                          │
│  ├── DTOs and validation                     │
│  └── Orchestration / use case logic          │
├─────────────────────────────────────────────┤
│  Domain (src/domain/)                        │
│  ├── Entities and value objects               │
│  ├── Domain events                           │
│  ├── Repository interfaces (ports)           │
│  └── Business rules and invariants           │
├─────────────────────────────────────────────┤
│  Shared (src/shared/)                        │
│  ├── Base classes, interfaces                │
│  ├── Common utilities                        │
│  └── Constants and enums                     │
└─────────────────────────────────────────────┘
```

## Layer Details

### Infrastructure Layer (`src/infrastructure/`)

The outermost layer. Handles HTTP, database connections, and external services.
This is the only layer that knows about NestJS decorators, TypeORM, and
third-party SDKs.

**Key directories:**
- `controllers/` — NestJS controllers defining HTTP routes → [[pages/api/auth-endpoints]], [[pages/api/payment-endpoints]]
- `repositories/` — TypeORM repository implementations → [[pages/database/typeorm-config]]
- `clients/` — HTTP clients for external services → [[pages/integration/stripe-client]], [[pages/integration/user-service-client]]
- `guards/` — Auth guards and rate limiters
- `interceptors/` — Logging, error transformation

**Depends on:** Application, Domain, Shared

### Application Layer (`src/application/`)

Orchestrates use cases. Contains command and query handlers that implement
[[pages/architecture/cqrs-pattern|CQRS]]. No framework imports — pure
TypeScript with dependency injection.

**Key directories:**
- `commands/` — Write operations (CreatePayment, RefundPayment)
- `queries/` — Read operations (GetPayment, ListPayments)
- `dtos/` — Input validation and output shaping → [[pages/data/payment-dto]]
- `services/` — Cross-cutting application services

**Depends on:** Domain, Shared

### Domain Layer (`src/domain/`)

The core. Contains entities, value objects, and business rules. Zero
external dependencies — not even NestJS or TypeORM.

**Key directories:**
- `entities/` — Domain models → [[pages/data/payment-entity]], [[pages/data/user-entity]]
- `events/` — Domain events → [[pages/business/payment-lifecycle]]
- `ports/` — Repository interfaces (implemented by Infrastructure)
- `rules/` — Business invariants and validations

**Depends on:** Shared only

### Shared Layer (`src/shared/`)

Base classes and utilities used across all layers. Must have no layer-specific
dependencies.

**Key contents:**
- `Result<T>` — Result monad for error handling without exceptions
- `BaseEntity` — Abstract entity with `id`, `createdAt`, `updatedAt`
- `DomainEvent` — Base class for domain events

**Depends on:** Nothing

## Request Flow (typical)

A typical API request flows through the layers like this:

```
HTTP Request
  → Controller (Infrastructure)
    → validates input, creates DTO
    → dispatches Command or Query
  → Command Handler (Application)
    → loads entity via repository interface (port)
    → calls domain methods
    → persists via repository interface
    → publishes domain events
  → Repository (Infrastructure)
    → maps entity to TypeORM entity
    → executes SQL via TypeORM
  → Response mapped back through layers
```

This flow touches multiple dimensions:
- **API**: [[pages/api/payment-endpoints]] (controller)
- **Business**: [[pages/business/payment-lifecycle]] (command handler logic)
- **Data**: [[pages/data/payment-entity]] (domain entity)
- **Database**: [[pages/database/payments-table]] (persistence)

## Key Design Decisions

1. **Ports & Adapters** — Domain defines repository interfaces; Infrastructure
   implements them. This allows swapping database or external services without
   touching business logic.

2. **CQRS** — Commands and queries are separated at the application layer.
   See [[pages/architecture/cqrs-pattern]] for details. Commands return
   `Result<void>`, queries return `Result<DTO>`.

3. **Domain Events** — State changes in entities emit events that other
   parts of the system can react to. Events are dispatched after successful
   persistence (not during entity method calls) to avoid partial state issues.

4. **No ORM in Domain** — Entity classes in `src/domain/entities/` are plain
   TypeScript. TypeORM decorators live on separate "persistence models" in
   `src/infrastructure/repositories/models/`. A mapper converts between them.

## Cross-Repo Pattern

Other services in the organization follow the same architecture with minor
variations. This consistency means:
- [[user-service::pages/architecture/layer-structure]] — Same 4-layer pattern
- [[order-service::pages/architecture/layer-structure]] — Same pattern + Saga orchestration
- Cross-service developers can navigate any repo using the same mental model
<!-- cross-repo: actual implementations may vary -->
