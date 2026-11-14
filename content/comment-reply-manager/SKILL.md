---
name: comment-reply-manager
description: Use when monitoring TikTok/Instagram comments — classify intent, auto-reply to FAQs, and DM high-intent commenters with LYNK affiliate links. Converts comment engagement into tracked affiliate sales.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- comment
- reply
- affiliate
- lynk
- tiktok
- instagram
- engagement
- funnel
version: 1.0.0
category: content
---

# Comment Reply Manager

Monitor TikTok/Instagram comments, classify intent, auto-reply to FAQs, and DM high-intent commenters with LYNK affiliate links.

**Purpose:** close the gap between comment engagement and affiliate sales. (Prior state: 196 clicks → 0 sales — engagement existed, the reply/DM funnel did not.)

## When to Use

**Trigger phrases:**
- "monitor comments" · "reply to comments" · "comment funnel"
- "auto-DM commenters" · "convert comments to sales"
- "classify comment intent" · "FAQ auto-reply"

**Use cases:**
- TikTok/Instagram posts with LYNK affiliate links in bio
- Product showcase content where buyers ask "where to buy"
- Comment volume too high for manual replies

## When NOT to Use

- Real-time streaming — run on a schedule (every 5–15 min), not live
- Legal / medical / financial advice — never auto-reply to regulated questions
- Accounts <1k followers — reply manually; DM automation risks flags at low volume
- Platform policy violation — always check current TikTok/Meta automation terms before running

## Scope Honesty

The **classification logic, reply templates, funnel logging, and rate-limit caps** below are the substance of this skill and hold regardless of backend. The **network calls are illustrative adapters**, not verified contracts:

- The Instagram Graph API call (`GET /{post_id}/comments`, fields `id,text,from,timestamp`) is a well-documented real endpoint.
- The TikTok Business API paths (`/open_api/v1.3/business/comment/...`) follow the portal's known URL scheme but **exact sub-paths and payload shapes were not confirmed here** — validate against https://business-api.tiktok.com/portal/docs before running, and expect auth scopes + app review.
- Treat every endpoint as needing a live smoke-test with your own tokens before trusting it.

## Intent Classification

Every comment is bucketed into exactly one class. This drives the action.

| Class | Signal | Action |
|---|---|---|
| `faq_price` | "how much", "price", "berapa", "$" | Auto-reply with price + LYNK link |
| `faq_where` | "where to buy", "link", "dimana", "mana" | Auto-reply "link in bio → [product]" |
| `faq_size` | "size", "ukuran", "fit", "M/L" | Auto-reply size guide link |
| `faq_ship` | "ship", "cod", "kirim", "delivery" | Auto-reply shipping policy |
| `high_intent_dm` | "buy", "want", "checkout", "pm", "dm me" | DM the LYNK link directly |
| `objection` | "scam", "fake", "trust", "review" | Reply with social proof + DM offer |
| `spam` | Bot patterns, repeated, off-topic | Ignore (no reply, no DM) |
| `positive` | Emoji, "love", compliments | Like / heart; no reply needed |
| `question_other` | Genuine question, not in FAQ | Queue for human reply |

Confidence threshold: **0.75**. Below that → `question_other` (human).

## Workflow

### 1. Fetch new comments

```python
import requests, os, time

def fetch_comments(post_id: str, since_ts: int) -> list[dict]:
    # TikTok Business API — GET /business/comment/list/
    # UNVERIFIED PATH — confirm against the Business API docs before use
    r = requests.get(
        "https://business-api.tiktok.com/open_api/v1.3/business/comment/list/",
        headers={"Authorization": f"Bearer {os.environ['TIKTOK_ACCESS_TOKEN']}"},
        params={"post_id": post_id, "start_time": since_ts, "page_size": 100},
    )
    r.raise_for_status()
    return r.json()["data"]["comments"]

# Instagram: GET /{post_id}/comments via Graph API
def fetch_ig_comments(post_id: str) -> list[dict]:
    r = requests.get(
        f"https://graph.facebook.com/v18.0/{post_id}/comments",
        params={"access_token": os.environ["IG_ACCESS_TOKEN"],
                "fields": "id,text,from,timestamp"},
    )
    r.raise_for_status()
    return r.json()["data"]
```

### 2. Classify each comment

```python
FAQ = [
    ("faq_price", ["berapa", "price", "how much", "$", "harga"]),
    ("faq_where", ["link", "where to buy", "dimana", "mana beli", "in bio"]),
    ("faq_size",  ["size", "ukuran", "fit", "xl", "m/l"]),
    ("faq_ship",  ["cod", "ship", "kirim", "delivery", "ongkir"]),
]

def classify(text: str, score: float = 1.0) -> tuple[str, float]:
    t = text.lower()
    # High-intent DM signals take precedence
    if any(k in t for k in ["want", "buy", "checkout", "pm", "dm me", "beli"]):
        return "high_intent_dm", 0.95
    if any(k in t for k in ["scam", "fake", "trust", "review"]):
        return "objection", 0.85
    for cls, keys in FAQ:
        if any(k in t for k in keys):
            return cls, 0.9
    # ...emoji-only, generic praise → positive
    if any(c in t for c in ["❤", "🔥", "😍", "love"]):
        return "positive", 0.8
    return "question_other", 0.4
```

For higher accuracy than keyword rules, swap `classify` for an LLM call (few-shot prompt with the table above as examples). Keep the keyword version as fallback when the API is down.

### 3. Auto-reply per class

```python
REPLIES = {
    "faq_price": "Harga {price} — bisa langsung cek di bio ya! 🛒",
    "faq_where": "Link lengkapnya ada di bio (klik @handle). Stok terbatas! ✨",
    "faq_size":  "Size chart lengkap ada di link bio ya. Kalau ragu, ambil 1 size lebih besar. 📏",
    "faq_ship":  "Kirim dari {city}, COD tersedia. Estimasi {days} hari. 📦",
    "objection": "100% original — cek review di bio. Kalau ada ragu, DM aku ya! 🤝",
}

def reply(comment_id: str, cls: str) -> str | None:
    text = REPLIES.get(cls)
    if not text:
        return None
    r = requests.post(
        "https://business-api.tiktok.com/open_api/v1.3/business/comment/reply/create/",
        headers={"Authorization": f"Bearer {os.environ['TIKTOK_ACCESS_TOKEN']}"},
        json={"comment_id": comment_id, "content": text},
    )
    r.raise_for_status()
    return r.json()["data"]["reply_id"]
```

### 4. DM high-intent commenters with the LYNK link

```python
def dm_lyk(user_id: str, product_slug: str) -> str:
    link = f"https://lynk.id/{os.environ['LYNK_HANDLE']}/{product_slug}"
    r = requests.post(
        f"https://business-api.tiktok.com/open_api/v1.3/business/direct_message/send/",
        headers={"Authorization": f"Bearer {os.environ['TIKTOK_ACCESS_TOKEN']}"},
        json={
            "user_id": user_id,
            "content": f"Hai! Ini link produknya ya: {link}\nKalau ada pertanyaan, reply di sini. 🙌",
        },
    )
    r.raise_for_status()
    return r.json()["data"]["message_id"]
```

Rate limit: max **20 DMs/hour** per account. Exceeding it risks a platform flag — see §Rate Limits.

### 5. Track the funnel

```python
import csv, datetime

def log_event(cls: str, comment_id: str, action: str, extra: str = ""):
    with open("funnel.csv", "a", newline="") as f:
        csv.writer(f).writerow([
            datetime.datetime.utcnow().isoformat(),
            cls, comment_id, action, extra,   # action: reply | dm | human_queue | skip
        ])
```

The metric that matters: **DMs sent → link clicks → sales.** If clicks stay flat while DMs rise, the DM copy is the problem, not the volume.

## Rate Limits (avoid flags)

| Action | Cap | Window |
|---|---|---|
| Public replies | 30 | hour |
| DMs | 20 | hour |
| Comment fetches | 1 | 5 min per post |

Jitter every request by 1–3 s. Never loop faster than the caps. A single flagged account costs more than a day of slower replies.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "More DMs = more sales" | Over DM'ing triggers spam flags and kills the account. Cap it. |
| "Reply to everything" | Spam comments replied-to train the algorithm wrong. Skip `spam` and `positive`. |
| "Keyword rules are enough" | Keywords miss context ("not for me but how much?"). Use an LLM classifier when volume justifies it. |
| "I'll check conversion later" | Without the funnel log you can't tell if the problem is reply, DM, or product. Log every event. |

## Verification

- [ ] Classifier accuracy >90% on a labeled sample of 100 real comments
- [ ] Auto-reply never fires on `question_other` or `spam`
- [ ] DM rate ≤20/hour, replies ≤30/hour, with jitter
- [ ] Every reply and DM appended to `funnel.csv`
- [ ] LYNK links use the correct `LYNK_HANDLE` / product slug
- [ ] No regulated questions (legal/medical/financial) auto-answered
- [ ] Funnel metrics reviewed weekly: DMs → clicks → sales
