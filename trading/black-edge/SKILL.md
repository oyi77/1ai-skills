---
name: black-edge
description: Apply institutional trading edge using order flow analysis, market microstructure, and dark pool signals.
domain: trading
tags:
- algorithms
- black
- edge
- markets
- trading
---
## Skill Definition

**Name:** `black-edge`

**Pattern:** `trading/black-edge`

**Description:** Reveals hidden market edges through alternative data synthesis, behavioral pattern analysis, and structural inefficiency detection. Combines quantitative signals with qualitative intelligence gathering.

---

## Implementation

Four-phase alternative data synthesis: satellite/web/credit card data, behavioral patterns, structural inefficiencies, and gray information networks.


### Phase 1: Alternative Data Synthesis

**Satellite Imagery Analysis (Retail/Logistics)**
- Parking lot occupancy rates at major retailers
- Shipping container volumes at ports
- Construction activity via drone imagery
- Energy flare patterns for production estimates

**Web Scraping Intelligence**
- Job posting velocity (hiring = growth)
- Product pricing changes across competitors
- Customer review sentiment trajectories
- Website traffic patterns (SimilarWeb data)

**Credit Card Transaction Aggregation**
- Consumer spending category shifts
- Geographic spending concentration
- Recurring revenue detection for SaaS
- Travel booking patterns

### Phase 2: Behavioral Pattern Detection

**Options Flow Analysis**
- Unusual volume in OTM calls before catalysts
- Put/call skew anomalies
- Block trade detection (>1000 contracts)
- Sweep vs. block differentiation

**Dark Pool Signature Recognition**
- Large off-exchange prints
- VWAP deviation patterns
- ATS (Alternative Trading System) flow concentration
- Institutional accumulation footprints

**Social Sentiment Edge**
- Reddit/WSB momentum pre-mainstream media
- Insider trading clusters (Form 4 filings)
- Short interest squeeze probability models
- Gamma exposure wall detection

### Phase 3: Structural Market Inefficiencies

**Microstructure Arbitrage**
- Order book imbalance detection
- Quote stuffing pattern recognition
- Latency arbitrage opportunities
- Market maker inventory signals

**ETF Creation/Redemption Dynamics**
- Premium/discount arbitrage
- Authorized participant flow tracking
- Basket trading vs. underlying divergence
- Creation unit threshold proximity

**Cross-Asset Correlation Breakdowns**
- Basis trade opportunities
- Pairs trading signal generation
- FX/commodity/equity divergence
- Volatility regime transitions

### Phase 4: The "Gray Information" Network

**Expert Network Synthesis**
- Former employee insights (legally obtained)
- Supply chain vendor intelligence
- Customer interviews (ground truth)
- Regulatory filing deep reads

**Channel Checks**
- Distributor inventory levels
- Carrier route utilization
- Component supplier utilization rates
- Semiconductor wafer starts

**Regulatory/Filing Forensics**
- 13F position change clustering
- Insider buying/selling pattern analysis
- SEC comment letter sentiment
- Patent filing acceleration/deceleration

---

## Black Edge Framework

The edge hierarchy from public information to proprietary networks, built on three pillars: signal detection, position sizing, and information security.


### Edge Hierarchy

```
Level 1: Public Information (Zero edge)
Level 2: Processed Public (Slight edge)
Level 3: Alternative Data (Real edge)
Level 4: Synthesized Intelligence (Significant edge)
Level 5: Proprietary Networks (Maximum edge) ← Black Edge territory
```

### The Three Pillars

**Pillar 1: Signal Detection**
- Build comprehensive alternative data feeds
- Cross-reference multiple non-correlated sources
- Identify leading indicators vs. lagging confirmations
- Backtest signal efficacy and decay rates

**Pillar 2: Position Sizing**
- Edge confidence score (0-100)
- Kelly Criterion adjusted for uncertainty
- Maximum position concentration limits
- Correlation risk across black edge positions

**Pillar 3: Information Security**
- Operational security for data sources
- Counter-surveillance on your own patterns
- Know when your edge is crowded
- Exit before edge arbitrage away

---

## Usage Examples

Practical scenarios: satellite retail analysis, options flow anomaly detection, and dark pool accumulation tracking.


### Example 1: Satellite Retail Analysis

```python
# Analyze parking lot data vs. consensus
## When to Use

**Trigger phrases:**
- "black edge"
- "Help me with black edge"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

parking_data = fetch_satellite_imagery(ticker="WMT")
consensus_revenue = get_analyst_estimates(ticker="WMT")

parking_trend = calculate_occupancy_trend(parking_data, period="3m")
expected_beat = parking_trend > consensus_revenue * 1.05

position_size = calculate_kelly_size(
    edge_confidence=85,
    historical_accuracy=0.72,
    payoff_ratio=2.5
)
```

### Example 2: Options Flow Anomaly

```python
# Detect unusual OTM call buying
flow = fetch_unusual_options_activity(
    min_volume=500,
    otm_percentage=10
)

sweeps = filter_sweep_orders(flow)
catalyst_date = find_next_catalyst(ticker=sweeps[0].ticker)

if sweeps.volume > 3 * avg_daily and days_to_catalyst < 30:
    signal_strength = "HIGH"
    position = buy_calls(sweeps[0], strike=sweeps[0].strike)
```

### Example 3: Dark Pool Accumulation

```python
# Identify institutional accumulation
dark_pool_prints = fetch_ats_volume(ticker="AAPL")

large_blocks = dark_pool_prints[
    dark_pool_prints.volume > 100000
    and dark_pool_prints.price > vwap
]

accumulation_score = calculate_accumulation(
    large_blocks, 
    lookback="20d"
)

if accumulation_score > 75 and price_near_support:
    entry = "LONG"
    target = calculate_measured_move("cup_and_handle")
```

---


Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

## Integration Points

**Cross-Skill Dependencies**
- `trading/crypto-trading-bot` - For microstructure analysis
- `trading/investing-algorithm-framework` - For prediction market sentiment
- `research/mckinsey-research` - For competitive intelligence frameworks
- `research/value-investing` - For fundamental overlay

**Data Source Requirements**
- Cignal AI / Thinknum (alternative data)
- Quiver Quantitative (political/wallstreetbets)
- Unusual Whales (options flow)
- Quiver Quant (insider trading)

---

## Risk Framework

Legal/regulatory risk, crowding risk, and operational risk with mitigation strategies and validation checklists.


### Black Edge Risks

**Legal/Regulatory Risk**
- MNPI (Material Non-Public Information) boundaries
- Insider trading statute compliance
- Data source terms of service
- Cross-border data restrictions

**Crowding Risk**
- Edge decay as more participants access same data
- Alpha arbitrage by sophisticated competitors
- Signal extraction costs rising
- Data provider exclusivity erosion

**Operational Risk**
- Alternative data quality issues
- False positive signal clusters
- Technology failure during execution
- Information leakage within firm

### Risk Mitigation

```python
# Edge Validation Checklist
edge_checks = {
    "legal_review": True,           # Counsel approved data sources
    "crowding_score": < 70,         # Not too many using same signal
    "backtest_alpha": > 0.15,       # 15% annual minimum
    "max_position": "portfolio_5%", # Concentration limit
    "information_security": "compartmentalized"
}
```

---

## Advanced Techniques

Information cascade modeling, counter-edge detection, and edge half-life tracking for sustained alpha generation.


### The "Information Cascade" Model

Sequence for maximum edge extraction:
1. **Ground Truth** (Channel checks, expert networks)
2. **Alternative Data** (Satellite, web scraping)
3. **Market Microstructure** (Options flow, dark pools)
4. **Sentiment Analysis** (Social media, prediction markets)
5. **Fundamental Validation** (Public filings overlay)

### Counter-Edge Detection

Know when you're being gamed:
- Quote stuffing preceding your entry
- Wash trading to trigger your signals
- Spoofing to create false liquidity
- Layering to manipulate order book

### The "Edge Half-Life" Concept

```
Timeframe    | Edge Duration
Day Trading  | 1-4 hours
Swing Trade  | 2-10 days
Position     | 2-8 weeks
Long-term    | 6-18 months
```

Monitor edge decay. When retail discovers your signal, it's time to evolve.

---

## Historical Precedents

**Renaissance Technologies (Medallion Fund)**
- Alternative data pioneers
- Satellite + weather data for commodities
- High-frequency signal extraction
- Maximum 5% edge concentration

**SAC Capital (Steven Cohen)**
- Expert network intelligence gathering
- "Edge" defined as information advantage
- Risk: Legal consequences for information boundaries

**Tiger Management (Julian Robertson)**
- Supply chain deep research
- Industry expert networks
- Fundamental + information synthesis

**Galleon Group (Raj Rajaratnam)**
- "Whisper networks" of insiders
- Cautionary tale: Edge crossed into illegality
- Lesson: Legal boundaries paramount

---

## Output Format

```yaml
black_edge_report:
  ticker: "AAPL"
  signal_type: "dark_pool_accumulation"
  confidence: 78
  pillar_scores:
    signal_detection: 85
    position_sizing: 70
    information_security: 80
  
  alternative_data:
    satellite: "parking_occupancy_up_12%"
    web_scraping: "job_postings_down_8%"
    credit_card: "spending_flat_qoq"
    
  market_microstructure:
    options_flow: "unusual_call_buying"
    dark_pool: "large_blocks_above_vwap"
    etf_premium: "slight_discount"
    
  edge_assessment:
    legal_status: "COMPLIANT"
    crowding_risk: "MODERATE"
    decay_timeline: "4-6_weeks"
    
  recommendation:
    action: "LONG"
    entry: "$175-180"
    target: "$210"
    stop: "$168"
    position_size: "4%_portfolio"
```

---

## Triggers

- `/black-edge analyze <ticker>` - Full edge assessment
- `/black-edge scan sector <sector>` - Find best opportunities
- `/black-edge validate <signal>` - Legal/compliance check
- `/black-edge monitor <position>` - Edge decay tracking

---

**Warning:** This skill operates at the frontier of information advantage. Always maintain strict legal and ethical boundaries. The goal is superior analysis, not insider trading. When in doubt, consult securities counsel.

**Donation:** Support development → https://www.tip.md/oyi77

## Evidence Standards (Non-Negotiable)

| Tier | Type | Weight | Verification | Examples |
|------|------|--------|--------------|----------|
| **T1** | Primary source | 1.0 | Direct URL + timestamp | Satellite imagery, on-chain data, SEC filings, options flow prints, dark pool tape, Form 4 insider filings, exchange order books |
| **T2** | Factual secondary | 0.7 | Cross-reference 2+ providers | Bloomberg/Reuters, Quiver Quant, Unusual Whales, Thinknum, Cignal AI, certified audits |
| **T3** | Opinion/social | 0.3 | Flag "speculative" | Reddit/WSB sentiment, Twitter/X, Discord, newsletters, YouTube analysts |

**Rules:**
1. No actionable recommendation (enter/exit/hedge) on T3-only evidence
2. Conviction score >0.5 requires >=50% T1/T2 weighted evidence
3. Every T3 claim must be paired with T1/T2 disconfirming evidence search
4. Always disclose evidence composition in every output

---

## Anti-Bias Checklist (Run Before Every Recommendation)

Six cognitive traps to evaluate before every recommendation to ensure evidence-driven decisions.

### 6 Cognitive Traps
- [ ] **Confirmation bias** -- Did I actively seek disconfirming alternative data points?
- [ ] **Anchoring** -- Am I over-weighting the first satellite/web-scraping signal?
- [ ] **Recency bias** -- Am I ignoring 3+ year historical pattern for this signal type?
- [ ] **Herd mentality** -- Is this edge already crowded (crowding score >70)?
- [ ] **Sunk cost** -- Am I defending a prior position because I invested in the research?
- [ ] **Overconfidence** -- Is my conviction score calibrated to evidence quality, not gut feel?

---

## Pre-Trade Risk Gate (5 Gates -- All Must Pass)

```
Gate 1: LIQUIDITY
  -> Daily volume >= 10x position size?
  -> Spread <0.5% (equities) / <0.1% (crypto large-cap)?
  -> Market cap: >$1B FULL | $100M-$1B REDUCED | <$100M SKIP
  -> Dark pool availability confirmed for entry?

Gate 2: CORRELATION
  -> 90d rolling correlation vs. portfolio <0.7?
  -> Sector concentration <30% at full Kelly?
  -> No >20% in single correlated cluster?
  -> Alternative data signal uncorrelated to existing positions?

Gate 3: SENTIMENT ALIGNMENT
  -> Dark pool flow direction aligns with thesis?
  -> Options flow confirms (not contradicts) positioning?
  -> Social sentiment not at speculative extreme (>80 Fear/Greed)?
  -> Insider activity (Form 4) aligns with signal direction?

Gate 4: MEMORY RECALL
  -> "Similar alternative data signals in past 2 years?"
  -> 3+ false positives for this signal type -> REDUCED
  -> Edge half-life tracked and within acceptable decay window?
  -> Behavioral drift detected -> SKIP until review

Gate 5: REGULATORY
  -> Data source legal in user jurisdiction?
  -> No MNPI (Material Non-Public Information) boundary crossed?
  -> Expert network engagement compliant with SEC guidelines?
  -> OFAC/SDN screening passed for counterparties?
  -> Data provider ToS permits intended use?

Output: FULL (proceed) | REDUCED (half size) | SKIP (block)
```

---

## When NOT to Use

- When you have no access to alternative data sources (satellite, web scraping, credit card transaction data)
- When relying exclusively on public financial statements and SEC filings (use `financial/all-in-one-finance` or `financial/wolf-finance` instead)
- When the time horizon is sub-minute scalping (alternative data signals have minimum half-life of hours, not milliseconds -- use `trading/crypto-trading-bot`)
- When legal/compliance review is unavailable and MNPI boundaries are unclear
- When the asset lacks sufficient options flow or dark pool data for microstructure analysis (micro-cap stocks, illiquid tokens)
- When you need standard fundamental valuation (DCF, earnings models, ratio analysis) without an information-asymmetry angle
- When the signal has already been discovered by the mainstream (edge decayed, crowding score >70)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I don't need satellite data, I'll just look at charts" | Satellite data catches demand shifts 2-6 weeks before they show in price; by then the edge is gone |
| "Options flow is too noisy, I'll skip it" | Unusual sweep activity preceded 78% of major catalyst moves in 2024; skipping it means flying blind |
| "Dark pool data is unreliable" | ATS prints above VWAP are institutional accumulation signatures with 65%+ directional accuracy |
| "I can just use Reddit sentiment alone" | Standalone social sentiment is T3 evidence (weight 0.3); without T1/T2 confirmation it is gambling, not edge |
| "Legal review slows me down, I'll skip compliance" | One MNPI violation can result in SEC enforcement, disgorgement, and criminal charges -- compliance is non-negotiable |
| "This edge has worked for months, no need to backtest decay" | Edge half-life for swing trades is 2-10 days; unmonitored decay turns alpha into negative alpha |
| "I'll just use one alternative data source" | Single-source signals have >40% false positive rate; cross-referencing 2+ non-correlated sources cuts this to <15% |

## Red Flags

- Using only social sentiment (Reddit/Twitter) without T1/T2 verification
- Ignoring dark pool divergences from public price action
- Acting on a single satellite image without trend confirmation
- Trading options flow signals without confirming via open interest and gamma exposure
- Bypassing legal/compliance review for expert network intelligence
- Claiming conviction >0.8 without T1 primary source evidence
- Ignoring crowding metrics on a well-known alternative data source
- Taking positions exceeding 5% portfolio concentration on a single black edge signal
- Skipping edge half-life estimation before position entry
- Using data that could constitute MNPI without counsel review

## Verification

After completing this skill, confirm:

- [ ] Alternative data sources verified (minimum 2 non-correlated T1/T2 sources)
- [ ] Options flow confirmed by 2+ providers (e.g., Unusual Whales + CBOE data)
- [ ] Dark pool signatures cross-referenced with ATS volume data
- [ ] Legal/compliance review completed for all data sources used
- [ ] Evidence composition disclosed in output (T1/T2/T3 percentages)
- [ ] Edge crowding score <70 before position entry
- [ ] Edge half-life estimated and within acceptable decay window
- [ ] All 5 pre-trade risk gates passed (Liquidity, Correlation, Sentiment, Memory, Regulatory)
- [ ] Anti-bias checklist completed with documented disconfirming evidence search
- [ ] Position sizing conforms to Kelly Criterion adjusted for uncertainty

---

**Cross-reference:** For complete financial analysis framework (fundamental, technical, risk management), also see `financial/all-in-one-finance` and `financial/wolf-finance`.

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
