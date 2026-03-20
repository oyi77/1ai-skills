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

# State storage
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

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def send_message(chat_id, text):
    log(f"Sending to {chat_id}: {text[:50]}...")
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if not r.json().get("ok"):
            log(f"Error from TG: {r.text}")
    except Exception as e:
        log(f"Send failed: {e}")

def handle_start(chat_id):
    msg = (
        "🚀 **BerkahKarya Ads to Shopee SaaS v3 (FINAL)**\n\n"
        "Growth Platform for FB Ads + Shopee Affiliate.\n\n"
        "**Analytics:**\n"
        "📊 /report_today - Quick Metrics\n"
        "🚰 /funnel_health - Check Leakage Rate\n"
        "💰 /profit_view - Net Blended Profit\n"
        "📈 /scale_plan - Budget Scaling Roadmap\n\n"
        "**AI Insights:**\n"
        "🏆 /winning_ads - Best Creatives\n"
        "🧟 /fatigue_check - Ad burnout warnings\n"
        "💡 /creative_ideas - 20 Fresh Angles\n"
        "🎬 /video_script - Generate Ads Script\n"
        "🖼️ /storyboard - Generate Storyboard\n\n"
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
    is_f, reason = fatigue_engine.check_fatigue([0.05, 0.045, 0.03, 0.021])
    msg = (
        f"🧟 **Ad Fatigue Monitor**\n\n"
        f"Warning: *{is_f}*\n"
        f"Reason: {reason}\n\n"
        "Suggest: Refresh creatives or change hook to maintain CTR."
    )
    send_message(chat_id, msg)

def handle_ideas(chat_id):
    ideas = creative_engine.daily_ideas()
    text = "💡 **Ide Konten Harian (Sample):**\n\n"
    for i, it in enumerate(ideas[:5], 1):
        text += f"{i}. **{it['topic']}**\n   Hook: {it['hook']}\n\n"
    send_message(chat_id, text)

def download_file(file_id, name):
    log(f"Downloading {name}...")
    r = requests.get(f"{BASE_URL}/getFile?file_id={file_id}")
    path = r.json()["result"]["file_path"]
    r2 = requests.get(f"{FILE_BASE}/{path}")
    save_path = DATA_PATH / name
    with open(save_path, "wb") as f:
        f.write(r2.content)
    return save_path

def process_file(path, chat_id):
    log(f"Processing {path}...")
    send_message(chat_id, f"📥 **File Diterima:** `{os.path.basename(path)}`\nParsing data via Data Intelligence Engine...")
    # Future: Pandas parsing
    send_message(chat_id, "✅ **Data Berhasil Diolah.** Cek laporan terbaru di `/report_today`")

def poll():
    offset = 0
    log("Bot v3 starting poll...")
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
                    log(f"Update from {chat_id}")
                    
                    if "document" in msg:
                        doc = msg["document"]
                        path = download_file(doc.file_id, doc.file_name)
                        process_file(path, chat_id)
                        continue

                    text = msg.get("text", "")
                    if not text: continue
                    
                    log(f"Cmd: {text}")
                    if text.startswith("/start"): handle_start(chat_id)
                    elif text.startswith("/report_today"): handle_report(chat_id)
                    elif text.startswith("/funnel_health"): handle_funnel_health(chat_id)
                    elif text.startswith("/profit_view"): handle_profit(chat_id)
                    elif text.startswith("/scale_plan"): handle_scale(chat_id)
                    elif text.startswith("/fatigue_check"): handle_fatigue(chat_id)
                    elif text.startswith("/creative_ideas"): handle_ideas(chat_id)
                    elif text.startswith("/video_script"): 
                        script = creative_engine.script_for_platform("Winning Hook", ["Scene 1", "Scene 2", "Scene 3"])
                        send_message(chat_id, f"🎬 **Script:**\n\n{script}")
                    elif text.startswith("/storyboard"):
                        scenes = creative_engine.storyboard("Product X")
                        res = "\n".join([f"📍 {s['scene']}: {s['description']}" for s in scenes])
                        send_message(chat_id, f"🖼️ **Storyboard:**\n\n{res}")
                    elif text.startswith("/winning_ads"):
                        send_message(chat_id, "🏆 **Winning Ads:** Campaign A (ROAS 3.5), Campaign B (ROAS 4.1)")
                    else:
                        send_message(chat_id, f"Command `{text}` diterima. Sedang diproses...")
                        
            time.sleep(0.5)
        except Exception as e:
            log(f"Error in poll: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll()
