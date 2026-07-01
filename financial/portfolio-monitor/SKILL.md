---
name: portfolio-monitor
description: Track portfolio company KPIs, variances, returns analysis. Use when user says "monitor portfolio", "track KPIs",
  "portfolio returns".
domain: financial
tags:
- analysis
- finance
- investment
- monitor
- portfolio
---

# Portfolio Monitor!

## Persona:!

**PE Principal** — Inspired by the `portfolio-monitoring` skill from anthropics/financial-services. Masters KPI tracking, return analysis, and variance monitoring.

**Core Philosophy:** Portfolio monitoring is about pattern recognition. Spot the degrading asset before it's obvious — leading indicators beat lagging indicators.

## Overview

Tracks portfolio company KPIs, monitors variances vs. underwriting, and calculates returns (IRR, MOIC). Handles the full workflow: ingest → track → analyze → report.

## When to Use

- Monthly portfolio review (all companies)
- Quarterly board meetings (underwriting vs. actuals)
- IRR/MOIC calculation (fund reporting)
- Variance analysis (KPIs vs. targets)
- Portfolio company comparison (peer benchmarking)
- Exit preparation (returns analysis)

## When NOT to Use:!

- Single company deep-dive (use `financial/meeting-prep`)
- Earnings analysis (use `financial/earnings-viewer`)
- Building DCF models (use `financial/model-builder`)
- Trading strategy (use `trading/alphaear-strategy`)

## Implementation:!


The implementation follows a phased approach: track KPIs, calculate returns, analyze variances, and generate portfolio reports.


### Phase 1: KPI Tracking!

**Portfolio KPIs:**
```python
kpi_dashboard = {
    "revenue_growth": {"target": "25%", "actual": "32%", "variance": "+7% ✅"},
    "gross_margin": {"target": "65%", "actual": "61%", "variance": "-4% 🔴"},
    "ebitda_margin": {"target": "20%", "actual": "18%", "variance": "-2% 🔴"},
    "headcount": {"target": 150, "actual": 135, "variance": "-15 ⚠️"},
    "burn_rate": {"target": "$500K", "actual": "$650K", "variance": "+$150K 🔴"}
}
```

### Phase 2: Returns Analysis!

**IRR/MOIC Calculation:**
```python
returns = {
    "company_a": {
        "invested": 15000000,  # $15M
        "realized": 25000000,  # $25M distributions
        "unrealized": 35000000,  # $35M fair value
        "irr": 0.28,          # 28% IRR
        "moic": 4.0,          # 4.0x MOIC
        "holding_period": 3.5    # years
    },
    "company_b": {
        "invested": 10000000,
        "realized": 0,
        "unrealized": 18000000,
        "irr": 0.22,
        "moic": 1.8,
        "holding_period": 2.0
    }
}
```

### Phase 3: Variance Commentary!

**Variance Analysis:**
```python
variances = {
    "revenue": {
        "variance_pct": "+7%",
        "explanation": "Enterprise deals closed faster than underwritten",
        "action": "Raise FY guidance +5%"
    },
    "gross_margin": {
        "variance_pct": "-4%",
        "explanation": "New product line margin 45% vs. 65% core",
        "action": "Price optimization study"
    },
    "burn": {
        "variance_pct": "+30%",
        "explanation": "Hired 15 ahead of plan for Q3 launch",
        "action": "Monitor headcount vs. roadmap"
    }
}
```

### Phase 4: Portfolio Report!

**Report Structure:**
```markdown
# Portfolio Report — Q1 2026

## Fund-Level Metrics
| Metric | Value | Target | Status |
|---------|-------|--------|--------|
| NAV | $480M | $450M | +$30M ✅ |
| IRR | 24% | 20% | +4% ✅ |
| MOIC | 2.1x | 2.0x | +0.1x ✅ |
| DPI | 0.8x | 0.7x | +0.1x ✅ |

## Company Highlights

Top performers and watch-list companies ranked by IRR, MOIC, and variance.

### ✅ Top Performers
1. **Co A** — IRR 28%, MOIC 4.0x (above plan)
2. **Co D** — IRR 25%, MOIC 2.5x (on plan)

### 🔴 Watch List
1. **Co B** — IRR 22%, burn +30% (action: cost review)
2. **Co F** — IRR 12%, revenue -5% (action: strategic review)

## Action Items
1. Co B: Cost optimization plan by Q2
2. Co F: Strategic review meeting scheduled
3. Co A: Double-down analysis (add $10M?)
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "KPIs are boring, skip tracking" | KPIs predict exits 18+ months out |
| "IRR is fine, skip variance" | Variance = early warning, catch before it's terminal |
| "Portfolio is small, skip report" | <5 companies = higher concentration risk, monitor MORE |
| "Quarterly is enough" | Monthly catches burns before they're fatal |

## Red Flags

- IRR < 15% for 3+ years (underperforming)
- MOIC < 1.5x at exit year (failed investment)
- Burn > 2x underwritten (runway risk!)
- Revenue growth < 10% (stagnation)
- Gross margin < 50% (pricing problem)
- 2+ companies on watch list (portfolio risk > 30%)

## Verification

After completing portfolio review, confirm:

- [ ] KPIs tracked: all companies, 5+ metrics each
- [ ] IRR/MOIC: calculated correctly (Excel formula verified)
- [ ] Variances: > 2% explained with action items
- [ ] Top performers: identified (≥ 2 highlighted)
- [ ] Watch list: identified (≥ 2 flagged)
- [ ] Returns: DPI/ RVPI / TVPI all calculated
- [ ] Report generated: 3-5 pages, executive summary
- [ ] Action items: 3+ specific, assigned with dates

## Integration Points:!

**Cross-Skill References:**
- `financial/model-builder` — For DCF updates on portfolio cos
- `financial/statement-auditor` — For LP reporting
- `trading/black-edge` — For adverse news monitoring
- `references/trading-checklist.md` — For portfolio risk validation!

**MCP Server Integrations:**
- FactSet MCP — For public comps benchmarking
- S&P Global MCP — For sector performance
- PitchBook MCP — For private market multiples!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
