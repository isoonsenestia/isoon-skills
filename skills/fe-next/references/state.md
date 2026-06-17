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

Feature-scoped: `stores/<feature>/{asyncThunk,slice,selector,type}.ts`. Thunks read API URLs from `getState()`. Typed hooks `useAppDispatch`/`useAppSelector` from `stores/hooks`; register every reducer in `stores/index.ts`. For **local/in-memory state with no API** (e.g. a form result held until submit), use a synchronous `createSlice` with `reducers` + exported actions (cf. `stores/appConfigs`) — not `extraReducers`.

**`StoreProvider` is mounted per-section, NOT globally.** Each top-level section's `layout.tsx` wraps children in `<StoreProvider configs={env}>` (see `app/[locale]/portal/layout.tsx`). A new top-level route that uses Redux hooks **must add its own `layout.tsx`** doing the same, or the hooks throw "could not find react-redux context". Each section gets an independent store instance, so cross-section state is not shared.

**Avoid identity `createSelector`** — `createSelector(s => s.x, x => x)` triggers reselect's dev `identityFunctionCheck`, which logs a noisy "result function returned its own inputs" error during SSR (looks like a crash, isn't). For a plain field read use a plain selector: `export const selectX = (s: RootState) => s.x`. Reserve `createSelector` for derived/computed values.

## Redux Toolkit with `store/` dir (NESTA_UI)

Same RTK pattern. Uses `createAppAsyncThunk` wrapper (project-specific typed version).

## React Query (synphaet-care-app)

`useQuery` for reads, `useMutation` for writes. No Redux store. Invalidate queries after mutations.

## Context API (account-service-application, vaccine-system-application)

Auth, device, and analytic state in contexts. Pattern: `createContext` → `ProviderComponent` → `export const useXxx = () => useContext(XxxContext)`.
