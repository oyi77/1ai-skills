---
name: gl-reconciler
description: Finds breaks, traces root cause, routes for sign-off. Use when user says "reconcile GL", "find breaks", "trace
  accounting error".
domain: financial
tags:
- analysis
- finance
- investment
- reconciler
---

# GL Reconciler

## Persona:

**Controller** — Inspired by the `gl-reconciler` agent from anthropics/financial-services. Masters general ledger reconciliation, break tracing, and variance analysis.

**Core Philosophy:** Every dollar must be accounted for. If the GL doesn't balance, nothing downstream can be trusted — not your financials, not your reports, not your audit.

## Overview:

Finds breaks between GL accounts, traces root causes, and routes for sign-off. Handles the full reconciliation workflow: extract → compare → trace → correct → approve.

## When to Use

- Month-end close process
- Variance > 2% in any GL account
- Suspense account balance > $0
- Pre-audit preparation
- Intercompany reconciliation
- Foreign currency revaluation)

## When NOT to Use:

- Building DCF models (use `financial/model-builder`)
- Earnings analysis (use `financial/earnings-viewer`)
- Pitch deck creation (use `financial/pitch-deck`)

## Implementation:


The implementation follows a phased approach: extract trial balance data, detect breaks, trace root causes, and route corrections for sign-off.


### Phase 1: Data Extraction

**Source Systems:**
```python
gl_sources = {
    "general_ledger": "extract_gl_trial_balance()",
    "subledgers": ["ap", "ar", "payroll", "fixed_assets"],
    "bank": "extract_bank_statements(period)",
    "intercompany": "extract_ic_entries(subsidiary)"
}
```

**Trial Balance Extract:**
```python
trial_balance = {
    "as_of": "2024-03-31",
    "accounts": {
        "1000_cash": {"dr": 500000, "cr": 0, "net": 500000},
        "2000_ap": {"dr": 0, "cr": 250000, "net": -250000},
        "3000_revenue": {"dr": 0, "cr": 1000000, "net": -1000000},
        "4000_cogs": {"dr": 600000, "cr": 0, "net": 600000}
    },
    "total_debits": 1500000,
    "total_credits": 1500000,  # MUST EQUAL!
    "variance": 0  # Target: $0
}
```

### Phase 2: Break Detection

**Common Break Types:**
```
break_rules = {
    "tb_out_of_balance": {"dr_total != cr_total", "severity": "critical"},
    "suspense_balance": {"account_1999 > 0", "severity": "high"},
    "intercompany_mismatch": {"sub_dr != parent_cr", "severity": "high"},
    "fx_variance": {"abs(variance) > 0.02 * balance", "severity": "medium"},
    "unreconciled_entries": {"status == 'unreconciled'", "severity": "medium"}
}
```

### Phase 3: Root Cause Tracing

**Trace Algorithm:**
```python
def trace_break(account, variance):
    # Step 1: Check subledger
    subledger_balance = get_subledger_balance(account)
    if subledger_balance != gl_balance:
        return f"Subledger mismatch: GL={gl_balance}, SL={subledger_balance}"
    
    # Step 2: Check timing differences
    cutoff_test = verify_cutoff(account, period_end)
    if not cutoff_test.passed:
        return f"Timing difference: {cutoff_test.details}"
    
    # Step 3: Check intercompany
    ic_entries = get_intercompany_entries(account)
    missing_ic = [e for e in ic_entries if e.status == 'missing']
    if missing_ic:
        return f"Missing intercompany entries: {len(missing_ic)}"
    
    # Step 4: Check FX revaluation
    fx_variance = calculate_fx_variance(account)
    if abs(fx_variance) > 0.02 * gl_balance:
        return f"FX revaluation error: {fx_variance}"
    
    return "Break cause: UNKNOWN — escalate to controller"
```

### Phase 4: Correction & Sign-Off

**Journal Entry Template:**
```python
je = {
    "date": "2024-03-31",
    "lines": [
        {"account": "1999_suspense", "dr": 0, "cr": 5000},
        {"account": "5000_expense", "dr": 5000, "cr": 0}
    ],
    "description": "Clear suspense account - March variance",
    "supporting": "invoice_123.pdf, bank_statement_march.pdf",
    "approval": {
        "prepared_by": "staff_accountant",
        "reviewed_by": "controller",
        "approved_by": "cfo"
    }
}
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Variance is small, close anyway" | $5K variance = $60K annual run-rate error |
| "Suspense can hold this" | Suspense > $0 = failed close |
| "Intercompany will clear next month" | I/C breaks compound, must resolve current period |
| "FX variance is just exchange rate" | FX must be revalued at period-end rates |

## Red Flags

- Trial balance out of balance (debits != credits)
- Suspense account with balance > $0
- Unreconciled entries > 5% of total
- Variance > 2% without explanation
- Sign-off by same person who prepared
- Missing support documentation

## Verification

After completing reconciliation, confirm:

- [ ] Trial balance: debits = credits, variance = $0
- [ ] All accounts reconciled: variance explained and documented
- [ ] Suspense account: $0 balance (all cleared)
- [ ] Intercompany: parent = subsidiary (both sides)
- [ ] FX revaluation: done at period-end rates
- [ ] Breaks traced: root cause identified for each
- [ ] Journal entries: prepared, reviewed, approved (3 eyes)
- [ ] Supporting docs: attached for all adjustments
- [ ] Sign-off memo: generated with approval chain

## Integration Points:

**Cross-Skill References:**
- `operations/finance-ops` — For month-end close checklist
- `financial/model-builder` — For balance sheet verification
- `financial/earnings-viewer` — For P&L reconciliation
- `references/trading-checklist.md` — For risk controls validation

**MCP Server Integrations:**
- NetSuite MCP — For GL extraction
- SAP MCP — For enterprise GL access
- Xero MCP — For SMB reconciliation

Load `references/trading-checklist.md` for complete trading checklists.

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
