---
name: skill-performance-monitor
description: Monitor and analyze skill effectiveness in real-time. Track usage, success rates, response quality, and user satisfaction for continuous optimization.
---
persona:
  name: "Brendan Gregg"
  title: "The Performance Engineering Expert - Master of Metrics"
  expertise: ['Performance Monitoring', 'Metrics', 'Observability', 'Analytics']
  philosophy: "If you can't measure it, you can't improve it."
  credentials: ['Netflix Senior Performance Engineer', "Author of 'Systems Performance'", 'Created performance methodologies']
  principles: ['Measure what matters', 'Alert on symptoms', 'Analyze root causes', 'Optimize iteratively']



# Skill Performance Monitor

## Overview

Monitor skill performance in real-time. Track usage patterns, success rates, response quality, and user satisfaction. Use data-driven insights to optimize skill selection and improve overall system effectiveness.

**Purpose**: Real-time skill analytics  
**Target**: All 1ai-skills  
**Output**: Optimization recommendations

---

## Core Functions

### 1. Usage Tracking
```
Track:
- How often each skill is used
- When skills are selected
- Success/failure of skill tasks
- Time to complete tasks
```

### 2. Quality Metrics
```
Measure:
- Response accuracy
- User satisfaction scores
- Task completion rates
- Error rates
```

### 3. Pattern Analysis
```
Identify:
- Peak usage times
- Popular skill combinations
- Failed skill matches
- Improvement opportunities
```

### 4. Optimization
```
Recommend:
- Better skill keywords
- New skill integrations
- Workflow improvements
- Training data
```

---

## Implementation

### Task Logger
```typescript
class SkillPerformanceMonitor {
  async logTask(task) {
    const log = {
      taskId: uuid(),
      timestamp: Date.now(),
      userRequest: task.input,
      matchedSkill: task.skill,
      success: task.success,
      duration: task.endTime - task.startTime,
      feedback: task.userFeedback, // 1-5 stars
      error: task.error
    };
    
    await this.saveToDatabase(log);
  }
}
```

### Analytics Engine
```typescript
async function analyzePerformance(skillName) {
  const logs = await getSkillLogs(skillName);
  
  const metrics = {
    usage: logs.length,
    successRate: logs.filter(l => l.success).length / logs.length,
    avgDuration: logs.reduce((a, b) => a + b.duration, 0) / logs.length,
    userRating: logs.reduce((a, b) => a + b.feedback, 0) / logs.filter(l => l.feedback).length,
    errors: logs.filter(l => l.error).map(l => l.error)
  };
  
  return metrics;
}
```

### Optimization Recommendations
```typescript
async function getRecommendations() {
  const skills = await getAllSkills();
  const recommendations = [];
  
  for (const skill of skills) {
    const metrics = await analyzePerformance(skill.name);
    
    // Check for issues
    if (metrics.successRate < 0.7) {
      recommendations.push({
        type: 'fix',
        skill: skill.name,
        issue: `Low success rate: ${(metrics.successRate * 100).toFixed(1)}%`,
        action: 'Improve skill prompts or keywords'
      });
    }
    
    if (metrics.usage === 0) {
      recommendations.push({
        type: 'remove',
        skill: skill.name,
        issue: 'Unused skill',
        action: 'Consider removing or promoting'
      });
    }
    
    if (metrics.userRating && metrics.userRating < 3) {
      recommendations.push({
        type: 'improve',
        skill: skill.name,
        issue: `Low rating: ${metrics.userRating.toFixed(1)}/5`,
        action: 'Review and enhance responses'
      });
    }
  }
  
  return recommendations;
}
```

---

## Metrics Dashboard

### Per-Skill Metrics
| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Success Rate | >90% | 70-90% | <70% |
| Avg Duration | <30s | 30-60s | >60s |
| User Rating | >4 | 3-4 | <3 |
| Usage/Week | >10 | 1-10 | 0 |

### System Metrics
| Metric | Target |
|--------|--------|
| Overall Success Rate | >85% |
| Average Response Time | <30s |
| User Satisfaction | >4/5 |
| Skill Match Rate | >90% |

---

## Analytics Views

### Skill Leaderboard
```typescript
async function getLeaderboard() {
  const skills = await getAllSkills();
  const rankings = await Promise.all(
    skills.map(async s => ({
      skill: s.name,
      score: await calculateScore(s)
    }))
  );
  
  return rankings.sort((a, b) => b.score - a.score);
}
```

### Trend Analysis
```typescript
async function getTrends(days = 7) {
  const logs = await getLogsSince(days);
  
  return {
    mostUsed: countBy(logs, 'skill').top(5),
    mostSuccessful: filterBy(logs, 'success').top(5),
    trending: calculateTrend(logs),
    issues: detectAnomalies(logs)
  };
}
```

---

## Auto-Optimization

### Triggered Actions
```typescript
const autoActions = {
  // If success rate drops below threshold
  lowSuccess: {
    threshold: 0.7,
    action: 'alert',
    notify: true
  },
  
  // If skill unused for extended period
  unused: {
    threshold: 30 * 24 * 60 * 60 * 1000, // 30 days
    action: 'recommend',
    suggestion: 'Consider deprecating or promoting'
  },
  
  // If error rate spikes
  errorSpike: {
    threshold: 0.2,
    action: 'fix',
    autoApply: false
  }
};
```

### Learning Integration
```typescript
async function improveFromFeedback(feedback) {
  // Learn from user corrections
  if (feedback.correctedSkill) {
    await addToKeywordMapping(
      feedback.userRequest,
      feedback.correctedSkill
    );
  }
  
  // Learn from success
  if (feedback.success && feedback.confident) {
    await addToTrainingData(feedback);
  }
}
```

---

## Reporting

### Daily Report
```typescript
async function generateDailyReport() {
  const stats = await getTodayStats();
  
  return `
## Daily Skill Performance Report

**Date**: ${new Date().toDateString()}

### Usage
- Total tasks: ${stats.total}
- Successful: ${stats.success} (${stats.successRate}%)
- Failed: ${stats.failed}

### Top Skills
${stats.topSkills.map(s => `- ${s.name}: ${s.usage} uses`).join('\n')}

### Issues
${stats.issues.map(i => `- ${i.skill}: ${i.issue}`).join('\n') || 'None'}

### Recommendations
${stats.recommendations.map(r => `- ${r}`).join('\n') || 'None'}
  `;
}
```

---

## Integration

### With Runtime-Self-Improvement
```
Monitor:
- Track skill performance
- Detect improvements
- Feed back to self-improvement

Loop:
1. Monitor → 2. Analyze → 3. Improve → 4. Monitor
```

### With Auto-Git-Committer
```
On optimization:
1. Apply improvements
2. Track new metrics
3. Commit changes
4. Monitor impact
```

### With Heartbeat
```
Periodic checks:
1. Get current metrics
2. Compare to baseline
3. Alert on anomalies
4. Recommend improvements
```

---

## Best Practices

### Do's
✅ Track everything initially  
✅ Review metrics daily  
✅ Act on warnings  
✅ Keep historical data  
✅ Share insights with user  

### Don'ts
❌ Don't over-optimize  
❌ Don't remove skills without backup  
❌ Don't ignore low usage  
❌ Don't rely only on metrics  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation

---

## Related Skills

- [runtime-self-improvement](/skills/runtime-self-improvement) - Apply improvements
- [auto-git-commiter](/skills/auto-git-commiter) - Commit changes
- [self-improving-agent](/skills/self-improving-agent) - Learn and improve
