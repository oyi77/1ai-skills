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
  agents content core development integrations marketing meta mindset
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
  # Canonical skill name is the frontmatter `name` field (the same identity
  # SKILLS.json is keyed on), NOT the directory basename. Nested grouping dirs
  # (content/video/gen -> video-gen, trading/executor -> trading-executor,
  # sales/pipeline -> sales-pipeline) would otherwise collide on short
  # basenames like `strategy` / `ops` / `team`.
  skill_name="$(sed -n 's/^name:[[:space:]]*//p' "$skill_file" | head -n1)"
  [ -n "$skill_name" ] || skill_name="$(basename "$skill_dir")"

  # Skip if name collision (identical frontmatter names in two dirs)
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

# The source tree is categorized but the runtime is flat. Rebase copied
# relative SKILL.md links to canonical frontmatter names; leave source,
# frontmatter, fenced examples, and non-SKILL links untouched. This also
# repairs unchanged copies when upgrading sync.
if ! $DRY_RUN; then
  python3 - "$REPO_ROOT" "$TARGET" <<'PY'
import re
import sys
from pathlib import Path

repo, runtime = Path(sys.argv[1]), Path(sys.argv[2])
sources = list(repo.glob("*/*/**/SKILL.md"))
names = {}
for source in sources:
    name = re.search(r"^name:\s*[\"']?([a-z0-9-]+)", source.read_text(), re.MULTILINE)
    if name:
        names[source.resolve()] = name.group(1)

for source in sources:
    name = names.get(source.resolve())
    if not name:
        continue
    copied = runtime / name / "SKILL.md"
    if not copied.is_file():
        continue

    lines = copied.read_text().splitlines(keepends=True)
    frontmatter, fence = True, False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if index == 0 and stripped == "---":
            continue
        if frontmatter:
            if stripped == "---":
                frontmatter = False
            continue
        if re.match(r"^(```|~~~)", stripped):
            fence = not fence
            continue
        if fence:
            continue

        def rebase(match):
            url = match.group(1)
            path, separator, fragment = url.partition("#")
            target = (source.parent / path).resolve()
            if target not in names:
                return match.group(0)
            rebased = "../" + names[target] + "/SKILL.md"
            return "](" + rebased + separator + fragment + ")"

        lines[index] = re.sub(r"\]\((\.{1,2}/[^)\s]+/SKILL\.md(?:#[^)\s]*)?)\)", rebase, line)

    rebased_text = "".join(lines)
    if rebased_text != copied.read_text():
        copied.write_text(rebased_text)
PY
fi

# Clean: remove skills from target that no longer exist in source.
# Skills installed by OTHER tools (Orca, Paseo, terminal-value, ...) also live
# in this directory and must never be removed by this script. Names matching
# EXTERNAL_ALLOWLIST (or carrying a foreign manager marker) are skipped.
EXTERNAL_ALLOWLIST=(
  computer-use cua-driver orca-cli orca-per-workspace-env orchestration
  paseo paseo-advisor paseo-committee paseo-handoff paseo-help paseo-plugin
  terminal-value terminalvalue-io
)

is_external() {
  local n="$1"
  for ext in "${EXTERNAL_ALLOWLIST[@]}"; do
    [ "$n" = "$ext" ] && return 0
  done
  # Any dir carrying a foreign manager marker file is also off-limits.
  compgen -G "$TARGET/$n/.*-managed-files.json" >/dev/null 2>&1 && return 0
  return 1
}

if $CLEAN; then
  echo ""
  echo "Cleaning stale skills..."
  # NOTE: iterate WITHOUT a trailing slash. `rm -rf path/` dereferences a
  # symlink and deletes the CONTENTS OF ITS TARGET (POSIX), which would
  # silently gut an external plugin such as ~/.opencode/understand-anything.
  for installed in "$TARGET"/*; do
    [ -e "$installed" ] || [ -L "$installed" ] || continue
    name="$(basename "$installed")"
    [ -n "${SOURCE_SKILLS[$name]+x}" ] && continue

    # Symlinked skills are owned by another tool; never touch them.
    if [ -L "$installed" ]; then
      echo "  ◦ kept (symlink to external skill): $name"
      continue
    fi
    [ -d "$installed" ] || continue

    if is_external "$name"; then
      echo "  ◦ kept (externally managed): $name"
      continue
    fi

    if $DRY_RUN; then
      echo "  [DRY] would remove: $name"
    else
      # No trailing slash: removes the directory itself, never a target.
      rm -rf -- "$installed"
      echo "  ✗ removed: $name"
    fi
    ((REMOVED++)) || true
  done
fi

echo ""
echo "Done: $SYNCED synced, $SKIPPED skipped (up to date or collision)"
if $CLEAN; then
  echo "      $REMOVED stale skills removed"
fi
