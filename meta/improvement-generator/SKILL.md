---
name: improvement-generator
description: Generate specific, actionable improvements for skills based on performance data and feedback. Create improvement
  plans, not just identify problems.
persona:
  name: Continuous Improvement Lead
  expertise: Root cause analysis, solution design, prioritization
  philosophy: Every problem has a solution
---
## Improvement Generator

Turn insights into action plans.

### Improvement Types

```yaml
improvement_categories:
  performance:
    - optimize_algorithms
    - reduce_memory
    - parallelize_work
  quality:
    - add_examples
    - improve_error_messages
    - enhance_documentation
  capability:
    - add_new_features
    - support_more_formats
    - handle_edge_cases
  reliability:
    - add_retries
    - improve_validation
    - better_error_handling
```

### Generation Process

```python
# Generate improvements
/improvement-generator create --skill seo-optimizer --data performance-report

# Prioritize improvements
/improvement-generator prioritize --impact high --effort low

# Create implementation plan
/improvement-generator plan --improvement "optimize-caching"
```

### Output Format

```yaml
improvement_plan:
  skill: seo-optimizer
  generated: 12_improvements
  prioritized:
    - id: IMP-001
      title: "Add response caching"
      impact: high
      effort: medium
      expected_gain: "40% faster"
      implementation_steps:
        - Add cache layer
        - Implement TTL
        - Add cache invalidation
      estimated_time: 2_hours
```

## When NOT to Use

- When the meta-skill would modify skills used by production systems
- When the evolution or learning process cannot be rolled back if it fails
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Meta-skill changes are applied without measuring performance impact
- Agent does not verify that changes maintain backward compatibility
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Performance is measured before and after meta-skill changes
- [ ] Backward compatibility is verified for all modifications
- [ ] All required outputs generated
- [ ] Success criteria met

