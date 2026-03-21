# Competitor Intelligence

**Automated competitor research and analysis using web search and LLM summarization.**

---

## Description

Research competitors by name or URL. Gathers pricing, features, marketing angle, and target audience via DuckDuckGo search. Summarizes findings via OmniRoute LLM into a structured markdown report.

## Usage

```bash
# Research by company name
python scripts/competitor_intel.py --name "PostAI"

# Research by URL
python scripts/competitor_intel.py --url "https://postai.com"

# Research with specific focus areas
python scripts/competitor_intel.py --name "Canva" --focus "pricing,features,api"

# Output to custom path
python scripts/competitor_intel.py --name "Buffer" --output reports/buffer_deep.md
```

## Output

Reports saved to `skills/research/competitor-intel/reports/YYYY-MM-DD-{name}.md`

Each report includes:
- Company Overview
- Pricing & Plans
- Key Features
- Marketing Angle & Positioning
- Target Audience
- Strengths & Weaknesses
- Opportunities for BerkahKarya

## Dependencies

```bash
pip install duckduckgo-search openai
```

## OmniRoute Config

- Base URL: `http://localhost:20128/v1`
- API Key: `omniroute`
- Model: `auto/pro-chat`

---

**Author:** Veris (BerkahKarya)
**Version:** 1.0.0

---

## Extended: Business Espionage Modules (added 2026-03-21)

Full competitive intelligence via `biz_spy.py`:

```bash
# Full espionage
python3 scripts/biz_spy.py --target "@targetbot" --modules social,tech,funnel,revenue,bot,model

# All modules
python3 scripts/biz_spy.py --target "competitor.com" --all
```

Modules: `social` | `ads` | `funnel` | `revenue` | `bot` | `tech` | `content` | `seo` | `model`

See `scripts/biz_spy.py` for full documentation.
