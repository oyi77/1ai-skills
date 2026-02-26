---
name: brainstorming
description: Effective brainstorming skill for features and projects. Clarify intent, explore options, and guide design decisions to align with user goals.
---

# Brainstorming Skill

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

## Related Skills

- [prd-generator](/skills/prd-generator) - Generate specifications
- [frontend-design](/skills/frontend-design) - Design implementation
- [code-reviewer](/skills/code-reviewer) - Review implementation
