---
name: postbridge-manager
description: >
  Manage PostBridge social media scheduler via API + browser automation.
  Use for: posting to TikTok/IG/YouTube/FB/Threads, scheduling, analytics,
  bulk upload, account connections, OAuth flow generation.
  Account: grahainsanmandiri@gmail.com | Plan: Pro (unlimited accounts)
---
persona:
  name: "Domain Expert"
  title: "Master of Postbridge Manager"
  expertise: ['Marketing Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# PostBridge Manager Skill

## Config

```
API Base:   https://api.post-bridge.com/v1
API Key:    REDACTED_POSTBRIDGE_KEY
Dashboard:  https://www.post-bridge.com/dashboard
Account:    grahainsanmandiri@gmail.com (Pro Plan - $49/mo)
Browser:    targetId C790D362929990FB49CE42759445D632 (openclaw profile)
```

## Key Facts

- **86 total accounts**: 38 FB, 12 IG, 13 Threads, 10 TikTok, 10 YouTube, 2 Twitter, 1 LinkedIn
- **1,602 posts** created | 126 scheduled | 1,475 posted
- **211 analytics records** | 8K total views | 76 likes
- **967 media** files uploaded
- **10,529 post-results** logged

## API Quick Reference

```python
import urllib.request, json

API = 'https://api.post-bridge.com/v1'
HEADERS = {'Authorization': 'Bearer REDACTED_POSTBRIDGE_KEY',
           'Content-Type': 'application/json'}

def pb_get(endpoint):
    req = urllib.request.Request(f'{API}{endpoint}', headers=HEADERS)
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

def pb_post(endpoint, data):
    req = urllib.request.Request(f'{API}{endpoint}',
        data=json.dumps(data).encode(), headers=HEADERS, method='POST')
    return json.loads(urllib.request.urlopen(req, timeout=15).read())
```

## Main Endpoints

### Social Accounts
```python
# List all (86 accounts)
pb_get('/social-accounts?limit=100')
# Returns: id, platform, username, status

# By platform
tiktok_ids = [a['id'] for a in accs if a['platform']=='tiktok']
# TikTok: bkjaya00, catatanoperator, sehatseraiphari, riviewprodukfashionjujur,
#          drlifehacks1, divasehatsetiaphari, massehatyuk, nugrohopratama5,
#          baimwongdiskon, clinicguru
```

### Posts
```python
# Create post
pb_post('/posts', {
    'caption': 'Your caption #hashtag',
    'scheduled_at': '2026-03-22T08:00:00Z',   # ISO UTC
    'social_accounts': [account_id1, account_id2],
    'media': [{'id': media_id}]                 # optional, required for IG/YT
})

# List posts
pb_get('/posts?limit=50&status=scheduled')  # status: scheduled/posted/draft
pb_get('/posts?limit=50')  # all

# Get post
pb_get(f'/posts/{post_id}')

# Delete post
# DELETE /v1/posts/{id}
```

### Analytics
```python
# Get analytics (sync first if stale)
pb_post('/analytics/sync', {})          # triggers TikTok+YT+IG refresh
pb_get('/analytics?limit=100')

# Fields per record: platform, platform_post_id, view_count,
#                    like_count, comment_count, share_count, post_result_id

# Top performer pattern:
items = pb_get('/analytics?limit=100')['data']
top = sorted(items, key=lambda x: -x.get('view_count',0))[:5]
```

### Post Results
```python
# Check success/failure per platform
pb_get('/post-results?limit=100')
# Fields: id, post_id, social_account_id, success, error, platform_data

# Get specific result
pb_get(f'/post-results/{result_id}')
# platform_data.username → which account posted
# platform_data.url → TikTok profile URL
```

### Media Upload
```python
# Step 1: Get upload URL
resp = pb_post('/media/create-upload-url', {
    'mime_type': 'video/mp4',    # or image/jpeg, image/png
    'file_size': file_size_bytes
})
upload_url = resp['upload_url']
media_id = resp['id']

# Step 2: PUT file to upload_url (signed S3)
with open('video.mp4', 'rb') as f:
    req = urllib.request.Request(upload_url, data=f.read(), method='PUT',
        headers={'Content-Type': 'video/mp4'})
    urllib.request.urlopen(req)

# Step 3: Use media_id in post creation
```

## Platform Rules (WAJIB)

| Platform | Video | Image | Text-only | Notes |
|----------|-------|-------|-----------|-------|
| YouTube | ✅ | ❌ | ❌ | VIDEO ONLY |
| TikTok | ✅ | ✅ slideshow | ❌ | media required |
| Instagram | ✅ | ✅ | ❌ | media required |
| Facebook | ✅ | ✅ | ✅ | all OK |
| Threads | ✅ | ✅ | ✅ | all OK |
| Twitter | ✅ | ✅ | ✅ | all OK |
| LinkedIn | ✅ | ✅ | ✅ | all OK |

## TikTok OAuth Flow (Browser Automation)

TikTok reconnect **requires user action** — generates OAuth URL → user opens on device logged into TikTok → PostBridge auto-receives token.

```python
# Step 1: Generate OAuth URL from PostBridge dashboard
# Run in browser (targetId: C790D362929990FB49CE42759445D632):

# Intercept popup URL
browser_eval("""
  window._captured = [];
  const orig = window.open;
  window.open = function(url, ...a) {
    window._captured.push(url);
    return orig.apply(this,[url,...a]);
  };
""")

# Click Connect TikTok → shows modal
browser_click('button[text="Connect Tiktok"]')
# Modal appears with "Connect" button

# Intercept fetch for limits check + navigation
browser_click('Connect button in modal')
# → browser navigates to TikTok OAuth URL

# Capture URL from browser.url after click
tiktok_oauth_url = browser.url  # https://www.tiktok.com/login?...&state=XXX

# Step 2: Send URL to user via Telegram
message(channel='telegram', target='codergaboets', message=f'Open this URL in TikTok-logged browser:\n{tiktok_oauth_url}')

# Step 3: User opens URL → logs in → PostBridge receives callback automatically
# Step 4: Verify connection
accounts = pb_get('/social-accounts?limit=100')['data']
new_tiktok = [a for a in accounts if a['platform']=='tiktok']
```

**OAuth URL structure:**
```
https://www.tiktok.com/login?...&redirect_url=...
  redirect_uri = https://www.post-bridge.com/api/tiktok-auth/callback
  state = {uuid}           → new connection
  state = refresh_{uuid}   → token refresh for existing accounts
  client_key = REDACTED_API_KEY
```

## Dashboard Pages

| Page | URL | Purpose |
|------|-----|---------|
| Create Post | /dashboard/create | text/image/video post |
| All Posts | /dashboard/posts | list, filter by status/platform |
| Calendar | /dashboard/posts/calendar | visual schedule |
| Scheduled | /dashboard/posts/scheduled | upcoming 126 posts |
| Posted | /dashboard/posts/posted | 1,475 published |
| Failed | /dashboard/posts/failed | failed posts |
| Analytics | /dashboard/analytics | views/likes/engagement chart |
| Bulk Tools | /dashboard/bulk-tools | bulk video/image upload |
| Connections | /dashboard/connections | manage 86 accounts |
| Settings | /dashboard/settings | profile, queue, email prefs |
| API Keys | /dashboard/api-keys | manage keys + webhook |
| Billing | /dashboard/settings/plans | Pro plan $49/mo |

## Bulk Tools (NEW Features)

- **Bulk Video Upload** — schedule multiple videos at once
- **Bulk Image Upload** — schedule multiple images at once
- **Bulk Video Creation** — AI-assisted 2x2 grid viral videos

## Known Issues

1. **Threads posting**: 36/100 failures → "Failed to post to Threads"
2. **Instagram rate limit**: 5/100 failures → too many posts too fast
3. **Instagram text-only**: 4/100 failures → no media attached
4. **Twitter 403**: 4/100 failures → likely auth token expired
5. **TikTok token**: Refresh needed every ~30 days → use OAuth flow above

## Account Groups (From Dashboard)

PostBridge supports account groups for easy targeting. Create via:
```python
# Via browser: Connections page → Create New Group section
# Select accounts → name group → Create Group
```

## Error Catalog & Fixes (Data-Driven)

### Platform Health (as of 2026-03-21)
| Platform | Success Rate | Main Issue |
|----------|-------------|------------|
| Facebook | 80% ✅ | Good |
| Twitter | 65% ⚠️ | Auth 403 |
| Instagram | 64% ⚠️ | Rate limit + transient errors |
| TikTok | 0% 🔴 | FILE_ACCESS (deleted media) |
| Threads | 11% 🔴 | Persistent API failures (known bug) |

### Error Types & Root Causes

| Error | Cause | Fix | Auto? |
|-------|-------|-----|-------|
| `FILE_ACCESS` | Media deleted from PostBridge S3 (`isDeleted=true`) | Re-upload media file | ❌ Manual |
| `No supported media` | Text post sent to IG/TikTok/YT | Filter accounts, add media | ✅ Auto-filter |
| `Failed to post to Threads` | PostBridge Threads API bug (66 failures seen) | Retry later or exclude Threads | ⚠️ Partial |
| `Rate limit` | Too many posts in short window | Space 30+ min apart | ✅ Reschedule |
| `Access token expired` | OAuth token expired | Reconnect account via dashboard | ❌ Manual OAuth |
| `403 Forbidden` | Auth token revoked | Reconnect account | ❌ Manual OAuth |
| `File access error` | Same as FILE_ACCESS above | Re-upload media | ❌ Manual |

### CRITICAL: Media Lifecycle
```
Upload media → PostBridge S3 (temporary storage)
                    ↓
           Media gets DELETED after use
                    ↓
         isDeleted=true, url=null
                    ↓
      Any post referencing deleted media → FILE_ACCESS ERROR
```
**Always re-upload media fresh before creating new posts.**
**Never reuse old media IDs from previous posts.**

### Platform Media Rules (HARD RULES)
```python
# NEVER send text-only to these platforms:
MEDIA_REQUIRED = {'tiktok', 'instagram', 'youtube'}

# YouTube needs VIDEO specifically (not image):
VIDEO_REQUIRED = {'youtube'}

# Text-only OK:
TEXT_OK = {'facebook', 'threads', 'twitter', 'linkedin'}

# Validation before posting:
def filter_accounts(accounts, has_media, mime_type):
    valid = []
    for acc in accounts:
        plat = acc['platform']
        if plat in MEDIA_REQUIRED and not has_media:
            continue  # skip — would fail
        if plat in VIDEO_REQUIRED and not mime_type.startswith('video/'):
            continue  # skip — would fail
        valid.append(acc)
    return valid
```

## Gotchas

- API returns TikTok accounts even when "refresh failed" on dashboard
- `/v1/analytics/sync` triggers background job — takes 30-60 sec to update
- Media upload: must PUT to signed URL within 15 min of getting it
- Scheduled posts: use UTC timezone in `scheduled_at`
- Vercel security checkpoint: API calls from this server work fine, dashboard browser calls sometimes hit checkpoint (use logged-in browser session)
- Magic link login: trigger from PostBridge login page → read email via gogcli → click link

## Script Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `postbridge_api.py` | CLI wrapper for all API ops | `python3 postbridge_api.py accounts tiktok` |
| `postbridge_health.py` | Health check + error diagnosis | `python3 postbridge_health.py` |
| `postbridge_smart_post.py` | Validated post creator | `python3 postbridge_smart_post.py --caption "..." --media video.mp4 --accounts all_tiktok` |
| `tiktok_oauth_flow.py` | TikTok OAuth flow docs + verifier | `python3 tiktok_oauth_flow.py status` |

### Smart Post — Correct Workflow
```bash
# Always upload fresh media first, then post
python3 skills/postbridge-manager/scripts/postbridge_smart_post.py \
  --caption "Your caption #hashtag" \
  --media /path/to/video.mp4 \
  --accounts all_tiktok \
  --delay-minutes 60

# Dry run first (preview without posting)
python3 postbridge_smart_post.py --caption "..." --media video.mp4 --accounts all_tiktok --dry-run

# Text-only to FB/Threads/Twitter only (safe)
python3 postbridge_smart_post.py --caption "..." --accounts all_text
```

## Common Workflows

### Post to all TikTok accounts
```python
tiktok_accs = [a['id'] for a in pb_get('/social-accounts?limit=100')['data'] 
               if a['platform']=='tiktok']
pb_post('/posts', {
    'caption': 'Your caption',
    'scheduled_at': '2026-03-22T01:00:00Z',
    'social_accounts': tiktok_accs,
    'media': [{'id': media_id}]
})
```

### Get analytics report
```python
pb_post('/analytics/sync', {})  # trigger refresh
import time; time.sleep(60)     # wait
data = pb_get('/analytics?limit=211')['data']
# aggregate by platform, sort by views
```

### Check failed posts
```python
results = pb_get('/post-results?limit=100')['data']
failed = [(r['error'], r['social_account_id']) 
          for r in results if not r['success']]
```
