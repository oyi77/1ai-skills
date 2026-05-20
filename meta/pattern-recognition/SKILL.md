---
name: pattern-recognition
description: Identify patterns in skill execution, errors, and successes. Recognize when situations match previous patterns and apply learned solutions.
persona:
  name: Pattern Recognition Expert
  expertise: Pattern matching, anomaly detection, similarity analysis
  philosophy: History repeats itself

## Pattern Recognition

Recognize patterns to predict and optimize.

### Pattern Types

```yaml
pattern_categories:
  input_patterns:
    - similar_queries
    - common_mistakes
    - edge_cases
    
  execution_patterns:
    - successful_sequences
    - failure_sequences
    - resource_usage_patterns
    
  error_patterns:
    - recurring_errors
    - error_clusters
    - recovery_strategies
```

### Usage

```python
# Detect patterns
/pattern-recognition analyze --skill seo-optimizer --lookback 30d

# Match current situation
/pattern-recognition match "current query" --skill seo-optimizer

# Suggest based on patterns
/pattern-recognition suggest --for "error message"
```

### Applications

- Predict likely failures before they happen
- Suggest optimizations based on past successes
- Group similar tasks for batch processing
- Identify outliers requiring special handling

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

