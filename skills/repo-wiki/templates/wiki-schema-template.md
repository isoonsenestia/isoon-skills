# WIKI-SCHEMA.md — {Project Name} Repository Knowledge Graph

This file governs how the LLM wiki agent operates in this repository.
Read this file before performing any wiki operation.

## Knowledge Graph Architecture

```
docs/
├── raw/                  ← Source of truth. Immutable. Engineer-validated.
│   ├── api-reference.md
│   ├── architecture.md
│   ├── business-logic.md     (when detected)
│   ├── data-entities.md      (when detected)
│   ├── database.md           (when detected)
│   ├── third-party.md        (when detected)
│   ├── setup.md
│   ├── runbook.md
│   ├── dependencies.md
│   ├── env-and-flags.md
│   └── testing.md
├── wiki/                 ← LLM-owned knowledge graph
│   ├── index.md          ← READ FIRST on every session
│   ├── log.md            ← Append on every action
│   ├── overview.md       ← Repo-level synthesis
│   └── pages/
│       ├── api/              ← API dimension
│       ├── architecture/     ← Architecture dimension
│       ├── business/         ← Business logic dimension
│       ├── data/             ← Data entity dimension
│       ├── database/         ← Database dimension
│       ├── integration/      ← Third-party integration dimension
│       └── cross-cutting/    ← Cross-dimension themes
├── manifest.json         ← Cross-repo graph edges (machine-readable)
├── WIKI-SCHEMA.md        ← This file. Governance.
└── VALIDATION-REPORT.md  ← Confidence ratings
```

**Rules:**
- Never modify files in `/docs/raw/`. They are immutable.
- You own everything in `/docs/wiki/`. Create, update, delete, reorganize.
- Always read `wiki/index.md` first to understand current state.
- Always append to `wiki/log.md` after every operation.
- Keep `manifest.json` in sync with wiki content.

---

## Document Dimensions

This repo has the following active dimensions:
{LIST_ACTIVE_DIMENSIONS}

Each dimension has a dedicated folder in `wiki/pages/` and a corresponding
raw doc in `raw/`. The raw doc is the source of truth; wiki pages synthesize
and cross-reference.

### Dimension Relationships

Pages connect across dimensions through typed graph edges:

| From Dimension | To Dimension | Common Relationships |
|----------------|--------------|---------------------|
| API → Business | `implements`, `triggers` |
| API → Data | `accepts`, `returns` |
| Business → Data | `operates-on`, `transforms` |
| Data → Database | `persisted-by`, `indexed-by` |
| API → Integration | `delegates-to`, `proxies` |
| Business → Integration | `orchestrates`, `depends-on` |

---

## Operations

### Ingest

**When:** Raw docs are updated, code changes land, or the human says "ingest."

**Workflow:**

1. Read `/docs/wiki/index.md` to understand current wiki state
2. Read the changed source(s) — raw docs or code files
3. Identify which dimensions are affected
4. For each affected page:
   - If exists → update with new information
   - If new → create in the appropriate `pages/{dimension}/` folder
5. Insert typed `[[wikilinks]]` with relationship annotations
6. Update `graph_edges` in frontmatter of affected pages
7. If new content **contradicts** existing pages:
   - Flag: `> ⚠️ **Contradiction:** {description}. See [[source]].`
   - Never silently overwrite
8. If exposed APIs, events, or entities changed → update `manifest.json`
9. Update `wiki/index.md`
10. Append to `wiki/log.md`:
    ```
    ## [{date}] ingest | {source description}
    Dimensions affected: {list}
    Pages created: [[page1]], [[page2]]
    Pages updated: [[page3]], [[page4]]
    Graph edges added: {count}
    Contradictions flagged: {count}
    Manifest updated: {yes/no}
    ```

### Query

**When:** Someone asks a question about the codebase.

**Workflow:**

1. Read `wiki/index.md` to find relevant pages
2. Identify which dimensions the question touches
3. Read relevant wiki pages, following `graph_edges` to connected pages
4. Follow `source_refs` to raw docs for authoritative detail
5. For cross-repo questions:
   - Read `docs/manifest.json` for this repo's external dependencies
   - If `docs-registry` is available, read `registry.json` for full graph
   - Note cross-repo links in the answer
6. Synthesize answer with `[[wikilink]]` citations
7. If substantial, offer to file as new wiki page
8. Log in `wiki/log.md`

**Cross-repo query pattern:**
When a question spans services, use manifest.json to trace the path:
```
Q: "How does user authentication flow from login to payment?"
→ Read user-service manifest: exposes POST /auth/login
→ Read payment-service manifest: consumes GET /users/:id
→ Follow graph edges across both repos' wiki pages
→ Synthesize the end-to-end flow
```

### Lint

**When:** The human says "lint", or periodically.

**Workflow:**

1. Scan all wiki pages and check:

   **Content health:**
   - Contradictions between pages
   - Stale claims superseded by newer sources
   - `<!-- TODO: verify -->` markers unresolved
   - Missing coverage in active dimensions

   **Graph health:**
   - Orphan pages (no inbound links)
   - Broken wikilinks (target doesn't exist)
   - Missing typed relationships (edges without relation type)
   - Dangling cross-repo links (manifest references non-existent services)
   - Unidirectional edges (A→B but no B→A awareness)

   **Implementation drift:**
   - Wiki claims vs actual source code
   - Wiki claims vs raw docs
   - Manifest vs actual API surface

   **Dimension coverage:**
   - Active dimensions with thin coverage
   - New code patterns suggesting a new dimension should be activated

2. Report by severity:
   - 🔴 **Critical:** Contradictions, implementation drift, broken graph edges
   - 🟡 **Warning:** Stale content, unresolved TODOs, thin dimensions
   - 🔵 **Info:** Orphans, suggested improvements, new dimension candidates

3. Log findings in `wiki/log.md`

### Sync

**When:** The human says "sync", or after significant wiki updates.

**Workflow:**

1. Validate `manifest.json` reflects current wiki state
2. Push manifest to `docs-registry/repos/{service-name}/`
3. Trigger registry regeneration (or note it for the human to do)
4. Log in `wiki/log.md`

### Auto-Ingest (CI)

**When:** PR merges to main (triggered by CI workflow).

Stricter variant of Ingest:
- Never delete pages or reorganize structure
- Never resolve contradictions — flag only
- Keep changes minimal and focused
- Always update manifest.json if API surface changed
- Include "What changed in the codebase" in log entry
- Flag uncertainty with `<!-- TODO: verify -->`

---

## Page Conventions

### Frontmatter

Every wiki page:

```yaml
---
title: "Page Title"
dimension: api | architecture | business | data | database | integration | cross-cutting
type: endpoint | pattern | flow | entity | table | client | overview | comparison
source_refs: ["raw/api-reference.md#section", "raw/architecture.md"]
tags: [auth, payment, user]
graph_edges:
  - target: "pages/api/auth-endpoints"
    relation: "implements"
  - target: "pages/data/user-entity"
    relation: "uses"
created: {date}
updated: {date}
---
```

### Wikilinks

| Link type | Format | Example |
|-----------|--------|---------|
| Same dimension | `[[pages/api/name]]` | `[[pages/api/auth-endpoints]]` |
| Cross dimension | `[[pages/data/name]]` | `[[pages/data/user-entity]]` |
| With relationship | `[[pages/api/name\|implements]]` | Shows the relationship type |
| To raw source | `[[raw/api-reference#section]]` | `[[raw/api-reference#post-auth]]` |
| Cross-repo | `[[repo-name::pages/api/name]]` | `[[user-service::pages/api/user-endpoints]]` |

**Cross-repo link format:** `[[{repo-name}::pages/{dim}/{page}]]`
These are resolved via manifest.json, not file paths. When rendering in
Obsidian, they appear as external links. When Claude reads them, it knows
to look up the target repo's manifest.

### Writing Style

- Write for developers who are new to this codebase
- Be direct and specific — no filler
- Use code blocks with language identifiers
- Mark uncertainty: `<!-- TODO: verify -->`
- Include concrete examples over abstract descriptions
- Every page should answer: "What is this, why does it exist, how does it connect?"

---

## Index Maintenance

`wiki/index.md` is the content catalog, organized by dimension:

```markdown
# {Service Name} — Knowledge Index

_Updated on every ingest. Read this first._

## Overview
- [[overview]] — Repo-level synthesis ({N} sources, updated: {date})

## API
- [[pages/api/auth-endpoints]] — Authentication endpoints (POST /auth/login, POST /auth/refresh)
- [[pages/api/payment-endpoints]] — Payment CRUD and webhooks

## Architecture
- [[pages/architecture/layer-structure]] — Clean Architecture layers and dependencies
- [[pages/architecture/cqrs-pattern]] — Command/Query separation

## Business Logic
- [[pages/business/payment-lifecycle]] — Payment state machine: created → processing → completed/failed

## Data Entities
- [[pages/data/payment-entity]] — Core Payment model with status enum
- [[pages/data/user-entity]] — User aggregate root

## Database
- [[pages/database/payments-table]] — payments table schema, indexes, constraints

## Third-Party Integrations
- [[pages/integration/stripe-client]] — Stripe SDK usage: PaymentIntents, Webhooks

## Cross-Cutting Themes
- [[pages/cross-cutting/authentication]] — Auth flow spanning API, business, and integration layers

## Raw Sources
- [[raw/api-reference]] — REST API endpoints and contracts
- [[raw/architecture]] — System design and patterns
...
```

---

## Log Maintenance

`wiki/log.md` is chronological, append-only.

```markdown
## [{date}] {operation} | {title}
Dimensions: {affected dimensions}
Pages touched: [[page1]], [[page2]]
Graph edges: +{added} / ~{modified}
```

Parseable with: `grep "^## \[" docs/wiki/log.md | tail -10`

---

## Manifest Maintenance

`manifest.json` is the machine-readable interface for cross-repo linking.
Update it whenever:
- API endpoints are added, removed, or changed
- Events are added or removed
- Exposed entities change
- New cross-repo dependencies are discovered

The manifest is the contract between this repo's wiki and the central
docs-registry. Keep it accurate — stale manifests break cross-repo navigation.

---

## Session Startup

1. Read this file (`docs/WIKI-SCHEMA.md`)
2. Read `docs/wiki/index.md` for current knowledge state
3. Read tail of `docs/wiki/log.md` (last 5 entries)
4. Read `CLAUDE.md` at repo root for project context
5. Orient: what dimensions are active, what's recently changed, what's the graph shape
