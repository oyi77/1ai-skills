# PostBridge API Reference

> Official API: https://api.post-bridge.com/reference
> API Key: pb_live_AT9Xm4PKaYBzAvFZYGgexi
> Rate Limit: 10 requests/second/key
> Auth: Bearer token in Authorization header

---

## Endpoints

### Analytics
- `GET /v1/analytics` — Get analytics (paginated: view_count, like_count, comment_count, share_count)
- `POST /v1/analytics/sync` — Sync analytics from TikTok/YouTube/Instagram (param: ?platform=tiktok|youtube|instagram)
- `GET /v1/analytics/{id}` — Get analytics by ID

### Posts
- `GET /v1/posts` — Get posts (filter: ?platform=tiktok|instagram|facebook|youtube&status=posted|scheduled|processing)
- `POST /v1/posts` — Create post (requires: caption, scheduled_at, social_accounts[], media[])
- `GET /v1/posts/{id}` — Get post by ID
- `PATCH /v1/posts/{id}` — Update post
- `DELETE /v1/posts/{id}` — Delete post

### Post Results
- `GET /v1/post-results` — Get post results (filter: ?post_id=X&platform=X)
- `GET /v1/post-results/{id}` — Get post result by ID

### Social Accounts
- `GET /v1/social-accounts` — Get accounts (filter: ?platform=X&username=X)
- `GET /v1/social-accounts/{id}` — Get account by ID

### Media
- `GET /v1/media` — Get media (filter: ?post_id=X&type=image|video)
- `GET /v1/media/{id}` — Get media by ID
- `POST /v1/media/create-upload-url` — Create signed upload URL (body: {name, mime_type, size_bytes})
- `DELETE /v1/media/{id}` — Delete media

---

## Connected Social Accounts (March 12, 2026)

| ID | Platform | Username |
|----|----------|----------|
| 48374 | tiktok | riviewprodukfashionjujur |
| 48373 | tiktok | drlifehacks1 |
| 48372 | tiktok | divasehatsetiaphari |
| 48338 | tiktok | massehatyuk |
| 48337 | tiktok | nugrohopratama5 |
| 48336 | tiktok | baimwongdiskon |
| 48335 | tiktok | clinicguru |
| 48186 | instagram | berkahkaryadigitalproduct |
| 48178 | facebook | Anak cerdas & kreatif |
| 48177 | facebook | Vanezia Herbal |
| 48176 | facebook | Marcello Mastroiani |
| 48175 | facebook | Francesca Inaudi |

---

## Analytics Sync Usage

```bash
# Trigger sync for all platforms
curl -X POST "https://api.post-bridge.com/v1/analytics/sync" \
  -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"

# Sync specific platform
curl -X POST "https://api.post-bridge.com/v1/analytics/sync?platform=tiktok" \
  -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"

# Get analytics
curl "https://api.post-bridge.com/v1/analytics?limit=50" \
  -H "Authorization: Bearer pb_live_AT9Xm4PKaYBzAvFZYGgexi"
```

---

## Key Learnings (March 12, 2026)

### Instagram Posts REQUIRE Media
- Error: "No supported media files found. Instagram only supports images and videos."
- 26 posts FAILED because they were text-only
- Instagram API rejects posts without image/video
- ALWAYS include media[] when posting to Instagram

### Analytics Only Available for YouTube (Currently)
- 2 analytics records found (both YouTube)
- TikTok and Instagram analytics may need time after sync
- Re-check after sync completes

### Post Workflow
1. Get social accounts → save IDs
2. Upload media → get media_id
3. Create post with caption + scheduled_at + social_accounts[] + media[]
4. Check post-results for success/failure
5. Sync analytics periodically for view counts

---

*Created: 2026-03-12 18:58 UTC+7*
*Source: PostBridge API Reference https://api.post-bridge.com/reference*
