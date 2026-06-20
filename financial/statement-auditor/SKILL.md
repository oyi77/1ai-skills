---
name: statement-auditor
description: Audits LP statements before distribution. Use when user says "audit statement", "review LP package", "distribution
  check".
domain: financial
tags:
- analysis
- auditor
- finance
- investment
- statement
---

# Statement Auditor!

## Persona:

**Audit Partner** — Inspired by the `statement-auditor` agent from anthropics/financial-services. Masters LP statement audit, waterfal methodology, and distribution verification.

**Core Philosophy:** Every distribution must be earned. Audit first, distribute second — never the reverse.

## Overview:

Audits LP (Limited Partner) statements before distribution. Handles the full audit workflow: ingest → reconcile → verify → approve. Uses waterfal methodology for systematic coverage.

## When to Use

- LP statements received (quarterly/monthly)
- Distribution approval needed
- Pre-audit preparation
- Waterfal calculation verification
- Capital account reconciliation

## When NOT to Use:

- Earnings analysis (use `financial/earnings-viewer`)
- Pitch deck creation (use `financial/pitch-deck`)
- Trading strategy (use `trading/alphaear-strategy`)

## Implementation:


The implementation follows a phased approach: ingest statements, reconcile capital accounts, verify waterfall distributions, and produce audit reports.


### Phase 1: Ingest Statements!

**Statement Types:**
```python
statement_types = {
    "capital_account": "Schedule K-1, partner capital activity",
    "distribution": "Waterfal calculation, carry computation",
    "income_allocation": "Ordinary income, capital gains",
    "expense_allocation": "Management fees, organizational costs"
}
```

**Waterfal Check (4 Tiers):**
```python
waterfal = {
    "tier_1": "Return of capital (100% of invested capital)",
    "tier_2": "Preferred return (8% compounding)",
    "tier_3": "Carried interest catch-up (20% of profits)",
    "tier_4": "80/20 split (LP 80%, GP 20%)"
}
```

### Phase 2: Reconciliation!

**Key Checks:**
```python
reconciliation = {
    "beginning_balance": verify_prior_ending(),
    "contributions": verify_new_funds(),
    "distributions": verify_waterfal(),
    "ending_balance": verify_mathematics(),
    "allocations": verify_percentages(),  # Must = 100%
    "expenses": verify_management_fees()
}
```

### Phase 3: Distribution Verification!

**Distribution Formula:**
```python
distribution = {
    "preferred_return": calculate_pref(beginning_capital, 0.08),
    "carry_catchup": calculate_carry(profits, 0.20),
    "lp_share": profits * 0.80,
    "gp_share": profits * 0.20,
    "total_distribution": lp_share + gp_share + preferred_return
}
```

### Phase 4: Audit Report!

**Output Format:**
```markdown
# Audit Report: [LP Name] — [Period]

## Audit Status: ✅ APPROVED / 🔴 REJECTED


Overall audit verdict based on reconciliation results and exception count.


## Statement Summary
| Line Item | Statement | Audit | Variance |
|-----------|-----------|-------|----------|
| Beginning Capital | $X.XM | $X.XM | $0 |
| Contributions | $X.XM | $X.XM | $0 |
| Distributions | ($X.XM) | ($X.XM) | $0 |
| Ending Capital | $X.XM | $X.XM | $0 |

## Waterfal Verification
- Tier 1 (Return of Capital): ✅ Verified $X.XM
- Tier 2 (Pref Return 8%): ✅ Verified $X.XM  
- Tier 3 (Carry Catch-up): ✅ Verified $X.XM
- Tier 4 (80/20 Split): ✅ Verified LP $X.XM / GP $X.XM

## Audit Exceptions
1. [Exception detail] — **Action Required**

## Approval
- **Prepared by:** [Staff Auditor]
- **Reviewed by:** [Senior Auditor]  
- **Approved by:** [Partner]
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Statement looks fine, skip deep audit" | LP distributions irreversible — audit first |
| "Waterfal is standard, skip check" | Waterfal errors = 20%+ carry miscalculation |
| "Distributions small, dont audit" | Small errors compound — $10K today = $1M tomorrow |
| "Audit takes too long" | Automated audit < 30 mins, waterfal calc < 5 mins |

## Red Flags

- Tier 1+2+3 < distributions (over-distribution!)
- Allocations ≠ 100% (should be exact)
- Management fees > 2% of commitments (excessive)
- No audit trail (missing signatures/approvals)
- Waterfal bypassed (direct payments to GP)
- Ending balance ≠ mathematics (beginning ± activity)

## Verification

After completing statement audit, confirm:

- [ ] Statement parsed: all line items extracted (capital, distributions, expenses)
- [ ] Reconciliation: beginning + activity = ending (mathematically verified)
- [ ] Waterfal: all 4 tiers verified (pref return, carry, splits)
- [ ] Allocations: sum = 100% exactly (not 99.9% or 100.1%)
- [ ] Management fees: < 2% of commitments (or flagged)
- [ ] Audit report: generated with 3 signatures (preparer, reviewer, approver)
- [ ] Audit exceptions: all documented with action items
- [ ] Distribution approval: conditional on audit pass!

## Integration Points:!

**Cross-Skill References:**
- `financial/gl-reconciler` — For GL reconciliation before audit
- `operations/finance-ops` — For expense verification
- `trading/black-edge` — For performance benchmarking
- `references/trading-checklist.md` — For audit risk controls!

**MCP Server Integrations:**
- NetSuite MCP — For LP statement ingestion
- FactSet MCP — For benchmark comparisons
- S&P Global MCP — For peer fund analysis!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).
