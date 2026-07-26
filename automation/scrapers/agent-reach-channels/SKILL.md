---
name: agent-reach-channels
version: 1.0.0
category: automation
domain: social-commerce
description: Use when multi-platform e-commerce and messaging channel extraction (Shopee, TikTok Shop, WeChat)
keywords: [shopee, tiktok-shop, wechat, scraping, commerce, messaging, southeast-asia, indonesia]
tags:
- ecommerce
- scraping
- agent-reach
- shopee
- tiktok
- wechat
source: Panniantong/Agent-Reach
---

# Agent-Reach Channels: Shopee, TikTok Shop, WeChat

Unified channel extraction framework for Southeast Asian e-commerce (Shopee, TikTok Shop) and Chinese messaging (WeChat).


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
- **Shopee:** Extract products, reviews, seller info from Indonesia/Malaysia/Philippines/Thailand/Singapore/Vietnam
- **TikTok Shop:** Extract TikTok Shop products, live streams, seller metrics
- **WeChat:** Extract Official Account articles, mini-programs, Moments, user profiles

## Channels

### Shopee (Tier 2: Requires auth)
**Backends:** shopee-cli (primary), Selenium web scraping (fallback)
**Auth:** Cookie-based (browser login or shopee-cli)
**Extraction:** Product data, reviews, seller info, pricing
**Regions:** .co.id (Indonesia), .com.my (Malaysia), .com.ph (Philippines), .com.sg (Singapore), .com.th (Thailand), .vn (Vietnam)

```python
from agent_reach.channels.shopee import ShopeeChannel

channel = ShopeeChannel()
# Check backend availability
status, msg = channel.check()
# Extract product data
data = channel.extract("https://shopee.co.id/product/123456789")
```

### TikTok Shop (Tier 2: Requires auth)
**Backends:** tiktok-shop-cli (primary), Playwright web scraping (fallback)
**Auth:** TikTok account login (cookies)
**Extraction:** Products, live streams, seller metrics, engagement data
**Patterns:** /shop/, /live/, seller profiles

```python
from agent_reach.channels.tiktok_shop import TikTokShopChannel

channel = TikTokShopChannel()
# Check backend
status, msg = channel.check()
# Extract shop data
data = channel.extract("https://www.tiktok.com/shop/product/789")
```

### WeChat (Tier 2: Requires auth)
**Backends:** wechat-cli (primary), Selenium web scraping (fallback)
**Auth:** QR code login or existing session
**Extraction:** Official Account articles, mini-programs, Moments, user profiles
**Patterns:** mp.weixin.qq.com, wechat.com, WeChat IDs

```python
from agent_reach.channels.wechat import WeChatChannel

channel = WeChatChannel()
# Check backend
status, msg = channel.check()
# Extract WeChat data
data = channel.extract("https://mp.weixin.qq.com/s/article123")
```

## Integration with 1ai-ecosystem

Use in:
- **Content generation:** Extract trending products → generate marketing content
- **Market research:** Monitor competitor pricing on Shopee/TikTok Shop
- **Social intelligence:** Track WeChat Official Accounts for brand mentions
- **Bot automation:** Feed scraped data to content/trading bots

## Testing

26/26 tests passing (100%):
- URL pattern matching (all regions, all platforms)
- Backend availability checks
- Error handling and fallback logic
- Channel contract compliance (can_handle, check, extract methods)

```bash
pytest tests/test_new_channels.py -v  # 26 passed
```

## Safety & Compliance

- ✅ Respects robots.txt and Terms of Service
- ✅ Uses official CLI tools where available
- ✅ Implements respectful rate limiting
- ✅ Handles auth securely (cookies, credentials)
- ⚠️ Always check platform T&Cs before large-scale scraping

## Known Limitations

- **Shopee:** shopee-cli stability varies by region
- **TikTok Shop:** Rate limiting on live stream metrics
- **WeChat:** Requires active session; QR login needed periodically

## Related Skills

- smart-scraper: General web scraping framework
- social-listener: Cross-platform social media monitoring
- content-monitor: Track content performance
- price-tracker: Price monitoring (can use Shopee extraction)


## Workflow
See the parent skill for authoritative workflow documentation.
