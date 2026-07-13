---
name: doc-templates
version: 1.0.0
severity: recommended
scope: [docs, research, planning]
pairs-with: [surpass]
description: Canonical documentation templates — feature matrix, gap analysis, competitor files, decision logs, QA reports, sprint notes
---

# §DOC-GEN — Document Generation Spec

These are the canonical file templates. Generate them on first run, update them on every run.
On subsequent sessions: read existing docs first, then update in-place (append new sections,
fill in 🔍 cells, close gaps). Never overwrite existing data unless explicitly correcting an error.

### File tree to maintain

```
docs/
├── research/
│   ├── FEATURE_MATRIX.md       ← master comparison table
│   ├── GAP_ANALYSIS.md         ← prioritized gap registry
│   └── competitors/
│       └── [name].md           ← one file per competitor
├── decisions/
│   └── [feature-name].md       ← one file per technical decision
├── exploration/
│   └── CODEBASE_AUDIT.md       ← living audit document
├── qa/
│   └── QA_REPORT_[feature].md  ← one file per feature QA cycle
└── sprints/
    └── SPRINT_[N].md           ← one file per sprint
```

### FEATURE_MATRIX.md — canonical template

```markdown
# Feature Matrix
> Platform: [Name] | Industry: [Vertical] | Updated: [Date]

## Legend
✅ Done | 🚧 Partial | ❌ Missing | ⭐ Best-in-class | 🔍 Unknown

## Competitor Registry
| ID | Name | URL | Type |
|----|------|-----|------|
| C1 | | | direct |
| C2 | | | direct |
| C3 | | | indirect |

## Core Features
| Feature | Ours | C1 | C2 | C3 | Priority |
|---------|:----:|:--:|:--:|:--:|----------|
| | | | | | P0/P1/P2/— |

## Performance
| Metric | Ours | C1 | C2 | C3 |
|--------|:----:|:--:|:--:|:--:|
| p95 Latency | 🔍 | 🔍 | 🔍 | 🔍 |
| Uptime SLA | 🔍 | 🔍 | 🔍 | 🔍 |
| Mobile UX | 🔍 | 🔍 | 🔍 | 🔍 |
| API available | 🔍 | 🔍 | 🔍 | 🔍 |

## UX & Onboarding
| Dimension | Ours | C1 | C2 | C3 |
|-----------|:----:|:--:|:--:|:--:|
| Time to first value | 🔍 | 🔍 | 🔍 | 🔍 |
| Setup steps | 🔍 | 🔍 | 🔍 | 🔍 |
| Documentation quality | 🔍 | 🔍 | 🔍 | 🔍 |
| Support channels | 🔍 | 🔍 | 🔍 | 🔍 |

## Pricing
| Tier | Ours | C1 | C2 | C3 |
|------|:----:|:--:|:--:|:--:|
| Free | 🚫 | | | |
| Starter | 🚫 | | | |
| Pro | 🚫 | | | |
| Enterprise | 🚫 | | | |
| Per-seat/payg | 🚫 | | | |

## Integrations
Mention key platform/API integrations.

## Key Differentiators
What's unique about each competitor? What's our wedge?
```

### GAP_ANALYSIS.md — canonical template

```markdown
# Gap Analysis
> Platform: [Name] | Updated: [Date]

## Open Gaps
| ID | Feature | Priority | Effort | Impact | Status |
|----|---------|----------|--------|--------|--------|
| G1 | | P0/P1 | S/M/L/XL | H/M/L | open/closed/in-progress |
```

### Competitor files — canonical template

```markdown
# [Competitor Name]
**URL:** [link] | **Type:** direct/indirect

## Overview
What do they do? Who are they for? Why do users pick them over us?

## Strengths
- ...
- ...

## Weaknesses
- ...
- ...

## Our Advantage
What can we do that they can't?
```

### Decision files — canonical template

```markdown
# Decision: [Title]
**Date:** YYYY-MM-DD

## Context
What problem needed a decision? What were the constraints?

## Options Considered
| Option | Pros | Cons |
|--------|------|------|
| A | ... | ... |
| B | ... | ... |

## Decision
**Chosen:** Option A
**Rationale:** [Why this one over others?]

## Consequences
What tradeoffs did we accept? What follow-ups are needed?
```

### QA Report — canonical template

```markdown
# QA Report: [Feature Name]
**Date:** YYYY-MM-DD | **Tester:** [Name]

## Summary
**Pass:** N/N | **Fail:** N | **Blocked:** N

## Test Cases
| ID | Scenario | Precondition | Steps | Expected | Actual | Verdict |
|----|----------|-------------|-------|----------|--------|---------|
| TC1 | | | | | | PASS/FAIL |
| TC2 | | | | | | PASS/FAIL |

## Issues Found
| ID | Severity | Description | Status |
|----|----------|-------------|--------|
| | HIGH/MED/LOW | | open/fixed |

## Verdict
PASS / CONDITIONAL PASS / FAIL
```

### Sprint file — canonical template

```markdown
# Sprint N
> [Date Range]

## Goal
What must be true at the end of this sprint?

## Commitments
- [ ] Feature A — owner
- [ ] Feature B — owner
- [ ] Bug fixes — owner

## Results
- Done: [list]
- Not done: [list with reasons]
- Trackers opened: [count]
- Trackers closed: [count]

## Retro
- What went well:
- What to improve:
- Actions:
```
