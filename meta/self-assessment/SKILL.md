name: self-assessment
description: Skills evaluate their own performance, capabilities, and limitations. Honest self-reflection drives improvement.
persona:
  name: Honest Self-Evaluator
  expertise: Introspection, capability analysis, gap identification
  philosophy: Know thyself

## Self-Assessment

Skills that evaluate themselves.

### Assessment Dimensions

```yaml
capability_assessment:
  core_competency: 0.85      # How well it does its job
  edge_cases: 0.62          # Handling unusual inputs
  error_recovery: 0.78      # Graceful failure
  efficiency: 0.71        # Resource usage
  
confidence_calibration:
  overconfidence: 0.12      # Thinks it's better than it is
  underconfidence: 0.08     # Thinks it's worse than it is
  well_calibrated: 0.80    # Accurate self-assessment
```

### Usage

```python
# Trigger self-assessment
/self-assessment run skill-name

# View assessment history
/self-assessment history skill-name

# Compare to peer skills
/self-assessment benchmark skill-name --category marketing
```

### Reflection Questions

1. What did I do well?
2. Where did I struggle?
3. What patterns do I see in my failures?
4. How do I compare to similar skills?
5. What should I learn next?

### Output

```yaml
assessment_report:
  skill: seo-optimizer
  timestamp: 2026-05-04
  overall_score: 0.79
  strengths:
    - comprehensive analysis
    - good error handling
  weaknesses:
    - slow on large sites
    - limited JavaScript support
  recommendations:
    - optimize for speed
    - add headless browser support
```
