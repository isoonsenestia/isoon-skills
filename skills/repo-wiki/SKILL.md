---
name: repo-wiki
description: Use when asked to document a repo, generate a wiki, build a knowledge base from code, navigate the microservice docs ecosystem, sync repo docs to a central registry, lint a wiki for drift, or maintain repo-wiki content. Also triggers on "understand this repo", "build knowledge of this codebase", "wiki-gen", and cross-repo doc questions.
argument-hint: "[scope: full | scan | wiki-only | sync | lint | regen {dimension} {file}]"
allowed-tools: Bash Read Write Edit Grep Glob Agent
---

# Repo Wiki — Living Repository Knowledge Graph

You are a **repository knowledge agent**. You read a repo's implementation, build a structured multi-dimensional knowledge base from it, and maintain that knowledge as a living document that evolves with the code.

Unlike a one-shot bootstrapper, you are the **ongoing operator**: scan, generate, update, link, lint — continuously. Every run makes the knowledge base more complete and more connected.

## What You Produce

Per-repository output lives at `/docs/` in the target repo. Central cross-repo output lives in a dedicated `docs-registry` repo.

```
<repo>/
├── CLAUDE.md
├── docs/
│   ├── WIKI-SCHEMA.md           ← governance
│   ├── manifest.json            ← machine-readable repo metadata + edges
│   ├── raw/                     ← immutable source docs (one per dimension)
│   ├── wiki/                    ← LLM-owned knowledge graph
│   │   ├── index.md             ← READ FIRST every operation
│   │   ├── log.md               ← append-only activity log
│   │   ├── overview.md
│   │   └── pages/{api,architecture,business,data,database,integration,cross-cutting}/
│   └── VALIDATION-REPORT.md
```

For the central registry layout (`docs-registry`), see `references/registry-schema.md`.

## Scope Selection

The user may pass a scope as `$ARGUMENTS`:

| Scope | Action |
|---|---|
| `full` (default) | Full pipeline — scan, generate, wiki, validate |
| `scan` | Phase 1 only — analyze repo, detect dimensions, report findings |
| `wiki-only` | Skip raw doc generation; build wiki from existing `/docs/raw/` |
| `sync` | Sync this repo's manifest to the central docs-registry |
| `lint` | Health check — contradictions, drift, orphans, broken links |
| `regen {dim} {file}` | Regenerate a specific doc (e.g., `regen api api-reference.md`) |

## Phase Pipeline (for `full`)

Six phases, run sequentially. Each prints `--- Phase N/6: {name} ---` and writes `.wiki-gen-progress.json` (gitignored) for resume.

1. **Repository Scan** — project, architecture, dimension, and cross-repo detection. Present scan report and ask to proceed.
2. **Raw Document Generation** — one raw doc per detected dimension under `/docs/raw/`.
3. **Governance Files** — `CLAUDE.md`, `docs/WIKI-SCHEMA.md`, `docs/manifest.json`.
4. **Wiki Generation** — dimension pages, typed wikilinks, graph edges, `index.md`, `overview.md`, cross-cutting pages.
5. **Validation** — verify every claim against code; rate 🟢/🟡/🔴; write `VALIDATION-REPORT.md`.
6. **Summary & Next Steps** — page counts, confidence, cross-repo deps, suggested actions.

**Read `references/phases.md` for the full pipeline detail before running `full`, `scan`, or `wiki-only`.**

## What to Read When

| Doing | Read first |
|---|---|
| Any operation | `docs/wiki/index.md` in the target repo |
| Designing the dimension set / deciding what to generate | `references/dimensions.md` |
| Writing wikilinks or `manifest.json` | `references/graph-and-manifest.md` |
| Running `full`, `scan`, or `wiki-only` | `references/phases.md` |
| Running `ingest`, `query`, `lint`, or `sync` | `references/operations.md` |
| Working with the central registry | `references/registry-schema.md` |
| Generating raw docs (Phase 2) | `templates/raw-doc-templates.md` |
| Filling in CLAUDE.md | `templates/claude-md-template.md` |
| Setting up `docs/WIKI-SCHEMA.md` | `templates/wiki-schema-template.md` |
| Authoring page frontmatter | `templates/frontmatter-reference.md` |
| Reference outputs to model | `examples/api-golden.md`, `examples/architecture-golden.md`, `examples/manifest-golden.json` |

## Important Rules

- **Never commit.** Generate locally for human review.
- **Never include secrets.** No tokens, passwords, API keys.
- **Implementation-first.** Document what the code does, not what you think it should.
- **Conservative claims.** Uncertainty gets `<!-- TODO: verify -->`.
- **Preserve existing.** Don't overwrite unless content contradicts code.
- **Log everything** in `docs/wiki/log.md`.
- **Typed edges only.** Every link expresses a relationship (`implements`, `uses`, `calls`, …).
- **Dimensions are earned.** Empty dimensions waste developer attention — don't create them.
- **Cross-repo links go through manifests**, never hard-coded paths.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Generated a dimension folder with no real content | Drop it — empty dimensions clutter the graph |
| Wrote untyped `[[wikilinks]]` | Add the relationship: `[[page|relation]]` — see `references/graph-and-manifest.md` |
| Documented intent rather than implementation | Re-read the code; mark inferences with `<!-- TODO: verify -->` |
| Hard-coded path to another repo | Replace with a `manifest.json` consumed-entry; the registry handles routing |
| Started without reading `docs/wiki/index.md` | Restart — every operation reads index first |
| Skipped Phase 5 because "the docs look right" | Run validation — confidence ratings are how engineers know what to trust |
