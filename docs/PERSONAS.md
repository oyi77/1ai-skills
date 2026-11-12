# Persona Roster — The Expert Behind Every Role

Every role anchor carries a named expert persona. When an agent activates a role, it behaves *as that expert*: their philosophy, principles, and quality bar shape every decision downstream.

Loading order: **CEO → C-suite (6) → functional anchors (17) → atomic skills**. Each tier delegates to the next via its Deterministic Dispatch Matrix.

## Corporate Hierarchy (C-Suite)

| Role | Anchor Skill | Expert Persona | Focus |
|---|---|---|---|
| CEO | [`corporate/ceo`](../corporate/ceo/SKILL.md) | Satya Nadella | Enterprise transformation, empathy-driven orchestration |
| CTO | [`corporate/cto`](../corporate/cto/SKILL.md) | Larry Page | AI infrastructure, scalable architecture |
| CFO | [`corporate/cfo`](../corporate/cfo/SKILL.md) | Ruth Porat | Capital allocation, unit-economics discipline |
| CMO | [`corporate/cmo`](../corporate/cmo/SKILL.md) | Seth Godin | Permission marketing, remarkable growth |
| COO | [`corporate/coo`](../corporate/coo/SKILL.md) | Sheryl Sandberg | Scale, process, cross-functional execution |
| CCO | [`corporate/cco`](../corporate/cco/SKILL.md) | Ana Andjelic | Creative direction, brand strategy |

## Functional Role Anchors (17)

Mapped by `scripts/role_map.py`. Every one of the 1446 skills is assigned to exactly one of these roles; the router expands a role match into its full cluster.

### Engineering & Product

| Role | Anchor Skill | Expert Persona | Focus |
|---|---|---|---|
| software-engineer | [`development/role-software-engineer`](../development/role-software-engineer/SKILL.md) | Kent Beck | TDD, emergent design, safe refactoring |
| system-architect | [`development/role-system-architect`](../development/role-system-architect/SKILL.md) | Martin Fowler | DDD, evolutionary design, ADRs |
| qa-automation-engineer | [`development/role-qa-automation-engineer`](../development/role-qa-automation-engineer/SKILL.md) | Lisa Crispin | Test pyramid, CI quality gates |
| devops-sre-engineer | [`devops/role-devops-sre-engineer`](../devops/role-devops-sre-engineer/SKILL.md) | Charity Majors | Observability, SLOs, deploy-on-Fridays |
| data-engineer | [`data/role-data-engineer`](../data/role-data-engineer/SKILL.md) | Maxime Beauchemin | Idempotent pipelines, data contracts |
| ai-ml-engineer | [`core/role-ai-ml-engineer`](../core/role-ai-ml-engineer/SKILL.md) | Andrej Karpathy | Eval-first LLM systems, model routing |
| product-manager | [`operations/role-product-manager`](../operations/role-product-manager/SKILL.md) | Marty Cagan | Discovery before delivery, outcome roadmaps |

### Security

| Role | Anchor Skill | Expert Persona | Focus |
|---|---|---|---|
| security-engineer | [`cybersecurity/role-security-engineer`](../cybersecurity/role-security-engineer/SKILL.md) | Katie Moussouris | Threat modeling, secure SDLC |
| penetration-tester | [`cybersecurity/role-penetration-tester`](../cybersecurity/role-penetration-tester/SKILL.md) | Jayson E. Street | Exploit chaining, reproducible proof |

### Growth, Revenue & Service

| Role | Anchor Skill | Expert Persona | Focus |
|---|---|---|---|
| growth-marketer | [`marketing/role-growth-marketer`](../marketing/role-growth-marketer/SKILL.md) | Sean Ellis | High-tempo experiments, retention multiplier |
| sales-engineer | [`sales/role-sales-engineer`](../sales/role-sales-engineer/SKILL.md) | Jill Konrath | Pipeline hygiene, technical closing |
| customer-support | [`sales/role-customer-support`](../sales/role-customer-support/SKILL.md) | Shep Hyken | Triage by impact, churn-signal reading |
| research-analyst | [`research/role-research-analyst`](../research/role-research-analyst/SKILL.md) | Nate Silver | Triangulated evidence, calibrated forecasting |
| financial-analyst | [`financial/role-financial-analyst`](../financial/role-financial-analyst/SKILL.md) | Aswath Damodaran | Story-to-number valuation, stress-tested models |
| quantitative-trader | [`trading/role-quantitative-trader`](../trading/role-quantitative-trader/SKILL.md) | Ed Thorp | Kelly sizing, walk-forward validation |

### Content & Experience

| Role | Anchor Skill | Expert Persona | Focus |
|---|---|---|---|
| ui-ux-designer | [`content/role-ui-ux-designer`](../content/role-ui-ux-designer/SKILL.md) | Don Norman | Human-centered design, error-state first |
| content-creator | [`content/role-content-creator`](../content/role-content-creator/SKILL.md) | David Ogilvy | Audience research, per-platform craft |

## How Personas Are Stored

Each anchor's `SKILL.md` frontmatter carries:

```yaml
persona:
  name: "Kent Beck"
  title: "Software Engineer — TDD & Emergent Design"
  philosophy: "Make it work, make it right, make it fast — in that order."
  expertise: ["Test-Driven Development", "Refactoring", ...]
  principles:
    - "Red, green, refactor. Never write production code without a failing test first."
    ...
```

Personas are persisted into `SKILLS.json` by `python3 scripts/lint-skills.py --write`, so routers and eval harnesses can read them without parsing markdown.

## Adding or Changing a Persona

1. Edit the anchor's `SKILL.md` frontmatter (keep `principles` ≤5, one line each).
2. Regenerate the registry: `python3 scripts/lint-skills.py --write`.
3. Verify: `python3 scripts/validate-skills.py && python3 scripts/test-skills.py`.
4. Principles must be actionable rules the agent can follow or violate — not slogans.

## Coverage Status

- 23/23 role anchors have personas (6 corporate + 17 functional).
- ~38 additional non-anchor skills carry ad-hoc personas (e.g., `content/gemini-image-generator` → Ansel Adams). These are optional flavor, not dispatch targets.
- Goal: every skill reachable through a role anchor inherits its persona's judgment layer; atomic skills supply the mechanics.
