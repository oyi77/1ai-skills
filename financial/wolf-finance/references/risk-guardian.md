# fin-risk-guardian: Position Sizing & Portfolio Risk Management

**REQUIRED SUB-SKILL:** Load `macro-liquidity.md` for correlation context. Markets correlate in stress.

## Pre-Trade 5-Gate Legitimacy Check

Run ALL 5 gates before ANY actionable recommendation. Document result for audit trail.

---

### Gate 1: Liquidity Check
- **Daily volume ≥ 10× intended position size?** If not → REDUCED
- **Bid-ask spread < 0.5%** (equities) / **< 0.1%** (crypto large-cap)? If not → flag slippage
- **Market cap check**:
  - >$1B = FULL position eligible
  - $100M–$1B = REDUCED (half size)
  - <$100M = SKIP (liquidity risk too high)

### Gate 2: Correlation Check
- **Portfolio correlation**: Pearson 90d rolling vs. existing positions
  - Correlation >0.7 with >20% of portfolio → REDUCED (concentration risk)
  - Correlation >0.8 with >30% of portfolio → SKIP (over-concentrated)
- **Sector concentration**: No more than 30% in one sector at full Kelly
- **Factor exposure**: Check value/growth, large/small cap balance

### Gate 3: Sentiment Alignment
- **Fear & Greed Index**:
  - >80 (Extreme Greed): No new long entries at full size → REDUCED
  - <15 (Extreme Fear): Contrarian longs valid, new shorts → SKIP
  - 15–30 (Fear): Selective longs with wide stops → REDUCED
- **Momentum alignment**: Entry in direction of 20-day trend preferred
- **VIX regime**: >25 = reduce size by 50%, >35 = SKIP all new trades

### Gate 4: Memory Recall (OWM Query)
- **Query**: "What happened last time in similar macro + sentiment conditions?"
- **Negative precedents**: 3+ similar setups with negative outcome → REDUCED
- **Behavioral drift**: Overtrading, revenge trading detected → SKIP until reviewed
- **Recent losses**: >3 consecutive losses → reduce size by 50%, review strategy

### Gate 5: Regulatory Check
- **Jurisdiction compliance**: Is asset available in user's declared jurisdiction?
- **US**: SEC/CFTC status; unregistered securities (check Howey test)
- **EU**: MiFID II appropriateness; ESMA leverage limits (30:1 for majors)
- **UK**: FCA regulations; crypto promotions compliance
- **Asia**: MAS (Singapore), OJK (Indonesia), JFSA (Japan) — check registered exchanges
- **Sanctions**: OFAC SDN list check for crypto wallets

**Gate Output**: `FULL` (all clear) / `REDUCED` (1–2 gates amber) / `SKIP` (any gate red)

---

## Position Sizing Models

### Method 1: Fixed Fractional (Recommended for Retail)
```
Position Size ($) = Account Size × Risk % ÷ (Entry Price – Stop Loss Price)

Conservative: Risk 0.5–1% per trade (account protection)
Moderate: Risk 1–2% per trade (balanced growth)
Aggressive: Risk 2–3% per trade (never exceed 3%)
```

### Method 2: Kelly Criterion (Systematic Traders with Edge Data)
```
f* = (b × p – q) / b
  b = net odds (reward/risk ratio)
  p = probability of winning (from 30+ historical trades)
  q = 1 – p

Practical Rule: Use HALF-KELLY (f*/2) to reduce variance
Never apply Kelly without minimum 30 historical trades for p estimation
```

### Method 3: Volatility-Adjusted Sizing (ATR-Based)
```
Position Size = (Account Risk $) ÷ (ATR × ATR Multiplier)

ATR Multiplier:
  Conservative = 2.0 (wider stop, smaller size)
  Moderate = 1.5 (balanced)
  Aggressive = 1.0 (tight stop, larger size)
```

### Method 4: Equal Risk Contribution (Portfolio Level)
```
Each position risk = Account × (Risk % / Number of Positions)
Example: $100k account, 2% risk, 5 positions → $400 risk each
Adjust position size so stop-loss loss = $400 per position
```

### Method 5: Optimal f (Advanced — Expectancy Model)
```
f = ( (P × W) – L ) / W
  P = win probability
  W = average win $
  L = average loss $ (positive number)

Warning: Optimal f overestimates risk in real markets. Use 25% of f.
```

---

## Portfolio-Level Risk Rules

| Rule | Conservative | Moderate | Aggressive |
|------|-------------|---------|-----------|
| Max single position | 3% | 5% | 8% |
| Max sector concentration | 15% | 25% | 35% |
| Max correlated cluster | 20% | 30% | 40% |
| Max leverage (gross exposure) | 1.0× (no leverage) | 1.5× | 2.0× |
| Portfolio daily stop | –1% | –2% | –3% |
| Portfolio drawdown circuit breaker | –8% → reduce 50% | –12% → reduce 50% | –15% → reduce 50% |
| Max crypto allocation | 5% | 15% | 25% |
| Max illiquid (<$1M/day) | 2% | 5% | 10% |

---

## Value at Risk (VaR) & Expected Shortfall

### Parametric VaR (95%, 1-Day)
```
VaR = Z-score × Portfolio Value × σ (daily volatility)
95% Z-score = 1.645
99% Z-score = 2.326

Example: $100k portfolio, σ=1.5%/day → 95% VaR = $2,467
```

### Historical VaR (Non-Parametric)
- Sort all daily P&L from worst to best
- 95th percentile loss = 95% VaR
- Captures fat tails, non-normal distributions

### Expected Shortfall (CVaR)
- Average loss BEYOND VaR threshold
- More conservative: "If we're in the 5% worst days, avg loss is..."
- Example: 95% VaR = $2,467, CVaR = $3,850

### Portfolio VaR with Correlation
```
Portfolio Variance = Σ (wi² × σi²) + Σ (2 × wi × wj × ρij × σi × σj)
VaR = Z-score × sqrt(Portfolio Variance)
```

---

## Drawdown Management

### Losing Streak Protocol
- **3 consecutive losses**: Reduce position size by 25%, review setup
- **5 consecutive losses**: Reduce position size by 50%, mandatory strategy review
- **7 consecutive losses**: SKIP all new trades; full behavioral audit required

### Portfolio Drawdown Alerts
- **–5% from peak**: Review open positions; tighten stops to breakeven
- **–10% from peak**: Cut risk by 50%; no new entries until recovery
- **–15% from peak**: Emergency close all speculative positions
- **–20% from peak**: Capital preservation mode only (cash/T-bills)

### Recovery Rules
- After –10% drawdown: Need +11.1% to recover
- After –20% drawdown: Need +25% to recover
- After –50% drawdown: Need +100% to recover (near impossible with same risk)
- **Rule**: Reduce risk faster than you increase it

---

## Stress Testing Framework

Before large position or portfolio allocation:

### 1. Single Asset Shock
- What if this asset drops 30% tomorrow? Portfolio impact?
- What if it drops 50%? Can you hold or forced to sell?

### 2. Correlation Shock (Market Crash)
- What if ALL risky assets drop 20% simultaneously?
- Correlation → 1.0 in crisis; diversification fails
- Hedge with uncorrelated assets (T-bills, gold, long vol)

### 3. Liquidity Shock
- Can you exit 100% of position within 3 days at <2% slippage?
- Scenario: Market closes for 2 days (circuit breakers), then gaps -15%

### 4. Margin Call Scenario (If Using Leverage)
- At what price level does margin call trigger?
- How much additional capital needed to avoid liquidation?
- Set stop-loss BEFORE margin call price

### 5. Tail Risk (Black Swan)
- Max historical drawdown of this asset in bear markets
- What if 2008-style crash (–50% equity, –70% crypto)?
- Portfolio insurance: Put options, VIX calls, inverse ETFs

---

## Portfolio Optimization (Modern Portfolio Theory)

### Efficient Frontier
```
Minimize: σp² = Σ wi²σi² + Σ 2wiwjρijσiσj
Subject to: Σ wi = 1, Σ wi × E(Ri) = Target Return

Output: Optimal weights for each asset class
```

### Risk Parity (Equal Risk Contribution)
- Allocate so each asset contributes EQUAL risk to portfolio
- Usually: More bonds, less equity (bonds less volatile per $)
- Leverage up low-risk assets to match portfolio volatility

### Kelly Optimal Portfolio (Multiple Assets)
```
f* = inverse(Covariance Matrix) × Expected Returns
Then: Use Half-Kelly for each asset

Warning: Kelly portfolios can be 100% in best asset (concentrated)
```

---

## Risk Guardian Output Template

```
TRADE PROPOSAL: [$TICKER] | [BUY/SELL] | [LONG/SHORT]
DATE: [YYYY-MM-DD] | ACCOUNT: $[balance] | RISK PROFILE: [Conservative/Moderate/Aggressive]

GATE RESULTS:
  Gate 1 Liquidity: [PASS/AMBER/FAIL]
    Daily Volume: $[X] vs. position $[Y] (ratio: [Z]×) → [note]
    Spread: [%] → [acceptable/high]
    Market Cap: $[X] → [FULL/REDUCED/SKIP]
  
  Gate 2 Correlation: [PASS/AMBER/FAIL]
    90d correlation vs. portfolio: [r] → [note]
    Sector exposure after entry: [%] → [note]
  
  Gate 3 Sentiment: [PASS/AMBER/FAIL]
    Fear & Greed: [score] → [zone]
    20d momentum: [%] → [aligned/against]
    VIX: [level] → [normal/elevated/crisis]
  
  Gate 4 Memory: [PASS/AMBER/FAIL]
    Similar setups past 2y: [n] (win rate: [%])
    Recent losing streak: [n] → [reduce size?]
  
  Gate 5 Regulatory: [PASS/AMBER/FAIL]
    Jurisdiction: [US/EU/UK/Asia] → [allowed/restricted]
    OFAC check: [clean/flagged]

GATE VERDICT: FULL / REDUCED / SKIP

POSITION SIZING:
  Method: [Fixed Fractional/Kelly/Volatility-Adjusted/Equal Risk]
  Account Risk: [%] = $[amount]
  Entry: $[price] | Stop: $[price] (structural/ATR-based)
  Position Size: [X shares/contracts/coins] = $[notional]
  % of Account: [%] (limit: [%] for profile)

PORTFOLIO IMPACT:
  New position weight: [%]
  Sector exposure after: [%] (limit: [%])
  Portfolio correlation change: [+/-]
  New Portfolio VaR (95%, 1d): $[amount] ([%])

STRESS TEST:
  –30% scenario: portfolio impact = –$[X] ([%])
  –50% scenario: portfolio impact = –$[X] ([%])
  Correlation shock (all –20%): impact = –$[X] ([%])
  Recovery needed: [%] to break even

BEHAVIORAL CHECK:
  Overtrading: [Y/N] (3+ trades/day = flag)
  Revenge trading: [Y/N] (increasing size after loss = flag)
  FOMO: [Y/N] (entering after +10% move = flag)
```

---

## Red Flags — STOP and Re-Run Gates

- Position size >8% (moderate) or >12% (aggressive) without FULL gates
- Correlation >0.7 with >30% of portfolio but proceeding anyway
- Fear & Greed >85 but "this time is different" (buying anyway)
- 5+ consecutive losses but not reducing size (revenge trading)
- Portfolio down –10% but adding risk (doubling down)
- Using leverage >2× when VIX >30 (margin call risk)
- Crypto allocation >25% in conservative profile
- Skipping Gate 4 (memory) because "this setup is unique"

**All of these mean: STOP. Re-run all 5 gates. Reduce size or SKIP entirely.**
