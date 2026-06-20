---
name: runtime-self-improvement
description: Automatically improve OpenClaw and 1ai-skills at runtime. Analyze performance, detect gaps, enhance skills, and
  self-optimize during operation.
domain: core
tags:
- improvement
- infrastructure
- memory
- runtime
- self
- self-improvement
---
persona:
  name: "Domain Expert"
  title: "Master of Runtime Self Improvement"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Runtime Self-Improvement Skill
## When to Use

**Trigger phrases:**
- "runtime self improvement"
- "Help me with runtime self improvement"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## Overview

Enable OpenClaw to continuously improve itself at runtime. Monitor performance, detect skill gaps, enhance existing skills, and optimize workflows automatically during operation.

**Purpose**: Autonomous self-improvement for OpenClaw  
**Target**: 1ai-skills, workflows, prompts, and configurations  
**Frequency**: Continuous during operation

---

## Core Functions
- Primary operation execution with input validation
- Error detection and automatic recovery
- Output formatting and quality assurance
- Integration hooks for downstream consumers


### 1. Performance Monitoring
```
During Operation:
- Track skill usage frequency
- Measure success/failure rates
- Monitor response quality
- Log user feedback
```

### 2. Gap Detection
```
Automatic:
- Identify unused skills
- Find skill overlaps
- Detect missing capabilities
- Analyze failure patterns
```

### 3. Skill Enhancement
```
On-Demand:
- Update skill descriptions
- Add new keywords
- Refine prompts
- Improve documentation
```

### 4. Workflow Optimization
```
Continuous:
- Optimize orchestration flows
- Reduce redundant steps
- Add missing integrations
- Streamline processes
```

---

## Implementation
1. Initialize the skill context with required configuration
2. Load any dependencies or connected services
3. Execute the primary operation
4. Handle errors gracefully with fallback strategies
5. Return structured results for consumption


### Hook: After Each Task
```typescript
// After completing any task, run self-improvement check
async function afterTaskCompletion(task) {
  // 1. Log task metrics
  await logTaskMetrics(task);
  
  // 2. Check for improvements
  const improvements = await analyzeTask(task);
  
  // 3. Apply if significant
  if (improvements.confidence > 0.8) {
    await applyImprovement(improvements);
  }
}
```

### Gap Detection Algorithm
```typescript
async function detectSkillGaps() {
  // 1. Get all user requests
  const requests = await getRecentRequests();
  
  // 2. Match to skills
  const matched = requests.map(r => findSkill(r));
  
  // 3. Find gaps (unmatched requests)
  const gaps = requests.filter(r => !matched(r));
  
  // 4. Propose new skills
  if (gaps.length > 10) {
    await suggestNewSkill(gaps);
  }
}
```

### Skill Enhancement
```typescript
async function enhanceSkill(skillName, feedback) {
  // 1. Analyze feedback
  const analysis = await analyzeFeedback(feedback);
  
  // 2. Update skill
  const updates = {
    keywords: [...skill.keywords, ...analysis.newKeywords],
    description: analysis.improvedDescription,
    examples: [...skill.examples, ...analysis.newExamples]
  };
  
  // 3. Apply changes
  await updateSkill(skillName, updates);
  
  // 4. Commit changes
  await autoGitCommit(`improvement(${skillName}): ${analysis.summary}`);
}
```

---

## Self-Modification Types
This section covers self-modification types for the runtime-self-improvement skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### 1. Keyword Expansion
```
Trigger: Skill used but not matched
Action: Add user keywords to skill
Example: User says "fix bug" → add "bug" to debugging skill
```

### 2. Description Refinement
```
Trigger: Skill fails to match
Action: Improve skill description
Example: Add clearer trigger phrases
```

### 3. Example Injection
```
Trigger: Successful task completion
Action: Add to skill examples
Example: Add successful prompt to skill examples
```

### 4. Prompt Optimization
```
Trigger: Repeated failures
Action: Improve skill prompts
Example: Add more specific instructions
```

---

## Safety Guards
This section covers safety guards for the runtime-self-improvement skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Always Validate
```typescript
const safeguards = {
  // Don't modify core identity
  protectedFiles: ['SOUL.md', 'USER.md', 'AGENTS.md'],
  
  // Require human approval for major changes
  requireApproval: ['new skill', 'delete skill', 'workflow changes'],
  
  // Limit changes per session
  maxChangesPerSession: 5,
  
  // Always create backup
  backupBeforeChange: true
};
```

### Approval Workflow
```typescript
async function applyChange(change) {
  if (change.requiresApproval) {
    // Ask human for approval
    const approved = await askHuman(change);
    if (!approved) return;
  }
  
  // Apply with backup
  await createBackup();
  await apply(change);
}
```

---

## Integration
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### With Heartbeat
```
During heartbeat:
1. Check for skill gaps
2. Analyze recent performance
3. Apply small improvements
4. Log changes for review
```

### With Memory System
```
Save learnings to:
- MEMORY.md (long-term)
- memory/YYYY-MM-DD.md (daily)
- skill-specific logs
```

---

## Metrics to Track

| Metric | Target |
|--------|--------|
| Skill match rate | >90% |
| Improvement suggestions | 5+/day |
| Auto-applied improvements | 2+/day |
| Success rate improvement | 5%+/week |

---

## Best Practices
This section covers best practices for the runtime-self-improvement skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Do's
✅ Back up before changes  
✅ Validate improvements  
✅ Log all modifications  
✅ Review changes regularly  
✅ Test before deploying  

### Don'ts
❌ Don't modify identity files  
❌ Don't delete without backup  
❌ Don't change core behaviors  
❌ Don't ignore user feedback  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation

---


## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- [self-improving](../self-improving/SKILL.md) - Basic self-improvement
- [auto-git-commiter](../auto-git-commiter/SKILL.md) - Auto-commit changes
- [skill-performance-monitor](../skill-performance-monitor/SKILL.md) - Monitor skill effectiveness
