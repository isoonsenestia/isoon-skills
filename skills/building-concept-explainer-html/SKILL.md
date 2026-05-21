---
name: building-concept-explainer-html
description: Use when asked to build a single-file interactive HTML page that teaches a concept — prompts like "create an interactive page about X", "make HTML so I can study this", "build a visual learning page for this topic", or after producing research/wiki content that the user wants to study visually.
---

# Building Concept-Explainer HTML

## Overview

A concept-explainer HTML page is a **learning artifact**, not a slide deck. Its job: compress a topic into one self-contained file the reader can scan, click through, and walk away from with a working mental model. Every interaction must *reveal information* — decoration that doesn't teach is wrong.

## When to Use

- User asks "create an interactive page about X", "make HTML to learn X", "build a learning page for X"
- You just produced research or wiki content and the user wants a visual study companion for it
- The concept has 4+ distinct sub-parts that benefit from named, comparable representations

**When NOT to use:**
- A paragraph of Markdown would suffice — don't reach for HTML
- The concept is purely a chart or diagram — use the right tool, not HTML
- The user actually needs a real app — build one, not a single file

## The Pattern

### Eight beats, in order

1. **Hero + meta-grid** — title, one-sentence tagline, 3–4 metadata cells (author / version / scope / scale) so the reader is oriented in 5 seconds.
2. **One-liner framing card** — the entire concept compressed to a single styled paragraph. Visually distinct (gradient or accent border).
3. **The mechanism** — *how it works* introduced with the page's first interactive element.
4. **Anatomy view** — pick a *canonical artifact* (code snippet, config, protocol message, file layout) and make every part clickable; a side panel reveals each region's role + why it's there + how it breaks.
5. **Walk-through / pipeline** — clickable or playable step sequence for any process, flow, or lifecycle the concept involves.
6. **Comparison columns** — side-by-side ✓/✗ or X-vs-Y cards. This is how you cut through fuzzy mental models that conflate adjacent ideas.
7. **Pitfalls / common mistakes** — table form, ideally with *mini interactive demos* (a button that reproduces the bad case) instead of essays.
8. **Term map / quick reference** — every term, what it is, where it's defined. The page's index.

Not all 8 always apply, but skipping 1, 2, or 8 is almost always wrong.

### The seven UI primitives

| Primitive | Use when |
|-----------|----------|
| Sidebar nav with scroll-spy | Page has ≥ 5 sections |
| Hero + meta-grid (3–4 cells) | Always — orient before depth |
| One-liner gradient card | "If you remember one thing" line |
| Pipeline / flow (clickable stages) | Concept is sequential (workflow, lifecycle) |
| Anatomy view (clickable regions) | The key artifact is *structured* — code, config, message |
| Expandable cards grid | 5–20 peer items (skills, options, components) |
| Side-by-side comparison columns | Two ideas readers conflate; force the contrast |

### Technical baseline (non-negotiable)

- **Single `.html` file**, zero external network requests (no CDN, no Google Fonts, no framework)
- **Vanilla JS** in one `<script>` at the end of body
- **Dark mode default**, monospace for code, system sans-serif for body
- **CSS custom properties** at `:root` so the whole page recolors from one place
- **Scroll-spy** sidebar links and `scroll-margin-top` on sections
- **Responsive** at ~900px: sidebar collapses, multi-column grids reflow to single

### Splitting into multiple pages

Use two cross-linked pages when the concept has *two distinct audiences or facets* — e.g. user-facing workflow vs. underlying mechanics. Each page gets its own sidebar with a "→ Other page" link at the top. Don't split for length alone — split for *role*.

## Quick Reference

| Goal | Primitive |
|------|-----------|
| Show how something works | Pipeline + clickable stages |
| Dissect a key artifact | Anatomy view with clickable color-coded regions |
| Enumerate peer items | Expandable cards grid |
| Force a comparison | Side-by-side columns with ✓/✗ headers |
| Make terms findable | Term map table at the end |
| Orient the reader fast | Hero + meta-grid + one-liner card |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Wall of prose with no nav | Sidebar with scroll-spy; line length ≤ 80ch; break to bullets |
| "Interactive" elements that only animate | Every click/hover must reveal information the reader couldn't get from reading |
| Pitfalls section as essays | Convert to mini demos — a button the reader presses to *trigger* the bad case |
| Single page when concept has two facets | Split into two cross-linked pages (user-facing + mechanics) |
| Workflow-summary in hero/title | Lead with the *idea*, not "this page does X then Y" |
| Decoration without function | Strip every color/animation/hover effect that doesn't teach |
| No term map | A learner can't look up what they half-remember without it |
| Fancy framework, fragile load | Single file, vanilla — works from filesystem, survives offline |

## Related

- **RELATED:** save-skill — for packaging this technique (or a refinement) as a future skill
- **RELATED:** repo-wiki — wiki sources are the most common upstream feed for these pages
