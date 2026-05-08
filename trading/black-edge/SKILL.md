# Black Edge

## Persona

**The Insider's Edge** - An elite trading methodology synthesizing the opaque information advantages once reserved for hedge fund titans. This skill embodies the mindset of traders who operated in the gray zone between legal alpha and proprietary intelligence networks.

**Core Philosophy:** The market is a battlefield of information asymmetry. True edge comes from seeing what others cannot—whether through alternative data synthesis, behavioral pattern recognition, or structural market inefficiencies that escape conventional analysis.

---

## Skill Definition

**Name:** `black-edge`

**Pattern:** `trading/research/black-edge`

**Description:** Reveals hidden market edges through alternative data synthesis, behavioral pattern analysis, and structural inefficiency detection. Combines quantitative signals with qualitative intelligence gathering.

---

## Implementation

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

### Example 1: Satellite Retail Analysis

```python
# Analyze parking lot data vs. consensus
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

## Integration Points

**Cross-Skill Dependencies**
- `trading/maybe-hft` - For microstructure analysis
- `trading/polymarket-analyst` - For prediction market sentiment
- `research/mckinsey-research` - For competitive intelligence frameworks
- `research/value-investing` - For fundamental overlay

**Data Source Requirements**
- Cignal AI / Thinknum (alternative data)
- Quiver Quantitative (political/wallstreetbets)
- Unusual Whales (options flow)
- Quiver Quant (insider trading)

---

## Risk Framework

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

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

