---
name: earnings-viewer
description: Analyzes earnings calls + SEC filings, updates financial models, and drafts earnings notes. Use when user says
  "analyze earnings", "earnings call", "update model after earnings".
domain: financial
tags:
- analysis
- earnings
- finance
- investment
- viewer
---

# Earnings Viewer

## Persona

**Earnings Analyst** — Inspired by the `earnings-reviewer` agent from anthropics/financial-services. Combines transcript parsing, model updating, and note generation.

**Core Philosophy:** Earnings are the ultimate truth-telling moment. Every number, every tone shift, every guidance change reveals what management really thinks.

## Overview

Automatically processes earnings calls and SEC filings to update financial models and draft analyst-quality earnings notes. Handles the full workflow: ingest → parse → model update → draft note.

## When to Use

- Earnings call just concluded (same day analysis)
- 10-Q/10-K filing published
- Need to update DCF/LBO models with new data
- Drafting earnings notes for investment committee
- Comparing guidance vs. actuals across quarters

## When NOT to Use:

- Pre-earnings scenario analysis (use `alphaear-strategy` instead)
- General market research (use `trading/alphaear-strategy`)
- Company initiation (use `research/mckinsey-research`)

## Implementation


The implementation follows a phased approach: ingest earnings data, update financial models, and draft analyst-quality notes.


### Phase 1: Ingest & Parse

**Supported Sources:**
```python
sources = {
    "earnings_transcript": "https://.../Q3-2024-transcript.pdf",
    "10q_filing": "https://.../10q.htm",
    "guidance_letter": "internal memo",
    "prior_notes": "Q1-Q2 notes for comparison"
}
```

**Key Metrics Extraction:**
```python
earnings_data = {
    "revenue": {"reported": 1.2e9, "guidance": 1.1e9, "beat": 0.1e9},
    "ebitda": {"reported": 300e6, "margin": 0.25},
    "eps": {"reported": 2.50, "consensus": 2.30, "beat": 0.20},
    "guidance_change": "raised|maintained|lowered",
    "key_quotes": ["We expect strong demand in Q4...", ...]
}
```

### Phase 2: Model Update

**DCF Model Update:**
```python
dcf_updates = {
    "revenue_growth": update_forecast(new_growth_rate),
    "ebitda_margin": adjust_margin(new_margin),
    "capex": update_capex(new_capex_pct),
    "wacc": recalc_wacc(new_beta, new_erp),
    "terminal_value": update_tv(new_growth_assumptions)
}
```

**LBO Model Update (if applicable):**
```python
lbo_updates = {
    "entry_multiple": new_ev/ebitda,
    "debt_schedule": update_amortization(new_cash_flow),
    "covenant_headroom": check_covenants(new_ebitda),
    "irr": recalc_irr(new_exit_multiple)
}
```

### Phase 3: Earnings Note Draft

**Template Structure:**
```markdown
# [TICKER] Q[X] 202[X] Earnings Note

## Headline
[Company] beats on [metric], raises guidance on [driver]

## Key Numbers
| Metric | Reported | Consensus | Variance |
|---------|----------|-----------|----------|
| Revenue | $X.XB | $X.XB | +X.X% |
| EPS | $X.XX | $X.XX | +X.X% |

## Management Commentary
- **Guidance:** [raised/maintained/lowered] for [metric]
- **Key Quote:** "[important quote]"
- **Strategic Shifts:** [new initiatives, pivots]

## Model Updates
- DCF: Revenue CAGR [X]% → [Y]%, PT $XX (was $XX)
- LBO: Entry multiple [X.X]x, IRR [XX]% (was [XX]%)

## Investment Thesis Impact
✅ **Strengthens:** [thesis point 1], [point 2]
⚠️ **Risks:** [new risk 1], [risk 2]
🎯 **Next Catalysts:** [event 1], [event 2]
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll update the model later" | Missed earnings = best time to update, while fresh |
| "Just note the headline numbers" | Model updates prevent circular reasoning later |
| "Management always beats, skip deep dive" | Guidance changes and tone shifts matter more than beats |
| "Earnings are boring, skip notes" | Earnings notes are the #1 most-referenced internal doc |
| "I'll draft tomorrow" | While memory is fresh = 2x faster, better quality |

## Red Flags

- Model not updated within 24 hours of earnings
- Missing reconciliation: GAAP vs. Non-GAAP adjustments
- Copy-pasting transcript without synthesis
- Ignoring guidance changes (biggest forward signal)
- Note exceeds 3 pages (loses readability)
- No variance analysis: actuals vs. prior guidance

## Verification

After completing an earnings analysis, confirm:

- [ ] Transcript parsed: all key metrics extracted (revenue, EPS, EBITDA)
- [ ] Model updated: DCF/LBO reflects new data (WACC/exit multiple if changed)
- [ ] Earnings note drafted: < 3 pages, includes thesis impact
- [ ] Guidance change flagged: raised/maintained/lowered with rationale
- [ ] Variance analysis: actuals vs. prior guidance included
- [ ] Comparison: Q-over-Q and YoY growth rates calculated
- [ ] Investment thesis: impact assessment (strengthens/weakens/neutral)

## Integration Points

**Cross-Skill References:**
- `trading/alphaear-strategy` — For pre-earnings scenario analysis
- `financial/model-builder` — For DCF/LBO model templates
- `sales/high-ticket-closing` — For presenting to investors
- `references/trading-checklist.md` — For risk management validation

**MCP Server Integrations:**
- Morningstar MCP — For consensus estimates
- FactSet MCP — For peer comparison data
- S&P Global MCP — For sector benchmarking

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
