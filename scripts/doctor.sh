#!/usr/bin/env bash
set -uo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
issues=0

scan_dest() {
  local dest="$1"
  local label="$2"
  if [ ! -d "$dest" ]; then
    echo "[$label] $dest does not exist — skipping."
    return 0
  fi
  echo "[$label] Scanning $dest..."
  for entry in "$dest"/*; do
    [ -e "$entry" ] || [ -L "$entry" ] || continue
    local name
    name="$(basename "$entry")"

    if [ -L "$entry" ]; then
      if [ ! -e "$entry" ]; then
        local target
        target="$(readlink "$entry")"
        echo "  BROKEN: $name -> $target"
        issues=$((issues + 1))
      fi
    elif [ -d "$entry" ]; then
      case "$name" in
        *.bak.*) ;;
        *)
          # In Cowork, non-symlink dirs are expected (built-ins / uploaded skills).
          # Only flag drift in the CLI destination.
          if [ "$label" = "cli" ]; then
            echo "  NOT-A-SYMLINK: $name (potential drift — not from the repo)"
            issues=$((issues + 1))
          fi
          ;;
      esac
    fi
  done
}

scan_dest "$SKILLS_DEST" "cli"

COWORK_BASE="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
if [ -d "$COWORK_BASE" ]; then
  SESSION="$(ls -t "$COWORK_BASE" 2>/dev/null | head -n1 || true)"
  if [ -n "${SESSION:-}" ]; then
    ACCOUNT="$(ls -t "$COWORK_BASE/$SESSION" 2>/dev/null | head -n1 || true)"
    if [ -n "${ACCOUNT:-}" ]; then
      scan_dest "$COWORK_BASE/$SESSION/$ACCOUNT/skills" "cowork"
    fi
  fi
fi

if [ "$issues" -eq 0 ]; then
  echo "All good."
else
  echo "Found $issues issue(s)."
fi
