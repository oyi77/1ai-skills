# Definition of Done for Skills

A skill is DONE when ALL of these are true:

## Structure Done

- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] All required fields present (name, description, domain)
- [ ] All required sections present (When to Use, Workflow, Verification)
- [ ] `python3 scripts/validate-skills.py` passes
- [ ] `bash scripts/audit-skills.sh --write` updates SKILLS.json

## Content Done

- [ ] Real workflow steps (not template placeholders)
- [ ] Imperative language throughout
- [ ] Concrete examples and commands
- [ ] Under 500 lines
- [ ] Description is action-oriented (50-200 chars)

## Quality Done

- [ ] No duplicate description with existing skills
- [ ] No broken internal links
- [ ] Security checklist reviewed (if applicable)
- [ ] Skill quality checklist passes
- [ ] Spot-checked by reading the full SKILL.md

## Integration Done

- [ ] SKILLS.json updated with new skill entry
- [ ] Skill discoverable via `/find` command
- [ ] Skill activatable by agent via `skill` tool
- [ ] CHANGELOG.md updated (if user-facing)
