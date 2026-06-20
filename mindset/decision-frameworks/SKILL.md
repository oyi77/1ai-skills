---
name: decision-frameworks
description: Apply structured decision frameworks like RICE, ICE, weighted scoring, and pre-mortem analysis. Use when prioritizing
  features, evaluating options, or making high-stakes decisions.
domain: mindset
tags:
- decision
- frameworks
- mindset
- personal-development
- soft-skills
---

# Decision Frameworks

Structured models for prioritization and decision-making. Covers RICE, ICE, weighted scoring, pre-mortem, and second-order thinking.

## When to Use

- Prioritizing roadmap features or initiatives
- Choosing between competing options (vendors, strategies, hires)
- Making high-stakes decisions with multiple stakeholders
- Reducing bias and increasing rigor in decision processes
- **When NOT to use**: Trivial decisions, emergencies requiring immediate action, or decisions with only one viable option

## Frameworks

### 1. RICE (Reach × Impact × Confidence / Effort)

**Best for**: Product prioritization, feature roadmaps

**Formula**: `RICE Score = (Reach × Impact × Confidence) / Effort`

| Factor | Definition | Scale |
|--------|------------|-------|
| **Reach** | How many people affected (per quarter)? | # of users/customers |
| **Impact** | How much will it improve their experience? | 0.25 (minimal) to 3 (massive) |
| **Confidence** | How certain are you? | 0-100% |
| **Effort** | How much work (person-months)? | # of person-months |

**Example**:
- Feature A: (1000 users × 1.5 impact × 80% confidence) / 2 months = **600 RICE score**
- Feature B: (500 users × 3 impact × 50% confidence) / 1 month = **750 RICE score**
- **Conclusion**: Prioritize Feature B (higher RICE score)

### 2. ICE (Impact × Confidence × Ease)

**Best for**: Quick prioritization when effort estimates are rough

**Formula**: `ICE Score = Impact × Confidence × Ease` (all scored 1-10)

**Example**:
- Idea A: 8 impact × 7 confidence × 3 ease = **168**
- Idea B: 6 impact × 9 confidence × 8 ease = **432**
- **Conclusion**: Prioritize Idea B

### 3. Weighted Scoring Matrix

**Best for**: Multi-criteria decisions (vendor selection, hiring, strategy)

**Process**:
1. List criteria (cost, speed, quality, risk, etc.)
2. Weight each criterion by importance (sum to 100%)
3. Score each option on each criterion (1-10)
4. Multiply score × weight, sum for total

**Example** (Vendor selection):

| Criterion | Weight | Vendor A Score | Vendor A Weighted | Vendor B Score | Vendor B Weighted |
|-----------|--------|----------------|-------------------|----------------|-------------------|
| Cost | 30% | 6 | 1.8 | 8 | 2.4 |
| Quality | 40% | 9 | 3.6 | 7 | 2.8 |
| Speed | 20% | 7 | 1.4 | 8 | 1.6 |
| Support | 10% | 6 | 0.6 | 9 | 0.9 |
| **Total** | | | **7.4** | | **7.7** |

**Conclusion**: Vendor B wins (7.7 > 7.4)

### 4. Pre-Mortem Analysis

**Best for**: Reducing overconfidence, identifying risks before committing

**Process**:
1. Assume the decision failed catastrophically
2. Each person writes down why it failed (5 min)
3. Share reasons (consolidate themes)
4. Mitigate top 3 risks or adjust decision

**Example**:
- Decision: Launch new product in 3 months
- Pre-mortem: "We failed because..."
  - Engineers underestimated complexity (add 25% buffer)
  - No marketing plan (assign owner now)
  -依赖外部API宕机 (build fallback)

### 5. Second-Order Thinking

**Best for**: Avoiding unintended consequences

**Process**: Ask "And then what?" after every decision.

**Example**:
- **First-order**: Cut prices → more customers
- **Second-order**: More customers → overload support → churn increases → reputation damage
- **Third-order**: Reputation damage → harder to raise prices later → margin squeeze

## When to Use Each Framework

| Framework | Best For | Avoid When |
|-----------|----------|------------|
| **RICE** | Product roadmap prioritization | Effort hard to estimate |
| **ICE** | Quick gut-check prioritization | High-stakes, need rigor |
| **Weighted scoring** | Multi-stakeholder, multi-criteria decisions | Criteria unclear or contentious |
| **Pre-mortem** | High-risk, high-confidence decisions | Low-stakes, trivial decisions |
| **Second-order thinking** | Strategy, policy, systems changes | Immediate tactical decisions |

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "I'll just go with my gut" | Gut is biased. Frameworks reduce bias and force explicit trade-offs. |
| "This takes too long" | 30 minutes of structured thinking saves weeks of wrong direction. |
| "We already know the answer" | If true, frameworks validate quickly. If false, they catch blind spots. |
| "Too many frameworks" | Pick one. RICE for product, weighted scoring for multi-criteria. |

## Red Flags

- You skip the framework and retrofit justification after deciding
- You game the scoring to favor your preferred option
- You don't involve stakeholders in weighting criteria
- You ignore the framework's recommendation without articulating why
- You use a framework for every trivial decision (analysis paralysis)

## Verification

- [ ] Framework selected matches decision type (RICE for roadmap, weighted for multi-criteria, etc.)
- [ ] Scoring done independently (not influenced by preferred outcome)
- [ ] Stakeholders aligned on criteria and weights (if applicable)
- [ ] Sensitivity tested (what if key assumptions change?)
- [ ] Top risks identified via pre-mortem (for high-stakes decisions)
- [ ] Decision documented with rationale (not just score)

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
