---
name: component-from-figma
disable-model-invocation: true
description: Use when asked to plan and build one his-design-system component from a Jira ticket plus either a `docs/specs/<Name>.spec.md` build spec or labelled Figma sheet nodes (component/anatomy/example/props) - "/component-from-figma", "build <Name> from this ticket and these nodes", "start HIS-xxx", HIS-xxx component tickets. Runs worktree + subagent-driven flow on the repo's figma-conformance skill.
---

Build the component described by the arguments.

Repo: `/Users/io/repos/his-design-system`. If the session cwd is elsewhere, work there via absolute paths;
the `figma-conformance` skill is at `.claude/skills/figma-conformance/SKILL.md` inside that repo - read it
directly when it is not loaded as a skill.

## Inputs

Parse from the arguments above:
- Jira ticket URL or key
- Component name
- Figma dev-mode node URLs, each labelled: component, anatomy, example, props

**Check `docs/specs/<Name>.spec.md` before asking for any of it.** A spec there already carries
the source node ids, the variant registry, the verified token table per anatomy part and the
settled prop contract, so the labelled URLs are not needed and the design questions are answered.
Only when there is no spec is the component node required; ask for whichever labelled URLs are
missing, in a single question, then proceed.

## Workflow

1. **Plan first, and let the spec decide how.** No code before the plan is agreed, either way.
   - **A `docs/specs/<Name>.spec.md` exists:** read it in full, plus
     `docs/specs/props-conventions.md`, which holds the cross-cutting prop decisions every spec
     cites. It is the plan's source - the spec supersedes extraction, and `figma-conformance`
     ground rule 10 states the precedence and what is left to do. **Skip brainstorming**;
     re-opening settled design questions is how a build session loses a day. Go straight to
     `superpowers:writing-plans`, one task per deliverable, each citing the spec section that
     governs it. The spec's own "Still open" section is the only list of things not yet decided,
     so nothing outside it needs a decision.
   - **No spec:** `superpowers:brainstorming`, then `superpowers:writing-plans`.
2. Isolate the work with `superpowers:using-git-worktrees` (worktrees live in
   `.claude/worktrees/`). Branch name carries the ticket key.
3. `figma-conformance` is the build skill. Its ground rules, Anatomy/Scaffold steps, and
   per-node loop govern every extraction and edit, including the spec precedence and the
   conflict report in ground rule 10.
4. Execute the plan with `superpowers:subagent-driven-development`, one plan task per
   subagent. Tell each subagent to load `figma-conformance` and to keep comments
   why-not-what with no references to plan tasks or ticket ids. **Where a spec exists, hand
   each subagent the spec path and the sections its task depends on**, and say that the spec
   replaces re-sampling. A subagent gets a fresh context and reads only what it is handed, so
   one that is not told will re-derive the token table from Figma.
5. Stories match the house shape. Read
   `packages/react/src/components/input/Input.stories.tsx` and
   `packages/react/src/components/input/Input.mdx` as the template before writing any story,
   and follow the "Storybook structure" section of `docs/rulebook.gen.md`.
6. Finish with `superpowers:verification-before-completion`, then review your own diff through
   `logic-first-review`. Commits stay local until your human partner says push.

## Deliverables

- Component, stories, both docs pages, gallery + visual test, a11y suite, changeset.
- The node conflict report, in the commit body or ledger entry.
