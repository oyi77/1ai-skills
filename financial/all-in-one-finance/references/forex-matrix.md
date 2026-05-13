# fin-forex-matrix: Currency Analysis

## Currency Strength Framework

### Relative Strength Matrix
Build a 8-currency matrix: USD, EUR, GBP, JPY, CHF, AUD, CAD, NZD
- Rank currencies by momentum (20d ROC) and carry return
- Strongest vs. weakest pair = highest-probability carry trade

### Central Bank Policy Divergence
Key driver of medium-term FX trends:

| Pair | Bullish Driver | Bearish Driver |
|------|---------------|---------------|
| USD/JPY | Fed hawkish + BOJ dovish | Fed cuts + BOJ hikes |
| EUR/USD | ECB hawkish + growth recovery | ECB cuts + energy crisis |
| AUD/USD | China stimulus + commodity boom | China slowdown + RBA cuts |
| GBP/USD | BOE hike cycle | UK political instability |

### Carry Trade Calculator
```
Annual Carry Return = (Interest Rate Currency A – Interest Rate Currency B)
Risk-Adjusted Carry = Annual Carry / 30d Realized Volatility
High sharpe carry trades: ratio > 0.5
```

### Intervention Risk
- BOJ historically intervenes when USD/JPY moves >3% rapidly
- Swiss National Bank (SNB): intervenes to prevent excessive CHF strength
- Monitor: central bank FX reserves trend (declining = intervention spending)

---

## Forex Output Template
```
PAIR: [CCY1/CCY2] | TIMEFRAME: [daily/weekly]
TREND: [direction] | STRENGTH: [strong/moderate/weak]
CARRY: [% annualized] | CARRY RISK-ADJ: [ratio]
POLICY DIVERGENCE: [central bank stance comparison]
KEY LEVEL: Support [x] | Resistance [x]
INTERVENTION RISK: [low/medium/high] — [rationale]
SIGNAL: [Long/Short/Neutral] | CONVICTION: [score]
```
