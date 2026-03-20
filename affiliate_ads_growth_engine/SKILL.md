# Affiliate Ads Growth Engine

> Multi-tenant AI Growth Platform for Facebook Ads + Shopee Affiliate.

## Vision
Standalone SaaS platform that ingests marketing data, detects winners/losers, generates creatives, automates campaign structures, and pushes strategy/analytics to the team (dashboard + Telegram). Built for affiliate marketers scaling Facebook Ads + Shopee Affiliate offers.

## Capabilities
1. **Data ingestion layer**
 - Facebook Ads API (ad accounts, campaigns, ads, insights)
 - Shopee Affiliate API (order, commission, product performance)
 - Custom CSV upload (if API unavailable)
 - Schedule ETL tasks per workspace

2. **Analytics + Detection**
 - Unified performance model (blended ROAS, CPL, CPA, EPC)
 - Winning vs losing detection (thresholds + anomaly detection)
 - Cohort filters (date range, country, platform, objective)
 - Alerting rules (telegram, email)

3. **Creative Intelligence Engine**
 - Auto-generate20+ fresh ad ideas per day (hooks + angles + patterns)
 - TikTok/Facebook script builder (Hook + Scenes + CTA format)
 - Storyboard builder (Problem → Solution → Product → CTA)
 - Creative pattern detector (testimonial, before-after, problem-solution, lifestyle)

4. **Competitor Ads Intelligence**
 - Input: Facebook Ads Library link, screenshot, or ad text
 - Detect hook, creative style, audience target, marketing strategy, campaign structure
 - Output: structured competitor strategy brief + action items

5. **Data Intelligence Engine**
 - Accepts Facebook Ads CSV/XLS, Shopee Click CSV, Shopee Conversion CSV
 - Normalizes campaign/adset/ad metrics + affiliate clicks/orders into one schema
 - Builds full funnel view: FB Ads → Click → Shopee Click → Order
 - Computes spend, impressions, clicks, CTR, CPC, Shopee clicks, orders, revenue, commission, conversion rate, ROAS, profit

6. **AI Analysis Engine**
 - Winning/losing detection with customizable thresholds (ROAS/CTR/CR/spend)
 - Outputs structured WINNING ADS + LOSING ADS tables (campaign, adset, creative, spend, orders, ROAS)
 - Analyzes hook, audience, creative style, best-selling products

7. **Advanced Analytics & Growth Modules**
 - **Leakage Rate Analysis** (Drop-Off Detector): Monitors CTR loss between FB clicks and Shopee landing.
 - **Ad Fatigue Prediction** (Creative Lifetime): Detects CTR decline and suggests creative refresh.
 - **Blended Profitability & Cashflow**: Calculates real net profit after ad costs and overhead.
 - **Scaling Blueprint Builder**: Automated budget recommendation (+20% increments) based on winning thresholds.

8. **Campaign Architect**
 - Blueprint builder: CBO/ABO structures, budget splits, placements
 - Scaling strategy recommendations (horizontal/vertical)
 - Experiment generator (audience splits, creative batches)
 - Push-to-Facebook (draft campaign creation via API)

9. **Reporting + Automation Suite**
 - Telegram bot commands (`/start`, `/report_today`, `/funnel_health`, `/profit_view`, `/scale_plan`, `/fatigue_check`, `/winning_ads`, `/creative_ideas`, `/video_script`, `/storyboard`)
 - Auto daily Telegram report + Google Drive + Google Sheets archival
 - Dashboard (spend vs revenue, ROAS, campaign/creative/hook performance)
 - Export: CSV, Google Sheets, Notion sync

## Architecture Overview
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Data Sources │ → │ Processing │ → │ Insights │
│ - FB Ads │ │ - ETL jobs │ │ - Detection │
│ - Shopee Aff. │ │ - Feature eng │ │ - Creative AI │
└──────────────┘ └──────────────┘ └──────┬───────┘
 │
 ┌───────────────────┴─────────────────┐
 │ Interfaces │
 │ - Dashboard (Next.js) │
 │ - Telegram bot │
 │ - API / Webhooks │
 └──────────────────────────────────────┘
```

## Directory Layout
```
skills/affiliate_ads_growth_engine/
├── SKILL.md
├── README.md
├── docs/
│ ├── architecture.md
│ ├── data_models.md
│ └── user_flows.md
├── config/
│ └── default_workspace.json
├── src/affiliate_ads_growth_engine/
│ ├── __init__.py
│ ├── config.py
│ ├── workspace.py
│ ├── data_sources/
│ │ ├── facebook_ads.py
│ │ ├── shopee_affiliate.py
│ │ └── csv_loader.py
│ ├── analytics/
│ │ ├── metrics.py
│ │ └── detection.py
│ ├── detection/
│ │ └── rules.py
│ ├── creative/
│ │ ├── idea_generator.py
│ │ ├── script_generator.py
│ │ └── storyboard.py
│ ├── campaign/
│ │ ├── architect.py
│ │ └── scaling.py
│ ├── reporting/
│ │ ├── telegram.py
│ │ ├── exporter.py
│ │ └── scheduler.py
│ ├── dashboard/
│ │ ├── api.py
│ │ └── schema.sql
│ └── utils/
│ ├── http.py
│ ├── auth.py
│ └── logger.py
└── scripts/
 ├── ingest_facebook.py
 ├── ingest_shopee.py
 ├── detect_winners.py
 ├── generate_creatives.py
 ├── build_campaign.py
 ├── send_report.py
 └── run_dashboard.py
```

## Workspace Support
- Multi-tenant by design: each workspace has its own config (API keys, ad accounts, data storage)
- SaaS ready: onboarding script provisions database tables + Telegram bot token + report schedule

## Next Steps
1. Implement config + workspace loader (config/default_workspace.json)
2. Build Facebook Ads + Shopee Affiliate connectors (data_sources/)
3. Implement analytics/detection modules
4. Hook creative generators to existing content engine (or integrate with existing video pipeline)
5. Build CLI + scheduler for automation
