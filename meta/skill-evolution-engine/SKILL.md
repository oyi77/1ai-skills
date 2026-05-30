---
name: skill-evolution-engine
description: Self-improving skill system that auto-extracts patterns from sessions into reusable skills with confidence scoring, skill versioning, import/export, and continuous improvement loops. Use when extracting skills from session patterns, running skill stocktakes, evolving instincts into skills, or managing skill versioning and gap analysis.
domain: meta
tags: [self-improvement, skill-evolution, confidence-scoring, continuous-learning, stocktake, gap-analysis]
persona:
  name: "Lamarck"
  title: "Skill Evolution Architect"
  expertise: ["Pattern Extraction", "Confidence Scoring", "Skill Versioning", "Gap Analysis", "Continuous Improvement Loops"]
  philosophy: "Skills are not written -- they are grown. Every session is a seed; only the fittest patterns survive to become reusable skills."
---

## Overview

The Skill Evolution Engine turns raw session activity into refined, reusable skills through a continuous improvement loop: observe, extract, score, evolve, and deploy. Instead of manually writing skills from scratch, the engine identifies repeated successful patterns in agent sessions, promotes them to instincts (atomic learned behaviors), clusters related instincts into coherent skills, and version-tracks them through their lifecycle. This creates a system that gets measurably better with every session.

## When to Use

- Extracting reusable patterns from successful agent sessions
- Promoting high-confidence instincts into full skills, commands, or agents
- Running a skill stocktake to audit quality, coverage, and freshness
- Identifying gaps where no skill exists for a common task pattern
- Versioning skills through major/minor/patch lifecycle
- Importing or exporting skill libraries across projects
- Configuring continuous learning hooks for automatic pattern capture

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Process / Steps
1. Gather requirements and constraints from the user
2. Validate prerequisites (tools, permissions, data)
3. Execute the core operation with error handling
4. Verify output meets quality standards
5. Report results and log for future reference


### 1. Observation Layer: Capture Session Patterns

**Hook-Based Observation Capture**

Automatic capture via PreToolUse/PostToolUse hooks records:
- Tool calls made (which tools, in what order)
- User corrections (where the agent was wrong and got corrected)
- Error resolutions (how errors were fixed)
- Repeated workflows (patterns seen 3+ times)
- Task outcomes (success/failure with context)

**Observation Storage**
```
projects/<project-hash>/observations.jsonl   # Per-project observations
instincts/personal/                          # Global instincts
```

Each observation is a JSONL record:
```json
{
  "timestamp": "2026-05-28T10:30:00Z",
  "session_id": "abc123",
  "project": "my-react-app",
  "pattern": "user-corrected-to-functional-style",
  "context": "Writing new React component, used class syntax, user said 'use hooks'",
  "tools": ["Edit", "Read"],
  "outcome": "correction"
}
```

### 2. Pattern Detection: From Observations to Instincts

A background observer agent (use a fast/cheap model) analyzes observations and creates atomic instincts:

**Instinct Structure**
```yaml
---
id: prefer-react-hooks
trigger: "when writing React components"
confidence: 0.7
domain: "code-style"
source: "session-observation"
scope: project
project_id: "a1b2c3d4e5f6"
project_name: "my-react-app"
created: "2026-05-28"
last_observed: "2026-05-28"
observation_count: 5
---

# Prefer React Hooks

## Action
Use functional components with hooks over class components.

## Evidence
- Observed 5 user corrections from class to functional style
- Zero corrections in the other direction
- Consistent across 3 sessions

## When This Does NOT Apply
- Legacy codebase explicitly using classes
- Error boundary components (require class syntax)
```

**Confidence Scoring**

| Confidence | Meaning | Behavior |
|------------|---------|----------|
| 0.3 - 0.4 | Tentative | Suggestion only, shown as "consider..." |
| 0.5 - 0.6 | Moderate | Applied with explicit note, easy to override |
| 0.7 - 0.8 | Strong | Auto-applied with logging, user can revert |
| 0.9 - 1.0 | Near certain | Candidate for promotion to skill |

**Confidence Update Rules**
- User follows instinct suggestion: +0.1 (cap at 1.0)
- User overrides instinct: -0.15 (floor at 0.1)
- Same pattern observed in new project: +0.05 (cross-project validation)
- No observations for 30 days: -0.05 (decay)
- Below 0.2: archived (not deleted, can be revived)

### 3. Skill Evolution: From Instincts to Skills

**Evolution Pipeline**
```
Observations -> Instincts (0.3) -> Clustered Instincts -> Draft Skill -> Validated Skill (0.9)
```

**Step 1: Cluster Related Instincts**
Group instincts by domain and trigger pattern:
```markdown
Cluster: "React Component Patterns"
  - prefer-react-hooks (0.8)
  - use-const-for-components (0.7)
  - extract-custom-hooks (0.6)
  - avoid-multiple-effects (0.7)
```

**Step 2: Synthesize into Skill**
Combine clustered instincts into a coherent skill:
```markdown
---
name: react-component-patterns
description: React component writing patterns learned from session observations.
confidence: 0.72  # Average of cluster
source: instinct-cluster
version: 0.1.0
---

## Patterns
[Combined content from all clustered instincts]
```

**Step 3: Validate**
- Apply the skill to 5+ new tasks
- Track success rate (must be >= 80%)
- If successful, bump to version 1.0.0
- If failing, iterate on skill content or reduce confidence

**Step 4: Promote to Production Skill**
- Version >= 1.0.0
- Confidence >= 0.9
- Validated on 10+ tasks
- Covers a distinct, reusable workflow

### 4. Skill Versioning and Lifecycle

**Semantic Versioning**
```yaml
version_format: major.minor.patch
major: Breaking changes to skill behavior or structure
minor: New patterns, capabilities, or expanded coverage
patch: Bug fixes, typo corrections, confidence adjustments
```

**Lifecycle Stages**
| Stage | Version | Confidence | Description |
|-------|---------|------------|-------------|
| Draft | 0.x.x | 0.3-0.6 | Extracted from observations, unvalidated |
| Beta | 0.9.x | 0.6-0.8 | Tested on a few tasks, needs broader validation |
| Stable | 1.x.x | 0.8-0.9 | Validated, reliable, in active use |
| Mature | 2.x.x+ | 0.9+ | Battle-tested, widely used, rarely fails |
| Deprecated | Any | Decreasing | Replaced by better skill, scheduled for removal |
| Archived | Any | < 0.2 | No longer active, preserved for reference |

**Version Commands**
```bash
# Create new version
/skill-evolution create-version skill-name --type minor

# Compare versions
/skill-evolution compare v1.0.0 v1.1.0 --skill react-patterns

# Rollback
/skill-evolution rollback skill-name --to v1.0.0

# View history
/skill-evolution history skill-name
```

### 5. Skill Import/Export

**Export Format**
```yaml
---
export_version: "1.0"
skill_name: "react-component-patterns"
version: "1.2.0"
confidence: 0.85
exported_at: "2026-05-28T10:00:00Z"
source_project: "my-react-app"
dependencies: ["typescript-patterns", "testing-library-patterns"]
---

[Full skill content here]
```

**Export Workflow**
```bash
# Export single skill with metadata
/skill-evolution export react-patterns --format yaml

# Export entire skill library
/skill-evolution export-all --format yaml --output skills-export.yaml

# Export only high-confidence skills
/skill-evolution export-all --min-confidence 0.7
```

**Import Workflow**
```bash
# Import with conflict resolution
/skill-evolution import skills-export.yaml --strategy merge

# Import strategies:
#   merge    - Keep both, user resolves conflicts
#   overwrite - Replace existing skills
#   skip     - Skip if skill already exists
#   upgrade  - Only import if version is higher
```

### 6. Skill Stocktake and Gap Analysis

**Stocktake Process**
```bash
/skill-evolution stocktake
```

Produces a report covering:

**Quality Audit**
```markdown
| Skill | Version | Confidence | Last Used | Quality |
|-------|---------|------------|-----------|---------|
| react-patterns | 1.2.0 | 0.85 | 2 days ago | Good |
| python-linting | 0.3.0 | 0.4 | 30 days ago | Needs review |
| docker-deploy | 1.0.0 | 0.9 | 1 day ago | Excellent |
```

**Coverage Analysis**
- Map observed task categories to existing skills
- Identify categories with no matching skill (gaps)
- Identify categories with low-confidence skills (weak coverage)
- Identify skills that are never triggered (dead skills)

**Gap Report**
```markdown
## Skill Gaps (no skill exists)
- "database migration rollback" - observed 8 times, no skill
- "API rate limiting implementation" - observed 5 times, no skill

## Weak Coverage (confidence < 0.6)
- "error-handling-patterns" - confidence 0.4, often overridden
- "caching-strategy" - confidence 0.5, few observations

## Dead Skills (unused in 30+ days)
- "legacy-build-system" - last used 45 days ago, consider archiving
```

### 7. Continuous Improvement Loop

The full cycle that keeps the system evolving:

```
  EXECUTE (run tasks using current skills)
      |
      v
  MONITOR (hooks capture observations)
      |
      v
  LEARN (background observer creates/updates instincts)
      |
      v
  EVOLVE (cluster instincts into skills, version, validate)
      |
      v
  DEPLOY (promote validated skills to production)
      |
      v
  MEASURE (track skill performance, pass@k metrics)
      |
      v
  [back to EXECUTE]
```

**Loop Configuration**
```json
{
  "evolutionInterval": "daily",
  "maxNewInstinctsPerCycle": 10,
  "maxSkillPromotionsPerCycle": 3,
  "qualityThreshold": 0.8,
  "observationRetentionDays": 90,
  "confidenceDecayDays": 30,
  "projectScoping": true,
  "autoPromote": false
}
```

**Safety Guardrails**
- Maximum 3 skill promotions per cycle (prevent noise)
- Quality threshold must be met before promotion (prevent bad skills)
- Auto-promote disabled by default (human review recommended for v1.0+)
- Breaking change detection: if a skill update would break dependent skills, require major version bump
- Rollback on failure: if a promoted skill causes task failures, auto-revert to previous version

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I can just write skills manually" | Manual skills encode what you think works; evolved skills encode what actually works based on evidence |
| "Confidence scoring is overkill" | Without confidence, every instinct is treated equally -- bad patterns pollute good ones |
| "I do not need project-scoped instincts" | Global instincts from a React project will mislead agents in a Go project; scoping prevents cross-project contamination |
| "Skill versioning adds complexity" | Unversioned skills cannot be safely updated, rolled back, or shared; versioning is the foundation of safe evolution |
| "The stocktake can wait" | Skill libraries rot without maintenance; dead skills waste context, gaps waste developer time |
| "Auto-promote everything" | Automated promotion without validation creates a feedback loop of bad skills reinforcing bad patterns |

## Red Flags

- Instincts never getting promoted (stuck at 0.5 confidence forever)
- Skill library growing but usage staying flat (dead skill accumulation)
- Single project instincts leaking into global scope (scoping failure)
- Confidence scores never decreasing (no override feedback captured)
- Observations accumulating but no background analysis running (pipeline stalled)
- Skills with version 0.x in production for months (validation never completed)
- Skill gaps identified in stocktake but never addressed (no follow-through)
- Import overwriting skills without conflict resolution (data loss risk)
- Evolution loop running but skill quality not improving (bad pattern detection)

## Verification

- [ ] Observation hooks active: PreToolUse/PostToolUse capturing patterns
- [ ] Background observer running: observations being processed into instincts
- [ ] Confidence scoring accurate: high-confidence instincts match actual success rates
- [ ] Project scoping enforced: project instincts do not leak to other projects
- [ ] Evolution pipeline working: instincts clustering into draft skills
- [ ] Versioning in place: all production skills at version >= 1.0.0
- [ ] Stocktake completed: quality audit, coverage analysis, and gap report generated
- [ ] Gaps addressed: identified skill gaps have creation plans or existing skills expanded
- [ ] Dead skills archived: unused skills removed from active library
- [ ] Continuous loop active: execute -> monitor -> learn -> evolve -> deploy -> measure cycle running
- [ ] Safety guardrails enforced: promotion limits, quality thresholds, rollback capability
- [ ] Import/export functional: skills portable across projects with conflict resolution
