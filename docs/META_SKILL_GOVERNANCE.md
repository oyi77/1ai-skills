# Meta-Skill Governance

## What Meta-Skills Are

Meta-skills are skills that operate on other skills. They manage, create, evaluate,
monitor, and improve the skill library itself. Unlike domain skills (which provide
expertise in a specific area), meta-skills are infrastructure that keeps the skill
ecosystem healthy.

## Current Inventory (2026-07-26)

13 meta-skills in `meta/` category:

| Skill | Role | Risk Level | Depends On |
|-------|------|------------|------------|
| auto-evolve | Autonomous system improvement; orchestrates find+create skills | medium | find-skills, create-skills, self-assessment |
| auto-learner | Autonomous learning from execution patterns | medium | pattern-recognition, performance-monitor |
| create-skills | Generates new skills when gaps are identified | high | meta-skill-datastore |
| data | Raw data storage layer for skill operations | low | — |
| feedback-collector | Collects and routes feedback signals | low | — |
| hooks-setup | Installs and configures session hooks | low | — |
| improvement-generator | Generates actionable improvements from performance data | medium | performance-monitor, self-assessment |
| meta-find-skills | Searches for skills across community repos | low | — |
| meta-skill-datastore | Centralized DB for meta-skill metrics | low | — |
| pattern-recognition | Identifies patterns in skill execution | low | performance-monitor |
| performance-monitor | Tracks skill execution metrics | low | — |
| self-assessment | Self-evaluation of skill quality | low | — |
| skill-evolution-engine | Self-improving skill creation system | high | meta-skill-datastore, create-skills |

## Categorization

Meta-skills fall into four functional groups:

### 1. Creation & Evolution
- `create-skills`, `skill-evolution-engine`, `auto-evolve`
- These skills **create or modify other skills**
- Require `human_approval: true` — no autonomous skill creation without user consent
- Must have `risk_level >= medium`

### 2. Monitoring & Evaluation
- `performance-monitor`, `self-assessment`, `pattern-recognition`, `feedback-collector`
- Read-only skill observation
- Safe to run autonomously
- `risk_level: low` or `info`

### 3. Discovery & Datastore
- `meta-find-skills`, `meta-skill-datastore`, `data`
- Infrastructure services
- No side effects on skill content
- `risk_level: info` or `low`

### 4. Infrastructure
- `hooks-setup`, `auto-learner`
- Session-level configuration and background learning
- `risk_level: low`

## Governance Rules

### Rule 1: Creation Gate
New meta-skills require:
- PR with description of what meta capability it provides
- Existing meta-skill list checked to avoid duplication
- `risk_level` and `permissions` declared in frontmatter
- If it creates/modifies skills → `human_approval: true` AND `risk_level >= medium`

### Rule 2: No Recursive Destruction
A meta-skill MUST NOT delete or disable:
- Itself
- Its own dependencies
- The `meta-skill-datastore` skill

### Rule 3: Lock Files
Skills in the creation/evolution group (`create-skills`, `skill-evolution-engine`, `auto-evolve`)
MUST:
- Write-protect all skill directories they are not explicitly authorized to modify
- Log every skill creation/modification to the datastore
- Include an undo capability (draft mode before final write)

### Rule 4: Version Pinning
Meta-skills that depend on specific script versions in `scripts/` MUST:
- Pin the version in their `dependencies` field
- Reference `DEPENDS_ON.md` or the script's versioned path

### Rule 5: Evaluation Requirement
Every meta-skill MUST have a corresponding eval case in `evals/cases/`.
Eval cases must:
- Exercise at least the primary code path
- Include an expected failure case
- Reference the skill name in the eval's `description` field

## Risk Model

| Risk Level | Allowed Operations | Approval Required | Examples |
|------------|-------------------|-------------------|----------|
| info | Read skill metadata | No | data, meta-find-skills |
| low | Read skill content, observe execution | No | performance-monitor, self-assessment |
| medium | Suggest changes, create drafts | User confirmation | auto-evolve, improvement-generator |
| high | Write/delete skill files | Explicit consent | create-skills, skill-evolution-engine |
| critical | Remove/modify meta-infrastructure | Full review | (none currently) |

## Quality Standards

All meta-skills pass the same validation pipeline as domain skills:
- `validate-skill-schema.py` — fields, types, risk_level declaration
- `lint-skills.py` — formatting, trigger phrases, descriptions
- `check-broken-links.py` — internal `/skills/` and `skill://` references
- `run-evals.py` — eval case execution

Additionally, meta-skills are subject to:
- **Dependency audit**: `depends_on` chains checked for cycles (via `skill-graph.py --topo-sort`)
- **Permission audit**: `permissions` field verified against actual skill operations
- **Annual review**: `last_reviewed` date must be within 12 months

## Lifecycle

```
1. Gap identified → 2. Proposal → 3. Review → 4. Implementation
         ↓                                                 |
   5. Registration (SKILLS.json)                            |
         ↓                                                 |
   6. Eval cases created ←─────────────────────────────────┘
         ↓
   7. Validation passes (schema, lint, links, evals)
         ↓
   8. Released (merged, tagged)
         ↓
   9. Monitoring (performance-monitor tracks usage)
         ↓
  10. Retirement (if usage < threshold for 6 months)
```

## Historical Context

This governance framework was established in Phase 12 of the 1ai-skills quality upgrade
plan (v3.29.0). Before this phase, meta-skills followed the same conventions as domain
skills with no special governance for their elevated capabilities.
