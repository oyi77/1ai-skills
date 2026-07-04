# Agent-Reach → 1ai-Ecosystem Integration

**Date:** 2026-07-04  
**Source:** https://github.com/Panniantong/Agent-Reach  
**Status:** TIER 1 INTEGRATION (in progress)

---

## Integration Scope

Port Agent-Reach's **multi-platform channel abstraction** (19 channels across TikTok, Instagram, Reddit, WeChat, Shopee, YouTube, etc.) into 1ai-ecosystem as a unified **OSINT + e-commerce data collector**.

### Channels to Integrate (PRIORITY ORDER)

| Channel | Platform | Purpose | Backend | Tier | Status |
|---------|----------|---------|---------|------|--------|
| **TikTok Shop** | TikTok Shop (CN/SEA) | Product data, reviews, seller metrics | TikTok API / web scraping | 2 | PENDING |
| **Shopee** | Shopee (SEA e-comm) | Products, reviews, seller info (ID/MY/PH/SG/TH/VN) | shopee-cli / Selenium | 2 | PENDING |
| **WeChat** | WeChat (messaging + payment) | Articles, group data, payment signals | wechat-jump / web | 2 | PENDING |
| **Xiaohongshu** | Xiaohongshu (Chinese social) | Trending posts, influencer profiles, product mentions | API / web scraping | 2 | PENDING |
| **Xueqiu** | Xueqiu (Chinese stocks/crypto) | Stock data, fund holdings, trading signals | API / web | 2 | PENDING |
| **YouTube** | YouTube | Video metadata, comments, transcripts | youtube-dl / pytube | 1 | PENDING |
| **TikTok** | TikTok (global) | Video metadata, trending sounds, engagement | TikTok API / web | 2 | PENDING |
| **Instagram** | Instagram (social) | Posts, Stories, Reels metadata | instagrapi / web | 2 | PENDING |
| **Reddit** | Reddit (community) | Posts, comments, thread data | PRAW API | 1 | PENDING |
| **Twitter** | Twitter/X | Tweets, engagement, trends | Tweepy / web scraping | 2 | PENDING |
| **V2EX** | V2EX (Chinese dev forum) | Tech discussions, startup signals | web scraping | 0 | PENDING |
| **Xiaoyuzhou** | Xiaoyuzhou (podcast platform) | Podcast data, guest profiles | web scraping | 0 | PENDING |
| **Bilibili** | Bilibili (Chinese video) | Video metadata, channel data, comments | BiliClient / web | 1 | PENDING |
| **LinkedIn** | LinkedIn (professional) | Profile data, job postings, engagement | linkedin-api / web | 2 | PENDING |
| **GitHub** | GitHub (code + community) | Repo data, stars, issues, discussions | GitHub API | 1 | PENDING |
| **RSS** | RSS/Atom feeds | Feed aggregation, article parsing | feedparser | 0 | PENDING |
| **Web** | Generic HTTP(S) | Page parsing, metadata extraction | requests / BeautifulSoup | 0 | PENDING |
| **Facebook** | Facebook (social) | Page posts, engagement | facebook-sdk / web | 2 | PENDING |
| **Exa Search** | Exa Search API | Web search + summarization | Exa API | 1 | PENDING |

**Tier:** 0 = zero-config, 1 = free API key, 2 = needs auth/cookies/setup

---

## Core Abstraction: `Channel` Base Class

**Location:** `/tmp/Agent-Reach/agent_reach/channels/base.py`

**Key Pattern:**
```python
class Channel(ABC):
    name: str                          # e.g., "shopee"
    description: str                   # e.g., "Shopee products (Indonesia/SEA)"
    backends: List[str]                # ordered: [preferred, fallback1, fallback2]
    tier: int                          # 0=zero-config, 1=free key, 2=auth required
    active_backend: Optional[str]      # set by check(), None = unavailable

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Does this channel handle this URL?"""
        ...

    def check(self, config=None) -> Tuple[str, str]:
        """Probe backends, set active_backend, return (status, message)."""
        ...

    def extract(self, url: str) -> list[dict]:
        """Extract structured data from URL using active_backend."""
        ...
```

**Integration Path:**
```
1ai-skills/automation/multi-platform/
├── __init__.py
├── base.py                          ← copy from Agent-Reach
├── channels/
│   ├── __init__.py
│   ├── tiktok_shop.py              ← copy + adapt
│   ├── shopee.py                    ← copy + adapt
│   ├── wechat.py                    ← copy + adapt
│   ├── xiaohongshu.py               ← copy + adapt
│   ├── xueqiu.py                    ← copy + adapt
│   ├── youtube.py                   ← copy + adapt
│   └── ... (17 more)
├── config.py                        ← backend routing + auth config
└── INTEGRATION.md                   ← THIS FILE
```

---

## Backend Routing Strategy

**Problem:** Each channel has multiple backends (primary + fallbacks). User may want to override.

**Solution:** `ordered_backends(config)` respects user override:

```python
# Default order (from Channel.backends)
backends = ["shopee-cli", "web scraping"]

# User override via config[f"{channel}_backend"] or env CHANNEL_BACKEND
user_override = "web scraping"

# ordered_backends() moves override to front
result = ["web scraping", "shopee-cli"]

# check() tries each in order, sets active_backend to first working one
active_backend = "web scraping"  # shopee-cli failed, web scraping works
```

**Config Example:**
```yaml
# ~/.1ai/channels/config.yaml
shopee_backend: "web scraping"      # force web scraping for Shopee
tiktok_backend: "api"               # prefer TikTok API
reddit_backend: "praw"              # use PRAW for Reddit
```

---

## Porting Checklist per Channel

For each channel:

### [CHANNEL_NAME]

- [ ] **Read:** Original channel .py file from `/tmp/Agent-Reach/agent_reach/channels/`
- [ ] **Extract:** Core logic (can_handle, check, extract)
- [ ] **Adapt:** Replace Agent-Reach paths with 1ai-ecosystem paths
  - `agent_reach.utils.process` → `1ai_skills.utils.process`
  - Hardcoded API keys → read from `~/.1ai/config/channels.env`
  - Agent-Reach logging → 1ai-ecosystem logging
- [ ] **Implement:** `can_handle()`, `check()`, `extract()` methods
- [ ] **Test:** Real data extraction
  - Example URL for platform (e.g., real Shopee product, YouTube video)
  - Verify output structure
  - Check error handling (invalid URL, auth failed, etc.)
- [ ] **Document:** Create CHANNEL.md with:
  - Purpose statement
  - Backends (ordered)
  - Auth requirements (tier, config keys)
  - Input contract (URL format, config keys)
  - Output contract (JSON schema)
  - Example usage + output
  - Known limitations (rate limits, geofencing, etc.)
- [ ] **Verify:** Run 1ai-ecosystem's VERIFICATION.md checklist
- [ ] **Commit:** PR to 1ai-skills with channel + tests + docs

---

## Real-World Validation Required

**Before marking channel "DONE":**

Each channel MUST extract real data:

1. **Shopee:** Extract real product from shopee.co.id (ID region)
   - Verify product name, price, seller, review count
   - Compare with browser view (screenshot side-by-side)

2. **WeChat:** Extract real article or group data
   - Verify content is parseable
   - Check auth flow works

3. **TikTok Shop:** Extract real product from TikTok Shop
   - Verify product metadata (title, price, sales, likes)
   - Handle pagination (if applicable)

4. **YouTube:** Extract metadata from real video URL
   - Title, duration, channel, upload date
   - Verify transcript download (if available)

5. **Reddit:** Fetch real thread data
   - Post title, score, comments
   - Verify PRAW auth flow

---

## Proof of Completion

After porting each channel:

**MUST provide:**
- Screenshot of real data extraction
- JSON output from `extract(url)`
- Comparison with Agent-Reach original (proof porting preserved behavior)

**Example:**
```
File: 1ai-skills/automation/multi-platform/channels/TEST_PROOF.md

## Shopee Channel Test

### Input
URL: https://shopee.co.id/product/123456789/

### Output
{
  "platform": "shopee",
  "product_id": "123456789",
  "title": "iPhone 15 Pro Max",
  "price": 18999000,  // IDR
  "currency": "IDR",
  "seller": "Apple Indonesia Official",
  "seller_rating": 4.9,
  "reviews_count": 15234,
  "in_stock": true,
  "likes": 8932,
  "thumbnail": "https://...",
  "url": "https://shopee.co.id/product/123456789/"
}

### Validation
✅ Matches browser view (screenshot attached)
✅ All required fields present
✅ Data freshness: <5 min
✅ Extraction time: 2.3s
```

---

## Data Schema (Normalized Across Platforms)

All channels normalize output to this schema:

```json
{
  "platform": "shopee|tiktok|youtube|...",
  "url": "https://...",
  "title": "string",
  "description": "string (optional)",
  "author": "string (username or channel)",
  "author_id": "string (internal platform ID)",
  "created_at": "ISO 8601 timestamp",
  "updated_at": "ISO 8601 timestamp (optional)",
  "engagement": {
    "likes": number,
    "comments": number,
    "shares": number,
    "views": number (optional)
  },
  "data": {
    "platform-specific fields": "..."
  },
  "source_backend": "the backend that extracted this (e.g., 'shopee-cli', 'api', 'web')",
  "extraction_time_ms": number,
  "error": "string (null if success)"
}
```

---

## Configuration & Auth

**Location:** `~/.1ai/config/channels.env`

**Template:**
```bash
# TikTok
TIKTOK_API_KEY=...
TIKTOK_API_SECRET=...

# Shopee
SHOPEE_API_KEY=...
SHOPEE_SHOP_ID=...

# WeChat
WECHAT_APP_ID=...
WECHAT_APP_SECRET=...

# Reddit
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...

# YouTube
YOUTUBE_API_KEY=...

# GitHub
GITHUB_TOKEN=...

# LinkedIn
LINKEDIN_EMAIL=...
LINKEDIN_PASSWORD=...
```

**Auth Tier Mapping:**
- **Tier 0:** No config needed (V2EX, RSS, generic web)
- **Tier 1:** Free API key (YouTube, Reddit, GitHub)
- **Tier 2:** Paid API or complex auth (TikTok, Shopee, WeChat, LinkedIn)

---

## Known Risks

- **Rate Limiting:** Each platform has different rate limits
  - Mitigation: Implement exponential backoff + queue system
- **Auth Expiry:** Tokens expire or cookies rot
  - Mitigation: Detect 401/403 errors, trigger re-auth workflow
- **API Breaking Changes:** Platforms update APIs frequently
  - Mitigation: Monitor releases, maintain fallback backends
- **Geofencing:** Some platforms restrict by region
  - Mitigation: Document region support per channel
- **Bot Detection:** Web scraping triggers captchas or blocks
  - Mitigation: Use proxy rotation + browser fingerprinting (Selenium/Puppeteer)

---

## Timeline

| Phase | Tasks | ETA |
|-------|-------|-----|
| **Discovery** (current) | Map channels, extract base.py | Jul 4 |
| **TIER 1 Adapt** | Port 5 core channels (Shopee, TikTok Shop, WeChat, Xiaohongshu, Xueqiu) | Jul 5-6 |
| **TIER 1 Test** | Real data extraction for each channel | Jul 7 |
| **TIER 2 Adapt** | Port 8 channels (YouTube, TikTok, Instagram, Reddit, Twitter, etc.) | Jul 8-9 |
| **TIER 2 Test** | Real data extraction for each channel | Jul 10 |
| **TIER 3 Adapt** | Port 6 low-complexity channels (GitHub, RSS, Web, V2EX, etc.) | Jul 11 |
| **Integration** | Wire into 1ai-ecosystem routing + CLI | Jul 12 |
| **Verification** | Full end-to-end test, multi-platform extraction | Jul 13 |
| **Documentation** | Create INTEGRATION.md, CHANNEL.md files, examples | Jul 14 |
| **SHIPPED** | Merge to 1ai-skills main | Jul 15 |

---

## Success Criteria

✅ All 19 channels ported to 1ai-skills/automation/multi-platform/  
✅ Each channel has CHANNEL.md + tests + real-world proof  
✅ Normalized data schema implemented  
✅ Backend routing + config system working  
✅ Multi-platform extraction workflow runs end-to-end  
✅ Error handling + auth recovery implemented  
✅ INTEGRATION.md updated with lessons learned  
✅ Merged to 1ai-skills main branch  

---

**Owner:** Integration Team  
**Last Updated:** 2026-07-04 20:42 UTC
