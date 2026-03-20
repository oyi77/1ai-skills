#!/usr/bin/env python3
from affiliate_ads_growth_engine.config import ConfigLoader
from affiliate_ads_growth_engine.workspace import Workspace
from affiliate_ads_growth_engine.data_sources.shopee_affiliate import ShopeeAffiliateConnector
import time

cfg = ConfigLoader().load()
workspace = Workspace(cfg)

shopee = cfg["shopee"]
connector = ShopeeAffiliateConnector(shopee["partner_id"], shopee["partner_key"], shopee["shop_id"], shopee["affiliate_token"])
now = int(time.time())
start = now -86400
orders = connector.get_affiliate_order(start, now)
print(orders)
