#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SKILLS_SRC="${SKILLS_SRC:-$REPO_ROOT/skills}"
SKILLS_DEST="${SKILLS_DEST:-$HOME/.claude/skills}"

mkdir -p "$SKILLS_DEST"

linked=0
refreshed=0
backed_up=0
found=0

for src in "$SKILLS_SRC"/*/; do
  [ -d "$src" ] || continue
  src="${src%/}"
  found=$((found + 1))
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

# Reap our own stale links. The loop above only visits skills that still exist in
# the repo, so deleting or renaming one leaves a dangling symlink that nothing
# cleans up. A link is ours to reap only if it points into this repo AND the repo
# no longer has a skill by that name; other plugins' skills, .bak backups, and
# symlinks pointing outside the repo are never candidates -- a foreign broken
# link is not ours to delete. Set REAP=0 to skip.
reaped=0
if [ "$found" -eq 0 ]; then
  echo "install.sh: no skills found in $SKILLS_SRC -- skipping reap (refusing to treat an empty source as 'everything was deleted')."
elif [ "${REAP:-1}" = "1" ]; then
  for entry in "$SKILLS_DEST"/*; do
    [ -L "$entry" ] || continue
    name="$(basename "$entry")"
    target="$(readlink "$entry")"
    case "$target" in
      "$REPO_ROOT"/*) ;;
      *) continue ;;
    esac
    if [ -d "$SKILLS_SRC/$name" ]; then continue; fi
    rm "$entry"
    echo "  reap: $name (gone from repo, was -> $target)"
    reaped=$((reaped + 1))
  done
fi

echo "install.sh done. linked=$linked refreshed=$refreshed reaped=$reaped backed_up=$backed_up"

# Optional: also sync to Claude Desktop's Cowork session.
if [ "${1:-}" = "--all" ] || [ "${1:-}" = "--cowork" ] || [ "${COWORK:-0}" = "1" ]; then
  exec "$REPO_ROOT/scripts/sync-cowork.sh"
fi
