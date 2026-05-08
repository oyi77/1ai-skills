name: skill-evolution
description: Manage skill versions, track changes, and enable safe evolution. Version control, dependency management, and rollback capabilities for skills.
persona:
  name: Version Control Expert
  expertise: Git, semantic versioning, dependency management
  philosophy: Change is constant, safety is paramount

## Skill Evolution

Version control for skills.

### Versioning Strategy

```yaml
version_format: major.minor.patch
major: breaking_changes
minor: new_features
patch: bug_fixes

examples:
  - 1.0.0: Initial release
  - 1.1.0: Added new capability
  - 1.1.1: Fixed bug
  - 2.0.0: Breaking change
```

### Evolution Workflow

```python
# Create new version
/skill-evolution create-version skill-name --type minor

# Compare versions
/skill-evolution compare v1.0.0 v1.1.0 --skill seo-optimizer

# Rollback if needed
/skill-evolution rollback skill-name --to v1.0.0
```

### Dependency Management

```yaml
dependencies:
  seo-optimizer:
    requires:
      - web-scraper: ">=2.0.0"
      - content-analyzer: ">=1.5.0"
    used_by:
      - content-strategy
      - marketing-suite
```

### Features

- Automatic versioning on changes
- Dependency tracking
- Breaking change detection
- Migration guides generation
- Rollback capabilities

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

