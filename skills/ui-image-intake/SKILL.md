---
name: ui-image-intake
description: Use when given a UI image (screenshot, mock, or multi-screen flow) to build or match frontend from - the user pasted a design image and asked to build/implement it, or you are about to write UI code where the only design source is an image
---

# UI Image Intake - Measure, Then Spec, Then Build

An image cannot tell you states, behaviour or data. It *can* tell you geometry and colour to the pixel, if you measure instead of eyeball. Measure, snap to the repo's design system, interview only for what neither image nor repo answers, then write a **semantic spec** (regions, components, behaviour, data) and a **design reference** (measured spacing, sizing, layout contract, type, state-weight). The build follows both, never the image.

## When to Use

- A mock/screenshot/flow image is the build target.
- About to write UI code whose only design source is an image.

**When NOT to use:** a Figma link exists (use the Figma MCP - real values live there); the image is bug context, not a build target.

## Measure before you write `design.md`

```
python3 references/measure.py <saved-image.png>
```

One JSON document per screen: DPR verdict, refined element boxes, pitch, exact-colour palette with nearest tokens, type metrics. Drill-down subcommands in `--help`. Values are **CSS px**, the unit the verify skill asserts in.

Refusals are values, not exceptions: capture not pixel-exact (`mode: snap-only`, measure nothing), side has no boundary (`UNMEASURABLE`), pitch ambiguous, colour off-scale (dE > 10, ask). Trust them - a wrong number recorded as measured is worse than an honest snap. `selftest` checks the tool against its fixtures.

## The Pipeline

0. **Pick the fidelity mode.** Measure in **both**; the mode governs only what you record. Snap mode records the nearest repo step plus the delta. Match mode records raw px, using an arbitrary-value utility where no step lands within 4px.
1. **Save and decompose.** Copy the pasted image to `<repo>/docs/ui-specs/assets/` first - temp paths vanish, and the saved copy is the oracle. Classify the input (page, flow, fragment), name each screen, inventory regions, components, text and icons.
2. **Profile and snap.** Run the `fe-next` repo profile, then snap each measured value: colour to a token, spacing to a scale step, type to a style, element to an existing component (reuse first). Mark each confident or ambiguous.
3. **Interview.** `AskUserQuestion`, batched by dimension, max 3 rounds, repo default first marked "(Recommended)". Question bank and what never to ask: `references/interview.md`.
4. **Spec.** Write `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.md` per `references/spec-template.md`. The spec stays pixel-free. Committing it is the user's call.
5. **Design reference.** Write `<YYYY-MM-DD>-<slug>.design.md` per `references/design-template.md`, filling the `measured | delta | method` cells from step 0. An empty `method` cell means the row is not done.
6. **Handoff.** Build from both artifacts via `fe-next`, then verify with `verify-ui-against-design-headless` against the saved image, the acceptance checklist and the measured targets.

## No user available (dispatched agent)

Halt only on **semantics** - states, behaviour, data - reporting "image input needs a pre-dispatch intake spec". Measurement and the design reference need no user: run them.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Eyeballing a value `measure.py` can read | Measure it, then snap; record both numbers and the method |
| Forcing one token across components measurement shows differ | Share a token only for the same measured kind; record why they differ |
| Asking about spacing or colour the repo already answers | Infer it; the interview is for semantics |
| Building straight from the image after the interview | Build from the spec and the design reference |
| Spec without an acceptance checklist | The checklist is what the verify skill consumes |
| Substituting a plain glyph for a real icon | Use the icon library; record per-icon fidelity |
| Skipping `design.md` because the spec "covers it" | The spec is semantic; geometry, type and state live in `design.md` |

## Related

- **RELATED:** `fe-next` (the builder - consumes both artifacts)
- **RELATED:** `verify-ui-against-design-headless` (the oracle - consumes the saved image, checklist and measured targets)
- **TOOL:** `references/measure.py` (geometry, colour and type from the image)
- **TEMPLATES:** `references/spec-template.md`, `references/design-template.md`
