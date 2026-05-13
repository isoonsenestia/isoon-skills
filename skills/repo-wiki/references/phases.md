# Phase Pipeline

Six phases, run sequentially for `full` scope. Each phase prints `--- Phase N/6: {name} ---` markers and writes `.wiki-gen-progress.json` at repo root for resume.

## Phase 1: Repository Scan

Build a complete understanding before generating anything.

**1.1 Project detection** — Scan `package.json`, `go.mod`, `pom.xml`, `Cargo.toml`, `requirements.txt`, `Dockerfile`, `docker-compose.yml`, `Makefile`. Determine language, framework, build system, runtime.

**1.2 Architecture detection** — Scan directory structure, entry points, route definitions, middleware chains, dependency injection, layer boundaries. Determine architectural pattern (MVC, Clean Architecture, microservice, monolith).

**1.3 Dimension detection** — For each of the 6 dimensions, scan for the indicators in `references/dimensions.md`. Record which dimensions have meaningful content.

**1.4 Cross-repo detection** — Scan for HTTP clients to internal services, event subscriptions, shared package imports, service discovery config, API gateway routes. Record every external dependency with the target service name.

**1.5 Scan report** — Present findings to the developer. Sample:

```
--- Phase 1/6: Repository Scan ---
Project: payment-service (TypeScript / NestJS / PostgreSQL)
Architecture: Clean Architecture with CQRS

Dimensions detected:
  ✓ API           — 24 endpoints across 6 controllers
  ✓ Architecture  — 4-layer structure with clear boundaries
  ✓ Business      — 8 command handlers, 3 state machines
  ✓ Data Entities — 12 TypeORM entities
  ✓ Database      — 18 migrations, 3 views
  ✓ Third-Party   — Stripe SDK, SendGrid, user-service client

Cross-repo dependencies:
  → user-service (REST API: 3 endpoints)
  → notification-service (Event: payment.completed)
  ← order-service (consumes POST /payments)

Proceed with full generation? [Y/n]
```

## Phase 2: Raw Document Generation

For each detected dimension, generate the corresponding raw doc in `/docs/raw/`.

- **Implementation-first:** document what the code does, not what design docs say.
- **Conservative:** state only what you can verify from code. Mark uncertainty with `<!-- TODO: verify -->`.
- **Structured:** use the frontmatter templates from `templates/raw-doc-templates.md`.
- **Cross-referenced but not wikilinked:** note connections; the wiki layer handles links.

Always generate: `setup.md`, `architecture.md`, `api-reference.md`, `runbook.md`, `dependencies.md`, `env-and-flags.md`.

Conditionally generate (when dimension detected): `business-logic.md`, `data-entities.md`, `database.md`, `third-party.md`, `testing.md`.

## Phase 3: Governance Files

Generate files that teach future Claude sessions how to operate.

- **`CLAUDE.md`** at repo root — from `templates/claude-md-template.md`. Includes a `## Wiki` section pointing to `/docs/wiki/`.
- **`docs/WIKI-SCHEMA.md`** — from `templates/wiki-schema-template.md`, customized for detected dimensions.
- **`docs/manifest.json`** — built from scan results. Schema in `references/graph-and-manifest.md`.

## Phase 4: Wiki Generation

Ingest each raw doc into the wiki layer:

1. Create dimension-specific pages in `pages/{dim}/`.
2. Extract entities, concepts, relationships.
3. Insert typed `[[wikilinks]]` with relationship annotations.
4. Populate `graph_edges` in frontmatter.
5. Update `index.md` (organized by dimension).
6. Log every action in `log.md`.

After all individual pages: generate `overview.md`, create `pages/cross-cutting/` for themes spanning dimensions (e.g., "authentication" touches API, business, integration), verify all wikilinks resolve.

## Phase 5: Validation

For each claim in each raw doc, verify against implementation. Rate confidence:

- 🟢 **HIGH** — verified
- 🟡 **MEDIUM** — inferred
- 🔴 **LOW** — unverified

Write `VALIDATION-REPORT.md`. Insert `<!-- TODO: verify -->` markers in docs where confidence is low.

## Phase 6: Summary & Next Steps

Report to developer:

- Dimensions generated and page counts
- Confidence breakdown (🟢/🟡/🔴 percentages)
- Cross-repo dependencies found
- Suggested actions: review raw docs against code, run `sync` to push manifest, run `lint` after engineers review
