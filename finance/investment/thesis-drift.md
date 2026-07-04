# THESIS-DRIFT: Investment Thesis Assumption Breakage Detection

**Portability**: 90pt | **Effort**: 4h | **Type**: Pure framework | **LOC**: 280

---

## Overview

THESIS-DRIFT is a detection framework that identifies when your investment thesis assumptions break under changing market conditions. It separates **fact-driven thesis deterioration** from **price volatility** and **restatement noise**.

**Core principle**: A thesis doesn't break because stock price falls. It breaks when *evidence* changes—earnings miss targets, competitive moats erode, management shifts allocation strategy, or regulatory winds shift.

**Integration**: Reads from `thesis-tracker` (assumption baselines), compares against current data, scores severity, and triggers decision rules.

---

## Design Philosophy

Long-term investing requires this distinction:

- **Thesis Drift** ✅ → Evidence changed. Example: "We assumed 15% revenue CAGR; three quarters show 8%."
- **Price Volatility** ❌ → Stock fell 30%, but business unchanged. Not a drift trigger.
- **Restatement Noise** ❌ → Same facts, different wording. Not a drift.

**Goal**: Only act when the business genuinely changed, not when the market mood swings.

---

## Core Framework: 6-Step Drift Detection

### Step 1: Load Thesis Baseline

From `thesis-tracker` output or `reports/{company}-thesis.md`, extract:
- **Core thesis** (5-sentence investment summary)
- **Core assumptions** (3-7 specific, testable hypotheses)
- **Red lines** (conditions that trigger automatic re-evaluation)
- **Valuation anchor** (fair value range, safety margin)
- **Buy price & entry thesis** (what made you buy at that level)

**If baseline missing**: Stop. Use `/thesis-tracker {company}` to establish baseline first.

### Step 2: Collect Current Evidence

Gather latest data:
- Most recent earnings report (revenue, margins, cash flow, guidance)
- Management commentary (guidance changes, strategic shifts, capital allocation moves)
- Competitive landscape updates (market share, new competitors, pricing)
- Regulatory changes (policy shifts, enforcement actions)
- Insider trading (large sells by officers suggest management confidence loss)

**Data sources**: Latest 10-K/20-F, earnings call transcript, latest analyst notes, company press releases, industry data.

### Step 3: Evidence-to-Assumption Mapping

Create a comparison matrix for each core assumption:

| Assumption | Original Basis | Current Evidence | Status | Severity |
|-----------|---|---|---|---|
| Revenue CAGR ≥15% | FY2024 guidance | Last 4 qtrs avg 8% YoY | 🔴 Broken | **CRITICAL** |
| Gross margin ≥60% | Historical 62% | Latest Q: 58% | 🟡 Weakening | MEDIUM |
| Market share in SEA ≥45% | 2024 report | 2026 data: 42% | 🟡 Slipping | MEDIUM |
| Management ROI-focused | 3-year buyback history | Zero buybacks this year | 🟡 Changed | LOW-MEDIUM |

**Rules**:
- 🟢 = Evidence supports assumption (no change)
- 🟡 = Evidence shows softening but not broken (warning zone)
- 🔴 = Evidence contradicts assumption (drift confirmed)

### Step 4: Severity Scoring (Quantitative)

Each broken assumption gets a **drift score** from 0-100:

#### Scoring Formula

```
Severity = (Assumption Weight × Change Magnitude) + Red Line Multiplier

Where:
  Assumption Weight = 1-5 (1=nice-to-have, 5=make-or-break)
  Change Magnitude = % deviation from assumption
    0-5%  = 1 point
    5-10% = 2 points
    10-20% = 3 points
    20-40% = 4 points
    >40%  = 5 points
  Red Line Multiplier = ×1.5 if red line triggered, ×1.0 otherwise
```

#### Severity Bands

| Score | Label | Urgency | Action |
|-------|-------|---------|--------|
| 0-15 | **Minor** | Low | Monitor. No action needed. |
| 16-35 | **Moderate** | Medium | Watch closely. Clarify in next earnings call. |
| 36-60 | **Major** | High | Reduce position 25-50% OR request urgent management discussion. |
| 61-85 | **Critical** | Urgent | Reduce to 25% or exit. Thesis substantially weakened. |
| 86-100 | **Thesis Broken** | Emergency | Exit position. Thesis assumptions invalidated. |

#### Example Calculation: Shopee

Shopee thesis assumed: "GMV CAGR ≥20%, take rate 2.5%, path to profitability within 24mo"

Current data: GMV CAGR now 12%, take rate compressed to 2.2%, losses widen, profitability pushed to 36 months.

```
Assumption 1: GMV CAGR ≥20%
  Weight: 5 (make-or-break for valuation)
  Current: 12%
  Deviation: -40% (from 20% to 12%)
  Change Magnitude: 5 points (>40% miss)
  Score: 5 × 5 × 1.0 = 25 points

Assumption 2: Take rate 2.5%
  Weight: 4 (important for margin targets)
  Current: 2.2%
  Deviation: -12%
  Change Magnitude: 3 points (10-20% range)
  Score: 4 × 3 × 1.0 = 12 points

Assumption 3: Profitability path 24mo
  Weight: 5 (valuation inflection point)
  Current: 36 months
  Deviation: +50%
  Change Magnitude: 5 points
  Score: 5 × 5 × 1.0 = 25 points

TOTAL SEVERITY SCORE: 25 + 12 + 25 = 62 → CRITICAL (61-85 band)
```

**Action triggered**: Reduce to 25% or exit. Thesis substantially weakened.

### Step 5: Decision Tree

Use this decision tree based on score:

```
START: Drift Detected
  │
  ├─ Score 0-15 (Minor)
  │   └─ Action: HOLD + MONITOR
  │       • Continue quarterly tracking
  │       • Set alert for next earnings
  │       • No position change
  │
  ├─ Score 16-35 (Moderate)
  │   ├─ Are red lines triggered? 
  │   │   ├─ YES → Reduce 25%
  │   │   └─ NO → HOLD + INCREASED MONITORING
  │   │       • Review management commentary in detail
  │   │       • Clarify in next earnings call
  │   │       • Decide: tolerate or exit
  │   │
  │   └─ Temporary or structural change?
  │       ├─ Temporary (one-time item, pricing pressure easing soon)
  │       │   └─ HOLD + Flag when circumstance reverses
  │       └─ Structural (market share loss, competitive breakthrough)
  │           └─ Reduce 25-50%
  │
  ├─ Score 36-60 (Major)
  │   ├─ Can thesis be saved?
  │   │   ├─ YES (management has clear plan, 1-2 quarters to fix)
  │   │   │   └─ Reduce 50%, keep 25-50% for upside
  │   │   │       Request emergency management call
  │   │   └─ NO (fundamental shifts, not fixable)
  │   │       └─ EXIT 75%, keep 25% lottery ticket if upside bet
  │   │
  │   └─ Must revalue position
  │       • New fair value range
  │       • New conviction score (lower)
  │
  ├─ Score 61-85 (Critical)
  │   └─ REDUCE 75% or EXIT
  │       • Thesis assumptions invalidated
  │       • Too much changed to maintain conviction
  │       • Keep 25% lottery ticket only if waiting for specific catalyst
  │       • Document: "Why I was wrong"
  │
  └─ Score 86-100 (Thesis Broken)
      └─ EXIT POSITION
          • Thesis is dead. Evidence overwhelming.
          • Do not wait for reversal. Move to next idea.
          • Document: Lessons learned
          • Review: Why did I miss this signal?

END
```

### Step 6: Output Drift Report

Generate structured report with these sections:

#### Report Structure

```
1. THESIS BASELINE (from thesis-tracker)
   - Company, Entry Price, Entry Date
   - 5-sentence core thesis
   - 3-7 core assumptions (with weights)
   - Red lines

2. DRIFT DETECTION SUMMARY
   - Severity Score: [0-100]
   - Severity Band: Minor / Moderate / Major / Critical / Thesis Broken
   - Drift Trigger: Which assumption(s) broke?
   - Fact vs. Price: What's evidence-driven vs. market noise?

3. ASSUMPTION-BY-ASSUMPTION BREAKDOWN

   | Assumption | Weight | Original | Current | Evidence | Status | Points |
   |---|---|---|---|---|---|---|
   | [example] | 5 | [baseline] | [current] | [source & detail] | 🔴 Broken | 25 |

4. RED LINE CHECK
   - Which red lines triggered (if any)?
   - Severity of each?
   - Required action per red line?

5. SEVERITY SCORING DETAIL
   - Calculation for each broken assumption
   - Why magnitude scored X?
   - Rollup to total score

6. DECISION TREE EXECUTION
   - Which branch applies?
   - Action: Hold / Reduce / Exit
   - Rationale

7. MANAGEMENT QUESTIONS
   - If staying in: What needs to clarify this?
   - Specific questions for earnings call
   - Red flags to listen for

8. NEXT STEPS
   - When to re-evaluate?
   - What catalyst/data triggers another check?
   - Monitoring checklist
```

---

## Real-World Example: Shopee Thesis Drift

### Baseline Thesis (Set July 2024)

**Company**: Shopee (SHOP)  
**Entry Price**: $32  
**Core Thesis** (5 sentences):
> Shopee captures Southeast Asian e-commerce growth via high-frequency transactions and network effects. Marketplace model scales with minimal capex. Management prioritizes profitability path; buyback signals confidence. GMV growth and take-rate stability drive margin expansion. Trading at 0.8× NTB vs. peers; 30% upside if profitability reaches timeline.

**Core Assumptions**:
1. GMV CAGR ≥20% (weight: 5 = make-or-break)
2. Take rate stable at 2.5-2.7% (weight: 4 = margin driver)
3. Adj. EBITDA margin path to 15%+ by 2026 (weight: 5 = valuation inflection)
4. Management capital allocation shareholder-friendly (buyback/buyback) (weight: 3 = confidence signal)
5. Regulatory environment stable (no surprise policy shifts) (weight: 4 = binary risk)

**Red Lines**:
- Take rate compressed >20% YoY (severity: HIGH)
- GMV growth drops below 10% for 2+ consecutive quarters (severity: HIGH)
- Guidance withdrawn or significantly reduced (severity: CRITICAL)
- Regulatory action changes business model (severity: CRITICAL)

**Valuation Anchor**:
- Fair value range: $35-42 (based on 15× 2027E EV/EBITDA)
- Safety margin: 30% (buy below $30; sell above $45)
- Conviction: 75/100

---

### Current Evidence (April 2026, 3 Quarters Later)

**Q1 2026 Earnings**:
- GMV CAGR (last 4 qtrs): 12% (vs. 20% assumption)
- Take rate: 2.2% (vs. 2.5% assumption, down 12%)
- Adj. EBITDA margin: -2% (vs. path to +15% by 2026)
- Guidance: Reduced FY26 GMV growth to 10-12% (vs. prior 18-20%)
- Buyback: Suspended. CEO cites "need to preserve cash for competitive investments"

---

### Drift Detection Execution

#### Step 1: Load Baseline ✓
[Loaded from thesis-tracker]

#### Step 2: Collect Evidence ✓
[Q1 2026 10-Q, earnings call transcript, analyst updates]

#### Step 3: Evidence Mapping

| Assumption | Weight | Original | Current | Evidence | Status |
|-----------|--------|----------|---------|----------|--------|
| GMV CAGR ≥20% | 5 | FY24 +22% | 4Q24-Q1'26 avg +12% | Last 4 qtrs: Q2'25 +18%, Q3 +14%, Q4 +11%, Q1'26 +9% | 🔴 BROKEN |
| Take rate 2.5%+ | 4 | Historical 2.6% | 2.2% | Q1 disclosure: 220bps vs. 260bps prior year | 🔴 BROKEN |
| EBITDA margin 15% by 2026 | 5 | Guidance: +15% path | -2% current | Management now guides +5-8% by 2027 (12-month slip + 7pp miss) | 🔴 BROKEN |
| Management shareholder focus | 3 | 3-yr buyback program, $500M authorized | Buyback suspended this quarter | CEO: "Redirecting to platform competition" | 🟡 WEAKENED |
| Regulatory stable | 4 | No major policy changes | No new policy but competitive pressure mounting | Indonesia, Vietnam intensifying seller subsidies | 🟡 MONITORING |

#### Step 4: Severity Scoring

```
Assumption 1: GMV CAGR ≥20% → -8pp miss (40% below target)
  Weight: 5 (make-or-break)
  Magnitude: 5 (>40% miss)
  Score: 5 × 5 × 1.0 = 25 points

Assumption 2: Take rate 2.5%+ → -0.3pp (12% below)
  Weight: 4 (margin driver)
  Magnitude: 3 (10-20% range)
  Score: 4 × 3 × 1.0 = 12 points

Assumption 3: EBITDA 15% by 2026 → -17pp miss (pushed to 2027, reduced to 5-8%)
  Weight: 5 (valuation inflection)
  Magnitude: 5 (>40% miss on timing and magnitude)
  Score: 5 × 5 × 1.0 = 25 points

Assumption 4: Buyback suspension (management priority shift)
  Weight: 3 (confidence signal)
  Magnitude: 3 (strategy shift)
  Score: 3 × 3 × 1.0 = 9 points

Red line check: GMV <10% for 2+ qtrs not yet hit, but Q1 at 9% → warning

TOTAL SCORE: 25 + 12 + 25 + 9 = 71 → CRITICAL (61-85 band)
```

#### Step 5: Decision Tree

Entry point: Score = 71 (CRITICAL)

Decision: **REDUCE 75% or EXIT**
- Thesis assumptions significantly invalidated
- Profitability path extended and downgraded
- Growth slowdown structural, not temporary
- Management redirecting strategy away from shareholder returns
- Valuation inflection delayed 12+ months
- Conviction drops from 75 → 35 (no longer high conviction)

**Specific Action**: Sell 75% of position at market. Keep 25% as lottery ticket (bet on turnaround catalyst).

#### Step 6: Output Report Structure

```
SHOPEE THESIS DRIFT REPORT
Date: 2026-04-15

I. BASELINE (July 2024)
   Entry Price: $32
   Conviction: 75/100
   Core Thesis: [5 sentences]
   Key Assumptions: GMV 20%+ CAGR, take rate 2.5%, profitability path 24mo

II. DRIFT SUMMARY
   Severity Score: 71/100
   Severity Band: CRITICAL
   Primary Trigger: GMV growth collapse (20% → 12%), profitability pushed out

III. ASSUMPTION BREAKDOWN
   [Table above]

IV. RED LINE STATUS
   - GMV <10% for 2 qtrs: ❌ Not yet triggered (9% in Q1, need Q2 confirmation)
   - Take rate compression >20%: ❌ Not triggered (12% is within range but trending)

V. SEVERITY CALCULATION
   [Show math for each assumption]
   Total: 71/100 = CRITICAL

VI. DECISION TREE
   Branch: Score 61-85 (Critical)
   Action: REDUCE 75% or EXIT
   Rationale:
   - Thesis assumptions invalidated by evidence
   - Growth structural slowdown, not cyclical
   - Profitability path extended; confidence loss
   - Valuation needs re-anchoring

VII. MANAGEMENT QUESTIONS FOR NEXT CALL
   Q1: "Can you walk us through the GMV growth deceleration? Is this market saturation or competitive loss?"
   Q2: "Take rate compression looks structural. What's the competitive dynamic?"
   Q3: "When do you expect EBITDA inflection? What drives it?"

VIII. NEXT STEPS
   - Monitor Q2 earnings for GMV trajectory confirmation
   - If Q2 GMV <8%, exit remaining 25%
   - If Q2 GMV rebounds to 12%+, consider re-entry signal
   - Watch for management strategy shift (price vs. volume)
```

---

## Integration with Thesis-Tracker

### Input Flow

```
1. Use /thesis-tracker {company} to establish baseline
   └─ Outputs: assumptions, red lines, valuation anchor, conviction

2. Three months later, use /thesis-drift {company}
   └─ Reads from thesis-tracker output
   └─ Compares vs. current evidence
   └─ Generates drift report + action

3. Act on decision tree
   └─ Reduce / Hold / Exit
   └─ Document why in investment journal
   └─ Set reminder for next check
```

### Output Format (JSON)

```json
{
  "company": "SHOP",
  "report_date": "2026-04-15",
  "baseline_date": "2024-07-01",
  "entry_price": 32,
  "current_price": 28,
  "thesis_baseline": {
    "core_assumptions": [
      { "assumption": "GMV CAGR ≥20%", "weight": 5, "status": "🔴 Broken" },
      { "assumption": "Take rate 2.5%+", "weight": 4, "status": "🔴 Broken" }
    ],
    "red_lines": [
      { "condition": "GMV <10% for 2 qtrs", "triggered": false }
    ]
  },
  "drift_evidence": {
    "gmv_cagr_current": "12%",
    "take_rate_current": "2.2%",
    "profitability_delay": "12 months",
    "buyback_suspended": true
  },
  "severity_score": 71,
  "severity_band": "CRITICAL",
  "decision": "REDUCE 75% or EXIT",
  "conviction_new": 35,
  "conviction_prior": 75,
  "next_check": "After Q2 earnings (July 2026)"
}
```

---

## Common Patterns & Anti-Patterns

### ✅ DO: Evidence-Driven Drift Detection

- "Revenue missed guidance by 15% for 2 consecutive quarters" → Drift signal ✓
- "Management suspended buyback citing competitive pressure" → Drift signal ✓
- "Take rate compressed 200bps YoY and stabilized" → Drift signal ✓
- "Market share lost to competitor with new capability" → Drift signal ✓

### ❌ DON'T: False Drift Triggers

- "Stock fell 30%" → Not a drift signal by itself ❌
- "Analyst downgraded valuation multiple" → Price drift, not thesis drift ❌
- "Report wording changed but facts identical" → Restatement noise, not drift ❌
- "CEO said something I dislike on earnings call" → Gut feeling, not evidence ❌

---

## Validation Checklist

Before executing drift detection:

- [ ] Thesis baseline exists (run `/thesis-tracker` if missing)
- [ ] Current evidence gathered (latest 10-K/10-Q, earnings transcript)
- [ ] All assumptions testable (not vague; linked to real metrics)
- [ ] Red lines clearly defined (specific triggers, not subjective)
- [ ] Severity score calculated with math (not gut feeling)
- [ ] Decision tree branch identified (score maps to action)
- [ ] Management questions prepared (for next earnings call)
- [ ] Position action documented (why reducing / holding / exiting)

---

## Next Steps in 1ai-Ecosystem

1. ✅ Deploy THESIS-DRIFT to 1ai-skills
2. → Wire to thesis-tracker for persistent baseline storage
3. → Build quarterly check calendar (reminders after each earnings)
4. → Create dashboard: Conviction Score vs. Current Price (visualize thesis health)
5. → Add peer benchmarking (how do others score the same drift?)
6. → Connect to alert system (when severity crosses threshold, notify immediately)

**Status**: Ready for TIER 1 deployment. Zero external dependencies. Pure framework.

---

## References

**Warren Buffett**: "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."

**Charlie Munger**: "The first rule of intelligent investing is not to lose money. The second rule is: don't forget the first rule."

**Keynes**: "When the facts change, I change my mind. What do you do?"

**Li Lu** (Berkshire VP): "Thesis drift = when the business changes, not when the price changes."

---

**Author**: AI Berkshire Integration Team  
**Date**: 2026-07-04  
**Portability**: 90pt | **Effort**: 4h | **Type**: Pure framework  
**Dependencies**: Zero (reads from thesis-tracker only)
