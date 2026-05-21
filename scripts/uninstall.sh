#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"

clean_dest() {
  local dest="$1"
  local label="$2"
  [ -d "$dest" ] || return 0

  local removed=0 skipped=0
  for entry in "$dest"/*; do
    [ -L "$entry" ] || continue
    local target
    target="$(readlink "$entry")"
    case "$target" in
      "$REPO_ROOT"/*)
        rm "$entry"
        removed=$((removed + 1))
        ;;
      *)
        skipped=$((skipped + 1))
        ;;
    esac
  done
  echo "uninstall.sh [$label]: removed=$removed skipped=$skipped ($dest)"
}

clean_dest "$SKILLS_DEST" "cli"

# Also clean the newest Cowork session, if present.
COWORK_BASE="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
if [ -d "$COWORK_BASE" ]; then
  SESSION="$(ls -t "$COWORK_BASE" 2>/dev/null | head -n1 || true)"
  if [ -n "${SESSION:-}" ]; then
    ACCOUNT="$(ls -t "$COWORK_BASE/$SESSION" 2>/dev/null | head -n1 || true)"
    if [ -n "${ACCOUNT:-}" ]; then
      clean_dest "$COWORK_BASE/$SESSION/$ACCOUNT/skills" "cowork"
    fi
  fi
fi
