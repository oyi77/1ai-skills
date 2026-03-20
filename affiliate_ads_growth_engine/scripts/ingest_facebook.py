#!/usr/bin/env python3
from affiliate_ads_growth_engine.config import ConfigLoader
from affiliate_ads_growth_engine.workspace import Workspace
from affiliate_ads_growth_engine.data_sources.facebook_ads import FacebookAdsConnector

cfg = ConfigLoader().load()
workspace = Workspace(cfg)
connector = FacebookAdsConnector(cfg["facebook"]["access_token"])

for account in workspace.facebook_accounts:
 data = connector.get_insights(account)
 print(f"Fetched {len(data.get('data', []))} rows for {account}")
