# Architecture

## Layers
1. **Ingestion Layer**
 - Facebook Ads API connector (batch + incremental)
 - Shopee Affiliate API connector
 - CSV uploader (fallback)
 - ETL jobs scheduled via scripts/ + cron

2. **Processing + Storage**
 - Workspace config (config/default_workspace.json)
 - Data stored in Postgres (tables defined in dashboard/schema.sql)
 - Feature engineering (metrics/metrics.py)
 - Detection rules (analytics/detection.py + detection/rules.py)

3. **Intelligence Layer**
 - Creative idea/script/storyboard generators (LLM integration, EdgeTTS, etc.)
 - Campaign architect + scaling strategy (campaign/)

4. **Interface Layer**
 - Dashboard API (dashboard/api.py)
 - Telegram bot (reporting/telegram.py)
 - Exporter (CSV, Google Sheets, Notion)
 - CLI scripts (scripts/)
