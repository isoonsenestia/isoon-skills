---
name: ui-image-intake
description: Use when given a UI image (screenshot, mock, or multi-screen flow) to build or match frontend from - the user pasted a design image and asked to build/implement it, or you are about to write UI code where the only design source is an image
---

# UI Image Intake - Semantic Setup Before Build

## Overview

An image shows structure, not truth: it cannot tell exact spacing, tokens, states, behavior, or data. Snap all visuals to the repo's design system, interview the user only for what neither the image nor the repo can answer, then write TWO artifacts: a **semantic spec** (regions, components, tokens, behavior, data) and a **design reference** (`design.md` - spacing rhythm, state-weight, component sizing, per-icon fidelity). The build follows both, never the image.

**Why two artifacts:** the semantic spec deliberately records no pixel values, which is correct for token snapping but leaves spacing, active-state emphasis, and icon fidelity as free guesses - the exact places a faithful build drifts. The design reference pins those visual decisions so the builder has a concrete target and the verifier has something to measure against.

## When to Use

- User pastes a mock/screenshot/flow image and asks to build, implement, or match it.
- About to write UI code where the only design source is an image.

**When NOT to use:**
- A Figma link is available - use the Figma MCP; real values exist there.
- The image is bug context or a reference, not a build target.
- Running as a dispatched dev-squad agent - see Dispatch guard below.

## The Pipeline

0. **Pick the fidelity mode** - this governs the whole run:
   - **Snap mode** (repo HAS a design system): snap all spacing/sizing to the repo scale; do NOT measure the image. The image gives structure only.
   - **Match mode** (greenfield with no system, OR the user said "match/clone this exactly"): you MUST measure the oracle image for spacing and sizing, then round each measurement to the nearest 4px step. Guessing is what causes spacing drift; here, measure.
1. **Decompose** - classify the input: single page, multi-screen flow, or component fragment. Flows: name each screen, record transition order. Per screen, inventory semantic regions (header/content/footer), components, visible text, icons. In snap mode record NO pixel values; in match mode record measured gaps (see step 5).
2. **Profile & snap** - run the fe-next repo profile; read `tailwind.config.*`, HSL tokens in `globals.css`, `src/components/ui/*` or AntD; grep for existing similar screens (the strongest prior). Snap every visual: color to existing token, spacing to nearest Tailwind step, type to existing style, element to existing component (reuse-first). Mark each snap **confident** or **ambiguous**.
3. **Interview** - `AskUserQuestion`, batched by dimension, at most 3 rounds, each option list leads with a repo-convention default marked "(Recommended)". Only ask what neither image nor repo answers: states & edge cases, behavior & navigation, data & copy, plus ambiguous snaps that materially change implementation. Question bank and defaults: `references/interview.md`. Responsive is defaulted (mock's viewport, standard stacking) - never asked.
4. **Spec** - write `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.md` following `references/spec-template.md`; copy the pasted image to `<repo>/docs/ui-specs/assets/<slug>.png` (pasted temp paths vanish; the saved copy is the verification oracle). Committing the spec is the user's call. (Greenfield with no repo: write to `<project>/docs/ui-specs/` and flag the default Tailwind scale.)
5. **Design reference** - write `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.design.md` following `references/design-template.md`. This is the visual target the builder reads *alongside* the spec. It pins the decisions the spec leaves open: **layout proportions** (anchor + relative size), **spacing rhythm** (the exact gap scale to follow), **state-weight** (the precise active/hover/selected treatment - do NOT invent a heavy ring where the image shows a soft fill), **component sizing** (button/swatch/control dimensions), **visual grouping** (dividers/separators), and **per-icon fidelity** (shape + weight, called out for any icon that is not a plain glyph - e.g. waveforms, hachure fills). Snap values to the repo scale; where the image forces a proportion the scale doesn't cover, record the nearest step and mark it.
6. **Handoff** - build from BOTH the spec and the design reference via fe-next (never re-guess visuals from the image), then verify with verify-ui-against-design-headless using the saved image plus the spec's acceptance checklist and the design reference's visual targets.

## Dispatch guard

If the prompt originates from a dev-squad `plan.md` (dispatched agent - no user available to answer): do not interview, do not guess. Halt and report: "image input needs a pre-dispatch intake spec". Intake happens interactively before dispatch; the plan task must reference an existing spec file instead of a raw image.

## Quick Reference

| Situation | Do this |
|---|---|
| Color not in the token set | Ask: add a token vs snap to nearest existing - never silently invent hex |
| New component vs variant of existing | Ask only if the choice changes implementation |
| Unreadable/blurry region | Name what is unreadable, request a better crop - never guess |
| Fresh repo, no design system | Default Tailwind scale, flag it in the spec, ask brand colors only |
| Fragment (single component) | Same pipeline scoped to the component; ask container context once |
| New API endpoint needed | Record as a note for the Backend agent - do not create it |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reading px/hex values off the image in SNAP mode | Snap to the repo scale/tokens; the image is structure, not truth |
| Guessing spacing in MATCH mode instead of measuring | Greenfield/clone has no scale to snap to - measure the oracle, round to 4px, don't guess |
| Each component picking its own gap, so parts don't align | Define ONE spacing scale in `design.md`; every component references it, none invents its own |
| Asking about spacing/color the repo already answers | Infer it; the interview is for semantics only |
| Building straight from the image after the interview | Build from the spec file |
| Spec without an acceptance checklist | The checklist is what verify-ui-against-design-headless consumes |
| Interviewing as a dispatched agent | Halt with "needs a pre-dispatch intake spec" |
| Inventing a heavy active state (e.g. `ring-2`) where the image shows a soft fill | Pin the exact state-weight in `design.md`; match the image's emphasis, don't over-emphasize |
| Guessing inter-item spacing, so the layout comes out too tight/loose | Record the spacing rhythm in `design.md` as an explicit gap scale; don't leave it to the builder |
| Substituting a plain glyph for a real icon (waveform, hachure) | Call out per-icon fidelity in `design.md`; use the icon library, not a text character |
| Skipping `design.md` because the spec "already covers it" | The spec is semantic; visual proportion/state/sizing live in `design.md` - both are required |

## Related

- **RELATED:** fe-next (the builder - consumes the spec AND the design reference)
- **RELATED:** verify-ui-against-design-headless (the oracle - consumes saved image + acceptance checklist + design-reference visual targets)
- **TEMPLATES:** `references/spec-template.md` (semantic spec), `references/design-template.md` (visual design reference)
