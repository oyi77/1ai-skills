---
name: model-builder
description: Builds and updates DCF, LBO, and 3-statement financial models in Excel with live data connections. Use when user
  says "build DCF", "create LBO model", "populate 3-statement model".
domain: financial
tags:
- analysis
- builder
- finance
- investment
- model
---

# Model Builder

## Persona

**Financial Modeling Expert** — Inspired by the `model-builder` agent from anthropics/financial-services. Masters Excel, Power Query, and financial mathematics.

**Core Philosophy:** Every model is a hypothesis about the future. Structure it so changes are traceable, assumptions are visible, and outputs are auditable.

## Overview

Creates institutional-quality financial models: DCF (Discounted Cash Flow), LBO (Leveraged Buyout), and 3-Statement Models. Outputs live Excel files with embedded formulas, scenario switches, and sensitivity tables.

## When to Use

- Building a DCF for valuation
- Creating an LBO model for private equity
- Populating 3-statement model templates
- Updating models with new earnings data
- Running sensitivity analysis on key assumptions
- Preparing models for investment committee

## When NOT to Use:

- Simple back-of-envelope math (use `trading/alphaear-strategy`)
- Earnings note drafting (use `financial/earnings-viewer`)
- Portfolio tracking (use `trading/investing-algorithm-framework`)

## Implementation


The implementation follows a phased approach: select model type, construct Excel workbook, and run sensitivity analysis.


### Phase 1: Model Selection & Setup

**DCF Model (Cash Flow Focus):**
```python
dcf_structure = {
    "revenue_projections": {"years": 5, "cagr": 0.15},
    "ebitda_margin": {"base": 0.25, "convergence": 0.22},
    "wacc": 0.095,  # Weighted Average Cost of Capital
    "terminal_growth": 0.025,
    "tax_rate": 0.21,
    "capex_pct": 0.03
}
```

**LBO Model (PE Focus):**
```python
lbo_structure = {
    "entry_multiple": 8.0,  # x EBITDA
    "debt_structure": {
        "senior_debt": 4.0,  # x EBITDA
        "subordinated_debt": 2.0,
        "equity_check": "rest"
    },
    "exit_multiple": 10.0,
    "holding_period": 5,  # years
    "irr_target": 0.20
}
```

**3-Statement Model (Full Accounting):**
```python
three_statement = {
    "income_statement": ["revenue", "cogs", "opex", "ebitda", "ebit", "net_income"],
    "balance_sheet": ["cash", "ar", "inventory", "ppne", "debt", "equity"],
    "cash_flow": ["bopi", "capex", "debt_service", "free_cash_flow"]
}
```

### Phase 2: Excel Construction

**DCF Excel Structure:**
```excel
[Assumptions Tab]
- Revenue Growth: 15% (linked to historicals)
- EBITDA Margin: 25% → 22% (convergence)
- WACC: 9.5% (calculated via CAPM)
- Terminal Growth: 2.5%

[DCF Tab]
Year:      0       1       2       3       4       5
Revenue:    100     115     132     152     175     201
EBITDA:     25      29      33      38      44      50
FCF:        15      18      21      24      28      32
PV of FCF:  14      16      18      20      23
Terminal Value:                              380
Enterprise Value:                          471
Less Net Debt:                          (50)
Equity Value:                             421
Shares Out:   100M
Price Target:  $4.21
```

### Phase 3: Sensitivity & Scenarios

**Data Table (Excel):**
```python
sensitivity = {
    "row_input": "wacc",  # 8.5%, 9.0%, 9.5%, 10.0%
    "col_input": "terminal_growth",  # 1.5%, 2.0%, 2.5%, 3.0%
    "outputs": ["enterprise_value", "price_target"],
    "scenarios": ["base", "bull", "bear"]
}
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll simplify the model" | Simple models hide critical assumptions |
| "Hardcode the numbers" | Hardcoded models break on first update |
| "Skip the audit trail" | Undocumented changes = model rot |
| "WACC is just 10%" | WACC drives 30%+ of valuation variance |
| "Terminal value doesn't matter" | TV is 60-70% of total DCF value |

## Red Flags

- Hardcoded numbers (not linked to assumptions tab)
- Missing circularity switches (debt calculations)
- No scenario manager (bull/base/bear)
- WACC calculated incorrectly (forget tax shield)
- Terminal value > 70% of total value (check!)
- No data validation (negative revenue, etc.)

## Verification

After building a model, confirm:

- [ ] Assumptions tab: all inputs visible, traceable
- [ ] DCF tab: 5-year projection, PV calculates correctly
- [ ] WACC: calculated via CAPM, not hardcoded
- [ ] Terminal value: < 70% of total enterprise value
- [ ] Sensitivity table: 2-input data table functions
- [ ] Scenarios: bull/base/bear switch works
- [ ] 3-statement: IS + BS + CFS balance (Assets = Liab + Equity)
- [ ] Excel file saved: .xlsx with formulas intact

## Integration Points

**Cross-Skill References:**
- `financial/earnings-viewer` — For updating models with earnings
- `trading/black-edge` — For alternative data inputs
- `sales/high-ticket-closing` — For presenting models to investors
- `references/trading-checklist.md` — For risk validation

**MCP Server Integrations:**
- FactSet MCP — For historical financials
- S&P Global MCP — For peer multiples
- Alpha Vantage MCP — For market data feeds

Load `references/trading-checklist.md` for complete trading checklists.

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
