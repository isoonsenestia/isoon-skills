# Raw Document Templates

Each raw doc in `/docs/raw/` follows a specific structure depending on its type.
These templates define the expected format. All raw docs are immutable after
engineer validation — the wiki layer handles synthesis and cross-referencing.

---

## Core Documents (always generated)

### api-reference.md

```markdown
---
title: "API Reference — {Service Name}"
type: raw-api
generated: {date}
scanner_confidence: {high|medium|low}
---

# API Reference

## Base URL
{base-url or route prefix}

## Authentication
{auth mechanism: JWT Bearer, API Key, OAuth2, none}

## Endpoints

### {GROUP: e.g., Authentication}

#### {METHOD} {PATH}
- **Description:** {what it does}
- **Auth:** {required/optional/none}
- **Request:**
  ```json
  {request body schema}
  ```
- **Response (200):**
  ```json
  {response schema}
  ```
- **Error Codes:**
  | Status | Code | Description |
  |--------|------|-------------|
  | 400 | INVALID_INPUT | {description} |

{Repeat for each endpoint}

## Middleware
{List middleware applied globally or per-route group}

## Rate Limits
{Rate limiting configuration if detected}

## Versioning
{API versioning strategy if detected}
```

### architecture.md

```markdown
---
title: "Architecture — {Service Name}"
type: raw-architecture
generated: {date}
scanner_confidence: {high|medium|low}
---

# Architecture

## Overview
{2-3 sentence architectural summary}

## Layers
{Describe each architectural layer, its responsibility, and dependencies}

### {Layer Name}
- **Responsibility:** {what this layer does}
- **Directory:** `{path}`
- **Depends on:** {other layers}
- **Key files:**
  - `{file}` — {what it does}

## Control Flow
{How a typical request flows through the layers}

## Key Design Decisions
- {Decision 1 and rationale}
- {Decision 2 and rationale}

## Patterns Used
- {Pattern: e.g., Repository Pattern, CQRS, Event Sourcing}
  - **Where:** {where it's applied}
  - **Why:** {rationale}
```

### setup.md

```markdown
---
title: "Setup — {Service Name}"
type: raw-setup
generated: {date}
scanner_confidence: {high|medium|low}
---

# Development Setup

## Prerequisites
- {requirement 1: e.g., Node.js >= 20}
- {requirement 2: e.g., Docker for local database}

## Installation
```bash
{step-by-step commands}
```

## Configuration
{How to set up .env, config files, etc.}

## Running Locally
```bash
{command to start the service}
```

## Common Tasks
| Task | Command |
|------|---------|
| {task} | `{command}` |
```

### runbook.md

```markdown
---
title: "Runbook — {Service Name}"
type: raw-runbook
generated: {date}
scanner_confidence: {high|medium|low}
---

# Operational Runbook

## Deployment
{How to deploy: CI/CD pipeline, manual steps, environments}

## Health Checks
{Health check endpoints, expected responses}

## Monitoring
{Logging, metrics, alerting configuration}

## Incident Response
{Common failure modes and how to diagnose/fix them}

## Rollback
{How to roll back a deployment}
```

### dependencies.md

```markdown
---
title: "Dependencies — {Service Name}"
type: raw-dependencies
generated: {date}
scanner_confidence: {high|medium|low}
---

# Dependencies

## Runtime Dependencies
| Package | Version | Purpose | Category |
|---------|---------|---------|----------|
| {package} | {version} | {why it's used} | {framework/database/auth/http/etc.} |

## Dev Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| {package} | {version} | {why it's used} |

## System Dependencies
- {e.g., PostgreSQL 15+, Redis 7+, Docker}
```

### env-and-flags.md

```markdown
---
title: "Environment & Feature Flags — {Service Name}"
type: raw-env
generated: {date}
scanner_confidence: {high|medium|low}
---

# Environment Variables & Feature Flags

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `{VAR}` | {yes/no} | {value or —} | {description} |

## Feature Flags
| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `{FLAG}` | {boolean/string/number} | {default} | {what it controls} |

## Configuration Files
{List of config files and their purposes}
```

---

## Detected Dimension Documents

### business-logic.md (when business logic detected)

```markdown
---
title: "Business Logic — {Service Name}"
type: raw-business
generated: {date}
scanner_confidence: {high|medium|low}
---

# Business Logic

## Domain Overview
{What business domain this service operates in}

## Use Cases

### {Use Case Name}
- **Actor:** {who triggers this}
- **Trigger:** {what starts it}
- **Flow:**
  1. {step 1}
  2. {step 2}
- **Outcomes:** {success/failure scenarios}
- **Business Rules:**
  - {rule 1}
  - {rule 2}

## State Machines

### {Entity} States
```
{state diagram in text or mermaid}
```
- **Transitions:**
  | From | To | Trigger | Guard |
  |------|----|---------|-------|
  | {state} | {state} | {event} | {condition} |

## Domain Events
| Event | Triggered By | Payload | Consumers |
|-------|-------------|---------|-----------|
| {event} | {action} | {schema} | {services} |
```

### data-entities.md (when domain models detected)

```markdown
---
title: "Data Entities — {Service Name}"
type: raw-data
generated: {date}
scanner_confidence: {high|medium|low}
---

# Data Entities

## Entity Map
{High-level entity relationship description}

## Entities

### {Entity Name}
- **Source:** `{file path}`
- **Type:** {aggregate root | entity | value object | DTO}
- **Fields:**
  | Field | Type | Required | Description |
  |-------|------|----------|-------------|
  | {field} | {type} | {yes/no} | {description} |
- **Relationships:**
  | Target | Type | Description |
  |--------|------|-------------|
  | {entity} | {has-many/belongs-to/has-one} | {description} |
- **Validations:**
  - {validation rule}
- **Transformations:**
  - {DTO mapping or serialization logic}
```

### database.md (when database layer detected)

```markdown
---
title: "Database — {Service Name}"
type: raw-database
generated: {date}
scanner_confidence: {high|medium|low}
---

# Database

## Connection
- **Type:** {PostgreSQL/MongoDB/MySQL/etc.}
- **Config:** `{config file path}`

## Schema

### {Table/Collection Name}
- **Source:** `{migration or schema file}`
- **Columns/Fields:**
  | Column | Type | Constraints | Description |
  |--------|------|-------------|-------------|
  | {col} | {type} | {PK/FK/UNIQUE/NOT NULL} | {description} |
- **Indexes:**
  | Name | Columns | Type | Purpose |
  |------|---------|------|---------|
  | {idx} | {cols} | {btree/gin/etc.} | {why} |
- **Foreign Keys:**
  | Column | References | On Delete |
  |--------|-----------|-----------|
  | {col} | {table.col} | {CASCADE/SET NULL/etc.} |

## Migrations
| Migration | Date | Description |
|-----------|------|-------------|
| {file} | {date} | {what it does} |

## Queries & Patterns
{Notable query patterns, views, stored procedures}
```

### third-party.md (when external integrations detected)

```markdown
---
title: "Third-Party Integrations — {Service Name}"
type: raw-integration
generated: {date}
scanner_confidence: {high|medium|low}
---

# Third-Party Integrations

## {Service Name: e.g., Stripe}
- **SDK/Client:** `{package name}` v{version}
- **Purpose:** {what it's used for}
- **Configuration:** `{config file or env vars}`
- **Endpoints Used:**
  | Operation | API Call | Description |
  |-----------|----------|-------------|
  | {op} | {method + path} | {what it does} |
- **Authentication:** {API key / OAuth / etc.}
- **Webhook Handling:**
  - Endpoint: `{path}`
  - Events: {list of handled events}
- **Error Handling:** {retry policy, circuit breaker, fallback}
- **Rate Limits:** {known limits}

{Repeat for each third-party service}
```

### testing.md (when test infrastructure detected)

```markdown
---
title: "Testing — {Service Name}"
type: raw-testing
generated: {date}
scanner_confidence: {high|medium|low}
---

# Testing

## Strategy
{Overview of testing approach: unit, integration, e2e}

## Running Tests
```bash
{test commands}
```

## Test Structure
| Type | Location | Framework | Count |
|------|----------|-----------|-------|
| {unit/integration/e2e} | `{path}` | {Jest/Vitest/Go test/pytest} | {approx count} |

## Fixtures & Factories
{How test data is managed}

## CI Pipeline
{How tests run in CI}
```

---

## Template Notes for the Scanner

- Fill in what you can verify from code. Leave blanks or `<!-- TODO: verify -->`
  for anything uncertain.
- The `scanner_confidence` field in frontmatter reflects overall document confidence.
- Individual uncertain claims should be marked inline with `<!-- TODO: verify -->`.
- These templates are guidelines, not rigid structures. Adapt sections to fit
  what the code actually contains. Remove sections that have no content rather
  than leaving empty sections.
