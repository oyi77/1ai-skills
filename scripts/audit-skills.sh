#!/usr/bin/env bash
# audit-skills.sh — Source of truth for skill counts and structure.
#
# Walks the repo, counts SKILL.md files per top-level category, emits:
#   - SKILLS.json     : machine-readable catalog for AI agents
#   - stdout summary  : human-readable totals
#
# Usage: bash scripts/audit-skills.sh [--write]
#   --write   write SKILLS.json (default: stdout only)
#
# If SKILLS.json already contains a "skills" array (enriched format from
# lint-skills.py), the --write flag merges fresh counts into it instead
# of overwriting. This keeps the per-skill metadata intact.

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
#
# If the existing SKILLS.json has a "skills" array (enriched format from
# lint-skills.py --write), merge fresh counts into it. Otherwise write
# count-only format.
if [[ $WRITE -eq 1 ]]; then
  out="$ROOT/SKILLS.json"
  HAS_ENRICHED=0
  if [[ -f "$out" ]] && python3 -c "import json,sys; d=json.load(open(sys.argv[1])); assert 'skills' in d" "$out" 2>/dev/null; then
    HAS_ENRICHED=1
  fi

  if [[ $HAS_ENRICHED -eq 1 ]]; then
    # Build categories JSON for python
    CATS_JSON="{"
    first=1
    for d in "${SKILL_DIRS[@]}"; do
      [[ $first -eq 0 ]] && CATS_JSON+=","
      first=0
      CATS_JSON+="\"$d\":${counts[$d]}"
    done
    CATS_JSON+="}"

    TOOLING_JSON="["
    first=1
    for d in "${TOOLING_DIRS[@]}"; do
      [[ $first -eq 0 ]] && TOOLING_JSON+=","
      first=0
      TOOLING_JSON+="\"$d\""
    done
    TOOLING_JSON+="]"

    python3 -c "
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
data['total_skills'] = int(sys.argv[2])
data['category_count'] = int(sys.argv[3])
data['categories'] = json.loads(sys.argv[4])
data['tooling_dirs'] = json.loads(sys.argv[5])
with open(sys.argv[1], 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')
" "$out" "$total" "${#SKILL_DIRS[@]}" "$CATS_JSON" "$TOOLING_JSON"
    printf '\nMerged counts into enriched %s\n' "$out"
  else
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
fi
