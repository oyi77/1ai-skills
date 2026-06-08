#!/usr/bin/env python3
"""
Persistent daemon: keyword monitor + auto-responder.
Run: python3 monitor_daemon.py
Stops: Ctrl+C or kill PID
"""

import asyncio, json, os
from datetime import datetime
from telethon import TelegramClient, events

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"
LOG_FILE = "/home/openclaw/.openclaw/workspace/logs/tg_monitor.log"
PAIJO_ID = 5220170786
OPENCLAW_BOT_ID = 8581574594

# Keywords that trigger alert to Paijo
ALERT_KEYWORDS = [
    "urgent",
    "bayar",
    "komplain",
    "error",
    "down",
    "masalah",
    "gagal",
    "refund",
]

# Auto-reply keywords (for DMs to our account)
AUTO_REPLIES = {
    "harga": "Harga paket kami mulai IDR 75K. Cek selengkapnya: https://lynk.id/jendralbot 🔥",
    "price": "Our packages start from IDR 75K. Check: https://lynk.id/jendralbot 🔥",
    "daftar": "Klik di sini untuk daftar: https://lynk.id/jendralbot ✅",
    "info": "Info lengkap ada di: https://lynk.id/jendralbot 📋",
    "beli": "Untuk pembelian, kunjungi: https://lynk.id/jendralbot 🛒",
    "gratis": "Ada produk GRATIS di sini: https://lynk.id/jendralbot 🎁",
}

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


async def main():
    client = TelegramClient(SESSION, 23913448, "REDACTED_ROTATED_CREDENTIAL")
    await client.connect()
    me = await client.get_me()
    log(f"✅ Monitor started as @{me.username}")

    # Monitor groups for alert keywords
    @client.on(events.NewMessage(incoming=True))
    async def handler(event):
        text = (event.text or "").lower()
        sender = await event.get_sender()
        sender_name = getattr(sender, "first_name", "Unknown")
        chat = await event.get_chat()
        chat_name = getattr(chat, "title", getattr(chat, "first_name", "DM"))
        is_dm = not event.is_group and not event.is_channel

        # Alert keywords in groups
        if not is_dm:
            for kw in ALERT_KEYWORDS:
                if kw in text:
                    alert = (
                        f"🚨 KEYWORD: '{kw}'\n"
                        f"Group: {chat_name}\n"
                        f"From: {sender_name}\n"
                        f"Msg: {event.text[:200]}"
                    )
                    log(f"ALERT: {alert}")
                    await client.send_message(PAIJO_ID, alert)
                    break

        # Auto-reply to DMs — NEVER reply to self (PAIJO_ID), bot owner, or OpenClaw Bot
        # Also ignore all bots to prevent loops
        EXCLUDED_IDS = [PAIJO_ID, me.id, OPENCLAW_BOT_ID]

        # Rigorous Bot Filtering
        is_bot = getattr(sender, "bot", False)
        sender_username = getattr(sender, "username", "") or ""
        is_bot_name = (
            sender_username.lower().endswith("bot") or "bot" in sender_name.lower()
        )

        if is_dm and sender.id not in EXCLUDED_IDS and not is_bot and not is_bot_name:
            for kw, reply in AUTO_REPLIES.items():
                if kw in text:
                    await event.reply(reply)
                    log(f"AUTO_REPLY to {sender_name} ({sender.id}): kw='{kw}'")
                    break

    log("👂 Listening for messages... (Ctrl+C to stop)")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
