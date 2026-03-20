#!/usr/bin/env python3
from affiliate_ads_growth_engine.analytics.metrics import PerformanceMetrics
from affiliate_ads_growth_engine.analytics.detection import DetectionEngine
from affiliate_ads_growth_engine.config import ConfigLoader

cfg = ConfigLoader().load()
engine = DetectionEngine(cfg.get("thresholds", {}))
metrics = PerformanceMetrics(spend=100, revenue=350, clicks=300, impressions=20000, conversions=15)
print(engine.classify(metrics))
