# Claude Code Setup — 1ai-Skills

Claude Code supports skill loading via `.claude/commands/` or plugin directory.

## Install Skills

### Option 1: Plugin Directory (Recommended)
```bash
# Clone the skills repo
git clone https://github.com/oyi77/1ai-skills.git ~/.claude/plugins/1ai-skills

# Or as a submodule in your project
cd /path/to/your/project
git submodule add https://github.com/oyi77/1ai-skills.git .claude/plugins/1ai-skills
```

### Option 2: Symlink to Commands
```bash
git clone https://github.com/oyi77/1ai-skills.git
mkdir -p ~/.claude/commands
ln -s $(pwd)/1ai-skills/development/* ~/.claude/commands/
ln -s $(pwd)/1ai-skills/marketing/* ~/.claude/commands/
# ... repeat for other categories as needed
```

## Creating Slash Commands

For each skill you want as a slash command, create a file in `.claude/commands/`:

### Example: `/systematic-debugging`
Create `.claude/commands/systematic-debugging.md`:

```markdown
Read and follow the skill at:
`~/.claude/plugins/1ai-skills/development/systematic-debugging/SKILL.md`

Apply the systematic debugging process to: $ARGUMENTS
```

### Example: `/seo-audit`
Create `.claude/commands/seo-audit.md`:

```markdown
Read and follow the skill at:
`~/.claude/plugins/1ai-skills/marketing/seo-optimizer/SKILL.md`

Perform a full SEO audit for: $ARGUMENTS
```

## CLAUDE.md Integration

Add to your project's `CLAUDE.md`:

```markdown
# Project Skills

This project uses 1ai-skills. Available skill categories:

## Development
- `/systematic-debugging` — Evidence-driven root cause analysis
- `/test-driven-development` — Red-green-refactor loop
- `/code-reviewer` — Production-quality review

## Marketing
- `/seo-audit` — Full SEO audit with GEO optimization
- `/viral-marketing` — Gary Vaynerchuk content strategy
- `/growth-engine` — Automated A/B testing

## Meta (Self-Evolving)
- `/find-skills` — Discover community skills
- `/create-skills` — Generate new skills
- `/auto-evolve` — Orchestrate evolution loop

When user triggers a skill phrase, load the corresponding SKILL.md from
`~/.claude/plugins/1ai-skills/` and follow it exactly.
```

## Using Slash Commands

```bash
# Debug a failing test
/systematic-debugging auth.test.ts is failing with timeout

# Run SEO audit
/seo-audit https://example.com

# Create a new skill
/create-skills I need a skill for social media sentiment analysis
```

## Batch Command Creation Script

Create all commands at once:

```bash
#!/bin/bash
SKILLS_DIR=~/.claude/plugins/1ai-skills
COMMANDS_DIR=~/.claude/commands
mkdir -p "$COMMANDS_DIR"

# Development commands
for skill in systematic-debugging test-driven-development code-reviewer; do
  cat > "$COMMANDS_DIR/$skill.md" <<EOF
Read and follow: $SKILLS_DIR/development/$skill/SKILL.md
Apply to: \$ARGUMENTS
EOF
done

# Marketing commands
for skill in seo-optimizer viral-marketing growth-engine; do
  cat > "$COMMANDS_DIR/$skill.md" <<EOF
Read and follow: $SKILLS_DIR/marketing/$skill/SKILL.md
Apply to: \$ARGUMENTS
EOF
done

echo "Commands created in $COMMANDS_DIR"
```

## Verification

Test that commands work:

```bash
# In Claude Code
/systematic-debugging "help me debug this error: TypeError: Cannot read property 'x' of undefined"

# Should load the SKILL.md and follow the 4-phase process
```

## Plugin Marketplace (If Available)

If Claude Code supports plugin marketplace:

```bash
# Check if marketplace is available
/plugin marketplace add oyi77/1ai-skills

# Install
/plugin install 1ai-skills@oyi77
```

## Troubleshooting

**Commands not appearing?**
- Check `.claude/commands/` files exist with `.md` extension
- Restart Claude Code session
- Verify file permissions are readable

**Skill content not loading?**
- Check paths in command files point to actual SKILL.md locations
- Test: `cat ~/.claude/plugins/1ai-skills/development/systematic-debugging/SKILL.md`

**Permission errors?**
- Ensure Claude Code has read access to the skills directory
- Run: `chmod -R a+r ~/.claude/plugins/1ai-skills/`
