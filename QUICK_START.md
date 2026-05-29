# Quick Start Guide

Get from zero to productive with 1ai-Skills in under 10 minutes.

---

## 1. Installation (2 min)

### Install via npx

```bash
npx skills add oyi77/1ai-skills
```

This copies all 1284 skills into your project's skill directory.

### Install Hooks (auto-evolve system)

```bash
# From the consuming repo (where skills were added)
node node_modules/1ai-skills/scripts/install-hooks.js --yes
```

During install the hook installer:

1. Copies hook scripts to `~/.claude/hooks/` (or equivalent agent config dir)
2. Wires hooks into `~/.claude/settings.json`
3. Auto-detects installed AI agents (Claude Code, OpenClaw, Cursor, Windsurf, etc.)
4. Creates evolve config at `~/.1ai-skills/evolve-config.json`

Alternatives: `git clone https://github.com/oyi77/1ai-skills.git` or `git submodule add https://github.com/oyi77/1ai-skills.git skills`.

### Verify Installation

```bash
# Check hooks are installed and active
node scripts/hooks-cli.js status

# Confirm skill count
bash scripts/audit-skills.sh

# Quick sanity: list categories
ls -d */
```

Expected output: 18 category directories (agents/, automation/, content/, ...) and hook status showing active.

---

## 2. Finding Skills (1 min)

### Browse by Category

```bash
# List all categories
ls -d */

# List skills in a category
ls marketing/
ls cybersecurity/
ls trading/
```

18 categories total. Largest: cybersecurity (783), development (83), content (62), core (48), marketing (47). See `README.md` for the full table.

### Search with grep

```bash
# Search skill names and descriptions across all SKILL.md files
grep -rl "description:.*SEO" --include="SKILL.md" .

# Find skills by trigger keyword
grep -rl "Use when.*debugging" --include="SKILL.md" .

# Search the machine-readable catalog
cat SKILLS.json
```

### Machine-Readable Catalog

`SKILLS.json` at the repo root lists every category and its count. Tools and scripts parse this for discovery. Regenerate it after adding or removing skills:

```bash
bash scripts/audit-skills.sh --write
```

---

## 3. Using Skills (2 min)

### How Agents Load Skills

Skills are self-contained markdown files loaded on demand. Agents discover skills through:

1. **SKILLS.json** -- machine-readable catalog (totals and category names)
2. **Category AGENTS.md** -- sub-index per category (e.g., `cybersecurity/AGENTS.md`)
3. **Individual SKILL.md** -- the actual skill content

Do NOT walk all 1284 skill directories. Use the catalog or grep to find what you need.

### Skill Anatomy (Quick Reference)

Every skill lives in `category/skill-name/SKILL.md` and follows this structure:

```yaml
---
name: skill-name-with-hyphens
description: What it does. Use when [trigger1], [trigger2], [trigger3].
persona:
  name: "Expert Name"
  title: "Title - Expertise Area"
  expertise: ["Area1", "Area2"]
---
```

Required sections inside the SKILL.md body:

| Section | Purpose |
|---------|---------|
| **Overview** | 2-3 sentences: what this skill does and why |
| **When to Use** | Trigger conditions + exclusions ("When NOT to Use") |
| **Process / Steps** | Numbered, specific actions with code examples |
| **Verification** | Checklist with evidence requirements |

Recommended sections: **Common Rationalizations** (excuse/reality table), **Red Flags** (signs of violations).

### Auto-Evolve System

Skills track their own usage and evolve automatically. See Section 5 for details.

To opt out per-skill, add to frontmatter:

```yaml
auto_evolve: false
```

To disable globally:

```bash
# Edit the evolve config
cat ~/.1ai-skills/evolve-config.json
# Set "enabled": false
```

---

## 4. Creating Skills (3 min)

### Minimal Viable Skill

Create the directory and file:

```bash
mkdir -p marketing/my-new-skill
```

Then create `marketing/my-new-skill/SKILL.md`:

```yaml
---
name: my-new-skill
description: Short description. Use when [trigger1], [trigger2].
---

# My New Skill

## Overview
2-3 sentences: what it does and why an agent should follow it.

## When to Use
- Trigger condition 1
- Trigger condition 2

### When NOT to Use
- For unrelated task Y

## Process / Steps
1. Run `specific-command --flag`
2. Analyze the output for X
3. Verify with evidence (see below)

## Verification
- [ ] Command X ran successfully (paste output)
- [ ] Output meets criteria Y
```

See `CONTRIBUTING.md` for the full template with all recommended sections (persona, Common Rationalizations, Red Flags).

### Required vs Recommended

**Required frontmatter:** `name` (lowercase-hyphen, matches dir), `description` (what + triggers).
**Required sections:** Overview, When to Use, Process/Steps, Verification.
**Recommended:** `persona` in frontmatter, Common Rationalizations, Red Flags sections. See `CONTRIBUTING.md` for the full spec.

### Naming Conventions

- Category dirs: `lowercase/` (no spaces)
- Skill dirs: `lowercase-hyphen-separated/` with `SKILL.md` (always uppercase)
- Supporting files: `lowercase-hyphen.md`
- `name` in frontmatter must match the directory name
- Persona names: Title Case (`Grace Hopper`)

### Validation Before PR

```bash
# 1. Validate all SKILL.md files (frontmatter, fields, name-vs-dir match)
python3 scripts/validate-skills.py

# 2. Auto-repair common issues (missing closing ---, missing name, missing H1)
python3 scripts/validate-skills.py --fix

# 3. Refresh the skill count catalog
bash scripts/audit-skills.sh --write

# 4. If you added/removed a category, update README.md, AGENTS.md, and llms.txt
```

Submit a PR with title `Add skill: skill-name` and a description of what it does and when to use it.

---

## 5. Auto-Evolve System (2 min)

### What It Does

The auto-evolve system makes skills self-improving. It tracks usage, collects feedback, identifies patterns, and evolves skills over time.

**System flow:** Execute -> Monitor -> Collect -> Recognize -> Assess -> Find -> Create -> Generate -> Learn -> Evolve -> Repeat

### Hooks That Fire

| Hook | Trigger | What It Does |
|------|---------|--------------|
| `session:start` | Agent session begins | Detects project type, suggests relevant skills, checks hooks health |
| `pre-commit` | Git commit | Validates SKILL.md structure before the commit goes through |
| `post-task` | Agent completes a task | Logs skill performance metrics |
| **Auto-Evolve Hooks** | | |
| `skill-tracker.js` | After Skill tool use | Tracks which skills were invoked and their context |
| `skill-committer.js` | After Write/Edit tool use | Detects skill file changes and stages them |
| `skill-feedback-capture.js` | On user prompt submit | Captures implicit feedback signals |
| `skill-evolver.js` | Session ends | Runs the evolution loop: analyze metrics, generate improvements |

Metrics are stored in the centralized SQLite datastore managed by `meta/data` (usage counts, success/failure signals, feedback, version diffs).

### Configuration

Evolve config lives at `~/.1ai-skills/evolve-config.json`:

```json
{
  "enabled": true,
  "skill_dirs": ["path/to/1ai-skills"],
  "evolve_on_session_end": true,
  "auto_commit_improvements": false
}
```

Key settings: `enabled` (master toggle), `skill_dirs` (auto-detected), `evolve_on_session_end` (run evolver at session end), `auto_commit_improvements` (default: false, requires manual review).

Manage hooks via CLI: `node scripts/hooks-cli.js status|list` and `node scripts/install-hooks.js --yes` to reinstall.

---

## 6. Troubleshooting

### Common Issues

**"Skills not found by agent"**
- Confirm skills are installed: `ls` should show category directories
- Confirm hooks are wired: `node scripts/hooks-cli.js status`
- Check the agent's config for the skill directory path

**"validate-skills.py reports errors"** -- Run `python3 scripts/validate-skills.py --fix`. Common fixes: missing closing `---`, missing `name` field, name-dir mismatch.

**"SKILLS.json count is wrong"** -- Regenerate: `bash scripts/audit-skills.sh --write`. Counts in README.md and AGENTS.md must match.

**"Hooks not firing"** -- Reinstall: `node scripts/install-hooks.js --yes`. Check `~/.claude/settings.json` for hook entries. Verify scripts are executable: `ls -la hooks/`.

**"Auto-evolve not running"** -- Check `cat ~/.1ai-skills/evolve-config.json` for `"enabled": true`. Verify hook status: `node scripts/hooks-cli.js status`.

**"Skill frontmatter parse errors"** -- Every SKILL.md must start with `---`. Required fields: `name` (lowercase-hyphen, matches dir), `description`.

### Validate Skills Locally

```bash
python3 scripts/validate-skills.py         # full validation
python3 scripts/validate-skills.py --fix   # auto-repair
bash scripts/audit-skills.sh --write       # regenerate SKILLS.json
```

### Report Issues

Open an issue at [github.com/oyi77/1ai-skills/issues](https://github.com/oyi77/1ai-skills/issues) with:
- Which skill or category is affected
- The validation output or error message
- Steps to reproduce

---

## Next Steps

- **Browse skills:** Read `SKILLS.json` for the full catalog, then explore categories that interest you
- **Use meta-skills:** Say "find skills" to auto-discover community skills, "create skills" to generate new ones
- **Read the contributing guide:** `CONTRIBUTING.md` has the full skill anatomy spec and PR process
- **Platform setup:** Check `docs/` for agent-specific integration guides (Claude, Cursor, OpenCode)
