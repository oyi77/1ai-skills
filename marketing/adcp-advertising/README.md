# AdCP Advertising Skill - Quick Guide

## Overview
Automate advertising campaigns with AI. Launch display, video, CTV, and multi-channel campaigns using natural language - no dashboards or manual setup required.

## Installation
Located in: `skills/1ai-skills/adcp-advertising/`

## Key Features
- 🎯 **Launch campaigns in minutes** - Natural language commands
- 🔍 **Discover ad inventory** - AI-powered product matching
- 🎨 **Upload creatives** - Banner, video, audio assets
- 📊 **Track ROI** - Real-time performance metrics
- 🎛️ **Auto-optimize** - Reallocate budget to top performers
- 🌐 **Precise targeting** - Demographics, behaviors, locations

## Quick Start

### 1. Discover Capabilities
```python
# Test agent URL: https://test-agent.adcontextprotocol.org/mcp
# Auth: set ADCP_TOKEN env var (do not hardcode)

caps = await agent.getAdcpCapabilities({})
```

### 2. Find Products
```python
products = await agent.getProducts({
  'brief': 'Display ads for tech startup, budget $5000',
  'brand_manifest': {'url': 'https://startup.com'}
})
```

### 3. Create Campaign
```python
campaign = await agent.createMediaBuy({
  'buyer_ref': 'campaign-2026-q1',
  'brand_manifest': {'url': 'https://startup.com'},
  'packages': [{
    'product_id': 'premium_display',
    'budget': 10000
  }]
})
```

### 4. Upload Creatives
```python
await agent.syncCreatives({
  'creatives': [{
    'buyer_ref': 'banner-300x250',
    'url': 'https://cdn.example.com/banner.jpg'
  }]
})
```

### 5. Monitor Performance
```python
delivery = await agent.getMediaBuyDelivery({
  'media_buy_id': campaign.media_buy_id
})
print(f"CTR: {delivery.totals.ctr}%, Spend: ${delivery.totals.spend}")
```

### 6. Optimize
```python
await agent.updateMediaBuy({
  'media_buy_id': campaign.media_buy_id,
  'updates': {
    'status': 'active',
    'budget_change': 5000  # Add $5000
  }
})
```

## API Tasks

1. **get_adcp_capabilities** - Discover features (~1s)
2. **get_products** - Find inventory (~60s)
3. **list_creative_formats** - View specs (~1s)
4. **create_media_buy** - Launch campaign (minutes-days)
5. **update_media_buy** - Modify campaign (minutes-days)
6. **sync_creatives** - Upload assets (minutes-days)
7. **list_creatives** - Query library (~1s)
8. **get_media_buy_delivery** - Track performance (~60s)

## Targeting

```python
targeting_overlay = {
  'geo': {
    'included': ['US-CA', 'US-NY'],  # DMA codes
    'excluded': ['US-TX']
  },
  'demographics': {
    'age_ranges': [{'min': 25, 'max': 44}],
    'genders': ['M', 'F']
  },
  'behavioral': {
    'interests': ['technology', 'gaming'],
    'purchase_intent': ['consumer_electronics']
  },
  'contextual': {
    'keywords': ['innovation', 'design'],
    'categories': ['IAB19']  # Technology & Computing
  }
}
```

## Natural Language Examples

**Campaign Management:**
- "Create a display ad campaign"
- "Launch Facebook ads for my product"
- "Pause my underperforming campaigns"

**Ad Discovery:**
- "Find advertising inventory for luxury brands"
- "Show me CTV ad placements in major cities"
- "What display ad options are available?"

**Performance:**
- "How is my campaign performing?"
- "Show me ROI by channel"
- "Reallocate budget to top performers"

**Targeting:**
- "Target professionals in California"
- "Create a retargeting campaign"
- "Target by device type and time of day"

## Test Agent

**Public Test Agent:**
- URL: https://test-agent.adcontextprotocol.org/mcp
- Auth: ${ADCP_AUTH_TOKEN}
- **No setup required** - Test everything immediately

**Interactive UI:**
- https://testing.adcontextprotocol.org

## Important Notes

⚠️ **Asynchronous** - Operations may take minutes to days
⚠️ **Human approval** - Check for pending status
⚠️ **Start with capabilities** - Always call get_adcp_capabilities first
⚠️ **Brand context** - Provide detailed manifests for better results
⚠️ **Strict formats** - Validate creatives against specifications
⚠️ **Monitor regularly** - Check delivery metrics for pacing

## Documentation

- **Main:** https://docs.adcontextprotocol.org
- **Quickstart:** https://docs.adcontextprotocol.org/docs/quickstart
- **Media Buy Protocol:** https://docs.adcontextprotocol.org/docs/media-buy/
- **Task Reference:** https://docs.adcontextprotocol.org/docs/media-buy/task-reference/

## Auto-Activation

Triggered by keywords:
- "ad campaign", "display ads", "video ads"
- "facebook ads", "google ads", "CTV"
- "media buying", "programmatic advertising"
- "advertising automation", "ROI tracking"

Auto-activates from `.agentrc` skill_keywords configuration.

## Integration

Use from OpenClaw sessions or sub-agents when users mention:
- Launching ad campaigns
- Managing ad spend
- Optimizing ad performance
- Multi-channel advertising

Perfect complement to existing marketing skills (promotion, content-creator, etc.).