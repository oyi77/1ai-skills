# fin-algo-execution: Algorithmic Trading & Execution

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` for position sizing and max drawdown enforcement.

## Execution Algorithms

### VWAP (Volume Weighted Average Price)
- **Objective**: Execute order at price matching VWAP benchmark
- **Mechanism**: Slice order to match market volume profile (open 15%, close 15%, mid 70%)
- **Best for**: Large orders, liquid equities, no urgency
- **Risk**: Adverse selection if stock trends away from VWAP

### TWAP (Time Weighted Average Price)
- **Objective**: Execute order evenly over time (ignore volume)
- **Mechanism**: Fixed slices every N minutes (e.g., 100 shares/5min for 6.5 hours)
- **Best for**: Predictable volume, less liquidity concern
- **Risk**: Executing during heavy volume spikes (buy at highs, sell at lows)

### POV (Percentage of Volume)
- **Objective**: Participate at fixed % of market volume (e.g., 10% POV)
- **Mechanism**: Dynamically adjust order size based on real-time volume
- **Best for**: Large orders needing discretion, adapting to volume
- **Risk**: Detected by HFT if POV >15% (information leakage)

### Implementation Shortfall (IS)
- **Objective**: Minimize difference between arrival price and execution price
- **Mechanism**: Aggressive immediate + passive limit orders (dynamic mix)
- **Best for**: Urgent orders, momentum trades, news events
- **Risk**: Market impact if too aggressive; opportunity cost if too passive

### Dark Pool / Iceberg
- **Objective**: Hide order size from public order book
- **Mechanism**: Route to dark pools (no pre-trade transparency)
- **Best for**: Block trades >$1M notional, minimizing market impact
- **Risk**: No price improvement guarantee, execution uncertainty

---

## Order Types & When to Use

| Order Type | Fill Certainty | Price Control | Slippage Risk | Use Case |
|------------|----------------|--------------|---------------|----------|
| **Market** | 100% | None | High | Urgent exit, liquid assets only |
| **Limit** | Low | Full | None | Patient entry, specific price |
| **Stop Market** | Triggered | None | High | Stop-loss, forced exit |
| **Stop Limit** | Triggered | Full | Varies | Stop-loss with price floor |
| **Trailing Stop** | Triggered | Dynamic | Varies | Lock in gains, let winners run |
| **Iceberg** | Medium | Good | Low | Large orders, hide size |
| **Fill-or-Kill (FOK)** | Binary | Full | None | All or nothing, no partial fills |
| **Immediate-or-Cancel (IOC)** | Partial | Full | Low | Fill what you can, cancel rest |

---

## Market Impact Models

### Temporary Impact (Immediate)
```
Impact = η × (Order Size / Daily Volume) ^ 0.5
η (eta) ≈ 0.1–0.3 for liquid large-cap
Higher for small-cap, crypto (η ≈ 0.5–1.0)
```

### Permanent Impact (Information Leakage)
```
Permanent = γ × (Order Size / Market Cap)
γ (gamma) ≈ 0.01–0.05 for liquid assets
HFT detects large POV >15% → prices move against you
```

### Slippage Estimation
- **Expected Slippage** = (Bid-Ask Spread / 2) + Market Impact
- **Example**: Spread = 0.02%, Impact = 0.15% → Total = 0.17% cost
- **Crypto**: Add 0.1–0.5% for large-cap, 0.5–2% for small-cap

---

## Advanced Execution: Optimal Splitting

### Almgren-Chriss Model (Optimal Execution Horizon)
```
Minimize: Total Cost = Execution Cost + Risk Penalty
Execution Cost = Impact × Shares × Price
Risk Penalty = λ × Volatility × sqrt(Shares × Time)

Output: Optimal trading rate (not too fast, not too slow)
```

### Key Parameters
- **Volatility (σ)**: Higher vol → slower execution (risk penalty dominates)
- **Risk aversion (λ)**: Higher λ → faster execution (fear of holding risk)
- **Market impact (η)**: Higher impact → slower execution (minimize cost)

---

## Crypto-Specific Execution

### DEX vs. CEX Routing
- **CEX (Binance, Coinbase)**: Lower fees, higher liquidity, KYC required
- **DEX (Uniswap, Jupiter)**: No KYC, slippage tolerance, MEV risk
- **Aggregators (1inch, Jupiter)**: Route across multiple pools for best price

### MEV (Maximal Extractable Value) Protection
- **Private mempools**: Flashbots (ETH), Jito (SOL) — avoid front-running
- **Slippage tolerance**: Set 0.5–1% for large trades, 0.1% for small
- **Deadline**: Set transaction deadline (5–10 min) to avoid stale quotes

### Cross-Exchange Arbitrage
- **Triangular arbitrage**: BTC→ETH→USDT→BTC (capture price diffs)
- **Spatial arbitrage**: Buy on Binance, sell on Coinbase (price differential)
- **Funding arbitrage**: Long spot, short perp (capture funding rate)

---

## Transaction Cost Analysis (TCA)

### Benchmark Comparison
| Benchmark | When to Use | Pros | Cons |
|-----------|--------------|------|------|
| **Arrival Price** | Measuring implementation shortfall | Standard for IS algos | Ignores market movement |
| **VWAP** | Large, passive orders | Industry standard | Penalizes trading with trend |
| **TWAP** | Time-sensitive execution | Simple, predictable | Ignores volume patterns |
| **Close Price** | End-of-day execution | Easy to compute | High variance for intraday |

### TCA Metrics
- **Implementation Shortfall** = (Exec Price – Arrival Price) / Arrival Price
- **Market Impact** = (Exec Price – Benchmark) / Benchmark (for first fills)
- **Opportunity Cost** = (Final Price – Exec Price) / Exec Price (unfilled shares)
- **Total Cost** = Commission + Spread + Market Impact + Opportunity Cost

---

## Output Template: Execution Plan

```
ORDER: [BUY/SELL] [TICKER] [SHARES/CONTRACTS] = $[NOTIONAL]
DATE: [YYYY-MM-DD] | URGENCY: [Low/Medium/High] | HORIZON: [Minutes/Hours/Days]

ALGORITHM SELECTION:
  Primary: [VWAP/TWAP/POV/IS] — [rationale]
  Secondary: [Dark Pool/Iceberg] — [if block >$500k]
  Benchmark: [Arrival/VWAP/TWAP]

EXECUTION PARAMETERS:
  Duration: [X hours] | POV: [%] | Limit Price: $[X] (or None)
  Max Participation: [%] (avoid detection)
  Start Time: [HH:MM] | End Time: [HH:MM] (avoid open/close if low urgency)

COST ESTIMATION:
  Expected Commission: $[X]
  Bid-Ask Cost: $[X] ([bps] bps)
  Market Impact: $[X] ([bps] bps)
  Total Expected Cost: $[X] ([bps] bps of notional)

SLIPPAGE & RISK:
  Slippage Tolerance: [%] (max adverse price movement)
  Market Impact Model: Almgren-Chriss (η=[], γ=[])
  HFT Detection Risk: [Low/Medium/High] (POV <15% = Low)
  
TCA BENCHMARK:
  Benchmark: [Arrival Price $X]
  Target Shortfall: <[bps] bps (institutional grade <10bps)
  Track: Real-time vs. benchmark, report post-trade
  
EXECUTION GATES:
  Liquidity: Daily Volume $[X] > 10× order → PASS
  Spread: Bid-Ask <[0.5%] → PASS
  Volatility: ATR <[5%] → PASS
  Market Open: Avoid first/last 30min → PASS
  
GATE VERDICT: FULL / REDUCED (limit POV) / SKIP (wait for liquidity)
```

---

## Red Flags — STOP and Review

- POV >20% for large orders (HFT detects, adverse selection)
- Market orders >$50k notional (slippage >1%)
- Executing >5% of daily volume in single order (market impact >2%)
- Using market orders during first/last 30min (spreads widen 2–5×)
- DEX trades without slippage tolerance (MEV bots drain)
- Holding crypto positions during CEX withdrawal suspension
- No TCA post-trade (can't improve without measurement)

**All of these mean: Re-run execution gates. Adjust algo or wait for liquidity.**
