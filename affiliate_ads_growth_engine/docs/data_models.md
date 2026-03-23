# Data Models

## Tables (Postgres)
- `workspaces` — multi-tenant config
- `facebook_ads_campaigns`
- `facebook_ads_adsets`
- `facebook_ads_ads`
- `facebook_ads_insights`
- `shopee_affiliate_orders`
- `shopee_affiliate_products`
- `creative_briefs`
- `campaign_blueprints`
- `alerts`
- `reports`

## Metrics
- `roas`, `cpa`, `cpl`, `ctr`, `cpm`, `frequency`
- `commission`, `epc`, `conversion_rate`
- Rolling windows:1d,3d,7d,30d

## Detection thresholds
- Customizable per workspace (config)
- Example: winning if ROAS >=2.0 & CPA <= target
