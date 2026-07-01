#!/usr/bin/env bash
# sync-skills.sh — Sync ALL 1ai-skills into ~/.agents/skills/
# Usage: ./scripts/sync-skills.sh [--dry-run] [--clean]
#
# Scans ALL SKILL.md files across all categories (content, core, development,
# marketing, cybersecurity, etc.) and copies to ~/.agents/skills/<skill-name>/

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

# Category directories that contain skills
CATEGORIES=(
  content core development integrations marketing meta mindset
  operations productivity research sales trading data devops
  cybersecurity automation financial mcp
)

# Find all SKILL.md across all categories (flat + nested)
SEARCH_DIRS=()
for cat in "${CATEGORIES[@]}"; do
  [ -d "$REPO_ROOT/$cat" ] && SEARCH_DIRS+=("$REPO_ROOT/$cat")
done

mapfile -t SKILLS < <(find "${SEARCH_DIRS[@]}" -name "SKILL.md" -type f | sort)

SYNCED=0
SKIPPED=0
REMOVED=0

echo "Source: $REPO_ROOT (all categories)"
echo "Target: $TARGET"
echo "Skills found: ${#SKILLS[@]}"
echo ""

# Build list of skill names from source
declare -A SOURCE_SKILLS

for skill_file in "${SKILLS[@]}"; do
  skill_dir="$(dirname "$skill_file")"
  skill_name="$(basename "$skill_dir")"

  # Skip if name collision (prefer content/ over others)
  if [ -n "${SOURCE_SKILLS[$skill_name]+x}" ]; then
    ((SKIPPED++)) || true
    continue
  fi
  SOURCE_SKILLS["$skill_name"]=1

  src="$skill_dir"
  dst="$TARGET/$skill_name"

  # Check if sync needed (compare SKILL.md mtime)
  if [ -f "$dst/SKILL.md" ]; then
    if [ "$skill_file" -ot "$dst/SKILL.md" ] 2>/dev/null; then
      ((SKIPPED++)) || true
      continue
    fi
  fi

  if $DRY_RUN; then
    echo "  [DRY] would sync: $skill_name"
  else
    rm -rf "$dst"
    cp -r "$src" "$dst"
    lines=$(wc -l < "$dst/SKILL.md")
    echo "  ✓ $skill_name (${lines}L)"
  fi
  ((SYNCED++)) || true
done

# Clean: remove skills from target that no longer exist in source
if $CLEAN; then
  echo ""
  echo "Cleaning stale skills..."
  for installed in "$TARGET"/*/; do
    [ -d "$installed" ] || continue
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
echo "Done: $SYNCED synced, $SKIPPED skipped (up to date or collision)"
if $CLEAN; then
  echo "      $REMOVED stale skills removed"
fi
