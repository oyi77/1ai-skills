---
name: wa-business-automation
description: WhatsApp Business automation for customer service, lead follow-up, appointment booking, and broadcast campaigns. High-value for Indonesian SMBs — Indonesia has 175M+ WhatsApp users. Use when: automating WhatsApp replies, bulk messaging, chatbot flows, appointment reminders, payment follow-ups, or post-purchase sequences. Revenue potential: $500-5000/client/month.
---

# WhatsApp Business Automation

## Overview

Automate WhatsApp for business use cases: chatbots, lead follow-up, appointment reminders, broadcast campaigns, and CRM sync. 

**Market**: Indonesia has 175M+ WhatsApp users — it's the #1 business communication channel.  
**Revenue**: $500–$5,000/client/month for setup + monthly retainer.  
**ROI for clients**: 3–10x faster response time, 40–60% more conversions.

---

## When to Use

- Business wants 24/7 WhatsApp autoresponder
- Appointment booking / reminder automation
- Lead follow-up sequences (after form fill or ads)
- Broadcast to existing customers (promos, announcements)
- Payment reminders / invoice follow-up
- Post-purchase support automation
- WhatsApp as CRM input channel

---

## When NOT to Use

- Personal WhatsApp accounts (ToS risk)
- Mass spam campaigns (get banned fast)
- Highly emotional / sensitive conversations

---

## Top Platforms

### 1. Wacli (Local — Already Installed)
```bash
# Check skill
cat skills/wacli/SKILL.md

# Send message
wacli send --to "6281234567890@s.whatsapp.net" --text "Halo! Ada yang bisa kami bantu?"

# Check new messages
wacli messages --limit 20
```

### 2. Fonnte API (Indonesian-friendly, cheap)
```
Base URL: https://api.fonnte.com
Auth: token in header
Price: IDR 50/message
```

### 3. WhatsApp Business API (Official)
```
Provider: Meta Business
Requires: Verified business account
Price: $0.015–0.085/conversation
Best for: Scale (10K+ messages/month)
```

### 4. WABLAS / WAPPIN (Indonesia)
```
Price: IDR 100K–500K/month
Easy setup, no verification needed
Good for small business (<1000 msgs/day)
```

---

## Quick Start — Fonnte API

```python
import requests

FONNTE_TOKEN = "your-token-here"

def send_wa_message(to: str, message: str) -> dict:
    """Send single WA message via Fonnte"""
    url = "https://api.fonnte.com/send"
    headers = {"Authorization": FONNTE_TOKEN}
    payload = {
        "target": to,  # format: 6281234567890
        "message": message,
        "countryCode": "62"
    }
    r = requests.post(url, json=payload, headers=headers)
    return r.json()

def broadcast_message(contacts: list, message: str) -> list:
    """Broadcast to multiple contacts with delay"""
    import time
    results = []
    for contact in contacts:
        result = send_wa_message(contact, message)
        results.append({"contact": contact, "status": result})
        time.sleep(3)  # anti-spam delay
    return results
```

---

## Automation Flows

### Flow 1: Lead Follow-Up (After FB/IG Ads)
```
Trigger: New lead from form/ads
→ Immediate: "Halo [name]! Terima kasih sudah tertarik dengan [product]. Tim kami akan hubungi dalam 1 jam."
→ +1 hour: "Hi [name]! Apakah Anda punya pertanyaan tentang [product]? Kami siap bantu!"
→ +24 hours (no reply): "Hai [name], kami masih di sini kalau butuh info lebih lanjut 😊"
→ +3 days (no reply): Final follow-up with offer/promo
```

### Flow 2: Appointment Reminder
```
-24h: "Reminder: Appointment Anda besok [date] jam [time]. Reply KONFIRM untuk konfirmasi."
-2h: "2 jam lagi! Sampai jumpa di [location]."
Missed: "Kami missyou hari ini! Mau reschedule? Reply YA"
```

### Flow 3: Post-Purchase Sequence
```
Day 0: Order confirmation + tracking
Day 3: "Pesanan sudah sampai? Bagaimana kondisinya?"  
Day 7: "Review produk kami yuk! [link]"
Day 14: "Produk terkait yang mungkin Anda suka: [link]"
Day 30: "Member loyalty offer: Diskon 15% untuk pembelian berikutnya!"
```

---

## Chatbot Builder (No-Code)

### Using Wacli + Python Autoresponder
```python
#!/usr/bin/env python3
# scripts/wa_chatbot.py

import subprocess
import json
import time

KEYWORD_RESPONSES = {
    "harga": "Harga produk kami: Paket Basic IDR 150K, Premium IDR 299K. Info lengkap: https://linktr.ee/berkahkarya",
    "order": "Untuk order, silahkan klik link ini: https://toko.berkahkarya.com",
    "lokasi": "Kami berlokasi di Jakarta Selatan. Google Maps: https://maps.app.goo.gl/xxx",
    "kontak": "WA: 081234567890 | Email: info@berkahkarya.com | Jam kerja: 09:00-17:00 WIB",
}

def get_recent_messages() -> list:
    """Get unread messages via wacli"""
    result = subprocess.run(
        ["wacli", "messages", "--unread", "--format", "json"],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except:
        return []

def auto_respond(message: dict) -> bool:
    """Check for keywords and respond"""
    text = message.get("text", "").lower()
    sender = message.get("from", "")
    
    for keyword, response in KEYWORD_RESPONSES.items():
        if keyword in text:
            subprocess.run([
                "wacli", "send",
                "--to", sender,
                "--text", response
            ])
            return True
    return False

def main():
    print("WA Chatbot running... (Ctrl+C to stop)")
    while True:
        messages = get_recent_messages()
        for msg in messages:
            auto_respond(msg)
        time.sleep(30)  # check every 30 seconds

if __name__ == "__main__":
    main()
```

---

## Client Pricing (Agency Model)

| Package | Price/Month | Deliverables |
|---------|-------------|--------------|
| Starter | IDR 500K | Basic autoresponder, 3 keyword flows |
| Growth | IDR 1.5M | 10 flows, broadcast, CRM integration |
| Scale | IDR 3.5M | Full automation, AI responses, analytics |
| Enterprise | IDR 7.5M+ | Custom, WhatsApp API, dedicated support |

**Setup fee:** 1x monthly rate

---

## Integration with BerkahKarya Stack

```
PostBridge → Schedule content
WA Automation → Follow up leads from content
LYNK → Track conversions
CRM → Log all interactions
```

---

## Scripts

- `scripts/wa_chatbot.py` — Keyword autoresponder
- `scripts/wa_broadcast.py` — Bulk message sender with delay
- `scripts/wa_followup.py` — Drip sequence scheduler
- `scripts/wa_appointment.py` — Booking + reminder flow

---

## Notes

- Always use business account, never personal
- Max 50-100 new contacts/day to avoid ban
- Anti-spam: 3-5 second delay between messages
- Use templates for broadcast (meta compliance)
- Log all sent messages for audit trail
