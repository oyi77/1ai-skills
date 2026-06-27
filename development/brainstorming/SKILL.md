---
name: brainstorming
description: Effective brainstorming skill for features and projects. Clarify intent, explore options, and guide design decisions
  to align with user goals.
domain: development
tags:
- brainstorming
- coding
- software-engineering
- testing
---

persona:
  name: "Domain Expert"
  title: "Master of Brainstorming"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Brainstorming Skill

## World-Class Expert Persona

**Kent Beck** - Creator of Extreme Programming and Test-Driven Development
- **Credentials**: Author of "Test-Driven Development by Example", "Extreme Programming Explained", Smalltalk Best Practice Patterns
- **Expertise**: Agile methodologies, software design patterns, evolutionary design, simplicity in code
- **Philosophy**: "Make it work, make it right, make it fast" - Focus on incremental improvement and continuous feedback
- **Core Principles**:
  - Simple design beats clever design
  - Listen to the code - it tells you what it wants to be
  - Embrace change through small, safe steps
  - Design emerges from conversation and experimentation
  - The best architecture is the one that can evolve

## Overview

Effective brainstorming skill to use before building features. Clarify intent, explore options, and guide design decisions to align with user goals. Based on playbooks.com compound-engineering-plugin.

**Purpose**: Product thinking and design
**Use Before**: Building features, solving problems
**Output**: Clear requirements and approach

---

## When to Use

- Starting a new feature
- Solving a complex problem
- Unclear requirements
- Design decisions
- Architecture choices

---

## Brainstorming Process

- Configure align, brainstorming, clarify, decisions, design settings before first use


### 1. Clarify Intent
```
Questions to ask:
- What problem are we solving?
- Who is the user?
- What is the success criteria?
- What are the constraints?
- What's the timeline?
```

### 2. Explore Options
```
Generate alternatives:
- Approach 1: [Option]
- Approach 2: [Option]
- Approach 3: [Option]

For each:
- Pros
- Cons
- Complexity
- Trade-offs
```

### 3. Evaluate Trade-offs
```
Compare options against:
- User value
- Development cost
- Maintenance burden
- Scalability
- Time to market
```

### 4. Make Recommendations
```
Recommended approach:
- Why this choice
- Key considerations
- Potential risks
- Follow-up questions
```

---

## Framework

- Configure align, brainstorming, clarify, decisions, design settings before first use


### The 5 Whys
```
Problem: [Describe issue]
Why 1: [First cause]
Why 2: [Second cause]
Why 3: [Root cause]
Why 4: [Core problem]
Why 5: [True problem]
```

### Jobs-to-Be-Done
```
User wants to [action]
So they can [benefit]
But currently [frustration]
```

### MoSCoW Method
```
Must have: Critical features
Should have: Important features
Could have: Nice to have
Won't have: Out of scope
```

---

## Decision Framework

- Configure align, brainstorming, clarify, decisions, design settings before first use


### Build vs Buy vs Open Source
```
Build:
- Custom requirements
- Long-term control
- Learning opportunity

Buy:
- Quick deployment
- Support included
- Maintenance handled

Open Source:
- Community support
- Cost-effective
- Customizable
```

### Architecture Decisions
```
1. What are we building?
2. What are the options?
3. What did we choose and why?
4. What are the trade-offs?
5. How will we validate?
```

---

## Output Template

```
## Brainstorming Results

- Configure align, brainstorming, clarify, decisions, design settings before first use


### Problem Statement
[Clear description]

### Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Options Explored

#### Option A: [Name]
- **Pros**: [List]
- **Cons**: [List]
- **Complexity**: Low/Medium/High

#### Option B: [Name]
- **Pros**: [List]
- **Cons**: [List]
- **Complexity**: Low/Medium/High

### Recommended Approach
[Selected option with rationale]

### Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

---

## Integration

- Configure align, brainstorming, clarify, decisions, design settings before first use


### Before Building
```
1. Run brainstorming skill
2. Document decisions
3. Get stakeholder buy-in
4. Start implementation
```

### With PRD Generator
```
brainstorming → prd-generator → implementation
```

---

## Best Practices

Recommended practices for brainstorming.

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### Do's
✅ Ask clarifying questions  
✅ Consider multiple options  
✅ Challenge assumptions  
✅ Document decisions  
✅ Involve stakeholders  

### Don'ts
❌ Don't jump to solutions  
❌ Don't ignore constraints  
❌ Don't overcomplicate  
❌ Don't skip validation  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on playbooks.com compound-engineering-plugin

---


## When NOT to Use

- When the code change is in a frozen release branch under change management
- When the task requires access to production systems the agent cannot reach
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Code changes are made without running the existing test suite
- Agent does not handle error cases or edge conditions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] All existing tests pass after code changes are applied
- [ ] Error handling covers documented failure modes and edge cases
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- [prd-generator](../prd-generator/SKILL.md) - Generate specifications
- [frontend-design](../../content/frontend-design/SKILL.md) - Design implementation
- [code-reviewer](../code-reviewer/SKILL.md) - Review implementation

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
