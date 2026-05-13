#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"

removed=0
skipped=0

for entry in "$SKILLS_DEST"/*; do
  [ -L "$entry" ] || continue
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

echo "uninstall.sh done. removed=$removed skipped=$skipped"
