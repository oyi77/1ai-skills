---
name: decision-making
description: Make sound decisions under uncertainty using frameworks like RICE, weighted matrix, decision trees, and pre-mortems.
domain: mindset
tags:
- decision
- making
- mindset
- personal-development
- soft-skills
---

# Decision Making

Framework for making effective decisions: frameworks (RICE, weighted matrix), decision trees, pre-mortems, and avoiding common biases.

## When to Use

- Prioritizing features, projects, or investments
- Choosing between multiple options with trade-offs
- High-stakes decisions under uncertainty
- Team decisions where alignment is needed
- **When NOT to use**: Routine low-stakes choices (use heuristics), or emergencies requiring instant action

## Decision Frameworks

### 1. RICE (Prioritization)

| Metric | Question | Scale |
|--------|----------|-------|
| **Reach** | How many people are affected? | 1-5 |
| **Impact** | How much does each person benefit? | 0.25, 0.5, 1, 2, 3 |
| **Confidence** | How sure are we of estimates? | 0.2, 0.5, 0.8, 1 |
| **Effort** | How much work does it take? | Person-months |

**Score**: `(Reach × Impact × Confidence) / Effort`

**Example**:
- Feature A: Reach 3, Impact 2, Confidence 0.8, Effort 2 → `(3×2×0.8)/2 = 2.4`
- Feature B: Reach 4, Impact 1, Confidence 0.5, Effort 1 → `(4×1×0.5)/1 = 2.0`
- **Pick Feature A** (higher score)

---

### 2. Weighted Decision Matrix

**Structure**: Criteria × Weight × Score

| Criteria | Weight (%) | Option A | Option B | Option C |
|----------|-----------|----------|----------|----------|
| Revenue potential | 30% | 8 (2.4) | 6 (1.8) | 7 (2.1) |
| Feasibility | 25% | 6 (1.5) | 8 (2.0) | 5 (1.25) |
| Time to market | 20% | 7 (1.4) | 5 (1.0) | 8 (1.6) |
| Strategic alignment | 25% | 9 (2.25) | 7 (1.75) | 6 (1.5) |
| **Total** | 100% | **7.55** | **6.55** | **6.45** |

**Pick**: Option A (highest weighted score).

---

### 3. Pre-Mortem

**Method**: Before making a decision, assume it failed badly. Then ask: "What went wrong?"

**How**:
1. Gather the team
2. "It's 12 months from now. Our decision was a disaster. What happened?"
3. List all failure modes
4. For each: "How likely? How severe? Can we prevent it?"

**Value**: Surfaces hidden risks. Breaks groupthink.

---

### 4. Decision Trees

**Structure**: Each branch = a decision or outcome. Each terminal node = a payoff.

**Simplified**:
```
                    ┌─ Good market (50%) → $10M profit
Launch? ─── Yes ───┼─ Medium market (30%) → $2M profit
                    └─ Bad market (20%) → -$3M loss
                    
          No → $0 (no change)
```

**Expected value (EV)** = `(0.5 × 10) + (0.3 × 2) + (0.2 × -3) = $5.6M`

**Decision**: If EV > cost to launch, do it.

---

### 5. "Reverse" or "Invert"

**Method**: Instead of asking "How can we succeed?", ask "How can we fail?" then prevent those.

---

### 6. Six Thinking Hats (De Bono)

| Hat | Focus | Questions |
|-----|-------|-----------|
| **White** | Facts, data, information | "What do we know? What's missing?" |
| **Red** | Emotions, intuition, gut | "How do I feel about this?" |
| **Black** | Risks, caution, problems | "What could go wrong?" |
| **Yellow** | Optimism, benefits, value | "What's the best case?" |
| **Green** | Creativity, new ideas | "What alternatives exist?" |
| **Blue** | Process, meta-thinking | "What's the decision process?" |

**Use**: Cycle through hats as a team to ensure all perspectives.

---

## Common Biases in Decisions

| Bias | Effect on Decision | Mitigation |
|------|-------------------|------------|
| **Optimism bias** | Underestimate risks, overestimate success | Pre-mortem; base rates |
| **Status quo bias** | Prefer current state, even if worse | Ask: "What would I do if starting fresh?" |
| **Overconfidence** | Overestimate own knowledge/ability | Seek disconfirming evidence |
| **Sunk cost** | Continue because of past investment | Ask: "Ignore past. Would I start this now?" |
| **Groupthink** | Team agrees too quickly | Appoint a devil's advocate |

---

## Delegating Decisions

| Decision Type | Who Decides |
|---------------|-------------|
| **Low stakes, reversible** | Delegate (or decide fast) |
| **Medium stakes** | Use framework (RICE, matrix) |
| **High stakes, irreversible** | Involve stakeholders, deliberate |

---

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "Analysis paralysis" (used to avoid deciding) | Pick a framework and use it as a forcing function |
| "My gut is usually right" | Gut works for familiar patterns. For novel situations, use frameworks. |
| "We don't have data" | Estimate. Use confidence scores. Better than guessing. |
| "We can decide later" | Procrastination is a decision (usually the wrong one). |

## Red Flags

- You can't name which framework you're using
- You keep adding options without removing any (no pruning)
- You keep delaying the decision
- Everyone in the room agrees too quickly (groupthink)
- You only consider one option (false dichotomy)

## Verification

- [ ] Decision framework selected (RICE, weighted matrix, decision tree, etc.)
- [ ] Criteria weighted by importance (if using weighted matrix)
- [ ] Pre-mortem conducted (assumed failure, listed causes, prevented each)
- [ ] Biases considered (optimism, status quo, sunk cost, overconfidence)
- [ ] Options pruned (not comparing >5 options without filtering)
- [ ] Decision delegated if low-stakes or reversible

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
