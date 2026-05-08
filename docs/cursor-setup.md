# Cursor Setup — 1ai-Skills

Cursor supports skills via `.cursor/rules/` for automatic context injection.

## Install Skills

```bash
# Clone the skills repo
git clone https://github.com/oyi77/1ai-skills.git .cursor/skills

# Or symlink if already cloned elsewhere
ln -s /path/to/1ai-skills .cursor/skills
```

## Adding Skills to Rules

### Method 1: Individual Skill Files

Copy specific SKILL.md files to `.cursor/rules/`:

```bash
# Copy development skills
cp 1ai-skills/development/systematic-debugging/SKILL.md .cursor/rules/systematic-debugging.mdc
cp 1ai-skills/development/test-driven-development/SKILL.md .cursor/rules/test-driven-development.mdc
cp 1ai-skills/development/code-reviewer/SKILL.md .cursor/rules/code-reviewer.mdc

# Copy marketing skills
cp 1ai-skills/marketing/seo-optimizer/SKILL.md .cursor/rules/seo-optimizer.mdc
```

### Method 2: Reference Entire Directory

Create `.cursorrules` (or `.cursor/rules/global.mdc`):

```markdown
# Project Rules

## Available Skills

Load skills from `.cursor/skills/` as needed.

### Development Workflow
@.cursor/skills/development/systematic-debugging/SKILL.md
@.cursor/skills/development/test-driven-development/SKILL.md
@.cursor/skills/development/code-reviewer/SKILL.md

### Marketing Workflow
@.cursor/skills/marketing/seo-optimizer/SKILL.md
@.cursor/skills/marketing/viral-marketing/SKILL.md
@.cursor/skills/marketing/growth-engine/SKILL.md

### Meta Skills (Self-Evolving)
@.cursor/skills/meta/find-skills/SKILL.md
@.cursor/skills/meta/create-skills/SKILL.md
@.cursor/skills/meta/auto-evolve/SKILL.md

## Activation Rules

When user mentions:
- "debug", "fix this", "why is it broken" → Load systematic-debugging
- "test", "TDD", "write tests" → Load test-driven-development
- "review my code", "code review" → Load code-reviewer
- "SEO", "audit", "optimize" → Load seo-optimizer
- "create a skill", "new skill" → Load create-skills
```

## Cursor Rules Format (.mdc)

Cursor uses `.mdc` files with frontmatter:

```markdown
---
alwaysApply: false
description: "Systematic debugging workflow"
trigger: ["debug", "fix", "why is this broken"]
---

# Systematic Debugging

@.cursor/skills/development/systematic-debugging/SKILL.md
```

## Automatic Context Injection

With `.cursor/rules/`, skills auto-load when:
1. File matches glob pattern in rule
2. Trigger keywords detected in conversation
3. `alwaysApply: true` is set

### Example: Auto-Apply for Test Files
Create `.cursor/rules/tdd-for-tests.mdc`:

```markdown
---
alwaysApply: false
glob: "**/*.test.ts"
description: "TDD for test files"
---

@.cursor/skills/development/test-driven-development/SKILL.md
```

## Using Skills in Cursor

### Method 1: Natural Language
```
User: Debug this error using systematic debugging principles.
```

### Method 2: @ References
```
User: @systematic-debugging help me fix this TypeError
```

### Method 3: Composer
Open Composer (Cmd+K) and reference skills:
```
@systematic-debugging @code-reviewer review my auth.ts changes
```

## Verification

Test that skills are loading:

1. Open a file in Cursor
2. Type: `// debug this function`
3. Cursor should suggest loading systematic-debugging skill
4. Check `.cursor/rules/` files are being read

## Batch Rule Creation Script

```bash
#!/bin/bash
SKILLS_DIR=.cursor/skills
RULES_DIR=.cursor/rules
mkdir -p "$RULES_DIR"

# Create rules for development skills
cat > "$RULES_DIR/debugging.mdc" <<EOF
---
alwaysApply: false
description: "Systematic debugging"
trigger: ["debug", "fix", "error"]
---
@$SKILLS_DIR/development/systematic-debugging/SKILL.md
EOF

cat > "$RULES_DIR/tdd.mdc" <<EOF
---
alwaysApply: false
description: "Test-driven development"
trigger: ["test", "TDD", "write tests"]
---
@$SKILLS_DIR/development/test-driven-development/SKILL.md
EOF

echo "Rules created in $RULES_DIR"
```

## Troubleshooting

**Skills not auto-loading?**
- Check `.cursor/rules/` files have `.mdc` extension
- Verify `trigger` keywords match your conversation
- Set `alwaysApply: true` for testing

**@ references not working?**
- Ensure path in rule file is correct
- Use absolute paths or paths relative to project root
- Check Cursor version supports `@` references

**Rules not appearing?**
- Restart Cursor after creating rule files
- Check `.cursorrules` or `.cursor/rules/global.mdc` syntax
- Open Cursor Settings → Rules to verify rules are loaded
