---
name: telegram-userbot
description: Full MTProto control of Telegram account via Telethon. DM, Voice Note, Call, Video Call, Group/Channel management, member scraping, bot cloning, outreach automation, broadcast, CRM tracking, content reposting, scheduled messaging, webhook triggers. Use for all Telegram automation as a real user (not bot API).
---

# Telegram Userbot — Full Control

Complete Telegram automation as real user @codergaboets.

## Account
- **Username**: @codergaboets | **Phone**: +6281347241993
- **API ID**: 23913448 | **API Hash**: REDACTED_ROTATED_CREDENTIAL
- **Session**: `.vilona/sessions/paijo.session`

## Quick Client

```python
from telethon import TelegramClient

client = TelegramClient(
    "/home/openclaw/.openclaw/workspace/.vilona/sessions/paijo.session",
    23913448, "REDACTED_ROTATED_CREDENTIAL"
)
await client.connect()
```

---

## 1. Messaging (DM & Group)

```python
# DM
await client.send_message("@username", "pesan")

# Reply to message
await client.send_message("@username", "reply", reply_to=msg_id)

# DM with media
await client.send_file("@username", "/path/file.jpg", caption="caption")

# Group message
await client.send_message(-1001234567890, "pesan ke grup")

# Pin message in group (admin only)
await client.pin_message(-1001234567890, msg_id)

# Edit message
await client.edit_message("@username", msg_id, "pesan baru")

# Delete message
await client.delete_messages("@username", [msg_id])
```

---

## 2. Voice Note (TTS)

```bash
pip install edge-tts --break-system-packages
python3 scripts/send_voice.py @username "teks pesan" id
```

```python
# Indonesian voice: id-ID-ArdiNeural (male) or id-ID-GadisNeural (female)
import edge_tts, asyncio, os, tempfile
from telethon import TelegramClient

async def send_voice(username, text, lang="id"):
    voice = "id-ID-ArdiNeural" if lang == "id" else "en-US-GuyNeural"
    mp3 = tempfile.mktemp(suffix=".mp3")
    ogg = mp3.replace(".mp3", ".ogg")
    await edge_tts.Communicate(text, voice).save(mp3)
    os.system(f"ffmpeg -i {mp3} -c:a libopus {ogg} -y -loglevel quiet")
    await client.send_file(username, ogg, voice_note=True)
    os.remove(mp3); os.remove(ogg)
```

---

## 3. Ring Call (Alert)

```bash
python3 scripts/ring_call.py @username 10   # ring 10 detik lalu hang up
```

```python
from scripts.ring_call import ring
await ring("@username", ring_seconds=8)
```

---

## 4. Video Call
```python
# Initiate video call (same as ring but video=True)
result = await client(RequestCallRequest(
    user_id=user, g_a_hash=g_a_hash, protocol=protocol,
    video=True,  # <-- video call
    random_id=random.randint(0, 0x7FFFFFFF)
))
```

---

## 5. Group Operations

```python
# Send to group
await client.send_message(-1001234567890, "pesan")

# Get all group members
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

result = await client(GetParticipantsRequest(
    channel=group, filter=ChannelParticipantsSearch(""),
    offset=0, limit=200, hash=0
))
members = result.users

# Kick member (admin)
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from datetime import datetime, timedelta
await client(EditBannedRequest(
    channel=group, participant=user,
    banned_rights=ChatBannedRights(until_date=None, view_messages=True)
))

# Promote to admin
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
await client(EditAdminRequest(
    channel=group, user_id=user,
    admin_rights=ChatAdminRights(post_messages=True, edit_messages=True),
    rank="Admin"
))

# Set group description
from telethon.tl.functions.channels import EditAboutRequest
await client(EditAboutRequest(channel=group, about="Deskripsi baru"))
```

---

## 6. Create Group / Channel

```python
# Create Group
from telethon.tl.functions.messages import CreateChatRequest
result = await client(CreateChatRequest(
    users=["@user1", "@user2"],
    title="Nama Grup"
))

# Create Channel/Supergroup
from telethon.tl.functions.channels import CreateChannelRequest
result = await client(CreateChannelRequest(
    title="Nama Channel",
    about="Deskripsi",
    megagroup=True,   # True = supergroup, False = broadcast channel
    broadcast=False
))
channel = result.chats[0]

# Convert group to supergroup
from telethon.tl.functions.messages import MigrateChatRequest
await client(MigrateChatRequest(chat_id=chat_id))
```

---

## 7. Channel Management

```python
# Post to channel
await client.send_message("@channelname", "konten postingan")

# Schedule post
from datetime import datetime, timedelta
await client.send_message(
    "@channelname", "konten",
    schedule=datetime.now() + timedelta(hours=2)
)

# Set channel photo
await client(EditPhotoRequest(channel=ch, photo=await client.upload_file("logo.jpg")))

# Add members to channel
from telethon.tl.functions.channels import InviteToChannelRequest
await client(InviteToChannelRequest(channel=ch, users=["@user1", "@user2"]))

# Get channel stats (requires admin)
from telethon.tl.functions.stats import GetBroadcastStatsRequest
stats = await client(GetBroadcastStatsRequest(channel=ch))
```

---

## 8. Search

```python
# Search messages in chat
async for msg in client.iter_messages("@username", search="keyword", limit=50):
    print(msg.text, msg.date)

# Search public channels/groups
from telethon.tl.functions.contacts import SearchRequest
result = await client(SearchRequest(q="keyword", limit=20))
for chat in result.chats:
    print(chat.title, chat.username)

# Global message search
from telethon.tl.functions.messages import SearchGlobalRequest
from telethon.tl.types import InputMessagesFilterEmpty
result = await client(SearchGlobalRequest(
    q="keyword", filter=InputMessagesFilterEmpty(),
    min_date=None, max_date=None, offset_rate=0,
    offset_peer=await client.get_input_entity("me"),
    offset_id=0, limit=50
))
```

---

## 9. Member Scraping (Research & Outreach)

```python
# Scrape all members from group
async def scrape_members(group_link):
    group = await client.get_entity(group_link)
    members = []
    async for user in client.iter_participants(group):
        if not user.bot and user.username:
            members.append({
                "id": user.id,
                "username": f"@{user.username}",
                "name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
                "phone": getattr(user, 'phone', None)
            })
    return members

# Usage
members = await scrape_members("@targetgroup")
# Save for outreach
import csv
with open("prospects.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["id","username","name","phone"])
    writer.writeheader()
    writer.writerows(members)
```

---

## 10. Broadcast / Bulk DM (Outreach)

```bash
python3 scripts/broadcast.py --targets prospects.csv --message "template.txt" --delay 30
```

**Rate limits (avoid ban):**
- Max 50 DMs/hari ke stranger
- Delay 30-60 detik antar DM
- Stop kalau ada FloodWaitError

```python
import asyncio
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError

async def bulk_dm(targets, message, delay=30):
    sent = 0
    for username in targets:
        try:
            await client.send_message(username, message)
            sent += 1
            print(f"✅ DM sent to {username} ({sent}/{len(targets)})")
            await asyncio.sleep(delay)
        except FloodWaitError as e:
            print(f"⏳ FloodWait: sleeping {e.seconds}s")
            await asyncio.sleep(e.seconds + 5)
        except UserPrivacyRestrictedError:
            print(f"🔒 {username}: privacy restricted, skip")
        except Exception as e:
            print(f"❌ {username}: {e}")
```

---

## 11. Bot Cloning / Analysis

```python
# Observe bot behavior
async def clone_bot_analysis(bot_username):
    bot = await client.get_entity(bot_username)
    
    # Send /start and capture response
    await client.send_message(bot_username, "/start")
    await asyncio.sleep(2)
    
    msgs = await client.get_messages(bot_username, limit=10)
    analysis = []
    for msg in msgs:
        analysis.append({
            "text": msg.text,
            "has_buttons": bool(msg.reply_markup),
            "buttons": [[btn.text for btn in row] 
                       for row in (msg.reply_markup.rows if msg.reply_markup else [])],
            "media": type(msg.media).__name__ if msg.media else None
        })
    return analysis

# Test all commands
commands = ["/start", "/help", "/menu", "/subscribe", "/price"]
for cmd in commands:
    await client.send_message("@targetbot", cmd)
    await asyncio.sleep(1)
    resp = await client.get_messages("@targetbot", limit=1)
    print(f"{cmd} → {resp[0].text[:100]}")
```

---

## 12. Scheduled Messaging

```python
from datetime import datetime, timedelta

# Schedule single message
await client.send_message(
    "@username", "pesan terjadwal",
    schedule=datetime(2026, 3, 14, 9, 0)  # 9 AM besok
)

# List scheduled messages
from telethon.tl.functions.messages import GetScheduledHistoryRequest
scheduled = await client(GetScheduledHistoryRequest(peer="@username", hash=0))

# Send scheduled now
from telethon.tl.functions.messages import SendScheduledMessagesRequest
await client(SendScheduledMessagesRequest(peer="@username", id=[msg_id]))
```

---

## 13. Content Reposting (Autopilot)

```python
# Forward post from channel to channel
async def auto_repost(source_channel, target_channel, keywords=None):
    async for msg in client.iter_messages(source_channel, limit=10):
        if keywords and not any(k.lower() in (msg.text or "").lower() for k in keywords):
            continue
        await client.forward_messages(target_channel, msg)
        await asyncio.sleep(5)

# Monitor and auto-forward new posts
from telethon import events

@client.on(events.NewMessage(chats="@sourcechannel"))
async def repost_handler(event):
    await client.forward_messages("@targetchannel", event.message)
```

---

## 14. Notification / Keyword Monitor

```python
# Watch group for keywords, alert to Paijo
KEYWORDS = ["urgent", "bayar", "komplain", "error", "down"]

@client.on(events.NewMessage(chats=[-1001234567890]))
async def monitor(event):
    if any(k in event.text.lower() for k in KEYWORDS):
        await client.send_message("@codergaboets", 
            f"🚨 KEYWORD ALERT\nGroup: {event.chat.title}\n"
            f"From: {event.sender.first_name}\n"
            f"Message: {event.text[:200]}"
        )
```

---

## 15. CRM / Lead Tracking

```python
import json, os
from datetime import datetime

CRM_FILE = "/home/openclaw/.openclaw/workspace/.vilona/knowledge/telegram_crm.json"

def log_contact(username, action, note=""):
    crm = json.load(open(CRM_FILE)) if os.path.exists(CRM_FILE) else {}
    if username not in crm:
        crm[username] = {"contacts": [], "status": "new"}
    crm[username]["contacts"].append({
        "date": datetime.now().isoformat(),
        "action": action,
        "note": note
    })
    json.dump(crm, open(CRM_FILE, "w"), indent=2)

# Usage
log_contact("@prospect123", "DM_sent", "Pitch AI tools")
log_contact("@prospect123", "replied", "Interested in price")
log_contact("@prospect123", "converted", "Paid IDR 150K")
```

---

## 16. Auto-Responder

```python
RESPONSES = {
    "harga": "Harga paket kami mulai IDR 75K. Cek: https://lynk.id/jendralbot",
    "daftar": "Klik link ini untuk mendaftar: https://lynk.id/jendralbot",
    "info": "Info lengkap ada di: https://lynk.id/jendralbot",
}

@client.on(events.NewMessage(incoming=True))
async def auto_reply(event):
    text = event.text.lower()
    for keyword, response in RESPONSES.items():
        if keyword in text:
            await event.reply(response)
            break
```

---

## 17. File / Media Distribution

```python
# Send document to multiple targets
targets = ["@user1", "@user2", "@user3"]
for target in targets:
    await client.send_file(target, "ebook.pdf", 
                           caption="📚 Ebook gratis dari BerkahKarya!")
    await asyncio.sleep(10)

# Send to group
await client.send_file(-1001234567890, "product_catalog.pdf")
```

---

## 18. Management Alert System

```python
# scripts/alert.py
# Escalation: DM → Ring → DM Paijo

MANAGEMENT = {
    "veris": "@alwayscuanbos",   # Ads Master
    "paijo": "@codergaboets",    # CEO
    # "sony": "@sony_tg",        # Ops Manager
    # "nuno": "@nuno_tg",        # Trading Master
}
```

**Alert levels:**
```
Level 1 (30 min overdue): DM ke PIC
Level 2 (1 jam overdue):  DM + Ring 8s
Level 3 (2 jam overdue):  Ring PIC + DM ke Paijo
Level 4 (CRITICAL):       Ring semua management sekaligus
```

```bash
python3 scripts/alert.py --target @alwayscuanbos --level ring --message "Task X overdue!"
python3 scripts/alert.py --target all --level both --message "SISTEM DOWN"
```

---

## Login (One-Time)

**Problem**: Telegram detects OTP shared in Telegram chat → blocks.
**Solution**: base64 encode OTP before sending.

```bash
# Step 1: Start background listener
nohup python3 scripts/otp_login.py > /tmp/otp.log 2>&1 &
sleep 6 && grep "WAITING" /tmp/otp.log

# Step 2: User encodes OTP
echo -n "12345" | base64  # → MTIzNDU=

# Step 3: Inject decoded code
echo "MTIzNDU=" | base64 -d > /tmp/tg_code.txt
# Background process picks it up → LOGIN DONE
```

---

## Dependencies

```bash
pip install telethon edge-tts --break-system-packages
# ffmpeg already installed (for audio conversion)
```

## Gotchas

| Issue | Fix |
|-------|-----|
| PhoneCodeExpiredError | Use background + file injection |
| PhoneCodeInvalidError | OTP detected as shared → use base64 |
| DiscardCallRequest error | Use `InputPhoneCall(id=..., access_hash=...)` |
| FloodWaitError | Respect the wait time + reduce DM rate |
| UserPrivacyRestrictedError | Skip — user blocked DMs from strangers |
| Session expired | Re-run otp_login.py |
| Ban risk | Max 50 DMs/day to strangers, 30s+ delay |

## When to Use

- Automating Telegram messaging (DMs, group messages)
- Scraping Telegram group/channel members
- Running Telegram-based lead generation
- Automating Telegram account activities
- Building Telegram automation workflows

## When NOT to Use

- Task is about Telegram Bot API, not userbot
- You need to build a Telegram bot (use bot framework)
- Task requires user interaction (use bot commands)
- You don't have Telegram account for userbot
- Task is about Telegram channel management (use channel tools)
- You need to handle payments (use payment tools)

## Red Flags

- Sending too many DMs (risk of ban)
- Not respecting rate limits (FloodWaitError)
- Using for spam or unsolicited messages
- Not handling privacy restrictions properly
- Ignoring Telegram Terms of Service

## Verification

- [ ] Account is not banned or restricted
- [ ] Rate limits are respected (30s+ between DMs)
- [ ] Messages are personalized (not generic spam)
- [ ] Privacy settings are checked before sending
- [ ] Error handling is in place for common errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain