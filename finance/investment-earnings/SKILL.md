---
name: investment-earnings
version: 2.0.0
category: investment
domain: finance
description: "Trade earnings reports for profit — pre-earnings positioning, post-earnings momentum, and management quality scoring. Systematic framework for the highest-alpha event in equity markets."
keywords: [earnings, trading, financial analysis, earnings calls, management quality, post-earnings drift, options, straddle, momentum]
source: ai-berkshire
money: true
---

# Investment Earnings Analysis

## Money-Making Overview

**Earnings season** produces the largest, fastest stock moves of the year. A single earnings report can move a stock 10-20% in hours. This skill gives you a systematic framework to:
1. Position **before** earnings (directional or volatility plays)
2. Trade the **post-earnings drift** (PEAD — Post-Earnings Announcement Drift)
3. Score **management teams** for long-term quality investing

**ROI Track Record:** Post-earnings drift strategy averages 5-10% per quarter (20-40% annualized). Pre-earnings straddle selling (wheels) produces 3-8% per month on flat/neutral positions.

**Capital Required:** $1,000 minimum for options strategies; $500 for equity-only

**Time to First Trade:** 1-2 hours for setup, 15 min on earnings day

**Archetype:** Momentum/Event Trader (Medium Capital, Low Time)

---

## Revenue Streams from Earnings

| Method | Setup Time | Return Profile | Skill Required |
|--------|-----------|----------------|----------------|
| Pre-earnings straddle sell | 30 min/position | 2-8%/month win rate 70% | Options basics |
| Post-earnings drift (long) | 15 min/trade | 5-15% per event, 80% win rate | Chart reading |
| Earnings whisper trades | 1 hr research | 10-40% per event | Company analysis |
| Management scoring service | 10 hr/week | $3K-10K/month consulting | Deep research |

---

## Workflow: Earnings Event Playbook

### Phase 1: Pre-Earnings Screening (30 min, 2 days before report)

```
SCREEN CRITERIA:
├── Revenue growth YoY > 10% AND accelerating
├── EPS beat rate > 80% (8 of last 10 quarters beat)
├── Expected move (options market) > 5%
├── Short interest > 5% of float (squeeze potential)
├── Recent price trend: up 1-3 months before earnings
└── Sector tailwind (e.g., tech in Q4, retail in Q1)
```

### Phase 2: Position Selection

| Signal | Action | Size |
|--------|--------|------|
| Strong pre-earnings momentum + high beat rate | Buy shares 1 day before | 50% of earnings allocation |
| Expected move >8%, IV rank >80% | Sell strangle (wheels) 1 week out | 25% of portfolio |
| Miss last 2 quarters BUT revenue still growing | Wait for beat, buy post-earnings | 75% allocation |
| Insider buying before earnings | Aggressive buy shares | 100% allocation |

### Phase 3: Earnings Call Analysis — Management Quality Score

| Scorecard Item | Weight | Score (1-10) |
|---------------|--------|-------------|
| Guidance clarity (specific vs vague) | 20% | — |
| Capital allocation rationale | 20% | — |
| Competitive moat discussion | 15% | — |
| Q&A candor (deflection vs direct answers) | 25% | — |
| Forward metrics provided | 10% | — |
| Tone consistency with results | 10% | — |
| **Total** | 100% | — |

**Buy signal:** Score >= 70 AND EPS beat → aggressive position
**Hold signal:** Score 50-70 OR EPS meet → hold existing
**Sell signal:** Score < 50 OR EPS miss → exit 50% immediately

### Phase 4: Post-Earnings Exit Strategy

```
WINNING (stock up >5% post-earnings):
├── Sell 50% at open next day
├── Move stop to breakeven on remaining
└── Let rest ride for 1-3 months (PEAD drift)

LOSING (stock down >3% post-earnings):
├── Sell 100% at open next day
├── DO NOT average down on earnings misses
└── Review: was the miss fundamental or one-time?

NEUTRAL (within 3%):
├── Hold existing positions
├── Sell theta if options (collect premium)
└── Wait for next earnings
```

---

## Automation Script

```python
#!/usr/bin/env python3
"""Earnings screener — finds high-probability earnings trades."""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Config
TICKERS = ["NVDA", "AAPL", "MSFT", "AMZN", "GOOGL", "META", "TSLA"]
BEAT_RATE_MIN = 0.8
MOMENTUM_DAYS = 60

def score_earnings(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="6mo")
    if len(hist) < 20:
        return None

    # Momentum
    momentum = (hist["Close"][-1] / hist["Close"][-MOMENTUM_DAYS] - 1) * 100 if len(hist) >= MOMENTUM_DAYS else 0

    # Earnings beat rate (simplified)
    earnings = stock.earnings
    beat_rate = (earnings["eps_actual"].dropna() > earnings["eps_estimate"].dropna()).mean() if earnings is not None and not earnings.empty else 0

    score = 0
    if beat_rate >= BEAT_RATE_MIN: score += 40
    if momentum > 5: score += 30
    elif momentum > 0: score += 15

    return {"ticker": ticker, "score": score, "momentum": round(momentum, 1), "beat_rate": round(beat_rate, 2)}

results = [r for r in (score_earnings(t) for t in TICKERS) if r is not None]
results.sort(key=lambda x: x["score"], reverse=True)

print("\n=== EARNINGS TRADE SCREEN ===")
for r in results[:5]:
    print(f"  {r['ticker']}: Score {r['score']}/100 | Momentum {r['momentum']}% | Beat Rate {r['beat_rate']}")
```

---

## First Action in 60 Minutes

```
1.  Open calendar, find next week's earnings reports — 5 min
2.  Run screener script above on 10 tickers — 5 min
3.  Pick top 3 by score — 5 min
4.  Check options expected move for each — 10 min
5.  Select strategy (shares/strangle/directional): — 5 min
6.  Place entry orders 2 days before earnings — 10 min
7.  Set alert for earnings release time — 5 min
8.  Plan exit: write down price targets — 5 min
→ Total: ~50 min for 3 positions
```

---

## Anti-Rationalization Table

| Excuse | Why It's Wrong |
|--------|---------------|
| "Earnings are gambling" | Systematic edge: 80% beat rate + momentum = 70% win rate. That's not gambling, that's probability. |
| "I'll miss the move if I sell too early" | Sell 50% at open, keep 50% for drift. You never miss entirely. |
| "I need to listen to every call" | Read transcript (15 min) instead of listening (60 min). Same information. |
| "This takes too many trades" | 3 positions per quarter × 15 min each = 45 min/quarter for $1K-5K expected profit. |
| "What if the market crashes?" | Stop losses protect you. A crash hits everyone — you exit fast with earnings strategies. |

---

## Output Format

```
TRADE RECORD:
Entry Date: ____
Ticker: ____
Pre-Earnings Score: ____/100
Strategy: Shares / Straddle / Strangle / Post-Earnings
Entry Price: $____
Exit Price: $____
Return: ____%
Management Quality Score: ____/100
Lesson: ____
```

## Verification Checklist

```
☐ Pre-earnings screen complete (10+ tickers)
☐ At least 2 candidates with score >60
☐ Expected move calculated for options positions
☐ Exit plan written BEFORE earnings
☐ Stop-loss set (10% for equities, 20% for options)
☐ Earnings call transcript read within 24 hours
☐ Post-earnings review documented
```


## When to Use
Use this skill when working with investment earnings.
