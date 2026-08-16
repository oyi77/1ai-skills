---
name: finance-trading
description: Use when analyzing financial markets using technical indicators, fundamental
  analysis, and macro trends. Use for investment research.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- finance
- investigation
- research
- trading
version: 1.0.0
category: research
---


# Finance Trading

## When to Use

**Trigger phrases:**
- "finance trading"
- "Help me with finance trading"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


> *"The way to build long-term returns is through preservation of capital and home runs."* — **Paul Tudor Jones**

Expert Advisor cross-platform berbasis Python untuk trading hedging dengan sistem trailing stop dan pending order otomatis.


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Finance Trading provides a structured framework for analyzing financial markets across multiple timeframes and asset classes. The full lifecycle spans from raw market data acquisition through signal generation, risk assessment, and position management. It integrates three analysis pillars — technical analysis for entry timing, fundamental analysis for valuation context, and macro analysis for directional bias — into a unified decision pipeline. This approach works across equities, forex, commodities, crypto, and fixed income markets using broker APIs, exchange data feeds, and economic databases as data sources.

At the core is a systematic methodology for transforming noisy market data into actionable trading signals. Price history, volume profiles, and order book data feed into indicator calculations that quantify trend strength, momentum, volatility regimes, and market structure. Fundamental data including earnings reports, economic releases, and central bank policy statements provide the contextual backdrop that separates technical noise from regime changes. The synthesis of these data streams produces a probabilistic view of market direction rather than a binary prediction.

Risk management is embedded throughout the analysis lifecycle. Position sizing models scale exposure based on account equity, volatility conditions, and conviction level. Stop-loss placement logic accounts for market microstructure, support/resistance levels, and ATR-based volatility bands. The system tracks drawdown limits, correlation-based diversification rules, and regime-dependent exposure caps to ensure no single analysis error leads to catastrophic loss.

The analysis process is iterative and adaptive — each trade outcome feeds back into the model. Win rates, risk-reward ratios, and edge decay metrics are tracked across market regimes to continuously calibrate which analytical frameworks perform best in current conditions. This closed-loop approach distinguishes professional trading analysis from ad-hoc market research by maintaining statistical rigor and process discipline across every decision.

## Market Research Methodology

### Data Source Hierarchy
- **Tier 1 (Primary)**: Exchange direct feeds for real-time price and volume data
- **Tier 2 (Economic)**: FRED API, EIA, BLS, central bank releases for macro indicators
- **Tier 3 (Sentiment)**: News sentiment from financial press, social media aggregation, put/call ratios, VIX term structure
- **Tier 4 (Fundamental)**: SEC EDGAR filings, earnings transcripts, company investor relations

### Research Workflow
1. **Screening** — Scan universe using volatility, volume, and momentum filters to identify candidates
2. **Context Analysis** — Determine the macro regime (risk-on/risk-off, trending/range-bound, low/high vol)
3. **Technical Assessment** — Apply timeframe-aligned indicator suite to identify structural levels
4. **Fundamental Check** — Verify valuation, earnings trajectory, and catalyst calendar against the trade thesis
5. **Risk Calibration** — Size position per volatility-adjusted risk limits, set stops and targets
6. **Execution Plan** — Determine entry method (limit/market/pegged), order type, and trade schedule

### Market Regime Classification
- **Trending** — Sustained directional moves; favor trend-following and momentum strategies
- **Range-Bound** — Price oscillates between identifiable support/resistance; favor mean-reversion and option premium selling
- **High Volatility** — Regime shifts, event-driven spikes; reduce size, widen stops, favor optionality
- **Low Volatility** — Compressed ranges, low ATR; favor breakout strategies and gamma positioning
- **Risk-On** — Capital flows into equities, crypto, EM, high-yield credit; favor long beta and cyclical exposure
- **Risk-Off** — Flight to safety (bonds, gold, USD, JPY); favor defensive sectors and tail hedges

## Fundamental Analysis for Trading

### Valuation Frameworks
- **Discounted Cash Flow (DCF)**: Project free cash flows and discount at WACC; sensitivity matrix on growth rate and terminal value assumptions
- **Comparable Company Analysis (Comps)**: EV/EBITDA, P/E, P/S, P/B multiples relative to sector peers with premium/discount assessment
- **Precedent Transactions**: M&A multiples from comparable acquisitions to gauge takeout valuation floors
- **Sum-of-the-Parts (SOTP)**: Segment-level valuation for conglomerates to identify hidden value

### Earnings Analysis
- **Surprise & Drift**: Magnitude of EPS beat vs consensus and post-earnings price drift patterns
- **Guidance Momentum**: Forward guidance trajectory, margin outlook, and revenue quality indicators
- **Revenue Quality**: Organic vs acquired growth, recurring vs transactional mix, geographic concentration
- **Balance Sheet Health**: Debt/EBITDA coverage, interest coverage ratio, current ratio, cash burn rate

### Catalyst Calendar
- Scheduled catalysts: earnings dates, product launches, regulatory decisions, index rebalancing, lockup expirations
- Macro catalysts: FOMC meetings, CPI/NFP releases, central bank policy statements, elections
- Event-driven: M&A announcements, restructuring, spin-offs, activist campaigns, management changes

## Technical Indicator Analysis

### Trend Following Indicators
- **Moving Averages**: EMA crossovers (8/21/50/200) for trend identification; SMA envelope bands for overextension detection
- **ADX**: Values above 25 confirm trending regime; below 20 suggests range-bound. +DI/-DI cross gives trade bias
- **Ichimoku Cloud**: Leading span A/B identifies support/resistance zones; cloud color indicates trend bias
- **Parabolic SAR**: Dot placement relative to price signals trend direction

### Momentum Indicators
- **RSI**: 14-period with overbought (70+) / oversold (30-) zones; divergence patterns for trend exhaustion
- **MACD**: Signal line cross = trigger; histogram zero-line cross = momentum shift; divergence = potential reversal
- **Stochastic Oscillator**: %K/%D crossover in oversold/overbought zones; divergence at extremes
- **Williams %R**: Values above -20 = overbought, below -80 = oversold; use with trend filter to avoid counter-trend entries

### Volatility Indicators
- **Bollinger Bands**: 20-period SMA with 2 std dev bands; squeeze = low volatility precedes expansion
- **ATR**: Volatility-adaptive stop placement (2-3 ATR); position sizing based on % of equity per ATR unit
- **Keltner Channels**: EMA-based bands using ATR for width; used with Bollinger Bands for squeeze setups
- **VIX Term Structure**: VIX futures contango/backwardation informs hedging cost and tail risk appetite

### Volume Analysis
- **Volume Profile**: High-volume nodes identify price acceptance zones; low-volume nodes identify runaway zones
- **OBV**: Divergence between OBV and price signals hidden accumulation/distribution
- **VWAP**: Institutional benchmark; price above/below VWAP indicates intraday bias
- **Delta Volume (Footprint)**: Bid-ask imbalance at each price level; cumulative delta divergence signals exhaustion

## Macro Trend Identification

### Macro Regime Indicators
- **Yield Curve Structure**: 2s10s spread (inversion signaling recession risk), slope steepening/flattening regime
- **Inflation Trends**: CPI MoM/YoY, Core PCE (Fed-preferred), PPI pipeline pressures, breakeven inflation rates from TIPS
- **Labor Market**: NFP headline vs revisions, unemployment rate, labor force participation, JOLTS quits rate, wage growth
- **Liquidity Conditions**: Central bank balance sheet trajectory (QT/QE), reverse repo facility usage, SOFR rates

### Geopolitical Risk Mapping
- **Conflict Zones**: Energy supply disruption risk from producing regions, trade route chokepoints
- **Sanctions & Tariffs**: Sector-specific trade restrictions, export control lists, secondary sanctions risk
- **Election Cycles**: Policy-driven sector rotation, deregulation/regulation expectations, fiscal spending agendas
- **Currency Regimes**: Pegged currency devaluation risk, capital control imposition, CBDC development impact

### Sector & Market Cycle Positioning
- **Business Cycle Phase**: Early expansion (cyclicals, small caps), late cycle (energy, materials, value), recession (defensives, treasuries)
- **Factor Rotation**: Momentum, value, quality, low-vol, size factor performance cycles identify risk appetite shifts
- **Credit Markets as Leading Indicator**: High-yield spreads, investment-grade CDS, loan default rates signal stress
- **Commodity Super-Cycles**: Structural supply/demand imbalances drive multi-year trends in energy, metals, and agriculture

## Trading Signal Generation

### Multi-Timeframe Alignment
- **Higher Timeframe (Weekly/Daily)**: Establishes the primary trend bias — only trade in direction of daily trend for swing positions
- **Medium Timeframe (4H/1H)**: Identifies entry zones within the primary trend — look for pullbacks to value areas
- **Lower Timeframe (15m/5m)**: Precision entry timing using candlestick patterns, volume spikes, or momentum triggers
- **Confluence Scoring**: Assign weights to each timeframe alignment; minimum threshold of 3 confluent factors before signal qualifies

### Signal Types & Criteria
| Signal Type | Entry Criteria | Exit Criteria | Risk-Reward Target |
|---|---|---|---|
| Trend Continuation | Pullback to 20/50 EMA with RSI pullback to 40-50 | Trend exhaustion (divergence, failed breakout) | 2:1 minimum |
| Breakout | Volume-confirmed break of key level with above-average vol | VWAP or level invalidation below breakout candle | 3:1 target |
| Mean Reversion | Price at 2+ std dev Bollinger Band with RSI >70/<30 | Return to SMA, then fade the fade | 1.5:1 |
| Divergence | Price HH/LL with RSI/MACD LH/LL | Confirmation of reversal structure | 2.5:1 |
| Event-Driven | Pre-catalyst positioning 1-3 days before known event | Event outcome + first hour price discovery | Variable |

### Entry Optimization
- Scale into positions across 2-3 price levels rather than single fill
- Use limit orders at volume-weighted value areas (VWAP, POC, EMA clusters)
- Wait for confirmation candle close before committing full size
- Avoid entries during low-liquidity periods (lunch hour, pre-holiday, major news overlap)


## Workflow

1. **Define Market Scan Criteria** — Set universe filters by asset class, volume threshold, volatility range, and market cap using screener APIs (finviz, tradingview screener, custom SQL on historical DB)

2. **Retrieve & Align Data** — Pull OHLCV from broker/exchange API with proper handling for splits, dividends, survivorship bias. Normalize across multiple timeframes in a unified DataFrame

3. **Apply Indicator Suite** — Compute trend (EMAs, Ichimoku), momentum (RSI, MACD, stochastic), volatility (ATR, Bollinger), and volume (OBV, VWAP) indicators on each timeframe

4. **Cross-Timeframe Confluence Check** — Score signal candidates by alignment across daily/hourly/15m. Minimum 3 of 5 confluence factors required before proceeding to fundamental filter

5. **Fundamental Validation Gate** — Verify macro regime compatibility, check earnings/event calendar, review valuation extremes against sector medians. Discard signals that contradict the fundamental picture

6. **Risk-Adjust & Plan Execution** — Compute position size per volatility-based risk budget, set initial stop at technical invalidation level, define take-profit zones. Log the full trade plan including contingency scenarios

7. **Post-Entry Monitoring & Adjustment** — Trail stops based on ATR contraction after entries move in profit. Re-evaluate thesis if price reaches key levels or catalyst outcomes deviate from expectations. Archive analysis for post-trade review


## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |
| "I already know this market" | Familiarity breeds overconfidence. Regimes change — verify your assumptions each cycle. |
| "More indicators give better signals" | Indicator stacking creates curve-fit noise. Stick to 3-5 uncorrelated signals per timeframe. |
| "This time is different" | Market psychology cycles repeat. Human behavior under risk does not change. |



## Common Pitfalls

- **Overfitting to historical data**: A strategy that backtests perfectly often fails live because it memorized noise. Forward-test on out-of-sample data and use walk-forward analysis with expanding windows
- **Ignoring transaction costs**: Slippage, commissions, and spread erode edge continuously. Always model realistic fills — assume 1-2 ticks slippage per trade for liquid markets, more for illiquid
- **Confusing luck with skill**: A ten-trade winning streak in a trending market proves nothing. Track Sharpe ratio, maximum drawdown, and profit factor over 100+ independent trades before concluding edge exists
- **Recency bias in regime assessment**: The last 50 bars dominate perception. Use multi-year lookback with regime-change detection to avoid trading last year's market
- **Analysis paralysis from information overload**: More data does not linearly improve decisions. Cap the indicator count per timeframe, use a fixed decision tree, and time-box each analysis to prevent diminishing returns

## Process

1. **Market Scan** — Filter the asset universe based on pre-defined criteria aligned with the current macro regime. Log candidate counts and screening rationale

2. **Deep Dive Analysis** — For each candidate, run the full analysis stack: macro context → fundamental valuation → technical structure → volume confirmation. Note any contradictory signals

3. **Trade Plan Construction** — Document entry price zone, stop level, take-profit targets, position size, and scenario branches. Pre-commit to invalidation conditions before the trade is live

4. **Execution & Monitoring** — Place orders per the plan, monitor for unexpected regime shifts or catalyst outcomes. Update the trade log with fill prices and time

5. **Post-Trade Review** — Compare actual outcome against the plan. Classify result (good setup stopped out / bad setup won / edge played correctly). Update the signal quality tracker and the trade journal


## Verification

- [ ] Universe screening criteria documented and justified
- [ ] Macro regime classified with supporting evidence from 3+ indicators
- [ ] Technical analysis completed on 3 timeframes with confluence score
- [ ] Fundamental check passed (valuation, earnings calendar, sector context)
- [ ] Risk-adjusted position size calculated and within account limits
- [ ] Trade plan written with entry, stop, targets, and contingency scenarios
- [ ] Post-trade review completed and categorized in the journal
- [ ] Regime check performed: strategy appropriate for current market conditions?

## Monetization

- **Swing Trading Signal Service**: Publish daily/weekly trade setups (entry + stop + target) via Telegram or Discord subscription. Price at $49-99/month per ticker or index-focused tier
- **Strategy Algo Licensing**: License parameterized trading strategies (trend-following, mean-reversion, event-driven) to prop firms or retail brokers as plug-in modules. One-time fee or royalty basis
- **Educational Content & Courses**: Create structured video courses on technical analysis, regime detection, and systematic trading. Sell on Gumroad or Kajabi at $197-497 per course
- **Consulting for Small Hedge Funds**: Provide independent trade research, portfolio construction, and risk framework design for emerging fund managers. Retainer at $2,000-5,000/month
- **Custom Indicator Development**: Build bespoke TradingView Pine Script or Python indicator suites for retail traders. Per-indicator pricing ($500-2,000) or bundle subscriptions
- **Quant Research Reports**: Monthly deep-dive reports analyzing specific market regimes, factor performance, or sector rotation dynamics. Distribute via Substack paid newsletter at $20-50/month
## Verification Checklist

- [ ] Technical indicators backtested on out-of-sample data
- [ ] Fundamental analysis covers financials, moat, management
- [ ] Macro trends contextualized (rates, inflation, policy)
- [ ] Position sizing respects risk limits
- [ ] Trade journal maintained with pre/post analysis
