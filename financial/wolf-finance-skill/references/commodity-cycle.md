# fin-commodity-cycle: Supply/Demand & Futures Analysis

## Commodity Analysis Framework

### 5 Core Commodity Sectors
1. **Energy**: Crude oil (WTI/Brent), natural gas, LNG
2. **Metals**: Gold, silver, copper, lithium, nickel
3. **Agriculture**: Corn, wheat, soybeans, coffee, sugar
4. **Soft Commodities**: Cotton, cocoa, orange juice
5. **Bulk Materials**: Iron ore, coal, potash

---

## Futures Curve Analysis

### Contango vs. Backwardation
- **Contango**: Futures price > Spot price → market expects oversupply; rolling futures = negative carry
- **Backwardation**: Spot price > Futures price → tight supply now; rolling futures = positive carry
- **Steep backwardation** = strong buy signal (supply squeeze)
- **Flattening contango** = potential supply tightening ahead

### Inventory Tracking
| Commodity | Key Inventory Report | Frequency |
|-----------|---------------------|-----------|
| Crude Oil | EIA Weekly Petroleum Report | Weekly |
| Natural Gas | EIA Natural Gas Storage | Weekly |
| Gold/Silver | COMEX registered stocks | Daily |
| Copper | LME warehouse stocks | Daily |
| Grains | USDA WASDE | Monthly |

### COT (Commitment of Traders) Analysis
- **Commercial hedgers** net short → producers hedging = bearish signal
- **Managed money** net long at extremes → crowded trade = reversal risk
- COT data source: CFTC.gov (weekly, released Friday)

---

## Supply/Demand Drivers

### Energy
- OPEC+ production decisions and compliance
- US shale rig count (Baker Hughes weekly)
- China oil demand (import data, tanker tracking)
- Strategic Petroleum Reserve (SPR) levels

### Metals
- Gold: Real yields (negative = bullish), central bank buying, DXY
- Copper: China PMI, global construction starts, EV adoption curve
- Lithium: EV sales data, battery gigafactory capacity

### Agriculture
- La Niña / El Niño crop disruption risk
- Black Sea shipping lanes (wheat/corn)
- Brazil soy crop estimates (CONAB)

---

## Commodity Output Template
```
COMMODITY: [name] | CONTRACT: [month/year]
SPOT: $[price] | FRONT FUTURES: $[price]
CURVE STRUCTURE: [Contango / Backwardation] | Degree: [steep/mild/flat]
CARRY: [positive/negative] — [% annualized]

SUPPLY/DEMAND BALANCE:
  Inventory: [level] vs [5y average] — [tight/balanced/surplus]
  Supply trend: [growing/stable/declining]
  Demand driver: [key factor]

COT POSITIONING:
  Managed Money: [net long/short] | Change (wk): [+/-]
  Commercial: [net long/short]
  Crowding risk: [high/moderate/low]

SIGNAL: [Bullish/Neutral/Bearish] | HORIZON: [weeks/months]
```
