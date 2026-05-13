# fin-options-derivatives: Options, Futures, and Swaps

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` for position sizing with leverage. Greek exposure requires strict stop-loss.

## Derivatives Universe

| Instrument | Leverage | Liquidity | Complexity | Use Case |
|------------|----------|-----------|------------|----------|
| **Equity Options** (Calls/Puts) | 10–50× | Excellent | Medium | Directional, income, hedging |
| **Index Options** (SPX, NDX) | 50–100× | Excellent | Medium | Portfolio hedge, direction |
| **Futures** (ES, NQ, CL) | 10–20× | Excellent | Low–Medium | Direction, spread trades |
| **Options on Futures** | 50–200× | Good | High | Leveraged direction + time decay |
| **Swaps** (IRS, CDS) | Variable | OTC | High | Institutional hedging |
| **Structured Products** | Variable | Poor | Very High | Yield enhancement (with caveats) |

---

## The Greeks (Options Sensitivity)

### Delta (Δ) — Direction
- **Definition**: Change in option price per $1 change in underlying
- **Call Delta**: 0 to +1.0 (ITM → +1.0, OTM → 0)
- **Put Delta**: –1.0 to 0 (ITM → –1.0, OTM → 0)
- **Delta 50 (ATM)**: ~0.50 for calls, –0.50 for puts
- **Delta hedging**: Buy/sell underlying to neutralize directional risk

### Gamma (Γ) — Delta Acceleration
- **Definition**: Change in Delta per $1 change in underlying
- **Highest Gamma**: ATM options near expiration (delta swings wildly)
- **Gamma risk**: Short gamma = unlimited risk (delta blows out)
- **Gamma scalping**: Long gamma strategy, delta-hedge to capture vol

### Theta (Θ) — Time Decay
- **Definition**: Option price erosion per day (always negative for longs)
- **Theta acceleration**: Exponential decay last 30 days
- **Theta strategies**: Sell options (covered call, iron condor) to collect decay
- **Negative theta**: Long options lose money if underlying stays flat

### Vega (ν) — Volatility Sensitivity
- **Definition**: Change in option price per 1% change in implied vol
- **High Vega**: Long-dated options, OTM options
- **Vol crush**: Post-earnings, post-news — implied vol drops → option price drops
- **Vega neutral**: Buy + sell options to hedge vol exposure

### Rho (ρ) — Interest Rate Sensitivity
- **Definition**: Change in option price per 1% change in risk-free rate
- **Relevance**: Mostly for long-dated options (LEAPS)
- **Call Rho**: Positive (higher rates → higher call prices)
- **Put Rho**: Negative (higher rates → lower put prices)

---

## Implied Volatility (IV) & VIX

### IV Rank vs. IV Percentile
- **IV Rank**: Current IV vs. 52-week high/low (0–100 scale)
- **IV Percentile**: % of days IV was lower over past year (0–100%)
- **High IV Rank (>80)**: Sell premium (high prob of profit)
- **Low IV Rank (<20)**: Buy options (cheap, direction play)

### VIX (Volatility Index) Interpretation

| VIX Level | Market Condition | Strategy |
|-----------|------------------|----------|
| <12 | Very low vol (complacency) | Buy SPX puts (cheap hedge) |
| 12–16 | Low vol (normal) | Sell premium (iron condor) |
| 16–20 | Moderate vol | Delta-neutral strategies |
| 20–30 | Elevated vol (stress) | Reduce size, buy protection |
| 30–40 | High vol (crisis) | Long vol (VXX, put spreads) |
| >40 | Extreme vol (panic) | Capitulation → contrarian long |

### Volatility Surface & Skew
- **25-Delta Put Skew**: Institutional demand for downside protection (negative skew)
- **25-Delta Call Skew**: Upside demand (positive skew, rare)
- **Term structure**: Short-term IV vs. long-term IV (contango/backwardation)
- **Smile/Smirk**: OTM puts cost more than ATM (tail risk premium)

---

## Option Strategies (Directional)

### Long Call (Bullish)
- **Setup**: Buy call, strike near ATM
- **Max Loss**: Premium paid (100%)
- **Max Gain**: Unlimited (underlying → ∞)
- **Breakeven**: Strike + Premium
- **When to use**: High conviction, low IV, earnings catalyst

### Long Put (Bearish)
- **Setup**: Buy put, strike near ATM
- **Max Loss**: Premium paid (100%)
- **Max Gain**: Strike – Premium (underlying → $0)
- **Breakeven**: Strike – Premium
- **When to use**: Crash protection, bearish on stock/sector

### Bull Call Spread
- **Setup**: Buy lower strike call, sell higher strike call
- **Max Loss**: Net debit paid
- **Max Gain**: (Strike2 – Strike1) – Net Debit
- **Breakeven**: Lower Strike + Net Debit
- **When to use**: Moderate bullish, reduce cost basis

### Bear Put Spread
- **Setup**: Buy higher strike put, sell lower strike put
- **Max Loss**: Net debit paid
- **Max Gain**: (Strike1 – Strike2) – Net Debit
- **Breakeven**: Higher Strike – Net Debit
- **When to use**: Moderate bearish, define risk

---

## Option Strategies (Income/Neutral)

### Covered Call
- **Setup**: Long 100 shares + sell call against
- **Max Gain**: (Strike – Stock Cost) + Premium
- **Max Loss**: Stock → $0 minus premium (still equity risk)
- **When to use**: Neutral to slightly bullish, willing to sell at strike

### Cash-Secured Put
- **Setup**: Sell put, cash reserved to buy shares
- **Max Gain**: Premium received
- **Max Loss**: (Strike – Premium) if stock → $0
- **When to use**: Want to buy stock at discount, bullish

### Iron Condor
- **Setup**: Sell OTM put spread + sell OTM call spread
- **Max Gain**: Net credit received
- **Max Loss**: Width of spread – net credit
- **When to use**: Neutral market, high IV environment

### Straddle (Long Volatility)
- **Setup**: Buy ATM call + buy ATM put
- **Max Loss**: Total premium paid
- **Max Gain**: Unlimited (big move either direction)
- **Breakeven**: Strike ± Total Premium
- **When to use**: Earnings, events with binary outcome

---

## Futures Trading

### Contract Specifications
| Contract | Underlying | Tick Size | Tick Value | Margin (initial) |
|----------|------------|-----------|------------|-------------------|
| **ES** (E-mini S&P) | S&P 500 | 0.25 pts | $12.50 | ~$12k |
| **NQ** (E-mini NASDAQ) | NASDAQ 100 | 0.25 pts | $5.00 | ~$15k |
| **CL** (Crude Oil) | WTI Crude | 0.01 pts | $10.00 | ~$6k |
| **GC** (Gold) | Gold 100oz | 0.10 pts | $10.00 | ~$8k |
| **ZB** (30y Bond) | T-Bond | 1/32 pt | $31.25 | ~$5k |

### Futures Strategies
- **Trend Following**: 50/200 MA crossover, momentum signals
- **Mean Reversion**: RSI <30 buy, >70 sell (range-bound markets)
- **Spread Trading**: Long one contract, short related (CL calendar, ES/NQ spread)
- **Roll Yield**: In contango (sell near, buy far); backwardation (buy near, sell far)

---

## Risk Management for Derivatives

### Leverage Limits
- **Retail**: Max 2× notional of account (e.g., $10k account → $20k notional)
- **Professional**: Max 5× notional, strict stop-loss at 2% account risk
- **Stop-Loss Rules**:
  - Options: Close at 50% max loss (premium decay accelerates)
  - Futures: 1.5× ATR stop, or 2% account risk per contract
  - Spreads: Close at 2× credit received (max loss approaching)

### Greek Risk Limits
- **Delta**: Net portfolio delta < 20% of account (direction limit)
- **Gamma**: Short gamma positions < 5% of account (explosion risk)
- **Theta**: Negative theta < –2% account/day (bleed check)
- **Vega**: Net vega < 10% account/vol point (vol risk)

---

## Output Template: Options Trade

```
TRADE: [BUY/SELL] [CALL/PUT] [TICKER] [EXPIRY] $[STRIKE]
DATE: [YYYY-MM-DD]
STRATEGY: [Long Call / Iron Condor / etc.]
NET DEBIT/CREDIT: $[amount] | CONTRACTS: [n]

GREEKS (per contract):
  Delta: [Δ] | Gamma: [Γ] | Theta: [Θ] | Vega: [ν]
  Net Portfolio Greeks: Δ=[x] Γ=[x] Θ=[x] ν=[x]

IMPLIED VOL:
  Current IV: [%] | IV Rank: [%] | IV Percentile: [%]
  IV vs. 30d avg: [+/-][%] (cheap/expensive)

BREAKEVEN: $[price] (underlying must reach)
MAX LOSS: $[amount] ([%] of position)
MAX GAIN: [unlimited / $X]

TRIGGER TO ENTER: [underlying >$X, IV <20%, etc.]
STOP LOSS: Close at $[price] or [X%] loss
PROFIT TARGET: Take 50% at $[price], let rest run

RISK GATES:
  Liquidity: Open Interest >[1000], Bid-Ask <[5%] → PASS
  Leverage: [X]× notional vs. account → WITHIN LIMIT
  Greeks: Net delta [x]% account → WITHIN LIMIT
  Volatility: IV Rank [x] → SUITABLE for strategy

GATE VERDICT: FULL / REDUCED / SKIP
POSITION SIZE: [X] contracts = $[notional] ([Y%] account)
```

---

## Red Flags — STOP and Review

- IV Rank >80 but buying options (should sell premium instead)
- Short gamma >5% account (unlimited risk if market moves)
- Theta bleed >2% account/day (bleeding to time decay)
- Futures leverage >10× account (liquidation risk)
- Straddle before earnings with IV >90th percentile (vol crush)
- Selling naked calls/puts (unlimited risk)
- Holding options through expiration without exercise plan

**All of these mean: Re-run risk gates. Reduce size or SKIP.**
