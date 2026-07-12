# UI Spec Template

Instantiate to `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.md`. Copy the source image to `<repo>/docs/ui-specs/assets/<slug>.png` first - the pasted temp path vanishes. Omit the Screens table for single pages/fragments. Repeat the "Screen" section per screen for flows.

```markdown
---
date: YYYY-MM-DD
source-image: ./assets/<slug>.png
repo: <repo-name>
screens: <N>
---

# <Feature or page name> - UI Spec

## Screens (flows only)

| # | Screen | Entered from | Exits to |
|---|---|---|---|
| 1 | <name> | <entry> | <exit> |

## Screen: <name>

### Layout

Semantic regions only - header / content sections / footer. No pixel values.

### Component map

| Element in mock | Repo component | Variant / props |
|---|---|---|
| <element> | <existing component or NEW> | <variant, size, props> |

### Token map

| Visual | Snapped value | Confidence |
|---|---|---|
| <e.g. primary button bg> | <e.g. `--primary`> | confident \| ambiguous-resolved |

### States

| State | Treatment |
|---|---|
| loading | <treatment> |
| empty | <treatment> |
| error | <treatment> |

### Behavior & navigation

| Element | Action / target |
|---|---|
| <element> | <what happens, where it goes> |

### Data & copy

- Source: <existing service + method / new endpoint (Backend note) / mock>
- Bindings: <field -> source path>
- i18n keys:

| Key | th | en |
|---|---|---|
| <key> | <th copy> | <en copy> |

- Backend notes: <new endpoints needed - for the Backend agent, not built here>

### Acceptance checklist

Measurable assertions consumable by verify-ui-against-design-headless:

- [ ] <e.g. gap card->band = `gap-4` = 16px>
- [ ] <e.g. button bg = `hsl(var(--primary))`>
```
