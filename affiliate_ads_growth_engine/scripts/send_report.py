#!/usr/bin/env python3
from affiliate_ads_growth_engine.config import ConfigLoader
from affiliate_ads_growth_engine.reporting.telegram import TelegramReporter

cfg = ConfigLoader().load()
reporter = TelegramReporter(cfg["reporting"]["telegram_bot_token"], cfg["reporting"]["telegram_chat_id"])
reporter.send_message("Daily report placeholder")
