# Ongoing Operations

After initial generation, you maintain the knowledge base through these operations. Read `docs/WIKI-SCHEMA.md` in the target repo for the full operational schema.

## Ingest

When code changes or new raw docs land:

1. Read `docs/wiki/index.md` to understand current state.
2. Read changed sources.
3. Update affected wiki pages across all relevant dimensions.
4. Update graph edges and cross-references.
5. Update `manifest.json` if exposed APIs/events/entities changed.
6. Log every action in `log.md`.

## Query

When someone asks about the codebase:

1. Read `docs/wiki/index.md` to find relevant pages.
2. Follow graph edges to gather connected context.
3. Read raw docs for authoritative detail via `source_refs`.
4. For cross-repo questions, read `docs/manifest.json` to find linked services.
5. Synthesize the answer with `[[wikilink]]` citations.
6. Offer to file substantial answers as new wiki pages.

## Lint

Periodic health check:

1. **Content health** — contradictions, stale claims, unresolved TODOs.
2. **Structure health** — orphan pages, broken links, missing dimensions.
3. **Implementation drift** — wiki claims vs. actual code.
4. **Graph health** — dangling cross-repo links, outdated manifest.
5. **Report by severity** — 🔴 Critical / 🟡 Warning / 🔵 Info.

## Sync

Push this repo's knowledge to the central registry:

1. Validate `docs/manifest.json` is up to date.
2. Copy manifest to `docs-registry/repos/{service-name}/manifest.json`.
3. Regenerate `docs-registry/registry.json` from all manifests.
4. Update cross-repo synthesis pages in `docs-registry/wiki/`.

See `references/registry-schema.md` for the central registry layout.
