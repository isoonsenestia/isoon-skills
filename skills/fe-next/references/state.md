# State Management — Four Patterns

Read before adding new state or wiring a feature.

## Redux Toolkit with `redux/` dir (backoffice-app)

Store at `redux/store.ts`. Always use typed hooks from `redux/hooks.ts`:

```typescript
const dispatch = useAppDispatch()
const data = useAppSelector(selectAppointments)
```

Per-feature: `*Thunk.ts` → `*Slice.ts` (extraReducers only) → `*Selector.ts`.

**Critical:** Dispatch `getConfig()` first and wait for config to load before dispatching feature thunks. Base URLs and API keys come from Redux config state.

## Redux Toolkit with `stores/` dir (patient-journey-app)

Feature-scoped: `stores/<feature>/asyncThunk.ts` + `stores/<feature>/slice.ts`. Thunks read API URLs from `getState()`.

## Redux Toolkit with `store/` dir (NESTA_UI)

Same RTK pattern. Uses `createAppAsyncThunk` wrapper (project-specific typed version).

## React Query (synphaet-care-app)

`useQuery` for reads, `useMutation` for writes. No Redux store. Invalidate queries after mutations.

## Context API (account-service-application, vaccine-system-application)

Auth, device, and analytic state in contexts. Pattern: `createContext` → `ProviderComponent` → `export const useXxx = () => useContext(XxxContext)`.
