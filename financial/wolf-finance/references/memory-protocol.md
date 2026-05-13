# fin-memory-protocol: Outcome-Weighted Memory, Audit Trail & Self-Evolution

## Purpose
This module enables the skill to **learn from every outcome** and continuously improve its analytical accuracy, calibration, and risk management. It is the brain's long-term memory and the engine of self-evolution.

---

## 5 Memory Layers (Every Trade Decision Must Log All 5)

| Layer | Contents | Format |
|-------|----------|--------|
| **Episodic** | What: entry/exit, P&L, market conditions at time | JSON |
| **Semantic** | Why: strategy, thesis, indicators, evidence tiers used | Text + tags |
| **Procedural** | How: execution slippage, timing vs. plan, gate results | JSON |
| **Affective** | Emotional: confidence level (1–10), FOMO check, overconfidence flag | Score |
| **Regulatory** | Compliance: structured JSON for MiFID II / SEC audit export | JSON schema |

---

## OWM Scoring Formula (Outcome-Weighted Memory)

```
OWM_Score = (Quality × 0.35) + (Similarity × 0.30) + (Recency × 0.20) + (Confidence × 0.10) + (Affect × 0.05)

Quality:    PnL > 0 → [0.6, 1.0] | PnL < 0 → [0.1, 0.5]
Similarity: cos(current_context, memory) — semantic distance
Recency:    30d = 0.71 | 90d = 0.50 | 1yr = 0.28 (power-law decay)
Confidence: max(original_conviction, 0.5)
Affect:     Drawdown → surface cautionary | Win streak → overconfidence check
```

---

## Trade Decision Record (TDR) — SHA-256 Audit Trail

```json
{
  "tdr_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "asset": "ticker/symbol/pair",
  "asset_class": "equity|crypto|forex|commodity|fixed_income|derivative",
  "direction": "long|short|close|hedge|reduce",
  "quantity": 0,
  "price_entry": 0.00,
  "price_target": 0.00,
  "price_stop": 0.00,
  "rationale": "free text — minimum 50 words",
  "evidence_tiers": {"T1_pct": 0.0, "T2_pct": 0.0, "T3_pct": 0.0},
  "conviction_score": 0.00,
  "modules_used": ["equity-fundamental", "risk-guardian"],
  "gate_results": {
    "gate1_liquidity": "FULL|REDUCED|SKIP",
    "gate2_correlation": "FULL|REDUCED|SKIP",
    "gate3_sentiment": "FULL|REDUCED|SKIP",
    "gate4_memory": "FULL|REDUCED|SKIP",
    "gate5_regulatory": "FULL|REDUCED|SKIP",
    "final": "FULL|REDUCED|SKIP"
  },
  "risk_params": {
    "stop_loss_price": 0.00,
    "stop_loss_pct": 0.00,
    "position_pct_portfolio": 0.00,
    "max_loss_dollar": 0.00,
    "kelly_fraction": 0.00
  },
  "bias_audit": {
    "confirmation_bias": false,
    "anchoring": false,
    "recency_bias": false,
    "herd_mentality": false,
    "sunk_cost": false,
    "overconfidence": false
  },
  "behavioral_flags": {
    "fomo_flag": false,
    "revenge_trade_flag": false,
    "size_creep_flag": false,
    "consecutive_losses": 0
  },
  "outcome": {
    "exit_price": null,
    "exit_date": null,
    "pnl_pct": null,
    "pnl_dollar": null,
    "thesis_correct": null,
    "gate_vindicated": null
  },
  "lessons_learned": "",
  "sha256_hash": "computed_at_write_time",
  "regulatory_flags": []
}
```

---

## Self-Evolution Protocol (APEX)

### Automatic Triggers
| Trigger | Condition | Action |
|---------|-----------|--------|
| Win Streak | 5+ consecutive wins | Check overconfidence; consider reducing size |
| Loss Streak | 3+ consecutive losses | Reduce size 50%; full strategy review |
| Module Failure | Same module wrong 3× | Recalibrate module weight |
| Regime Change | Correlation structure breaks | Recalibrate factor weights |
| Calibration Drift | Conviction 0.8+ but win rate <50% | Recalibrate conviction mapping |
| User Feedback | Any corrective feedback | Log as T1 semantic memory |
| New Instrument | Asset class not in registry | Draft new reference module |

### Learning Loop (After Every Closed Position)
```
1. OUTCOME LOGGING
   → Record exit price, P&L, thesis status (correct/wrong/partial)
   → Was gate result (FULL/REDUCED/SKIP) vindicated by outcome?
   → Which modules generated useful signal? Which were noise?

2. CALIBRATION UPDATE
   → Win rate by module (rolling 30 trades)
   → Win rate by market regime
   → Conviction score accuracy (Brier score)
   → Update module signal weights accordingly

3. BIAS AUDIT RETROSPECTIVE
   → Which biases were present? (even if trade worked)
   → FOMO-driven trades tracked separately (usually worse)
   → Compare bias-flagged vs. clean trade performance

4. REGIME MAPPING
   → Tag each trade with regime (expansion/contraction/crisis/stagflation)
   → Build regime-conditional performance database
   → Enables better regime detection and strategy selection

5. DOCUMENTATION
   → Lessons learned: minimum 1 sentence per trade
   → Pattern library: recurring good setups
   → Anti-pattern library: recurring bad setups to avoid
```

### Conviction Score Calibration (Brier Score)
```
Brier Score = Mean((Forecast – Outcome)²)
  Forecast = conviction score (0–1)
  Outcome = 1 (worked) or 0 (failed)

Perfect calibration: Brier = 0.00
No skill baseline: Brier = 0.25
Target: Brier < 0.15

Monthly recalibration:
  → If conviction 0.8 → win rate 55%: Scale down all conviction scores
  → Build recalibration table: raw score → calibrated score
```

### Module Performance Tracking
```
Monthly, for each module:
  Precision = TP / (TP + FP)
  Recall = TP / (TP + FN)
  F1 = 2 × Precision × Recall / (Precision + Recall)

Retirement (F1 < 0.4 for 6mo): Retire or retool
Enhancement (F1 > 0.7 consistently): Increase weight, elevate priority
```

---

## Behavioral Drift Detection

**Overtrading:** >10 new positions in 7 days | average holding declining | size increasing while win rate declining

**Revenge Trading:** Entry immediately after loss with larger size | re-entering after stop-out | trading to "make back losses"

**FOMO:** Entry after >20% move without thesis update | buying what "everyone is talking about" | T3-only evidence

**Response:** Flag in TDR. 24-hour cool-down. Gate 4 automatically set to REDUCED.

---

## Memory Output Template

```
MEMORY QUERY: "[current setup description]"

TOP 3 SIMILAR PAST SETUPS (by OWM score):
  1. [Asset] | [Date] | OWM: X.XX | P&L: +X% | [CORRECT/WRONG]
     Lesson: [key takeaway]
  2. [Asset] | [Date] | OWM: X.XX | P&L: –X% | [CORRECT/WRONG]
     Lesson: [key takeaway]
  3. [Asset] | [Date] | OWM: X.XX | P&L: +X% | [CORRECT/WRONG]
     Lesson: [key takeaway]

AGGREGATE (N similar setups):
  Win Rate: X% | Avg Win: +X% | Avg Loss: –X% | Sharpe: X.X

GATE 4 RESULT: FULL | REDUCED | SKIP
BEHAVIORAL FLAGS: [None / FOMO / Revenge / Overconfidence / Recency Bias]
```
