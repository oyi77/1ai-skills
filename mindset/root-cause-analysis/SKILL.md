---
name: root-cause-analysis
description: Diagnose root causes using 5 Whys, fishbone diagrams, fault trees, and Pareto analysis. Use when troubleshooting
  recurring problems or post-incident analysis.
domain: mindset
tags:
- cause
- mindset
- personal-development
- root
- soft-skills
---

# Root Cause Analysis

Systematic methods for finding the root cause of problems, not just symptoms. Covers 5 Whys, fishbone (Ishikawa) diagrams, fault tree analysis, and Pareto analysis.

## When to Use

- Post-incident or post-mortem analysis
- Troubleshooting recurring problems
- Quality issues or defects
- Process improvement initiatives
- **When NOT to use**: Emergencies requiring immediate fixes (fix first, analyze later), or when root cause is obvious

## Methods

### 1. 5 Whys

**Process**: Ask "Why?" 5 times to drill from symptom to root cause.

**Example** (Website down):
1. **Why is the website down?** Server crashed.
2. **Why did the server crash?** Out of memory.
3. **Why did it run out of memory?** Memory leak in the app.
4. **Why is there a memory leak?** No automated tests for long-running processes.
5. **Why no tests?** Testing wasn't prioritized in sprint planning.

**Root cause**: Testing not prioritized → **Fix**: Add testing to definition of done.

**Trap**: Stopping too early ("server crashed" is not the root cause).

### 2. Fishbone Diagram (Ishikawa)

**Purpose**: Categorize potential causes into buckets (6 Ms: Man, Machine, Method, Material, Measurement, Mother Nature).

**Process**:
1. Draw problem on the right (fish head)
2. Draw main branches (categories: People, Process, Technology, etc.)
3. Brainstorm causes under each category
4. Identify root cause

**Example** (High customer churn):
```
People          Process           Technology
  |               |                  |
  - Poor training - No onboarding   - Buggy product
  - High turnover - Slow support    - Poor UX
       \            \               /
        \            \             /
         \            \           /
          ───────────[High Churn]
```

**Root cause**: No onboarding process (new users don't understand product value).

### 3. Fault Tree Analysis (FTA)

**Purpose**: Work backward from failure to identify contributing factors (logical AND/OR gates).

**Process**:
1. Start with top event (failure)
2. Identify immediate causes (AND/OR logic)
3. Recurse until you reach root causes

**Example** (Deployment failure):
```
Deployment fails
     ├─ (OR)
     ├─ Tests fail
     │   ├─ (AND)
     │   ├─ Code has bug
     │   └─ Tests don't catch bug
     └─ Deploy script breaks
         ├─ (AND)
         ├─ Script has error
         └─ No CI validation
```

**Root causes**: Tests don't catch bug + No CI validation of deploy scripts.

### 4. Pareto Analysis (80/20 Rule)

**Purpose**: Focus on the 20% of causes that drive 80% of problems.

**Process**:
1. List all causes with frequency/impact
2. Sort by frequency
3. Calculate cumulative %
4. Focus on top causes (80% threshold)

**Example** (Support tickets):
| Cause | Count | Cumulative % |
|-------|-------|--------------|
| Login issues | 50 | 50% |
| Billing errors | 30 | 80% |
| UX confusion | 15 | 95% |
| Other | 5 | 100% |

**Conclusion**: Fix login + billing (80% of tickets).

## When to Use Each Method

| Method | Best For | Avoid When |
|--------|----------|------------|
| **5 Whys** | Simple, linear problems | Complex, multi-cause issues |
| **Fishbone** | Brainstorming multiple causes | Single obvious root cause |
| **Fault Tree** | Logical AND/OR dependencies | Simple linear problems |
| **Pareto** | Prioritizing causes by impact | All causes are equally important |

## Common Traps

| Trap | Description | Fix |
|------|-------------|-----|
| **Stopping at symptoms** | "Server crashed" (not root cause) | Keep asking "Why?" |
| **Blame game** | "John made a mistake" | Focus on systems, not people |
| **Single cause bias** | Assuming one root cause | Look for multiple contributing factors |
| **Confirmation bias** | Only investigating likely causes | Brainstorm widely first |

## Example: Post-Mortem (Production Outage)

**Incident**: API down for 2 hours, $50K revenue lost.

**5 Whys**:
1. Why down? Database connection pool exhausted.
2. Why exhausted? Too many slow queries.
3. Why slow? Missing index on `user_id`.
4. Why missing? Schema change didn't update indexes.
5. Why not caught? No automated migration review.

**Root cause**: No automated migration review process.

**Fix**:
- Immediate: Add missing index
- Short-term: Review all migrations for missing indexes
- Long-term: Add CI check for index coverage

**Pareto**:
- Slow queries: 80% of latency issues
- Missing indexes: 60% of slow queries
- **Focus**: Automated index analysis in CI

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "We know the root cause" | Intuition is often wrong. Use structured methods. |
| "This is a one-off" | If it happened once, it can happen again. Find the root cause. |
| "We don't have time" | Skipping RCA means the problem recurs. Pay now or pay later (more). |
| "It's user error" | User error is a symptom. Root cause is poor UX or training. |

## Red Flags

- You blame people instead of systems
- You stop at the first "Why" (surface cause)
- You don't document the analysis (lessons lost)
- You identify root cause but don't implement fixes
- The same problem recurs (RCA was incomplete)

## Verification

- [ ] Method selected (5 Whys, fishbone, fault tree, Pareto)
- [ ] Root cause(s) identified (not just symptoms)
- [ ] Contributing factors documented (people, process, technology)
- [ ] Fixes defined (immediate, short-term, long-term)
- [ ] Follow-up plan set (verify fixes prevent recurrence)
- [ ] Lessons documented (post-mortem, wiki, etc.)

## Overview

> Section content — see SKILL.md body for full details.
