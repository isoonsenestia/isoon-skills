#!/usr/bin/env bash
set -uo pipefail

SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"
issues=0

echo "Scanning $SKILLS_DEST..."

for entry in "$SKILLS_DEST"/*; do
  # Skip if the glob did not match anything
  [ -e "$entry" ] || [ -L "$entry" ] || continue
  name="$(basename "$entry")"

  if [ -L "$entry" ]; then
    if [ ! -e "$entry" ]; then
      target="$(readlink "$entry")"
      echo "  BROKEN: $name -> $target"
      issues=$((issues + 1))
    fi
  elif [ -d "$entry" ]; then
    case "$name" in
      *.bak.*) ;;
      *)
        echo "  NOT-A-SYMLINK: $name (potential drift — not from the repo)"
        issues=$((issues + 1))
        ;;
    esac
  fi
done

if [ "$issues" -eq 0 ]; then
  echo "All good."
else
  echo "Found $issues issue(s)."
fi
