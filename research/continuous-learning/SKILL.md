---
name: continuous-learning
description: Evolve insights from sessions into actionable skills. Create confidence-weighted learning that improves agent performance over time. Based on playbooks.com continuous-learning-v2.
---
persona:
  name: "Domain Expert"
  title: "Master of Continuous Learning"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Continuous Learning Skill

## Overview

Evolve instinct-based insights from sessions into actionable skills with confidence-weighted learning. This skill creates a feedback loop that improves agent performance over time based on playbooks.com continuous-learning-v2.

**Purpose**: Self-improvement through learning  
**Output**: New skills, improvements, learnings  
**Frequency**: Ongoing

---

## When to Use

- After successful task completion
- When encountering recurring patterns
- Before similar future tasks
- To capture learnings from failures

---

## Learning Loop

```
┌─────────────────────────────────────────────────────────┐
│                    Learning Cycle                         │
├─────────────────────────────────────────────────────────┤
│  1. Capture    →  2. Analyze    →  3. Synthesize       │
│       ↓                ↓               ↓                │
│  4. Document   →  5. Integrate  →  6. Apply           │
└─────────────────────────────────────────────────────────┘
```

### Phase 1: Capture
```
After each session, capture:
- Successful patterns
- Effective prompts
- Useful tools
- Mistakes made
- Edge cases discovered
```

### Phase 2: Analyze
```
Identify:
- Patterns across sessions
- High-value learnings
- Confidence levels
- When approaches worked/failed
```

### Phase 3: Synthesize
```
Create:
- New skill recommendations
- Prompt improvements
- Tool additions
- Workflow optimizations
```

### Phase 4: Document
```
Store in:
- MEMORY.md (curated learnings)
- skill-specific notes
- session logs
```

### Phase 5: Integrate
```
Apply:
- Update existing skills
- Create new skills
- Modify workflows
```

### Phase 6: Apply
```
Use learnings in:
- Future tasks
- Skill selection
- Problem solving
```

---

## Confidence Weighting

### Levels
```
HIGH (0.8-1.0): Repeated success, verified approach
MEDIUM (0.5-0.7): Worked a few times, needs testing
LOW (0.2-0.4): Single success, uncertain
EXPLORATORY (<0.2): Hypothesis, needs validation
```

### Application Rules
```
High confidence:
- Apply automatically
- Add to skill defaults

Medium confidence:
- Suggest as option
- Test in parallel

Low confidence:
- Propose for testing
- Monitor results

Exploratory:
- Try alongside existing
- Compare results
```

---

## Insight Types

### 1. Prompt Insights
```
What worked:
- Specific phrasing
- Structure
- Examples

How to apply:
- Add to skill prompts
- Create new patterns
```

### 2. Tool Insights
```
What worked:
- Tool combinations
- Sequencing
- Parameters

How to apply:
- Add to workflow skills
- Update tool usage
```

### 3. Approach Insights
```
What worked:
- Problem decomposition
- Reasoning patterns
- Verification methods

How to apply:
- Create methodology skills
- Update process skills
```

### 4. Failure Insights
```
What didn't work:
- Root causes
- Edge cases
- Assumptions wrong

How to prevent:
- Add to skill guards
- Create validation steps
```

---

## Implementation

### Session Analysis
```typescript
async function analyzeSession(session) {
  const insights = {
    prompts: extractPromptPatterns(session),
    tools: extractToolUsage(session),
    approaches: extractApproaches(session),
    failures: extractFailures(session)
  };
  
  const weighted = insights.map(i => ({
    ...i,
    confidence: calculateConfidence(i)
  }));
  
  return weighted;
}
```

### Skill Generation
```typescript
async function generateSkill(insight) {
  if (insight.confidence < 0.5) return null;
  
  const skill = {
    name: insight.name,
    trigger: insight.trigger,
    action: insight.action,
    confidence: insight.confidence
  };
  
  return skill;
}
```

---

## Learning Storage

### Structure
```
learning/
├── insights/
│   ├── high-confidence/
│   ├── medium-confidence/
│   └── exploratory/
├── skills/
│   ├── created/
│   └── proposed/
├── patterns/
│   ├── prompts/
│   ├── tools/
│   └── approaches/
└── feedback/
    ├── success/
    └── failure/
```

---

## Integration

### With Runtime-Self-Improvement
```
1. Capture insights during tasks
2. Analyze for patterns
3. Generate skills
4. Apply improvements
5. Commit changes
```

### With Skill-Performance-Monitor
```
- Track insight effectiveness
- Measure improvement impact
- Identify new opportunities
```

---

## Metrics

| Metric | Target |
|--------|--------|
| Insights captured/session | 3+ |
| High-confidence insights | 30%+ |
| Skills generated/month | 5+ |
| Improvement in success rate | 10%+/quarter |

---

## Best Practices

### Do's
✅ Capture every session  
✅ Be specific about what worked  
✅ Weight confidence honestly  
✅ Review learnings regularly  
✅ Test before full application  

### Don'ts
❌ Don't overfit to single cases  
❌ Don't ignore failures  
❌ Don't skip edge cases  
❌ Don't apply low-confidence blindly  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on playbooks.com continuous-learning-v2

---


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

## Related Skills

- [runtime-self-improvement](/skills/runtime-self-improvement) - Apply improvements
- [skill-performance-monitor](/skills/skill-performance-monitor) - Track effectiveness
- [self-improving-agent](/skills/self-improving-agent) - Basic self-improvement
