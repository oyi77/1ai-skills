# fin-memory-protocol: Outcome-Weighted Memory & Audit Trail

## 5 Memory Layers

Every trade decision must log to all 5 layers:

| Layer | Contents | Format |
|-------|----------|--------|
| **Episodic** | What: entry/exit, PnL, market conditions at time | JSON |
| **Semantic** | Why: strategy, thesis, indicators, evidence tiers used | Text + tags |
| **Procedural** | How: broker, execution slippage, timing vs. plan | JSON |
| **Affective** | Emotional: confidence level (1–10), FOMO check, overconfidence flag | Score |
| **Trade Record** | Regulatory: structured JSON for MiFID II export | JSON schema |

---

## OWM Scoring Formula

For memory retrieval relevance:

```
OWM_Score = (Quality × 0.35) + (Similarity × 0.30) + (Recency × 0.20) + (Confidence × 0.10) + (Affect × 0.05)

Quality:    PnL > 0 → maps to (0.6, 1.0); PnL < 0 → maps to (0.1, 0.5) [warnings still retrieved]
Similarity: cos(current_context_embedding, memory_embedding) — semantic similarity
Recency:    Power-law decay: 30d = 0.71, 90d = 0.50, 1yr = 0.28
Confidence: max(original_confidence_score, 0.5) — floor prevents ignoring early trades
Affect:     Drawdown active → cautionary memories surface; win streak → overconfidence check
```

---

## SHA-256 Audit Trail

Every Trade Decision Record (TDR) structure:

```json
{
  "tdr_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "asset": "ticker/symbol",
  "direction": "long|short|close|hedge",
  "quantity": 0,
  "price": 0.00,
  "rationale": "free text",
  "evidence_tiers": {"T1": 0.0, "T2": 0.0, "T3": 0.0},
  "conviction_score": 0.00,
  "gate_result": "FULL|REDUCED|SKIP",
  "risk_params": {
    "stop_loss": 0.00,
    "position_pct": 0.00,
    "max_loss_$": 0.00
  },
  "behavioral_checks": {
    "confirmation_bias": false,
    "overconfidence": false,
    "fomo_flag": false
  },
  "sha256_hash": "computed at write time",
  "regulatory_flags": []
}
```

**Verification**: `sha256(JSON.stringify(tdr_without_hash_field))` must match stored hash.

---

## Behavioral Drift Detection

Run weekly reflection:
- **Strategy drift**: Are recent trades matching declared strategy? (e.g., value investor now day-trading)
- **Style creep**: Position sizes growing without corresponding strategy change?
- **Recency bias check**: Last 3 trades all same direction → flag for review
- **Loss aversion**: Cutting winners early + holding losers longer than stops → flag

**Intervention levels**:
- 1 flag: Advisory note
- 2 flags: REDUCED all new positions
- 3+ flags: SKIP all new positions pending human review

---

## Regulatory Export

MiFID II Article 17 required fields: order time, instrument, direction, quantity, price, counterparty, decision rationale.

EU AI Act Article 14: Human oversight log — document all AI-assisted decisions with human review timestamps.

Export format: JSONL (one TDR per line) or CSV for compliance software ingestion.
