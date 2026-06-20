---
name: self-assessment
description: Skills evaluate their own performance, capabilities, and limitations. Honest self-reflection drives improvement.
domain: meta
tags:
- assessment
- meta-learning
- self
- self-improvement
- skill-evolution
persona:
  name: Honest Self-Evaluator
  expertise: Introspection, capability analysis, gap identification
  philosophy: Know thyself
---
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
## When to Use

**Trigger phrases:**
- "self assessment"
- "Help me with self assessment"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

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

## Overview

> Section content — see SKILL.md body for full details.
