---
name: portfolio-manager
description: Portfolio Manager — BerkahKarya Quant Fund. Use when relevant to this domain.
domain: trading
tags:
- algorithms
- manager
- markets
- portfolio
- trading
---
# Portfolio Manager — BerkahKarya Quant Fund

Managing capital across strategies. Risk first, returns second.

## Current Trading Setup

```
Account: Paper trading (transitioning to live)
Broker:  Ostium (cTrader platform)
Pairs:   XAUUSD primary, future: EURUSD, GBPUSD
Capital: $100 starting (phase 1)
Target:  $528/month = 528% ROI (aggressive, paper verified first)
```

## Strategy Portfolio

Active, planned, and future strategies ranked by readiness and expected return.


### Strategy 1: XAUUSD Asia 7-Candle Breakout (Active)
```
Session:    Asia, 07:00-15:00 UTC+7
Entry:      15:00 UTC+7, breakout of 7-candle range
Win rate:   61.4% (backtested)
Profit PF:  4.1
Risk/trade: 1% account ($1 paper, $10 live phase 1)
Target:     $528/month
Status:     ✅ Strategy ready, paper trading pending
```

### Strategy 2: XAUUSD London Session (Planned)
```
Session:    London open 14:00 UTC+7
Type:       Trend following on breakout of Asian range
Status:     📋 Research phase
```

### Strategy 3: Multi-pair Momentum (Future)
```
Pairs:      EURUSD, GBPUSD, USDJPY
Type:       High timeframe trend + low timeframe entry
Status:     📋 Concept phase
```

---

## Risk Management Framework

Position sizing formulas, maximum drawdown rules, and trade logging format for the quant fund.


### Position Sizing
```python
def calculate_position_size(account_balance, risk_pct=0.01, stop_pips=20):
    """
    Standard position sizing with 1% risk per trade.
    
    account_balance: USD
    risk_pct: 0.01 = 1% risk
    stop_pips: pips to stop loss
    
    Returns: lot size
    """
    risk_amount = account_balance * risk_pct
    pip_value = 10  # $10/pip for 1 standard lot XAUUSD
    lot_size = risk_amount / (stop_pips * pip_value)
    return round(lot_size, 2)

# Example: $1000 account, 1% risk, 20 pip stop
# lot_size = (1000 * 0.01) / (20 * 10) = $10 / $200 = 0.05 lots
```

### Maximum Drawdown Rules
```
Daily DD limit:    3% → STOP trading for the day
Weekly DD limit:   7% → STOP, review strategy
Monthly DD limit:  15% → STOP, report to Paijo, strategy review
Account DD limit:  25% → FULL STOP, return to paper trading
```

### Trade Logging
```python
TRADE_LOG_PATH = ".vilona/knowledge/trading/trading_log.json"

trade_entry = {
    "id": "trade_001",
    "date": "2026-03-13",
    "time": "15:02",
    "pair": "XAUUSD",
    "direction": "BUY",
    "entry": 2650.50,
    "stop_loss": 2649.50,   # 10 pip stop
    "take_profit": 2652.50,  # 20 pip TP (1:2 RR)
    "lot_size": 0.01,
    "risk_usd": 1.00,
    "strategy": "asia_7c_breakout",
    "session": "asia",
    "candle_range_pips": 8.5,
    "outcome": "WIN",
    "pnl_usd": 2.00,
    "duration_min": 45,
    "notes": "Clean breakout, held to TP"
}
```

---

## Performance Analytics

Monthly performance reports and phase gate criteria for progression from paper to live to scaled trading.


### Monthly Performance Report
```
╔══════════════════════════════════════════╗
║     QUANT FUND MONTHLY REPORT            ║
║     {month} {year}                       ║
╠══════════════════════════════════════════╣
║ Starting Balance: ${start}               ║
║ Ending Balance:   ${end}                 ║
║ Net P&L:          ${pnl} ({pct}%)       ║
╠══════════════════════════════════════════╣
║ TRADE STATS                              ║
║ Total trades:    {total}                 ║
║ Win rate:        {wr}%                   ║
║ Profit factor:   {pf}                    ║
║ Avg win:         ${avg_win}              ║
║ Avg loss:        ${avg_loss}             ║
║ Best trade:      ${best}                 ║
║ Worst trade:     ${worst}                ║
╠══════════════════════════════════════════╣
║ RISK METRICS                             ║
║ Max daily DD:    {max_dd}%               ║
║ Sharpe ratio:    {sharpe}                ║
║ Recovery factor: {rf}                    ║
╚══════════════════════════════════════════╝
```

### Phase Gates (Paper → Live → Scale)
```
Phase 1: Paper Trading
  □ 30 trades completed
  □ Win rate ≥55% over 30 trades
  □ Max DD <15% of paper account
  □ Profit factor ≥1.5
  → PASS: Move to Phase 2

Phase 2: Live Trading ($100)
  □ 30 live trades
  □ Win rate ≥55%
  □ Profitable month (net positive)
  □ Following risk rules strictly
  → PASS: Double capital ($200)

Phase 3: Scaling
  □ 3 consecutive profitable months
  □ Each month: double previous capital
  □ Max $10,000 per strategy
  
Phase 4: Quant Fund
  □ $50K+ AUM
  □ External investors
  □ Monthly investor reports
  □ Audited track record
```

---

## Investor Reporting (Future)

When BerkahKarya Quant Fund accepts external capital:
- Monthly P&L report (this template)
- Quarterly strategy review
- Risk disclosure document
- Track record (audited)
- Monthly Sharpe ratio, drawdown stats


## When to Use

- Managing capital allocation across multiple trading strategies
- Tracking performance metrics (IRR, MOIC, Sharpe, win rate) for a quant fund
- Implementing phase gates for progression from paper to live to scaled trading
- Calculating position sizes with risk-based formulas
- Generating investor reports for fund performance review

## Red Flags

- Position sizing exceeds 1% risk per trade without override justification
- Drawdown exceeds daily 3% limit without automatic trading halt
- Win rate below 55% after 30+ trades (strategy underperforming)
- Moving from paper to live without meeting all phase gate criteria
- No trade log maintained (missing audit trail for performance review)

## Verification

After completing portfolio management setup, confirm:

- [ ] Position sizing formula tested with known account balances and risk percentages
- [ ] Drawdown limits configured: daily 3%, weekly 7%, monthly 15%, account 25%
- [ ] Trade log format captures all required fields (entry, SL, TP, P&L, strategy)
- [ ] Phase gate criteria documented and measurable (30 trades, 55% WR, PF 1.5)
- [ ] Monthly report template generates correct P&L, Sharpe, and drawdown stats

---

## Integration
```
portfolio-manager → trading/strategy/xauusd_asia_7c_breakout (signals)
                 → finance-tracker (P&L reporting)
                 → telegram-userbot (trade alerts, daily P&L)
                 → business-intelligence (quant fund KPIs)
```

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
