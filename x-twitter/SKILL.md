---
name: twitter-cli
description: Search, read, and post on X/Twitter using twitter-cli (no API key needed — uses browser cookies from OpenClaw browser profile). Use when searching tweets, reading threads, or monitoring topics on X/Twitter. For official API v2 writes, use xurl instead.
---

# twitter-cli — X/Twitter via Browser Cookies

`twitter-cli` uses cookies dari browser yang sudah login — tidak perlu API key.

---

## ⚠️ WAJIB: Setup Auth Sebelum Pakai

**twitter-cli butuh cookies dari OpenClaw browser.** Cookies TIDAK otomatis terdeteksi karena twitter-cli tidak tahu OpenClaw browser profile.

### Step 1: Refresh cookies (jalankan ini dulu)

```bash
python3 ~/.openclaw/workspace/scripts/refresh_twitter_cookies.py
```

Output: menulis `~/.twitter_env` dengan `TWITTER_AUTH_TOKEN` dan `TWITTER_CT0`.

### Step 2: Source env sebelum setiap perintah

```bash
source ~/.twitter_env && twitter search "query"
```

### Troubleshooting auth

```bash
# Cek apakah cookies sudah ada
cat ~/.twitter_env | head -2

# Refresh ulang (kalau cookies expired atau login baru)
python3 ~/.openclaw/workspace/scripts/refresh_twitter_cookies.py
source ~/.twitter_env

# Cek cookies di OpenClaw browser
python3 -c "
import browser_cookie3, os
jar = browser_cookie3.vivaldi(cookie_file=os.path.expanduser('~/.openclaw/browser/openclaw/user-data/Default/Cookies'))
cks = {c.name: c.value for c in jar if 'x.com' in c.domain}
print('auth_token' in cks, 'ct0' in cks)
"
```

**Kenapa harus manual?**  
twitter-cli cari cookies di Vivaldi/Chrome default profile (`~/.config/vivaldi/`), bukan di OpenClaw browser profile (`~/.openclaw/browser/openclaw/`). OpenClaw punya profile sendiri yang terpisah.

---

## Commands

```bash
# Search tweets
source ~/.twitter_env && twitter search "LLM caching optimization" 
source ~/.twitter_env && twitter search "from:anthropic prompt caching"

# Read tweet + replies
source ~/.twitter_env && twitter tweet <tweet_id_or_url>

# Home timeline
source ~/.twitter_env && twitter feed

# Trending
source ~/.twitter_env && twitter trending
```

---

## Cookie Location

| Browser Profile | Path |
|----------------|------|
| **OpenClaw (PAKAI INI)** | `~/.openclaw/browser/openclaw/user-data/Default/Cookies` |
| Vivaldi default | `~/.config/vivaldi/Default/Cookies` (kosong — X tidak login di sini) |

---

## Script Helper

```
~/.openclaw/workspace/scripts/refresh_twitter_cookies.py
```

Jalankan kalau:
- Pertama kali setup
- Cookies expired (twitter search error "not_authenticated")
- Setelah re-login ke X di OpenClaw browser
