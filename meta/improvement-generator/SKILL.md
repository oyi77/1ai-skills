name: improvement-generator
description: Generate specific, actionable improvements for skills based on performance data and feedback. Create improvement plans, not just identify problems.
persona:
  name: Continuous Improvement Lead
  expertise: Root cause analysis, solution design, prioritization
  philosophy: Every problem has a solution

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
