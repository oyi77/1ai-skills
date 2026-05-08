---
name: month-end-closer
description: Accruals, roll-forwards, variance commentary. Use when user says "month-end close", "accruals", "roll-forward".
---

# Month-End Closer

## Persona:

**Corporate Controller** — Inspired by the `month-end-closer` agent from anthropics/financial-services. Masters accrual accounting, roll-forward schedules, and variance analysis.

**Core Philosophy:** Close is not a deadline — it's a discipline. Every month-end is a pulse check on business health.

## Overview:

Automates the month-end close process: accruals, roll-forwards, variance commentary, and close checklist. Handles the full workflow: review → accrue → roll-forward → analyze → close.

## When to Use:

- Month-end close (every month, 3-5 day cycle)
- Quarter-end close (extended review)
- Year-end close (audit preparation)
- Variance analysis (actuals vs. budget)
- Pre-audit close review)

## When NOT to Use:

- DCF model building (use `financial/model-builder`)
- Earnings call prep (use `financial/earnings-viewer`)
- KYC onboarding (use `financial/kyc-screener`)

## Implementation:

### Phase 1: Pre-Close Checklist

**Close Tasks (Day 1-2):**
```python
pre_close = {
    "bank_reconciliation": {"status": "complete", "variance": 0},
    "ap_accruals": {"bills_received": 45, "accrued": 42, "missing": 3},
    "ar_accruals": {"unbilled_revenue": 280000, "accrued": 280000},
    "payroll_accrual": {"period_cost": 85000, "accrued": 85000},
    "depreciation": {"calc": "computed", "entry_posted": True},
    "intercompany": {"ic_entries": 12, "unreconciled": 0}
}
```

### Phase 2: Accrual Calculations

**Accrual Template:**
```python
accruals = {
    "vendor_accruals": {
        "electricity": {"invoice_date": "2024-03-28", "amount": 15000, "period": "March"},
        "legal_fees": {"invoice_date": "2024-03-30", "amount": 25000, "period": "March"},
        "bonuses": {"accrual_pct": 0.15, "base": 500000, "amount": 75000}
    },
    "roll_forward": {
        "prior_month_accrual": 120000,  # Reverse
        "new_accrual": 180000,           # New
        "net_change": 60000               # Explain
    }
}
```

### Phase 3: Variance Commentary

**Variance Analysis (Actuals vs. Budget):**
```python
variance = {
    "revenue": {
        "budget": 2500000,
        "actual": 2800000,
        "variance": 300000,  # +12%
        "explanation": "Q4 surge in enterprise deals, 3 new contracts > $100K"
    },
    "cogs": {
        "budget": 1250000,
        "actual": 1400000,
        "variance": 150000,  # +12%
        "explanation": "Higher COGS from new product line, margin held at 50%"
    },
    "opex": {
        "budget": 600000,
        "actual": 580000,
        "variance": -20000, # -3.3%
        "explanation": "Lower T&E from travel restrictions, delayed hires"
    }
}
```

### Phase 4: Close Package

**Close Deliverables:**
```markdown
# March 2024 Month-End Close Package

## Close Status: ✅ COMPLETE (3.5 days)

## Key Metrics
| Metric | Budget | Actual | Variance |
|---------|--------|--------|----------|
| Revenue | $2.5M | $2.8M | +$300K (+12%) |
| EBITDA | $750K | $920K | +$170K (+22.7%) |
| Net Income | $450K | $580K | +$130K (+28.9%) |

## Accruals Summary
- Total accruals: $320K (vs. $260K prior)
- Reversals: $120K (prior month)
- Net new accruals: $200K

## Variance Commentary
1. Revenue +12%: Q4 enterprise surge (3 deals >$100K)
2. EBITDA +22.7%: Margin expansion to 32.9%
3. Headcount: 85 (vs. 80 budget) — 5 delayed start

## CFO Sign-Off: ✅ Approved 2024-04-05
```

## Common Rationalizations:

| Rationalization | Reality |
|---|---|
| "Variance is immaterial, skip commentary" | >2% variance = material, must explain |
| "Will close faster without accruals" | Missing accruals = restated financials |
| "Q4 is always messy, skip details" | Q4 = hardest close, needs MORE detail |
| "Prior accruals auto-reverse" | Must verify reversal, not assume |

## Red Flags:

- Close > 5 days (target: 3-4 days)
- Variance > 5% without written explanation
- Accruals < prior month with no rationale
- Suspense account with balance after close
- CFO hasn't sign-off within 24 hours
- Prior month accruals not reversed

## Verification:

After month-end close, confirm:

- [ ] All accruals posted: AP, AR, Payroll, Depreciation
- [ ] Roll-forward: prior reversed, new posted, net explained
- [ ] Variance > 2%: written commentary with business driver
- [ ] Trial balance: debits = credits (variance = $0)
- [ ] Key metrics: Revenue, EBITDA, Net Income vs. budget
- [ ] Close package: generated with CFO sign-off
- [ ] Close time: < 5 days (3-4 target)
- [ ] Prior month accruals: all reversed and verified
- [ ] Next month prep: recurring accrual schedule ready

## Integration Points:

**Cross-Skill References:**
- `financial/gl-reconciler` — For GL reconciliation before close
- `financial/model-builder` — For comparing actuals vs. budget
- `operations/finance-ops` — For finance ops dashboard
- `references/trading-checklist.md` — For close risk controls

**MCP Server Integrations:**
- NetSuite MCP — For close checklist automation
- Xero MCP — For SMB month-end
- QuickBooks MCP — For automated accruals

Load `references/trading-checklist.md` for complete trading checklists.
