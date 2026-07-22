---
name: verify-ui-against-design-headless
description: Use when verifying a UI component matches a design or pixel spec in a Next.js (or similar) repo that has no DOM test runner (no jsdom/RTL) — to actually see and measure the rendered result, not just confirm it compiles.
---

# Verify a UI Component Against a Design with Headless Chrome

**Rule:** Build a throwaway preview route that renders the component in a faithful container, run dev, screenshot it with headless Chrome, and for exact values inject a client-side `getBoundingClientRect()` readout rendered as on-screen text. Delete the harness before committing. **A green `tsc`/`lint`/`build` is NOT evidence of a pixel match.**

**Why:** Matching the obesity result ruler to Figma — `tsc`/`lint`/`build` all passed while the padding was still wrong, twice. Only a headless screenshot plus an on-page measurement (`band←card 16.0px · tick←band 16.0px`) confirmed the spec. The advisor's line: a self-screenshot proves "matches what I *think* the design wants," not "matches the design" — so measure, and let the design (or user) be the oracle.

**How to apply:**
- Preview route *under the locale segment* so i18n/providers resolve: `src/app/[locale]/<tmp>/page.tsx`, rendering the component inside a copy of its real card context.
- `PORT=37xx npm run dev &`; wait + trigger compile with `curl -s -o /dev/null --retry 40 --retry-connrefused --retry-delay 1 <url>` (bare sleeps race startup).
- Screenshot: `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=W,H --screenshot=out.png <url>`, then Read the PNG.
- Exact pixels: a client `useEffect` that queries the DOM (e.g. `[class*="<arbitrary-class-substring>"]`), computes gaps from `getBoundingClientRect()`, and renders them as visible text.
- Teardown: `rm -rf` the route + kill dev before commit. A stale `.next/types` for the deleted route makes `tsc` error — `rm -rf .next` and rebuild.

## Assert spacing against the design reference (don't eyeball it)

A screenshot proves *presence*; it does not prove *spacing*. When the build came from `ui-image-intake`, there is a `<slug>.design.md` with a single spacing scale (`edge`, `section`, `item`, `group`, `card-pad`, …) in px. Verify each numerically instead of by eye — this is what catches "parts don't align."

- **Build a target list from `design.md`**: each row is `(label, selectorA, selectorB, expectedPx)`. Cover at least one gap per scale token, and always compare the SAME token across different components (e.g. `card-pad` on the toolbar vs the bottom cards) — cross-component drift is the common failure.
- **Measure in the page**: a client `useEffect` reads `getBoundingClientRect()` for each pair, computes the gap, and renders `label: actual / expected` as on-screen text (and `console.log`s it so the dev log carries it too).
- **Assert with tolerance ±2px** (sub-pixel rounding, borders). Flag any row outside tolerance as FAIL with both numbers; do not report "matches" while any row fails.
- **Consistency check**: assert equal-token gaps are equal to each other, not just to the target — e.g. `toolbar card-pad == bottom card-pad`. A build can hit each target individually yet still look inconsistent if one component used a different token.
- Divide measured values by `--force-device-scale-factor` if you read them off the 2x screenshot rather than from the in-page readout; the in-page `getBoundingClientRect()` is already in CSS px, so prefer it.

**Anti-example:** Declaring a design-match task done because `next build` passed — that shipped the wrong inset twice before a screenshot caught it. Second anti-example: a screenshot that "looked right" while the toolbar used `p-1.5` and the bottom cards used `p-1` — only a cross-component `card-pad` assertion would have failed it.

## Related

- **RELATED:** ui-image-intake (produces the `<slug>.design.md` spacing scale this skill asserts against)
