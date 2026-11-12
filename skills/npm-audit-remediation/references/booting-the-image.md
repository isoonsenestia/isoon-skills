# Booting the real image for verification

The goal is the shipped image serving the requests whose code paths the dependency changes touch, against real instances of every backing service.

## Setup

- All files (compose, env, stub SQL, seed users, generated passwords) live outside the repo, in the session scratchpad. Generate passwords with `openssl rand`; never use real credentials.
- One compose file: one container per backing service (database, cache, queue broker, message bus) plus the app built from the repo `Dockerfile`, with `depends_on` health checks. Use a compose project name of your own so teardown cannot hit anything else.
- On arm64 hosts, images without an arm64 build (SQL Server: `mcr.microsoft.com/mssql/server:2022-latest`) run with `platform: linux/amd64`.
- Env: `NODE_ENV=production` and the production feature flags. If a changed package sits on a worker, cron or queue path, boot with workers on; otherwise workers off is fine, but say which paths stayed unexercised.

## ORM sync against an empty database

Services that sync models at boot (Sequelize `autoLoadModels`/`synchronize`, TypeORM `synchronize`) fail on an empty database in ways production never sees:

- Associations become `FOREIGN KEY` constraints on non-key columns, which the database rejects.
- Two models mapping one table: whichever syncs first decides the columns.
- Raw SQL in the code needs objects no model declares (stored procedures, extra columns).
- The failure is often logged as "Unable to connect to the database" after retries. Run with the ORM's SQL logging on and read the statement that failed before assuming a network problem.

Pre-create the tables the sync trips on, without foreign keys, one failure at a time, and add the procedures or columns raw queries need. Seed one user per role the requests need.

## Requests

Drive the paths the changes touch, plus a baseline:

- heartbeat or health route
- a JSON POST, an urlencoded POST and a compressed (`Content-Encoding: gzip`) POST when a body parser changed
- an auth-guarded route with no token, a forged token, and a real login token
- one route per backing service (a query on each database, a queue job when workers are on)
- each advisory trigger you reproduced, then heartbeat again and the container restart count

## Teardown

`docker compose -p <project> down -v --remove-orphans`, then remove the images you built or pulled. Leave the global build cache alone and tell the user its size instead.
