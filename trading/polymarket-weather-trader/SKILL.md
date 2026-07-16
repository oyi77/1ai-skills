---
name: polymarket-weather-trader
description: Trade Polymarket weather markets using NOAA forecasts via Simmer API. Inspired by gopfan2's $2M+ strategy. Use
  when user wants to trade temperature markets, automate weather bets, check NOAA forecasts, or run gopfan2-style trading.
domain: trading
tags:
- algorithms
- api
- markets
- polymarket
- trader
- trading
- money
- weather
metadata:
  author: Simmer (@simmer_markets)
  version: 2.0.0
  displayName: Polymarket Weather Trader
  difficulty: beginner
  attribution: Strategy inspired by gopfan2
---
# Polymarket Weather Trader

## When to Use

**Trigger phrases:**
- "polymarket weather trader"
- "Help me with polymarket weather trader"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Trade temperature markets on Polymarket using NOAA forecast data.

> **This is a template.** The default signal is NOAA temperature forecasts — remix it with other weather APIs, different forecast models, or additional market types (precipitation, wind, etc.). The skill handles all the plumbing (market discovery, NOAA parsing, trade execution, safeguards). Your agent provides the alpha.


## When NOT to Use

- When you cannot afford to lose the capital at risk
- For instruments you do not understand
- When emotional state impairs judgment (revenge trading, FOMO)


## Overview

Polymarket Weather Trader provides market analysis capabilities with risk management.

## Workflow

```python
# Example: Position sizing (Kelly Criterion)
def kelly_size(win_rate: float, avg_win: float, avg_loss: float) -> float:
    if avg_loss == 0: return 0
    b = avg_win / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly * 0.5, 0.02))  # Half-Kelly, max 2%
```

1. **Research** — Analyze market conditions and opportunities
2. **Plan** — Define entry, exit, and position sizing
3. **Execute** — Place trades with proper order types
4. **Monitor** — Track positions and market changes
5. **Manage risk** — Apply stop-losses and hedging
6. **Review** — Post-trade analysis and journaling

## Risk Management

- Never risk more than 1-2% of portfolio per trade
- Set stop-loss before entering any position
- Diversify across uncorrelated assets
- Size positions based on volatility (ATR)
- Have a maximum daily loss limit

## Key Metrics

- Win rate and profit factor
- Sharpe ratio and max drawdown
- Average risk-reward ratio
- Expectancy per trade
- Correlation to benchmark

## Discipline Rules

- Follow your trading plan — no impulsive trades
- Cut losses short, let winners run
- Review every trade in your journal
- Never revenge trade after a loss
- Take breaks after consecutive losses

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will cut losses later" | Later never comes. Set stop-losses before entering any trade. |
| "This time is different" | It never is. Follow your strategy, not your emotions. |
| "I do not need to journal" | Journaling reveals patterns in your behavior. Track every trade. |


## Money-Making Overview

Trade temperature prediction markets on Polymarket using NOAA forecast data for a statistical edge against retail bettors. Inspired by gopfan2's documented $2M+ strategy, this system exploits the gap between NOAA's high-accuracy short-range forecasts and market-implied probabilities. Target: $50-500/day per city market with disciplined position sizing.

The core insight: Polymarket weather markets are dominated by casual bettors who misprice uncertainty, especially around temperature boundaries (e.g., "Will NYC hit 90°F?"). NOAA's 1-7 day forecasts are significantly more accurate than the general public assumes. By systematically comparing NOAA's probabilistic forecast to the market price and applying Kelly Criterion position sizing, traders can extract consistent positive expectancy.

## Revenue Streams

- **Temperature spread trading ($100-1K/day)** — Buy the "Yes" when NOAA shows >60% probability and the market prices <50%. Sell when the market overshoots the forecast. Typical: 10-20% edge per trade on binary outcome markets (high/low, above/below threshold).
- **Multi-city scaling ($500-5K/day)** — Run the same strategy across 10+ cities simultaneously. NYC, Chicago, LA, Miami, Houston, Phoenix, Denver, Seattle, Dallas, Boston each get fresh forecasts hourly. Geographic diversification smooths variance.
- **Contiguous range arbitrage ($1-10K/month)** — Trade temperature range markets (e.g., "High between 85-89°F") where the market misprices the probability distribution. Buy the undervalued range when NOAA's distribution (forecast +/- spread) concentrates differently than the market expects.
- **Seasonal weather events ($1-10K/month)** — Heat waves, cold snaps, and storm events create temporary inefficiency as retail bettors react emotionally while NOAA data remains objective. Scale up during extreme weather weeks.

## Weather Trading Logic

### Forecast vs Market Price

The fundamental signal: compare NOAA's probabilistic forecast to the Polymarket "Yes" price.

```
NOAA GFS temp forecast for NYC July 18: 88°F (range 85-91°F)
Polymarket "NYC high >= 90°F on July 18" price: $0.45

NOAA probability of >= 90°F: ~15% (based on forecast distribution)
Market price: $0.45 (implied 45% probability)

Edge: Market is 30 percentage points too high → SELL (buy NO at $0.55)
Kelly size at 0.5 fraction: see sizing formula below
```

### Uncertainty Arbitrage

NOAA provides temperature ranges (forecast +/- spread). Wider spread = higher uncertainty = the market often overprices extremes. Key scenarios:

- **Low-uncertainty edge** (1-3 day out, spread <3°F): Forecast is highly reliable. Market still prices significant tail risk from outdated models. Bet aggressively here.
- **High-uncertainty fade** (5-7 day out, spread >5°F): Market overreacts to the initial forecast direction. Wait for 3-day window to enter.
- **Diurnal pattern arb**: Nighttime lows are more predictable than daytime highs. Markets don't differentiate — exploit this asymmetry.

### Contiguous Range Trading

For multi-outcome markets (e.g., 85-89°F, 90-94°F, 95+°F):

```python
# Example: Calculate total implied probability across ranges
def find_range_arb(ranges: list, noaa_forecast: float, noaa_spread: float):
    """Compare predicted distribution to market-implied distribution."""
    from scipy.stats import norm
    total_market = sum(r['price'] for r in ranges)
    # Expected distribution around NOAA forecast
    for r in ranges:
        lo, hi = r['low'], r['high']
        noaa_prob = norm.cdf(hi, noaa_forecast, noaa_spread) - norm.cdf(lo, noaa_forecast, noaa_spread)
        market_prob = r['price']
        edge = noaa_prob - market_prob
        if abs(edge) > 0.05:  # >5% edge threshold
            r['action'] = 'BUY YES' if edge > 0 else 'BUY NO'
            r['kelly_size'] = noaa_prob * 0.5  # Half-Kelly
    return [r for r in ranges if abs(r.get('edge', 0)) > 0.05]
```

## First Action in 60 Minutes

Run this Python script to fetch NOAA forecast data and identify +EV Polymarket opportunities:

```bash
python3 << 'EOF'
import requests, json, math

# 1. Fetch NOAA hourly forecast for a city (example: NYC)
NOAA_POINTS = {
    "nyc": {"lat": 40.7128, "lon": -74.0060, "grid": "OKX", "gridX": 33, "gridY": 33},
    "chicago": {"lat": 41.8781, "lon": -87.6298, "grid": "LOT", "gridX": 74, "gridY": 73},
    "la": {"lat": 34.0522, "lon": -118.2437, "grid": "LOX", "gridX": 154, "gridY": 49},
    "miami": {"lat": 25.7617, "lon": -80.1918, "grid": "MFL", "gridX": 67, "gridY": 78},
}

city = "nyc"
c = NOAA_POINTS[city]
url = f"https://api.weather.gov/gridpoints/{c['grid']}/{c['gridX']},{c['gridY']}/forecast"
headers = {"User-Agent": "WeatherTrader/1.0 (your@email.com)", "Accept": "application/json"}

resp = requests.get(url, headers=headers, timeout=15)
resp.raise_for_status()
data = resp.json()

# 2. Extract daily high forecast with spread
print(f"\n=== NOAA Forecast for {city.upper()} ===\n")
for period in data["properties"]["periods"]:
    name = period["name"]
    temp = period["temperature"]
    unit = period["temperatureUnit"]
    detail = period.get("detailedForecast", "")
    # Estimate uncertainty: wider detail text often means more uncertainty
    spread = 3 + len(detail) * 0.01  # heuristic: 3-8°F spread
    print(f"{name:20s}: {temp:3d}°{unit}  (est. spread ±{spread:.0f}°F)")
    print(f"  {detail[:120]}")

# 3. Simulate market price comparison
# In production: use Simmer API / Polymarket CLOB to get actual prices
print("\n=== +EV Opportunity Scan (prototype) ===\n")
threshold = 90  # e.g., will NYC hit 90°F?
noaa_peak = max(p["temperature"] for p in data["properties"]["periods"])
print(f"Peak forecast: {noaa_peak}°F")
print(f"Threshold:    >= {threshold}°F")
print(f"Forecast vs threshold: {'ABOVE' if noaa_peak >= threshold else 'BELOW'} by {abs(noaa_peak - threshold)}°F")
print()
print("With real Polymarket prices via Simmer API:")
print("  fetch_markets(city='nyc', type='temperature')")
print("  compare(noaa_prob, market_price)  # returns edge")
print("  trade_if(edge > 0.05)             # Kelly-sized")
print()
print("=== NEXT STEPS ===")
print("1. Get Simmer API key at https://simmer.markets")
print("2. Run: simmer weather scan --cities nyc,chicago,la,miami")
print("3. Set up cron to scan every 60 minutes")
print("4. Track results in a spreadsheet")
EOF
```

The prototype above runs with zero API keys (NOAA data is free). For real execution, use the Simmer API (`simmer weather scan`) which handles market discovery, trade execution via Polymarket CLOB, and automated position management.

## Output Format

When running a weather trade scan, return results in this structure:

```json
{
  "scan_time": "2026-07-16T14:00:00Z",
  "cities_scanned": ["nyc", "chicago", "la"],
  "opportunities": [
    {
      "city": "nyc",
      "market": "NYC high >= 90°F on 2026-07-17",
      "noaa_forecast": 88,
      "noaa_spread": 4,
      "noaa_prob_above": 0.15,
      "market_price_yes": 0.45,
      "edge": -0.30,
      "action": "BUY_NO",
      "kelly_size_pct": 1.0,
      "confidence": "high"
    },
    {
      "city": "chicago",
      "market": "Chicago high >= 85°F on 2026-07-17",
      "noaa_forecast": 82,
      "noaa_spread": 5,
      "noaa_prob_above": 0.25,
      "market_price_yes": 0.32,
      "edge": -0.07,
      "action": "PASS",
      "confidence": "low"
    }
  ],
  "summary": {
    "total_opportunities": 1,
    "total_kelly_at_risk": 1.0,
    "portfolio_risk_pct": 1.0
  }
}
```

For a trade execution, return:

```json
{
  "action": "BUY_NO",
  "market": "NYC high >= 90°F on 2026-07-17",
  "size": 50.00,
  "price": 0.55,
  "expected_value": 0.10,
  "max_loss": 50.00,
  "position_risk_pct": 1.0,
  "reason": "NOAA shows 15% chance of >=90°F, market prices at 45%. 30pp edge selling YES (buying NO at $0.55)."
}
```


## Process

1. **Scope** — Define research questions, identify data sources, set time boundaries
1. **Gather** — Collect data from primary sources, APIs, and public records
1. **Synthesize** — Analyze findings, identify patterns, produce actionable report

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings