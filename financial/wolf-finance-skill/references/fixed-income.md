# fin-fixed-income: Bonds, Credit, and Rates Analysis

**REQUIRED SUB-SKILL:** Load `macro-liquidity.md` for yield curve context. Load `risk-guardian.md` for duration risk.

## Fixed Income Universe

| Instrument | Risk | Return | Liquidity | Use Case |
|------------|------|---------|-----------|----------|
| **Treasury Bills** (0–1y) | Near zero | Low | Excellent | Cash equivalent, parking |
| **Treasury Notes** (2–10y) | Low–moderate | Medium | Excellent | Duration hedge, curve plays |
| **Treasury Bonds** (20–30y) | Moderate | Higher | Good | Long-duration, pension matching |
| **TIPS** | Inflation-linked | Real yield | Good | Inflation hedge |
| **Municipal Bonds** | Tax-advantaged | Tax-equivalent yield | Varies | High tax bracket investors |
| **Corporate IG** (A–BBB) | Low–moderate | Credit spread | Good | Yield pickup over Treasuries |
| **Corporate HY** (BB–C) | High | High yield | Lower | Risk-on, recovery play |
| **Convertible Bonds** | Equity upside | Bond floor + option | Lower | Equity替代 with downside protection |
| **MBS/ABS** | Prepayment risk | Spread over Treasuries | Varies | Yield enhancement, securitized exposure |

---

## Yield Curve Analysis

### Curve Shapes & Implications

| Shape | Description | Economic Signal | Strategy |
|-------|-------------|-----------------|----------|
| **Normal** | 10y > 2y > 3m | Healthy growth | Barbell (short + long) |
| **Inverted** | 3m > 2y > 10y | Recession warning (6–18mo) | Short duration, cash, quality |
| **Steepening** | 10y–2y spread widening | Recovery / growth | Long duration, steepener trades |
| **Flat** | 10y ≈ 2y ≈ 3m | Transition / uncertainty | Neutral duration, credit spread trades |
| **Bear Flattening** | Rates up, curve flattens | Tightening / growth | Underweight duration, credit cautious |
| **Bull Flattening** | Rates down, curve flattens | Slowing growth | Long duration, quality spread compression |

### Key Spreads to Monitor
- **2s10s** (10y–2y): >0.50% normal; <0 inverted; <–0.50% deep inversion
- **3m10y** (10y–3m): Most reliable recession predictor (inverts → recession)
- **10y–TIPS** (Breakeven): >2.5% = high inflation expectations; <1.5% = deflation risk
- **OIS–Libor/SOFR spread**: Banking sector stress indicator

---

## Duration & Convexity

### Duration Measures
- **Macaulay Duration**: Weighted avg time to receive cash flows (years)
- **Modified Duration**: % price change for 1% rate change (≈ Macaulay / (1+yield))
- **Effective Duration**: For bonds with embedded options (callable, MBS)
- **Key Rate Duration**: Sensitivity to specific points on yield curve

### Rules of Thumb
- Duration ≈ maturity for zero-coupon bonds
- Duration < maturity for coupon-paying bonds (higher coupon = lower duration)
- 1% rate increase → price drop ≈ duration % (e.g., 5y duration → –5% price)
- **Convexity**: Curvature benefit; better convexity = less price drop when rates rise

### Hedging Duration Risk
- **Sell Treasury futures**: Short 10y/30y futures to offset duration
- **Interest rate swaps**: Pay fixed, receive floating (benefits if rates rise)
- **Options**: Buy puts on TLT (20y+ Treasury ETF) or call on TBT (inverse 20y)

---

## Credit Analysis Framework

### Investment Grade (IG): AAA → BBB–

| Rating | Spread vs. Treasury | Default Probability (5y) | Key Risk |
|--------|----------------------|--------------------------|---------|
| **AAA** | +0.3–0.5% | <0.1% | Sovereign/megacap only |
| **AA** | +0.5–0.8% | <0.3% | Large corps, stable CF |
| **A** | +0.8–1.5% | <0.5% | Solid IG, cyclical okay |
| **BBB** | +1.5–2.5% | 1–2% | Last IG rung, downgrade risk |

### High Yield (HY): BB+ → C

| Rating | Spread vs. Treasury | Default Probability (5y) | Key Risk |
|--------|----------------------|--------------------------|---------|
| **BB** | +3–5% | 2–5% | Fallen angels, recovery plays |
| **B** | +5–8% | 5–15% | Leveraged, cyclical, stressed |
| **CCC/C** | +8–15%+ | 15–40%+ | Distressed, restructuring |

### Credit Spread Drivers
- **Business risk**: Sector cyclicality, competitive position, regulatory
- **Financial risk**: Leverage (Debt/EBITDA), interest coverage, maturity wall
- **Market risk**: Risk-on/risk-off, liquidity, mutual fund flows
- **Event risk**: M&A, LBO, spin-offs, litigation, ESG shocks

---

## Bond Valuation & Relative Value

### Yield Measures
- **Current Yield**: Annual coupon / current price (ignores principal, reinvestment)
- **Yield to Maturity (YTM)**: IRR of all cash flows at current price
- **Yield to Worst (YTW)**: Minimum of YTM, YTC (call), YTP (put)
- **Option-Adjusted Spread (OAS)**: Spread after adjusting for embedded options
- **Z-Spread**: Spread over zero-coupon curve (measures credit + liquidity)

### Relative Value Scoring
```
Score = (Carry + Roll-down + Convexity Benefit) – (Duration Risk + Credit Risk)

Carry: Coupon – Financing cost (repo)
Roll-down: Price gain as bond "rolls down" curve (shorter maturity = higher price)
Convexity: Second-order benefit (gains > losses for equal rate moves)
```

### Screen for Value
1. **Cheapest-to-deliver (CTD)**: In futures delivery basket, which bond is cheapest?
2. **New issue concession**: New bonds often price 5–15bps cheap to secondary
3. **Best-value on curve**: 5y vs. 7y vs. 10y — which has best roll-down?
4. **Cross-market**: US vs. German vs. UK yields — relative attractiveness

---

## Municipal Bonds (US Focus)

### Tax-Equivalent Yield (TEY)
```
TEY = Municipal Yield / (1 – Marginal Tax Rate)
Example: 3.0% muni yield, 37% tax rate → TEY = 3.0% / 0.63 = 4.76%
```

### Credit Quality in Munis
- **General Obligation (GO)**: Backed by full faith & credit of issuer (safest)
- **Revenue Bonds**: Backed by project cash flows (toll roads, airports, utilities)
- **Conduit Bonds**: Private entity uses municipal issuer as conduit (higher risk)
- **State ratings**: Illinois, New Jersey (weak); Utah, Tennessee (strong)

### Key Risks
- **Interest rate risk**: Duration similar to Treasuries
- **Call risk**: Issuers refinance when rates fall (reinvestment risk)
- **AMT risk**: Alternative Minimum Tax may apply to private-activity bonds
- **State fiscal health**: Pension underfunding, revenue volatility

---

## Mortgage-Backed Securities (MBS)

### Prepayment Risk
- **PSA model**: 100 PSA = 6% annual prepayment; 200 PSA = 12% (faster prepay)
- **Refinancing incentive**: When mortgage rate < coupon – 100–150bps, prepays accelerate
- **Turnover**: Home sales drive prepays (housing turnover ~5%/year)
- **Burnout**: Highly refinanced pools have lower remaining prepayment risk

### MBS Valuation
- **Pool selection**: New issue vs. seasoned, high/low FICO, LTV ratios
- **Specified pools**: Targeted characteristics (low balance, streaming, disaster areas)
- **TBA (To-Be-Announced)**: Forward MBS delivery, dollar roll implied financing
- **Agency vs. Non-Agency**: GSE-backed (AAA) vs. private-label (credit risk)

---

## Portfolio Construction with Fixed Income

### Laddering Strategy
- **Equal weight** across maturities (1y, 2y, 3y... 10y)
- **Benefits**: Reinvestment risk diversication, liquidity at regular intervals
- **Rebalancing**: As bonds mature, reinvest at long end (maintain ladder)

### Barbell Strategy
- **Short end** (1–2y) + **Long end** (10–30y), skip intermediate
- **Benefit**: Liquidity (short) + yield (long), no middle-duration drag
- **Bull steepener**: Profits if curve steepens (long rallies, short stable)

### Bullet Strategy
- **Concentrate** at single maturity (e.g., all 5y bonds)
- **Use case**: Funding a known liability (pension payout, college tuition)
- **Risk**: Reinvestment risk if rates lower at maturity

### Credit Allocation
- **Core**: 60% IG (A–BBB), 20% HY (BB), 20% Treasuries
- **Aggressive**: 40% IG, 40% HY (B), 20% Equities/alternatives
- **Defensive**: 80% Treasuries/TIPS, 15% IG (A–AA), 5% Gold/alternatives

---

## Risk Metrics for Fixed Income

| Metric | Formula | Interpretation |
|--------|----------|----------------|
| **Duration** | Σ (t × PV(CFt)) / Price | % price change for 1% rate shift |
| **Convexity** | ΔDuration / ΔYield | Curvature benefit (always positive) |
| **Spread Duration** | Sensitivity to credit spread change | HY bonds have high spread duration |
| **Yield Beta** | ΔBond Yield / ΔBenchmark Yield | Correlation with Treasury curve |
| **VaR (95%, 1d)** | Historical/parametric | Max loss 95% of days |
| **Expected Shortfall** | Avg loss beyond VaR | Tail risk measure |

---

## Output Template: Bond Analysis

```
BOND: [ISIN/CUSIP] | [Issuer] | [Coupon%] | [Maturity]
DATE: [YYYY-MM-DD]
RATING: [Moody's/S&P/Fitch] | Outlook: [Stable/Negative/Positive]

YIELD & VALUATION:
  Current Yield: [%] | YTM: [%] | YTW: [%]
  Z-Spread: [bps] vs. Treasury | OAS: [bps] (if callable)
  Price: $[] (Par: $100) | Duration: [years] | Convexity: []

RELATIVE VALUE:
  vs. Treasury: +[bps] (cheap/fair/rich)
  vs. Sector peers: +[bps] (cheap/fair/rich)
  New issue concession: [bps] (if applicable)

CREDIT ANALYSIS:
  Debt/EBITDA: [x] | Interest Coverage: [x]
  Rating trajectory: [upgrade/stable/downgrade watch]
  Sector outlook: [expanding/stable/contracting]
  Key covenant: [incurrence/maintenance, leverage cap]

RISK FACTORS:
  1. Duration risk: [x]% price drop if rates +1%
  2. Credit risk: Downgrade possible if [condition]
  3. Liquidity: [bid-ask spread, trading volume]
  4. Call risk: Callable at $[price] on [date]

RECOMMENDATION: BUY / HOLD / SELL / AVOID
POSITION SIZE: [X%] fixed income allocation | GATE STATUS: [FULL/REDUCED/SKIP]
TARGET PRICE: $[] (YTM: [%]) | STOP: $[] or spread >[bps]
```

---

## Red Flags — STOP and Review

- Duration >10y in rising rate environment (bear steepener)
- HY allocation >25% when credit spreads <300bps (late cycle)
- Callable bond bought at premium (call risk = capital loss)
- Municipal bond AMT exposure for high-tax-bracket investor
- MBS pool with 200+ PSA prepayment (reinvestment risk)
- Bullet strategy with no liquidity buffer (all bonds mature same year)
- CCC-rated bonds in portfolio >5% (tail risk concentration)

**All of these mean: Re-run risk gates. Adjust duration/credit mix.**
