---
name: trade-off-analysis
description: Evaluate opportunity costs and prioritize using Eisenhower Matrix, MoSCoW, and cost of delay. Use when prioritizing
  with constrained resources.
domain: mindset
tags:
- mindset
- 'off'
- personal-development
- soft-skills
- trade
---

# Trade-Off Analysis

Framework for explicit trade-off evaluation and prioritization under constraints. Covers opportunity cost, Eisenhower Matrix, MoSCoW, and cost of delay.

## When to Use

- Prioritizing initiatives with limited time/budget/people
- Choosing between mutually exclusive options
- Evaluating what to cut when resources are constrained
- Making explicit trade-offs visible to stakeholders
- **When NOT to use**: Unlimited resources (rare), non-exclusive options (do both), or decisions with one dominant choice

## Core Concept: Opportunity Cost

**Definition**: The value of the next-best alternative you forgo when making a choice.

**Formula**: `Opportunity Cost = Value of Best Alternative - Value of Chosen Option`

**Example**:
- Option A: Build feature (expected $100K revenue)
- Option B: Fix technical debt (expected $80K cost savings)
- **If you choose A**: Opportunity cost = $80K (you forgo the cost savings)
- **If you choose B**: Opportunity cost = $100K (you forgo the revenue)

**Key insight**: Every "yes" is a "no" to something else. Make it explicit.

## Frameworks

### 1. Eisenhower Matrix

**Best for**: Task prioritization (personal or team)

| Urgent / Important | **Urgent** | **Not Urgent** |
|--------------------|------------|----------------|
| **Important** | **DO** (crises, deadlines) | **SCHEDULE** (strategy, planning) |
| **Not Important** | **DELEGATE** (interruptions, some emails) | **ELIMINATE** (busy work, time-wasters) |

**Example**:
- DO: Production down (urgent + important)
- SCHEDULE: Quarterly planning (not urgent, but important)
- DELEGATE: Expense reports (urgent, not important)
- ELIMINATE: Unnecessary meetings (neither)

**Common trap**: Spending all time in "Urgent" quadrants. Schedule time for "Important but Not Urgent."

### 2. MoSCoW Method

**Best for**: Feature prioritization, MVP scoping

| Priority | Meaning | Decision Rule |
|----------|---------|---------------|
| **Must have** | Non-negotiable for launch | If missing, don't ship |
| **Should have** | Important but not critical | Ship if time allows |
| **Could have** | Nice to have | Ship if zero cost |
| **Won't have** | Out of scope | Explicitly deprioritize |

**Example** (MVP for SaaS product):
- **Must**: User auth, core workflow, billing
- **Should**: Email notifications, basic reporting
- **Could**: Dark mode, advanced analytics
- **Won't**: Mobile app, integrations

### 3. Cost of Delay (CD3)

**Best for**: Prioritizing features with time-sensitive value

**Formula**: `CD3 = Cost of Delay / Duration`

**Example**:
| Feature | Value ($K/mo) | Duration (mo) | Cost of Delay ($/mo) | CD3 |
|---------|---------------|---------------|----------------------|-----|
| Feature A | 50 | 2 | 50 | **25** |
| Feature B | 30 | 1 | 30 | **30** |
| Feature C | 80 | 4 | 80 | **20** |

**Conclusion**: Prioritize Feature B (highest CD3), then A, then C.

**Insight**: Smaller, high-value features often beat large, slow features.

### 4. Opportunity Cost Stack Ranking

**Process**:
1. List all options
2. For each, calculate expected value (or score)
3. Sort by value/cost ratio (bang for buck)
4. Fund from top until resources exhausted
5. Explicitly document what you're NOT doing (opportunity cost)

**Example**:

| Initiative | Expected Value ($K) | Cost (person-months) | Value/Cost | Rank | Decision |
|------------|---------------------|----------------------|------------|------|----------|
| A | 500 | 10 | 50 | 1 | ✅ Fund |
| B | 300 | 5 | 60 | 2 | ✅ Fund |
| C | 200 | 8 | 25 | 3 | ❌ Defer |
| D | 150 | 3 | 50 | 4 | ❌ Defer |

**Conclusion**: Fund A and B (15 person-months). Defer C and D (opportunity cost = $350K forgone value).

## Trade-Off Dimensions

| Dimension | Trade-Off | Example |
|-----------|-----------|---------|
| **Speed vs Quality** | Ship fast with bugs vs ship slow, polished | MVP vs enterprise-grade |
| **Cost vs Performance** | Cheap/slow vs expensive/fast | Shared hosting vs dedicated servers |
| **Flexibility vs Simplicity** | Configurable (complex) vs opinionated (simple) | WordPress vs static site |
| **Short-term vs Long-term** | Quick wins vs strategic investment | Hack vs rebuild |

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "We can do both" | Resources are finite. Doing both means doing both poorly. |
| "This won't take long" | Underestimating effort is the default. Buffer by 50%. |
| "We can't say no to the CEO" | Someone must make trade-offs explicit. That's your job. |
| "Let's just try it and see" | Experiments have opportunity cost. Prioritize experiments too. |

## Red Flags

- You say "yes" to everything (no explicit trade-offs)
- You haven't calculated opportunity cost (what are you NOT doing?)
- You prioritize based on who's loudest, not value/cost
- You don't revisit priorities when new information arrives
- You spend all time in "Urgent" quadrant (firefighting, no strategy)

## Verification

- [ ] Opportunity cost made explicit (what are you forgoing?)
- [ ] Framework selected (Eisenhower, MoSCoW, CD3, or stack ranking)
- [ ] All options evaluated with same criteria (apples to apples)
- [ ] Resources mapped to priorities (funding decisions aligned)
- [ ] Trade-off dimensions identified (speed vs quality, cost vs performance, etc.)
- [ ] Stakeholders aligned on priorities and what's deferred

## Overview

> Section content — see SKILL.md body for full details.
