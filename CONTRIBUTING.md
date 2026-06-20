# Contributing to 1ai-Skills

Thank you for contributing! This guide covers how to create, modify, and review skills.

## Before You Submit (CI will fail if you skip these)

```bash
# 1. Validate every SKILL.md (frontmatter, fields, name-vs-dir match)
python3 scripts/validate-skills.py

# 2. Refresh the skill count catalog
bash scripts/audit-skills.sh --write

# 3. If you added/removed a category, update README.md, AGENTS.md, and llms.txt to mention the new total.
```

If validation finds issues, run `python3 scripts/validate-skills.py --fix` for auto-repair (missing closing `---`, missing name, missing description from H1).

## Quality Linting (Recommended)

For deeper quality checks (duplicate names, description quality, cross-reference validation):
```bash
python3 scripts/lint-skills.py

To regenerate the enriched SKILLS.json with per-skill metadata (name, description, tags, persona):
```bash
python3 scripts/lint-skills.py --write
```


## Skill Anatomy (Required)

Every skill MUST follow this structure:

```yaml
---
name: skill-name-with-hyphens
description: What it does. Use when [trigger1], [trigger2], [trigger3].
persona:  # Optional but recommended
  name: "Expert Name"
  title: "Title - Expertise Area"
  expertise: ["Area1", "Area2"]
  philosophy: "Core quote or principle"
  credentials: ["Credential 1", "Credential 2"]
  principles: ["Principle 1", "Principle 2"]
---

# Skill Title

## Overview
2-3 sentences: what this skill does and why it matters.

## When to Use
- Trigger condition 1
- Trigger condition 2
- When NOT to use (exclusions)

## Process / Steps
1. Step one (specific action, not vague advice)
2. Step two
3. Step three

## Common Rationalizations
| Rationalization | Reality |
|---|---|
| "I'll do this later" | Why this excuse is wrong |

## Red Flags
- Sign the skill is being violated
- Behavioral pattern to watch for

## Verification
After completing the skill's process, confirm:
- [ ] Checklist item with evidence requirement
- [ ] Another checklist item (must be verifiable)
```

## Section Rules

### Frontmatter (Required)
- `name`: Lowercase, hyphen-separated, matches directory name
- `description`: Start with what it does (third person), then trigger conditions ("Use when...")
- Max 1024 characters

### Overview (Required)
- 2-3 sentences maximum
- Answer: What does this skill do? Why should an agent follow it?

### When to Use (Required)
- Bullet list of trigger conditions (symptoms, task types, user phrases)
- Include "When NOT to Use" section with exclusions

### Process (Required)
- Numbered steps, not paragraphs
- Specific actions: "Run `npm test`" NOT "verify tests work"
- Include code examples where helpful
- Use ASCII flowcharts for decision points

### Common Rationalizations (Recommended)
- Table with excuses agents use to skip steps
- Reality column with factual counter-arguments
- Example: "I'll add tests later" → "Untested code breaks. Test first."

### Red Flags (Recommended)
- Observable signs the skill is being violated
- Things to watch for during execution

### Verification (Required)
- Checklist with evidence requirements
- Each item must be verifiable (test output, build result, screenshot)
- "Seems right" is never sufficient

## Naming Conventions

| Item | Convention | Example |
|------|------------|---------|
| Category directory | lowercase, no spaces | `marketing/`, `trading/` |
| Skill directory | lowercase-hyphen-separated | `seo-optimizer/`, `black-edge/` |
| SKILL.md | Always uppercase | `SKILL.md` |
| Supporting files | lowercase-hyphen-separated.md | `examples.md`, `frameworks.md` |
| Persona names | Title Case | `Grace Hopper`, `Richard Feynman` |

## Directory Structure

```
1ai-skills/
├── category/              # e.g., marketing/, trading/, development/
│   └── skill-name/       # e.g., seo-optimizer/
│       ├── SKILL.md       # Required: skill definition
│       ├── _meta.json     # Optional: metadata for app stores
│       └── support.md    # Optional: reference material
├── references/            # Shared checklists (SEO, trading, etc.)
├── docs/                 # Setup guides per platform
└── hooks/                # Session lifecycle hooks
```

## Pull Request Process

1. **Fork** the repository
2. **Create** your skill: `category/skill-name/SKILL.md`
3. **Follow** the anatomy above exactly
4. **Test** your skill with an AI agent (Claude, OpenCode, Cursor)
5. **Verify** all checklist items in your skill work
6. **Submit** PR with:
   - Clear title: `Add skill: skill-name`
   - Description: what it does, when to use, persona (if any)
   - Screenshot or output example if applicable

## What Makes a Good Skill?

✅ **Specific** — Actionable steps, not vague advice
✅ **Verifiable** — Clear exit criteria with evidence requirements
✅ **Battle-tested** — Based on real workflows, tested with agents
✅ **Minimal** — Only what's needed to guide the agent
✅ **Progressive** — Main SKILL.md is entry point, supporting files load on demand

❌ **No generic advice** — "Write good code" is useless
❌ **No duplication** — Reference other skills, don't copy them
❌ **No vague steps** — "Make it work" doesn't tell the agent anything
❌ **No missing verification** — Every skill needs exit criteria

## Shared References

If your skill needs reference material > 50 lines, put it in `references/`:

- `references/seo-checklist.md` — SEO audits
- `references/marketing-checklist.md` — Marketing campaigns
- `references/code-review-checklist.md` — Code reviews
- `references/trading-checklist.md` — Trading strategies

In your skill, reference like:
```markdown
Load `references/seo-checklist.md` for the full SEO audit checklist.
```

## Cross-Skill References

Reference other skills by name:
```markdown
If the build breaks, use the `systematic-debugging` skill.
For test writing, follow the `test-driven-development` skill.
```

Don't duplicate content between skills — reference and link instead.

## Meta-Skills (v3.0)

The `meta/` category contains 12 self-evolving skills:
- `find-skills` — Discovers community skills when local ones don't cover a need
- `create-skills` — Generates new skills when none exist
- `auto-evolve` — Orchestrates the full evolution loop

When creating skills that interact with the self-evolving system, see `meta/meta-orchestrator/SKILL.md`.

## License

By contributing, you agree your contribution will be licensed under the MIT License.
