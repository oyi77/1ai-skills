#!/bin/bash
set -e

echo "[pre-commit] Validating SKILL.md files..."

CHANGED_SKILLS=$(git diff --cached --name-only | grep "SKILL.md$" || true)

if [ -z "$CHANGED_SKILLS" ]; then
  echo "[pre-commit] No SKILL.md files changed. Skipping validation."
  exit 0
fi

ERRORS=0

for skill_file in $CHANGED_SKILLS; do
  echo "[pre-commit] Checking: $skill_file"

  if ! head -1 "$skill_file" | grep -q "^---$"; then
    echo "[pre-commit] ERROR: Missing frontmatter in $skill_file"
    ERRORS=$((ERRORS + 1))
    continue
  fi
  
    if ! grep -q "^name:" "$skill_file"; then
    echo "[pre-commit] ERROR: Missing 'name' in frontmatter: $skill_file"
    ERRORS=$((ERRORS + 1))
  fi
  
  if ! grep -q "^description:" "$skill_file"; then
    echo "[pre-commit] ERROR: Missing 'description' in frontmatter: $skill_file"
    ERRORS=$((ERRORS + 1))
  fi
  
    if ! grep -q "^## Overview\|^## When to Use\|^## Process\|^## Verification" "$skill_file"; then
    echo "[pre-commit] WARNING: Missing recommended sections in $skill_file"
    echo "[pre-commit]   Required: Overview, When to Use, Process, Verification"
  fi
  
    if grep "^description:" "$skill_file" | grep -qv "Use when"; then
    echo "[pre-commit] WARNING: description should include 'Use when' trigger phrases: $skill_file"
  fi
  
  echo "[pre-commit] ✓ $skill_file passed basic validation"
done

if [ $ERRORS -gt 0 ]; then
  echo "[pre-commit] FAILED: $ERRORS error(s) found. Fix before committing."
  exit 1
fi

echo "[pre-commit] All SKILL.md files validated successfully."
