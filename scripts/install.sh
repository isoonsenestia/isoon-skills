#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_SRC="${SKILLS_SRC:-$REPO_ROOT/skills}"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"

mkdir -p "$SKILLS_DEST"

linked=0
refreshed=0
backed_up=0

for src in "$SKILLS_SRC"/*/; do
  [ -d "$src" ] || continue
  src="${src%/}"
  name="$(basename "$src")"
  dest="$SKILLS_DEST/$name"

  if [ -L "$dest" ]; then
    ln -sfn "$src" "$dest"
    refreshed=$((refreshed + 1))
  elif [ -e "$dest" ]; then
    backup="$dest.bak.$(date +%s)"
    mv "$dest" "$backup"
    ln -s "$src" "$dest"
    backed_up=$((backed_up + 1))
    echo "Backed up $name -> $backup"
  else
    ln -s "$src" "$dest"
    linked=$((linked + 1))
  fi
done

echo "install.sh done. linked=$linked refreshed=$refreshed backed_up=$backed_up"
