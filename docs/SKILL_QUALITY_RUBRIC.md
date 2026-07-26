# 1ai-Skill Quality Rubric v1.0.0

Scoring framework for evaluating skill quality. Used by the evaluation system
(Phase 7) and by authors as a self-assessment checklist.

Each dimension is scored 0-10. The quality score is the percentage of points
earned out of the maximum possible for that skill's tier.

---

## Tier Definitions

Skills are evaluated in one of three tiers based on complexity:

| Tier | Criteria | Max Points |
|------|----------|------------|
| **Reference** | Read-only, advisory, documentation. No executable code. No side effects. No tool requirements beyond read. | 40 |
| **Standard** | Has code examples, tool requirements, or structured outputs. May modify system state. | 70 |
| **Operational** | Has dependencies, permissions, long-running processes, or multi-agent coordination. Requires risk-level documentation. | 100 |

Tier is determined automatically: Reference if `risk_level=info` AND
`code_blocks < 3`, Operational if `risk_level >= high` OR `permissions`
is populated OR `dependencies` has entries. Default is Standard.

---

## Dimension 1: Completeness (max 10)

| Score | Criteria |
|-------|----------|
| 0 | No frontmatter or body |
| 2 | Frontmatter has name and description only |
| 4 | All required frontmatter fields AND all required sections present |
| 6 | Same as 4 + has `## When NOT to Use` section |
| 8 | Same as 6 + has `## Anti-Rationalization Table` with 3+ rows |
| 10 | Complete: all required + recommended sections, anti-rationalization, verification checklist |

## Dimension 2: Depth & Specificity (max 10)

| Score | Criteria |
|-------|----------|
| 0 | Stub: no substance beyond frontmatter |
| 2 | Content exists but generic (could apply to any tool/domain) |
| 4 | Domain-specific with real command names, configs, API references |
| 6 | Same as 4 + concrete parameters, version numbers, error handling |
| 8 | Same as 6 + edge cases, failure modes, dead-end decision trees |
| 10 | Battle-tested: real-world scenarios, non-obvious traps, recovery procedures, and provenance (why these choices work) |

## Dimension 3: Code Quality & Verifiability (max 10)

| Score | Criteria |
|-------|----------|
| 0 | No code blocks |
| 2 | Code blocks present but illustrative (not runnable) |
| 4 | Runnable code blocks with language annotations |
| 6 | Same as 4 + code guarded against real errors (try/except, validation) |
| 8 | Same as 6 + expected outputs documented, surface-level unit test |
| 10 | Production-grade: tested statements, benchmark numbers, output examples in comments, no placeholder values |

## Dimension 4: Safety & Risk Management (max 10)
*(Weighted 2x for Operational-tier skills)*

| Score | Criteria |
|-------|----------|
| 0 | No safety documentation |
| 3 | Risk level declared, no further detail |
| 5 | `## When NOT to Use` section with concrete contraindications |
| 7 | Same as 5 + explicit permission declarations in frontmatter |
| 10 | Same as 7 + `human_approval` correctly set, rollback procedures documented, irreversible-action warnings |

## Dimension 5: Anti-Rationalization (max 10)

| Score | Criteria |
|-------|----------|
| 0 | No anti-rationalization section |
| 3 | Has `## Anti-Rationalization Table` header but 0-1 rows |
| 5 | Table with 2-3 rows covering obvious shortcuts |
| 8 | Table with 4-6 rows covering both obvious and subtle rationalizations |
| 10 | Table with 7+ rows, covers the temptation to skip verification, the false economy of "just this once," and reasons why the skill might fail silently |

## Dimension 6: Discoverability & Routing (max 10)

| Score | Criteria |
|-------|----------|
| 0 | Missing description or "Use when" trigger |
| 2 | Description exists but no trigger phrase |
| 4 | Description has "Use when" but no tags |
| 6 | Full description + tags + domain/category set correctly |
| 8 | Same as 6 + triggers/non_triggers fields populated |
| 10 | Same as 8 + cross-references to related skills in dependencies, alias entries in registry for common misspellings |

## Dimension 7: Cross-References & Dependencies (max 10)

| Score | Criteria |
|-------|----------|
| 0 | No cross-references |
| 3 | `skill://` links present and all resolve |
| 5 | Same as 3 + `dependencies` array populated in frontmatter |
| 7 | Same as 5 + backward references (dependent skills link back) |
| 10 | Same as 7 + dependency graph is acyclic, version constraints on deps |

## Dimension 8: Maintenance Hygiene (max 10)

| Score | Criteria |
|-------|----------|
| 0 | No author/license/version fields |
| 3 | Author and license present |
| 5 | Same as 3 + version field with correct semver |
| 7 | Same as 5 + last_reviewed date within 6 months |
| 10 | Same as 7 + owners array, evaluation_profile populated, changelog entry links |

## Dimension 9: Verification (max 10)
*(Standard and Operational tiers only)*

| Score | Criteria |
|-------|----------|
| 0 | No verification section |
| 3 | `## Verification` header exists but generic ("check the output") |
| 5 | Concrete verification steps with expected observable results |
| 7 | Same as 5 + automated check script or assertion |
| 10 | Same as 7 + rollback/recovery procedure documented |

## Dimension 10: Monetization / ROI Context (max 10)
*(Content, marketing, sales, trading categories only)*

| Score | Criteria |
|-------|----------|
| 0 | No mention of value creation |
| 3 | Skilled described as "useful" without concrete outcomes |
| 5 | Mentions specific income or efficiency metric |
| 7 | Case study or real numbers ("used to find 3 zero-day vulns in a week") |
| 10 | Full ROI breakdown with expected value calculation |

---

## Quality Score Computation

```
points_earned = sum(scores)
max_points = tier_max_points  # 40/70/100

# Safety weight for Operational tier
if tier == "Operational":
    safety_bonus = min(dimension4_score, 10) * 0.2  # up to 2 extra points
    points_earned += safety_bonus

quality_score = min(round(points_earned / max_points * 100), 100)
```

| Quality Score | Rating | Label |
|---------------|--------|-------|
| 90-100 | A | Production-ready |
| 70-89 | B | Solid, minor gaps |
| 50-69 | C | Adequate, needs work |
| 30-49 | D | Significant gaps |
| 0-29 | F | Not fit for use |

---

## Usage

### For Authors
Run self-assessment before submitting a new skill:
```bash
python3 scripts/evaluate-skill.py --skill <name>
```

### For Reviewers
Score new skills against the rubric in code review. Target: B+ (75+) for
merge, A- (85+) for core/cybersecurity/finance skills.

### For Automated Evaluation
The 10 dimensions map to the `evaluation_profile` in skill frontmatter:
```yaml
evaluation_profile:
  quality_score: 85
  test_count: 12
  last_evaluated: "2026-07-26"
```
