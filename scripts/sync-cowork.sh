#!/usr/bin/env bash
# sync-cowork.sh — mirror repo skills into the newest Claude Desktop ("Cowork") session.
#
# Cowork stores skills at:
#   ~/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin/
#     <sessionId>/<accountId>/skills/<name>/SKILL.md
# That directory is a server-synced runtime cache, so a future desktop-app update may
# wipe / restructure it. We symlink into the newest session by mtime and skip any name
# that already exists there with non-repo content (Cowork built-ins, manually uploaded
# user skills) so we never shadow them.
set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
SKILLS_SRC="${SKILLS_SRC:-$REPO_ROOT/skills}"

# Allow override (tests) but otherwise auto-detect.
if [ -z "${SKILLS_DEST:-}" ]; then
  COWORK_BASE="$HOME/Library/Application Support/Claude/local-agent-mode-sessions/skills-plugin"
  if [ ! -d "$COWORK_BASE" ]; then
    echo "sync-cowork.sh: Cowork base not found at $COWORK_BASE — skipping (no-op)."
    exit 0
  fi
  SESSION="$(ls -t "$COWORK_BASE" 2>/dev/null | head -n1 || true)"
  if [ -z "${SESSION:-}" ]; then
    echo "sync-cowork.sh: no Cowork sessions yet — skipping (no-op)."
    exit 0
  fi
  ACCOUNT="$(ls -t "$COWORK_BASE/$SESSION" 2>/dev/null | head -n1 || true)"
  if [ -z "${ACCOUNT:-}" ]; then
    echo "sync-cowork.sh: no Cowork account dirs under $SESSION — skipping (no-op)."
    exit 0
  fi
  SKILLS_DEST="$COWORK_BASE/$SESSION/$ACCOUNT/skills"
fi

if [ ! -d "$SKILLS_DEST" ]; then
  echo "sync-cowork.sh: $SKILLS_DEST does not exist — skipping (no-op)."
  exit 0
fi

echo "sync-cowork.sh: target=$SKILLS_DEST"

linked=0
refreshed=0
backed_up=0
skipped=0

found=0

for src in "$SKILLS_SRC"/*/; do
  [ -d "$src" ] || continue
  src="${src%/}"
  found=$((found + 1))
  name="$(basename "$src")"
  dest="$SKILLS_DEST/$name"

  if [ -L "$dest" ]; then
    target="$(readlink "$dest")"
    case "$target" in
      "$REPO_ROOT"/*)
        ln -sfn "$src" "$dest"
        refreshed=$((refreshed + 1))
        ;;
      *)
        echo "  skip: $name (existing symlink points outside repo: $target)"
        skipped=$((skipped + 1))
        ;;
    esac
  elif [ -e "$dest" ]; then
    # Real directory / file already there — likely a Cowork built-in or user-uploaded
    # skill that the desktop owns. Never overwrite; just warn.
    echo "  skip: $name (exists in Cowork, not ours to touch)"
    skipped=$((skipped + 1))
  else
    ln -s "$src" "$dest"
    linked=$((linked + 1))
  fi
done

# Reap our own stale links. The loop above only visits skills that still exist in
# the repo, so deleting or renaming one leaves a dangling symlink that no script
# cleans up -- doctor.sh reports it as BROKEN until someone removes it by hand.
# A link is ours to reap only if it points into this repo AND the repo no longer
# has a skill by that name; Cowork built-ins, uploaded skills, and symlinks
# pointing elsewhere are never candidates. Set REAP=0 to skip.
reaped=0
if [ "$found" -eq 0 ]; then
  echo "sync-cowork.sh: no skills found in $SKILLS_SRC -- skipping reap (refusing to treat an empty source as 'everything was deleted')."
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

echo "sync-cowork.sh done. linked=$linked refreshed=$refreshed skipped=$skipped reaped=$reaped backed_up=$backed_up"
