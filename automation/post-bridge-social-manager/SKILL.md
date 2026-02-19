# Post Bridge Social Manager

Post to multiple social media platforms via post-bridge.com API.

## Setup

**API Key:** `pb_live_LzxK4Q4428kb1b6KETgdue`

**Base URL:** `https://api.post-bridge.com/v1`

## Features

- Post to X (Twitter), LinkedIn, Facebook, Instagram, TikTok
- Schedule posts
- Multi-platform distribution
- Media upload support

## Usage

### Post to Social Media

```javascript
const response = await fetch('https://post-bridge.com/api/v1/posts', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${api_key}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    content: 'Your post content here',
    platforms: ['twitter', 'linkedin', 'facebook'],
    media_urls: ['https://example.com/image.jpg'],
    scheduled_at: '2026-02-18T12:00:00Z' // optional
  })
});
```

### Response

```json
{
  "success": true,
  "post_id": "post_123456",
  "platforms": {
    "twitter": "https://twitter.com/user/status/123",
    "linkedin": "https://linkedin.com/feed/update/456"
  }
}
```

## Platforms Supported

| Platform | ID | Notes |
|----------|-----|-------|
| X (Twitter) | `twitter` | Max 280 chars |
| LinkedIn | `linkedin` | Article or text |
| Facebook | `facebook` | Page or profile |
| Instagram | `instagram` | Image required |
| TikTok | `tiktok` | Video supported |

## Environment Variables

```env
POST_BRIDGE_API_KEY=pb_live_LzxK4Q4428kb1b6KETgdue
POST_BRIDGE_BASE_URL=https://post-bridge.com/api/v1
```

## Commands

- `post-bridge post` - Create a new post
- `post-bridge schedule` - Schedule a post
- `post-bridge list` - List recent posts
- `post-bridge delete` - Delete a post
