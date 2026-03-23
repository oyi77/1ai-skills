# User Flows

## Onboarding
1. Create workspace (config/default_workspace.json copy)
2. Add FB ad accounts + Shopee affiliate credentials
3. Schedule ingestion jobs
4. Connect Telegram bot + dashboard login

## Daily Ops
1. Ingest new data (`scripts/ingest_*`)
2. Run detection (`scripts/detect_winners.py`)
3. Push Telegram report (`scripts/send_report.py`)
4. Generate creatives + campaign blueprint as needed
5. Apply scaling strategies + push to FB Ads

## Alert Flow
- Detection finds winning/losing ads
- Record in DB + send Telegram alert
- Suggest actions (duplicate, kill, scale)
