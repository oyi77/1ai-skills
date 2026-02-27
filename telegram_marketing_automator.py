#!/usr/bin/env python3
"""
TELEGRAM MARKETING AUTOMATOR (LIVE AUTO-REPLY MODE)
Author: Vilona AI Architect
Date: 2026-02-28
Mode: SMART BOT (Live Auto-Reply Only - No Broadcast Spam)
"""

import telebot
import requests
import time
import logging
import random
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler('/home/openclaw/.openclaw/workspace/output/telegram_bot_activity.log'),
        logging.StreamHandler()
    ]
)

# === CONFIGURASI VERIS (USER) ===
# Ambil dari input chat terakhir
TOKEN = "8665546627:AAE2oKXp7BcpN3tGf1jNSpRPotMYwM8DEM" # VERIS TOKEN
LYNX_PRODUCT_URL = "https://lynx.id"  # Placeholder - UPDATE ME INI
SCALEV_PRODUCT_URL = "https://scalev.io" # Placeholder - UPDATE ME INI
NETLIFY_BUNDLE_URL = "https://berkahkarya.org/bundle.html" # Placeholder - UPDATE ME INI

# === JAWABAN PROMOSI PINTAR (PAIN-AGITATE) ===
PROMO_REPLY = {
    "beli": f"🦾 Pakai Veris! Ini adalah 'All-Access Pass' seharga Rp 499.000. Akses 14+ Tools AI BerkahKarya SEUMUR HIDUP. Pembelian aman via Lynx.id:\n\n{LYNX_PRODUCT_URL}",
    "harga": f"💰 Harga Promo: Rp 499.000 (Coret dari Rp 2.499.000). Hemat 80% Sekarang!",
    "nomor": f"📞 Hubungi Admin via WhatsApp: 0812-3456-7890 (Veris). Pembayaran bisa via Transfer Bank.",
    "join": f"🚀 Gabung Grup Premium! Akses update tools baru, blueprint scaling, dan support langsung via Telegram. Link: https://t.me/berkahkarya",
    "grup": f"👥 Sama kayak di atas, gabung komunitas agensi digital kita. Kita bisa sharing strategi di sana.",
    "diskusi": f"💡 Boleh diskusi? Apa yang mau lo bahas? Marketplace, iklan, atau teknik sales? Gue (AI) akan bantu breakdown.",
    "default": f"👋 Halo! Terima kasih sudah mau beli paket berkahkarya. Mohon info selanjutnya via DM atau WA ya Boss! ✨"
}

# === GREETINGS (HUMAN-LIKE) ===
GREETINGS = [
    "Halo Boss! Ada yang bisa gue bantu?",
    "Siang Bro! Ready for action.",
    "Halo Kak! Mau info paket All-Access?",
    "Malam Pak! Kapan landing?"
    "Pagi Mas! Gue standby."
]

# === KEYWORD DETECTION ===
SELLING_KEYWORDS = ["beli", "harga", "nomor", "tanya", "order", "transfer", "bayar"]
GROUP_KEYWORDS = ["join", "gabung", "grup", "masuk", "daftar"]
IGNORE_KEYWORDS = ["test", "cek", "debug", "hello", "halo", "salam", "siang", "pagi"]

# === TELEGRAM BOT SETUP ===
bot = telebot.TeleBot(TOKEN)

def start(message):
    chat_id = message.chat.id
    if chat_id.type == 'private':
        bot.send_message(chat_id, "🦾 Vilona Marketing Bot AKTIF.\n\nMode: Live Auto-Reply (Smart).\n\nFitur:\n- Auto-Reply 'Beli', 'Harga', 'Nomor'.\n- Auto-Reply 'Join', 'Grup'.\n- No Broadcast Spam.\n\nSiap menerima pesan...")
    else:
        logging.info(f"Bot added to group: {chat_id.title}")

def handle_message(message):
    """Main handler: Smart Keyword Detection & Auto-Reply"""
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    logging.info(f"[MSG] From: {user_name} ({user_id}) | Text: {text}")

    # 1. JANGAN PROSES IGNORE KEYWORDS (Optimasi)
    if text and any(kw in text.lower() for kw in IGNORE_KEYWORDS):
        return # Stop processing immediately

    # 2. GREETINGS CHECK (Random Human-Like)
    if text.lower() in ["halo", "siang", "pagi", "salam", "hai", "bro", "sis", "kak"]:
        greeting = random.choice(GREETINGS)
        time.sleep(random.uniform(1.0, 2.5)) # Natural delay
        try:
            bot.send_message(chat_id, greeting)
            logging.info(f"[GREETING] Replied to {user_name}: {greeting}")
        except Exception as e:
            logging.error(f"[GREETING] Error: {str(e)}")
        return # Stop here, don't double reply

    # 3. LOGIC UTAMA (KEYWORD MATCHING)
    lower_text = text.lower()
    
    # Deteksi Kategori Pesan
    is_selling = any(kw in lower_text for kw in SELLING_KEYWORDS)
    is_group_request = any(kw in lower_text for kw in GROUP_KEYWORDS)
    is_discussion = "diskusi" in lower_text or "tanya" in lower_text

    # LOGIC GROUP (JALANIN / GRUP BARU)
    if chat_id.type == 'supergroup' or chat_id.type == 'group':
        if is_group_request:
            # Jangan promosi terus-terus di grup yang sama
            chance = random.randint(1, 3)
            if chance == 1: # 33% chance to reply
                reply = random.choice([
                    "👥 Info grup ada di DM Bosku ya, biar gak spam di sini.",
                    f"🚀 Daftar lewat link di: {LYNX_PRODUCT_URL}"
                ])
                try:
                    bot.send_message(chat_id, reply, reply_to_message_id=message.message_id)
                except Exception as e:
                    logging.error(f"[GROUP] Error: {str(e)}")
            return
        else:
            # Jangan jawab diskusi di grup, biar DM aja
            return # Stop here
    
    # LOGIC PRIVATE (DM / GROUP) - Fokus Jualan
    if chat_id.type == 'private' or chat_id.type == 'supergroup':
        if is_selling:
            # Cek keyword spesifik
            if "beli" in lower_text:
                reply_text = PROMO_REPLY["beli"]
            elif "harga" in lower_text:
                reply_text = PROMO_REPLY["harga"]
            elif "nomor" in lower_text:
                reply_text = PROMO_REPLY["nomor"]
            else:
                reply_text = PROMO_REPLY["default"]
            
            # JUALAN MODE: Kirim Link Jualan
            # Logic: Kirim link Lynx/Netlify secara langsung (tanpa harus order manual lagi)
            try:
                # Kirim "Typing..." action
                bot.send_chat_action(chat_id, 'typing')
                time.sleep(random.uniform(2.0, 4.0)) # Delay simulasi ngetik
                
                # Kirim Pesan Jualan
                sent_msg = bot.send_message(chat_id, reply_text)
                logging.info(f"[SALES] Replied to {user_name} for 'buy': {sent_msg.message_id}")
                
            except Exception as e:
                logging.error(f"[SALES] Error: {str(e)}")
            return

        elif is_group_request:
            reply_text = PROMO_REPLY["join"]
            try:
                bot.send_message(chat_id, reply_text)
                logging.info(f"[GROUP] Replied to {user_name} for 'join': {reply_text}")
            except Exception as e:
                logging.error(f"[GROUP] Error: {str(e)}")
            return

        elif is_discussion:
            reply_text = PROMO_REPLY["diskusi"]
            try:
                bot.send_message(chat_id, reply_text)
                logging.info(f"[DISCUSSION] Replied to {user_name}: {reply_text}")
            except Exception as e:
                logging.error(f"[DISCUSSION] Error: {str(e)}")
            return

def error(update, context):
    """Global Error Handler"""
    logging.error(f"[ERROR] Update {update} caused error {context.error}")

if __name__ == '__main__':
    logging.info("🦾 VILONA TELEGRAM MARKETING BOT STARTED")
    logging.info(f"Mode: LIVE AUTO-REPLY (Smart)")
    logging.info("Listening for messages...")
    
    bot.infinity_polling(timeout=10, long_polling=True)
