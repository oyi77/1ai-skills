# Marketing Automation & Workflows Reference

Automation isn't about removing the human — it's about removing the repetitive
so humans can focus on strategy and creativity.

## Table of Contents
1. [Automation Architecture](#automation-architecture)
2. [Essential Workflow Recipes](#essential-workflow-recipes)
3. [Marketing Tech Stack](#marketing-tech-stack)
4. [Content Repurposing Pipeline](#content-repurposing-pipeline)
5. [Reporting Automation](#reporting-automation)
6. [AI in Marketing Workflows](#ai-in-marketing-workflows)

---

## Automation Architecture

### The Automation Decision Framework

Before automating anything, ask:
1. **Does this happen more than 3× per week?** → Automate
2. **Is the process the same every time?** → Automate
3. **Does it require creative judgment?** → Assist with AI, don't fully automate
4. **What's the cost of errors?** → High cost = human review required

### Automation Layers

```
Layer 1: Simple Triggers (Zero-code)
  → Auto-responders, scheduled posts, form notifications
  Tools: Native platform features, Zapier, Make

Layer 2: Conditional Workflows (Low-code)
  → If/then sequences, lead scoring updates, segment moves
  Tools: Mautic, HubSpot, ActiveCampaign, n8n

Layer 3: Multi-System Orchestration (Code-optional)
  → CRM sync, cross-platform attribution, custom pipelines
  Tools: n8n, custom scripts, MCP integrations

Layer 4: AI-Powered Automation (AI-assisted)
  → Content generation, dynamic personalization, predictive scoring
  Tools: Claude API, custom AI pipelines
```

---

## Essential Workflow Recipes

### 1. New Lead Processing
```
Trigger: Form submission / sign up

→ Add to CRM with source + UTM data
→ Send welcome email (immediate)
→ Calculate lead score (demographic + behavioral)
→ If score > 50 → Notify sales team in Slack/WhatsApp
→ If score < 50 → Add to nurture sequence
→ Tag with source channel for attribution
→ Add to retargeting audience
```

### 2. Content Publishing Pipeline
```
Trigger: Content marked "Ready to Publish"

→ Publish to blog/website
→ Submit URL to Google for indexing
→ Generate 3 social post variants (LinkedIn, Twitter, Instagram)
→ Schedule social posts across 7 days
→ Add to next newsletter roundup
→ Create short link with UTM tracking
→ Notify team in Slack
```

### 3. Abandoned Cart / Trial Recovery
```
Trigger: Cart abandoned OR trial inactive 3 days

→ Wait 1 hour → Send "Something go wrong?" email
→ Wait 24 hours → Send "Here's what you're missing" email
  → If opened → Add to "interested" segment
→ Wait 72 hours → Send incentive email (discount/extension)
  → If clicked → Notify sales for personal follow-up
→ Wait 7 days → Final email "Last chance"
→ If no action → Move to "dormant" segment
→ Add to retargeting ads for 30 days
```

### 4. Customer Onboarding
```
Trigger: Purchase / subscription activated

→ Send welcome email with setup guide (immediate)
→ Wait 1 day → "Quick start" email with video tutorial
→ If activated key feature → Congrats email
→ If NOT activated in 3 days → "Need help?" email
→ Wait 7 days → "Power user tips" email
→ Wait 14 days → NPS survey
  → If NPS 9-10 → Ask for review/testimonial
  → If NPS 0-6 → Notify support for outreach
→ Wait 30 days → Upsell/cross-sell email
```

### 5. Content Refresh Cycle
```
Trigger: Monthly (automated check)

→ Pull top 50 blog posts by organic traffic
→ Check for traffic decline > 20% MoM
→ For declining posts:
  → Check SERP position changes
  → Flag outdated stats, links, or screenshots
  → Create content refresh task
  → Assign to writer with specific update notes
→ After refresh → Resubmit to Google
→ Add "Last updated: {date}" to page
```

### 6. Weekly Marketing Report
```
Trigger: Every Monday 8:00 AM

→ Pull metrics from Google Analytics / GA4
→ Pull ad spend + results from Meta/Google Ads
→ Pull email metrics from email platform
→ Pull social metrics from social tools
→ Calculate WoW changes for key KPIs
→ Generate summary with top wins + concerns
→ Send to stakeholders via email/Slack
```

---

## Marketing Tech Stack

### Essential Stack by Company Stage

**Solo Founder / Pre-revenue:**
| Function | Tool (Free/Cheap) | Monthly Cost |
|----------|------------------|-------------|
| Website | Carrd, Framer, WordPress | $0-19 |
| Email | Brevo, MailerLite | $0-25 |
| Social scheduling | Buffer, Later | $0-15 |
| Analytics | GA4 + GSC | $0 |
| CRM | HubSpot Free, Twenty | $0 |
| Design | Canva Free | $0 |
| Link tracking | Dub Free | $0 |
| **Total** | | **$0-59/mo** |

**Growing Team (5-20 people):**
| Function | Tool | Monthly Cost |
|----------|------|-------------|
| Website | Webflow, WordPress | $30-50 |
| Email/Automation | ConvertKit, ActiveCampaign | $50-200 |
| Social | Buffer Pro, Hootsuite | $30-100 |
| Analytics | GA4 + Looker Studio | $0 |
| CRM | HubSpot Starter, Pipedrive | $50-200 |
| Ads | Meta Ads + Google Ads | $500-5000 |
| SEO | Ahrefs Lite, Semrush | $100-200 |
| Design | Canva Pro | $13 |
| Automation | Zapier, Make | $20-50 |
| **Total** | | **$800-6000/mo** |

**Scaling Company (20-100 people):**
| Function | Tool | Monthly Cost |
|----------|------|-------------|
| Marketing platform | HubSpot Pro, Mautic (self-hosted) | $0-800 |
| CRM | HubSpot, Salesforce | $200-1000 |
| Email | Customer.io, Braze | $200-500 |
| Analytics | Mixpanel, Amplitude | $0-1000 |
| Ads | Full platform mix | $5000+ |
| SEO | Ahrefs Standard, Surfer SEO | $200-400 |
| Content | Webflow, headless CMS | $50-200 |
| Automation | n8n (self-hosted), Zapier Teams | $0-200 |
| Attribution | Dub Pro, TripleWhale | $100-500 |

### Indonesia/UMKM-Specific Stack
| Function | Tool | Notes |
|----------|------|-------|
| Messaging | WhatsApp Business | Free, essential for IDN market |
| Social | Instagram + TikTok | Primary discovery channels |
| Marketplace | Tokopedia, Shopee | Built-in audience |
| Payment | Midtrans, Xendit | Local payment gateway |
| Website | Berdu, WordPress | Local hosting options |
| Email | Brevo | Free tier, supports Bahasa |
| Analytics | GA4 | Free |
| Design | Canva | Bahasa Indonesia templates available |

---

## Content Repurposing Pipeline

### The 1-to-10 System

Take ONE piece of pillar content and systematically create 10+ pieces:

```
1. PILLAR CONTENT (Blog post, webinar, or video)
   │
   ├── 2. LinkedIn post (key insight + hook)
   ├── 3. Twitter/X thread (step-by-step breakdown)
   ├── 4. Instagram carousel (visual summary, 8-12 slides)
   ├── 5. TikTok/Reel (60-sec video highlighting one point)
   ├── 6. Email newsletter section (curated excerpt)
   ├── 7. Quote graphic (strongest statement as image)
   ├── 8. Infographic (data/process visualization)
   ├── 9. Podcast talking point (discussion starter)
   └── 10. Community post (question format for engagement)
```

### Repurposing Rules
- **Rewrite, don't truncate** — each platform needs native content
- **Lead with the best insight** — don't save the punchline
- **Adapt format** — LinkedIn loves stories, Twitter loves lists, IG loves visuals
- **Stagger publishing** — spread over 1-2 weeks, don't dump everything at once
- **Track which derivative performs best** — invest more in that format

---

## Reporting Automation

### Automated Dashboard Data Sources

```python
# Conceptual pipeline — adapt to your tools
data_sources = {
    "website": "GA4 API → sessions, conversions, bounce rate",
    "email": "ESP API → sends, opens, clicks, unsubscribes",
    "social": "Native APIs → followers, engagement, reach",
    "ads": "Platform APIs → spend, impressions, clicks, conversions",
    "crm": "CRM API → leads, MQLs, SQLs, deals, revenue",
    "seo": "GSC API → impressions, clicks, CTR, position"
}

# Weekly report structure
report = {
    "period": "last 7 days",
    "kpis": calculate_kpis(data_sources),
    "wow_change": compare_to_previous_week(kpis),
    "top_performers": get_top_3(kpis),
    "concerns": get_declining_metrics(kpis),
    "recommendations": generate_action_items(kpis),
}
```

---

## AI in Marketing Workflows

### Where AI Adds Value (Not Hype)

| Task | AI Role | Human Role |
|------|---------|-----------|
| Content drafts | Generate first draft (70% done) | Edit, fact-check, add voice (30%) |
| Subject lines | Generate 10 variants | Select best 2-3 for A/B test |
| Ad copy | Generate variants per framework | Approve, adjust brand voice |
| Keyword research | Expand seed keywords, cluster by intent | Validate relevance, prioritize |
| Competitor analysis | Scrape and summarize | Interpret strategic implications |
| Reporting | Pull data, calculate metrics, summarize | Make decisions based on insights |
| Personalization | Dynamic content per segment | Define segments and rules |
| Customer research | Analyze reviews and survey data | Conduct interviews, synthesize |

### Where AI Falls Short (Keep Humans)
- **Strategy decisions** — AI can inform, humans must decide
- **Brand voice creation** — AI can follow rules, humans must create them
- **Crisis communication** — Too high-stakes for automation
- **Relationship building** — Genuine human connection can't be faked
- **Creative concepting** — AI can iterate, humans must originate
- **Ethics and compliance** — AI can flag, humans must judge

### AI Content Quality Control
Every AI-generated piece must pass:
- [ ] **Fact check** — verify all statistics, claims, and references
- [ ] **Brand voice** — does it sound like you, not like "an AI"?
- [ ] **Originality** — is it saying something useful, not just generic?
- [ ] **Human edit** — has a human reviewed and improved it?
- [ ] **No hallucinations** — are all product features, pricing, etc. accurate?
