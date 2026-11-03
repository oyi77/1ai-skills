---
name: auto-consolidator
description: Use when consolidating overlapping or redundant skills across the 1ai-skills library by demoting narrow skills into sub-reference tables inside canonical parent skills without deleting physical SKILL.md files. Prevents router prefix collisions, context bloat, and redundant dispatch.
domain: core
subdomain: meta-skills
category: core
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- consolidation
- deduplication
- registry-management
- skill-maintenance
- context-optimization
triggers:
- auto consolidate
- consolidate skills
- demote skills
- merge skills
- reduce skill count
- dedup skills
argument-hint: "[category | all]"
---

# Auto-Consolidator

## Overview

Auto-Consolidator maintains the skill library's density by detecting overlapping, redundant, or prefix-colliding skills and demoting them into sub-reference tables inside canonical parent skills. It implements the **Zero Deletion Invariant**: physical SKILL.md files are never removed (preserving broken-link safety and external references), but their top-level registration in `SKILLS.json` is removed, and they are linked from the canonical parent's `## Sub-Skills & Specialized Playbooks` table.

This prevents router prefix collisions (e.g., 14 `gate-*` skills competing for the same query token), reduces context bloat, and keeps the active registry count manageable while preserving all 1,419+ physical playbooks.

## When to Use

**Trigger phrases:**
- "auto consolidate", "consolidate skills", "demote skills"
- "merge skills", "reduce skill count", "dedup skills"

Use directly when:
- Audit reveals prefix-family collisions (e.g., `seo-*`, `better-*`, `gate-*`).
- A canonical parent skill exists but lacks sub-skill references.
- SKILLS.json active count exceeds operational threshold.
- New skills are imported via `find-skills` and overlap with existing ones.

## When NOT to Use

- When a skill is the sole representative of its domain (no parent to demote into).
- When all skills in a family are atomic specialized playbooks (e.g., 780+ cybersecurity technique skills — exempt from demotion).
- When the user explicitly wants all skills individually routable.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Deleting redundant SKILL.md files saves disk space." | Physical files preserve external references, check-broken-links.py passes, and agents can still read them via direct path. Deleting breaks links. |
| "All skills should be individually routable for maximum discoverability." | 1,400 flat skills cause ~75k token context bloat and accuracy drops below 65%. Hierarchical dispatch is required at scale. |
| "Prefix families are fine as long as triggers are specific." | Triggers help but don't eliminate collision. A single parent router with sub-references routes more deterministically than 14 competing siblings. |
| "Consolidation is a one-time cleanup." | New imports and skill creation continuously add overlaps. Consolidation is a recurring maintenance operation. |

## Workflow

### 1. Detect Overlap Groups

Scan SKILLS.json for prefix families and near-duplicate names:

```python
from collections import defaultdict
import json

d = json.load(open("SKILLS.json"))
groups = defaultdict(list)
for s in d["skills"]:
    parts = s["name"].split("-")
    if len(parts) >= 2:
        groups[parts[0]].append(s["name"])

# Flag groups with >3 members
for prefix, members in groups.items():
    if len(members) > 3:
        print(f"COLLISION GROUP: {prefix}-* ({len(members)} skills)")
```

### 2. Identify Canonical Parent

For each overlap group, determine the canonical parent skill:
- The skill with the broadest description and highest tag count.
- The skill already registered as a `role-*` or `*-router`.
- If no natural parent exists, create one (e.g., `marketing/seo-hub`).

### 3. Demote Sub-Skills

For each non-canonical member:
1. Keep the physical SKILL.md on disk (Zero Deletion Invariant).
2. Remove the skill's top-level entry from SKILLS.json.
3. Add a sub-reference row in the canonical parent's `## Sub-Skills & Specialized Playbooks` table:

```markdown
## Sub-Skills & Specialized Playbooks

| Sub-Skill | Path | Purpose |
|---|---|---|
| `seo-technical` | `marketing/seo-technical/SKILL.md` | Technical SEO audit across 9 categories |
| `seo-geo` | `marketing/seo-geo/SKILL.md` | AI Overviews and GEO optimization |
```

### 4. Re-Index and Verify

```bash
python3 scripts/lint-skills.py --write
python3 scripts/sync-counts.py
python3 scripts/check-broken-links.py
python3 scripts/test-skills.py --quick
bash scripts/sync-skills.sh
```

### 5. Audit Router Collision Score

Run the router on a representative query from the overlap group and confirm the parent skill scores highest:

```bash
python3 scripts/skill_router.py "seo audit technical"
# Expected: parent scores > any individual sub-skill
```

## Verification

- [ ] Overlap groups identified with collision counts
- [ ] Canonical parent selected per group (broadest description, highest tag count)
- [ ] Sub-skills demoted from SKILLS.json but physical files retained
- [ ] `## Sub-Skills & Specialized Playbooks` table added to parent with relative paths
- [ ] All 4 validation gates pass (lint, broken-links, validate, test-skills)
- [ ] Router collision score confirms parent ranks highest for group queries
- [ ] Active registry count reduced; physical skill count unchanged