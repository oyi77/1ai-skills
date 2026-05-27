# fin-equity-technical: Technical Analysis Framework

## Multi-Timeframe Confluence Methodology

Never use a single timeframe. Always confirm across at least 2 timeframes.

### Timeframe Hierarchy
- **Macro Trend**: Monthly / Weekly (primary direction)
- **Trading Trend**: Daily (entry zone identification)
- **Execution**: 4H / 1H (precise entry/exit timing)

---

## Indicator Matrix

### Trend Indicators
| Indicator | Signal | Notes |
|-----------|--------|-------|
| 200-day SMA | Price above = bull, below = bear | Primary trend filter |
| 50-day SMA | Crossover with 200d = Golden/Death Cross | Secondary trend |
| EMA 20/50 | Short-term momentum | Slope matters as much as position |
| Ichimoku Cloud | Price above cloud = bull; Kumo twist = trend change | Best on daily+ |

### Momentum Indicators
| Indicator | Overbought | Oversold | Divergence Signal |
|-----------|-----------|---------|------------------|
| RSI (14) | >70 | <30 | Price new high + RSI lower high = bearish div |
| MACD | Histogram expanding positive | Histogram expanding negative | Line crossover |
| Stochastic (14,3,3) | >80 | <20 | Use with trend filter only |

### Volume Indicators
- **OBV**: Trend confirmation — OBV rising with price = healthy; divergence = warning
- **Volume Profile**: High-volume nodes = strong S/R; low-volume gaps = fast-move zones
- **VWAP**: Institutional price reference; reclaim after breakdown = bullish

### Volatility
- **Bollinger Bands** (20, 2σ): Band squeeze = volatility contraction → expansion incoming
- **ATR**: Position sizing input; stop = 1.5–2.0 × ATR from entry
- **VIX / VVIX**: Market fear gauge; VIX > 30 = elevated fear, potential contrarian buy

---

## Chart Pattern Recognition

### Continuation Patterns
- **Bull Flag**: Strong pole + tight consolidation; target = pole length projected from breakout
- **Cup & Handle**: Rounded base + small pullback; breakout above handle = entry
- **Ascending Triangle**: Flat resistance + rising support; breakout = bullish

### Reversal Patterns
- **Head & Shoulders**: Neckline break = target = head-to-neckline distance
- **Double Bottom / Top**: Second test + divergence + volume = high conviction
- **Falling Wedge**: Bullish reversal; breakout + volume confirmation required

### Candle Patterns (require context/confirmation)
- Hammer / Inverted Hammer at support = potential reversal
- Engulfing candle with high volume = momentum shift
- Doji at extreme = indecision / potential turn

---

## Support & Resistance Framework

Priority order for S/R levels:
1. **All-time highs/lows** (strongest)
2. **Previous cycle highs/lows**
3. **High-volume nodes** (Volume Profile POC)
4. **Fibonacci retracements** (0.236, 0.382, 0.5, 0.618, 0.786)
5. **Round numbers** (psychological levels)
6. **Moving averages** (dynamic S/R)

---

## Entry/Exit Framework

### Entry Criteria (require 3 of 5):
- [ ] Price above key MA on primary timeframe
- [ ] Momentum indicator confirming (RSI > 50 and rising)
- [ ] Volume expansion on breakout/bounce
- [ ] No negative divergence on higher timeframe
- [ ] Risk/reward ≥ 2:1 to nearest resistance

### Stop Loss Placement
- Below recent swing low (structural stop)
- Below key moving average
- Never wider than 2× ATR without reducing position size
- Hard rule: **maximum 1–2% portfolio risk per trade**

### Profit Taking Framework
- **Partial exit at R1** (1st resistance): take 1/3 off
- **Partial exit at R2** (2nd resistance): take 1/3 off
- **Trail stop** for remaining 1/3 using ATR or swing low

---

## Technical Analysis Output Template

```
ASSET: [Ticker] | TIMEFRAME: [primary] confirmed on [secondary]
PATTERN: [identified pattern]
TREND: [Bullish / Bearish / Neutral] on [timeframe]

KEY LEVELS:
  Support: $[S1], $[S2]
  Resistance: $[R1], $[R2]
  Current Price: $[price]

INDICATORS:
  RSI([14]): [value] — [interpretation]
  MACD: [bullish/bearish crossover / divergence]
  Volume: [above/below average] — [trend confirmation / divergence]

SETUP:
  Entry Zone: $[low]–$[high]
  Stop Loss: $[price] ([ATR multiplier] × ATR)
  Target 1: $[R1] (R:R = [ratio])
  Target 2: $[R2] (R:R = [ratio])

CONVICTION: [Low / Medium / High]
INVALIDATION: [specific price level that breaks the thesis]
```
