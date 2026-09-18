# Design Review Framework

Adapted from *A Philosophy of Software Design*. Used by the Architecture focus area of `pr-review`.

## Complexity costs

Every design finding must name exactly one:

- `Change amplification` - one policy or behavior change requires edits in several places.
- `Cognitive load` - a reader or caller must remember implementation detail, ordering, or exceptional rules beyond its responsibility.
- `Unknown unknowns` - a caller can miss a necessary behavior because the contract does not make the requirement visible.

## Boundary questions

Ask these while tracing the diff and its callers:

1. What domain outcome does the caller need?
2. What detail or policy must the caller currently know to obtain it?
3. Which module has the knowledge and control to own that detail?
4. Does the API the diff introduces expose intent while hiding implementation detail?
5. Do related policies change together and belong behind one boundary?

## Design checks

- `Deep module` - a simple interface hides substantial related complexity.
- `General-purpose module` - an API supports natural use cases without caller-specific special cases.
- `Different abstraction` - controller, service, and repository do not repeat the same implementation-level story.
- `Pull complexity downward` - the owner handles unavoidable detail instead of distributing it to callers.
- `Error design` - invariants, validation, or safe defaults can remove an error case before it reaches callers.
- `Consistency` - names, contracts, parameter order, and result shapes let readers reuse understanding.
- `Obviousness` - names, control flow, and comments make behavior clear. Comments capture why, constraints, or invariants rather than restating code.

## Comment pattern for step 4

State the observation, then the cost, then the design direction:

> This caller currently owns `[detail or policy]`, which creates `[complexity cost]`. Could `[module or API]` own it so `[future change or domain outcome]` stays in one place?

Name the boundary, not the implementation. If the right boundary is the real issue, a concrete patch that keeps the wrong boundary is noise.
