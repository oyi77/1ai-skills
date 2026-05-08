# Financial Services Index

Map financial skills to the workflows from [anthropics/financial-services](https://github.com/anthropics/financial-services). Use this to find the right skill for each financial workflow.

## 📊 Core Financial Analysis (Compare to `financial-analysis` plugin)

| Skill | Category | Compared to anthropics/financial-services |
|-------|----------|-----------------------------------------------|
| `trading/black-edge` | trading | Alternative data synthesis (satellite, web scraping, credit cards) — similar to their data connectors but more "gray edge" |
| `trading/alphaear-strategy` | trading | Multi-signal: news + sentiment + options flow — similar to `market-researcher` + `earnings-reviewer` |
| `trading/trading/polymarket-api` | trading | Prediction market API — matches their `earnings-reviewer` (probability analysis) |
| `trading/trading/polymarket-weather-trader` | trading | Weather derivatives via prediction markets |
| `trading/trading/tushare-finance` | trading | Python financial data library — similar to their S&P Capital IQ connector |
| `operations/finance-ops` | operations | CFO dashboard, unit economics, cost intelligence — similar to `gl-reconciler` + `month-end-closer` |
| `sales/high-ticket-closing` | sales | Investment committee pitch — matches their `pitch-agent` |
| `marketing/stripe-revenue-bot` | marketing | Revenue tracking — similar to their `valuation-reviewer` |

## 🔨 Investment Banking (Compare to `investment-banking` plugin)

| Skill | anthropics Equivalent | What's Missing |
|-------|----------------------|----------------|
| `sales/high-ticket-closing` | `pitch-agent` (pitch deck, CIM, teaser) | No `/one-pager`, `/pitch-deck`, `/cim` commands |
| `sales/business-development` | `kyc-screener` (KYC, onboarding) | No KYC document parser |
| `trading/alphaear-strategy` | `market-researcher` (sector overview, comps) | No `/sector`, `/screen` commands |

## 🏦 Private Equity (Compare to `private-equity` plugin)

| Skill | anthropics Equivalent | What's Missing |
|-------|----------------------|----------------|
| `trading/black-edge` | `deal-sourcing` (sourcing, screening) | No `/source`, `/screen-deal` commands |
| `trading/alphaear-strategy` | `dd-meeting-prep` (management meetings) | No `/dd-checklist`, `/ic-memo` commands |
| `operations/finance-ops` | `portfolio-monitoring` (KPIs, returns) | No `/portfolio`, `/returns` commands |

## 💰 Wealth Management (Compare to `wealth-management` plugin)

| Skill | anthropics Equivalent | What's Missing |
|-------|----------------------|----------------|
| `operations/finance-ops` | `client-review`, `financial-plan` | No `/client-review`, `/financial-plan` commands |
| `sales/high-ticket-closing` | `investment-proposal`, `client-report` | No `/proposal`, `/client-report` commands |
| `trading/trading/tushare-finance` | `portfolio-rebalance` | No `/rebalance`, `/tax-loss-harvesting` commands |

## 💼 MCP Server Integrations (Compare to `financial-analysis/.mcp.json`)

**anthropics has 11 data connectors:**
- Daloopa, Morningstar, S&P Global, FactSet, Moody's, MT Newswires, Aiera, LSEG, PitchBook, Chronograph, Egnyte

**1ai-skills currently has:** None configured!

### Recommended Additions:
```json
{
  "mcpServers": {
    "alpha-vantage": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-alpha-vantage"],
      "env": { "ALPHA_VANTAGE_API_KEY": "your-key" }
    },
    "yahoo-finance": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-yahoo-finance"]
    },
    "polymarket": {
      "url": "https://gamma-api.polymarket.com/"
    }
  }
}
```

## 📋 Recommended New Skills (Gap Analysis)

Based on comparison with anthropics/financial-services:

### High Priority (Missing Core Workflows)
1. **`financial/earnings-reviewer`** — Earnings call + filings → model update → note draft (like their `earnings-reviewer`)
2. **`financial/model-builder`** — DCF, LBO, 3-statement models (like their `model-builder`)
3. **`financial/pitch-deck`** — Populate pitch deck templates (like their `pitch-agent`)
4. **`financial/kyc-screener`** — Parse onboarding docs, run rules engine (like their `kyc-screener`)

### Medium Priority
5. **`financial/gl-reconciler`** — Find breaks, trace root cause (like their `gl-reconciler`)
6. **`financial/month-end-closer`** — Accruals, roll-forwards, variance commentary
7. **`financial/statement-auditor`** — Audit LP statements (like their `statement-auditor`)
8. **`financial/valuation-reviewer`** — Ingest GP packages, run valuation template

### Low Priority (Nice to Have)
9. **`financial/meeting-prep`** — Briefing pack before client meetings
10. **`financial/portfolio-monitor`** — Track portfolio KPIs, variances
11. **`financial/tax-loss-harvesting`** — Identify TLH opportunities
12. **`financial/ai-readiness`** — Assess portfolio company AI readiness

## 🔗 Cross-Reference by Workflow

### "Analyze earnings"
→ `trading/alphaear-strategy` (news + sentiment + options)
→ *Missing: dedicated earnings-reviewer skill*

### "Build DCF model"
→ *Missing!* Need `financial/model-builder`

### "Source deals"
→ `trading/black-edge` (alternative data)
→ *Missing: dedicated deal-sourcing skill*

### "Pitch to investors"
→ `sales/high-ticket-closing`
→ *Missing: `/pitch-deck` command*

### "Reconcile GL"
→ `operations/finance-ops` (cost intelligence)
→ *Missing: dedicated GL reconciler*

### "Screen companies"
→ `trading/alphaear-strategy` (multi-signal)
→ *Missing: `/screen` command*

---

## 📚 References

- [anthropics/financial-services](https://github.com/anthropics/financial-services) — Full repo
- [financial-analysis plugin](https://github.com/anthropics/financial-services/tree/master/plugins/vertical-plugins/financial-analysis) — 11 MCP connectors
- [investment-banking plugin](https://github.com/anthropics/financial-services/tree/master/plugins/vertical-plugins/investment-banking) — Pitch deck, CIM, teaser
- [private-equity plugin](https://github.com/anthropics/financial-services/tree/master/plugins/vertical-plugins/private-equity) — Deal sourcing, IC memo
- [wealth-management plugin](https://github.com/anthropics/financial-services/tree/master/plugins/vertical-plugins/wealth-management) — Client review, rebalancing

---

**Note:** 1ai-skills has more "edge" and "alternative data" focus (black-edge, alphaear) while anthropics focuses on institutional workflows (pitch decks, models, reconciliations). Consider adding the missing institutional workflows.
