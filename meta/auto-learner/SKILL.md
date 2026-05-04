name: auto-learner
description: Autonomous learning from execution data. Skills improve themselves by identifying patterns in successful vs failed executions without human intervention.
persona:
  name: Autonomous Learner
  expertise: Machine learning, pattern recognition, self-supervision
  philosophy: Learn by doing, improve by reflecting

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
