#!/usr/bin/env python3
"""
Telegram Raw API Sender - Workaround for cron autonomous reporting
Uses Telegram Bot API directly (HTTP POST) - no session required
"""

import requests
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/home/openclaw/.openclaw/workspace")

# Telegram Bot Configuration (from openclaw.json)
BOT_TOKEN = "8581574594:AAGzrA9DGjzJx3Ak2D6P3NhoQyXyskpMF2Q"
CHAT_ID = "5220170786"

# Telegram Bot API endpoint
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_telegram_message(message):
    """Send message via Telegram Bot API (raw HTTP)"""
    try:
        # Truncate if too long (Telegram max 4096 chars)
        if len(message) > 4000:
            message = message[:3980] + "\n\n[...truncated...]"

        # Prepare payload
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"  # Can format with Markdown
        }

        # Send via HTTP POST
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                print(f"✅ Telegram message sent (Message ID: {result['result']['message_id']})")
                return True
            else:
                print(f"❌ Telegram API error: {result.get('description')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code} - {response.text}")
            return False

    except requests.Timeout:
        print("❌ Request timeout (30s)")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Test Telegram Bot API"""
    test_message = f"""📡 **TELEGRAM RAW API TEST**

**Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is sent via **Telegram Bot API** directly (HTTP POST)
No OpenClaw session required!

Bot Token: `{BOT_TOKEN[:20]}...`
Chat ID: `{CHAT_ID}`

✅ If you see this, raw API works!
"""
    result = send_telegram_message(test_message)
    
    if result:
        print("\n✅ SUCCESS: Telegram Bot API working!")
        print("✅ Heartbeat reports will now be sent autonomously via cron!")
    else:
        print("\n❌ FAILED: Check bot token or network")

if __name__ == "__main__":
    main()