#!/usr/bin/env python3
"""
Task Alert System — DM + Ring escalation.
Usage: python3 alert.py --target @username --level dm|ring|both --message "text"
"""
import asyncio, argparse
from telethon import TelegramClient
from ring_call import ring, SESSION, API_ID, API_HASH

MANAGEMENT = {
    "veris": "@alwayscuanbos",   # Ads Master (id=157228659)
    "paijo": "@codergaboets",    # CEO (id=5220170786)
    "sony": 7963750650,          # Ops Manager (Mas Sony, +6285811600060)
    # "nuno": "@nuno_username",  # Trading Master
}


async def send_dm(username: str, message: str):
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.connect()
    await client.send_message(username, message)
    print(f"💬 DM → {username}: {message[:50]}")
    await client.disconnect()


async def alert_all_management(message: str, ring_seconds: int = 8):
    """Alert all management: DM + ring everyone."""
    for name, username in MANAGEMENT.items():
        print(f"🚨 Alerting {name} ({username})...")
        await send_dm(username, f"🚨 URGENT: {message}")
        await ring(username, ring_seconds)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", default="all", help="@username or 'all'")
    parser.add_argument("--level", choices=["dm", "ring", "both"], default="dm")
    parser.add_argument("--message", required=True)
    parser.add_argument("--ring-seconds", type=int, default=8)
    args = parser.parse_args()

    targets = list(MANAGEMENT.values()) if args.target == "all" else [args.target]

    for target in targets:
        if args.level in ("dm", "both"):
            await send_dm(target, args.message)
        if args.level in ("ring", "both"):
            await ring(target, args.ring_seconds)


if __name__ == "__main__":
    asyncio.run(main())
