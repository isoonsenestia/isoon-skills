---
name: senestia-bug-intake
description: Use when triaging a customer-reported bug in Senestia's Atlassian (ACS, DDST, customer-service projects) and an engineering counterpart needs to be filed. Triggers on phrases like "create engineering ticket from this bug", "intake this customer report", "track [ACS-X] in [PE/APS/…]", or while working a customer-service ticket and needing the dev follow-up.
---

# Senestia Bug Intake

## Overview

Take a customer-reported bug from a Senestia customer-service Jira project, file the engineering counterpart on the correct PECS-board project with sprint + label + bidirectional link, and post a Thai short summary back on the source for customer support. The Thai summary is iterated with the user every run.

## When to Use

- User asks to "intake", "create engineering ticket from", or "track in [project]" a customer bug.
- Working a customer-service Jira ticket (ACS, DDST, etc.) and the dev counterpart is missing.
- Need cross-project bidirectional linking plus a Thai customer-facing reply.

**When NOT to use:**
- The bug already has a linked engineering ticket — check the source's links first.
- Source is not actionable as engineering work (pure support question) — comment on source only.
- Outside Senestia's Atlassian tenant — defaults won't match.

## The Pattern

### Step 1 — Read source + resolve cloudId

```
mcp__claude_ai_Atlassian__getAccessibleAtlassianResources   # pick the Senestia cloudId
mcp__claude_ai_Atlassian__getJiraIssue cloudId=… issueIdOrKey=<SOURCE-KEY>
```

Capture: summary, description, reporter, priority, encounter status. Keep them for the engineering body and the Thai summary.

### Step 2 — ASK the user (don't guess)

1. **Target engineering project key.** User's main board is **PECS** (boardId 562; sprints `PE Sprint N`). Candidates usually live under it — APS, KSW, ICDX, DDPD, CHOC, etc. Confirm which.
2. **Sprint name** — usually the active or upcoming `PE Sprint N`.
3. **Issue type** — Bug / Task / Story. **ASK; do not default.**
4. **Label** — default `2nd-backlogs` (plural, hyphen, lowercase) for support-originated bugs. Confirm.
5. **Assignee** — default current user via `atlassianUserInfo`. Confirm if otherwise.

Resolve the sprint ID by JQL on any existing issue in the target with that sprint:

```jql
project = TARGET AND sprint = "PE Sprint N"
```

Extract `customfield_10020[0].id` from the first hit.

### Step 3 — Create the engineering ticket

```
mcp__claude_ai_Atlassian__createJiraIssue
  cloudId=… projectKey=TARGET issueTypeName=<chosen>
  summary="[<Type>] <concise English title>"
  assignee_account_id=<assignee>
  labels=["2nd-backlogs"]
  additional_fields={"customfield_10020": <SPRINT_ID_INT>}
  description="<English markdown body>"
```

Description should include: Summary, `Reported via [SOURCE-KEY|url]`, Root cause (or "Under investigation"), Repository link if known.

### Step 4 — Bidirectional link

```
mcp__claude_ai_Atlassian__createIssueLink
  cloudId=… type="Action item"
  inwardIssue=<NEW-KEY>       # NEW reads "action item from SOURCE"
  outwardIssue=<SOURCE-KEY>   # SOURCE reads "has action item NEW"
```

### Step 5 — Thai short summary (mandatory, iterative)

Apply the style memory `feedback-thai-writing-style`: no casual intensifiers (`เป๊ะ`, `เลย`, `มากๆ`), prefer labeled sub-points (`สาเหตุ:`) over inline bold, avoid robotic translations of tech terms.

Suggested skeleton:

```
**สรุปสาเหตุและแนวทางแก้ (สั้น)**

**สาเหตุ**: <1-2 sentences in plain Thai>

**เงื่อนไขเกิด**:
* <bullet>
* <bullet>

**แนวทางแก้**: <1 sentence>
* Tech ticket: [NEW-KEY|url] (Sprint name)
```

**Draft → present → revise loop.** Show the draft to the user *before* posting. Apply their wording edits. Re-present. Repeat until the user says **"enough for feedback"** (or equivalent — "ok ship it", "save", "good"). Then post via `addCommentToJiraIssue`.

If the feedback reveals a new persistent style rule, append it to `feedback-thai-writing-style.md` after the user signals enough.

### Step 6 — Report

| Field | Value |
|---|---|
| Source | [SOURCE-KEY](url) |
| Engineering | [NEW-KEY](url) |
| Sprint | PE Sprint N |
| Label | 2nd-backlogs |
| Issue type | Bug / Task / Story |
| Link | NEW **action item from** SOURCE |

## Quick Reference

| Field | How to resolve |
|---|---|
| Sprint custom field id | `customfield_10020` |
| Sprint name → ID | JQL `project = X AND sprint = "PE Sprint N"` → first hit's `customfield_10020[0].id` |
| Link type name | `Action item` |
| Default label | `2nd-backlogs` (plural, hyphen, lowercase) |
| Default assignee | `atlassianUserInfo.account_id` |
| Main board | PECS, boardId 562, sprints `PE Sprint N` |
| Customer-service source projects | ACS (appointment), DDST (daily-dashboard support), plus other service-desk projects |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Passing `customfield_10020` as sprint name string | It's an integer sprint ID; resolve via JQL first |
| Using `linkType` / `inwardIssueKey` keys in `createIssueLink` | The MCP tool wants `type`, `inwardIssue`, `outwardIssue` (no `Key` suffix, camelCase) |
| Spelling label `2nd-backlog` (singular) | Use `2nd-backlogs` (plural) — Senestia canonical |
| Defaulting target project to APS for every bug | ASK — PECS board covers many engineering projects |
| Defaulting issue type to Bug | ASK every time; not all engineering counterparts are bugs |
| Posting Thai summary on the first draft | Iterate with user until "enough for feedback" |
| Trying to edit a posted comment via MCP | No `editComment` exists; post a corrected new comment if needed |
| Skipping bidirectional link verification | After `createIssueLink`, both tickets should show the link; confirm before reporting |

## Related

- **REQUIRED BACKGROUND:** `feedback-thai-writing-style` memory — Thai copy style rules.
- **RELATED:** `review` — for the engineering ticket's eventual PR review.
