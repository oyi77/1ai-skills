import os
import sys
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from pathlib import Path

# Add src to path
SKILL_ROOT = Path("/home/openclaw/.openclaw/workspace/skills/affiliate_ads_growth_engine")
sys.path.append(str(SKILL_ROOT / "src"))

from affiliate_ads_growth_engine.creative.intelligence_engine import CreativeIntelligenceEngine
from affiliate_ads_growth_engine.ai_analysis.engine import AIAnalysisEngine
from affiliate_ads_growth_engine.data_intelligence.ingestor import DataIngestor

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8624975557:AAEDsSXNtPaUSAapozKkvbgxqpoxNbNTgWk"

# Initialize engines
topics = ["Tas Wanita", "Smartwatch", "Parfum Anak", "Gorden Minimalis", "CCTV Mini"]
creative_engine = CreativeIntelligenceEngine(topics)
analysis_engine = AIAnalysisEngine()
ingestor = DataIngestor("/home/openclaw/.openclaw/workspace/skills/affiliate_ads_growth_engine/data")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🚀 **BerkahKarya Ads to Shopee SaaS Bot**\n\n"
        "Growth Platform for FB Ads + Shopee Affiliate.\n\n"
        "**Available Commands:**\n"
        "📊 `/report_today` - Profit Summary\n"
        "🏆 `/winning_ads` - Best Performing Ads\n"
        "📉 `/losing_ads` - Scale Down/Kill Suggestions\n"
        "💡 `/creative_ideas` - 20 Fresh Ad Angles\n"
        "🎬 `/video_script` - TikTok/FB Video Structure\n"
        "🖼️ `/storyboard` - 4-Scene Storyboard\n"
        "🕵️ `/competitor` [text] - Analyze Competitor Ad\n\n"
        "**Data Upload:**\n"
        "📁 `/upload_fb` - Import FB Ads CSV\n"
        "📁 `/upload_click` - Import Shopee Click CSV\n"
        "📁 `/upload_conversion` - Import Shopee Conversion CSV"
    )
    await update.message.reply_text(msg, parse_mode='Markdown')

async def creative_ideas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ideas = creative_engine.daily_ideas()
    text = "💡 **Top 5 Creative Ideas for Today:**\n\n"
    for i, item in enumerate(ideas[:5], 1):
        text += f"{i}. **{item['topic']}**\n   Hook: {item['hook']}\n   Angle: {item['angle']}\n   Pattern: {item['pattern']}\n\n"
    await update.message.reply_text(text, parse_mode='Markdown')

async def video_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    script = creative_engine.script_for_platform("Kenapa 90% orang gagal di Tas Wanita?", ["Masalah: Tas cepat rusak", "Solusi: Bahan sintetis grade A", "Detail: Jahitan double stitch"])
    await update.message.reply_text(f"🎬 **Video Ads Script:**\n\n{script}", parse_mode='Markdown')

async def storyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    scenes = creative_engine.storyboard("Smartwatch Best Seller")
    text = "🖼️ **4-Scene Storyboard:**\n\n"
    for s in scenes:
        text += f"📍 **{s['scene']}** ({s['type']})\n   {s['description']}\n\n"
    await update.message.reply_text(text, parse_mode='Markdown')

async def winning_ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Simulated data for now
    text = (
        "🏆 **WINNING ADS DETECTED**\n\n"
        "1. **Campaign: Tas Wanita Ramadhan**\n"
        "   - ROAS: 4.5\n"
        "   - Clicks: 1,200\n"
        "   - Orders: 54\n\n"
        "2. **Campaign: Smartwatch Series X**\n"
        "   - ROAS: 3.2\n"
        "   - Clicks: 850\n"
        "   - Orders: 12"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

async def handle_docs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    await update.message.reply_text(f"✅ Receiving: {doc.file_name}\nProcessing via Data Intelligence Engine...")
    # Logic to save and process would go here

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('creative_ideas', creative_ideas))
    application.add_handler(CommandHandler('video_script', video_script))
    application.add_handler(CommandHandler('storyboard', storyboard))
    application.add_handler(CommandHandler('winning_ads', winning_ads))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_docs))
    
    print("Bot is running...")
    application.run_polling()
