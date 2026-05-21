#!/usr/bin/env bash
# continuous-learning/evaluate-session.sh — Stop-hook activator.
#
# Prompts the user whether anything from the just-ended session is worth
# turning into a reusable skill. If yes, opens $EDITOR on a stub at
# ~/.claude/skills/learned/draft-<timestamp>.md.
#
# Headless-safe: skips the prompt with timeout when stdin/stdout is not a tty
# or CLAUDE_NONINTERACTIVE=1.

set -uo pipefail

cat >/dev/null  # discard hook stdin

LEARNED_DIR="${HOME}/.claude/skills/learned"
mkdir -p "$LEARNED_DIR" || exit 0

# Non-interactive guard — Stop hook may not have a usable tty.
if [ -n "${CLAUDE_NONINTERACTIVE:-}" ] || [ ! -t 0 ] || [ ! -t 1 ]; then
  exit 0
fi

# Best-effort prompt with timeout — don't block session teardown.
echo "" >&2
echo "[continuous-learning] Anything from this session worth turning into a skill? (y/N)" >&2
read -r -t 8 ans 2>/dev/null || ans=""

case "${ans:-}" in
  y|Y|yes|YES)
    stamp=$(date -u +"%Y%m%d-%H%M%S")
    draft="${LEARNED_DIR}/draft-${stamp}.md"
    cat > "$draft" <<'STUB_EOF'
---
name: REPLACE-WITH-KEBAB-NAME
description: Use when REPLACE — describe the trigger condition that should re-activate this skill.
---

# REPLACE — One-line rule

The rule (imperative, one sentence).

**Why:** The concrete past incident this rule prevents from recurring.

**How to apply:** When/where this guidance kicks in.

## Anti-example (optional)

What going wrong looks like, so the reader recognizes the failure mode.
STUB_EOF
    editor="${EDITOR:-vi}"
    echo "[continuous-learning] Opening draft: $draft" >&2
    "$editor" "$draft" </dev/tty >/dev/tty 2>&1 || true
    echo "[continuous-learning] Draft saved. Rename to ${LEARNED_DIR}/<skill-name>/SKILL.md when ready." >&2
    ;;
  *)
    : # no-op
    ;;
esac

exit 0
