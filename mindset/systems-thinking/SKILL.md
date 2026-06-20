---
name: systems-thinking
description: Understand feedback loops, leverage points, and system archetypes to solve complex problems. Use when addressing
  recurring issues or unintended consequences.
domain: mindset
tags:
- mindset
- personal-development
- soft-skills
- systems
- thinking
---

# Systems Thinking

Framework for understanding complex, interconnected systems. Covers feedback loops (reinforcing/balancing), leverage points, and system archetypes.

## When to Use

- Diagnosing recurring problems that resist simple fixes
- Understanding unintended consequences of interventions
- Designing policies, processes, or products with network effects
- Analyzing ecosystems (markets, organizations, platforms)
- **When NOT to use**: Simple linear cause-effect problems, isolated incidents, or when immediate tactical action is required

## Core Concepts

### Feedback Loops

| Type | Behavior | Symbol | Example |
|------|----------|--------|---------|
| **Reinforcing (R)** | Exponential growth or collapse | ⊕ | Viral growth: more users → more invites → more users |
| **Balancing (B)** | Stabilizing, goal-seeking | ⊖ | Thermostat: temp drops → heat turns on → temp rises → heat turns off |

**Causal Loop Diagram** (CLD):
```
       +
Users ──→ Invites
  ↑         │
  │         │ +
  └─────────┘
    (R loop)
```

### Leverage Points (Donella Meadows)

Places to intervene in a system (ranked from least to most effective):

| Rank | Leverage Point | Example |
|------|----------------|---------|
| 12 (weak) | Constants (subsidies, taxes) | Lower AWS pricing |
| 9 | Delays in feedback loops | Faster CI/CD (ship-learn-iterate loop) |
| 6 | Information flows | Make metrics visible to teams |
| 3 | Goals of the system | Shift from "grow users" to "retain engaged users" |
| 1 (strong) | Paradigm (mental model) | Move from "features = value" to "outcomes = value" |

**Key insight**: Most people intervene at low-leverage points (tweaking parameters) instead of high-leverage points (changing goals or mental models).

### Stock and Flow

- **Stock**: Accumulation (users, revenue, technical debt, morale)
- **Flow**: Rate of change (new signups/day, churn/month, bugs added/week)

**Example**:
- Stock: Active users
- Inflow: New signups
- Outflow: Churn
- **Net change**: Signups - Churn

If churn > signups, stock declines (user base shrinks).

## System Archetypes

Recurring patterns in complex systems.

### 1. Fixes That Fail

**Pattern**: Quick fix addresses symptom but creates side effects that worsen the problem long-term.

**Example**:
- Problem: Bugs in production
- Fix: Rush patches without tests
- Side effect: Technical debt increases → more bugs
- **Solution**: Invest in tests and refactoring (high-leverage)

**Diagram**:
```
Problem ──(fix)──> Symptom relief
   ↑                     │
   │                     │ (delay)
   └──(side effect)──────┘
```

### 2. Shifting the Burden

**Pattern**: Symptomatic solution is easier than fundamental solution, so fundamental solution atrophies.

**Example**:
- Problem: Support overwhelmed with tickets
- Symptomatic fix: Hire more support agents
- Fundamental fix: Improve product UX
- **Result**: Keep hiring support; UX never improves

**Solution**: Invest in fundamental fix (UX) even though it's harder.

### 3. Tragedy of the Commons

**Pattern**: Individuals exploit shared resource for personal gain; resource degrades.

**Example**:
- Shared resource: Codebase quality
- Individual behavior: Ship fast without tests (personal velocity up)
- **Result**: Codebase degrades, everyone slows down

**Solution**: Align incentives (reward quality, not just speed) or enforce limits (code review, CI gates).

### 4. Success to the Successful

**Pattern**: Winner gets more resources, reinforcing their advantage (rich get richer).

**Example**:
- Team A ships fast → gets more headcount → ships even faster
- Team B struggles → gets fewer resources → falls further behind

**Solution**: Rebalance resources, invest in B's leverage points.

## Causal Loop Diagrams (CLD)

**How to draw**:
1. Identify key variables (stocks: users, revenue; flows: growth rate, churn)
2. Draw arrows showing causal relationships
3. Label polarity: `+` (same direction), `-` (opposite direction)
4. Identify loops: R (reinforcing), B (balancing)

**Example**: Product-market fit loop
```
       +              +
PMF ──────> Retention ──────> Word of mouth
 ↑                                 │
 │                                 │ +
 └─────────(R loop)────────────────┘
```

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "Just fix the symptom" | Symptom relief often worsens root cause (Fixes That Fail). |
| "This time it's different" | System archetypes recur. If it looks like Shifting the Burden, it probably is. |
| "We need more resources" | Often the leverage point is redesigning the system, not adding resources. |
| "It's too complex to model" | Even simple CLDs reveal non-obvious feedback loops. |

## Red Flags

- You keep applying the same fix and the problem recurs
- Your solution has significant delays before impact (feedback loop delayed)
- You're treating symptoms instead of root causes
- Unintended consequences keep surprising you
- You're intervening at low-leverage points (constants, subsidies) instead of high-leverage (goals, paradigms)

## Verification

- [ ] Key variables identified (stocks and flows)
- [ ] Feedback loops mapped (reinforcing or balancing)
- [ ] System archetype identified (Fixes That Fail, Shifting the Burden, etc.)
- [ ] Leverage points evaluated (intervening at high-leverage points)
- [ ] Delays accounted for (how long until feedback manifests?)
- [ ] Unintended consequences anticipated (second-order effects)

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
