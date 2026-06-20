---
name: performance-monitor
description: Track and analyze skill execution performance. Measure latency, success rates, accuracy, and resource usage for
  continuous improvement.
domain: meta
tags:
- meta-learning
- monitor
- performance
- self-improvement
- skill-evolution
persona:
  name: Performance Engineer
  expertise: Metrics, monitoring, optimization
  philosophy: If you can't measure it, you can't improve it
  credentials: SRE at Google, built monitoring systems
---
## Performance Monitor

Track every skill execution with comprehensive metrics.

### Metrics Tracked

```yaml
execution_metrics:
  latency_ms: 245
  success: true
  error_type: null
  tokens_used: 1847
  cost_usd: 0.004
  cache_hit: false
  
quality_metrics:
  user_satisfaction: 0.87  # 0-1 scale
  output_quality: 0.92   # auto-rated
  completeness: 0.95     # task completion %
  
resource_metrics:
  memory_mb: 127
  cpu_percent: 34
  disk_io: 2.3
```

### Usage

```python
# Start monitoring
## When to Use

**Trigger phrases:**
- "performance monitor"
- "Help me with performance monitor"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/performance-monitor start skill-name

# Get report
/performance-monitor report skill-name --days 7

# Compare skills
/performance-monitor compare skill1 skill2 --metric success_rate
```

### Features

- Real-time metric collection
- Historical trend analysis
- Anomaly detection
- Performance regression alerts
- Cost tracking per skill

## When NOT to Use

- When monitoring collects data subject to employee privacy regulations
- When performance metrics are used for compensation decisions
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Monitoring collects metrics without actionable alerting thresholds
- Agent does not distinguish between leading and lagging indicators
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Alerting thresholds are actionable, not just informational
- [ ] Leading indicators are distinguished from lagging indicators
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
