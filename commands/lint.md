# /lint — Lint and fix skill content quality

Run content linter on skills and auto-fix common issues.

## Steps

1. Run `python3 scripts/lint-skills.py` — content linting
2. Run `python3 scripts/lint-skills.py --write` — auto-fix mode
3. Check for:
   - Missing YAML frontmatter fields
   - Inconsistent formatting
   - Template placeholder text
   - Missing sections
   - Description quality
4. Report fixes applied and remaining issues
