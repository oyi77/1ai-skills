#!/usr/bin/env bash
# audit-skills.sh — Source of truth for skill counts and structure.
#
# Walks the repo, counts SKILL.md files per top-level category, emits:
#   - SKILLS.json     : machine-readable catalog for AI agents
#   - stdout summary  : human-readable totals
#
# Usage: bash scripts/audit-skills.sh [--write]
#   --write   write SKILLS.json (default: stdout only)

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

WRITE=0
[[ "${1:-}" == "--write" ]] && WRITE=1

# Top-level dirs that hold skills (skip tooling dirs).
SKILL_DIRS=(
  agents automation content core cybersecurity data development
  devops financial integrations marketing mcp meta mindset operations
  productivity research sales trading
)
# Tooling / docs dirs (not skill homes).
TOOLING_DIRS=(docs hooks manifests references scripts)

total=0
declare -A counts

for d in "${SKILL_DIRS[@]}"; do
  if [[ -d "$d" ]]; then
    c=$(find "$d" -name "SKILL.md" 2>/dev/null | wc -l | tr -d ' ')
  else
    c=0
  fi
  counts[$d]=$c
  total=$((total + c))
done

# Pretty stdout summary
printf '\n=== 1ai-skills audit ===\n'
printf '%-15s %6s\n' "category" "skills"
printf '%-15s %6s\n' "---------------" "------"
for d in "${SKILL_DIRS[@]}"; do
  printf '%-15s %6d\n' "$d" "${counts[$d]}"
done
printf '%-15s %6s\n' "---------------" "------"
printf '%-15s %6d\n' "TOTAL" "$total"
printf '\nTooling dirs (no skills): %s\n' "${TOOLING_DIRS[*]}"

# JSON output. NOTE: deliberately deterministic — no timestamp — so CI
# can verify SKILLS.json is current with `git diff --quiet`. If you need
# a timestamp, generate one separately.
if [[ $WRITE -eq 1 ]]; then
  out="$ROOT/SKILLS.json"
  {
    printf '{\n'
    printf '  "total_skills": %d,\n' "$total"
    printf '  "category_count": %d,\n' "${#SKILL_DIRS[@]}"
    printf '  "categories": {\n'
    first=1
    for d in "${SKILL_DIRS[@]}"; do
      [[ $first -eq 0 ]] && printf ',\n'
      first=0
      printf '    "%s": %d' "$d" "${counts[$d]}"
    done
    printf '\n  },\n'
    printf '  "tooling_dirs": ['
    first=1
    for d in "${TOOLING_DIRS[@]}"; do
      [[ $first -eq 0 ]] && printf ', '
      first=0
      printf '"%s"' "$d"
    done
    printf ']\n'
    printf '}\n'
  } > "$out"
  printf '\nWrote %s\n' "$out"
fi
