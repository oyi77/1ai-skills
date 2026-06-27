## What
<!-- One-sentence summary of the change -->

## Why
<!-- Link to issue: Fixes #123 -->

## How
<!-- Brief technical approach -->

## Checklist
- [ ] `SKILL.md` has valid YAML frontmatter (`name`, `description`, `domain`)
- [ ] Content is real (no template placeholders like "Section content — see SKILL.md body")
- [ ] `## When to Use` section present with 3+ triggers
- [ ] `bash scripts/audit-skills.sh --write` run (SKILLS.json updated)
- [ ] `python3 scripts/validate-skills.py` passes
- [ ] Internal `/skills/<name>` links resolve to existing skills
- [ ] No duplicate description with another skill
- [ ] CHANGELOG.md updated (if user-facing change)

## Type
- [ ] New skill
- [ ] Skill content fix
- [ ] Infrastructure (hooks, scripts, CI)
- [ ] Documentation
