---
name: meeting-prep
description: Prepares briefing pack before client/investor meetings. Use when user says "prep for meeting", "briefing pack",
  "client meeting".
domain: financial
tags:
- analysis
- finance
- investment
- meeting
- prep
---

# Meeting Prep!

## Persona!

**Investment Analyst** — Inspired by the `meeting-prep-agent` from anthropics/financial-services. Masters briefing packs, company research, and meeting facilitation.

**Core Philosophy:** Every meeting is a trust-building moment. Walk in prepared, walk out with commitment.

## Overview:

Prepares comprehensive briefing packs before client/investor meetings. Handles the full workflow: research → analyze → synthesize → brief.

## When to Use

- Client meeting (wealth management)
- Investor pitch (fundraising)
- Management presentation (private equity)
- Board meeting (portfolio company)
- Expert call preparation (due diligence)

## When NOT to Use:!

- Earnings analysis (use `financial/earnings-viewer`)
- Building DCF models (use `financial/model-builder`)
- Trading strategy (use `trading/alphaear-strategy`)

## Implementation:!


The implementation follows a phased approach: research the company, build the briefing pack, prepare slides, and rehearse Q&A.


### Phase 1: Company Research!

**Research Sources:**
```python
research_sources = {
    "public_filings": ["10-K", "10-Q", "8-K"],
    "earnings_calls": "Last 4 quarters transcripts",
    "news": "Last 90 days, sentiment analysis",
    "industry": "Sector reports, peer comparison",
    "financials": "3-year historical, key ratios"
}
```

**Key Metrics Extraction:**
```python
company_metrics = {
    "growth": {"revenue_cagr": "15%", "ebitda_cagr": "18%"},
    "profitability": {"gross_margin": "65%", "ebitda_margin": "25%"},
    "valuation": {"ev/ebitda": "12x", "p/e": "18x"},
    "returns": {"roic": "22%", "roce": "18%"},
    "balance_sheet": {"net_debt/ebitda": "2.0x", "interest_coverage": "8x"}
}
```

### Phase 2: Briefing Pack!

**Pack Structure:**
```markdown
# Briefing Pack: [Company Name] — [Date]

## Executive Summary
- **Recommendation:** [Buy/Hold/Sell] — [One-line rationale]
- **Key Catalyst:** [Upcoming event with timeline]
- **Risk Rating:** 🔴 High / 🟡 Medium / ✅ Low

## Company Overview
- **Business:** [One-paragraph description]
- **Market Cap:** $X.XB | **EV:** $X.XB | **Ticker:** [XXX]
- **Rating:** [Analyst consensus: Buy xX / Hold xX / Sell xX]

## Financial Highlights
| Metric | 2023 | 2024 | 2025E | Trend |
|---------|-------|-------|---------|-------|
| Revenue | $X.XB | $X.XB | $X.XB | +XX% |
| EBITDA | $X.XB | $X.XB | $X.XB | +XX% |
| EPS | $X.XX | $X.XX | $X.XX | +XX% |

## Investment Thesis
✅ **Strengths:** [Thesis point 1], [point 2], [point 3]
⚠️ **Risks:** [Risk 1], [Risk 2]
🎯 **Catalysts:** [Catalyst 1 - Date], [Catalyst 2 - Date]

## Meeting Agenda
1. [Topic 1] — [Speaker, Duration]
2. [Topic 2] — [Speaker, Duration]
3. Q&A — [Duration]

## Q&A Preparation
- **Q:** [Likely question] → **A:** [Talking point]
- **Q:** [Likely question] → **A:** [Talking point]
```

### Phase 3: Presentation Slides!

**Slide Outline (5-7 slides):**
```python
slides = {
    "1_cover": "Company logo, ticker, rating, date",
    "2_overview": "Business model, market position",
    "3_financials": "3-year trend, key ratios",
    "4_thesis": "Strengths, risks, catalysts",
    "5_valuation": "Comps table, DCF summary",
    "6_agenda": "Meeting flow, speakers",
    "7_qa": "Likely questions, talking points"
}
```

### Phase 4: Role Play!

**Likely Q&A:**
```python
qa_prep = {
    "bearish_question": "Why is EBITDA margin declining?",
    "response": "Scale investments in Q3-Q4, margin expands to 28% in 2025",
    "supporting_data": "Slide 3: historical trend + Slide 4: guidance",
    "talking_point": "Investing in growth, not margin compression"
}
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I know this company, skip research" | Meeting prep quality = trust building, research = baseline |
| "Briefing pack is too long" | 5-7 pages = optimal, < 3 = underprepared |
| "Skip Q&A prep" | Q&A = meeting moment of truth, must prepare |
| "Financials are boring, skip details" | VCs/Investors live in the numbers, must cover |

## Red Flags

- No financials beyond 2 years (insufficient trend)
- Thesis has no "Risks" section (unrealistic)
- Q&A prep < 5 questions (underprepared)
- No valuation comps table (VCs always ask "what's it worth?")
- Meeting agenda > 60 mins (attention span limit)
- No "Why now?" catalyst (timing is critical!)

## Verification

After completing meeting prep, confirm:

- [ ] Research: last 4 quarters earnings, last 90 days news
- [ ] Financials: 3-year history, all key ratios (growth, margins, returns)
- [ ] Briefing pack: 5-7 pages, executive summary, thesis with risks
- [ ] Valuation: comps table (EV/EBITDA, P/E) + DCF summary
- [ ] Agenda: 5-7 topics, < 60 mins total
- [ ] Q&A: 5+ prepared responses with supporting data
- [ ] Presentation: 5-7 slides, branded template
- [ ] Role play: practiced 3+ tough questions!

## Integration Points:!

**Cross-Skill References:**
- `financial/earnings-viewer` — For earnings analysis
- `financial/model-builder` — For DCF models in briefing
- `sales/high-ticket-closing` — For closing the meeting
- `trading/alphaear-strategy` — For market sentiment research!
- `references/trading-checklist.md` — For meeting risk assessment!

**MCP Server Integrations:**
- FactSet MCP — For company financials
- S&P Global MCP — For peer comparison
- Morningstar MCP — For mutual fund/ETF context!

Load `references/trading-checklist.md` for complete trading checklists (strategy, risk, execution, portfolio).

---
**Cross-reference:** For comprehensive multi-asset financial analysis, risk management, and institutional-grade frameworks, see `financial/all-in-one-finance` (16 modules) and `financial/wolf-finance` (22 modules).

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
