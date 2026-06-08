#!/usr/bin/env python3
"""
Scrape members from Telegram group/channel for outreach.
Usage: python3 scrape_members.py @groupname output.csv
"""

import asyncio, csv, sys
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterEmpty

SESSION = "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session"


async def scrape(group_link: str, output: str = "members.csv"):
    client = TelegramClient(SESSION, 23913448, "REDACTED_ROTATED_CREDENTIAL")
    await client.connect()

    group = await client.get_entity(group_link)
    print(f"Scraping: {group.title}")

    members = []
    async for user in client.iter_participants(group, aggressive=True):
        if user.bot:
            continue
        members.append(
            {
                "id": user.id,
                "username": f"@{user.username}" if user.username else "",
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "phone": getattr(user, "phone", "") or "",
            }
        )
        if len(members) % 100 == 0:
            print(f"  Scraped: {len(members)}")

    with open(output, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "username", "first_name", "last_name", "phone"]
        )
        writer.writeheader()
        writer.writerows(members)

    print(f"✅ {len(members)} members saved to {output}")
    await client.disconnect()


if __name__ == "__main__":
    group = sys.argv[1] if len(sys.argv) > 1 else input("Group link/username: ")
    output = sys.argv[2] if len(sys.argv) > 2 else "members.csv"
    asyncio.run(scrape(group, output))
