# CLAUDE.md — {Project Name}

## Project Identity

- **Service:** {service-name}
- **Language:** {language} / {framework}
- **Type:** {backend-api | frontend | fullstack | library | worker | gateway}
- **Repo:** {github-url}

## What This Service Does

{2-3 sentence description of the service's purpose and role in the org.}

## Quick Start

```bash
# Install dependencies
{install-command}

# Run locally
{run-command}

# Run tests
{test-command}

# Build
{build-command}
```

## Tech Stack

- **Runtime:** {Node.js 20 / Go 1.22 / Python 3.12 / etc.}
- **Framework:** {NestJS / Express / Gin / FastAPI / etc.}
- **Database:** {PostgreSQL / MongoDB / Redis / etc.}
- **ORM:** {TypeORM / Prisma / GORM / SQLAlchemy / etc.}
- **Auth:** {JWT / OAuth2 / API Key / etc.}
- **CI/CD:** {GitHub Actions / GitLab CI / etc.}

## Project Structure

```
{high-level directory tree}
```

## Key Commands

| Command | Description |
|---------|-------------|
| `{cmd}` | {description} |

## Conventions

- {Convention 1: e.g., "All API routes defined in src/routes/"}
- {Convention 2: e.g., "Database migrations in src/migrations/ using TypeORM"}
- {Convention 3: e.g., "Environment variables in .env, schema in src/config/"}

## Wiki

This repository has a living knowledge base in `/docs/wiki/`.

**How to use it:**
- Claude reads `/docs/wiki/index.md` automatically to navigate knowledge
- Ask any question about this codebase — Claude synthesizes from the wiki
- To update: make code changes, then tell Claude to "ingest"
- To check health: tell Claude to "lint the wiki"

**Dimensions covered:** {list of active dimensions}

**Cross-repo links:** This service's relationships with other services are
documented in `/docs/manifest.json` and linked via the `docs-registry`.

For wiki governance details, see `/docs/WIKI-SCHEMA.md`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `{VAR}` | {yes/no} | {description} |

## Deployment

{Brief deployment notes: how to deploy, where it runs, key infrastructure}

## Related Services

| Service | Relationship | Link |
|---------|-------------|------|
| {service-name} | {calls/consumes/produces} | [[{service-name}::pages/api/overview]] |
