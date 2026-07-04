# THESIS-TRACKER: Investment Hypothesis Versioning & Drift Detection

**Portability**: 90pt | **Effort**: 4h | **Type**: Pure framework | **LOC**: 280

---

## Overview

THESIS-TRACKER is a persistent hypothesis management system that captures investment theses, tracks conviction evolution, detects assumption drift, and maintains a historical audit trail. It operates as the "long-term memory" layer above DYP-Ask (which generates the analysis) and below portfolio decisions.

**Core principle**: A thesis is only as good as the assumptions it rests on. Track them visibly, update them quarterly, and alert when they break.

**Target user**: Value investors, long-short hedge funds, and individual investors who need to:
1. Document thesis once, reuse across quarters
2. See exactly what changed (conviction, fair value, assumptions)
3. Detect when assumptions are failing before price action confirms it
4. Compare thesis quality across peers (who saw the drift first?)

---

## The THESIS-TRACKER Framework

### Data Structure: Thesis Version

Every thesis is stored as an immutable version. Changes create new versions, not overwrites.

```yaml
# THESIS: Alibaba (BABA) — Long-term ecosystem play
# Created: 2026-04-01
# Current Version: 3 (as of 2026-07-04)

thesis_id: "baba_alibaba_2026q2"
company_ticker: "BABA"
company_name: "Alibaba Group Holding"
thesis_name: "China e-commerce consolidator with cloud upside"

# Each version is timestamped, immutable
versions:
  - version_number: 1
    date_created: "2026-04-01"
    conviction_score: 65  # 0-100
    thesis_stage: "research"  # research, thesis, active, closed
    
    # The DYP-Ask output embedded here
    core_business: "Marketplace operator taking 5-8% commission; cloud segment growing 20% YoY"
    moat: "Network effects (500M+ users), ecosystem lock-in (Alipay, logistics), regulatory advantage"
    
    # Key assumptions (from DYP-Ask Q5)
    assumptions:
      - assumption_id: "a1_gmv_growth"
        text: "China e-commerce GMV grows 8% CAGR through 2028"
        criticality: "HIGH"  # HIGH, MEDIUM, LOW
        
      - assumption_id: "a2_take_rate"
        text: "Alibaba maintains 5% average take rate (vs 3% in 2020)"
        criticality: "HIGH"
        
      - assumption_id: "a3_cloud_margin"
        text: "Cloud segment reaches 20% operating margin by 2028"
        criticality: "MEDIUM"
        
      - assumption_id: "a4_regulatory"
        text: "Chinese regulators do not impose additional antitrust constraints"
        criticality: "HIGH"
        
      - assumption_id: "a5_competition"
        text: "Pinduoduo + ByteDance remain fragmented, no unified competitor emerges"
        criticality: "MEDIUM"
    
    # Key metrics to monitor
    key_metrics:
      - metric_id: "m1_gmv_quarterly"
        name: "Quarterly GMV (CNY)"
        current_value: "500B"
        unit: "CNY"
        frequency: "quarterly"
        threshold_alert: "growth drops below 5%"
        
      - metric_id: "m2_take_rate"
        name: "Take rate (as % of GMV)"
        current_value: "5.2%"
        unit: "%"
        frequency: "quarterly"
        threshold_alert: "falls below 4.5%"
        
      - metric_id: "m3_cloud_margin"
        name: "Cloud operating margin"
        current_value: "8%"
        unit: "%"
        frequency: "quarterly"
        threshold_alert: "fails to grow 2% YoY"
    
    # Valuation snapshot
    valuation:
      date: "2026-04-01"
      stock_price: "$85.00"
      market_cap: "$230B"
      fair_value_base: "$95-110"  # DCF base case range
      fair_value_bear: "$70-80"   # stress-test case
      fair_value_bull: "$120-140" # upside scenario
      implied_margin_of_safety: "12%"  # (fair_value_base_low - price) / price
      
    # Exit triggers (from DYP-Ask Q11)
    exit_triggers:
      - trigger_id: "t1_gmv_collapse"
        condition: "Quarterly GMV growth turns negative 2+ quarters"
        action: "REASSESS"
        
      - trigger_id: "t2_take_rate_compression"
        condition: "Take rate falls below 4%"
        action: "SELL_50%"
        
      - trigger_id: "t3_regulatory_crackdown"
        condition: "Chinese government bans marketplace features or imposes trading caps"
        action: "SELL_100%"
        
      - trigger_id: "t4_price_target_hit"
        condition: "Stock price reaches $110+ (top of fair value range)"
        action: "SELL_25%"
    
    # Original DYP-Ask response (JSON format)
    dyp_ask_output:
      q1_core_business: "Marketplace takes 5-8% commission on GMV; cloud segment 15% of revenue"
      q3_moat: "Network effects, ecosystem (Alipay, Cainiao), regulatory approval as state-backed platform"
      q5_assumptions: ["GMV CAGR 8%", "Take rate 5%", "Cloud margin 20%", "Regulatory stable"]
      q6_stress_tests: ["GMV CAGR 3%", "Take rate 3%", "Cloud margin 10%", "Regulatory antitrust"]
      q9_dcf_fair_value: "$95-110"
      q10_conviction: 65
      q11_sell_triggers: ["GMV negative 2Q", "Take rate <4%", "Regulatory ban", "Price >$110"]
    
    # Session metadata
    created_by: "investment_team"
    notes: "Initial thesis after 20-hour research sprint. See linked DYP-Ask output."
    
  - version_number: 2
    date_created: "2026-06-15"
    conviction_score: 58  # DOWN from 65 — GMV growth slowing
    thesis_stage: "active"
    
    core_business: "Same"
    moat: "Same"
    
    # Assumptions UNCHANGED (this is key — we track what changed vs. what stayed)
    assumptions:
      - assumption_id: "a1_gmv_growth"
        text: "China e-commerce GMV grows 8% CAGR through 2028"
        criticality: "HIGH"
        status: "at_risk"  # NEW FIELD: was 'new', now 'at_risk', 'broken', 'validated'
        notes: "Q1 2026 actual: 6% YoY (miss vs 8% target). Need to reassess."
      
      - assumption_id: "a2_take_rate"
        text: "Alibaba maintains 5% average take rate"
        criticality: "HIGH"
        status: "validated"
        
      - assumption_id: "a3_cloud_margin"
        text: "Cloud segment reaches 20% operating margin by 2028"
        criticality: "MEDIUM"
        status: "on_track"
        
      - assumption_id: "a4_regulatory"
        text: "Chinese regulators do not impose additional antitrust constraints"
        criticality: "HIGH"
        status: "validated"
        
      - assumption_id: "a5_competition"
        text: "Pinduoduo + ByteDance remain fragmented"
        criticality: "MEDIUM"
        status: "at_risk"
        notes: "ByteDance Douyin Commerce growing 40% YoY. Consolidation pressure increasing."
    
    key_metrics:
      - metric_id: "m1_gmv_quarterly"
        current_value: "480B"  # DOWN from 500B
        prior_value: "500B"
        change_pct: "-4%"
        status: "declining"
        
      - metric_id: "m2_take_rate"
        current_value: "5.1%"  # STABLE
        prior_value: "5.2%"
        change_pct: "-1.9%"
        status: "stable"
        
      - metric_id: "m3_cloud_margin"
        current_value: "10%"  # UP 2%
        prior_value: "8%"
        change_pct: "+25%"
        status: "improving"
    
    # Valuation UPDATE
    valuation:
      date: "2026-06-15"
      stock_price: "$78.50"  # DOWN from $85
      market_cap: "$210B"
      fair_value_base: "$88-100"  # REVISED DOWN due to lower GMV growth
      fair_value_bear: "$65-75"
      fair_value_bull: "$110-120"
      implied_margin_of_safety: "12%"
    
    exit_triggers:
      # UNCHANGED from v1 (we don't delete; we mark status)
      - trigger_id: "t1_gmv_collapse"
        condition: "Quarterly GMV growth turns negative 2+ quarters"
        action: "REASSESS"
        status: "active"
      
      - trigger_id: "t2_take_rate_compression"
        condition: "Take rate falls below 4%"
        action: "SELL_50%"
        status: "active"
      
      - trigger_id: "t3_regulatory_crackdown"
        condition: "Chinese government bans marketplace features"
        action: "SELL_100%"
        status: "active"
      
      - trigger_id: "t4_price_target_hit"
        condition: "Stock price reaches $110+"
        action: "SELL_25%"
        status: "inactive"  # Price below target; removed from immediate watch
    
    dyp_ask_output: "See v1; did NOT re-run DYP-Ask (only monitoring phase)"
    
    created_by: "investment_team"
    notes: "Q1 earnings miss triggered version 2. GMV growth disappointing; ByteDance competition heating up. Conviction down 7 points. Reassess in Q3."
    
  - version_number: 3
    date_created: "2026-07-04"
    conviction_score: 52  # DOWN another 6 points — now uncertain
    thesis_stage: "active"
    
    core_business: "Same"
    moat: "ERODING — ByteDance Douyin Commerce now 2nd-largest marketplace"
    
    assumptions:
      - assumption_id: "a1_gmv_growth"
        text: "China e-commerce GMV grows 8% CAGR through 2028"
        criticality: "HIGH"
        status: "broken"  # KEY CHANGE: assumption no longer holds
        confidence: "40%"  # We now think growth more likely 5-6%
        revised_assumption: "China e-commerce GMV grows 5-6% CAGR through 2028"
        notes: "Q2 2026: 4% YoY (miss again). Market maturation. Changed assumption."
      
      - assumption_id: "a2_take_rate"
        text: "Alibaba maintains 5% average take rate"
        criticality: "HIGH"
        status: "at_risk"
        confidence: "60%"
        notes: "Price competition from ByteDance (who undercuts on fees). Take rate may compress to 4.5-4.8%."
      
      - assumption_id: "a3_cloud_margin"
        text: "Cloud reaches 20% operating margin by 2028"
        criticality: "MEDIUM"
        status: "on_track"
        confidence: "75%"
      
      - assumption_id: "a4_regulatory"
        text: "Chinese regulators do not impose additional antitrust constraints"
        criticality: "HIGH"
        status: "at_risk"
        confidence: "50%"
        notes: "New proposal from SAMR: 'mandatory interoperability for marketplaces.' Unclear impact."
      
      - assumption_id: "a5_competition"
        text: "Pinduoduo + ByteDance remain fragmented"
        criticality: "MEDIUM"
        status: "broken"
        confidence: "20%"
        revised_assumption: "ByteDance Douyin Commerce consolidates 15-20% of e-commerce by 2028"
        notes: "ByteDance growing 40% YoY (vs Alibaba 4%). Market share shift accelerating."
    
    key_metrics:
      - metric_id: "m1_gmv_quarterly"
        current_value: "460B"
        prior_value: "480B"
        change_pct: "-4.2%"
        status: "deteriorating"
      
      - metric_id: "m2_take_rate"
        current_value: "4.9%"
        prior_value: "5.1%"
        change_pct: "-3.9%"
        status: "compressing"
      
      - metric_id: "m3_cloud_margin"
        current_value: "11%"
        prior_value: "10%"
        change_pct: "+10%"
        status: "stable"
    
    valuation:
      date: "2026-07-04"
      stock_price: "$72.00"
      market_cap: "$193B"
      fair_value_base: "$80-92"  # REVISED DOWN again
      fair_value_bear: "$60-70"
      fair_value_bull: "$100-110"
      implied_margin_of_safety: "11%"  # Margin eroding
    
    exit_triggers:
      - trigger_id: "t1_gmv_collapse"
        status: "triggered"  # NOW TRIGGERED: 2 quarters of negative growth
        action: "SELL_50%"
        executed: false
        
      - trigger_id: "t2_take_rate_compression"
        status: "approaching"
        
      - trigger_id: "t3_regulatory_crackdown"
        status: "monitoring"  # SAMR proposal being drafted
        
      - trigger_id: "t4_price_target_hit"
        status: "inactive"
    
    dyp_ask_output: "See v1"
    
    decision: "HOLD → REDUCE (sell 50% at next strength; reassess full thesis end of Q3)"
    created_by: "investment_team"
    notes: "Two consecutive earnings misses. GMV growth assumption broken. Moat eroding vs ByteDance. Conviction now below 55% threshold. SELL TRIGGER t1 hit: execute 50% reduction."
```

---

## Monthly Update Checklist

Use this template monthly to move from version N to version N+1.

```markdown
# Monthly Thesis Update — [THESIS_ID] — [MONTH] [YEAR]

**Prepared by:** [name]  
**Date:** [date]  
**Current version:** [N]  

## Step 1: Collect Quarterly Data (if Q-end) or Latest Metrics
- [ ] **GMV/Revenue:** Most recent quarter reported → compare vs. thesis forecast
- [ ] **Take rate / Operating margins:** Latest reported
- [ ] **Competitive position:** Market share data, competitor earnings highlights
- [ ] **Regulatory updates:** News, policy changes, enforcement actions
- [ ] **Management changes:** CEO departures, COO replacements, board changes
- [ ] **Product updates:** Major feature launches, exits from segments

## Step 2: Stress-Test Each Assumption

For EACH assumption in the thesis:
- [ ] **Status:** Is it still true? (new / validated / at_risk / broken)
- [ ] **Confidence:** Your honest estimate: 0-100%
- [ ] **Evidence:** Quote the metric that proves/disproves it
- [ ] **Action:** If broken, what is the revised assumption?

Example:
```
Assumption: GMV grows 8% CAGR
Status: at_risk → broken
Evidence: Q1 actual 6%, Q2 actual 4% (miss 2 quarters)
Revised assumption: GMV grows 5-6% CAGR (market maturation, competition)
New conviction: 40% (vs. 90% when thesis started)
```

## Step 3: Update Key Metrics

- [ ] **Metric 1:** Current value / Prior value / Change % / Status
- [ ] **Metric 2:** (repeat)
- [ ] **Metric N:** (repeat)

## Step 4: Check Exit Triggers

- [ ] **Trigger 1 (GMV collapse):** Hit? Action needed?
- [ ] **Trigger 2 (Take rate):** Hit? Action needed?
- [ ] **Trigger 3 (Regulatory):** Hit? Action needed?
- [ ] **Trigger 4 (Price target):** Hit? Action needed?

## Step 5: Revalue the Company (Optional; Full DCF ~2 hours)

- [ ] **Update assumptions:** Replace broken ones with revised
- [ ] **Recalculate DCF:** Base / Bear / Bull cases
- [ ] **New fair value range:** _____ – _____
- [ ] **New margin of safety:** _____ %

## Step 6: Update Conviction & Recommendation

- [ ] **Old conviction:** [N-1]
- [ ] **New conviction:** [N] (explain why up/down)
- [ ] **Recommendation:** BUY / HOLD / REDUCE / SELL
- [ ] **Position action:** INCREASE / MAINTAIN / TRIM / EXIT

## Step 7: Write the Update Summary

- [ ] **What changed:** Bullish, bearish, or neutral?
- [ ] **What stayed the same:** Still core to thesis?
- [ ] **Decision:** Next review date, monitoring priorities

---

**Conviction Change:** Old [65] → New [52] (↓ 13 points)

**Recommendation:** BUY → REDUCE (sell 50% at next strength)

**Next Review:** End of Q3 2026 (post-Q3 earnings, early Sep)

**Monitoring:** GMV growth trend, ByteDance market share, SAMR regulatory draft
```

---

## Drift Detection Pattern

Drift = An assumption you made is no longer true, but price hasn't reflected it yet.

### The 3-Signal Drift Detector

**Signal 1: Assumption Status Changes**
```
For each assumption, check:
- Is the metric trending away from the assumption?
- Has the trend persisted 2+ quarters?
- Is there new competitive/regulatory pressure?

Example:
✗ "GMV grows 8%" → Q1: 6%, Q2: 4% → Assumption broken (signal 1 detected)
```

**Signal 2: Conviction Drop vs. Price**
```
Track this ratio quarterly:
  Price-to-Conviction Ratio = Stock Price / Conviction Score

If price is FLAT but conviction drops 15+ points → Drift detected
The market hasn't woken up yet.

Example:
- Q2: Price $85, Conviction 65 → Ratio = 1.31
- Q3: Price $78 (↓ 8%), Conviction 52 (↓ 20%) → Ratio = 1.50
→ Price fell less than conviction worsened → Market lagging reality
```

**Signal 3: Trigger Approach**
```
Track distance to exit triggers:
- Trigger: "GMV growth turns negative 2+ quarters"
- Q1: 6% (1 miss)
- Q2: 4% (2 misses) → APPROACHING TRIGGER
- Q3: -1% → TRIGGER HIT

Early warning: Watch Q1 result carefully; if miss, review thesis before Q2.
```

### When to Alert the Portfolio Manager

| Situation | Action |
|-----------|--------|
| 1 assumption broken, conviction ↓ 5-10 points | **Monitor** — update docs, keep position |
| 2+ assumptions broken OR conviction ↓ 15+ points | **Review** — consider position trim |
| Exit trigger hit OR conviction < 50 | **Act** — execute REDUCE/SELL decision |
| New regulatory/competitive threat + trigger approaching | **Escalate** — hold emergency review |

---

## Integration with DYP-Ask

### Input: DYP-Ask Output → Thesis-Tracker Storage

When you run DYP-Ask (initial thesis or refresh):

1. **Save the output** in thesis JSON:
```json
{
  "thesis_id": "baba_alibaba_2026q2",
  "version_number": 1,
  "dyp_ask_output": {
    "q1_core_business": "...",
    "q3_moat": "...",
    "q5_assumptions": ["...", "...", "..."],
    "q9_dcf_fair_value": "$95-110",
    "q10_conviction": 65,
    "q11_sell_triggers": ["...", "...", "..."]
  }
}
```

2. **Extract key data** into thesis structure:
   - DYP-Ask Q5 assumptions → thesis.assumptions (with IDs, criticality)
   - DYP-Ask Q9 DCF → thesis.valuation
   - DYP-Ask Q10 conviction → thesis.conviction_score
   - DYP-Ask Q11 triggers → thesis.exit_triggers

3. **Store once, track forever** — don't re-run DYP-Ask until next major event (earnings, strategic pivot, market shock)

### Output: Thesis-Tracker → Portfolio Actions

Monthly/Quarterly, thesis-tracker produces:

```yaml
drift_alert:
  thesis_id: "baba_alibaba_2026q2"
  version_number: 3
  alert_type: "trigger_hit"  # or "assumption_broken", "conviction_drop", "approaching_trigger"
  severity: "HIGH"
  
  description: "Exit trigger t1 (GMV collapse) HIT: 2 consecutive quarters of YoY growth below target."
  
  action_required: "Sell 50% position at next opportunity (target: $75-80)"
  
  evidence:
    - "Q1 2026: 6% YoY (miss vs. 8% thesis target)"
    - "Q2 2026: 4% YoY (2nd miss, trigger threshold)"
    - "Metric trend: deteriorating; no recovery in pipeline"
  
  recommendation: "REDUCE"
  next_review: "2026-09-30 (post-Q3 earnings)"
```

This alert feeds into:
- Portfolio dashboard (show all REDUCE positions)
- Risk management system (adjust position sizing)
- Investment committee (highlight drift vs. peer theses)

---

## Template: Starting a New Thesis

```yaml
thesis_id: "[TICKER]_[COMPANY_SHORT_NAME]_[YEARQ]"  # e.g., "aapl_apple_2026q2"
company_ticker: "TICKER"
company_name: "Full Company Name"
thesis_name: "One-liner describing the bet"

versions:
  - version_number: 1
    date_created: "YYYY-MM-DD"
    conviction_score: "XX"  # 0-100; start >60 or thesis isn't worth the effort
    thesis_stage: "research"  # or "thesis", "active", "closed"
    
    # (Copy from DYP-Ask output)
    core_business: "..."
    moat: "..."
    
    assumptions:
      - assumption_id: "a1"
        text: "..."
        criticality: "HIGH"  # or MEDIUM, LOW
    
    key_metrics:
      - metric_id: "m1"
        name: "..."
        current_value: "..."
        frequency: "quarterly"  # or "monthly", "annual"
        threshold_alert: "..."
    
    valuation:
      stock_price: "$..."
      fair_value_base: "$...-..."
      fair_value_bear: "$...-..."
      fair_value_bull: "$...-..."
    
    exit_triggers:
      - trigger_id: "t1"
        condition: "..."
        action: "REASSESS"  # or SELL_50%, SELL_100%
    
    created_by: "[Your Name]"
    notes: "..."
```

---

## Next Steps in 1ai-Ecosystem

1. ✅ Deploy THESIS-TRACKER to 1ai-skills
2. → Integrate with `quality-screen` for pre-screening (don't start thesis unless quality passes)
3. → Build dashboard showing:
   - All theses + current conviction
   - Drift alerts (which theses have broken assumptions?)
   - Conviction vs. Price ratio (which are most mispriced?)
4. → Add peer benchmarking (how do my thesis convictions compare to others?)
5. → Connect to trade execution (when trigger hits, auto-alert trading desk)

---

## Real-World Example: Alibaba Q1-Q3 2026 (Three Versions)

See the detailed thesis structure above. Key learning:
- Started with 65% conviction (justified by research)
- Two consecutive earnings misses → conviction dropped to 52%
- Assumptions broken, triggers hit → REDUCE decision made
- All versions preserved in history (never delete; just mark status)
- Next thesis owner can see exactly when and why conviction worsened

---

## Common Failure Modes & Fixes

| Failure | Why | Fix |
|---------|-----|-----|
| Conviction never changes | Fear of admitting error | Update monthly; if metrics miss 2 quarters, conviction must fall |
| Thesis never closed | Sunk cost bias | Set explicit close date + trigger; force decision by Q4 |
| Assumptions never broken | Overconfidence | Run drift detector monthly; if 2 metrics miss, mark assumption "at_risk" |
| Trigger never hit | Too lenient | Thresholds should reflect actual thesis logic (not hope) |
| No version history | Can't learn | Store every update; compare v1 vs. v3 to see what changed |

---

## Storage & Backup

**Recommended setup:**
```
~/projects/1ai-skills/finance/investment/theses/
├── by_ticker/
│   ├── BABA_alibaba_2026q2.yaml
│   ├── AAPL_apple_2026q3.yaml
│   └── ...
├── by_date/
│   ├── 2026-04/
│   ├── 2026-05/
│   └── ...
└── README.md (index of all active theses)
```

Each thesis is a single YAML file (immutable; append new versions).

---

## References

**Warren Buffett's "Circle of Competence"**: Invest only in businesses you fully understand. Document your understanding as a thesis, not a memo.

**Charlie Munger's Inversion**: "Instead of 'why will this succeed?', ask 'how could my assumptions be completely wrong?'" — This is drift detection.

**George Soros' Reflexivity**: Markets and reality interact. Your thesis may be sound, but if the market sees it differently, your position will move against you before reality confirms your thesis. Monitor drift early.

**Seth Klarman's Margin of Safety**: A thesis is only valid if the margin of safety holds. If fair value drops, re-check the margin.

---

## Acceptance Criteria (TIER 1 Deployment)

- ✅ Framework captures thesis versioning (immutable versions, metadata)
- ✅ Template shows 3-month Alibaba history (versions 1, 2, 3)
- ✅ Monthly update checklist guides users through assumption re-validation
- ✅ Drift detection pattern identifies broken assumptions before price moves
- ✅ Integration with DYP-Ask documented (input/output contract)
- ✅ Exit triggers from DYP-Ask Q11 tracked through versions
- ✅ Zero external dependencies (pure framework, spreadsheet-compatible)

---

**Status**: Ready for TIER 1 deployment. Integration with DYP-Ask complete. All criteria met.

**Owner**: Investment Framework Team  
**Deployed**: 2026-07-04  
**Version**: 1.0
