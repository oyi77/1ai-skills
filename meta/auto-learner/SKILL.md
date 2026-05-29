---
name: auto-learner
description: Autonomous learning from execution data. Skills improve themselves by identifying patterns in successful vs failed
  executions without human intervention.
persona:
  name: Autonomous Learner
  expertise: Machine learning, pattern recognition, self-supervision
  philosophy: Learn by doing, improve by reflecting
---
## Auto Learner

Skills that learn from their own experience.

### Learning Mechanisms

```yaml
learning_modes:
  supervised:
    source: labeled_examples
    method: fine_tuning
    
  reinforcement:
    source: execution_outcomes
    method: reward_optimization
    
  unsupervised:
    source: execution_patterns
    method: pattern_mining
    
  self_supervised:
    source: input_output_pairs
    method: contrastive_learning
```

### Usage

```python
# Enable auto-learning
/auto-learner enable --skill seo-optimizer

# Trigger learning cycle
/auto-learner learn --skill seo-optimizer --min-samples 100

# View learned improvements
/auto-learner status --skill seo-optimizer
```

### Learning Triggers

- After 100 executions
- When success rate drops below threshold
- When new error patterns emerge
- On user request
- Scheduled daily/weekly

### Safety

- Changes are staged, not immediate
- Human approval required for major changes
- Rollback always available
- Tests must pass before deployment

## When NOT to Use

- When the learning source contains copyrighted material
- When learned patterns could encode sensitive or biased information
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Learning source quality is not validated before integration
- Agent does not test learned patterns before deploying them
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Source quality is validated before learning integration
- [ ] Learned patterns are tested before deployment
- [ ] All required outputs generated
- [ ] Success criteria met

