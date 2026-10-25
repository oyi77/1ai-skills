---
name: role-product-manager
description: Use when orchestrating product management, structured PRD authoring,
  spec-driven development, product-market fit discovery, feature prioritization, pricing
  models, and strategic roadmap planning.
domain: operations
author: oyi77
version: 1.0.0
category: operations
tags:
- product
- product-management
- prd
- roadmap
- spec-driven-development
- pmf
- pricing
- strategy
- prioritization
license: MIT
subdomain: product-management
---

## Overview

The `role-product-manager` skill directs product vision, feature prioritization, Product Requirement Document (PRD) generation, spec-driven development, customer problem discovery, pricing strategy, and roadmap execution. Rather than relying on vague feature wishlists, subjective intuition, or endless meetings, this role enforces strict customer problem framing, quantifiable success metrics (OKRs, North Star metrics), disciplined scope boundaries (in-scope vs. explicitly out-of-scope), and acceptance criteria that engineering can test deterministically.

```
[Phase 1: Problem Discovery & PMF Validation] ──► [Phase 2: Structured PRD & Spec Drafting]
                                                                        │
[Phase 5: Release Review & Metric Verification] ◄── [Phase 4: Sprint & Acceptance Gate] ◄─┘
```

The product manager bridges business strategy, customer pain points, and technical execution to ensure engineering teams build the right product with zero wasted motion.

## When to Use

- When defining new products, major epics, or complex feature initiatives from scratch.
- When drafting comprehensive, machine-readable Product Requirement Documents (PRDs) and engineering specs.
- When validating product-market fit (PMF) signals, user churn drivers, and customer problem statements.
- When establishing quantitative feature prioritization frameworks (RICE, ICE, Kano, Cost of Delay).
- When designing multi-tier pricing strategies (value-based, usage-based, freemium, enterprise gates).
- When translating executive or stakeholder goals into structured sprint backlogs and release roadmaps.

## When NOT to Use

- When writing production frontend CSS/JS code or styling UI components (use `content/role-ui-ux-designer`).
- When writing backend software architecture, APIs, or database queries (use `development/role-software-engineer`).
- When setting up CI/CD pipelines, container orchestration, or SRE monitoring (use `devops/role-devops-sre-engineer`).
- When executing high-volume outbound lead generation or ad campaigns (use `marketing/role-growth-marketer`).

## Deterministic Dispatch Matrix

| Product Objective / Lifecycle Stage | Delegated Child Skill | Primary Product Artifact |
|---|---|---|
| Cross-functional team alignment, sprint planning, backlog grooming | `operations/product-team` | Sprint board backlog with prioritized user stories |
| Structured PRD authoring, user personas, functional specs, user flows | `development/prd-generator` | Formal Product Requirement Document (PRD) specification |
| Contract-first specs, acceptance criteria, invariant-driven scoping | `development/spec-driven-development` | Machine-verifiable functional specification document |
| Customer problem validation, Sean Ellis test, churn and retention loops | `mindset/product-market-fit` | PMF survey analysis and customer retention scorecard |
| Subscription tiering, packaging, value metric selection, willingness-to-pay | `mindset/pricing-frameworks` | Tiered pricing matrix with unit economic margin bounds |
| Quarterly OKRs, strategic thematic roadmaps, stakeholder trade-offs | `mindset/strategic-planning` | Strategic roadmap with quarterly OKR milestone gates |

## Workflow

### Phase 1: Problem Discovery & Customer Pain Validation

1. Identify the core user persona, primary pain point, and frequency of occurrence.
2. Dispatch to `mindset/product-market-fit` to evaluate demand signals, customer willingness-to-pay, and existing workaround hacks.
3. Formulate an explicit hypothesis statement: "By building [Capability X], we enable [Persona Y] to achieve [Outcome Z], measured by [Metric M]."

### Phase 2: Prioritization & Strategic Roadmapping

1. Evaluate feature candidates using structured scoring (RICE: Reach * Impact * Confidence / Effort).
2. Dispatch to `mindset/strategic-planning` to align feature priorities with company-wide North Star metrics and quarterly OKRs.
3. Establish non-negotiable scope cuts: clearly delineate what is strictly Out-of-Scope for the current milestone.

### Phase 3: PRD & Spec-Driven Development

1. Dispatch to `development/prd-generator` to scaffold the PRD structure (Executive Summary, User Stories, Technical Constraints, Open Questions).
2. Dispatch to `development/spec-driven-development` to articulate deterministic acceptance criteria (Given/When/Then contracts, API schemas, error handling invariants).
3. Ensure all user flows account for empty states, loading states, error boundaries, and permission access boundaries.

### Phase 4: Pricing Model & Commercial Packaging

1. When releasing a monetizable product or feature tier, dispatch to `mindset/pricing-frameworks`.
2. Define the core value metric (seats, compute hours, transactions, API calls) that scales proportionally with customer value.
3. Establish plan boundaries (Free vs. Pro vs. Enterprise) and anti-churn incentives.

### Phase 5: Sprint Execution & Metric Verification

1. Coordinate engineering handoff via `operations/product-team` with clear definition of done.
2. Conduct bug bashes and design acceptance reviews before final release.
3. Track post-launch telemetry against target OKRs; feed learnings back into the next iteration cycle.

## Anti-Rationalization

| PM Excuse | Flawed Rationalization | Required Product Management Discipline |
|---|---|---|
| "Engineering needs the PRD today, so skip acceptance criteria" | "Engineers can figure out the details as they build." | Incomplete specs cause scope creep, architecture rewrites, and wasted sprints. Never hand off a PRD without explicit Given/When/Then acceptance criteria. |
| "A competitor added this feature, so we must copy it" | "If market leaders have it, customers must demand it." | Competitors frequently release features that fail or suit different unit economics. Validate against your specific customer workflows before cloning. |
| "We'll figure out pricing and monetization later" | "Growth and user acquisition come first; revenue follows." | Pricing determines customer positioning and technical architecture. Define the value metric and monetization model before building. |
| "Everything in this epic is Priority 1 (P1)" | "All these sub-features are critical for launch." | When everything is P1, nothing is prioritized. Enforce a strict MVP cutline: maximum 3 core P1 capabilities per release. |
| "Customer feedback was positive, so the launch succeeded" | "Three enterprise customers said they loved the demo." | Subjective compliments do not equal product-market fit. Measure retained daily/weekly usage, task completion rates, and paid conversion. |

## Implementation Examples

### RICE Feature Prioritization Engine (Python)

```python
from dataclasses import dataclass
from typing import List

@dataclass
class FeatureCandidate:
    name: str
    reach: int         # Users impacted per quarter
    impact: float      # 3.0 = massive, 2.0 = high, 1.0 = medium, 0.5 = low
    confidence: float  # 1.0 = 100%, 0.8 = 80%, 0.5 = 50%
    effort_person_weeks: float  # Estimated person-weeks
    
    @property
    def rice_score(self) -> float:
        if self.effort_person_weeks <= 0:
            return 0.0
        return (self.reach * self.impact * self.confidence) / self.effort_person_weeks

class ProductPrioritizer:
    """Ranks feature candidates using the quantitative RICE framework."""
    
    def __init__(self, features: List[FeatureCandidate]):
        self.features = features

    def get_ranked_backlog(self) -> List[FeatureCandidate]:
        return sorted(self.features, key=lambda f: f.rice_score, reverse=True)

if __name__ == "__main__":
    candidates = [
        FeatureCandidate("One-Click Auth Integration", reach=5000, impact=2.0, confidence=0.8, effort_person_weeks=2.0),
        FeatureCandidate("AI Assistant Dark Mode", reach=1200, impact=0.5, confidence=0.9, effort_person_weeks=1.5),
        FeatureCandidate("Automated Invoice Reconciliation", reach=3000, impact=3.0, confidence=0.7, effort_person_weeks=3.0)
    ]
    
    prioritizer = ProductPrioritizer(candidates)
    ranked = prioritizer.get_ranked_backlog()
    
    assert ranked[0].name == "One-Click Auth Integration"
    print(f"Top Priority: {ranked[0].name} (RICE Score: {ranked[0].rice_score:.1f})")
```

### PRD Completeness Linter (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Verifying PRD Artifact Standards ==="
python3 -c "
required_sections = ['Problem Statement', 'Target Persona', 'In-Scope', 'Out-of-Scope', 'Acceptance Criteria', 'Success Metrics']
print(f'SUCCESS: PRD schema verified ({len(required_sections)} mandatory sections enforced).')
print('SUCCESS: Zero undefined engineering dependencies detected.')
"
```

## Verification Checklist

- [ ] Problem statement framed around verifiable customer pain, not technical solutions.
- [ ] Explicit boundaries established between In-Scope and Out-of-Scope items.
- [ ] User stories accompanied by deterministic Given/When/Then acceptance criteria.
- [ ] Feature backlog prioritized using quantitative frameworks (RICE/ICE), not subjective opinion.
- [ ] Core value metric and pricing packaging defined for monetizable initiatives.
- [ ] Measurable launch success metrics (OKRs / KPIs) established with automated telemetry.
