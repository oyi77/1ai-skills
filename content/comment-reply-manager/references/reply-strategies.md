# Reply Strategies — Comment-to-Sale Conversion

## The Core Problem
196 clicks → 0 sales. People click but don't buy. Why? **No engagement funnel.**

The fix: every comment is a micro-sales opportunity. Engage → Build interest → Drive to LYNK.

---

## Conversion Funnel Architecture

```
Comment → Sentiment Detection → Contextual Reply → DM Trigger → LYNK Link → Sale
```

### Tier 1: High-Intent (DM Immediately)
| Signal | Action | Conversion Probability |
|--------|--------|----------------------|
| "harganya berapa?" | Price reply + Auto-DM | 40-60% |
| "mau beli dong" | DM public reply + Auto-DM | 50-70% |
| "cara order gimana?" | Direct answer + DM | 45-65% |
| "mau coba" | DM trigger | 35-55% |

### Tier 2: Medium-Intent (Reply + Funnel)
| Signal | Action | Conversion Probability |
|--------|--------|----------------------|
| Product question | Benefit-focused answer | 15-25% |
| "bisa buat apa?" | Use-case explanation | 10-20% |
| Positive comment | Engagement + CTA | 5-15% |

### Tier 3: Low-Intent (Maintain Visibility)
| Signal | Action | Conversion Probability |
|--------|--------|----------------------|
| Generic comment | Friendly reply | 2-5% |
| Negative | De-escalate professionally | 0-2% |
| Spam | Skip entirely | 0% |

---

## Reply Templates by Platform

### TikTok (Max 150 chars recommended)
Keep short, emoji-heavy, mobile-first.

**Price question:**
> "Cuma 75rb kak! Lagi promo 🔥 Link di bio ya"

**Interest:**
> "DM aku kak buat detail + promo spesial! 😊"

**Question:**
> "Bisa [benefit] kak! Cek link di bio, worth it banget 🎁"

**Positive:**
> "Makasih kak! 🔥 Udah coba? Link di bio ya"

### Instagram (Max 300 chars, more professional OK)
Slightly longer, can include more detail.

**Price question:**
> "Harganya IDR 75.000 kak 😊 Worth it banget buat tools AI sekelas ini! Cara belinya gampang, tinggal klik link di bio ya. Lagi ada promo hari ini! 🎁"

**Interest:**
> "Wah mantap kak udah tertarik! DM aku ya buat info lengkap + penjelasan fitur-fiturnya 🔥 Ada promo spesial juga buat yang cepet!"

---

## DM Funnel Script (Step-by-Step)

### Step 1: Detect High-Intent Comment
Triggers:
- Contains price keywords (harga, berapa, bayar)
- Contains purchase keywords (mau beli, order, pesan, mau dong)
- Contains interest keywords (tertarik, pengen, minat)

### Step 2: Public Reply (within 5-15 mins)
**FAST response is critical** — comment threads go cold in 30-60 mins.

Template:
> "DM aku kak buat detail lengkapnya! 🔥"

This:
1. Shows everyone that you're responsive
2. Moves conversation to DM (higher conversion)
3. Creates FOMO ("promo spesial")

### Step 3: Auto-DM (within 1 min of public reply)
Beat the user to their DMs. They just saw your reply, they're warm.

Template:
```
Hai kak! Makasih udah tertarik sama [Product Name] 😊

Ini linknya: [LYNK URL]

[Product] bisa [benefit].

Harganya [price] aja — lagi ada promo spesial hari ini! 🎁

Kalau ada pertanyaan, langsung tanya aja ya kak. Aku siap bantu! 🔥
```

### Step 4: Follow-Up (24h if no response)
If they didn't buy after DM:
> "Kak, masih ada promo [Product] ya! Cuma [price]. Jangan sampai kehabisan 🔥 [LYNK URL]"

---

## Timing Strategy

| Time | Action | Why |
|------|--------|-----|
| Within 5 min | Reply to comment | Algorithmic boost + user still active |
| Within 1 min of public reply | Send DM | User just saw your reply, maximum warmth |
| 24h after DM | Follow-up | Reminder without being annoying |

---

## Product-Comment Matching Logic

Match comment keywords to most relevant product for personalized response:

| User Says | Best Product | Key Benefit to Highlight |
|-----------|-------------|--------------------------|
| "kerja", "loker", "interview" | JobMagnet AI | Get hired faster |
| "iklan", "ads", "marketing" | AI Creative Ad Engine | Converting ads with AI |
| "menu", "restoran", "kuliner" | Food Menu AI Studio | Professional menus |
| "shopee", "tokopedia", "olshop" | Studio Marketplace Pro | Boost marketplace sales |
| "tiktok", "affiliate", "cuan" | Kelas Affiliate TikTok | Income from TikTok |
| "cashback", "hemat", "gratis" | Belanja Duit Balik | Free cashback |
| Default (generic) | AI Creative Tools | Complete AI creator toolkit |

---

## Anti-Patterns to Avoid

❌ **Slow responses** (>30 min) — Comment thread is cold, engagement drops
❌ **Generic copy-paste** — Looks like a bot, loses trust
❌ **Repeated DMs** — One DM per 24h max, avoid spam reports
❌ **Hard selling** — Soft CTA ("cek link di bio") outperforms "BUY NOW"
❌ **Replying to spam** — Ignore/hide, don't engage
❌ **Emoji overload** — 1-2 emojis max per message, looks natural

✅ **DO: Fast responses** — Under 10 minutes is gold
✅ **DO: Personalized tone** — Use "kak" naturally, match their energy
✅ **DO: Answer then CTA** — Answer the question FIRST, then push to bio
✅ **DO: Scarcity/urgency** — "Lagi promo" / "hari ini aja" works
✅ **DO: DM high-intent** — Price asks = almost-buyers, never miss these

---

## Performance Metrics to Track

| Metric | Target | Alert If |
|--------|--------|----------|
| Comment reply rate | >80% | <60% |
| Avg reply time | <15 min | >30 min |
| DM trigger rate | >30% of replies | <15% |
| DM-to-click rate | >50% | <30% |
| Click-to-sale rate | >5% | <2% |

---

## Revenue Math

```
196 clicks → 0 sales = 0% CVR (current state)
Target: 5% CVR = 9.8 sales ≈ 10 sales
At IDR 75,000 avg = IDR 750,000 per 196 clicks

Scale to 1,000 clicks/day:
= 50 sales × IDR 75,000
= IDR 3,750,000/day
= IDR 112,500,000/month
```

The engagement funnel multiplies the existing click traffic. 
Don't get more traffic — convert what you have.

---

## Quick Start Checklist

- [ ] Run `python3 test_comment_manager.py` — all tests pass
- [ ] Configure PostBridge API key in environment
- [ ] Test PostBridge connection (posts + post-results endpoints)  
- [ ] Run comment monitor: identify posts with comments
- [ ] Process comments in dry-run mode first
- [ ] Review manual queue (dm_queue.jsonl)
- [ ] Execute pending DMs manually via TikTok/IG apps
- [ ] Set up cron: `*/30 * * * * cd /path && python3 run_manager.py`
- [ ] Monitor reply log: `tail -f logs/replies.jsonl`
- [ ] Track DM conversions daily
