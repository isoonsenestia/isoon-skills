---
name: npm-audit-remediation
description: Use when asked to handle, triage, list or fix `npm audit` findings in a Node service - a security ticket, Dependabot or Socket alerts, "ดู npm audit", a vulnerable transitive dependency pinned by a framework, or deciding between `npm audit fix`, an `overrides` entry and a major bump.
---

# Remediating npm audit findings

## Overview

The audit count is not the risk. Each change is decided per root cause, by whether the vulnerable code path is reachable, and the smallest change that closes a reachable path wins. An override made for an unreachable production advisory adds risk and buys nothing but a lower number.

Dev dependencies are judged differently: they run on developer machines and in CI with install scripts and repo secrets, so a critical or high there is a supply-chain risk even when nothing ships it.

## When NOT to use

- The Node runtime itself must change: use **upgrading-node-runtime** first; it calls this skill for its dependency step.

## The pattern

### 1. One toolchain for every command

Read `.nvmrc` (or `engines.node`). Every command is one call: `source ~/.nvm/nvm.sh; nvm use >/dev/null; node -v; <cmd>`. Without the `source`, a non-interactive shell skips nvm and silently runs the system Node; the result counts only if that same call printed the expected `node -v`. Call binaries as `./node_modules/.bin/<tool>`, not `npx`, which can resolve a global copy.

### 2. Snapshot and group by root cause

Snapshots go outside the repo (`$TMPDIR` or the session scratchpad). Take one before any change and one after each commit.

```bash
D=${TMPDIR:-/tmp}/audit-$(basename "$PWD"); mkdir -p "$D"
npm audit --json > "$D/all-$1.json"; npm audit --omit=dev --json > "$D/prod-$1.json"   # $1 = before|after-<commit>
jq -r --slurpfile p "$D/prod-$1.json" '.vulnerabilities|to_entries[]|[.value.severity, .key,
  (if $p[0].vulnerabilities[.key] then "prod" else "dev" end),
  (.value.fixAvailable|if type=="object" then "\(.name)@\(.version)\(if .isSemVerMajor then " MAJOR" else "" end)" else tostring end),
  ([.value.via[]|select(type=="object")|.url]|unique|join(" "))]|@tsv' "$D/all-$1.json"
```

Rows with no advisory URL are parents counted again for a child. Work on the rows that carry a URL. Diff advisory ids between snapshots with `jq -r '[.vulnerabilities[].via[]|objects|.url]|unique[]'`.

### 3. Reachability per root cause (critical, high, then prod moderate)

Read each advisory (`gh api /advisories/<GHSA>`, a read-only public lookup) for the exact trigger, then prove or disprove that trigger in this app:

- **Who calls it:** `npm ls <pkg>`, then grep `src` for the API named in the advisory (`qs.stringify`, `_.template`, `FileTypeValidator`, `@Sse`).
- **Library internals:** read the installed code in `node_modules` for the options it passes (`qs.parse(str, { allowPrototypes: true })`) and for env-gated features (`OTEL_METRICS_EXPORTER`, `OTEL_PROPAGATORS`).
- **Shipped or not:** the Dockerfile install flags (`--omit=dev`, `--ignore-scripts`) and what production code loads at runtime: imports, `require`, and packages loaded by name such as an ORM dialect string (`dialect: "sqlite"` loads `sqlite3`). A devDependency loaded at runtime ships anyway.
- **Env you cannot see:** ask the user. If you cannot ask (you are a subagent, or the user is away), mark the row "unknown: depends on `<VAR>`", treat it as reachable for the fix decision, and put the question at the top of your report.

Output one table: root cause, advisory, trigger, reachable (yes / no + evidence / unknown), fix path.

### 4. Choose the fix, smallest first

| Situation | Fix |
|---|---|
| Fix inside existing ranges | `npm audit fix` (never `--force`), one pass |
| After that pass, a row still shows a non-major `fixAvailable` | `npm update <pkg>`; the lock diff must touch only that package |
| Dev-only critical or high, standalone package (not a framework or its CLI), major bump available, not loaded at runtime | bump it in its own commit |
| Reachable, parent pins an exact old version, patched release on the same major | `overrides` scoped under the parent: `{"<parent>": {"<pkg>": "<x.y.z>"}}`. Read the package's changelog between versions for behaviour changes |
| Reachable, fix is a 0.x minor, a framework major (NestJS, OTel SDK, `@nestjs/cli`) or any other major | ask the user; if you cannot, list it as a follow-up with the reason. Never fold it into the security PR unasked |
| Unreachable production advisory | leave it; record the evidence in the PR |

After `npm audit fix`, diff the advisory ids. A fix can raise a parent that pins a new vulnerable child (a framework patch pinning `file-type`, `multer`); triage those new rows like the rest. Do not run `npm audit fix` a second time: to drop the new child it may downgrade the parent and reopen the advisory the first pass closed.

Check what it lowered: for each package whose version went down in the lock diff, `npm ls <pkg>` before and after. A root-level copy that moved down while the nested copies kept their majors is hoisting, not a downgrade. A real downgrade of a direct dependency or of a parent is a finding.

`npm audit fix` itself moves many lockfile entries; that is accepted. Beyond the rows above, change no dependency the audit did not ask for: no hand range bumps of unrelated direct deps, no downgrades to make tests pass. A test that slows or breaks after a fix is a finding to diagnose, not to pin away.

### 5. Reproduce before trusting the fix

For a reachable runtime advisory, try the trigger against the app's own stack (a minimal app on the repo's `node_modules`, or the booted service). "Before" is the tree after the `npm audit fix` commit and before this fix; "after" is with the fix.

A first attempt that does not crash proves little. Vary what the advisory describes: chunking (one write against separate writes), timing between chunks, padding or trailing data, each encoding or option it names. Read the patch diff to see which state it guards. Only after those variants, write "did not reproduce; the change follows the advisory" in the PR.

### 6. Verify

1. `npm ci`, build, typecheck, lint (no autofix), tests, then the audit table again.
2. Lint and test failures that already fail on the commit your branch was cut from (run them there to confirm) are fixed too, in their own commit after the dependency commits. This is the one change outside the audit scope.
3. Coverage gaps: `.npmrc` `ignore-scripts=true` means native modules (sqlite3, bcrypt) are never built, and `describe.skip` suites prove nothing. Exercise anything you changed that the suite does not reach.
4. Boot the real image and serve requests: the repo's own run skill if it has one, otherwise follow `references/booting-the-image.md`. Check `node -v` inside the image against the version the audit and tests ran on; a floating base tag can differ. "Modules initialised, then connection refused" is not a boot.

If containers cannot run here (no Docker, no disk, no registry login), commits may still be made, but the work is not done: open nothing beyond a draft PR, mark the boot as not verified in it, list the requests to make on staging, and lead your report (to the user, or to whoever dispatched you) with that. If containers become available later, run this step then and send the result as an addendum to that report.

### 7. Ship

One commit per concern (audit fix, each targeted update, each override, each bump, pre-existing lint), with the GHSA id and the reachability reason in the message. PR body: before/after counts all and prod, the reachability table, each override with when to remove it, and what was not verified.

## Common mistakes

| Mistake | Reality |
|---|---|
| Treating the total as the target | Parents are double counted; reachability decides |
| Overriding every flagged package | Each override is untested-combination risk and future debt |
| Global `overrides` entry | Leaks into every consumer; scope under the parent |
| Override with no removal note | The next framework major silently gets the old version |
| Audit on one Node, build on another | Results do not describe what ships |
| Second `npm audit fix` pass | Can downgrade a parent and reopen what the first pass closed |
| Trusting the after-count without diffing ids | New advisories hide inside a lower total |
| One failed repro, then "not exploitable" | Crashes often need split writes, timing or padding |
| `npx tsc` errors you cannot reproduce | A global TypeScript ran; use `./node_modules/.bin/tsc` |
| Green tests after a native-module bump | With `ignore-scripts` the binding never loaded |
| Boot check that never served a request | Proves module wiring only |

## Related

- **RELATED:** upgrading-node-runtime
- **RELATED:** the repo's own run skill, when it has one, replaces `references/booting-the-image.md`
