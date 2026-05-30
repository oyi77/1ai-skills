---
name: postbridge-social-manager
description: PostBridge Social Manager. Use when relevant to this domain.
---
# PostBridge Social Manager

Complete integration with PostBridge API (https://api.post-bridge.com) for multi-platform social media posting, analytics, and media management.

## ⚠️ CRITICAL WARNINGS — READ FIRST

Key aspects of postbridge-social-manager relevant to this section.


### Instagram REQUIRES Media
> **26 posts FAILED SILENTLY because they were text-only.**  
> Instagram posts MUST include `media[]` (image or video).  
> Text-only posts to Instagram are REJECTED without any error message.  
> **ALWAYS include media when posting to Instagram.**

### Always Verify Post Results
> After posting, ALWAYS call `GET /v1/post-results` to confirm success/failure.  
> Posts can fail silently — the API returns 200 even when platform rejects content.

---

## Setup

```env
POSTBRIDGE_API_KEY=REDACTED_ROTATED_CREDENTIAL
POSTBRIDGE_BASE_URL=https://api.post-bridge.com/v1
```

**Auth:** `Authorization: Bearer {api_key}` on every request  
**Rate Limit:** 10 requests/second — add `time.sleep(0.2)` between calls in batch operations

---

## Complete API Reference

Full API documentation with endpoints, methods, and response formats.


### Posts

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/v1/posts` | List posts. Filter: `?platform=tiktok&status=posted\|scheduled\|processing` |
| POST | `/v1/posts` | Create post. **REQUIRED fields:** `caption`, `scheduled_at`, `social_accounts[]`, `media[]` |
| GET | `/v1/posts/{id}` | Get single post |
| PATCH | `/v1/posts/{id}` | Update existing post |
| DELETE | `/v1/posts/{id}` | Delete post |

### Post Results

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/v1/post-results` | Get results for all posts (success/failure/errors) |
| GET | `/v1/post-results/{id}` | Get result for specific post |

### Social Accounts

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/v1/social-accounts` | List connected accounts. Filter: `?platform=tiktok&username=@name` |
| GET | `/v1/social-accounts/{id}` | Get specific account details |

### Media

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/v1/media` | List all media items |
| POST | `/v1/media/create-upload-url` | Create signed upload URL. Body: `{name, mime_type, size_bytes}` |
| DELETE | `/v1/media/{id}` | Delete media item |

### Analytics

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/v1/analytics` | Get metrics (view_count, like_count, comment_count, share_count per post) |
| POST | `/v1/analytics/sync` | Trigger refresh. Query: `?platform=tiktok\|youtube\|instagram` |
| GET | `/v1/analytics/{id}` | Get analytics for specific post |

---

## Workflows

Step-by-step workflows for common operations.


### 1. Media Upload (Required for Instagram)

```python
import requests
import time

API_KEY = "REDACTED_ROTATED_CREDENTIAL"
BASE_URL = "https://api.post-bridge.com/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

def upload_media(file_path: str, mime_type: str) -> str:
    """Upload media and return media_id. Required for Instagram posts."""
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)
    
    # Step 1: Get signed upload URL
    resp = requests.post(
        f"{BASE_URL}/media/create-upload-url",
        headers=HEADERS,
        json={"name": file_name, "mime_type": mime_type, "size_bytes": file_size}
    )
    resp.raise_for_status()
    data = resp.json()
    media_id = data["media_id"]
    upload_url = data["upload_url"]
    
    # Step 2: Upload file to signed URL
    with open(file_path, "rb") as f:
        put_resp = requests.put(
            upload_url,
            data=f,
            headers={"Content-Type": mime_type}
        )
        put_resp.raise_for_status()
    
    return media_id  # Use this in post creation
```

### 2. Create Post

```python
def create_post(caption: str, account_ids: list, media_ids: list, scheduled_at: str) -> dict:
    """
    Create a post. media_ids is REQUIRED for Instagram.
    scheduled_at format: "2026-03-12T15:00:00Z" (ISO 8601 UTC)
    """
    resp = requests.post(
        f"{BASE_URL}/posts",
        headers=HEADERS,
        json={
            "caption": caption,
            "scheduled_at": scheduled_at,
            "social_accounts": account_ids,  # List of account IDs
            "media": media_ids               # REQUIRED for Instagram
        }
    )
    resp.raise_for_status()
    return resp.json()
```

### 3. Verify Post Results (MANDATORY After Posting)

```python
def check_post_results(post_id: str = None) -> list:
    """Always check results — posts can fail silently."""
    url = f"{BASE_URL}/post-results"
    if post_id:
        url = f"{BASE_URL}/post-results/{post_id}"
    
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    results = resp.json()
    
    # Log failures
    for result in (results if isinstance(results, list) else [results]):
        if result.get("status") != "success":
            print(f"❌ FAILED: Post {result.get('post_id')} — {result.get('error')}")
        else:
            print(f"✅ SUCCESS: Post {result.get('post_id')} on {result.get('platform')}")
    
    return results
```

### 4. Analytics Sync + Fetch

```python
def get_analytics(platform: str = "tiktok") -> list:
    """Sync then fetch analytics. platform: tiktok|youtube|instagram"""
    # Step 1: Trigger refresh
    sync_resp = requests.post(
        f"{BASE_URL}/analytics/sync?platform={platform}",
        headers=HEADERS
    )
    sync_resp.raise_for_status()
    
    # Step 2: Wait for sync to complete
    time.sleep(30)  # Analytics sync takes ~30 seconds
    
    # Step 3: Fetch analytics
    resp = requests.get(f"{BASE_URL}/analytics", headers=HEADERS)
    resp.raise_for_status()
    data = resp.json()
    
    # Returns: view_count, like_count, comment_count, share_count per post
    return data

def get_post_analytics(post_id: str) -> dict:
    """Get analytics for a specific post."""
    resp = requests.get(f"{BASE_URL}/analytics/{post_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()
```

### 5. Full Posting Workflow

```python
def post_to_instagram_and_tiktok(
    video_path: str,
    caption: str,
    instagram_account_id: str,
    tiktok_account_ids: list,
    scheduled_at: str
):
    """
    Complete workflow: upload media → create post → verify results.
    Instagram ALWAYS requires media.
    """
    # Step 1: Upload media (required for Instagram)
    print("📤 Uploading media...")
    media_id = upload_media(video_path, "video/mp4")
    print(f"✅ Media uploaded: {media_id}")
    
    time.sleep(0.2)  # Rate limit: 10 req/sec
    
    # Step 2: Create post for ALL accounts (include media for Instagram)
    all_accounts = [instagram_account_id] + tiktok_account_ids
    print(f"📮 Creating post for {len(all_accounts)} accounts...")
    post = create_post(
        caption=caption,
        account_ids=all_accounts,
        media_ids=[media_id],  # REQUIRED for Instagram
        scheduled_at=scheduled_at
    )
    post_id = post["id"]
    print(f"✅ Post created: {post_id}")
    
    # Step 3: Verify results (after scheduled time)
    time.sleep(2)
    print("🔍 Checking post results...")
    results = check_post_results(post_id)
    
    return {"post_id": post_id, "results": results}
```

### 6. Batch Posting with Rate Limiting

```python
def batch_post(posts: list, delay_seconds: float = 0.2):
    """
    Post multiple items with rate limiting.
    Rate limit: 10 req/sec → use 0.2s delay between requests.
    """
    results = []
    for i, post_data in enumerate(posts):
        print(f"[{i+1}/{len(posts)}] Posting...")
        
        # Upload media if path provided
        media_ids = []
        if post_data.get("media_path"):
            media_id = upload_media(post_data["media_path"], post_data.get("mime_type", "video/mp4"))
            media_ids.append(media_id)
            time.sleep(delay_seconds)
        
        # Create post
        result = create_post(
            caption=post_data["caption"],
            account_ids=post_data["account_ids"],
            media_ids=media_ids,
            scheduled_at=post_data["scheduled_at"]
        )
        results.append(result)
        time.sleep(delay_seconds)  # Rate limiting
        
        # Pause every 10 posts
        if (i + 1) % 10 == 0:
            print("⏸ Pausing 2s to respect rate limits...")
            time.sleep(2)
    
    return results
```

---

## Get Social Account IDs

```python
def get_social_accounts(platform: str = None) -> list:
    """Get connected account IDs. Use these in post creation."""
    url = f"{BASE_URL}/social-accounts"
    if platform:
        url += f"?platform={platform}"
    
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    accounts = resp.json()
    
    for acc in accounts:
        print(f"Platform: {acc['platform']} | ID: {acc['id']} | Username: {acc['username']}")
    
    return accounts

# Current connected accounts: 12 total
# - TikTok: 7 accounts
# - Instagram: 1 account (berkahkaryadigitalproduct) ← REQUIRES MEDIA
# - Facebook: 4 accounts
```

---

## Error Handling

```python
def safe_create_post(caption: str, account_ids: list, media_ids: list, scheduled_at: str) -> dict:
    """Create post with full error handling."""
    # Validate: Check if Instagram accounts are in the list
    instagram_accounts = get_social_accounts("instagram")
    instagram_ids = {acc["id"] for acc in instagram_accounts}
    
    has_instagram = any(acc_id in instagram_ids for acc_id in account_ids)
    
    if has_instagram and not media_ids:
        raise ValueError("❌ BLOCKED: Instagram post requires media[] — upload media first!")
    
    try:
        result = create_post(caption, account_ids, media_ids, scheduled_at)
        
        # Always verify
        time.sleep(1)
        results = check_post_results(result["id"])
        
        failed = [r for r in results if r.get("status") != "success"]
        if failed:
            print(f"⚠️ {len(failed)} platform(s) failed:")
            for f in failed:
                print(f"  - {f['platform']}: {f.get('error', 'Unknown error')}")
        
        return result
        
    except requests.HTTPError as e:
        print(f"❌ HTTP Error: {e.response.status_code} — {e.response.text}")
        raise
```

---

## Common Mistakes to Avoid

| ❌ Wrong | ✅ Correct |
|---------|----------|
| Post to Instagram without media | Always upload media first via `/media/create-upload-url` |
| Skip post-results check | Always call `GET /v1/post-results` after posting |
| Use old base URL `post-bridge.com/api/v1` | Use `api.post-bridge.com/v1` |
| No rate limit delays in batch | Add `time.sleep(0.2)` between API calls |
| Use `platforms: ['instagram']` format | Use `social_accounts: [account_id]` format |
| No analytics sync before reading | Call `POST /analytics/sync` first, wait 30s |

---

## Quick Reference Commands (curl)

```bash
# List all posts
curl -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  https://api.post-bridge.com/v1/posts

# List posted TikTok posts
curl -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  "https://api.post-bridge.com/v1/posts?platform=tiktok&status=posted"

# Check all post results
curl -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  https://api.post-bridge.com/v1/post-results

# Get connected accounts
curl -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  https://api.post-bridge.com/v1/social-accounts

# Sync TikTok analytics
curl -X POST -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  "https://api.post-bridge.com/v1/analytics/sync?platform=tiktok"

# Get analytics
curl -H "Authorization: Bearer $POSTBRIDGE_API_KEY" \
  https://api.post-bridge.com/v1/analytics
```

---

## Integration with Other Skills

- **viral-content-creator**: Generate videos → upload via this skill
- **tiktok-carousel-creator**: Create carousels → schedule via PostBridge
- **analytics-dashboard**: Pull PostBridge analytics into unified dashboard
- **content-scheduler**: Schedule posts using PostBridge API
- **social-media-upload**: Use PostBridge as the posting backend

---

**API Reference:** https://api.post-bridge.com/reference  
**Last Updated:** 2026-03-12  
**Critical Fix:** Instagram media requirement — 26 posts failed without this

## When to Use

- When you need automated assistance with a specific technical task
- When the task requires domain expertise this agent provides
- When consistency and repeatability matter more than creative exploration

## When NOT to Use

- Task is about social media management, not automation
- You need to build a custom social media tool (use development)
- Task requires real-time engagement (use social media tools)
- You don't have PostBridge account
- Task is about content creation (use content tools)
- You need analytics (use analytics tools)

## Red Flags

- Claiming completion without running verification
- Skipping the analysis phase and jumping to implementation
- Ignoring existing codebase patterns and conventions

## Verification

- [ ] Output matches the original requirements
- [ ] All code or content runs without errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain