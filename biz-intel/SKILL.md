---
name: biz-intel
description: >
  Business Intelligence & Competitive Espionage skill. Analyze, reverse-engineer,
  and extract full business intelligence from any competitor: business model,
  revenue streams, marketing strategy, content strategy, ads, pricing, tech stack,
  social proof, funnel architecture. Use to improve own business or clone competitor.
---

# Business Intel & Espionage Skill

## What This Skill Does

Full competitive intelligence on any business — from social media presence to
revenue estimation, from ad creative to pricing strategy. Outputs actionable
intelligence you can use to improve BerkahKarya or clone the business.

---

## Intelligence Modules

| Module | What It Extracts | Tools Used |
|--------|-----------------|------------|
| `social_spy` | Content strategy, posting frequency, top posts, engagement | Twitter-CLI, browser, TikTok/IG scrape |
| `ads_spy` | Ad creatives, copy, targeting, spend estimate | Facebook Ad Library, TikTok Ads, browser |
| `funnel_spy` | Landing pages, checkout flow, upsell chain, pricing | Browser automation, web fetch |
| `revenue_spy` | Revenue estimation, transaction volume, pricing tiers | App stores, marketplaces, Similarweb |
| `bot_spy` | Telegram bot architecture (uses bot-extractor skill) | Telethon |
| `tech_spy` | Tech stack, hosting, analytics tools, integrations | Wappalyzer, headers, DNS |
| `content_spy` | Content themes, hooks, formats, top performing content | Social platforms |
| `seo_spy` | Keywords, traffic sources, backlinks, ranking | Similarweb, search results |
| `model_spy` | Business model, monetization, pricing, profit model | Cross-analysis of all above |

---

## Quick Start

```bash
# Full espionage on a business
python3 skills/biz-intel/scripts/biz_spy.py --target "berkahkarya.org" --all

# Specific modules
python3 skills/biz-intel/scripts/biz_spy.py --target "@targetbot" --modules bot,funnel,revenue

# Social media spy
python3 skills/biz-intel/scripts/biz_spy.py --target "vidabot" --modules social,content,ads

# Generate improvement report for own business
python3 skills/biz-intel/scripts/biz_spy.py --target "competitor.com" --compare "berkahkarya.org"

# Clone blueprint
python3 skills/biz-intel/scripts/biz_spy.py --target "competitor.com" --mode clone
```

---

## Module Details

### 1. SOCIAL SPY
**What:** Full analysis of competitor's social media strategy

```python
# Extracts:
{
  "platforms": ["tiktok", "instagram", "twitter", "youtube"],
  "posting_frequency": {"tiktok": "3x/day", "instagram": "1x/day"},
  "content_themes": ["AI tools", "income tips", "lifestyle"],
  "top_performing_hooks": ["Teman saya ketawa...", "90% gagal karena..."],
  "engagement_rate": {"tiktok": "2.3%", "instagram": "0.8%"},
  "follower_count": {"tiktok": 45000, "instagram": 12000},
  "growth_rate": {"tiktok": "+500/week"},
  "best_posting_times": ["19:00", "12:00", "07:00"],
  "hashtag_strategy": ["#AITools", "#CaraKerja", "#UMKM"],
  "caption_formula": "pain point → story → solution → CTA"
}
```

### 2. ADS SPY
**What:** Reverse-engineer competitor's ad strategy

```python
# Sources:
# - Facebook Ad Library (public)
# - TikTok Creative Center (public)
# - Manual browser scraping

{
  "active_ads": 12,
  "ad_platforms": ["facebook", "instagram", "tiktok"],
  "ad_formats": ["video", "carousel", "static"],
  "creative_themes": ["before/after", "testimonial", "demo"],
  "copy_patterns": {
    "headline": ["Cara X dalam Y menit", "Tanpa X, bisa Y"],
    "cta": ["Coba Gratis", "Klaim Sekarang", "Lihat Demo"],
    "pain_points": ["buang waktu", "mahal", "ribet"]
  },
  "estimated_monthly_spend": "IDR 5-15 juta",
  "top_performing_ad_url": "...",
  "landing_page_url": "..."
}
```

### 3. FUNNEL SPY
**What:** Map entire customer journey from ad to checkout

```
AD → Landing Page → Opt-in → Thank You → Upsell 1 → Upsell 2 → Checkout → Post-purchase
```

```python
{
  "funnel_stages": [
    {"stage": "landing", "url": "...", "headline": "...", "cta": "..."},
    {"stage": "optin", "fields": ["email", "name"], "offer": "free ebook"},
    {"stage": "thank_you", "redirect": "upsell_page"},
    {"stage": "upsell_1", "price": "IDR 297K", "offer": "video course"},
    {"stage": "checkout", "payment": ["dana", "gopay", "transfer"]},
  ],
  "average_order_value": "IDR 149K",
  "upsell_rate_estimate": "30%",
  "checkout_friction": "low/medium/high",
  "trust_signals": ["testimonials", "money_back", "security_badges"]
}
```

### 4. REVENUE SPY
**What:** Estimate competitor's revenue

```python
# Estimation methods:
# 1. Marketplace: check product sold count × price
# 2. App: review count × ~50 (industry conversion) × price
# 3. Digital: traffic × conversion rate × AOV
# 4. Bot: message count patterns, user base size
# 5. Social: follower count × engagement × typical affiliate rate

{
  "revenue_estimate_monthly": {
    "low": "IDR 15 juta",
    "mid": "IDR 45 juta",
    "high": "IDR 120 juta"
  },
  "revenue_streams": [
    {"stream": "digital products", "estimate": "IDR 30 juta/month"},
    {"stream": "affiliate", "estimate": "IDR 10 juta/month"},
    {"stream": "consulting", "estimate": "IDR 5 juta/month"},
  ],
  "pricing_tiers": ["IDR 49K", "IDR 149K", "IDR 499K"],
  "transaction_volume_estimate": "~300 sales/month",
  "confidence": "medium"
}
```

### 5. BOT SPY
**What:** Full Telegram bot architecture extraction (uses bot-extractor skill)

```python
# Reuses bot_extractor.py
# Outputs: menus, callbacks, commands, input flows, tech hints
# See: skills/bot-extractor/SKILL.md
```

### 6. TECH SPY
**What:** Identify tech stack, tools, integrations

```python
{
  "hosting": "Vercel / AWS / DigitalOcean",
  "framework": "Next.js / Laravel / Flask",
  "payment": ["Midtrans", "Xendit", "Stripe"],
  "analytics": ["Google Analytics", "Facebook Pixel", "PostHog"],
  "email": ["Mailchimp", "Brevo", "custom SMTP"],
  "chatbot": "Telegram Bot (aiogram)",
  "crm": "Notion / Airtable",
  "scheduling": "PostBridge / Buffer",
  "ad_pixels": ["fb_pixel_id: 1234...", "tiktok_pixel_id: ..."],
  "cdn": "Cloudflare",
  "ssl": true,
  "whois": {"registrar": "Namecheap", "created": "2024-01-15"}
}
```

### 7. CONTENT SPY
**What:** Deep analysis of content strategy

```python
{
  "content_pillars": ["education", "inspiration", "promotion"],
  "top_formats": ["talking head", "screen record", "text overlay"],
  "hook_patterns": [
    "negative hook: X% orang gagal karena...",
    "curiosity: Cara X yang jarang orang tau",
    "story: Dulu gue juga...",
    "social proof: Klien gue berhasil...",
  ],
  "cta_patterns": ["link di bio", "DM gue", "klik sekarang"],
  "posting_schedule": {"days": ["Mon","Wed","Fri","Sat"], "times": ["07:00","12:00","19:00"]},
  "viral_content_analysis": [
    {"views": "500K", "hook": "...", "format": "...", "topic": "..."}
  ]
}
```

### 8. SEO SPY
**What:** Traffic, keywords, and search strategy

```python
{
  "monthly_traffic_estimate": "15K-50K visits",
  "top_keywords": ["ai tools indonesia", "cara bikin video ai", ...],
  "traffic_sources": {"organic": "40%", "social": "35%", "direct": "25%"},
  "top_pages": ["/tools", "/pricing", "/blog/ai-tools"],
  "backlinks": ["tokopedia.com", "tiktok.com", ...],
  "domain_authority": 28,
  "content_gaps": ["gue rank untuk X tapi kompetitor tidak"]
}
```

### 9. MODEL SPY
**What:** Full business model analysis

```python
{
  "business_type": "Digital Product Creator / SaaS",
  "target_market": "UMKM Indonesia, kreator konten, marketer",
  "value_proposition": "AI tools murah & mudah untuk Indonesia",
  "revenue_model": "one-time purchase + subscription",
  "acquisition_channels": ["tiktok organic", "telegram bot", "affiliate"],
  "retention_mechanism": ["telegram group", "regular new products"],
  "cost_structure": {
    "ai_api": "~$200/month",
    "hosting": "~$50/month",
    "ads": "~IDR 5 juta/month",
  },
  "moat": "audience trust + product variety",
  "weaknesses": ["no recurring revenue", "dead buttons in bot", "low conversion"],
  "opportunities": ["subscription model", "reseller program", "B2B"]
}
```

---

## Output Formats

### 1. Intelligence Report (Markdown)
Full detailed report per module

### 2. Clone Blueprint (JSON + Code)
Everything needed to replicate the business

### 3. Improvement Plan (for own business)
Gap analysis between competitor and BerkahKarya + action steps

### 4. One-Page Summary
Executive brief: key numbers, strategy, opportunities

---

## Data Sources

| Source | What | Access |
|--------|------|--------|
| Facebook Ad Library | Active ads, copy, creative | Public API / browser |
| TikTok Creative Center | Trending ads, top creatives | Public / browser |
| Twitter/X | Posts, engagement, strategy | twitter-cli (cookies) |
| Telegram bots | Full architecture | Telethon sessions |
| Website | Tech stack, funnel, pricing | Browser automation |
| WHOIS | Domain age, registrar | DNS lookup |
| Shopee/Tokopedia | Product sales count | Web scrape |
| LYNK.id | Product list, pricing, reviews | Web scrape |
| Similarweb | Traffic estimates | Web fetch |
| Google Search | Rankings, backlinks | Browser |
| App Store | Reviews, download estimates | Web fetch |

---

## Workflow: Spy on a Competitor

```
1. IDENTIFY
   └── Input: business name / URL / Telegram bot / social handle

2. DISCOVER
   └── Find all channels: website, socials, bot, ads, marketplace

3. EXTRACT per module
   ├── social_spy → content strategy
   ├── ads_spy → ad creative + copy
   ├── funnel_spy → customer journey
   ├── revenue_spy → money estimation
   ├── tech_spy → technology
   └── model_spy → business model

4. SYNTHESIZE
   └── Generate: Intelligence Report + Clone Blueprint + Improvement Plan

5. ACT
   ├── Clone: replicate what works
   ├── Improve: apply to BerkahKarya
   └── Counter: find gaps to exploit
```

---

## Case Study: @vidabot_generator_bot (2026-03-21)

### Summary Intelligence
- **Business:** AI video generation bot for Indonesian creators
- **Revenue estimate:** IDR 5-30 juta/month (Rp 5-30M)
- **Model:** Pay-per-feature Telegram bot + future subscription
- **Target:** Content creators, UMKM, social media managers
- **Moat:** Simple UX, Indonesian language, Telegram-first
- **Weaknesses:** Dead features, no /help, low UX score (34/100)
- **Opportunities for clone:** Add subscription, add /help, fix dead buttons, add analytics

### Clone Effort Estimate
- Bot code: 2-3 days (generated skeleton exists)
- AI integration: 3-5 days (connect to Replicate/Runway/Kling API)
- Deployment: 1 day
- **Total: ~1 week to launch MVP**

---

## Script Reference

| Script | Description |
|--------|-------------|
| `biz_spy.py` | Main orchestrator — runs all modules |
| `social_spy.py` | Social media intelligence |
| `ads_spy.py` | Ad creative + copy extraction |
| `funnel_spy.py` | Landing page + checkout flow mapping |
| `revenue_spy.py` | Revenue estimation engine |
| `tech_spy.py` | Tech stack fingerprinting |
| `content_spy.py` | Content strategy analysis |
| `model_spy.py` | Business model synthesis |
| `report_generator.py` | Generate formatted intelligence reports |

## Integration with Other Skills

- **bot-extractor** → `bot_spy` module
- **bca-checker** → verify cashflow health
- **postbridge-manager** → monitor competitor posting frequency via PostBridge analytics
- **twitter-cli** → social_spy, content_spy
- **browser automation** → funnel_spy, ads_spy, tech_spy
