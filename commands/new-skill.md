# /new-skill — Create a new skill from template

Scaffold a new skill with proper structure and frontmatter.

## Steps

1. Ask for:
   - Skill name (kebab-case)
   - Category (agents, automation, content, core, cybersecurity, data, development, devops, financial, integrations, marketing, mcp, meta, mindset, operations, productivity, research, sales, trading)
   - Description (1-2 sentences, action-oriented)
   - Tags (3-5 relevant tags)
2. Create `<category>/<skill-name>/SKILL.md` with:
   - YAML frontmatter (name, description, domain, tags)
   - `## When to Use` section with 3+ trigger conditions
   - `## When NOT to Use` section with 2+ contraindications
   - `## Overview` section (placeholder for author)
   - `## Workflow` section (placeholder for author)
   - `## Verification` section (placeholder checklist)
3. Run `bash scripts/audit-skills.sh --write` to update SKILLS.json
4. Run `python3 scripts/validate-skills.py` to verify

## Template

```markdown
---
name: <skill-name>
description: <action-oriented description>
domain: <category>
tags:
- <tag1>
- <tag2>
- <tag3>
---

# <Skill Title>

## When to Use
- <trigger 1>
- <trigger 2>
- <trigger 3>

## When NOT to Use
- <contraindication 1>
- <contraindication 2>

## Overview
<2-3 sentence overview>

## Workflow
1. **Step 1** — <description>
2. **Step 2** — <description>
3. **Step 3** — <description>

## Verification
- [ ] <check 1>
- [ ] <check 2>
- [ ] <check 3>
```
