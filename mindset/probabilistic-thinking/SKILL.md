---
name: probabilistic-thinking
description: Apply Bayesian updating, base rates, and expected value to decision-making. Use when reasoning under uncertainty
  or evaluating risks.
domain: mindset
tags:
- mindset
- personal-development
- probabilistic
- soft-skills
- thinking
---

# Probabilistic Thinking

Reasoning with probabilities instead of binary certainty. Covers Bayesian updating, base rates, calibration, and expected value.

## When to Use

- Evaluating risks or forecasting outcomes
- Updating beliefs based on new evidence
- Making decisions with incomplete information
- Assessing trade-offs with uncertain payoffs
- **When NOT to use**: Decisions with known outcomes, moral absolutes, or when probabilities are unknowable

## Core Concepts

### Bayes' Theorem

**Formula**: `P(H|E) = P(E|H) × P(H) / P(E)`

**In words**: Update your belief (hypothesis H) based on new evidence (E).

**Example** (Medical test):
- **Prior**: 1% of population has disease (P(H) = 0.01)
- **Evidence**: Test is 90% accurate (P(E|H) = 0.9, false positive rate = 10%)
- **Question**: You test positive. What's the probability you have the disease?

**Calculation**:
- P(E) = (0.9 × 0.01) + (0.1 × 0.99) = 0.108
- P(H|E) = (0.9 × 0.01) / 0.108 = **8.3%**

**Insight**: Even with a positive test, you likely don't have the disease (base rate is low).

### Base Rates

**Principle**: Start with the baseline probability before considering specific evidence.

**Example**:
- "This startup will unicorn" → Base rate: <1% of startups become unicorns. Strong evidence needed to overcome this prior.
- "This candidate will succeed" → Base rate: What % of past hires in this role succeeded? Start there.

**Common mistake**: Ignoring base rates and over-weighting anecdotal evidence.

### Expected Value (EV)

**Formula**: `EV = Σ (Probability × Payoff)`

**Example** (Investment decision):
- 60% chance of +$100K
- 30% chance of $0
- 10% chance of -$50K
- **EV** = (0.6 × 100) + (0.3 × 0) + (0.1 × -50) = **$55K**

**Decision rule**: Take actions with positive EV, even if individual outcomes vary.

### Calibration

**Definition**: How well your confidence matches reality.

**Exercise**:
1. Make 100 predictions with confidence levels (e.g., "70% confident X happens")
2. Track outcomes
3. **Well-calibrated**: 70% of your "70% confident" predictions came true

**Common bias**: Overconfidence (you say 90%, but only 60% come true).

## Probability Fallacies

| Fallacy | Description | Example |
|---------|-------------|---------|
| **Gambler's Fallacy** | Believing past outcomes affect independent future events | "I flipped heads 5x, next must be tails" (still 50/50) |
| **Base Rate Neglect** | Ignoring baseline probability | "This person fits the profile of a terrorist" (ignoring 99.99% aren't) |
| **Conjunction Fallacy** | Thinking specific scenarios are more likely than general ones | Linda is a bank teller AND feminist > Linda is a bank teller (impossible) |
| **Availability Heuristic** | Overweighting recent/vivid events | Plane crashes are rare but feel common because they're memorable |

## Worked Example: Hiring Decision

**Scenario**: Candidate aced the interview. Should you hire?

**Base rate**: 40% of hires in this role succeed (P(H) = 0.4)

**Evidence**: Interview score 9/10. Historically, 80% of successful hires scored 9+, but 30% of failed hires also scored 9+ (false positives).

**Bayesian update**:
- P(E|H) = 0.8 (score 9+ given success)
- P(E|¬H) = 0.3 (score 9+ given failure)
- P(E) = (0.8 × 0.4) + (0.3 × 0.6) = 0.50

**P(H|E)** = (0.8 × 0.4) / 0.50 = **64%**

**Conclusion**: Positive signal (64% > 40% base rate), but far from certain. Look for more evidence (work sample, references).

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "I'm 100% sure" | Almost nothing is 100%. Overconfidence kills calibration. |
| "This time it's different" | Maybe, but base rates are a strong prior. Need exceptional evidence. |
| "Probabilities don't apply here" | Every uncertain outcome has a probability, even if hard to quantify. |
| "Expected value is just a number" | EV is the decision rule for rational long-term outcomes. |

## Red Flags

- You express certainty ("definitely", "impossible") about uncertain events
- You ignore base rates when evaluating evidence
- You confuse probability with outcome (70% doesn't mean "will happen")
- You cherry-pick evidence and don't update beliefs
- You make decisions based on single outcomes instead of expected value

## Verification

- [ ] Base rate identified (what's the prior probability?)
- [ ] Evidence evaluated (how strong is this signal?)
- [ ] Belief updated using Bayes' theorem or intuition (posterior probability)
- [ ] Expected value calculated (if decision involves payoffs)
- [ ] Calibrated (confidence matches reality over time)
- [ ] Fallacies avoided (gambler's fallacy, base rate neglect, etc.)

## Overview

> Section content — see SKILL.md body for full details.
