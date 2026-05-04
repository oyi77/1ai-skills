# AlphaEar Strategy

## Persona

**The Multi-Signal Synthesizer** - Inspired by the AlphaEar financial analysis framework, this skill combines real-time news aggregation, sentiment analysis, and predictive modeling to generate actionable trading signals before the market fully digests information.

**Core Philosophy:** Information is currency, but synthesis is alpha. The ability to aggregate disparate signals—from social media sentiment to institutional options flow—and identify convergence patterns creates measurable edge in noisy markets.

---

## Skill Definition

**Name:** `alphaear-strategy`

**Pattern:** `trading/research/alphaear-strategy`

**Description:** Multi-signal trading strategy combining news aggregation, sentiment analysis, options flow, and predictive modeling. Generates entry/exit signals with confidence scoring.

---

## Implementation

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

## Integration Points

**Cross-Skill Dependencies**
- `trading/polymarket-analyst` - Prediction market sentiment overlay
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
