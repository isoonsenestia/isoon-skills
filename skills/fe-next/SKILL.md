---
name: fe-next
description: Use when working in a Senestia Next.js repo — building, reviewing, refactoring, or fixing components, pages, hooks, services, forms, styles, auth, or i18n. Also triggers when dispatched from dev-squad as the Frontend agent.
argument-hint: "[task description or 'review' | 'fix' | 'build <thing>']"
allowed-tools: Bash Read Write Edit Grep Glob Agent
---

# Frontend Agent — Next.js (Senestia)

Read the project context, match existing patterns, deliver code that fits the codebase — never generic boilerplate.

## Startup Sequence

Run before writing any code.

1. **Read `CLAUDE.md`** in the project root for env, conventions, constraints.
2. **Check the wiki** at `~/claude-things/senestia-wiki/` — read the relevant domain index for entity/concept terminology.
3. **Profile the repo** with the commands below.
4. **Grep for what already exists** before reinventing.
5. **Extract acceptance criteria and API deps** from the user's prompt.

### Profile commands

```bash
# Router type
ls app/ pages/ src/app/ src/pages/ 2>/dev/null

# State management
ls redux/ store/ stores/ contexts/ 2>/dev/null
grep -rl "createAsyncThunk"           --include="*.ts" --include="*.tsx" . | grep -v node_modules | head -3
grep -rl "@tanstack/react-query"      --include="*.ts" --include="*.tsx" . | grep -v node_modules | head -3

# Auth pattern
ls middleware.ts 2>/dev/null
ls app/\(authorized\)/ app/\(unauthorized\)/ 2>/dev/null
ls contexts/useAuth* contexts/AuthContext* 2>/dev/null

# Component export style — match whichever count is higher
grep -rl "React\.FC"                  --include="*.tsx" components/ app/ src/ 2>/dev/null | wc -l
grep -rl "export default function"    --include="*.tsx" components/ app/ src/ 2>/dev/null | wc -l

# Ant Design version
grep '"antd"' package.json
```

### Signal → pattern → reference

| Signal | Pattern | Read |
|---|---|---|
| `pages/` or `src/pages/` | Pages Router | `references/playbooks.md` |
| `app/` or `src/app/` | App Router | `references/playbooks.md` |
| Building / fixing a component | A or B by grep count | `references/components.md` |
| Adding / changing an API call | `XxxService` / `xxxRepository` / inline thunk | `references/services.md` |
| Configuring HTTP | next/config / runtime / proxy | `references/axios.md` |
| Writing a data-fetching hook | manual / React Query | `references/hooks.md` |
| `middleware.ts` | next-auth JWT | `references/auth.md` |
| `app/(authorized)/` dir | `useValidateToken` | `references/auth.md` |
| `contexts/useAuth*` | Firebase | `references/auth.md` |
| Redux dirs / React Query / contexts | RTK / RQ / Context | `references/state.md` |
| Building a form | Formik / AntD / useState by complexity | `references/forms.md` |
| Any user-visible string | `t()` via next-intl | `references/i18n.md` |
| `"antd": "4.*"` | v4 — Modal uses `visible` | — |
| `"antd": "5.*"` | v5 — Modal uses `open` | — |

### Directory layout

```
pages/ | app/ | src/app/   ← routes
components/   ← reusable UI
hooks/        ← custom hooks
services/ | _repositories/ ← API layer
redux/ | store/ | stores/  ← RTK state
contexts/     ← React context providers
utils/        ← pure helpers
locales/      ← i18n JSON (th.json, en.json)
constants/    ← shared enums
middleware.ts ← auth + i18n routing
```

## Universal Rules

- Tailwind only — no CSS Modules, no inline styles.
- Ant Design for interactive controls (Table, Form, Modal, Tabs, Alert, Spin, Button).
- App Router interactive components add `"use client"`.
- Default export (not named) for components.
- No `any` in props.
- Never put axios calls directly in components.
- Every user-visible string goes through `t()` (next-intl).
- Use `npm ci`, never `npm install`.
- For App Router + Redux: dispatch `getConfig()` first and wait before feature thunks.

## Output Requirements

Before claiming done:

- `npx tsc --noEmit` passes
- `npm run lint` passes
- No regressions in callers of any shared component you touched

Do not deliver: untyped `any`, hardcoded Thai/English strings, inline styles, CSS Modules, duplicate components, direct axios in pages.

## Dev-Squad Integration

When dispatched from `dispatch.sh`, write the sentinel after work is done:

```bash
mkdir -p ~/.done && touch ~/.done/Frontend
```

## Common Mistakes

| Mistake | Fix |
|---|---|
| Hardcoded base URL | Use Redux config / publicRuntimeConfig / proxy — see `references/axios.md` |
| Mixed component styles in one repo | Match dominant pattern by grep count |
| Dispatched feature thunk before `getConfig()` | Wait for config to load (Redux + App Router only) |
| `visible` prop on AntD v5 Modal | Use `open` — `visible` was removed |
| New endpoint that needs a backend route | Note it for the Backend agent; do not create it here |
| Made up entity names | Read the wiki — use real domain terminology |
