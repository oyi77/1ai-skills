---
name: polymarket-analyst
description: Analyze Polymarket prediction markets for expected value, market inefficiencies, and trading opportunities. Use when analyzeing polymarket prediction markets for expected value, market inefficiencies, and.
domain: research
author: oyi77
license: Apache-2.0
subdomain: research
tags:
- analysis
- analyst
- investigation
- polymarket
- research
- trading
version: 1.0.0
---
# Polymarket Analyst

## When to Use

**Trigger phrases:**
- "polymarket analyst"
- "Help me with polymarket analyst"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


Analyze Polymarket predictions, calculate expected value, and identify trading opportunities.


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Polymarket is a decentralized prediction market where participants trade shares that pay 1 USDC if the event resolves Yes and 0 USDC otherwise. The polymarket analyst evaluates these contracts to identify mispriced outcomes — markets where the implied probability (the contract price) diverges from a well-reasoned estimate of the true likelihood. These divergences create positive-expected-value (EV+) trading opportunities.

The core analytical framework is straightforward: compute Expected Value per share = (Estimated True Probability × 1.0) − Current Market Price. A contract trading at 35¢ implies a 35 % market-implied probability. If research suggests a true 42 % likelihood, the edge is 7 percentage points and the EV is +7¢ per share — a strong entry signal. The challenge lies not in the arithmetic but in producing reliable probability estimates and correctly sizing positions under uncertainty.

Beyond pure EV calculation, the analyst must assess market microstructure — liquidity depth, bid-ask spreads, the presence of informed participants, and the resolution mechanism. A liquid market like a major election may have spreads of 0.1–0.2¢ and six-figure depth, allowing large positions with minimal slippage. An obscure market with $500 in liquidity and 5¢ spreads demands far more conservative sizing and an explicit slippage model.

Disciplined bankroll management is what separates sustainable prediction-market trading from gambling. The analyst applies fractional Kelly sizing, accounts for correlation among simultaneously held positions, tracks calibration metrics (Brier score over the last 100 resolved markets), and maintains a trading journal to iteratively improve both probability models and execution discipline.

```python
# Example: Fetch Polymarket market price via CLOB API
import requests

def price_from_slug(slug: str) -> float:
    url = f"https://clob.polymarket.com/markets/{slug}"
    data = requests.get(url, timeout=15).json()
    outcomes = data.get("outcomes", "").replace(" ", "").split(",")
    return float(outcomes[0]) if outcomes else 0.5
```

## Process

1. **Discover markets** — Scan Polymarket for active markets by category. Filter by minimum liquidity ($10K+), volume trend, and time to resolution (2–30 days optimal). Categorize by type: binary Yes/No, multi-outcome, or scalar.

2. **Assess information landscape** — Research the underlying event sources: official data releases, trusted news, expert commentary, and market-specific signal providers. Identify whether any participant likely holds a material information advantage.

3. **Build a probability model** — Construct a base-rate estimate from historical frequencies, then update with current information using Bayes' Theorem. For political markets: polling averages with incumbency and turnout adjustments. For financial markets: derivatives-implied probabilities and macro forecasts.

4. **Compute expected value** — Edge = estimated_true_prob − market_price. EV per share = Estimated Probability × 1 USDC − Current Price. Adjust for fees (currently zero on Polymarket), settlement risk, and opportunity cost. Only enter positions with edge above a minimum threshold (≥5 % for liquid markets, ≥20 % for niche).

5. **Size the position** — Apply the Kelly Criterion: f* = (edge × odds) / (odds − 1). Use fractional Kelly (¼ to ½) for real-money allocation. Account for correlated exposures across the portfolio. Set a per-market maximum (e.g., 5 % of bankroll).

6. **Execute and monitor** — Place limit orders near the best bid/ask. Set price alerts at key probability thresholds. Recompute EV daily or after material events. Close when edge converges to zero or a better opportunity arises.

7. **Review and archive** — After resolution, compare your estimate against the outcome. Record entry/exit prices, EV at entry, P&L, and lessons learned. Track aggregate win rate, average EV, and Kelly growth rate over time.

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
| "This market looks obvious — I know the outcome" | Certainty is a cognitive trap. Every prediction has base rate uncertainty. Quantify probability explicitly before risking capital. |
| "I will wait for a better price before entering" | While waiting, the price may move against you or the market may resolve. Enter when EV exceeds threshold; scale in if liquidity permits. |
| "The market price is efficient — it reflects all available information" | Prediction markets are not perfectly efficient. Retail sentiment, unmodelled base rates, and information cascades create persistent mispricings that a disciplined analyst can exploit. |
| "I need to double down to recover my loss" | This is the gambler's fallacy. Each trade is an independent EV decision. Sunk costs are irrelevant. Recalibrate from current state only. |
| "This niche market has no competition — easy money" | Low-liquidity markets carry high slippage and manipulation risk. The edge may vanish when you try to exit. Size accordingly and prefer liquid venues. |
| "My model is correct and the market is wrong" | Your model is a hypothesis, not ground truth. Track calibration — if your probability estimates are systematically off, recalibrate the model, don't blame the market. |

## Code Examples

```python
# Example 1: Fetch Polymarket markets and compute expected value
import requests

def fetch_active_markets(limit=50, offset=0):
    """Fetch active markets from Polymarket CLOB API."""
    url = "https://clob.polymarket.com/markets"
    params = {"limit": limit, "offset": offset, "closed": "false"}
    resp = requests.get(url, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()

def implied_price(market):
    """Extract Yes outcome price as implied probability."""
    outcomes = market.get("outcomes", "")
    if not outcomes:
        return 0.5
    prices = [float(p) for p in outcomes.replace(" ", "").split(",")]
    return prices[0] if prices else 0.5

def expected_value(est_prob, market_price):
    """EV per share. Each correct share redeems for 1 USDC."""
    return (est_prob * 1.0) - market_price

# Scan for EV+ opportunities
markets = fetch_active_markets(limit=20)
for m in markets:
    mp = implied_price(m)
    est = mp + 0.05  # placeholder — replace with calibrated model
    ev = expected_value(est, mp)
    if ev > 0:
        print(f"{m.get('question',''):60s} Price={mp:.3f} EV={ev:+.3f}")
```

```python
# Example 2: Kelly Criterion position sizing
def kelly_fraction(win_prob, price):
    """Full Kelly fraction for a binary prediction market."""
    odds = (1.0 - price) / price       # net odds per share
    edge = (win_prob * 1.0) - price   # EV per share
    if odds <= 0 or edge <= 0:
        return 0.0
    return edge / (odds * price)

def position_size(bankroll, win_prob, price, kelly_pct=0.25):
    """
    bankroll: total available capital
    kelly_pct: fractional Kelly multiplier (0.25 = conservative)
    """
    full = kelly_fraction(win_prob, price)
    return round(bankroll * full * kelly_pct, 2)

br = 10_000
p_yes = 0.35
est_true = 0.42
size = position_size(br, est_true, p_yes, kelly_pct=0.25)
print(f"Position: ${size} ({size/br*100:.1f}% of bankroll)")
```

```python
# Example 3: Mispricing scanner
def find_mispriced(markets, model, threshold=0.05):
    """Return market contracts where |EV| exceeds threshold.
    `model` is a callable(market) -> estimated_true_prob."""
    hits = []
    for m in markets:
        mp = implied_price(m)
        est = model(m)
        ev = expected_value(est, mp)
        if abs(ev) >= threshold:
            hits.append({
                "question": m.get("question"),
                "price": mp,
                "estimate": est,
                "ev": ev,
                "liquidity": m.get("liquidity", 0),
                "slug": m.get("slug", ""),
            })
    hits.sort(key=lambda x: abs(x["ev"]), reverse=True)
    return hits
```

## Setup / Configuration

Setting up the Polymarket analysis toolchain:

- **Python 3.9+** with `requests`, `pandas`, `numpy`, `scipy` for analysis; `web3` optional for on-chain operations.
- **Polymarket CLOB API**: no authentication needed for market-data queries. Trading requires API credentials from the Polymarket dashboard (Settings → API Keys).
- **Data sources**: register for polling aggregators (FiveThirtyEight, RealClearPolitics), futures-implied probabilities (CME FedWatch), and sports-statistics feeds relevant to your target categories.
- **Environment variables**: store `POLYMARKET_API_KEY` and `POLYMARKET_SECRET` in `.env`; never hardcode secrets.
- **Model storage**: maintain a local SQLite database of resolved markets for calibration tracking.

## Common Issues / Troubleshooting

| Issue | Likely Cause | Solution |
|---|---|---|
| API rate-limit errors | Burst requests to /markets endpoint | Add 0.5–1.0 s delay; implement exponential backoff with jitter |
| Price shows 0.00 | Market closed or not yet active | Check `closed` flag; filter by `active` status in API params |
| Slippage on entry | Low liquidity — order exceeds book depth | Use limit orders at mid-price; split into multiple smaller orders |
| Resolution dispute | Ambiguous outcome or Oracle disagreement | Verify resolution rules before entry; avoid unclear sources |
| Model predictions consistently off | Model drift from stale base rates | Recalibrate weekly against resolved markets; track Brier score |
| Kelly recommends >100 % bankroll | Very high edge at low price | Cap max position at 15–25 % of bankroll regardless of Kelly output |

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Automated EV bot | 2–4 weeks | Script scans active markets daily, computes EV from calibrated model, submits limit orders via CLOB API. Compound returns through fractional Kelly sizing. Target 15–30 % annualized ROI. |
| Signal subscription | 1–3 months | Weekly Polymarket analysis with specific picks, full EV calculations, and position size guidance. Charge $50–200/month for real-time alerts via Telegram/Discord. |
| Managed account | 3–6 months | Operate a discretionary or systematic strategy for accredited investors. Whitelist addresses on Polymarket. Charge 20–30 % performance fee. |
| Cross-platform arb | On-going | Monitor price gaps between Polymarket and Kalshi, Metaculus, Manifold. Execute when spread exceeds transaction costs (fees + slippage). |
| Market-making / liquidity mining | On-going | Provide two-sided quotes on liquid markets to capture bid-ask spread. Requires automated quoting infrastructure and adverse-selection risk management. |

### Preparation

Before analyzing any market: define the universe of markets to monitor (by category, minimum liquidity, time-to-resolution range), calibrate the probability model against resolved markets, set up data pipelines for automatic price and volume ingestion, and establish bankroll management parameters — total allocation, per-market limits, and stop-loss rules for correlated exposures.

### Execution

During analysis sessions: scan all active markets for EV+ opportunities daily, verify model assumptions against current information, compute position sizes using fractional Kelly, place limit orders with documented rationale. Re-evaluate open positions after every material news event or significant price movement (>10%).

### Stewardship

Post-resolution: reconcile trade outcomes against model estimates, compute aggregate statistics (win rate, average EV captured, Sharpe ratio, Kelly growth rate), update the probability model with new outcome data, and prune markets from the monitored universe if they fail liquidity or resolution-quality thresholds. Maintain a trading journal with key analysis checkpoints for iterative improvement.
- [ ] Probability model calibrated on 50+ resolved markets (check Brier score < 0.20)
- [ ] Market liquidity confirmed sufficient for intended position size (10× the order minimum)
- [ ] Resolution source and rules verified from market description and event details
- [ ] Current market price fetched — stale data eliminated
- [ ] Position size respects fractional Kelly limits and portfolio correlation model
- [ ] Limit order constructed to minimize slippage (not market order)
- [ ] Trade logged with timestamp, price, edge, EV per share, and rationale
- [ ] Exit conditions (stop-profit / re-evaluation triggers) documented