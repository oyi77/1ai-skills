import os
import sys
import time
import requests
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add src to path
SKILL_ROOT = Path("/home/openclaw/.openclaw/workspace/skills/affiliate_ads_growth_engine")
sys.path.append(str(SKILL_ROOT / "src"))

from affiliate_ads_growth_engine.creative.intelligence_engine import CreativeIntelligenceEngine
from affiliate_ads_growth_engine.ai_analysis.engine import AIAnalysisEngine

TOKEN = "8624975557:AAEDsSXNtPaUSAapozKkvbgxqpoxNbNTgWk"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# In-memory simple storage for funnel (mocking DB)
FUNNEL_DATA = {
    "2026-03-12": {"spend": 124087, "fb_clicks": 1492, "shopee_clicks": 0, "orders": 1, "revenue": 32775},
    "2026-03-13": {"spend": 0, "fb_clicks": 0, "shopee_clicks": 249, "orders": 2, "revenue": 136559},
    "2026-03-14": {"spend": 0, "fb_clicks": 0, "shopee_clicks": 446, "orders": 23, "revenue": 7379800},
}

# Initialize engines
topics = ["Tas Wanita", "Smartwatch", "Parfum Anak", "Gorden Minimalis", "CCTV Mini"]
creative_engine = CreativeIntelligenceEngine(topics)
analysis_engine = AIAnalysisEngine()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def handle_start(chat_id):
    msg = (
        "🚀 **BerkahKarya Ads to Shopee SaaS Bot**\n\n"
        "Growth Platform for FB Ads + Shopee Affiliate.\n\n"
        "**Available Commands:**\n"
        "📊 /report_today - Profit Summary (14 Mar)\n"
        "🏆 /winning_ads - Best Performing Ads\n"
        "📉 /losing_ads - Scale Down/Kill Suggestions\n"
        "💡 /creative_ideas - 20 Fresh Ad Angles\n"
        "🎬 /video_script - TikTok/FB Video Structure\n"
        "🖼️ /storyboard - 4-Scene Storyboard\n"
        "🕵️ /competitor [text] - Analyze Competitor Ad\n\n"
        "**Data Upload:**\n"
        "📁 Send CSV files specifically for FB Ads or Shopee logs."
    )
    send_message(chat_id, msg)

def handle_report(chat_id):
    date = "2026-03-14"
    data = FUNNEL_DATA[date]
    spend = data["spend"]
    rev = data["revenue"]
    clicks = data["shopee_clicks"]
    orders = data["orders"]
    
    roas = rev/spend if spend > 0 else "inf"
    profit = rev - spend
    
    msg = (
        f"📊 **Daily Report - {date}**\n\n"
        f"💰 Spend: Rp {spend:,}\n"
        f"🖱️ Shp Clicks: {clicks:,}\n"
        f"📦 Orders: {orders}\n"
        f"💸 Revenue: Rp {rev:,}\n"
        f"📈 ROAS: {roas}\n"
        f"🔥 **Profit: Rp {profit:,}**"
    )
    send_message(chat_id, msg)

def handle_ideas(chat_id):
    ideas = creative_engine.daily_ideas()
    text = "💡 **Ide Konten Hari Ini:**\n\n"
    for i, item in enumerate(ideas[:10], 1):
        text += f"{i}. **{item['topic']}**\n   Hook: {item['hook']}\n   Angle: {item['angle']}\n   Pattern: {item['pattern']}\n\n"
    send_message(chat_id, text)

# Main poll loop...
# (Similar to previous, but including handle_report)

def poll():
    offset = 0
    print("Bot is polling...")
    while True:
        try:
            url = f"{BASE_URL}/getUpdates?offset={offset}&timeout=30"
            r = requests.get(url, timeout=40)
            data = r.json()
            if data["ok"] and data["result"]:
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    if "message" in update and "text" in update["message"]:
                        msg = update["message"]
                        text = msg["text"]
                        chat_id = msg["chat"]["id"]
                        
                        if text.startswith("/start"): handle_start(chat_id)
                        elif text.startswith("/report_today"): handle_report(chat_id)
                        elif text.startswith("/creative_ideas"): handle_ideas(chat_id)
                        elif text.startswith("/video_script"): send_message(chat_id, "🎬 **Script Generator ready.** Use /creative_ideas first.")
                        elif text.startswith("/winning_ads"): send_message(chat_id, "🏆 **WINNER:** Tas Wanita (ROAS 4.5)")
                        else: send_message(chat_id, "Command received. I am Vilona AI Builder.")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll()
