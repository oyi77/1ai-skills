# fin-macro-liquidity: Global Macro & Central Bank Liquidity

**REQUIRED SUB-SKILL:** Load `forex-matrix.md` for currency implications. Load `commodity-cycle.md` for real asset impact.

## Global Central Bank Dashboard

### Federal Reserve (Fed) — United States
- **Mandate**: Dual (maximum employment + price stability ~2% PCE)
- **Policy Rate**: Fed Funds Rate (current: check FRED DFF)
- **Balance Sheet**: <$8T (QT ongoing, ~$95B/month runoff)
- **Key Tools**: OMO, Overnight Reverse Repo (ON RRP), Discount Window
- **Stress Indicator**: SOFR – Fed Funds = banking stress (>10bps = concern)

### European Central Bank (ECB) — Eurozone
- **Mandate**: Single (price stability <2% HICP)
- **Policy Rate**: Deposit Facility Rate (DFR), Main Refinancing Rate
- **Balance Sheet**: >€7T (PEPP ended, APP runoff)
- **Key Tools**: TLTROs, PEPP, negative rates (history)
- **Stress Indicator**: BTP-Bund spread (>250bps = peripheral stress)

### Bank of Japan (BoJ) — Japan
- **Mandate**: Price stability (2% CPI target, long elusive)
- **Policy Rate**: –0.1% (negative), 10y JGB yield target ~0%
- **Balance Sheet**: >¥700T (YCC abandoned Dec 2024)
- **Key Tools**: YCC (yield curve control), ETF purchases (suspended)
- **Stress Indicator**: USD/JPY (intervention >150, <130)

### Bank of England (BoE) — United Kingdom
- **Mandate**: Price stability (2% CPI) + financial stability
- **Policy Rate**: Bank Rate (currently 5.00% range)
- **Balance Sheet**: >£800B (gradual QT, active gilt sales)
- **Key Tools**: Gilt purchases, Term Funding Scheme
- **Stress Indicator**: 10y Gilt yield (>5% = stress, LDI crisis risk)

### People's Bank of China (PBoC) — China
- **Mandate**: Multiple (growth, employment, stability, CNY stability)
- **Policy Rate**: MLF (Medium-term Lending Facility) ~2.5%
- **Balance Sheet**: >¥40T (targeted RRR cuts, not QE)
- **Key Tools**: RRR (reserve requirement ratio), MLF, PSL, LPR
- **Stress Indicator**: USD/CNY (near 7.30 cap), credit growth slowdown

---

## Liquidity Regimes & Asset Impact

### Quantitative Easing (QE) — "Liquidity On"
- **Fed/ECB/BoJ expanding balance sheets** → Asset price support
- **Effects**: Lower yields, tighter credit spreads, risk-on sentiment
- **Winners**: Equities (growth > value), credit, EM, crypto
- **Losers**: USD (weakens), safe-haven bonds (yields rise)

### Quantitative Tightening (QT) — "Liquidity Off"
- **Balance sheet runoff** → Liquidity drains from system
- **Effects**: Higher yields, wider spreads, volatility ↑
- **Winners**: USD (strengthens), short-duration bonds
- **Losers**: Growth equities, crypto, leveraged credit, EM

### Pivot Points (Policy Reversals)
- **Fed pause → cut cycle**: Major risk-on catalyst (check dot plot)
- **ECB front-loading cuts**: Peripheral spreads compress
- **BoJ normalization**: Carry trade unwind (JPY strength, global ripple)
- **PBoC stimulus**: Commodity demand, AUD/NOK benefit

---

## Key Liquidity Indicators

### Money Market Stress
| Indicator | Source | Bullish | Bearish |
|-----------|--------|---------|--------|
| **SOFR – Fed Funds** | FRED | <5bps | >20bps (stress) |
| **ON RRP Usage** | NY Fed | >$500B (abundant) | <$100B (drain) |
| **3m Libor/SOFR spread** | FRED | <10bps | >50bps (bank stress) |
| **TED Spread** (3m T-bill – 3m Libor) | FRED | <30bps | >100bps (crisis) |
| **Cross-Currency Basis** (USD/EUR, USD/JPY) | Bloomberg | >–10bps | <–50bps (USD shortage) |

### Yield Curve & Rates
| Indicator | Calculation | Bullish | Bearish |
|-----------|-------------|---------|--------|
| **2s10s Spread** | 10y – 2y Treasury | >0.50% (normal) | <0 (inversion = recession warning) |
| **3m10y Spread** | 10y – 3m T-bill | >0 (normal) | <–0.50% (deep inversion) |
| **10y Treasury** | FRED DGS10 | Falling (bonds rally) | Rising (bear steepener) |
| **MOVE Index** | Bloomberg | <100 (low vol) | >150 (rate volatility = stress) |

### Dollar Smile Theory
- **Left smile (Risk-Off)**: USD strong (safe haven), recession fears → Buy USD, T-bills
- **Bottom (Risk-On)**: USD weak, global growth → Sell USD, buy EM, commodities
- **Right smile (US Outperformance)**: USD strong, US growth > rest → Buy USD, US equities

---

## Global Liquidity Transmission

### The Plumbing (How Liquidity Flows)
1. **Fed creates reserves** → Primary dealers → Money market funds → Assets
2. **ECB creates euros** → European banks → European assets + carry trades
3. **BoJ ultra-loose** → Yen carry trade (borrow JPY, buy USD assets) → Global liquidity
4. **PBoC stimuls** → Chinese demand → Commodities (copper, iron ore) → EM exports

### Feedback Loops
- **Strong USD** → EM debt stress (USD-denominated) → Risk-off → USD stronger
- **Fed cuts** → USD weaker → EM capital inflows → Commodity demand → Growth
- **BoJ hikes** → Carry trade unwind → JPY stronger → Global liquidity contraction

---

## Liquidity Monitor Output Template

```
DATE: [YYYY-MM-DD]
GLOBAL LIQUIDITY REGIME: [QE/QT/Pivot/Neutral]
DOLLAR SMILE POSITION: [Left(Risk-Off)/Bottom(Risk-On)/Right(US-Outperf)]

CENTRAL BANK SNAPSHOT:

Fed (US):
  Funds Rate: [%] | Balance Sheet: $[X]T (QT: $[Y]B/mo)
  SOFR – FF: [bps] → [normal/stressed]
  ON RRP: $[X]B → [abundant/draining]
  Yield Curve 2s10s: [bps] → [normal/inverted]
  Signal: [Hawkish/Neutral/Dovish]

ECB (Eurozone):
  Deposit Rate: [%] | Balance Sheet: €[X]T (QT: €[Y]B/mo)
  BTP-Bund: [bps] → [normal/stressed]
  Peripheral spreads: [10y Spain/Italy/Portugal]
  Signal: [Hawkish/Neutral/Dovish]

BoJ (Japan):
  Policy Rate: [%] | 10y JGB: [%] (YCC abandoned)
  USD/JPY: [rate] → [intervention risk?]
  Carry Trade Viability: [Strong/Moderate/Unwind]
  Signal: [Tightening/Neutral/Easing]

PBoC (China):
  MLF Rate: [%] | USD/CNY: [rate] (cap: ~7.30)
  RRR: [%] | Credit Growth: [% YoY]
  Signal: [Stimulative/Neutral/Restrictive]

LIQUIDITY INDICATORS:
  MOVE Index: [level] → [low vol/moderate/high stress]
  Cross-Currency Basis (EUR/USD): [bps] → [USD abundance/shortage]
  TED Spread: [bps] → [normal/stressed]
  Global M2 Growth: [% YoY] → [expansion/contraction]

ASSET IMPLICATIONS:
  Equities: [Risk-on: buy growth / Risk-off: defensive]
  USD: [Strong/Weak/Neutral] → FX trades: [EUR/USD, USD/JPY targets]
  Credit: [Spreads tightening/widening] → HY vs. IG allocation
  Commodities: [Demand driven by China/USD] → Oil, copper outlook
  Crypto: [Liquidity-driven: BTC correlates with M2] → Heat score

TRADING THEMES (Next 3–6 Months):
  1. [Fed pivot → duration long, growth equities]
  2. [BoJ normalization → JPY long, carry trade unwind hedge]
  3. [China stimulus → commodity long, AUD/NOK long]
  4. [ECB cuts → peripheral spreads tighten, ITA/BONO long]

RISK MONITOR:
  Banking stress: [SOFR spread, cross-currency basis]
  Sovereign stress: [10y JGB, BTP-Bund, Gilt yields]
  EM crisis risk: [USD strength, credit spreads]
  Tail risk: [MOVE >150, TED >100bps, ON RRP <$100B]
```

---

## Red Flags — STOP and Re-Assess

- SOFR – Fed Funds >20bps (banking sector stress)
- ON RRP <$100B (liquidity drain, repo crisis risk)
- 3m10y spread <–0.50% (deep inversion, recession imminent)
- MOVE Index >150 (rate volatility = asset class stress)
- Cross-currency basis <–50bps (global USD shortage)
- USD/JPY >155 (BoJ intervention imminent, carry trade unwind)
- BTP-Bund >300bps (European periphery crisis)
- TED spread >100bps (interbank lending freezing)

**All of these mean: Risk-off mode. Reduce risk assets, increase USD/cash hedge.**
