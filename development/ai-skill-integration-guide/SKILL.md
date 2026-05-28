---
name: ai-skill-integration-guide
description: Meta-skill for integrating external GitHub skill repos into 1ai-skills. Covers discovery, deduplication, format conversion, category mapping, validation, and quality gates. Use when integrating external skill repos, bulk skill imports, skill format conversion.
domain: development
tags: [meta, integration, skills, github, bulk-import, format-conversion, quality-gates]
---

## Overview

Meta-skill that teaches agents how to integrate external skill repositories into the 1ai-skills library. Covers the full pipeline from discovery through validation, ensuring new skills are unique, properly formatted, correctly categorized, and quality-gated before merge.

## Discovery

Before importing anything, understand what the external repo offers.

1. Read the repo README for purpose, scope, and skill count
2. Check if the repo uses SKILL.md files, AGENTS.md, or another structure
3. List all skill files and extract their frontmatter (name, description, domain, tags)
4. Identify the unique value — what does this repo offer that 1ai-skills does not already cover?

```bash
# List all potential skill files in the external repo
find /path/to/external-repo -name "SKILL.md" -o -name "*.md" | head -50

# Extract frontmatter from each
for f in $(find /path/to/external-repo -name "SKILL.md"); do
  echo "=== $f ==="
  sed -n '/^---$/,/^---$/p' "$f"
done
```

## Deduplication

Always check for overlap before importing. Redundant skills degrade the library.

1. Grep existing SKILLS.json for similar skill names:

```bash
grep -i "keyword" /home/openclaw/projects/1ai-skills/SKILLS.json
```

2. Grep existing skills for similar descriptions:

```bash
grep -ri "description.*keyword" /home/openclaw/projects/1ai-skills/*/SKILL.md
```

3. Check the target category's current count and capacity
4. For each candidate skill, document: overlaps found, unique value, import decision (import / skip / merge)

## Format Conversion

All 1ai-skills must follow the standard YAML frontmatter format.

**Required frontmatter fields**:
```yaml
---
name: skill-name          # kebab-case, unique across repo
description: What it does. Use when [trigger1], [trigger2].  # max ~200 chars
domain: category-name     # must match an existing category directory
tags: [tag1, tag2, tag3]  # 3-8 relevant tags
---
```

**Conversion checklist**:
- [ ] Name is kebab-case and unique (grep for conflicts)
- [ ] Description starts with what, ends with "Use when..." triggers
- [ ] Domain maps to an existing category directory
- [ ] Tags are lowercase, relevant, and not redundant with domain
- [ ] File is at `<category>/<skill-name>/SKILL.md`
- [ ] Body starts with `## Overview` after frontmatter
- [ ] No user-specific paths, tokens, or credentials hardcoded
- [ ] Content is self-contained — does not require external context to understand

## Category Mapping

Map external skills to the existing 18 categories:

| Category | Focus |
|----------|-------|
| `automation/` | Bots, scrapers, pipelines, workflow automation |
| `agents/` | Agent architectures, autonomous systems |
| `content/` | Video, podcast, design, UI generation |
| `core/` | Self-improvement, memory, orchestration, infrastructure |
| `cybersecurity/` | Threat hunting, forensics, pen testing, SOC, compliance |
| `data/` | Data cleaning, visualization, pipelines, reporting |
| `development/` | TDD, debugging, code review, patterns, frameworks |
| `devops/` | Docker, K8s, CI/CD, cloud ops, GitOps |
| `financial/` | Finance analysis, investing, tax, accounting |
| `integrations/` | Platform integrations (GitHub, Discord, Notion, Slack) |
| `marketing/` | SEO, growth, email, social, affiliate |
| `mcp/` | MCP server skills |
| `meta/` | Self-improving meta-skills, skill management |
| `operations/` | Governance, KYC, project management, HR, legal |
| `productivity/` | Calendar, email, meetings, workspace tools |
| `research/` | Analysis, deep research, competitive intelligence |
| `sales/` | Lead gen, closing, B2B, CRM, influence |
| `trading/` | Crypto, DeFi, strategies, smart contracts |

**If no category fits**: Propose a new category in the PR with justification. New categories need at least 3 skills to be viable.

## Validation

Run the full validation pipeline after import.

```bash
# 1. Refresh the skill catalog
bash /home/openclaw/projects/1ai-skills/scripts/audit-skills.sh --write

# 2. Verify counts match
bash /home/openclaw/projects/1ai-skills/scripts/audit-skills.sh

# 3. Update documentation with new counts
# - README.md: skill count in header
# - llms.txt: category table
# - package.json: description field if count mentioned
# - AGENTS.md: category table
```

## Quality Gates

Every imported skill must pass these gates before merge:

**Gate 1 — Self-Contained**: The skill is fully understandable without reading the source repo. No "see the README for details" — all details are in the SKILL.md.

**Gate 2 — Actionable**: The skill provides concrete steps, commands, code examples, or decision frameworks. Not just a description of what something is.

**Gate 3 — Unique Value**: No existing 1ai-skill covers the same ground. If there is overlap, the new skill must be clearly differentiated or merged into the existing one.

**Gate 4 — Correct Format**: YAML frontmatter is valid, required fields present, naming conventions followed, category mapping is correct.

**Gate 5 — No Leaks**: No hardcoded paths, API keys, user-specific config, or internal URLs. Safe for any user to install.

## Process Summary

```
1. Discovery    → Read repo, list skills, extract metadata
2. Dedup        → Grep existing skills, document overlaps
3. Convert      → Apply format, fix frontmatter, restructure body
4. Categorize   → Map to existing categories or propose new
5. Validate     → Run audit script, update docs
6. Quality Gate → Check 5 gates, fix failures
7. Submit       → PR with import summary and count changes
```

## When to Use

- Integrating skills from an external GitHub repository
- Bulk importing skills from a curated collection
- Converting non-standard skill formats to 1ai-skills format
- Auditing an external repo for importable content
- Validating skill quality before merge
