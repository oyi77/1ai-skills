#!/usr/bin/env bash
# sync-skills.sh — Sync 1ai-skills repo into ~/.agents/skills/
# Usage: ./scripts/sync-skills.sh [--dry-run] [--clean]
#
# Scans all SKILL.md files in content/ (including nested subdirs like content/video/)
# and copies them to ~/.agents/skills/<skill-name>/

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
DRY_RUN=false
CLEAN=false

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=true ;;
    --clean) CLEAN=true ;;
  esac
done

# Find all SKILL.md files in content/ (flat + nested)
mapfile -t SKILLS < <(find "$REPO_ROOT/content" -name "SKILL.md" -type f | sort)

SYNCED=0
SKIPPED=0
REMOVED=0

echo "Source: $REPO_ROOT/content/"
echo "Target: $TARGET"
echo "Skills found: ${#SKILLS[@]}"
echo ""

# Build list of skill names from source
declare -A SOURCE_SKILLS

for skill_file in "${SKILLS[@]}"; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"
  SOURCE_SKILLS["$skill_name"]=1

  src="$skill_dir"
  dst="$TARGET/$skill_name"

  # Check if sync needed (compare SKILL.md mtime)
  if [ -f "$dst/SKILL.md" ]; then
    if [ "$skill_file" -ot "$dst/SKILL.md" ] 2>/dev/null; then
      # Installed is newer — skip
      ((SKIPPED++)) || true
      continue
    fi
  fi

  if $DRY_RUN; then
    echo "  [DRY] would sync: $skill_name"
  else
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "  ✓ synced: $skill_name ($(wc -l < "$dst/SKILL.md")L)"
  fi
  ((SYNCED++)) || true
done

# Clean: remove skills from target that no longer exist in source
if $CLEAN; then
  echo ""
  echo "Cleaning stale skills..."
  for installed in "$TARGET"/*/; do
    name="$(basename "$installed")"
    if [ -z "${SOURCE_SKILLS[$name]+x}" ]; then
      if $DRY_RUN; then
        echo "  [DRY] would remove: $name"
      else
        rm -rf "$installed"
        echo "  ✗ removed: $name"
      fi
      ((REMOVED++)) || true
    fi
  done
fi

echo ""
echo "Done: $SYNCED synced, $SKIPPED skipped (up to date)"
if $CLEAN; then
  echo "      $REMOVED stale skills removed"
fi
