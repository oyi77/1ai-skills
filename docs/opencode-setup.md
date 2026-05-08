# OpenCode Setup — 1ai-Skills

OpenCode uses agent-driven skill execution via the `skill` tool and `AGENTS.md`.

## Install Skills

### Option 1: Clone and Load
```bash
git clone https://github.com/oyi77/1ai-skills.git ~/.claude/skills/1ai-skills
```

### Option 2: Submodule (Recommended for OpenCode Projects)
```bash
cd /path/to/your/project
git submodule add https://github.com/oyi77/1ai-skills.git .claude/skills/1ai-skills
git submodule update --init --recursive
```

## AGENTS.md Configuration

Create or update `/path/to/project/.claude/AGENTS.md`:

```markdown
# AGENTS.md

## Available Skills

Load skills from ~/.claude/skills/1ai-skills/ as needed.

### Core Skills
- `core/session-brain` — Query bk-hub for project context on session start
- `core/self-improvement` — Continuous self-improvement loop
- `core/teamwork` — Multi-agent coordination

### Development Skills
- `development/systematic-debugging` — Evidence-driven root cause analysis
- `development/test-driven-development` — Red-green-refactor loop
- `development/code-reviewer` — Production-quality code review

### Marketing Skills
- `marketing/seo-optimizer` — Full-stack SEO with GEO optimization
- `marketing/viral-marketing` — Gary Vaynerchuk's content machine
- `marketing/growth-engine` — Automated A/B testing

### Meta Skills (Self-Evolving)
- `meta/find-skills` — Discover community skills
- `meta/create-skills` — Generate new skills autonomously
- `meta/auto-evolve` — Orchestrate evolution loop

## Skill Activation

Skills activate via:
1. **Direct mention**: "Use the `systematic-debugging` skill"
2. **Trigger phrases**: "debug this", "why is this broken"
3. **Tool call**: `skill(name="systematic-debugging")`
```

## Using Skills in OpenCode

### Method 1: Natural Language
```
User: Debug this error using systematic debugging principles.
```

### Method 2: Skill Tool
```javascript
skill(name="systematic-debugging")
```

### Method 3: Category + Skills
```javascript
task(
  category="ultrabrain",
  load_skills=["systematic-debugging"],
  prompt="Debug the failing test in auth.ts"
)
```

## Session Brain (Recommended)

Enable `core/session-brain` for persistent context:

```bash
# In your session startup
skill(name="session-brain")
```

This loads project context from bk-hub at session start.

## Self-Evolving System

The `meta/` skills form a self-improving loop:

```bash
# 1. Find missing skills
skill(name="find-skills")  # Discovers community skills

# 2. Create new skills
skill(name="create-skills")  # Generates skills that don't exist

# 3. Auto-evolve
skill(name="auto-evolve")    # Orchestrates: find → create → improve
```

## Verification

After setup, verify skills are loadable:

```javascript
// Test in OpenCode
skill(name="systematic-debugging")
// Should return the full SKILL.md content
```

## Troubleshooting

**Skills not found?**
- Check path: `ls ~/.claude/skills/1ai-skills/`
- Verify AGENTS.md references correct path

**Skill not activating?**
- Ensure trigger phrases match SKILL.md description
- Try explicit `skill(name="...")` call

**Meta-skills not working?**
- Verify bk-hub is running: `curl http://localhost:9099/brain/status`
- Check meta-skill dependencies in their SKILL.md
