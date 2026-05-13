# Analytics Tracking Setup Reference

Set up measurement infrastructure correctly the first time so you can
actually know what's working. No tracking = no optimization.

## Table of Contents
1. [Tracking Stack Setup](#tracking-stack-setup)
2. [GA4 Configuration](#ga4-configuration)
3. [Google Tag Manager](#google-tag-manager)
4. [Conversion Event Setup](#conversion-event-setup)
5. [UTM Parameter System](#utm-parameter-system)
6. [Platform Pixel Setup](#platform-pixel-setup)
7. [Tracking Audit Checklist](#tracking-audit-checklist)

---

## Tracking Stack Setup

### Essential Tracking Stack (Every Business Needs)

```
Google Analytics 4 (GA4)       — Website analytics and behavior
Google Tag Manager (GTM)       — Tag deployment without code changes
Google Search Console (GSC)    — SEO performance and indexation
Meta Pixel + CAPI             — Facebook/Instagram ad attribution
UTM Parameters                — Campaign source tracking
```

### Extended Stack (Growth Stage)
```
+ Hotjar / Microsoft Clarity  — Heatmaps and session recordings
+ Mixpanel / Amplitude        — Product analytics (SaaS/apps)
+ Google Looker Studio        — Custom reporting dashboards
+ Platform-specific pixels    — TikTok, LinkedIn, Twitter/X
+ Server-side tracking        — First-party data collection
+ Dub / link tracking         — Link-level attribution
```

### Setup Priority Order
1. GA4 + GTM (do this FIRST, before any marketing)
2. UTM system documented and shared with team
3. Conversion events defined and configured
4. Ad platform pixels installed
5. Search Console verified
6. Dashboard built
7. Heatmaps/recordings for optimization pages

---

## GA4 Configuration

### Essential GA4 Setup Steps
1. **Create GA4 property** at analytics.google.com
2. **Install tracking code** via GTM (recommended) or direct
3. **Configure data streams** — web, iOS, Android as applicable
4. **Set up conversions** — mark key events as conversions
5. **Link Google Ads** — for ad attribution
6. **Link Search Console** — for organic search data
7. **Configure data retention** — set to 14 months (maximum)
8. **Enable Google Signals** — for cross-device tracking
9. **Set up audiences** — for remarketing and analysis

### Key Events to Track (Recommended)

**E-commerce:**
```
view_item           — Product page viewed
add_to_cart         — Item added to cart
begin_checkout      — Checkout started
purchase            — Transaction completed
refund              — Refund processed
```

**SaaS / Lead Gen:**
```
sign_up             — Account created
login               — User logged in
generate_lead       — Form submitted / lead captured
tutorial_begin      — Onboarding started
tutorial_complete   — Onboarding completed
first_value_action  — Key activation event (custom)
upgrade             — Plan upgraded (custom)
```

**Content / Media:**
```
page_view           — Page viewed (automatic)
scroll              — 90% page scroll (automatic)
file_download       — Document downloaded (automatic)
video_start         — Video play initiated
video_complete      — Video watched to end
newsletter_signup   — Email subscription
```

### Custom Events Syntax (gtag.js)
```javascript
// Track a custom event
gtag('event', 'generate_lead', {
  'event_category': 'form',
  'event_label': 'contact_page',
  'value': 50  // estimated lead value
});

// Track purchase
gtag('event', 'purchase', {
  'transaction_id': 'T12345',
  'value': 99.99,
  'currency': 'USD',
  'items': [{
    'item_name': 'Pro Plan',
    'price': 99.99,
    'quantity': 1
  }]
});
```

### GA4 AI Traffic Tracking
Track visitors from AI search engines:
```
Create custom segment:
  Source contains: chatgpt OR perplexity OR gemini OR copilot OR claude
  OR
  Medium: ai-referral
```

---

## Google Tag Manager

### GTM Container Setup
1. Create GTM account and container at tagmanager.google.com
2. Install GTM snippet on all pages (in `<head>` and after `<body>`)
3. Configure GA4 tag with your Measurement ID
4. Set up triggers for key events
5. Test in Preview/Debug mode before publishing

### Common GTM Triggers

| Trigger | Type | Use For |
|---------|------|---------|
| All Pages | Page View | GA4 pageview tracking |
| Form Submit | Form Submission | Lead capture events |
| Click - CTA Button | Click - All Elements | CTA click tracking |
| Scroll Depth | Scroll Depth | Content engagement |
| Timer | Timer | Time on page signals |
| Custom Event | Custom Event | JavaScript-triggered events |
| YouTube Video | YouTube Video | Video engagement tracking |

### Data Layer for Custom Events
```javascript
// Push custom event data to GTM
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({
  'event': 'form_submit',
  'form_name': 'demo_request',
  'form_location': 'pricing_page'
});
```

---

## Conversion Event Setup

### Conversion Mapping Template

| Business Goal | Event Name | Trigger | Value |
|--------------|-----------|---------|-------|
| Lead captured | generate_lead | Form submit on /contact | $25 (avg lead value) |
| Free trial start | sign_up | Redirect to /welcome | $50 (trial value) |
| Demo booked | book_demo | Calendly completion | $100 (demo value) |
| Purchase | purchase | Thank you page / API | Actual transaction value |
| Newsletter signup | newsletter_signup | Email form submit | $5 (subscriber value) |

### Assign Monetary Values
Even non-revenue events need estimated values for ROAS calculation:
```
Value = (Conversion rate to revenue) × (Average revenue per conversion)

Example: Newsletter signup
  - 5% of subscribers eventually purchase
  - Average purchase = $200
  - Newsletter signup value = 0.05 × $200 = $10
```

---

## UTM Parameter System

### Standard UTM Parameters
```
utm_source    → Platform name (google, facebook, linkedin, newsletter)
utm_medium    → Traffic type (cpc, email, social, referral, organic)
utm_campaign  → Campaign identifier (q3-launch, summer-sale-2026)
utm_content   → Creative variant (video-a, cta-red, hero-image-v2)
utm_term      → Keyword (paid search only)
```

### UTM Naming Convention Rules
- All lowercase
- Hyphens instead of spaces or underscores
- Consistent across all team members
- Document in shared spreadsheet
- Never use UTMs on internal site links (pollutes data)
- Include date in campaign name for seasonal campaigns

### UTM Template by Channel
```
Email newsletter:
  ?utm_source=newsletter&utm_medium=email&utm_campaign=weekly-digest-2026-04

Facebook ad:
  ?utm_source=facebook&utm_medium=cpc&utm_campaign=q3-launch&utm_content=video-a

LinkedIn organic post:
  ?utm_source=linkedin&utm_medium=social&utm_campaign=thought-leadership

Google Search ad:
  ?utm_source=google&utm_medium=cpc&utm_campaign=brand-search&utm_term=your-brand-name

Influencer link:
  ?utm_source=instagram&utm_medium=influencer&utm_campaign=spring-collab&utm_content=creator-name

WhatsApp broadcast:
  ?utm_source=whatsapp&utm_medium=messaging&utm_campaign=flash-sale
```

### UTM Governance Document
Create a shared document for your team:
```markdown
# UTM Naming Standards — {Brand}

## Approved Sources
facebook, instagram, google, linkedin, tiktok, twitter,
youtube, newsletter, whatsapp, referral, direct

## Approved Mediums
cpc, cpm, email, social, organic, referral, affiliate,
influencer, messaging, display, video

## Campaign Naming Format
{quarter}-{campaign-name}-{year}
Example: q3-product-launch-2026

## Content Naming Format
{format}-{variant}
Example: video-a, carousel-b, static-c
```

---

## Platform Pixel Setup

### Meta Pixel + Conversions API (CAPI)
```
1. Create pixel in Meta Events Manager
2. Install base pixel code via GTM
3. Configure standard events (ViewContent, AddToCart, Purchase)
4. Set up Conversions API for server-side tracking
5. Verify events with Pixel Helper Chrome extension
6. Test with Test Events tool in Events Manager
```

**Why CAPI matters:** Browser-side pixels miss 20-40% of conversions due to
ad blockers and iOS privacy changes. CAPI sends events server-side.

### Google Ads Conversion Tracking
```
1. Create conversion action in Google Ads
2. Install global site tag via GTM
3. Add conversion event tag for each conversion type
4. Enable enhanced conversions (hashed email/phone)
5. Import GA4 conversions into Google Ads (alternative)
```

### TikTok Pixel
```
1. Create pixel in TikTok Ads Manager
2. Install via GTM
3. Configure events: ViewContent, AddToCart, Purchase
4. Set up Events API for server-side tracking
```

### LinkedIn Insight Tag
```
1. Create Insight Tag in LinkedIn Campaign Manager
2. Install via GTM
3. Configure conversion tracking for form submissions and page visits
```

---

## Tracking Audit Checklist

Run this monthly to ensure data quality:

### Data Collection
- [ ] GA4 receiving data (check Realtime report)
- [ ] All key pages tracked (no gaps in page_view data)
- [ ] Conversion events firing correctly (test each one)
- [ ] Event parameters passing correctly (check DebugView)
- [ ] No duplicate tracking (GTM + direct install = double counting)
- [ ] Internal traffic filtered (exclude office IPs)
- [ ] Bot traffic filtered (GA4 has built-in, verify)

### Attribution
- [ ] UTMs on all campaign links (spot-check 10 recent links)
- [ ] UTM naming convention followed (check for typos/inconsistencies)
- [ ] Ad platform pixels receiving conversion data
- [ ] Cross-domain tracking set up (if multiple domains)
- [ ] Attribution window appropriate per platform

### Reporting
- [ ] Dashboard data matches source data (spot-check 3 metrics)
- [ ] Goals/KPIs still relevant (update if business changed)
- [ ] Custom reports generating correctly
- [ ] Automated reports sending on schedule
- [ ] Team knows where to find key metrics

### Compliance
- [ ] Cookie consent banner present and functional
- [ ] Privacy policy updated with tracking disclosure
- [ ] Opt-out mechanism working (GDPR/CCPA/PDP)
- [ ] Data retention settings appropriate
- [ ] No PII (personally identifiable information) in GA4 events
