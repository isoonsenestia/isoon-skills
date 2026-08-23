# Design Reference Template

Instantiate to `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.design.md`. This is the **visual target** the builder reads alongside the semantic spec. It pins what the spec deliberately leaves open.

Every numeric row carries `measured | delta | method`. Run `references/measure.py <image>` and fill them from its output. A row with an empty `method` cell is not done, and `verify-ui-against-design-headless` reports it as `UNVERIFIED` rather than passing it.

`method` is one of: `edge-peak` | `pitch` | `box-fill` | `glyph-metric` | `histogram` | `snapped-approx`.

Use `snapped-approx` only where measurement genuinely cannot reach: any gap whose endpoint is text (the line box adds unknown leading, so the true value is +/-4px), and line-height without a multi-line block to measure.

```markdown
---
date: YYYY-MM-DD
source-images:
  - ./assets/<slug>.png
spec: ./<YYYY-MM-DD>-<slug>.md
measured-with: references/measure.py (unit: CSS px, dpr: <n>)
---

# <Feature or page name> - Design Reference

## Layout proportions

| Region | Anchor | Size / width | measured | delta | method |
|---|---|---|---|---|---|
| <region> | <top-center, fixed> | `w-[200px]` | 200 | 0 | edge-peak |

## Spacing scale (ONE scale for the whole screen)

Define a single named scale and make every component reference it. Where no repo scale step lands within 4px of the measurement, use an arbitrary-value utility (`w-[200px]`, `top-[76px]`) rather than a step that is visibly wrong: 200 sits dead centre between `w-48` and `w-52`, and 76 is not a step at all.

Fill every row - a missing one becomes a guess:

| Token | Where it applies | Value | = px | measured | delta | method |
|---|---|---|---|---|---|---|
| `edge` | floating element <- viewport edge | `left-4/top-4` | 16 | 16 | 0 | edge-peak |
| `section` | between panel sections | `gap-5` | 20 | 19 | -1 | snapped-approx |
| `item` | between items in a row | `gap-1` | 4 | 4 | 0 | pitch |
| `group` | between visual groups (across a divider) | `mx-1` | 4 | | | |
| `card-pad` | inner padding of toolbars/small cards | `p-1` | 4 | 4 | 0 | box-fill |
| `panel-pad` | inner padding of the properties panel | `p-4` | 16 | | | |
| `label-control` | section label <- its control | `gap-2` | 8 | 10 +/-4 | | snapped-approx |

**Consistency rule.** Two components share a token when measurement reports them as the same kind: same box extent and same padding. Where the measured cells differ they get different tokens, and this file records why. Forcing one token across components that differ is how a 44px elevated card with 4px padding and a 36px flat pill with zero padding end up sharing a wrong value.

## Layout contract

Flex vs grid is **not** measurable from a raster: `grid-cols-N`, `flex` with `gap`, `flex-wrap` on one line, and `justify-between` with equal children all rasterise identically. So measure the contract and let the builder pick the mechanism.

Uniformity is the **variance of per-child extents**, never colour coverage %. Coverage answers "which colours and how much"; it silently merges two same-coloured elements of different sizes and drops a child from the count.

| Region | Axis | N | Child size | Pitch | Gap | Uniform? | Container start | Build |
|---|---|---|---|---|---|---|---|---|
| stroke swatches | x | 5 | 22x22 | 27 | 5 | yes (extent variance 0) | x=28 | flex + gap |

Convention: default `flex` + `gap`. Use `grid` when children are equal-size and the row is justified across the full container width.

## Typography

| Element | font-size | cap | x-height | descender | snapped style | method |
|---|---|---|---|---|---|---|
| section label | 13 (cap 9 / 0.71) | 9 | 6 | 0 | `text-xs` | glyph-metric |

font-size carries the assumed cap ratio and the +/-1px candidate band, because cap height maps to a size range rather than one value. Line-height is `snapped-approx` unless a multi-line block exists to measure.

## State-weight

The exact emphasis per state, measured from the image, not chosen for effect.

| State | Treatment | measured | method |
|---|---|---|---|
| hover | <e.g. `bg-slate-100`> | | |
| active / selected | `bg-violet-200` fill only, no ring | `#dddafd` at 4.7% coverage, no ring pixels | histogram |
| selected swatch | `ring-1 ring-offset-1` | 1px ring at both edges | box-fill |
| slider thumb | <neutral, not accent> | | |

## Component sizing

| Component | Size | measured | delta | method |
|---|---|---|---|---|
| icon button | `h-9 w-9`, icon 16 | 36x36 | 0 | box-fill |
| swatch | `h-[22px] w-[22px]`, rounded-md | 22x22 | 0 | box-fill |
| panel toggle | `h-8` | 32 | 0 | box-fill |

## Visual grouping

Dividers / separators / groups the image shows that the semantic spec omits. Note their pixel position - a 1px divider inside a repeated row inflates any pitch measured across it.

- <e.g. toolbar: 1px divider at x=733, separating the lock tool from the drawing tools>

## Per-icon fidelity

| Element | Icon | Fidelity note |
|---|---|---|
| <e.g. pressure smooth> | <lucide name> | <e.g. sine waveform, not the char "~"> |

## Visual acceptance targets

Measurable, consumed by verify-ui-against-design-headless alongside the spec's semantic checklist. Each target names its measured value so a disagreement is a number, not an opinion.

- [ ] active tool fill = `#dddafd`, no ring pixels
- [ ] toolbar item gap = 4px (pitch 40 - box 36, `derived`)
- [ ] panel width = 200px
```
