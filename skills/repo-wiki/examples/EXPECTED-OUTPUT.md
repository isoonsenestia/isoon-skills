# Expected Output — repo-wiki

After a `full` run on a typical TypeScript/NestJS backend service, expect:

## Files Generated

### Raw Docs (`/docs/raw/`)
| File | Generated When | Approx Size |
|------|---------------|-------------|
| `setup.md` | Always | 100-200 lines |
| `architecture.md` | Always | 150-300 lines |
| `api-reference.md` | Always | 200-500 lines (depends on endpoint count) |
| `runbook.md` | Always | 80-150 lines |
| `dependencies.md` | Always | 50-200 lines (depends on package count) |
| `env-and-flags.md` | Always | 30-100 lines |
| `business-logic.md` | When detected | 150-400 lines |
| `data-entities.md` | When detected | 100-300 lines |
| `database.md` | When detected | 100-250 lines |
| `third-party.md` | When detected | 80-200 lines |
| `testing.md` | When detected | 60-150 lines |

### Wiki Pages (`/docs/wiki/pages/`)
Expect 15-40 wiki pages depending on service complexity:

| Dimension | Typical Page Count | Examples |
|-----------|-------------------|----------|
| `api/` | 3-8 | One page per endpoint group |
| `architecture/` | 2-5 | Layer structure, patterns, decisions |
| `business/` | 2-6 | Use cases, state machines, event flows |
| `data/` | 3-10 | One page per entity/aggregate |
| `database/` | 2-6 | Tables, migrations, query patterns |
| `integration/` | 1-4 | One page per external service |
| `cross-cutting/` | 1-3 | Auth, error handling, logging |

### Governance Files
| File | Location |
|------|----------|
| `CLAUDE.md` | Repo root |
| `WIKI-SCHEMA.md` | `/docs/` |
| `manifest.json` | `/docs/` |
| `VALIDATION-REPORT.md` | `/docs/` |

### Wiki Infrastructure
| File | Location |
|------|----------|
| `index.md` | `/docs/wiki/` |
| `log.md` | `/docs/wiki/` |
| `overview.md` | `/docs/wiki/` |
| `.obsidian/` | `/docs/wiki/` (when Obsidian enabled) |

## Quality Indicators

A good run should produce:

- **Validation Report:** 60%+ 🟢 HIGH confidence ratings
- **Graph Density:** Every wiki page has at least 2 `graph_edges`
- **Cross-Dimension Links:** Each dimension links to at least 1 other dimension
- **Index Coverage:** Every wiki page appears in `index.md`
- **Manifest Completeness:** All public endpoints listed in `exposes.api`
- **No Orphans:** Zero wiki pages with no inbound links (check via Obsidian graph)

## Timing

| Phase | Expected Duration |
|-------|------------------|
| 1. Scan | 1-2 min |
| 2. Raw Docs | 3-5 min |
| 3. Governance | 1-2 min |
| 4. Wiki Gen | 3-5 min |
| 5. Validation | 2-4 min |
| 6. Summary | <30 sec |
| **Total** | **10-18 min** |
