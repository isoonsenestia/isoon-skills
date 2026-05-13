# Task Playbooks

## Build a new page — Pages Router

1. Check `pages/` for similar pages to copy layout and `getStaticProps` structure
2. Create `pages/<route>.tsx` with `getStaticProps` loading i18n messages
3. Add `NextPageWithLayout` type and `getLayout` for shared layout
4. Extract API calls to `services/`, fetching logic to a hook in `hooks/`
5. Add new translation keys to `locales/th.json` (and `en.json` if present)
6. Run `npx tsc --noEmit`

## Build a new page — App Router

1. Identify the correct route group: `app/[locale]/`, `app/(authorized)/`, or `app/(unauthorized)/`
2. Add `"use client"` if the page uses state, effects, or event handlers
3. For Redux repos: dispatch `getConfig()` in `useEffect`, then dispatch feature thunks after config loads
4. Messages come from the layout's `NextIntlClientProvider`; call `useTranslations()` directly
5. Run `npx tsc --noEmit`

## Build a new component

1. `grep -r "ComponentName" components/ app/ src/` — confirm it doesn't already exist
2. Create `components/<Name>/<Name>.tsx` (and `components/<Name>/index.ts` for re-export if the repo uses that pattern)
3. Use Tailwind classes, not inline styles
4. Use Ant Design for interactive UI controls
5. Export as default

## Fix a UI bug

1. Read the failing component fully before touching anything
2. Identify root cause: state, API data shape, Tailwind class conflict, or Ant Design version prop mismatch
3. Fix the smallest thing that resolves the issue
4. Check other places that use the same component or pattern for the same bug

## Connect a new API endpoint

1. Identify the service pattern this repo uses (`services/`, `_repositories/`, or inline thunk — see `references/services.md`)
2. Add the typed function following the existing pattern in that directory
3. For Redux repos: add a thunk + slice + selector
4. For non-Redux repos: create or update a hook that calls the service/repository
5. Never put axios calls directly in components
