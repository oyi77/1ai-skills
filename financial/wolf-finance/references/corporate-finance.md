# fin-corporate-finance: M&A, Capital Structure & Corporate Transactions

**REQUIRED SUB-SKILL:** Load `equity-fundamental.md` for target company analysis. Load `risk-guardian.md` for portfolio impact.

---

## Mergers & Acquisitions (M&A)

### Deal Structure Types
| Structure | Tax Treatment | Speed | Complexity | Best For |
|-----------|--------------|-------|------------|----------|
| **Stock Purchase** | Carryover basis | Medium | Low | Clean targets, no liabilities |
| **Asset Purchase** | Step-up basis (buyer benefit) | Medium | High | Distressed, selective assets |
| **Merger (Statutory)** | Varies (tax-free if stock-for-stock) | Slow | Medium | Public company acquisitions |
| **Reverse Merger** | Varies | Fast | Medium | Private company going public |
| **Tender Offer** | Capital gains for shareholders | Fast | Medium | Hostile or friendly public targets |

### Valuation Methodologies (Triangulation Required)
```
1. DCF (Intrinsic Value)
   → 5–10yr projected FCF + Terminal Value
   → WACC as discount rate
   → Sensitivity: WACC ±1%, terminal growth ±0.5%

2. Comparable Companies (Trading Comps)
   → EV/EBITDA, P/E, EV/Revenue, EV/FCF
   → Premium/discount to peer median justified by quality/growth/moat

3. Precedent Transactions (Deal Comps)
   → Control premium: typically 20–40% over pre-announcement price
   → Source: CapIQ, Bloomberg, Mergermarket

4. LBO Floor Value
   → Maximum price PE sponsor can pay and still hit 20–25% IRR
   → Tests downside discipline

5. Sum of Parts (SOTP)
   → For conglomerates, segment-by-segment valuation
   → Often reveals "conglomerate discount"
```

### Synergy Framework
```
Revenue Synergies (Harder to achieve, 2–4 year realization):
  → Cross-selling: TAM expansion
  → Pricing power: reduced competition
  → Geographic expansion, new distribution channels
  → Apply 30–50% haircut to stated projections (optimism bias)

Cost Synergies (More reliable, 1–2 year realization):
  → Headcount reduction (G&A overlap)
  → Procurement leverage (vendor consolidation)
  → IT consolidation, real estate rationalization
  → Apply 20–30% haircut to stated projections

One-time Transaction Costs (Always model separately):
  → Investment banking fees: 1–2% deal value
  → Legal/accounting: 0.5–1%
  → Integration costs: 2–5% of combined revenue (year 1–2)
```

### Accretion/Dilution Analysis
```
Accretion = Acquirer EPS increases post-merger (good for stock price)
Dilution = Acquirer EPS decreases post-merger (bad signal)

Key drivers:
  → Deal price vs. target earnings
  → Mix of cash vs. stock consideration
  → Synergies achieved vs. integration costs
  → Financing cost (interest on debt used)

Rule of thumb: >15% EPS accretion = strong deal for acquirer shareholders
```

---

## Leveraged Buyout (LBO) Model

### LBO Return Drivers (Value Creation)
1. **Earnings growth** — EBITDA expansion during hold period
2. **Multiple expansion** — Buy at 7× EBITDA, sell at 9× EBITDA
3. **Debt paydown** — Leverage reduction increases equity value
4. **Dividends/recap** — Extract cash before exit (controversial)

### LBO Capital Structure (Typical)
```
Senior Secured Debt (Term Loan A/B):  40–50% of total cap
Subordinated / Mezzanine Debt:         10–20%
High Yield Bonds:                       0–20%
Equity (PE Sponsor + Mgmt rollover):   30–40%

Target leverage: 4–6× EBITDA at entry
Exit leverage: 2–3× EBITDA at sale (debt paydown)
```

### PE Return Benchmarks
| IRR | Multiple (MoIC) | Quality |
|-----|-----------------|---------|
| >25% | >3.0× | Exceptional (top quartile) |
| 20–25% | 2.5–3.0× | Strong (second quartile) |
| 15–20% | 2.0–2.5× | Acceptable |
| <15% | <2.0× | Below hurdle rate |

---

## WACC (Weighted Average Cost of Capital)

```
WACC = (E/V × Ke) + (D/V × Kd × (1 – Tax Rate))

Where:
  E = Market value of equity
  D = Market value of debt
  V = E + D
  Ke = Cost of equity (CAPM: Rf + β × ERP)
  Kd = Cost of debt (pre-tax yield)
  ERP = Equity Risk Premium (~5.0–6.0% for US)
  Rf = Risk-free rate (current 10y Treasury yield)

Size Premium Adjustment:
  Large cap (>$10B): 0%
  Mid cap ($2B–$10B): +1–1.5%
  Small cap ($300M–$2B): +2–3%
  Micro cap (<$300M): +3–5%
```

---

## IPO Analysis Framework

### Pre-IPO Due Diligence
1. **S-1 analysis**: Revenue quality, growth trajectory, path to profitability
2. **Comparable public companies**: Peer multiple at IPO discount (15–20% typical)
3. **Lock-up expiration risk**: 90–180d lock-up → insider selling pressure
4. **Underwriter credibility**: Goldman/MS/JPM tier vs. mid-tier bankers
5. **Anchor investors**: Quality of cornerstone book (institutions vs. retail)
6. **Pre-IPO cap table**: Founder/VC ownership, existing preferred overhang

### IPO Pricing Signals
- **Oversubscribed (>10×)**: Expect pop on first day, but watch for quick reversal
- **Price at top/above range**: Strong demand, post-IPO supply overhang risk
- **Price below range**: Weak demand, potential continued selling
- **Retail vs. institutional mix**: >50% retail → momentum, higher volatility

---

## Capital Structure Optimization

### Modigliani-Miller in Practice
- **Optimal leverage**: Balance tax shield (debt interest deductible) vs. financial distress costs
- **Pecking order theory**: Internal funds → debt → equity (equity issuance = expensive signal)
- **Agency costs**: Too much debt → underinvestment; too little → empire building

### Credit Metrics (Watch Levels)
| Metric | Investment Grade | Speculative | Distressed |
|--------|-----------------|-------------|------------|
| Net Debt/EBITDA | <2.0× | 2.0–5.0× | >5.0× |
| Interest Coverage (EBIT/Interest) | >5× | 2–5× | <2× |
| FCF/Debt Service | >1.5× | 1.0–1.5× | <1.0× |
| Debt/Equity | <50% | 50–100% | >100% |

---

## Dividend & Capital Return Analysis

### Capital Return Hierarchy (Shareholder Value)
1. **Organic reinvestment** (highest ROIC projects) — best if ROIC > WACC
2. **Strategic M&A** — only if creates value, not empire building
3. **Debt repayment** — especially with floating-rate debt rising
4. **Share buybacks** — optimal if stock trading below intrinsic value
5. **Dividends** — stable, but sticky; cutting = severe signal

### Buyback Quality Check
- Are shares bought back at/below intrinsic value? (Good: value-enhancing)
- Are buybacks funded by debt at low rates? (Watch: leverage creep)
- Is management using buybacks to offset dilutive stock comp? (Neutral)
- Do buybacks consistently happen at market peaks? (Bad: value destructive)

---

## Corporate Finance Output Template

```
TRANSACTION / COMPANY: [Name]
ANALYSIS TYPE: [M&A / LBO / IPO / Capital Return]

VALUATION:
  Method 1 (DCF):      $X–Y per share
  Method 2 (Comps):    $X–Y (EV/EBITDA: Xz)
  Method 3 (Precedent):$X–Y (control premium: X%)
  Weighted Midpoint:   $X

ACCRETION/DILUTION: [+X% / –X% to acquirer EPS]
SYNERGIES (NPV):    $XM revenue / $XM cost (haircut applied)
IRR (if LBO):       X%
MOIC (if PE):       X.Xz

GATE RESULT:        [FULL / REDUCED / SKIP]
CONVICTION SCORE:   [0.00–1.00]
EVIDENCE MIX:       T1: X% | T2: X% | T3: X%
```
