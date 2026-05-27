---
name: adcp-advertising
description: AdCP Advertising Skill. Use when relevant to this domain.
persona:
  name: Gary Halbert
  title: The Prince of Print - Master of Direct Response
  expertise:
  - Direct Response
  - Copywriting
  - Advertising
  - Sales Letters
  philosophy: If you want to be successful, find someone who has achieved the results you want and copy what they do.
  credentials:
  - Wrote most mailed letter in history
  - Coached top copywriters
  - Marketing legend
  principles:
  - AIDA always
  - Test headlines
  - Benefits over features
  - Strong call to action
---
# AdCP Advertising Skill

## Name
adcp-advertising

## Display Name
AdCP Advertising

## Description
Automate advertising campaigns with AI. Create ads, buy media, manage ad budgets, discover ad inventory, run display ads, video ads, CTV campaigns, and optimize ad performance. Perfect for marketing automation, programmatic advertising, media buying, ad management, campaign optimization, creative management, and performance tracking. Launch Facebook ads, Google ads, display advertising, video marketing, and multi-channel campaigns using natural language. Supports ad targeting, audience segmentation, ROI tracking, and automated bidding.

## Author
AdCP Community

## License
MIT

## Homepage
https://docs.adcontextprotocol.org

## Repository
https://github.com/edyyy62/openclaw-adcp

## Category
advertising

## Subcategory
marketing-automation

## Type
agent

## Keywords
advertising, ads, marketing, campaigns, adcp, programmatic, media-buying, display-ads, video-ads, facebook-ads, google-ads, ctv, connected-tv, marketing-automation, ad-management, campaign-optimization, targeting, roi-tracking, performance-marketing, retargeting

---

## What It Does

**Automate your advertising campaigns with AI.** This skill enables OpenClaw agents to discover ad inventory, launch campaigns, manage creatives, and optimize performance across display, video, CTV, audio, and more - all through natural language commands.

**No dashboards. No forms. No ad platform expertise required.**

### Key Capabilities:

- 🎯 **Launch campaigns in minutes** - "Create a $10k display campaign targeting tech professionals in California"
- 🔍 **Discover ad inventory instantly** - "Find premium video placements for luxury brands"
- 🎨 **Upload ads with ease** - "Upload these banner images as creatives"
- 📊 **Track ROI in real-time** - "Show me campaign performance and CTR by creative"
- 🎛️ **Auto-optimize spend** - "Reallocate budget to top-performing packages"
- 🌐 **Target precisely** - Demographics, behaviors, interests, locations, devices, times

---

## Who It's For

- **Marketing teams** running Facebook ads, Google ads, and multi-channel campaigns
- **Media buyers** managing programmatic ad spend across publishers
- **Agencies** automating client campaign management and reporting
- **E-commerce brands** launching product ads and retargeting campaigns
- **Startups** running lean marketing with AI-powered automation

---

## Why Use AdCP

- **Skip the learning curve** - No need to master complex ad platforms
- **Save time** - Launch in 5 minutes vs hours of manual setup
- **Spend smarter** - AI automatically optimizes budgets to top performers
- **Scale faster** - Manage unlimited campaigns through simple commands
- **Test risk-free** - Public test agent included, no setup required

---

## Quick Start

### No setup required. Use the included test agent to try everything:

**Step 1: Discover what's available**
```
"Show me advertising capabilities"
```
→ Browse available channels, publishers, and formats.

**Step 2: Find ad inventory**
```
"Find display ads for a tech startup, budget $5000"
```
→ AI searches and shows matching products with pricing.

**Step 3: Launch campaign**
```
"Create campaign with Product prod_123, $5000 budget, targeting California tech professionals"
```
→ Campaign goes live instantly.

**Step 4: Upload your ads**
```
"Upload these banner images as creatives"
```
→ Drop files, get instant creative IDs.

**Step 5: Monitor performance**
```
"Show campaign metrics and ROI"
```
→ Real-time impressions, clicks, CTR, spend.

---

## Usage Examples

### Quick campaign launch:
```
User: "I need to run display ads for my SaaS product"
Agent: [Discovers products] "Found 5 display packages. Want details?"
User: "Create campaign with Product 1, $10k budget, target CTOs"
Agent: [Creates campaign] "Campaign live! ID: mb_abc123"
```

### Performance optimization:
```
User: "How are my video ads performing?"
Agent: [Shows metrics] "Package A: 2.3% CTR, Package B: 0.8% CTR"
User: "Move $5k from B to A"
Agent: [Reallocates] "Budget updated. Package A now $15k"
```

### Multi-channel campaign:
```
User: "Launch omnichannel campaign: display in CA, video in NYC, $50k total"
Agent: [Creates packages] "3 packages created across display and video"
```

---

## Natural Language Understanding

The skill understands:
- **Budgets:** `$5000`, `five thousand dollars`, `5k budget`
- **Locations:** `California`, `major US cities`, `New York and LA`
- **Audiences:** `tech professionals`, `age 25-45`, `high income`
- **Goals:** `brand awareness`, `drive conversions`, `increase sales`

---

## Workflow

### 1. Discovery Phase
```
"Find video advertising for luxury brands"
```
→ Agent searches inventory
→ Shows matched products with pricing
→ Explains targeting and formats

### 2. Campaign Creation
```
"Create campaign with Product 1, $25k, target professionals"
```
→ Agent creates media buy
→ Sets up targeting overlay
→ Returns campaign ID and status

### 3. Creative Management
```
"Upload my banner ads"
```
→ Agent syncs creatives
→ Assigns to campaign
→ Returns creative IDs

### 4. Monitoring & Optimization
```
"Show performance"
```
→ Agent fetches delivery data
→ Shows metrics by package/creative
→ Suggests optimizations

---

## API Tasks

AdCP provides 8 standardized tasks for the complete advertising lifecycle:

1. **get_adcp_capabilities** - Discover agent features and portfolio (~1s)
2. **get_products** - Find inventory using natural language (~60s)
3. **list_creative_formats** - View creative specifications (~1s)
4. **create_media_buy** - Launch campaigns (minutes-days, may require approval)
5. **update_media_buy** - Modify campaigns (minutes-days)
6. **sync_creatives** - Upload creative assets (minutes-days)
7. **list_creatives** - Query creative library (~1s)
8. **get_media_buy_delivery** - Track performance (~60s)

---

## Quick Example Code

```python
# 1. Discover capabilities
caps = await agent.getAdcpCapabilities({})

# 2. Find products
products = await agent.getProducts({
  'brief': 'Q1 2026 brand awareness campaign for tech startup',
  'brand_manifest': {'url': 'https://startup.com'},
  'filters': {'channels': ['display', 'video']}
})

# 3. Create campaign
campaign = await agent.createMediaBuy({
  'buyer_ref': 'q1-2026-awareness',
  'brand_manifest': {'url': 'https://startup.com'},
  'packages': [{
    'buyer_ref': 'pkg-001',
    'product_id': products.products[0].product_id,
    'pricing_option_id': 'cpm-standard',
    'budget': 15000
  }],
  'start_time': {'type': 'asap'},
  'end_time': '2026-03-31T23:59:59Z'
})

# 4. Upload creatives
await agent.syncCreatives({
  'creatives': [...],  # Your creative assets
  'assignments': {
    'creative_001': ['pkg-001']
  }
})

# 5. Monitor performance
delivery = await agent.getMediaBuyDelivery({
  'media_buy_id': campaign.media_buy_id
})

# 6. Optimize
await agent.updateMediaBuy({
  'media_buy_id': campaign.media_buy_id,
  'updates': {
    'status': 'active',
    'budget_change': 5000
  }
})
```

---

## Test Agent

For development and testing, use the public test agent:

**Agent URL:** https://test-agent.adcontextprotocol.org/mcp
**Auth Token:** REDACTED_ADCP_TOKEN

**Interactive testing:** https://testing.adcontextprotocol.org

---

## Critical Notes

- **AdCP is asynchronous** - Operations may take minutes to days
- **Human approval may be required** - Check for pending status
- **Start with capabilities** - Always call get_adcp_capabilities first
- **Brand context matters** - Provide detailed brand manifests for better results
- **Targeting is additive** - Product targeting + your overlay = final targeting
- **Creative formats are strict** - Always validate against format specifications
- **Monitor performance** - Regular delivery checks ensure campaign success

---

## Documentation

- **Main Docs:** https://docs.adcontextprotocol.org
- **Quickstart:** https://docs.adcontextprotocol.org/docs/quickstart
- **Media Buy Protocol:** https://docs.adcontextprotocol.org/docs/media-buy/
- **Task Reference:** https://docs.adcontextprotocol.org/docs/media-buy/task-reference/
- **Complete API Index:** https://docs.adcontextprotocol.org/llms.txt
## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

