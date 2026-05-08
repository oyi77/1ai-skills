---
name: ai-readiness
description: Assess portfolio company AI readiness, AI adoption maturity. Use when user says "AI readiness", "AI maturity", "assess AI adoption".
---

# AI Readiness!

## Persona:!

**AI Strategist** — Inspired by the `ai-readiness` skill from anthropics/financial-services. Masters AI adoption frameworks, maturity assessment, and value creation through AI.

**Core Philosophy:** AI readiness isn't about having GPUs — it's about culture, data, and leadership. Assess the COMPANY, not the tech stack.

## Overview:!

Assesses portfolio company AI readiness across 5 dimensions: Strategy, Data, Tech, Culture, ROI. Outputs maturity score (1-5) and roadmap.

## When to Use:!

- Due diligence (pre-investment)
- Board presentation (AI strategy update)
- Portfolio company assessment (annual)
- Value creation planning (AI-driven)
- Strategic review (underperforming AI adoption)
- Investment committee memo (AI thesis)

## When NOT to Use:!

- Earnings analysis (use `financial/earnings-viewer`)
- Building DCF models (use `financial/model-builder`)
- General portfolio monitoring (use `financial/portfolio-monitor`)
- Pitch deck creation (use `financial/pitch-deck`)

## Implementation:!

### Phase 1: Strategy Assessment!

**AI Strategy Scorecard:**
```python
strategy_assessment = {
    "vision": {
        "score": 4,  # 1-5
        "evidence": "CEO committed, AI-first messaging",
        "gap": "No AI KPIs linked to exec comp"
    },
    "governance": {
        "score": 3,
        "evidence": "AI steering committee exists",
        "gap": "No AI risk framework documented"
    },
    "roadmap": {
        "score": 5,
        "evidence": "3 AI products launched 2024",
        "gap": "No 2026-2027 AI roadmap yet"
    }
}
```

### Phase 2: Data Maturity!

**Data Readiness:**
```python
data_assessment = {
    "infrastructure": {
        "score": 3,  # 1-5
        "details": "Data lake exists, but siloed",
        "gap": "No unified data warehouse"
    },
    "quality": {
        "score": 4,
        "details": "95% clean customer data",
        "gap": "5% products missing category tags"
    },
    "governance": {
        "score": 2,
        "details": "No data lineage tracking",
        "gap": "Implement data catalog + lineage"
    }
}
```

### Phase 3: Tech Stack!

**AI/ML Capabilities:**
```python
tech_assessment = {
    "mlops": {
        "score": 3,
        "tools": "Basic MLflow, limited automation",
        "gap": "No model registry, no A/B testing"
    },
    "infrastructure": {
        "score": 4,
        "cloud": "AWS (SageMaker)",
        "gap": "No GPU cluster for training"
    },
    "talent": {
        "score": 3,
        "headcount": "5 data scientists, 2 ML engineers",
        "gap": "No Chief AI Officer"
    }
}
```

### Phase 4: ROI Analysis!

**AI Value Creation:**
```python
roi_analysis = {
    "cost_savings": {
        "2023": 500000,   # $500K
        "2024": 1200000,  # $1.2M
        "2025_pct": 8000000,  # $8M projected
        "roi": "3.5x"   # Return on AI investment
    },
    "revenue_growth": {
        "ai_products": "$12M (15% of revenue)",
        "growth_rate": "80% YoY",
        "target": "25% of revenue by 2027"
    }
}
```

### Phase 5: Maturity Score!

**Overall AI Readiness (1-5):**
```python
maturity_score = {
    "overall": 3.4,  # Weighted average
    "strategy": 4.0,
    "data": 3.0,
    "tech": 3.5,
    "culture": 3.0,
    "roi": 4.0
}
# Interpretation:
# 1.0-1.9 = AI Novice (avoid or heavy discount)
# 2.0-2.9 = AI Explorer (monitor closely)
# 3.0-3.9 = AI Adopter (standard weighting)
# 4.0-4.9 = AI Leader (premium valuation)
# 5.0 = AI Native (top-tier valuation)
```

### Phase 6: Roadmap!

**AI Roadmap (100-Day Plan):**
```markdown
# AI Roadmap: [Company Name]

## Quick Wins (0-30 Days)
1. ✅ Appoint Chief AI Officer
2. ✅ Launch data catalog (lineage tracking)
3. ✅ Set AI KPIs for exec team

## Foundation (30-60 Days)
1. Build unified data warehouse (Snowflake/BigQuery)
2. Implement MLOps (model registry + A/B testing)
3. Hire 3 more ML engineers

## Scale (60-100 Days)
1. Launch 3 AI products (generative AI features)
2. Achieve $20M AI revenue run-rate
3. Target AI Readiness: 4.0+ (up from 3.4)
```

## Common Rationalizations:!

| Rationalization | Reality |
|---|---|
| "They have GPUs, they're AI-ready" | GPUs ≠ strategy/culture/data — assess ALL 5 dimensions |
| "AI readiness is a tech checklist" | Culture = #1 predictor of AI success (people, not tools) |
| "Startup, skip assessment" | Early-stage = biggest AI upsie potential OR downfall |
| "5.0 is the goal always" | 3.5-4.0 is plenty for most B2B companies |

## Red Flags:!

- AI readiness < 2.0 (novice — heavy discount or pass)
- No AI strategy (CEO doesn't mention AI in earnings)
- Data quality < 80% (garbage in, garbage out)
- No AI talent (0 data scientists/ML engineers)
- ROI < 1.5x (AI investment losing money!)
- No AI KPIs (not measured = not managed)
- Culture score < 2.5 (leaders don't understand AI)

## Verification:!

After completing AI readiness assessment, confirm:

- [ ] Strategy assessed: vision, governance, roadmap (all 1-5 scored)
- [ ] Data assessed: infrastructure, quality, governance (all scored)
- [ ] Tech assessed: MLOps, infrastructure, talent (all scored)
- [ ] Culture assessed: leadership, talent, adoption (all scored)
- [ ] ROI calculated: cost savings, revenue growth, ROI multiple
- [ ] Overall score: 1-5 with weighted breakdown
- [ ] Roadmap: 100-day plan with quick wins + foundation + scale
- [ ] Report generated: 3-5 pages, maturity score highlighted
- [ ] Investment thesis: AI impact assessed (strengthens/weakens/neutral)

## Integration Points:!

**Cross-Skill References:**
- `financial/model-builder` — For AI-driven revenue in DCF
- `financial/meeting-prep` — For board presentation
- `trading/black-edge` — For AI competitive intelligence
- `references/trading-checklist.md` — For AI investment risk!

**MCP Server Integrations:**
- PitchBook MCP — For AI company comps
- S&P Global MCP — For AI sector analysis
- FactSet MCP — For AI adoption benchmarking!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).
