# fin-quant-strategies: Systematic Trading & Quantitative Finance

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` for position limits. Load `algo-execution.md` for implementation.

---

## Factor Investing Framework

### The Fama-French Factor Zoo
| Factor | Return Premium | Signal | Regime |
|--------|---------------|--------|--------|
| **Market (MKT)** | 5–6% ERP | Market beta | All regimes |
| **Size (SMB)** | 2–3% | Small cap > large cap | Risk-on |
| **Value (HML)** | 3–4% | Low P/B vs. high P/B | Recovery/value regime |
| **Profitability (RMW)** | 2–3% | High ROE vs. low ROE | Defensive |
| **Investment (CMA)** | 1–2% | Conservative vs. aggressive CapEx | Stable |
| **Momentum (MOM)** | 4–5% | 12-1 month returns | Trending markets |
| **Quality** | 2–3% | Composite: ROE + low debt + accruals | Risk-off, defensive |
| **Low Vol** | 2–3% | Beta, realized vol | Risk-off |
| **Carry** | 3–4% | Interest rate differential | Low volatility regime |

### Factor Timing (Regime-Based)
```
EXPANSION (GDP+ , Inflation moderate):
  → Overweight: Momentum, Quality, Value
  → Underweight: Low Vol, Defensive

LATE CYCLE (GDP slowing, Inflation high):
  → Overweight: Value, Commodities, Low Vol
  → Underweight: Growth, Momentum

RECESSION (GDP–, Inflation falling):
  → Overweight: Low Vol, Quality, Bonds
  → Underweight: Small Cap, Value, Cyclicals

RECOVERY (GDP+, Inflation low):
  → Overweight: Small Cap, Momentum, Value
  → Underweight: Low Vol, Bonds
```

---

## Statistical Arbitrage (Stat Arb)

### Pairs Trading
```
1. Identify cointegrated pairs:
   → Same sector, similar business model
   → Augmented Dickey-Fuller (ADF) test on spread: p-value <0.05

2. Z-Score calculation:
   Z = (Spread – Mean) / Std Dev
   Entry: Z > +2.0 (sell expensive, buy cheap)
   Exit: Z reverts to 0
   Stop: Z > +3.0 (mean reversion failed)

3. Half-life of mean reversion:
   → Ornstein-Uhlenbeck process: θ parameter
   → Half-life = ln(2) / θ
   → Trade only if half-life < your horizon (don't hold forever)

4. Cointegration breaks:
   → Fundamental change in one company (earnings miss, M&A, regulation)
   → Monitor ADF on rolling 60d window — exit if cointegration breaks
```

### Market Neutral Strategies
```
Long-Short Equity (Market Neutral):
  → Beta-hedge: Short SPY/SPX futures to neutralize market exposure
  → Dollar-neutral: Equal $ long and short
  → Factor-neutral: Neutral on size, value, momentum factors
  
Risk targets:
  → Gross exposure: 150–200% (typical)
  → Net exposure: –10% to +10% (market neutral)
  → Position max: 3–5% gross per position (concentrated = alpha, not arb)
```

---

## Momentum Strategies

### Time-Series Momentum (Trend Following)
```
Signal: 12-1 month return (skip last month to avoid reversal)
Universe: Diversified: equities, bonds, commodities, FX

Simple rules:
  → Asset return > 0 in last 12 months → Long
  → Asset return < 0 in last 12 months → Short
  
Risk-adjusted momentum:
  → Signal = 12-1 month return / realized 1yr volatility
  → Equal-vol weight positions (target X% annualized vol each)

Momentum crashes:
  → Occur at market bottoms (sharp reversals)
  → Hedge: Overlapping momentum (add 1-3 month short-term signal)
  → Reduce exposure when cross-sectional dispersion is low
```

### Cross-Sectional Momentum
```
Rank all assets in universe by 12-1 month return
Long top quintile (Q1)
Short bottom quintile (Q5)
Monthly rebalance

Enhancements:
  → Residual momentum: Orthogonalize to factor exposures
  → Earnings-adjusted momentum: Remove earnings surprise component
  → Industry-neutral momentum: Long/short within same industry
```

---

## Mean Reversion Strategies

### Short-Term Reversal
```
Signal: 1-week or 1-month return
  → Top performers this week → Short next week
  → Bottom performers this week → Long next week
  
Works best: Large-cap, liquid equities; options expiration weeks
Doesn't work: Strong trending markets; earnings weeks

Intraday mean reversion:
  → Gap-fill strategies (open gap vs. prior close)
  → VWAP reversion after large institutional prints
  → Options expiration pinning effects
```

### Volatility Mean Reversion
```
VIX mean reversion:
  → VIX spikes >30 = elevated (expect mean reversion to 15–20)
  → Trade: Short VIX ETPs (UVXY, SVIX) on VIX >35 spikes
  → Risk: VIX can stay high; tail risk of infinite loss on naked short

IV rank mean reversion in options:
  → IV Rank >80: Sell premium (strangles, iron condors)
  → IV Rank <20: Buy premium (debit spreads, calendars)
  → IV crush post-earnings = core edge for premium sellers
```

---

## Quantitative Risk Models

### Multi-Factor Risk Model
```
Portfolio Return = α + β1(MKT) + β2(SMB) + β3(HML) + β4(MOM) + ε

Risk decomposition:
  → Systematic risk = β factors × factor covariance matrix × β'
  → Idiosyncratic risk = ε variance (company-specific)
  → Target: High alpha (ε), controlled systematic exposure

Portfolio optimization:
  → Markowitz mean-variance (theoretical framework)
  → Black-Litterman (incorporate views into optimization)
  → Risk parity (equal risk contribution from each factor)
  → Constraints: Long-only, max weight, turnover limit, factor neutrality
```

### Drawdown Control Models
```
Constant Proportion Portfolio Insurance (CPPI):
  m = multiplier (typically 3–5)
  Investment = m × (Portfolio Value – Floor)
  Floor = Maximum acceptable loss level

Target Volatility:
  Target position size = Target Vol / Realized Vol × Capital
  When vol rises → reduce exposure automatically
  When vol falls → increase exposure automatically

Max Drawdown Kill Switch:
  → Daily P&L < –2%: Reduce all positions 50%
  → Portfolio drawdown > 10%: Halt new trades, review
  → Portfolio drawdown > 15%: Full stop, strategy review
```

---

## Machine Learning in Finance

### ML Strategy Types
| Approach | Use Case | Risk |
|----------|----------|------|
| **Random Forest / XGBoost** | Feature importance, classification | Overfitting on small samples |
| **LSTM / Transformer** | Time-series forecasting | Data requirements, regime change |
| **Reinforcement Learning** | Dynamic hedging, execution | Sparse reward, hard to train |
| **NLP / Sentiment** | News signal extraction | Short half-life, adversarial |
| **Graph Neural Networks** | Correlation networks, contagion | Interpretability |

### Critical Backtesting Rules
```
1. Walk-forward validation only (no look-ahead bias)
2. Out-of-sample test set: Never touched during model development
3. Minimum 30+ independent signals (not correlated observations)
4. Transaction costs: Include slippage, spread, market impact
5. Survivorship bias: Use point-in-time data (Bloomberg Terminal or Compustat)
6. Overfitting test: Sharpe ratio degrades <50% out-of-sample? Overfit.
7. Monte Carlo: Test on 1,000+ random permutations of train/test splits
8. Regime robustness: Does it work in 2008, 2020, 2022 separately?

Red flags:
  → Sharpe >3 in backtest: Almost always overfit
  → Strategy with >50 parameters: Overfit
  → Backtest better than live by >50%: Execution/slippage issues
```

### Sharpe Ratio Standards
| Sharpe | Assessment |
|--------|-----------|
| >2.0 | Exceptional (likely overfit if backtest-only) |
| 1.5–2.0 | Excellent (institutional quality) |
| 1.0–1.5 | Good (acceptable for most strategies) |
| 0.5–1.0 | Marginal (needs improvement or diversification) |
| <0.5 | Reject (noise exceeds signal) |

---

## Quant Strategies Output Template

```
STRATEGY: [Name]
TYPE: [Momentum / Mean Reversion / Stat Arb / Factor / ML]
UNIVERSE: [Asset class, number of instruments]

BACKTEST METRICS:
  Period:          [start] – [end]
  CAGR:            X%
  Volatility:      X%
  Sharpe:          X.X
  Max Drawdown:    –X%
  Win Rate:        X%
  Calmar Ratio:    X.X
  OOS Sharpe:      X.X (degradation from IS: X%)

IMPLEMENTATION:
  Rebalance:       [Daily/Weekly/Monthly]
  Turnover:        X%/month
  Capacity:        $XM (market impact limit)
  Execution algo:  [VWAP/TWAP/IS]

REGIME ANALYSIS:
  → Works in: [list regimes]
  → Fails in: [list regimes]
  → Correlation to SPY: X.X
```
