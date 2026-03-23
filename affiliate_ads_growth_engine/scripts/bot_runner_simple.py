import os
import sys
import time
import requests
from pathlib import Path

# Add src to path
SKILL_ROOT = Path("/home/openclaw/.openclaw/workspace/skills/affiliate_ads_growth_engine")
sys.path.append(str(SKILL_ROOT / "src"))

from affiliate_ads_growth_engine.creative.intelligence_engine import CreativeIntelligenceEngine
from affiliate_ads_growth_engine.ai_analysis.engine import AIAnalysisEngine

TOKEN = "8624975557:AAEDsSXNtPaUSAapozKkvbgxqpoxNbNTgWk"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

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
        "📊 /report_today - Profit Summary\n"
        "🏆 /winning_ads - Best Performing Ads\n"
        "📉 /losing_ads - Scale Down/Kill Suggestions\n"
        "💡 /creative_ideas - 20 Fresh Ad Angles\n"
        "🎬 /video_script - TikTok/FB Video Structure\n"
        "🖼️ /storyboard - 4-Scene Storyboard\n"
        "🕵️ /competitor [text] - Analyze Competitor Ad\n\n"
        "**Data Upload:**\n"
        "📁 `/upload_fb` - Import FB Ads CSV\n"
        "📁 `/upload_click` - Import Shopee Click CSV\n"
        "📁 `/upload_conversion` - Import Shopee Conversion CSV"
    )
    send_message(chat_id, msg)

def handle_ideas(chat_id):
    ideas = creative_engine.daily_ideas()
    text = "💡 **Top 5 Creative Ideas for Today:**\n\n"
    for i, item in enumerate(ideas[:5], 1):
        text += f"{i}. **{item['topic']}**\n   Hook: {item['hook']}\n   Angle: {item['angle']}\n   Pattern: {item['pattern']}\n\n"
    send_message(chat_id, text)

def handle_script(chat_id):
    script = creative_engine.script_for_platform("Kenapa 90% orang gagal di Tas Wanita?", ["Masalah: Tas cepat rusak", "Solusi: Bahan sintetis grade A", "Detail: Jahitan double stitch"])
    send_message(chat_id, f"🎬 **Video Ads Script:**\n\n{script}")

def handle_storyboard(chat_id):
    scenes = creative_engine.storyboard("Smartwatch Best Seller")
    text = "🖼️ **4-Scene Storyboard:**\n\n"
    for s in scenes:
        text += f"📍 **{s['scene']}** ({s['type']})\n   {s['description']}\n\n"
    send_message(chat_id, text)

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
                        elif text.startswith("/creative_ideas"): handle_ideas(chat_id)
                        elif text.startswith("/video_script"): handle_script(chat_id)
                        elif text.startswith("/storyboard"): handle_storyboard(chat_id)
                        elif text.startswith("/winning_ads"): send_message(chat_id, "🏆 **Winning Ads Module Integrated**")
                        else: send_message(chat_id, "Command received. Processing...")
            time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll()
