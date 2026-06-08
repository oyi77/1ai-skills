#!/usr/bin/env python3
"""
Bulk DM broadcaster with rate limiting.
Usage: python3 broadcast.py --targets prospects.csv --message "Halo {name}!" --delay 30
"""

import asyncio, csv, argparse, sys
from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError, PeerFloodError

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"


async def bulk_dm(targets: list, message: str, delay: int = 30):
    client = TelegramClient(SESSION, 23913448, "REDACTED_ROTATED_CREDENTIAL")
    await client.connect()

    sent, failed = 0, 0
    for t in targets:
        username = t.get("username", t) if isinstance(t, dict) else t
        name = t.get("name", username) if isinstance(t, dict) else username
        msg = message.replace("{name}", name).replace("{username}", str(username))
        try:
            await client.send_message(username, msg)
            sent += 1
            print(f"✅ [{sent}/{len(targets)}] {username}")
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            print(f"⏳ FloodWait {e.seconds}s — pausing...")
            await asyncio.sleep(e.seconds + 10)
        except (UserPrivacyRestrictedError, PeerFloodError):
            print(f"🔒 {username}: restricted, skip")
            failed += 1
        except Exception as e:
            print(f"❌ {username}: {e}")
            failed += 1

    print(f"\n📊 Done: {sent} sent, {failed} failed")
    await client.disconnect()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--targets", required=True, help="CSV file or @username")
    parser.add_argument("--message", required=True)
    parser.add_argument("--delay", type=int, default=30)
    args = parser.parse_args()

    if args.targets.endswith(".csv"):
        with open(args.targets) as f:
            targets = list(csv.DictReader(f))
    else:
        targets = [args.targets]

    asyncio.run(bulk_dm(targets, args.message, args.delay))
