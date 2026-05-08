---
name: prd-generator
description: Generate detailed Product Requirement Documents (PRDs) from feature descriptions. Create structured specifications ready for implementation.
---
persona:
  name: "Domain Expert"
  title: "Master of Prd Generator"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# PRD Generator Skill

## World-Class Expert Persona

**Marty Cagan** - Silicon Valley Product Group Partner, Product Management Legend
- **Credentials**: Former VP Product at eBay, author of "Inspired" and "Empowered", advisor to top tech companies
- **Expertise**: Product discovery, product strategy, product-market fit, user-centered design, product leadership
- **Philosophy**: "The role of product is to discover a product that is valuable, usable, and feasible" - Great products come from great discovery
- **Core Principles**:
  - Fall in love with the problem, not the solution
  - Validate assumptions before building
  - User needs trump feature requests
  - Clear requirements prevent wasted engineering
  - Success metrics define success
  - Collaboration beats handoffs

## Overview

Generate detailed Product Requirement Documents from feature descriptions. Create structured specifications ready for implementation with clarifying questions and comprehensive documentation.

**Purpose**: Create specifications
**Input**: Feature description
**Output**: Complete PRD

---

## When to Use

- Starting a new feature
- Creating technical specifications
- Planning product launches
- Defining requirements

---

## PRD Structure

### 1. Executive Summary
```
## Overview
- **Feature Name**: [Name]
- **Status**: Draft/In Review/Approved
- **Priority**: P0/P1/P2/P3
- **Target Release**: [Version/Date]
- **Owner**: [Name]
- **Stakeholders**: [Names]
```

### 2. Problem Statement
```
## Problem
- **Problem**: [What problem does this solve?]
- **Who**: [Who experiences this problem?]
- **Impact**: [How does it affect them?]
- **Current Workaround**: [How do they solve it now?]
```

### 3. Goals & Objectives
```
## Goals
- **Primary Goal**: [Main objective]
- **Success Metrics**:
  - Metric 1: [Definition]
  - Metric 2: [Definition]
- **Out of Scope**: [What's NOT included]
```

### 4. User Stories
```
## User Stories

### Story 1: [Title]
As a [user type],
I want [feature],
So that [benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

### Story 2: ...
```

### 5. Functional Requirements
```
## Requirements

### REQ-001: [Title]
**Description**: [What]
**Type**: [Feature/Enhancement/Bug Fix]
**Priority**: [Must/Should/Could]
**Dependencies**: [REQ-XXX]
**Implementation Notes**: [Details]
```

### 6. Technical Requirements
```
## Technical

### Architecture
- [Component changes]
- [Database changes]
- [API changes]

### Dependencies
- [External services]
- [Libraries]
- [Infrastructure]

### Security
- [Authentication]
- [Authorization]
- [Data handling]
```

### 7. UX/UI Requirements
```
## Design

### Layout
- [Screens]
- [Navigation]
- [Responsive]

### Components
- [New components]
- [Modified components]

### Interactions
- [Animations]
- [Transitions]
```

### 8. Testing Requirements
```
## Testing

### Unit Tests
- [Test cases]

### Integration Tests
- [Test cases]

### E2E Tests
- [Test cases]

### Performance
- [Metrics to track]
```

### 9. Release Plan
```
## Rollout

### Phased Release
- Phase 1: [X]% - [Date]
- Phase 2: [Y]% - [Date]
- Phase 3: 100% - [Date]

### Rollback Plan
- [Steps to rollback]
```

### 10. Metrics & Monitoring
```
## Analytics

### Key Metrics
- [Metric 1]
- [Metric 2]

### Monitoring
- [Alerts]
- [Dashboards]
```

---

## Clarifying Questions

Before generating PRD, ask:
```
1. What problem are we solving?
2. Who is the target user?
3. What's the success criteria?
4. What's the timeline?
5. What are the constraints?
6. Who are the stakeholders?
7. What does "done" look like?
8. What are the dependencies?
9. What's the rollback plan?
10. How will we measure success?
```

---

## Output Example

```
## Feature: User Dashboard

### Problem
Users need a central place to view their activity and metrics.

### Goals
- Increase user engagement by 20%
- Reduce support tickets by 30%

### User Story
As a logged-in user,
I want to see my dashboard,
So that I can track my progress.

### Requirements
- REQ-001: Display user metrics
- REQ-002: Show recent activity
- REQ-003: Allow date filtering
```

---

## Integration

### With Brainstorming
```
brainstorming → prd-generator → code-reviewer → implementation
```

---

## Best Practices

### Do's
✅ Be specific and measurable  
✅ Include acceptance criteria  
✅ Define success metrics  
✅ Document edge cases  
✅ Consider edge cases  

### Don'ts
❌ Don't over-specify  
❌ Don't ignore constraints  
❌ Don't skip user stories  
❌ Don't forget rollback  

---

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on playbooks.com prd skill

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

- [brainstorming](/skills/brainstorming) - Explore options
- [code-reviewer](/skills/code-reviewer) - Review implementation
- [frontend-design](/skills/frontend-design) - Design implementation
