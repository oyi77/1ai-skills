# PostBridge Manager

Full PostBridge API wrapper — post scheduling, analytics, account management,
health monitoring, and smart post creation with automatic error prevention.

---

## 📦 Dependencies & Tools Required

### No External Packages Needed
All scripts use Python stdlib only (`urllib`, `json`, `os`, `sys`).

```bash
# No pip install required!
# Only: Python 3.8+
```

### Config

```python
API_BASE = 'https://api.post-bridge.com/v1'
API_KEY  = 'REDACTED_POSTBRIDGE_KEY'    # BerkahKarya API key
```

Override with env var:
```bash
export PB_API_KEY="pb_live_your_key_here"
```

### PostBridge Account

- **Account:** grahainsanmandiri@gmail.com
- **Plan:** Pro ($49/month) — unlimited accounts
- **Login:** Magic link via email (no password)
- **Dashboard:** https://www.post-bridge.com/dashboard

---

## 🚀 Scripts

### `postbridge_api.py` — CLI Wrapper

```bash
# List all accounts
python3 scripts/postbridge_api.py accounts

# TikTok accounts only
python3 scripts/postbridge_api.py accounts tiktok

# Analytics summary
python3 scripts/postbridge_api.py analytics

# Sync analytics (trigger refresh from platforms)
python3 scripts/postbridge_api.py analytics sync

# List scheduled posts
python3 scripts/postbridge_api.py posts scheduled

# All posts
python3 scripts/postbridge_api.py posts

# Recent post results (success/fail)
python3 scripts/postbridge_api.py post-results

# Failure analysis
python3 scripts/postbridge_api.py failed-analysis

# Upload media file
python3 scripts/postbridge_api.py media-upload /path/to/video.mp4
```

---

### `postbridge_health.py` — Health Monitor & Error Diagnosis

```bash
# Full health check (recommended before any campaign)
python3 scripts/postbridge_health.py

# JSON report (for scripts)
python3 scripts/postbridge_health.py --report

# List failed posts with fix recommendations
python3 scripts/postbridge_health.py --failed
```

**What it checks:**
- Platform success rates (Facebook, Instagram, TikTok, YouTube, Threads, Twitter)
- Error breakdown by category with root cause
- Media file health (detects deleted S3 files)
- Account token status
- Recommendations per error type

**Platform health as of 2026-03-21:**
| Platform | Success Rate | Main Issue |
|----------|-------------|------------|
| Facebook | 80% ✅ | Good |
| Twitter | 65% ⚠️ | Auth 403 |
| Instagram | 64% ⚠️ | Rate limit |
| TikTok | ~0% 🔴 | Deleted media (FILE_ACCESS error) |
| Threads | 11% 🔴 | PostBridge API bug (known) |

---

### `postbridge_smart_post.py` — Validated Post Creator

**Prevents common errors automatically:**
- Skips Instagram/TikTok/YouTube if no media attached
- Validates media before posting (checks `isDeleted` flag)
- Auto-uploads media fresh on every post

```bash
# Post video to all 10 TikTok accounts
python3 scripts/postbridge_smart_post.py \
  --caption "Your caption here #hashtag" \
  --media /path/to/video.mp4 \
  --accounts all_tiktok \
  --delay-minutes 60

# Preview without posting
python3 scripts/postbridge_smart_post.py \
  --caption "..." \
  --media video.mp4 \
  --accounts all_tiktok \
  --dry-run

# Text post to Facebook/Threads/Twitter only
python3 scripts/postbridge_smart_post.py \
  --caption "Text caption here" \
  --accounts all_text

# Specific accounts (by ID)
python3 scripts/postbridge_smart_post.py \
  --caption "..." \
  --media video.mp4 \
  --accounts "48373,48374,49663"

# Schedule at specific time (UTC)
python3 scripts/postbridge_smart_post.py \
  --caption "..." \
  --media video.mp4 \
  --accounts all_tiktok \
  --scheduled-at "2026-03-22T08:00:00Z"
```

**Account group shortcuts:**
- `all_tiktok` → all 10 TikTok accounts
- `all_text` → Facebook + Threads + Twitter (text-safe)
- `all` → all 86 accounts (use with care + media)

---

### `tiktok_oauth_flow.py` — TikTok Connection Helper

```bash
# Check TikTok connection status
python3 scripts/tiktok_oauth_flow.py status

# Get instructions to reconnect TikTok
python3 scripts/tiktok_oauth_flow.py connect

# Get instructions to refresh tokens
python3 scripts/tiktok_oauth_flow.py refresh

# Verify after user authorizes
python3 scripts/tiktok_oauth_flow.py verify
```

---

## ⚡ Platform Rules (CRITICAL)

```
PLATFORM    | VIDEO | IMAGE | TEXT-ONLY | Notes
------------|-------|-------|-----------|------------------
YouTube     | ✅    | ❌    | ❌        | VIDEO ONLY
TikTok      | ✅    | ✅    | ❌        | Media required
Instagram   | ✅    | ✅    | ❌        | Media required
Facebook    | ✅    | ✅    | ✅        | All OK
Threads     | ✅    | ✅    | ✅        | All OK (11% success rate, PostBridge bug)
Twitter/X   | ✅    | ✅    | ✅        | All OK
LinkedIn    | ✅    | ✅    | ✅        | All OK
```

**postbridge_smart_post.py enforces these rules automatically.**

---

## 🚨 Error Catalog & Fixes

| Error | Root Cause | Fix |
|-------|-----------|-----|
| `File access error` | Media deleted from PostBridge S3 (`isDeleted: true`) | Re-upload fresh media every time |
| `No supported media files` | Text post sent to IG/TikTok/YouTube | Use `postbridge_smart_post.py` (auto-filters) |
| `Failed to post to Threads` | PostBridge Threads API bug | Known issue, retry or exclude Threads |
| `Rate limit reached` | Too many posts too fast | Space posts 30+ min apart |
| `Access token expired` | OAuth token expired | Reconnect account in PostBridge dashboard |
| `403 Forbidden` | Twitter auth revoked | Reconnect Twitter in dashboard |

**Golden Rules:**
1. **NEVER reuse old media IDs** — PostBridge deletes media after use
2. **ALWAYS fresh upload** before creating post
3. **NEVER send text-only to TikTok/Instagram/YouTube**

---

## 📊 Account Inventory

### TikTok (10 accounts)
| ID | Username |
|----|---------|
| 48335 | @clinicguru |
| 48336 | @baimwongdiskon |
| 48337 | @nugrohopratama5 |
| 48338 | @massehatyuk |
| 48372 | @divasehatsetiaphari |
| 48373 | @drlifehacks1 |
| 48374 | @riviewprodukfashionjujur |
| 49642 | @sehatseraiphari |
| 49659 | @catatanoperator |
| 49663 | @bkjaya00 |

### Instagram (12 accounts), YouTube (10), Facebook (38), Threads (13), Twitter (2), LinkedIn (1)

Run `python3 scripts/postbridge_api.py accounts` for full list.

---

## 🔄 TikTok OAuth — How to Reconnect

TikTok OAuth **requires user action** (cannot be fully automated from server):

1. Gue generate OAuth URL from PostBridge dashboard
2. Kirim URL ke kamu via Telegram
3. Kamu buka di browser yang sudah login TikTok → authorize
4. PostBridge auto-receives callback → token saved

**Generate URL:**
```python
# Via browser automation (see tiktok_oauth_flow.py)
# Browser navigates to PostBridge → click Connect TikTok → capture redirect URL
```

**Why can't it be fully automated:**
- TikTok OAuth requires `redirect_uri` whitelist (hardcoded to post-bridge.com)
- PostBridge callback needs active session cookie from same browser
- Cloudflare Turnstile blocks automated form submission

---

## ⚠️ Gaps & Roadmap

### Not Yet Implemented
- [ ] Webhook receiver (get notified when post publishes/fails)
- [ ] Auto-retry failed posts
- [ ] Bulk scheduling from CSV/JSON
- [ ] Analytics dashboard (charts)
- [ ] Auto-reconnect expired tokens (needs browser automation per platform)
- [ ] TikTok fully automated reconnect

### Partially Implemented
- [~] TikTok OAuth — URL generation works, user must click manually
- [~] Media upload — works but no progress indicator for large files

### Fully Working
- [x] All API endpoints (posts, accounts, analytics, media, post-results)
- [x] Platform filtering (auto-remove wrong platform/media combos)
- [x] Media health check (detect deleted files before posting)
- [x] Error diagnosis with root cause analysis
- [x] Health monitoring (platform success rates)
- [x] Smart post creation (validates before posting)
- [x] Analytics sync trigger

---

## 📁 File Structure

```
marketing/postbridge-manager/
├── README.md                      ← This file
├── SKILL.md                       ← Skill spec
├── scripts/
│   ├── postbridge_api.py         ← CLI wrapper (accounts, analytics, posts)
│   ├── postbridge_health.py      ← Health monitor + error diagnosis
│   ├── postbridge_smart_post.py  ← Validated post creator
│   └── tiktok_oauth_flow.py      ← TikTok connection helper
└── references/
    └── (place PostBridge API docs here)
```
