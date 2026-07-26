# 1ai-Skill Standard v1.0.0

Canonical specification for authoring, validating, and maintaining 1ai-skills.
Every SKILL.md file and SKILLS.json entry in this repository conforms to this
standard.

---

## 1. File Structure

A skill is a directory named `<skill-name>` within a category directory,
containing exactly one `SKILL.md` file. The directory name is the skill's
canonical identifier (kebab-case).

```
category-name/
  skill-name/
    SKILL.md         # Required: the skill definition
    assets/          # Optional: images, diagrams, templates
    examples/        # Optional: runnable code examples
```

The category directory matches the primary category from the
[20-category taxonomy](#6-category-taxonomy).

---

## 2. SKILL.md Frontmatter

Every SKILL.md MUST begin with YAML frontmatter between `---` delimiters.
Frontmatter is the machine-readable metadata block that powers discovery,
validation, and routing.

### 2.1 Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string (kebab-case) | Canonical identifier. MUST match directory name. Pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$` |
| `category` | string (enum) | Primary category from the taxonomy. Maps to the parent directory. |
| `description` | string (30-500 chars) | One-paragraph summary. MUST include a "Use when" trigger phrase explaining when the agent activates this skill. |
| `tags` | array of strings | Discovery tags. First tag SHOULD be the primary domain. Min 1, no duplicates. |

### 2.2 Optional Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `schema_version` | semver | `1.0.0` | Version of this standard the frontmatter conforms to. |
| `version` | semver | `0.1.0` | Skill revision per semver. See [SKILL_VERSIONING.md](SKILL_VERSIONING.md). |
| `status` | enum | `active` | `draft`, `active`, `deprecated`, or `removed`. |
| `domain` | string | (same as category) | Legacy alias for `category`. Prefer `category` in new skills. Existing skills may use either. |
| `subcategory` | string | — | Optional refinement within category (e.g. `blockchain-security` within `cybersecurity`). |
| `triggers` | array | — | Explicit input patterns that should activate this skill. |
| `non_triggers` | array | — | Situations where this skill MUST NOT activate. |
| `inputs` | array of objects | — | Structured inputs the skill expects. Each has `name`, optional `type`, `description`, `required`. |
| `outputs` | array of objects | — | Structured outputs the skill produces. Each has `name`, optional `type`, `description`. |
| `dependencies` | array of skill names | — | Other skills this skill depends on (kebab-case names). |
| `tool_requirements` | array of objects | — | Tools the agent must have. Each has `tool`, optional `purpose`, `required` (bool). |
| `permissions` | array of objects | — | Explicit permission declarations. Each has `resource`, `action`, optional `justification`. |
| `risk_level` | enum | `info` | `info`, `low`, `medium`, `high`, or `critical`. |
| `human_approval` | boolean | `false` | Requires explicit human approval before execution. **MUST** be `true` if `risk_level` is `high` or `critical`. |
| `supported_agents` | array | — | Agent platforms tested on (e.g. `claude-code`, `opencode`, `cursor`). |
| `author` | string | `""` | Original maintainer (GitHub handle). |
| `license` | string | `MIT` | SPDX license identifier. |
| `last_reviewed` | string (date) | — | ISO 8601 date of last accuracy/safety review. |
| `owners` | array | — | Current responsible maintainers. |
| `evaluation_profile` | object | — | Populated by the evaluation system. Contains `quality_score` (0-100), `test_count`, `last_evaluated`. |

### 2.3 Frontmatter Example

```yaml
---
name: onchain-transaction-forensics
schema_version: "1.0.0"
version: "3.2.0"
status: active
category: cybersecurity
subcategory: blockchain-security
description: >
  Trace and analyze blockchain transactions to investigate illicit fund flows,
  identify wallet clusters, and map transaction graphs across multiple
  blockchains. Use when investigating stolen funds, following money trails
  on-chain, analyzing suspicious addresses, or tracing cross-chain transactions.
tags:
  - blockchain
  - forensics
  - onchain
  - tracing
  - money
risk_level: medium
human_approval: false
dependencies:
  - wallet-address-intelligence
tool_requirements:
  - tool: etherscan-api
    purpose: Query transaction data
    required: true
  - tool: web3-provider
    purpose: Interact with chain RPCs
    required: true
author: oyi77
license: MIT
last_reviewed: "2026-07-20"
---
```

### 2.4 Legacy Compatibility

Existing skills (`domain` field instead of `category`) are valid.
The validator accepts `domain` as an alias for `category`. New skills SHOULD
use `category`.

---

## 3. SKILL.md Body Structure

The body follows the YAML frontmatter and contains the human-readable skill
definition. Sections are indicated by Markdown headings (`##`, `###`).

### 3.1 Required Sections

| Section | Requirement |
|---------|-------------|
| `## When to Use` | MUST be present. First section after frontmatter. Describes activation conditions. |
| `## Workflow` or `## Process` or `## Steps` | MUST be present. Step-by-step execution guide. |

### 3.2 Strongly Recommended Sections

| Section | Guidance |
|---------|----------|
| `## Overview` | Brief introduction, prerequisites, scope. |
| `## When NOT to Use` | Anti-patterns, scope boundaries, contraindications. |
| `## Anti-Rationalization Table` | 2-column table (`Rationalization` vs `Reality`) that pre-emptively answers shortcuts. |
| `## Verification` | How to confirm the skill executed correctly. Checkpoints, expected outputs. |

### 3.3 Quality Indicators

A high-quality SKILL.md includes most of:

- **Measured code blocks** (guarded by language, runnable)
- **Real examples** with realistic (not placeholder) values
- **Decision trees** for branching execution paths
- **Dead-end warnings** for when the skill cannot complete
- **Monetization/ROI** context when applicable
- **Cross-references** to related skills

---

## 4. SKILLS.json Registry

Every registered skill has an entry in `SKILLS.json` at the repository root.
The registry mirrors the on-disk skill directories and is the primary
discovery index for agents.

### 4.1 Required Registry Fields

| Field | Source |
|-------|--------|
| `name` | From frontmatter |
| `category` | From frontmatter (or `domain`) |
| `description` | From frontmatter |
| `domain` | From frontmatter (or `category`) |
| `tags` | From frontmatter |

### 4.2 Optional Registry Fields

| Field | Source |
|-------|--------|
| `version` | From frontmatter |
| `author` | From frontmatter |
| `risk_level` | From frontmatter |
| `subdomain` | From frontmatter |

### 4.3 Registry Synchronization

The registry is kept in sync with on-disk skills via `scripts/lint-skills.py --write`.
A skill is "orphaned" if it has an entry in SKILLS.json but no corresponding
SKILL.md file — this is allowed only for `status: removed` entries (backward
compatibility references). All other entries MUST have a matching directory.

---

## 5. Schema Validation

The canonical schema lives at `schemas/skill.schema.json` (JSON Schema Draft-07).

Validation points:
- **Pre-commit**: `scripts/validate-skill-schema.py` checks all frontmatter
- **CI**: Schema validation in CI pipeline
- **Lint**: `scripts/lint-skills.py` checks structural quality
- **Test**: `scripts/test-skills.py` checks functional correctness

---

## 6. Category Taxonomy

The 20-category taxonomy governs directory layout and discovery:

| Category | Scope |
|----------|-------|
| `agents` | AI agent orchestration, multi-agent patterns |
| `automation` | Bots, workflows, scrapers, process automation |
| `content` | Video, audio, design, writing, documentation |
| `core` | AI infrastructure, memory, self-improvement, model routing |
| `cybersecurity` | Threat hunting, forensics, pentesting, SOC, incident response |
| `data` | Data pipelines, analysis, visualization, ETL |
| `development` | TDD, debugging, code review, PRD, engineering workflows |
| `devops` | Docker, Kubernetes, CI/CD, cloud ops, GitOps |
| `finance` | Finance analysis, valuation, tax, portfolio management |
| `financial` | (Alias for `finance` — see below) |
| `integrations` | GitHub, Discord, Notion, Slack, Stripe, Firebase, Supabase |
| `marketing` | SEO, viral content, email, ads, growth |
| `mcp` | Model Context Protocol servers and tool integrations |
| `meta` | Self-evolving meta-skills, performance monitoring |
| `mindset` | Negotiation, leadership, critical thinking |
| `operations` | Business ops, governance, HR, legal, project management |
| `productivity` | Calendars, email, meetings, workspace management |
| `research` | Deep research, market analysis, competitive intelligence |
| `sales` | Lead gen, CRM, outreach, sales automation |
| `trading` | Crypto, DeFi, Polymarket, trading strategies |

**Note**: `finance` and `financial` coexist historically. `finance` is the
preferred canonical name. `financial` exists for backward compatibility.
Both map to the same taxonomy category.

---

## 7. Naming Conventions

- Directory names (skill identifiers): **kebab-case** — lowercase letters,
  digits, hyphens only. No underscores. Pattern: `^[a-z][a-z0-9]*(-[a-z0-9]+)*$`
- Category directory names: **lowercase**, plural, no hyphens
- File names: `SKILL.md` (case-sensitive)
- Description: starts with action verb, includes "Use when" trigger phrase
- Tags: lowercase, hyphen-separated where multi-word

---

## 8. Versioning Compatibility

| Schema Version | Breaking Changes |
|----------------|------------------|
| 1.0.0 | Initial standard. Accepts `domain` and `category` interchangeably. |

See [SKILL_VERSIONING.md](SKILL_VERSIONING.md) for the full versioning model.

---

## 9. Compliance

Skills MUST pass all of:

1. **Frontmatter validation**: `scripts/validate-skill-schema.py` (schema conformance)
2. **Structural quality**: `scripts/lint-skills.py` (required sections, description quality)
3. **Functional tests**: `scripts/test-skills.py` (code syntax, cross-references)
4. **Registry sync**: SKILLS.json matches on-disk skills

A skill that fails any of these is considered non-compliant and SHOULD be
fixed before the next release.
