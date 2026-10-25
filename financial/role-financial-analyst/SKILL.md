---
name: role-financial-analyst
description: Use when orchestrating financial analysis, cashflow modeling, DCF valuations,
  general ledger reconciliation, financial statement audits, and CFO operations.
domain: financial
author: oyi77
version: 1.0.0
category: financial
tags:
- finance
- financial-analysis
- valuation
- dcf
- accounting
- gl-reconciliation
- cashflow
- auditing
license: MIT
subdomain: financial-analysis
---

## Overview

The `role-financial-analyst` skill directs corporate financial analysis, financial statement audits, three-statement financial modeling, valuation reviews, and automated general ledger (GL) reconciliations. Rather than treating finance as disconnected spreadsheets or manual balance checks, this role establishes rigorous mathematical models for cashflow forecasts, DCF/LBO valuations, automated break detection in accounting ledgers, and institutional-grade financial telemetry.

```
[Phase 1: Financial Ingestion & Audit] ──► [Phase 2: GL Reconciliation & Breaks] ──► [Phase 3: Financial Modeling (3-Statement/DCF)]
                                                                                                    │
                   [Phase 5: CFO Telemetry & Report] ◄── [Phase 4: Valuation & Variance] ◄──────────┘
```

The financial analyst enforces accounting equation invariants (Assets = Liabilities + Equity), double-entry debit-credit parity, verifiable audit trails, and defensible valuation assumptions grounded in empirical historical data.

## When to Use

- When building three-statement financial models, revenue forecasts, or operational budget projections.
- When performing company or asset valuations using Discounted Cash Flow (DCF), Comparable Company Analysis, or LBO models.
- When auditing balance sheets, income statements, and cashflow statements for inconsistencies or breaks.
- When executing automated general ledger reconciliations to trace breaks between sub-ledgers and bank statements.
- When monitoring corporate financial runway, burn rates, multi-stream revenues, and unit economics.
- When preparing financial documentation packs for investor presentations, quarterly reviews, or LP statements.

## When NOT to Use

- When executing automated high-frequency crypto/derivative trades on exchanges (use `trading/role-quantitative-trader`).
- When implementing application software code or backend database schemas (use `development/role-software-engineer`).
- When designing UI design tokens or website layouts (use `content/role-ui-ux-designer`).
- When auditing cloud infrastructure configurations or cybersecurity vulnerabilities (use `cybersecurity/role-security-engineer`).

## Deterministic Dispatch Matrix

| Financial Scope / Analytical Objective | Delegated Child Skill | Primary Financial Artifact |
|---|---|---|
| Comprehensive financial data extraction, ticker analysis, market ratios | `financial/all-in-one-finance` | Multi-asset financial overview and key financial ratios |
| Real-time multi-stream revenue tracking, cashflow burn, runway alerts | `financial/finance-tracker` | Cashflow telemetry, runway runway projection, gap alerts |
| Strategic CFO operational modeling, cost optimization, capital planning | `operations/finance-ops` | Operational budget models and cost-reduction plans |
| Building dynamic 3-statement models, DCF, LBO, and scenario forecasts | `financial/model-builder` | Formula-linked financial models with sensitivity tables |
| Auditing private equity / venture GP packages, NAV, and LP statements | `financial/valuation-reviewer` | Valuation review memorandum with empirical comps |
| Auditing financial statements, balance checks, break detection | `financial/statement-auditor` | Audit report identifying ledger breaks and discrepancies |
| Reconciling general ledger balances, finding breaks, tracing accounting errors | `financial/gl-reconciler` | Reconciled trial balance with error resolution trail |

## Workflow

### Phase 1: Ingestion & Financial Data Hygiene

1. Ingest raw financial data (trial balances, bank feeds, ERP ledgers, SEC filings).
2. Validate data types and currency normalizations using `financial/all-in-one-finance`.
3. Assert that starting balance matches the prior closed period's ending balance.

### Phase 2: General Ledger Reconciliation & Break Resolution

1. Dispatch to `financial/gl-reconciler` to match transactions between bank statements and sub-ledgers.
2. Assert double-entry equality: sum of debits must identically equal sum of credits ($$\sum \text{Debits} - \sum \text{Credits} = 0$$).
3. If breaks are detected, trace transaction IDs, timing lags, and currency exchange variances to produce an adjusting journal entry.

### Phase 3: Three-Statement Financial Modeling

1. Dispatch to `financial/model-builder` to link Income Statement, Balance Sheet, and Cashflow Statement dynamically.
2. Enforce structural integrity: Net Income feeds Retained Earnings; Cash from operations, investing, and financing ties to the ending cash balance on the Balance Sheet.
3. Incorporate scenario analysis (Base, Bull, Bear) with explicit driver toggles (revenue growth, gross margin, churn).

### Phase 4: Valuation & Investment Due Diligence

1. Dispatch to `financial/valuation-reviewer` or `financial/statement-auditor` to audit asset valuation assumptions.
2. Build Discounted Cash Flow (DCF) models using Weighted Average Cost of Capital (WACC) and defensible Terminal Value multiples.
3. Conduct sensitivity analysis across terminal growth rates and discount rates.

### Phase 5: CFO Telemetry & Board Presentation

1. Track daily revenue velocity, runway, and cash burn via `financial/finance-tracker`.
2. Model operational cost structures and unit economics through `operations/finance-ops`.
3. Compile executive financial summaries and board-ready memos with verified audit trails.

## Anti-Rationalization

| Financial Excuse | Flawed Rationalization | Required Financial Discipline |
|---|---|---|
| "A $10,000 rounding discrepancy is immaterial" | "It doesn't affect the big picture analysis." | Unreconciled breaks mask larger offsetting errors or fraud. Every break must be resolved to zero. |
| "Hardcoding future growth at 20% is standard" | "Everyone uses a flat 20% assumption for SaaS." | Hardcoded assumptions obscure operational reality. Ground growth in cohort retention and pipeline velocity. |
| "The cashflow statement can be estimated" | "Income statement already shows we are profitable." | Profit does not equal cash. A company can be profitable on paper while going bankrupt from working capital lockup. Model cashflow explicitly. |
| "Balance sheet doesn't balance, just add a plug" | "We can adjust the plug during year-end audit." | Balance sheet plugs undermine the integrity of the entire model. Enforce strict mathematical linkage across statements. |
| "Terminal growth of 6% is reasonable" | "The business is in a high-growth tech sector." | Terminal growth cannot exceed long-term GDP growth (typically 2-3%). Anchor terminal assumptions in macroeconomic reality. |

## Implementation Examples

### Automated General Ledger Double-Entry Auditor (Python)

```python
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class JournalEntry:
    entry_id: str
    account: str
    debit: float
    credit: float

def audit_journal_entries(entries: List[JournalEntry]) -> Dict[str, float]:
    """Validates double-entry accounting invariant: Total Debits == Total Credits."""
    total_debits = sum(e.debit for e in entries)
    total_credits = sum(e.credit for e in entries)
    discrepancy = round(total_debits - total_credits, 2)
    
    print(f"Total Debits:  ${total_debits:,.2f}")
    print(f"Total Credits: ${total_credits:,.2f}")
    print(f"Discrepancy:   ${discrepancy:,.2f}")
    
    if discrepancy != 0.0:
        raise ValueError(f"CRITICAL BREAK: General ledger is out of balance by ${discrepancy:,.2f}!")
        
    print("SUCCESS: General ledger is perfectly balanced.")
    return {"total_debits": total_debits, "total_credits": total_credits, "balance": 0.0}

if __name__ == "__main__":
    sample_entries = [
        JournalEntry("1", "Cash", 5000.0, 0.0),
        JournalEntry("2", "Accounts Receivable", 2500.0, 0.0),
        JournalEntry("3", "Revenue", 0.0, 7500.0),
    ]
    audit_journal_entries(sample_entries)
```

### Financial Model Invariant Verification (Bash/Python)

```bash
#!/usr/bin/env bash
set -euo pipefail

MODEL_DATA="data/financial_model.json"
echo "=== Validating Financial Statement Invariants ==="

python3 -c "
import json
with open('$MODEL_DATA') as f:
    data = json.load(f)

# Invariant: Assets == Liabilities + Equity
assets = data.get('total_assets', 0)
liabilities = data.get('total_liabilities', 0)
equity = data.get('total_equity', 0)

diff = abs(assets - (liabilities + equity))
assert diff < 0.01, f'Balance sheet does not balance! Diff: {diff}'
print('SUCCESS: Balance sheet equation holds (Assets == Liabilities + Equity).')
"
```

## Verification Checklist

- [ ] Double-entry accounting invariants hold ($$\sum \text{Debits} == \sum \text{Credits}$$).
- [ ] General ledger reconciliations contain zero unexplained breaks or plug figures.
- [ ] Three financial statements (Income, Balance Sheet, Cash Flow) are dynamically and mathematically linked.
- [ ] Valuation discount rates (WACC) and terminal growth rates are grounded in macro benchmarks.
- [ ] Financial runway and burn rates are tracked with automated gap alerting.
- [ ] Full audit trail documented for all adjusting entries and financial statement changes.
