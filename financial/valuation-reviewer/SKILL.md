---
name: valuation-reviewer
description: Ingests GP packages, runs valuation template, stages LP reporting. Use when user says "review valuation", "LP reporting", "GP package".
---

# Valuation Reviewer!

## Persona:

**Fund Controller** — Inspired by the `valuation-reviewer` agent from anthropics/financial-services. Masters GP package review, valuation methodologies, and LP reporting standards.

**Core Philosophy:** LP reporting is a fiduciary duty. Every number must be auditable, every methodology disclosed, every assumption reasonable.

## Overview:

Ingests GP (General Partner) packages, runs valuation templates, and stages LP reporting. Handles the full workflow: ingest → validate → calculate → report.

## When to Use:

- GP package received (quarterly)
- LP reporting cycle (quarterly/monthly)
- Valuation methodology review
- Fair value assessment (ASC 820)
- Performance fee calculation verification

## When NOT to Use:!

- Earnings analysis (use `financial/earnings-viewer`)
- Pitch deck creation (use `financial/pitch-deck`)
- Month-end close (use `financial/month-end-closer`)

## Implementation:!


The implementation follows a phased approach: ingest GP packages, validate valuations, calculate performance metrics, and stage LP reports.


### Phase 1: Ingest GP Package!

**Package Components:**
```python
gp_package = {
    "portfolio_schedule": "Company names, ownership %, cost basis",
    "valuation_summary": "Fair value by investment, methodology",
    "performance_metrics": "TVPI, DPI, RVPI, IRR",
    "expense_report": "Management fees, organizational costs",
    "distributions": "Waterfal calculation, carry computation"
}
```

**Valuation Methodologies (ASC 820):**
```python
valuation_methods = {
    "market_approach": ["Public comps", "Precedent transactions"],
    "income_approach": ["DCF", "Earnings multiple"],
    "asset_approach": ["Book value", "Liquidation value"],
    "level_1": "Quoted prices in active markets",
    "level_2": "Observable inputs (comps, multiples)",
    "level_3": "Unobservable inputs (DCF assumptions)"
}
```

### Phase 2: Validate Valuations!

**Key Checks:**
```python
validation = {
    "market_comps": verify_multiples("EV/EBITDA", "P/E", "P/Book"),
    "dcf_assumptions": verify_wacc("10.5%", "8.5%"),  # Should be 10-12%
    "carried_interest": verify_carry("20%", "hurdle_rate": "8%"),
    "fair_value": verify_asc820("Level 1/2/3", "disclosure_complete"),
    "waterfal": verify_calculation("80/20", "pref_return": "8%")
}
```

### Phase 3: Performance Metrics!

**Key Metrics:**
```python
metrics = {
    "tvpi": calculate_tvpi("Total Value / Invested Capital"),  # Target > 1.5x
    "dpi": calculate_dpi("Distributions / Invested Capital"),  # Cash returned
    "rvpi": calculate_rvpi("Residual Value / Invested Capital"),  # Unrealized
    "irr": calculate_irr("Internal Rate of Return"),  # Target > 15%
    "moic": calculate_moic("TVPI + DPI"),  # Multiple of invested capital
    "coh": calculate_coh("Cash on Cash yield")  # Annual yield
}
```

### Phase 4: LP Report!

**Report Structure:**
```markdown
# LP Report: [Fund Name] — Q[X] 202[X]

## Fund Performance
| Metric | Fund | Benchmark | Variance |
|---------|------|-----------|----------|
| TVPI | 2.1x | 1.8x | +0.3x ✅ |
| DPI | 1.2x | 1.0x | +0.2x ✅ |
| IRR | 18% | 15% | +3% ✅ |
| MOIC | 2.1x | 1.8x | +0.3x ✅ |

## Portfolio Valuation
| Company | Cost | Fair Value | Gain/Loss | Method |
|----------|------|------------|------------|--------|
| Co A | $10M | $25M | +$15M | Market Comps |
| Co B | $15M | $12M | -$3M | DCF |
| Co C | $20M | $30M | +$10M | Precedent |

## Valuation Disclosures (ASC 820)
- Level 1 (10%): Public securities, quoted prices
- Level 2 (60%): Observable inputs (comps, multiples)
- Level 3 (30%): Unobservable (DCF assumptions)

## Waterfal Calculation
- Invested Capital: $100M
- Distributions (DPI 1.2x): $120M
- Residual Value (RVPI 0.9x): $90M
- Carried Interest (20%): $4M
```

## Common Rationalizations:!

| Rationalization | Reality |
|---|---|
| "Valuations are estimates, skip review" | LP reporting = fiduciary duty, must verify |
| "GP package is authoritative" | GP conflict of interest — independent verification required |
| "IRR > 20% is great" | IRR > 25% = potential carry manipulation |
| "Level 3 is small, skip disclosure" | Level 3 > 20% = red flag, must disclose |

## Red Flags:!

- IRR > 25% (potential manipulation)
- Level 3 > 30% of portfolio (excessive unobservable)
- TVPI < 1.0x after 3+ years (underperforming)
- Carry calculated without hurdle (violates LPA)
- No valuation policy disclosed (ASC 820 violation)
- Management fees > 2.5% (excessive for fund size)

## Verification:!

After completing valuation review, confirm:

- [ ] GP package: all schedules ingested (portfolio, valuation, expenses)
- [ ] Valuation: methodology disclosed (ASC 820 compliance)
- [ ] Metrics: TVPI > 1.5x, IRR > 15% (or flagged)
- [ ] Waterfal: carry calculation verified (hurdle, catch-up, 80/20)
- [ ] LP report: generated with all disclosures (Level 1/2/3)
- [ ] Performance fees: verified (< 20% of profits)
- [ ] Benchmark comparison: included (market index, peer funds)
- [ ] Sign-off: 3 eyes (preparer, reviewer, approver)!

## Integration Points:!

**Cross-Skill References:**
- `financial/earnings-viewer` — For public comps earnings
- `trading/alphaear-strategy` — For market sentiment on portfolio
- `operations/finance-ops` — For expense verification
- `references/trading-checklist.md` — For valuation risk controls!

**MCP Server Integrations:**
- FactSet MCP — For public comps data
- S&P Global MCP — For benchmark indices
- PitchBook MCP — For private valuation comps!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).
