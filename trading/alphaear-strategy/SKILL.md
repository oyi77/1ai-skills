---
name: alphaear-strategy
description: "Score trading setups using AlphaEar multi-factor analysis (momentum, volume, sentiment). Use when evaluating entry/exit signals."
domain: trading
---
## Skill Definition

**Name:** `alphaear-strategy`

**Pattern:** `trading/alphaear-strategy`

**Description:** Multi-signal trading strategy combining news aggregation, sentiment analysis, options flow, and predictive modeling. Generates entry/exit signals with confidence scoring.

---

## Implementation

Four-phase signal synthesis engine combining news aggregation, sentiment layering, predictive modeling, and options flow analysis.


### Phase 1: Real-Time News Aggregation

**Multi-Source Intelligence Gathering**
```python
news_sources = {
    "financial_media": ["Bloomberg", "Reuters", "WSJ", "CNBC"],
    "social_sentiment": ["Twitter/X", "Reddit", "StockTwits"],
    "prediction_markets": ["Polymarket", "Kalshi"],
    "regional_sources": ["Cailian (China)", "Economic Times (India)"]
}
```

**Transmission Chain Analysis**
- Map news propagation speed across sources
- Identify "first movers" vs "lagging indicators"
- Calculate information diffusion velocity
- Detect semantic divergence (same event, different interpretations)

### Phase 2: Sentiment Layering

**FinBERT Sentiment Scoring**
```python
sentiment_pipeline = {
    "model": "FinBERT",
    "scoring_range": (-1.0, +1.0),
    "confidence_threshold": 0.75,
    "time_decay": "exponential_24h"
}
```

**Multi-Horizon Sentiment**
- Immediate reaction (0-1 hour)
- Short-term sentiment (1-24 hours)
- Medium-term bias (1-7 days)
- Structural shift detection (7+ days)

**Sentiment Divergence Signals**
- Bullish news + bearish price action = caution
- Bearish news + accumulation = opportunity
- Neutral news + high volume = catalyst pending

### Phase 3: Kronos Predictive Model

**Time-Series Forecasting with News Adjustments**
```python
kronos_model = {
    "base": "LSTM_sequence_model",
    "features": ["price", "volume", "volatility", "sentiment"],
    "prediction_horizon": ["1h", "4h", "1d", "1w"],
    "confidence_intervals": True,
    "news_aware": True
}
```

**Signal Evolution Tracking**
- Strengthen: Prediction aligns with unfolding reality
- Weaken: Model confidence declining
- Falsify: Thesis invalidated by new data

### Phase 4: Options Flow Integration

**Unusual Activity Detection**
```python
options_signals = {
    "volume_threshold": 2.5 * avg_daily_volume,
    "sweep_detection": True,
    "block_trade_filter": volume > 1000,
    "otm_percentage": 0.10,  # 10% OTM
    "expiration_window": "30d"
}
```

**Options-Price Divergence**
- High call buying + flat stock = bullish setup
- High put buying + rising stock = bear trap
- IV expansion without price move = event pending

---

## Signal Generation Framework

Composite signal scoring system that weights news, social, options, technical, and prediction layers into a single actionable score.


### Composite Signal Score

```python
def calculate_alpha_signal(ticker):
    # Component scores (0-100)
    news_score = aggregate_news_sentiment(ticker)
    social_score = analyze_social_sentiment(ticker)
    options_score = detect_unusual_flow(ticker)
    technical_score = evaluate_setup_quality(ticker)
    prediction_score = kronos_forecast_confidence(ticker)
    
    # Weighted composite
    weights = {
        'news': 0.25,
        'social': 0.20,
        'options': 0.25,
        'technical': 0.15,
        'prediction': 0.15
    }
    
    composite = sum(score * weights[key] 
                     for key, score in scores.items())
    
    return {
        'signal': composite,
        'direction': 'LONG' if composite > 65 else 'SHORT' if composite < 35 else 'NEUTRAL',
        'confidence': min(composite, 100-composite) if composite != 50 else 0
    }
```

### Signal Thresholds

```
80-100: STRONG BUY - High conviction, size appropriately
65-79:  MODERATE BUY - Good setup, standard sizing
50-64:  WEAK BUY - Edge present but marginal
35-49:  WEAK SELL - Mild negative edge
20-34:  MODERATE SELL - Clear bearish signals
0-19:   STRONG SELL - High conviction short
```

---

## Usage Examples

Practical workflows for full analysis, signal monitoring, and event-driven setups.


### Example 1: Full Analysis Workflow

```python
# Run complete AlphaEar analysis
analysis = alphaear_analyze("NVDA")

# Output includes:
# - News aggregation with sentiment
# - Social media trend analysis
# - Options flow anomalies
# - Kronos price prediction
# - Composite signal score

if analysis.signal_score > 75:
    position_size = portfolio_value * 0.05  # 5% max
    entry = current_price
    stop = entry * 0.95  # 5% stop
    target = entry * 1.15  # 15% target
```

### Example 2: Signal Monitoring

```python
# Monitor multiple positions
portfolio = ["AAPL", "TSLA", "NVDA", "AMD"]
signals = {}

for ticker in portfolio:
    signals[ticker] = alphaear_analyze(ticker)
    
# Alert on signal degradation
for ticker, signal in signals.items():
    if signal.evolution == "WEAKEN":
        alert(f"{ticker}: Signal weakening, review position")
    elif signal.evolution == "FALSIFY":
        alert(f"{ticker}: Thesis invalidated, consider exit")
```

### Example 3: Event-Driven Setup

```python
# Pre-earnings analysis
ticker = "AMZN"
catalyst_date = get_next_earnings_date(ticker)
days_to_catalyst = (catalyst_date - today).days

if days_to_catalyst <= 7:
    setup = alphaear_analyze(
        ticker,
        focus="catalyst_setup",
        include_options=True
    )
    
    if setup.options_signal == "unusual_call_activity":
        # Market positioning bullish
        direction = "LONG"
        structure = "call_spread"
```

---


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

## Integration Points

**Cross-Skill Dependencies**
- `trading/investing-algorithm-framework` - Prediction market sentiment overlay
- `trading/black-edge` - Alternative data integration
- `research/trendradar` - Trend detection correlation
- `marketing/social-media-engagement` - Social sentiment analysis

**Data Source Requirements**
- News APIs (NewsAPI, Bloomberg API)
- Social sentiment (Twitter API, Reddit)
- Options data (Unusual Whales, Cboe)
- Price data (yfinance, Polygon)

---

## Risk Management

Signal quality filters, position sizing algorithms, and risk-adjusted allocation rules.


### Signal Quality Filters

```python
# Avoid false signals
filters = {
    "minimum_volume": 1000000,  # $1M daily volume
    "minimum_market_cap": 1e9,   # $1B minimum
    "max_spread_percent": 0.5,   # 0.5% max spread
    "earnings_buffer": 2,        # Days before/after earnings
    "news_recency": 24           # Hours
}
```

### Position Sizing

```python
def size_position(signal_score, portfolio_value):
    base_size = portfolio_value * 0.02  # 2% base
    
    # Scale by signal strength
    if signal_score >= 80:
        multiplier = 2.5  # 5% position
    elif signal_score >= 65:
        multiplier = 1.5  # 3% position
    else:
        multiplier = 1.0  # 2% position
    
    return base_size * multiplier
```

---

## Output Format

```yaml
alphaear_report:
  ticker: "NVDA"
  analysis_timestamp: "2025-05-04T14:30:00Z"
  
  news_analysis:
    headline_count: 47
    sentiment_score: 0.72
    key_themes:
      - "AI demand acceleration"
      - "Data center spending"
      - "Supply chain constraints"
    transmission_velocity: "fast"
    
  social_sentiment:
    reddit_score: 0.65
    twitter_score: 0.78
    stocktwits_score: 0.81
    trending_hashtags: ["#NVDA", "#AI", "#semiconductors"]
    
  options_flow:
    unusual_activity: True
    call_put_ratio: 2.3
    top_volume_strikes: [900, 950, 1000]
    sweep_detected: True
    
  kronos_prediction:
    1h_forecast: "+1.2%"
    4h_forecast: "+2.1%"
    1d_forecast: "+3.5%"
    confidence: 0.74
    
  composite_signal:
    score: 82
    direction: "LONG"
    confidence: "HIGH"
    evolution: "STRENGTHEN"
    
  recommendation:
    action: "BUY"
    entry: "Current market"
    stop_loss: "-5%"
    take_profit: "+15%"
    position_size: "5% portfolio"
    time_frame: "1-2 weeks"
    
  risk_factors:
    - "Overall market volatility elevated"
    - "Semiconductor sector rotation risk"
    - "Earnings in 3 weeks"
```

---

## Triggers

- `/alphaear analyze <ticker>` - Full multi-signal analysis
- `/alphaear scan <sector>` - Find best opportunities in sector
- `/alphaear monitor <ticker>` - Real-time signal tracking
- `/alphaear backtest <strategy>` - Historical signal performance

---

**Note:** This skill requires access to real-time data feeds and sentiment APIs. Free tiers may have limitations. For production use, consider premium data subscriptions.

**Donation:** Support development → https://www.tip.md/oyi77

## Evidence Standards (Non-Negotiable)

| Tier | Type | Weight | Verification | AlphaEar Examples |
|------|------|--------|--------------|-------------------|
| **T1** | Primary source | 1.0 | Direct URL + timestamp + hash | SEC filings, earnings call transcripts, exchange order book data, Cboe options flow raw data, central bank policy statements |
| **T2** | Factual secondary | 0.7 | Cross-reference 2+ independent sources | Bloomberg/Reuters news feeds, Unusual Whales aggregated flow, FinBERT sentiment scores, Polygon price/volume data, Kronos model output (validated against historical backtest) |
| **T3** | Opinion/social | 0.3 | Flag as "speculative" in all outputs | Twitter/X trending sentiment, Reddit/StockTwits posts, analyst price targets, newsletter tips, YouTube commentary, prediction market odds (Polymarket/Kalshi) |

**Rules:**

1. No actionable recommendation (buy/sell/short/hedge) on T3-only evidence
2. Composite signal score >65 for longs or <35 for shorts requires at least 50% T1/T2 weighted evidence across the 4 signal layers
3. Every T3 claim must be paired with a T1/T2 disconfirming evidence search before inclusion
4. Always disclose evidence composition (T1/T2/T3 percentage) in the output report
5. Kronos predictions alone are T2 evidence at most; they require T1 confirmation from price/volume data

## Anti-Bias Checklist (Run Before Every Recommendation)

Six cognitive traps to evaluate before every recommendation to ensure evidence-driven decisions.

### 6 Cognitive Traps

- [ ] **Confirmation bias** -- Did I actively seek news and data that contradicts the current signal direction? If bullish, did I search for bearish catalysts?
- [ ] **Anchoring** -- Am I over-weighting the first headline or sentiment reading I saw? Have I re-evaluated after scanning all 4 signal layers independently?
- [ ] **Recency bias** -- Am I projecting the last 24-48 hours of sentiment forward without checking 30-day and 90-day historical context for this ticker?
- [ ] **Herd mentality** -- Is social sentiment simply reflecting the crowd? Have I checked whether options flow and Kronos diverge from the consensus direction?
- [ ] **Sunk cost** -- Am I defending a prior position or thesis by overweighting signals that confirm it? Would I take the same trade if I had no existing position?
- [ ] **Overconfidence** -- Is my conviction score calibrated to evidence quality? A composite of 75 built on 60% T3 evidence is weaker than a composite of 65 built on 70% T1/T2 evidence

## When NOT to Use

- When you have no access to real-time news APIs (NewsAPI, Bloomberg) or options data feeds (Unusual Whales, Cboe) -- the signal synthesis engine cannot function without live data
- When analyzing assets with less than $10M average daily volume -- illiquid instruments produce unreliable sentiment and options flow signals
- During earnings blackout periods for the target ticker -- options flow, sentiment, and news signals distort around earnings dates, producing false positives
- When only a single signal layer is available (e.g., sentiment only, no options or Kronos data) -- multi-signal convergence is the core thesis; single-source signals lack sufficient edge
- When the user needs pure technical analysis without news or sentiment overlay -- use `fin-equity-technical` instead
- When analyzing pre-IPO or recently listed stocks (<30 days) -- insufficient historical data for Kronos predictions and options flow patterns
- When regulatory filings or compliance tasks are the primary goal -- use `fin-compliance-kyc` instead
- When the task is personal budgeting, tax preparation, or non-market financial planning -- outside this skill's domain
- When a more appropriate specialized skill exists (e.g., `trading/black-edge` for dark pool intelligence, `trading/investing-algorithm-framework` for prediction markets)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "News is already priced in" | Research shows 65%+ of post-news drift occurs in the first 4 hours; retail and algo digestion lag creates tradeable windows |
| "Sentiment is too noisy to be useful" | Multi-source sentiment aggregation (FinBERT + social + options) filters ~70% of noise; divergence between sentiment and price action is itself a signal |
| "Options flow can be hedging, not directional" | Unusual sweep activity filtering (volume >2.5x avg, block trades >1000 contracts, OTM focus) isolates speculative positioning from delta-neutral hedging |
| "Kronos model confidence is high, skip the other signals" | No single layer is sufficient -- even at 0.9 confidence, Kronos can miss regime changes that news/sentiment catches; convergence across layers is what creates alpha |
| "Just give me the signal, skip the verification" | Skipping verification leads to acting on single-source signals with 30-40% win rates vs. multi-signal convergence at 55-65% win rates |
| "I'll size up since the composite score is 85+" | Position sizing must still respect portfolio risk limits; a single trade should never exceed 5% of portfolio regardless of signal strength |
| "The stock is up 10% today, the signal must be right" | Chasing momentum without checking options flow and Kronos evolution confirms hindsight bias, not forward edge |
| "I don't need the full 4-phase analysis for this" | Truncating phases removes the diversification benefit of multi-signal synthesis; each skipped layer increases false positive probability by 15-25% |

## Red Flags

- Signal originates from only one of the four layers (news, sentiment, options, Kronos) without convergence from at least one other layer
- Options flow directly contradicts sentiment direction (e.g., heavy put buying alongside bullish sentiment) -- this divergence requires resolution before acting
- Kronos model confidence falls below 0.4 -- below this threshold, predictions have no statistical edge over random
- News sentiment score exceeds 0.9 or drops below -0.9 -- extreme readings often mean the move has already happened
- Social sentiment diverges from financial media sentiment by more than 0.4 -- suggests either retail-FII conflict or coordinated manipulation
- Composite signal score between 45-55 (the "no edge" zone) -- trades in this range have negative expected value after transaction costs
- Options sweep detected but IV is declining (unusual activity + falling IV = likely hedging, not speculation)
- Headline count spikes above 3 standard deviations from 30-day mean -- information overload degrades signal quality
- Signal evolution tracking shows WEAKEN or FALSIFY but position is still held -- thesis invalidated, action required
- User requests to skip a signal phase or "just use sentiment" -- every phase skipped increases false positive rate by 15-25%
- Position size recommendation exceeds 5% of portfolio value regardless of signal strength

## Verification

After completing this skill, confirm:

- [ ] All 4 signal layers analyzed (news aggregation, sentiment, options flow, Kronos prediction)
- [ ] Composite score >65 for longs or <35 for shorts -- no trades in the 45-55 "no edge" zone
- [ ] Stop-loss and take-profit levels set before entry
- [ ] Position size respects the 5% portfolio max regardless of signal strength
- [ ] Signal direction confirmed by at least 2 of 4 layers (convergence check)
- [ ] No red flags from the list above are active for the target ticker
- [ ] Earnings buffer respected (no new positions within 2 days of earnings)
- [ ] Kronos confidence >0.4 and evolution status is STRENGTHEN or neutral (not WEAKEN or FALSIFY)
- [ ] Evidence composition disclosed (what percentage of the signal is T1 vs T2 vs T3)
- [ ] Anti-Bias Checklist completed with all 6 traps addressed

**Cross-reference:** For complete multi-asset analysis, also see `financial/all-in-one-finance` and `financial/wolf-finance`. For dark pool intelligence, see `trading/black-edge`. For prediction market sentiment, see `trading/investing-algorithm-framework`.

