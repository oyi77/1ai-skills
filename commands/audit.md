# /audit — Run comprehensive skill library audit

Validate the entire 1ai-skills library for quality, consistency, and completeness.

## Steps

1. Run `python3 scripts/validate-skills.py` — structural validation
2. Run `bash scripts/audit-skills.sh` — count verification
3. Check for:
   - Orphaned skills (on disk, not in SKILLS.json)
   - Missing skills (in SKILLS.json, not on disk)
   - Duplicate descriptions
   - Broken internal `/skills/` links
   - Placeholder content
   - Missing required sections (When to Use, Overview)
   - Short descriptions (<30 chars)
4. Generate audit report with severity ratings
5. Suggest fixes for each issue found

## Quality Gates

- [ ] All SKILL.md files pass structural validation
- [ ] Zero orphaned or missing skills
- [ ] Zero duplicate descriptions
- [ ] Zero broken internal links
- [ ] Zero placeholder content
- [ ] All skills have When to Use section
- [ ] All descriptions ≥30 chars
