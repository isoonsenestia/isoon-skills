# Auth — Three Patterns

Detect by signals, then follow the matching pattern.

## Pattern 1: `middleware.ts` + next-auth JWT (backoffice-app)

**Signal:** `middleware.ts` exists at root and imports `getToken` from `next-auth/jwt`.

All routes except `/[locale]/login` and `/api/*` are protected by middleware. Pages don't need explicit auth checks. Read user data with `useSession()`:

```tsx
"use client"
import { useSession } from "next-auth/react"
const { data: session } = useSession()
```

## Pattern 2: Route groups + `useValidateToken` (growth-monitoring-application)

**Signal:** `app/(authorized)/` and `app/(unauthorized)/` dirs exist. No `middleware.ts`.

Put new protected pages under `app/(authorized)/`. The layout calls `useValidateToken()` which polls a validation endpoint every 60s and redirects to login on failure. No page-level auth needed.

## Pattern 3: Firebase + `useAuth` hook (account-service-application)

**Signal:** `contexts/useAuth.tsx` or `contexts/AuthContext.tsx` exists.

Call `useAuth()` in the component. Use the repo's `<PageManager authenticatedOnly={true}>` wrapper for protected pages.
