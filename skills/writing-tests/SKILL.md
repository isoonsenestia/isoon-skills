---
name: writing-tests
description: Use when writing a test for a dev-squad TDD-first task (or any time you must author a unit, integration, or e2e test) — guides tier selection and meaningful assertions. Triggers when a WRITE_TEST prompt says "use the writing-tests skill" or when asked to write tests for a feature/bugfix.
---

# Writing Tests

Pick the smallest tier that genuinely exercises the task, then write assertions that
would fail if the behavior were wrong — never tautologies.

## Tier selection

| Tier | Use when | Gated by the dev-squad loop? |
|------|----------|------------------------------|
| **Unit** | logic in one function/module, no I/O | YES — RED→GREEN enforced |
| **Integration** | two+ units / a real dependency that runs bare (in-memory DB, local fs) | YES if it runs with no external infra; else the task falls to the floor |
| **E2E** | full stack through a running app + browser | NO — authored, but the loop cannot run it bare; the task falls to the floor and a human/CI verifies e2e |

Default to **unit**. Reach for integration only when the behavior is in the seam
between units. Write e2e only when the task is explicitly an end-to-end flow — and
know the harness will not execute it.

## Write a test that can fail for the right reason

- Assert on the actual observable output/state the task changes, not on a constant
  you also hardcode in the implementation.
- Cover the happy path AND at least one edge/error case the task implies.
- The test must reference the not-yet-existing API so it is RED before implementation
  (a compile error counts as RED, but prefer an assertion that pins behavior).
- Do not weaken or delete existing tests.

## Per-stack idioms

**go** — `*_test.go`, package `testing`. Table-driven tests for multiple cases:
```go
func TestFeature(t *testing.T) {
    cases := []struct{ in, want int }{{1, 2}, {3, 6}}
    for _, c := range cases {
        if got := Double(c.in); got != c.want {
            t.Errorf("Double(%d)=%d want %d", c.in, got, c.want)
        }
    }
}
```

**nextjs** — unit/integration: `*.test.ts(x)` / `*.spec.ts(x)` with vitest or jest.
e2e: Playwright under `e2e/` or `__tests__/`. Query by role/label, assert on
user-visible output, not implementation details.

## Anti-patterns

- `assert true`, `expect(1).toBe(1)`, asserting a value the impl will trivially return.
- Testing mocks instead of behavior.
- One giant test; prefer focused cases named for the behavior.
