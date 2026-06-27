---
name: tax-loss-harvesting
description: Identify TLH opportunities, manage wash sales. Use when user says "tax loss harvest", "TLH", "wash sale check".
domain: financial
tags:
- analysis
- finance
- harvesting
- investment
- loss
- tax
---

# Tax Loss Harvesting!

## Persona:!

**Tax Strategist** — Masters tax optimization, wash sale rules, and year-end planning. Inspired by wealth management best practices.

**Core Philosophy:** Taxes are the ONE cost you can control. Every dollar saved in taxes is a dollar working for you.

## Overview:!

Identifies tax-loss harvesting opportunities, manages wash sale constraints, and optimizes year-end tax positioning. Handles: scan → identify → trade → document.

## When to Use

- Year-end tax planning (November-December)
- Portfolio down > 10% (harvest losses)
- Wash sale risk management (30-day windows)
- Rebalancing with tax efficiency
- Tax-alpha generation (defer gains, realize losses)
- Advisor client reporting (wealth management)

## When NOT to Use:!

- Building DCF models (use `financial/model-builder`)
- Pitch deck creation (use `financial/pitch-deck`)
- Trading strategy (use `trading/alphaear-strategy`)
- Portfolio monitoring (use `financial/portfolio-monitor`)

## Implementation:!


The implementation follows a phased approach: scan for loss opportunities, check wash sale rules, execute tax-alpha trades, and document for IRS reporting.


### Phase 1: Opportunity Scan!

**TLH Scan:**
```python
tlh_opportunities = {
    "lot_1": {
        "ticker": "AAPL",
        "purchase_date": "2024-03-15",
        "cost_basis": 180.00,
        "current_price": 142.00,
        "unrealized_loss": -3800,  # $3,800 loss
        "holding_days": 420,
        "wash_sale_safe": True    # > 30 days
    },
    "lot_2": {
        "ticker": "TSLA",
        "purchase_date": "2025-03-20",  # < 30 days ago!
        "cost_basis": 250.00,
        "current_price": 195.00,
        "unrealized_loss": -5500,
        "holding_days": 18,
        "wash_sale_risk": True    # ⚠️ WAIT!
    }
}
```

### Phase 2: Wash Sale Check!

**Wash Sale Rules (30-Day Window):**
```
wash_sale_check = {
    "ticker": "TSLA",
    "sale_date": "2025-04-08",
    "sale_loss": -5500,
    "buy_within_30d": {
        "date": "2025-03-25",  # < 30 days!
        "shares": 100,
        "wash_sale_violation": True  # ⚠️ Cannot claim loss!
        "adjust_cost_basis": True   # Add loss to new basis
    },
    "safe_action": "Wait until 2025-04-24 to repurchase"
}
```

### Phase 3: Tax-Alpha Execution!

**TLH Strategy:**
```
tax_alpha = {
    "realized_losses": {
        "year": 2025,
        "short_term": 15000,  # Ordinary income offset!
        "long_term": 25000,   # Cap gains offset
        "total": 40000
    },
    "defered_gains": {
        "position": "MSFT",
        "gain": 35000,
        "action": "Hold > 1 year for LTCG rates"
    },
    "tax_savings": {
        "marginal_rate": 37%,
        "st_savings": 15000 * 0.37,  # $5,550
        "ltc_savings": 25000 * 0.15,  # $3,750
        "total_saved": 9300
    }
}
```

### Phase 4: Documentation!

**Tax Report:**
```markdown
# Tax-Loss Harvesting Report — 2025 Tax Year

## Summary
| Metric | Value |
|---------|-------|
| Total Losses Realized | $40,000 |
| Tax Savings (Ordinary) | $5,550 |
| Tax Savings (LTCG) | $3,750 |
| Net Tax Savings | $9,300 ✅ |

## Realized Losses
| Ticker | Purchase | Sale | Basis | Proceeds | Loss | Wash Sale? |
|---------|----------|------|-------|----------|-------|-------|-------------|
| AAPL | $180 | $142 | $18K | $14.2K | $3.8K | ✅ Safe |
| GOOGL | $140 | $98 | $14K | $9.8K | $4.2K | ✅ Safe |
| MSFT | $380 | $350 | $38K | $35K | $3K | ⚠️ Wait 15 more days |

## Wash Sale Monitoring
- **TSLA**: Purchased 2025-03-20, DO NOT sell until 2025-04-24
- **MSFT**: Purchased 2025-03-10, DO NOT sell until 2025-04-14
- **Action**: Set calendar reminders for wash sale dates
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Market is up, skip TLH" | Bull markets have losers too — harvest ALL years |
| "Wash sale is just a deferral" | Wash sales can cascade across years = tax trap |
| "Only do TLH in December" | Year-round TLH = 3x more opportunities |
| "Small losses aren't worth it" | $1K loss = $370 tax savings (37% bracket) |

## Red Flags

- Selling with wash sale violation (cannot claim loss!)
- Harvesting > $3K net losses (limitation per year)
- Selling winners to buy losers (terrible tax strategy)
- Not tracking 30-day windows (spreadsheet required!)
- Missing tax documentation (IRS audit risk)
- Harvesting in IRA/401k (no tax benefit!)

## Verification

After completing TLH analysis, confirm:

- [ ] Opportunities scanned: all positions with unrealized losses
- [ ] Wash sale check: 30-day window verified for each trade
- [ ] Tax savings: calculated (ordinary vs. LTCG rates)
- [ ] Documentation: trade date, basis, proceeds, wash status
- [ ] IRS limitts: net losses ≤ $3K/year (excess carries forward)
- [ ] Calendar: 30-day wash sale dates set
- [ ] Report generated: 2-3 pages, tax savings summary
- [ ] Advisor note: sent to client (wealth management)

## Integration Points:!

**Cross-Skill References:**
- `operations/finance-ops` — For tax provisioning
- `financial/portfolio-monitor` — For position tracking
- `trading/alphaear-strategy` — For market timing
- `references/trading-checklist.md` — For tax-trading risk!

**MCP Server Integrations:**
- Alpha Vantage MCP — For real-time prices
- Yahoo Finance MCP — For position tracking
- Morningstar MCP — For tax-efficient fund selection!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
