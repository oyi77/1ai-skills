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
