# Design Reference Template

Instantiate to `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.design.md`. This is the **visual target** the builder reads alongside the semantic spec. It pins what the spec deliberately leaves open. Snap every value to the repo scale; where the image forces a proportion the scale doesn't cover, record the nearest step and mark it `approx`.

```markdown
---
date: YYYY-MM-DD
source-image: ./assets/<slug>.png
spec: ./<YYYY-MM-DD>-<slug>.md
---

# <Feature or page name> - Design Reference

## Layout proportions

Anchor + relative size per region. No absolute px unless the image forces it.

| Region | Anchor | Size / width | Notes |
|---|---|---|---|
| <region> | <e.g. top-center, fixed> | <e.g. w-52, auto> | <e.g. floating, offset-4 from edge> |

## Spacing scale (ONE scale for the whole screen)

Define a single named scale here and make EVERY component reference it. Do not let a component invent its own gap - that is what makes parts fail to align. In **match mode**, measure each relationship on the oracle image and round to the nearest 4px step; in **snap mode**, snap to the repo scale.

Fill every row - these relationships are mandatory (a missing one becomes a guess):

| Token | Where it applies | Value | = px |
|---|---|---|---|
| `edge` | any floating element ← viewport edge | `left-4/top-4` | 16 |
| `section` | between panel sections | `gap-5` | 20 |
| `item` | between items in a row (swatches, toggles, tools) | `gap-1.5` | 6 |
| `group` | between visual groups (across a divider) | `mx-1` | 4 |
| `card-pad` | inner padding of toolbars/small cards | `p-1.5` | 6 |
| `panel-pad` | inner padding of the properties panel | `p-4` | 16 |
| `label-control` | section label ← its control | `gap-2` | 8 |

Consistency rule: if two components show the same *kind* of gap, they use the same token. One `item` value, one `section` value, etc. - reused, never re-guessed per component.

## State-weight

The EXACT emphasis for each interactive state. Match the image - do not over-emphasize (no invented `ring-2` where the image shows a soft fill).

| State | Treatment |
|---|---|
| hover | <e.g. `bg-slate-100`> |
| active / selected | <e.g. `bg-indigo-100` fill only, NO ring> |
| selected swatch | <e.g. subtle `ring-1 ring-indigo-400`> |
| slider thumb | <e.g. neutral `bg-slate-800`, not accent> |

## Component sizing

| Component | Size |
|---|---|
| icon button | <e.g. h-9 w-9, icon 16, strokeWidth 2> |
| swatch | <e.g. h-6 w-6, rounded-md> |
| primary button | <e.g. h-9, px-3, text-sm> |

## Visual grouping

Dividers / separators / groups the image shows that the semantic spec omits.

- <e.g. toolbar: separator after the lock tool; separator before the frame/shapes tool>

## Per-icon fidelity

Call out any icon that is NOT a plain glyph - the builder must use the icon library, never a text character.

| Element | Icon | Fidelity note |
|---|---|---|
| <e.g. pressure smooth> | <lucide/react-icon name> | <e.g. sine waveform, not the char "∿"> |
| <e.g. fill hachure> | CSS pattern | <e.g. clear 45deg repeating lines, not faint dots> |

## Visual acceptance targets

Measurable, consumable by verify-ui-against-design-headless (complements the spec's semantic checklist):

- [ ] <e.g. active tool = bg-indigo-100 with NO ring>
- [ ] <e.g. toolbar item gap = 6px>
- [ ] <e.g. pressure icons render as waveforms, not text glyphs>
```
