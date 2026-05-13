# fin-sentiment-engine: Cross-Asset Sentiment & Alternative Data

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` to size positions based on sentiment extremes.

## Sentiment Sources by Asset Class

### Equity Sentiment
| Source | Type | Weight | Refresh | Use Case |
|--------|------|--------|---------|----------|
| **Fear & Greed Index** | Composite (7 inputs) | 1.0 | Daily | Market-wide sentiment |
| **AAII Sentiment** | Retail survey (bull/bear/neutral) | 0.7 | Weekly | Contrarian indicator |
| **NAAIM Exposure** | Professional manager equity exposure | 0.8 | Weekly | Smart money positioning |
| **Put/Call Ratio (CBOE)** | Options flow (0.4=bull, 1.0=bear) | 0.8 | Daily | Panic vs. euphoria |
| **VIX (Volatility Index)** | Implied 30d vol (S&P 500) | 1.0 | Real-time | Fear gauge |
| **Short Interest** | % float shorted (FINRA) | 0.7 | Bi-monthly | Crowded shorts |
| **Insider Trading (SEC 4)** | Executive buys vs. sells | 0.9 | Daily | Smart money signal |

### Crypto Sentiment
| Source | Type | Weight | Refresh | Use Case |
|--------|------|--------|---------|----------|
| **Crypto Fear & Greed** | Composite (5 inputs) | 1.0 | Daily | BTC/ETH sentiment |
| **Funding Rates** | Perpetual swap (positive=longs pay) | 0.9 | Hourly | Leverage positioning |
| **Long/Short Ratio** | Exchange accounts (Coinglass) | 0.7 | Daily | Retail vs. pro |
| **Stablecoin Ratio (SSR)** | Stablecoin supply vs. market cap | 0.6 | Daily | Dry powder indicator |
| **Google Trends** | "Bitcoin" search volume | 0.5 | Daily | Retail FOMO |
| **Social (Twitter/Reddit)** | Sentiment analysis (NLP) | 0.4 | Real-time | Hype cycle detection |

### Forex Sentiment
| Source | Type | Weight | Refresh | Use Case |
|--------|------|--------|---------|----------|
| **CFTC Commitment of Traders** | Speculative vs. commercial positions | 0.9 | Weekly | Extreme positioning |
| **Risk-On/Risk-Off** | Aussie/Yen (AUD/JPY) cross | 0.8 | Real-time | Carry trade health |
| **EM FX positioning** | USD/RMB, USD/TRY, USD/ZAR spreads | 0.7 | Daily | EM crisis preview |
| **Central Bank hawkishness** | Speeches, dot plots, meeting minutes | 0.8 | Event-driven | Policy shift anticipation |

---

## Sentiment Score Calculation (0–100)

### Components (Equal Weight for Composite)
1. **Fear & Greed Index** (F&G): 0–100 → direct mapping
2. **VIX Normalize**: (VIX – 10) / (40 – 10) × 100 → invert (high VIX = low score)
3. **Put/Call Ratio**: (P/C – 0.4) / (1.0 – 0.4) × 100 → cap 0–100
4. **AAII Bull-Bear Spread**: (Bull% – Bear%) / 2 + 50 → normalize
5. **NAAIM Exposure**: (Exposure – 20) / (120 – 20) × 100 → cap 0–100

### Composite Score Interpretation
| Score | Zone | Market State | Strategy |
|-------|------|--------------|----------|
| 0–15 | Extreme Fear | Capitulation | Strong Buy (contrarian) |
| 16–30 | Fear | Oversold | Buy / Accumulate |
| 31–45 | Caution | Bearish bias | Reduced longs, defensive |
| 46–55 | Neutral | Balanced | Hold, range-trade |
| 56–70 | Optimism | Overbought | Trim, take profits |
| 71–85 | Greed | Euphoria building | Reduce 50–70%, hedge |
| 86–100 | Extreme Greed | Top formation | Sell majority, puts/shorts |

---

## Alternative Data Sources

### Satellite & Geospatial
- **Oil inventories**: Track tanker movements, storage levels (Ursa Space, Orbital Insight)
- **Retail foot traffic**: Parking lot fullness (Thasos, Unacast) → Retail sales proxy
- **Crop yields**: Agricultural output (Planet Labs) → Commodity price impact
- **Shipping activity**: Port congestion (FleetMon) → Supply chain stress

### Credit Card & Transaction
- **Consumer spending**: Real-time transaction data (Affinity, Earnest) → Revenue proxy
- **SMB health**: Small business transaction trends → Employment/growth proxy
- **Travel/hospitality**: Airline bookings, hotel occupancy → Reopening trades

### Web Scraping & NLP
- **Job postings**: Indeed/Glassdoor trends → Hiring slowdwn = recession signal
- **E-commerce pricing**: Amazon price changes → Inflation gauge, margin pressure
- **App downloads**: Mobile app rankings → User growth proxy (meta, Snapchat)
- **Review sentiment**: Yelp, Google Reviews → Consumer discretionary health

### Social Media & News Analytics
- **Reddit (WSB, investing)**: Mention volume, sentiment (StockTwits API)
- **Twitter/X**: Cashtags ($AAPL), follower growth, retweet velocity
- **News sentiment**: RavenPack, Sentiment Trader → Headline tone analysis
- **Earnings call NLP**: Management tone (optimism/pessimism) → Guidance indicator

### Supply Chain & Logistics
- **Container freight rates**: Shanghai Containerized Freight Index (SCFI)
- **Semiconductor lead times**:芯片 delivery delays → Tech production bottleneck
- **Inventory levels**: Retailer warehousing data → Restocking cycle
- **Trucking rates**: DAT Freight & Analytics → Economic activity proxy

---

## Sentiment Divergence Signals

### Bullish Divergence (Buy Signal)
- **Price making lower lows, sentiment NOT making lower lows** → Bullish divergence
- **VIX staying low while market sells off** → Smart money calm (buy the dip)
- **Put/Call ratio spiking (panic) while F&G holds >30** → False fear (contrarian buy)

### Bearish Divergence (Sell Signal)
- **Price making higher highs, volume DECLINING** → Exhaustion, distribution
- **VIX making lower lows while market rallies** → Complacency (sell, hedge)
- **F&G >80, insider selling accelerating** → Smart money exiting (top)

---

## Sentiment Output Template

```
DATE: [YYYY-MM-DD]
ASSET CLASS: [Equity/Crypto/Forex/Commodity]
COMPOSITE SENTIMENT SCORE: [0–100] / Zone: [Extreme Fear → Extreme Greed]

COMPONENT SCORES:
  Fear & Greed Index: [score] → [zone]
  VIX (normalized): [score] → [low vol/high vol]
  Put/Call Ratio: [ratio] → [score]
  AAII Bull-Bear: [+]% / [-]% / [=]% → [score]
  NAAIM Exposure: [%] → [score]
  Crypto Funding (if crypto): [%] → [score]
  CFTC Positioning (if forex): [longs/shorts] → [score]

TIME FRAME ANALYSIS:
  1-Day: [score] → [shift from yesterday]
  1-Week: [score] → [trend]
  1-Month: [score] → [regime]

EXTREME POSITIONING ALERTS:
  ✓ Fear & Greed <15 for 5+ days → Capitulation BUY signal
  ✓ VIX >30 for 3+ days → Panic, contrarian long
  ✓ Put/Call >1.2 → Excessive hedging, bullish divergence
  ✗ F&G >85 for 5+ days → Euphoria, SELL signal
  ✗ VIX <12 for 2+ weeks → Complacency, hedge portfolio
  ✗ Insider selling >buying for 30d → Smart money exiting

ALTERNATIVE DATA HIGHLIGHTS:
  Satellite: [oil storage/shipping/retail traffic] → [implication]
  Credit Card: [consumer spend trend] → [revenue impact]
  Social Media: [mention volume Δ, sentiment] → [hype cycle stage]
  Supply Chain: [freight rates/inventory] → [margin impact]

DIVERGENCES (Trade Signals):
  Bullish: [price ↓↓, sentiment steady] → BUY the dip
  Bearish: [price ↑↑, volume ↓] → SELL, take profits
  Neutral: [aligned] → No divergence trades

ACTION RECOMMENDATION:
  Based on [score] in [zone]:
  → [BUY / ACCUMULATE / HOLD / TRIM / SELL]
  → Position size: [X%] (adjusted for sentiment extreme)
  → Hedge with: [VIX calls / puts / inverse ETF]
  → Next catalyst: [earnings/Fed meeting/GDP release]
```

---

## Red Flags — STOP and Cross-Check

- F&G >85 (euphoria) but recommending "buy the breakout"
- VIX <12 (complacency) but allocating 100% to equities
- Put/Call ratio <0.4 (excessive optimism) before earnings
- Crypto funding >0.1% sustained but "long-term hold" thesis
- Insider selling >3× buying for 30 days but "strong buy" rating
- AAII bearish <20% but claiming "market is oversold"
- Social media mentions +500% in 7 days (parabolic FOMO)

**All of these mean: Sentiment extreme. Re-run risk gates. Contrarian or hedge.**
