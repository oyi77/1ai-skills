# fin-equity-fundamental: Deep Fundamental Analysis

**REQUIRED SUB-SKILL:** Load `risk-guardian.md` before finalizing any position size recommendation.

## 20-Module Analysis Framework (A–T)

Run all modules for full investment memo. For quick queries: A–C + K + P minimum.

---

### A — Revenue Quality & Composition
- **Recurring vs. one-time**: Subscription ARR, license vs. services, government contracts
- **Concentration risk**: Top 3 customers as % of total revenue (>20% = red flag)
- **Organic vs. acquired growth**: Pro-forma adjustments quality check
- **Revenue recognition**: Point-in-time vs. over-time; red flag = accelerating deferred revenue burn
- **Geographic breakdown**: Emerging market exposure, FX translation impact
- **Seasonality**: Q4 skew, cyclical patterns, working capital swings

### B — Profitability Trajectory & Margins
- **Gross margin trend** (3–5 years): Expanding = pricing power; compressing = competition/input costs
- **Operating leverage**: Revenue growing faster than OpEx = scalable model
- **Net margin sustainability**: Strip one-time items, restructuring charges, goodwill impairment
- **EBITDA quality**: Add-backs must be <15% of EBITDA; exclude stock-based comp if >10% revenue
- **FCF conversion**: FCF/Net Income >1.0 = high quality; <0.7 = accrual risk

### C — Cash Flow Integrity & Manipulation Detection
- **FCF = Operating CF – CapEx** (maintenance vs. growth CapEx split)
- **Accrual ratio** = (Net Income – FCF) / Avg Total Assets; >5% = manipulation risk
- **Beneish M-Score**: 8-variable model; score >–1.78 suggests earnings manipulation
- **Piotroski F-Score**: 9-point financial strength score (≥7 = strong)
- **CFO vs. Net Income trend**: Divergence >2 years = quality concern
- **CapEx intensity**: Maintenance CapEx as % of D&A (should be ~80–100%)

### D — Forward Guidance & Management Credibility
- **Historical guidance accuracy**: Beat/miss pattern over last 8 quarters
- **Capital allocation track record**: Buyback timing (shares retired at fair value?), M&A ROIC
- **Insider alignment**: Executive comp structure (performance-based vs. time-based), stock ownership
- **10b5-1 plans**: Scheduled sales vs. discretionary dumps
- **Earnings call tone analysis**: Sentiment drift, avoidance of direct questions
- **Restatement history**: Accounting revisions, non-relapse commitment

### E — Competitive Landscape & TAM
- **Porter's Five Forces** rapid assessment (threat of entry, supplier power, buyer power, substitutes, rivalry)
- **Market share trend**: Gaining/holding/losing vs. competitors
- **TAM methodology**: Bottom-up (preferred) vs. top-down; growth assumptions sanity check
- **Disruption timeline**: Threat from substitutes (AI, automation, regulatory shifts)
- **Moat assessment**: Network effects, switching costs, intangible assets, cost advantages
- **Competitive response**: Pricing pressure, new product cycles, patent cliffs

### F — Core KPIs & Unit Economics (by Sector)
- **SaaS**: ARR, NRR (>110% = strong), CAC payback (<18 months), LTV/CAC (>3x), magic number (>0.8)
- **Retail**: SSS (same-store sales), inventory turns, GMROI, e-commerce penetration %
- **Industrial**: Utilization rates, backlog, book-to-bill ratio, days sales outstanding
- **Financials**: NIM, ROA, ROE, efficiency ratio, NPL ratio, CET1 ratio
- **Healthcare**: Pipeline NPV, phase success rates, patent cliff exposure, reimbursement risk
- **Always compare vs. sector median and best-in-class benchmarks**

### G — Product Pipeline & Innovation Cycle
- **R&D efficiency**: Revenue per R&D dollar (improving = positive)
- **Patent portfolio**: Quality (citations, family size), expiry schedule (cliff risk)
- **Product launch cadence**: Success rate, time-to-market vs. competitors
- **Technology debt**: Legacy platform risk, migration costs, technical obsolescence
- **Acqui-hires vs. organic R&D**: Quality of innovation sources
- **Open-source exposure**: Dependency on OSS, contribution vs. free-riding

### H — Partner Ecosystem & Supply Chain Resilience
- **Supplier concentration**: >30% from single supplier = flag; dual-sourcing assessment
- **Geographic risk**: China/Taiwan exposure, friend-shoring progress, inventory days
- **Customer stickiness**: Contractual lock-in, switching costs, multi-year agreements
- **Channel partner health**: Margin structure, exclusivity terms, channel stuffing risk
- **Inventory quality**: FIFO/LIFO, write-down history, obsolescence reserves
- **Logistics resilience**: Port dependency, freight cost pass-through, 3PL relationships

### I — Executive Team & Capital Allocation Priorities
- **C-suite tenure**: >5 years average = stability; <2 years = turnover risk
- **Founder-led premium**: >10% insider ownership, vision alignment
- **Capital allocation hierarchy**: R&D > organic CapEx > M&A > buybacks > dividends (growth)
- **Related-party transactions**: Disclosures, fairness opinions, independent director approval
- **Board independence**: <30% affiliated directors; audit committee financial expertise
- **Succession planning**: CEO/CFO replacement readiness, internal talent pipeline

### J — Macro & Policy Sensitivity
- **Interest rate duration**: Debt maturity profile, floating rate exposure, refinancing risk
- **FX exposure**: % revenue from international markets, natural hedges, hedging policy effectiveness
- **Regulatory tail risk**: Pending legislation (antitrust, privacy, ESG), compliance costs
- **Sector cyclicality**: Beta vs. market, correlation with credit cycle, recession resilience
- **Fiscal policy exposure**: Infrastructure spend, subsidies, tax reform impact
- **Climate risk**: Physical (assets) + transition (stranded assets), TCFD disclosure quality

### K — Multi-Method Valuation Matrix

| Method | Best For | Key Inputs | Weight (Growth/Mature) |
|--------|----------|-----------|------------------------|
| **DCF** | Cash-generative, predictable | WACC, terminal growth, FCF projections | 40% / 60% |
| **PEG Ratio** | Growth stocks | P/E ÷ EPS growth; <1.0 = undervalued | 15% / 5% |
| **EV/EBITDA** | Capital-intensive, leveraged | Peer median comparison, lease adjustments | 20% / 25% |
| **Owner Earnings** | Buffett-style | Net income + D&A – maintenance CapEx | 10% / 20% |
| **Reverse DCF** | All (sanity check) | What growth rate justifies current price? | 10% / 10% |
| **Rule of 40** | SaaS | Revenue growth % + FCF margin % ≥40 = healthy | 5% / 0% |
| **P/B, P/S** | Asset-heavy, pre-profit | Book value quality, revenue multiples | 0% / 15% |

**Output**: Fair value range (bear / base / bull), implied upside/downside, margin of safety %

### L — Ownership Structure & Insider Activity
- **Institutional ownership**: 13F changes (last 2 quarters), activist investor presence
- **Insider buy/sell ratio**: Net buying 3-month window; Form 4 analysis
- **Short interest**: >15% float = crowded short OR high conviction; days-to-cover
- **Index inclusion/exclusion**: Passive flow impact (S&P 500, Russell, MSCI rebalancing)
- **Retail sentiment**: Reddit/WallStreetBets mentions, retail brokerage flow data
- **Insider trading litigation**: SEC actions, 10b5-1 plan timing vs. news releases

### M — Long-Term Monitoring Dashboard
- **R&D efficiency trend**: Revenue per R&D dollar (improving = positive)
- **Customer acquisition**: CAC inflation = demand saturation signal; churn rate trend
- **Employee satisfaction**: Glassdoor trend as leading indicator of culture/retention
- **ESG controversy score**: MSCI评级变化, climate litigation, labor disputes
- **Debt covenant compliance**: Headroom, waiver history, springing covenants
- **Tax rate sustainability**: Low-tax jurisdictions, OECD Pillar Two impact modeling

### N — Accounting Quality & Forensic Red Flags
- **Beneish M-Score**: 8 variables (DSRI, GMI, AQI, SGI, DEPI, SGAI, TATA, LVGI); >–1.78 = manipulation risk
- **Altman Z-Score**: Z > 2.99 = Safe; 1.81–2.99 = Grey; <1.81 = Distress
- **Piotroski F-Score**: 9 points (profitability: ROA, CFO; leverage: ΔLEV, ΔLIQ; efficiency: ΔMARGIN, ΔTURN)
- **Aggressive accounting**: LIFO→FIFO switches, pension assumption changes, SBC capitalization
- **Off-balance-sheet**: Operating leases (ASC 842), VIEs, guarantees, contingent liabilities
- **Related-party**: Transactions with subsidiaries, JVs, executive-linked entities

### O — ESG Integration & Regulatory Exposure
- **MSCI ESG rating**: Trend (AAA→BBB), controversy flags, peer percentile
- **Scope 1/2/3 emissions**: Trajectory vs. Net Zero commitments, carbon pricing exposure
- **Governance**: Board independence, dual-class shares, poison pills, shareholder rights
- **Social**: Labor relations, supply chain labor standards, data privacy breaches
- **Regulatory pipeline**: Upcoming legislation impact (AI regulation, privacy laws, antitrust)
- **TCFD alignment**: Climate risk disclosure quality, scenario analysis rigor

### P — Variant View & Consensus Blind Spots (Alpha Generator)
- **State consensus explicitly**: What is the 80% view on this stock?
- **Market pricing**: What is already discounted in current valuation?
- **Variant view articulation**: Specific evidence contradicting consensus
- **Pre-mortem**: If thesis is wrong in 12 months, what caused it? (3 scenarios)
- **Black swan hedging**: Tail risks not in base case (regulatory ban, tech obsolescence)
- **Activist target**: Is company vulnerable to proxy fight, breakup, strategic review?

### Q — Credit Analysis (Bondholders' Perspective)
- **Interest coverage**: EBIT / interest expense; <2.0x = concern
- **Debt/EBITDA**: <3.0x = investment grade; >4.0x = high yield; >5.0x = distressed
- **Covenant package**: Incurrence vs. maintenance, restricted payments, liens
- **Maturity wall**: Next 3 years' debt due, refinancing risk at higher rates
- **Asset liens**: Secured vs. unsecured debt, collateral coverage ratio
- **Credit default swap (CDS) spreads**: Widening = market concern

### R — Dividend & Buyback Sustainability
- **Dividend coverage**: FCF / dividends; <1.2x = cut risk
- **Payout ratio**: Dividends / earnings; >80% = unsustainable
- **Buyback effectiveness**: Shares outstanding trend, average repurchase price vs. current
- **Dividend aristocrat status**: 25+ years of increases = quality signal
- **Special dividends**: One-time returns of capital, balance sheet excess cash
- **Management guidance**: Payout policy statements, capital return commitments

### S — Scenario Analysis & Stress Testing
- **Base case**: Consensus GDP, no shocks, 3-year projection
- **Bear case**: Recession, margin compression, multiple contraction (P/E → 12x)
- **Bull case**: Market share gains, margin expansion, multiple expansion (P/E → 20x)
- **Liquidation value**: Asset-based floor (NCAV, book value per share)
- **Acquisition premium**: Takeover multiple (1.3x–2.0x revenue for SaaS)
- **Probability-weighted NPV**: Assign probabilities to each scenario, sum PV

### T — Peer Group Comparison Matrix
- **Direct comps**: 3–5 closest peers by business model, geography, size
- **Relative valuation**: Where trades vs. peers on P/E, EV/EBITDA, P/S
- **Quality differential**: ROIC, moat strength, balance sheet vs. peers
- **Growth differential**: Revenue CAGR, market share momentum vs. peers
- **Capital allocation**: Better/worse capital deployer than peer median?
- **Discount/premium justification**: Why market misprices vs. peers (or vice versa)

---

## Investment Memo Output Template

```
COMPANY: [$TICKER] | [Company Name]
DATE: [YYYY-MM-DD]
ANALYST CONVICTION: [0.0–1.0] | EVIDENCE: T1:[%] T2:[%] T3:[%]
RECOMMENDATION: BUY / ACCUMULATE / HOLD / REDUCE / SELL / AVOID
ACTION PRICE: $[entry] | FAIR VALUE: $[base] ($[bear]–$[bull])
POSITION SIZE: [X%] portfolio | GATE STATUS: FULL / REDUCED / SKIP
TIME HORIZON: [months] | STOP LOSS: $[price] or [X%] drawdown

THESIS (3 bullets):
• [Core bull/bear case]
• [Key catalyst within 12 months]
• [Margin of safety or upside driver]

VARIANT VIEW / PRE-MORTEM:
Consensus says: [what 80% believe]
My variant: [contrarian evidence]
If wrong in 12mo: [3 failure scenarios with probabilities]

VALUATION SUMMARY:
Method          | Weight | Value    | Upside
DCF             | 40%    | $[X]     | +X%
EV/EBITDA       | 25%    | $[X]     | +X%
Owner Earnings  | 20%    | $[X]     | +X%
PEG             | 15%    | $[X]     | +X%
Weighted Avg    | 100%   | $[X]     | +X%

RISK FACTORS (Top 3):
1. [Risk] — Mitigation: [action]
2. [Risk] — Mitigation: [action]
3. [Risk] — Mitigation: [action]

ADD TRIGGERS: [conditions to double down]
TRIM TRIGGERS: [conditions to reduce 50%]
EXIT TRIGGERS: [conditions to close entirely]

EVIDENCE MAP:
[T1] SEC 10-K [URL] — [key finding]
[T1] Earnings transcript [URL] — [key finding]
[T2] Bloomberg consensus — [key finding]
[T3] [analyst name] report — FLAG speculative
```

---

## Quick Reference: Quality Score (0–100)

| Category | Weight | Metric | Score |
|----------|--------|---------|-------|
| Revenue Quality | 15% | Recurring %, concentration, growth | /15 |
| Profitability | 20% | Margins, FCF conversion, ROIC | /20 |
| Management | 15% | Insider buys, capital allocation, tenure | /15 |
| Moat/Competitive | 15% | Porter's 5, market share trend | /15 |
| Balance Sheet | 15% | Debt/Equity, interest coverage, liquidity | /15 |
| Valuation | 10% | DCF + comps, margin of safety | /10 |
| ESG/Governance | 10% | Board independence, controversies | /10 |

**Total Quality Score: /100 → A (90+), B (75–89), C (60–74), D (<60)**
