# Interview Question Bank

Rules: batch by dimension via `AskUserQuestion` (up to 4 questions per call), at most 3 rounds total. Every option list leads with a repo-convention default marked "(Recommended)". Skip any question the image or the repo already answers - the hard test for every question: neither the image nor the repo can answer it.

## States & edge cases

Propose defaults by component type; ask only to confirm or override:

| Component | Default states |
|---|---|
| Form | Inline validation on blur; submit shows loading on the button; API error shows toast; success behavior asked (navigate vs success view) |
| List / table | Loading skeleton; empty state with message; error with retry |
| Detail / card page | Loading skeleton; not-found state |
| Modal / dialog | Confirm shows loading; ask whether backdrop dismisses |

Then one open question: which states exist that the mock does not show? (loading / empty / error / validation / disabled)

## Behavior & navigation

- Per interactive element: propose the target/action inferred from flow arrows, element naming, or existing routes; ask to confirm.
- Form submit: which endpoint, and what happens on success.
- Flows: confirm screen order and back-navigation behavior.

## Data & copy

- Data source: existing service (grep `services/` / `_repositories/` first and propose the match) / new endpoint (record as Backend-agent note, never create) / mock data.
- Field bindings: propose from the API shape when a service exists; ask only unmapped fields.
- Copy: is the mock text final? Propose th/en i18n keys per fe-next i18n rules; if the mock shows one language, ask for the other only when not derivable.

## Ambiguous snaps

Ask only when the choice materially changes implementation:

- New component vs a variant of an existing component.
- Off-token colour: `measure.py` reports the measured hex and its nearest token with a dE. Ask only when dE > 10 - add a token, snap to the nearest, or use the raw hex.
- `token-source: tailwind-default` in the measure output: the repo's own tokens could not be resolved, so ask for brand colours rather than snapping to stock Tailwind.
- A region that may overflow: fixed vs scrollable.
- The capture is refused as not pixel-exact: confirm whether it is an unscaled 1x screenshot, or accept snap mode with no measured rows.

## Situations and their answers

| Situation | Do this |
|---|---|
| Colour not in the token set | Ask: add a token vs snap to nearest - never silently invent a hex |
| New component vs variant of existing | Ask only if the choice changes implementation |
| Unreadable/blurry region | Name what is unreadable, request a better crop - never guess |
| Fresh repo, no design system | Default Tailwind scale, flag it in the spec, ask brand colours only |
| Fragment (single component) | Same pipeline scoped to the component; ask container context once |
| New API endpoint needed | Record as a note for the Backend agent - do not create it |
