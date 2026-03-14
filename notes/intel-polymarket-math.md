# Polymarket Trading Math — @LunarResearcher
## Source: https://x.com/LunarResearcher/status/2031454281572954438
## Stats: 351K views, 257 likes, 913 bookmarks

## Key Formulas

### LMSR (Logarithmic Market Scoring Rule)
```
C(q) = b × ln(Σ e^(qi / b))
Price: p_k(q) = e^(qk/b) / Σ e^(qi/b)  (softmax function!)
Max loss: L_max = b × ln(n)
```

### Expected Value
```
EV = Σ(probability × payoff)
Only trade when EV > 0
```

### Kelly Criterion (Position Sizing)
```
f* = (p × b - q) / b
Use QUARTER-Kelly (divide by 4) for safety
Example: 60% win, 1:1 payout → Kelly = 20% → Use 5%
```

### Price Impact
- Buying moves price against you
- Model the impact curve before trading
- Know how many shares you can buy before edge disappears

## 5 Mental Traps
1. Base Rate Neglect — always check base rates
2. Sunk Cost Fallacy — past losses don't matter
3. Survivorship Bias — 87% of wallets LOSE money
4. Bad Bayesian Updating — update beliefs proportionally
5. Anti-Kelly Sizing — use quarter-Kelly, never YOLO

## For BerkahKarya Quant Fund
- Document this as trading framework for Nuno
- Apply to XAUUSD strategy (same EV/Kelly math)
- Polymarket as additional revenue stream when capital available
