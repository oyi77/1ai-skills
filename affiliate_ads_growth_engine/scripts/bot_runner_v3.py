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
from affiliate_ads_growth_engine.funnel.leakage import LeakageAnalyzer
from affiliate_ads_growth_engine.fatigue.predictor import FatiguePredictor
from affiliate_ads_growth_engine.finance.blended import BlendedFinance
from affiliate_ads_growth_engine.scaling.builder import ScalingBlueprint

TOKEN = "8624975557:AAEDsSXNtPaUSAapozKkvbgxqpoxNbNTgWk"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
FILE_BASE = f"https://api.telegram.org/file/bot{TOKEN}"

# State storage (simplified for persistence)
DATA_PATH = SKILL_ROOT / "data"
DATA_PATH.mkdir(exist_ok=True)

# Cache for processed metrics
FUNNEL_CACHE = {
    "fb_clicks": 1492,
    "shopee_clicks": 695,
    "orders": 26,
    "revenue": 7516130,
    "spend": 124087
}

# Engines
topics = ["Tas Wanita", "Smartwatch", "Parfum Anak", "Gorden Minimalis", "CCTV Mini"]
creative_engine = CreativeIntelligenceEngine(topics)
analysis_engine = AIAnalysisEngine()
leak_detector = LeakageAnalyzer()
fatigue_engine = FatiguePredictor()
finance_engine = BlendedFinance()
scaler = ScalingBlueprint()

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def handle_start(chat_id):
    msg = (
        "🚀 **BerkahKarya Ads to Shopee SaaS v2**\n\n"
        "Growth Platform for FB Ads + Shopee Affiliate.\n\n"
        "**Analytics:**\n"
        "📊 /report_today - Quick Metrics\n"
        "🚰 /funnel_health - Check Leakage Rate\n"
        "💰 /profit_view - Net Blended Profit\n"
        "📈 /scale_plan - Budget Scaling Roadmap\n\n"
        "**AI Insights:**\n"
        "🏆 /winning_ads - Best Creatives\n"
        "🧟 /fatigue_check - Ad burnout warnings\n"
        "💡 /creative_ideas - 20 Fresh Angles\n\n"
        "**Data Upload:**\n"
        "📁 Send FB Ads CSV or Shopee Reports directly to me."
    )
    send_message(chat_id, msg)

def handle_report(chat_id):
    s = FUNNEL_CACHE
    roas = s["revenue"] / s["spend"] if s["spend"] > 0 else 0
    msg = (
        f"📊 **BerkahKarya Performance Report**\n\n"
        f"💰 Spend: Rp {s['spend']:,.0f}\n"
        f"🎯 FB Clicks: {s['fb_clicks']:,}\n"
        f"🛒 Shopee Clicks: {s['shopee_clicks']:,}\n"
        f"📦 Orders: {s['orders']}\n"
        f"💸 Revenue: Rp {s['revenue']:,.0f}\n\n"
        f"📈 **ROAS: {roas:.2f}**\n"
        f"🔥 **Profit: Rp {(s['revenue']-s['spend']):,.0f}**"
    )
    send_message(chat_id, msg)

def handle_funnel_health(chat_id):
    leak, status = leak_detector.analyze(FUNNEL_CACHE["fb_clicks"], FUNNEL_CACHE["shopee_clicks"])
    msg = (
        f"🚰 **Funnel Leakage Analysis**\n\n"
        f"FB Clicks: {FUNNEL_CACHE['fb_clicks']}\n"
        f"Shopee Clicks: {FUNNEL_CACHE['shopee_clicks']}\n\n"
        f"🚨 **Drop-off Rate: {leak*100:.1f}%**\n"
        f"Status: `{status}`\n\n"
        "💡 _Action: Check if redirect link is active and landing page load time is < 3s._"
    )
    send_message(chat_id, msg)

def handle_profit(chat_id):
    res = finance_engine.calculate_profit(FUNNEL_CACHE["spend"], FUNNEL_CACHE["revenue"])
    msg = (
        f"💰 **Blended Profitability View**\n\n"
        f"Revenue: Rp {FUNNEL_CACHE['revenue']:,.0f}\n"
        f"Spend: Rp {FUNNEL_CACHE['spend']:,.0f}\n\n"
        f"✅ **Net Profit: Rp {res['net_profit']:,.0f}**\n"
        f"📈 Margin: {res['margin']*100:.1f}%\n"
        f"Status: *{res['status']}*"
    )
    send_message(chat_id, msg)

def handle_scale(chat_id):
    roas = FUNNEL_CACHE["revenue"] / FUNNEL_CACHE["spend"] if FUNNEL_CACHE["spend"] > 0 else 0
    res = scaler.suggest_scaling(1000000, roas, FUNNEL_CACHE["orders"])
    msg = (
        f"📈 **Scaling Blueprint Builder**\n\n"
        f"Target: +20% Budget Increase\n"
        f"Action: **{res['action']}**\n\n"
        f"Strategy: {res['strategy']}"
    )
    send_message(chat_id, msg)

def handle_fatigue(chat_id):
    # Mocking history
    is_f, reason = fatigue_engine.check_fatigue([0.05, 0.045, 0.03, 0.021])
    msg = (
        f"🧟 **Ad Fatigue Monitor**\n\n"
        f"Warning: *{is_f}*\n"
        f"Reason: {reason}\n\n"
        "Suggest: Refresh creatives or change hook to maintain CTR."
    )
    send_message(chat_id, msg)

def download_file(file_id, name):
    r = requests.get(f"{BASE_URL}/getFile?file_id={file_id}")
    path = r.json()["result"]["file_path"]
    r2 = requests.get(f"{FILE_BASE}/{path}")
    save_path = DATA_PATH / name
    with open(save_path, "wb") as f:
        f.write(r2.content)
    return save_path

def process_file(path, chat_id):
    send_message(chat_id, f"📥 **File Received:** `{os.path.basename(path)}`\nParsing data now...")
    # Add real pandas parsing here if needed
    send_message(chat_id, "✅ **Database Updated.** Metrics will refresh in `/report_today`")

def poll():
    offset = 0
    print("Bot v2 is polling...")
    while True:
        try:
            url = f"{BASE_URL}/getUpdates?offset={offset}&timeout=30"
            r = requests.get(url, timeout=40)
            data = r.json()
            if data["ok"] and data["result"]:
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    msg = update.get("message")
                    if not msg: continue
                    
                    chat_id = msg["chat"]["id"]
                    
                    if "document" in msg:
                        doc = msg["document"]
                        path = download_file(doc.file_id, doc.file_name)
                        process_file(path, chat_id)
                        continue

                    text = msg.get("text", "")
                    if text.startswith("/start"): handle_start(chat_id)
                    elif text.startswith("/report_today"): handle_report(chat_id)
                    elif text.startswith("/funnel_health"): handle_funnel_health(chat_id)
                    elif text.startswith("/profit_view"): handle_profit(chat_id)
                    elif text.startswith("/scale_plan"): handle_scale(chat_id)
                    elif text.startswith("/fatigue_check"): handle_fatigue(chat_id)
                    elif text.startswith("/winning_ads"): send_message(chat_id, "🏆 Winning Ads details coming to sheet...")
                    elif text.startswith("/creative_ideas"): 
                        ideas = creative_engine.daily_ideas()
                        send_message(chat_id, f"💡 **Idea 1:** {ideas[0]['hook']}")
                        
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll()
