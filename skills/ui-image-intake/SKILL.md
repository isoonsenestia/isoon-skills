---
name: ui-image-intake
description: Use when given a UI image (screenshot, mock, or multi-screen flow) to build or match frontend from - the user pasted a design image and asked to build/implement it, or you are about to write UI code where the only design source is an image
---

# UI Image Intake - Semantic Setup Before Build

## Overview

An image shows structure, not truth: it cannot tell exact spacing, tokens, states, behavior, or data. Snap all visuals to the repo's design system, interview the user only for what neither the image nor the repo can answer, write a spec. The build then follows the spec, never the image.

## When to Use

- User pastes a mock/screenshot/flow image and asks to build, implement, or match it.
- About to write UI code where the only design source is an image.

**When NOT to use:**
- A Figma link is available - use the Figma MCP; real values exist there.
- The image is bug context or a reference, not a build target.
- Running as a dispatched dev-squad agent - see Dispatch guard below.

## The Pipeline

1. **Decompose** - classify the input: single page, multi-screen flow, or component fragment. Flows: name each screen, record transition order. Per screen, inventory semantic regions (header/content/footer), components, visible text, icons. Record NO pixel values from the image.
2. **Profile & snap** - run the fe-next repo profile; read `tailwind.config.*`, HSL tokens in `globals.css`, `src/components/ui/*` or AntD; grep for existing similar screens (the strongest prior). Snap every visual: color to existing token, spacing to nearest Tailwind step, type to existing style, element to existing component (reuse-first). Mark each snap **confident** or **ambiguous**.
3. **Interview** - `AskUserQuestion`, batched by dimension, at most 3 rounds, each option list leads with a repo-convention default marked "(Recommended)". Only ask what neither image nor repo answers: states & edge cases, behavior & navigation, data & copy, plus ambiguous snaps that materially change implementation. Question bank and defaults: `references/interview.md`. Responsive is defaulted (mock's viewport, standard stacking) - never asked.
4. **Spec** - write `<repo>/docs/ui-specs/<YYYY-MM-DD>-<slug>.md` following `references/spec-template.md`; copy the pasted image to `<repo>/docs/ui-specs/assets/<slug>.png` (pasted temp paths vanish; the saved copy is the verification oracle). Committing the spec is the user's call.
5. **Handoff** - build from the spec via fe-next (never re-guess visuals from the image), then verify with verify-ui-against-design-headless using the saved image plus the spec's acceptance checklist.

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
| Reading px/hex values off the image | Snap to the repo scale/tokens; the image is structure, not truth |
| Asking about spacing/color the repo already answers | Infer it; the interview is for semantics only |
| Building straight from the image after the interview | Build from the spec file |
| Spec without an acceptance checklist | The checklist is what verify-ui-against-design-headless consumes |
| Interviewing as a dispatched agent | Halt with "needs a pre-dispatch intake spec" |

## Related

- **RELATED:** fe-next (the builder - consumes the spec)
- **RELATED:** verify-ui-against-design-headless (the oracle - consumes saved image + acceptance checklist)
