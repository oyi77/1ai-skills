# Link Attribution & Growth Tactics Reference

Combining link-level attribution (inspired by Dub) with founder-stage growth
playbooks (inspired by Marketing-for-Founders).

## Table of Contents
1. [Link Attribution](#link-attribution)
2. [UTM Strategy](#utm-strategy)
3. [Growth Playbook by Stage](#growth-playbook-by-stage)
4. [Launch Platforms & Directories](#launch-platforms--directories)
5. [Referral & Affiliate Programs](#referral--affiliate-programs)
6. [Outreach & Direct Sales](#outreach--direct-sales)
7. [Community-Led Growth](#community-led-growth)

---

## Link Attribution

### Why Links Matter for Attribution
Every marketing touchpoint generates a link. Each link is an attribution event.
Modern link management turns passive URLs into active measurement tools.

### Link Attribution Framework
```
Click → Lead → Activation → Revenue

For every link, track:
1. WHO clicked (device, geo, referrer)
2. WHAT they did next (signed up, purchased, bounced)
3. WHERE they came from (channel, campaign, content piece)
4. WHEN in the journey (first touch, assist, last touch)
5. HOW MUCH revenue attributed (per-link ROI)
```

### Branded Short Links Best Practices
- Use a branded domain (go.yourbrand.com, link.yourbrand.com)
- Make slugs descriptive: `go.brand.com/launch-offer` not `go.brand.com/x7k2`
- One link per unique distribution point (separate links for email vs social)
- Add UTM parameters to every link (auto-appended by link platform)
- Use geo/device targeting to personalize destination per audience
- Generate QR codes for offline-to-online tracking (print, events, packaging)

### Link-Level Metrics to Track
| Metric | What It Tells You |
|--------|-------------------|
| Total clicks | Reach and distribution effectiveness |
| Unique clicks | Actual audience size reached |
| Click-to-conversion rate | Link quality and targeting fit |
| Revenue per link | Direct monetary attribution |
| Time to conversion | Length of decision journey |
| Device/geo breakdown | Audience composition |
| Referrer distribution | Which channels drive traffic |

### Tools: Open-Source Link Management
- **Dub** (dub.co) — Modern link attribution platform, branded links, conversion tracking, affiliate programs. Open-source (AGPL-3.0)
- Self-hosted gives full data ownership and privacy compliance

---

## UTM Strategy

### UTM Parameter Standards

```
utm_source:    Platform name (lowercase, no spaces)
               → google, facebook, linkedin, newsletter, twitter, youtube

utm_medium:    Traffic type
               → cpc, organic, social, email, referral, affiliate, display

utm_campaign:  Campaign identifier
               → q3-launch, summer-sale-2026, welcome-series, blog-promo

utm_content:   Creative/content variant
               → hero-video, sidebar-cta, email-btn-red, carousel-slide-3

utm_term:      Keyword or targeting detail (paid search mainly)
               → ai-marketing-tools, competitor-brand-name
```

### UTM Naming Rules
- All lowercase, hyphens instead of spaces or underscores
- Consistent across all team members (document in a shared sheet)
- Never use UTMs on internal links (pollutes attribution data)
- Include date in campaign name for seasonal campaigns
- Use content parameter for A/B test variants

### UTM Builder Template
```
Base URL:  https://yoursite.com/landing-page
Source:    facebook
Medium:    cpc
Campaign:  q3-product-launch
Content:   video-ad-v2

Result: https://yoursite.com/landing-page?utm_source=facebook&utm_medium=cpc&utm_campaign=q3-product-launch&utm_content=video-ad-v2
```

---

## Growth Playbook by Stage

### Stage 1: First 10 Users ($0 Budget)
This is validation, not marketing. You need signal, not scale.

**Tactics:**
1. **Personal network** — DM/email 50 people you know who fit the persona
2. **Cold outreach** — 20 personalized DMs/emails daily to target users
3. **Build in public** — Share progress on Twitter/X, LinkedIn (founder's personal account)
4. **Online communities** — Answer questions on Reddit, IndieHackers, niche forums
5. **Co-founder/early user calls** — 30-min calls, offer free access for feedback

**Do NOT do yet:** SEO, paid ads, content marketing, social media management

### Stage 2: 10 → 100 Users ($0-500/month)
Now validate the channel, not just the product.

**Tactics:**
1. **Product launch** — Product Hunt, Hacker News, BetaList, IndieHackers
2. **Directory listings** — Submit to 20+ relevant directories and aggregators
3. **SEO foundations** — Set up blog, write 5 cornerstone articles targeting long-tail keywords
4. **Cold email at scale** — 50-100 personalized emails/week with clear value prop
5. **Social proof** — Collect and display testimonials, logos, usage stats
6. **Partnerships** — Find complementary tools, cross-promote

**Start experimenting with:** Basic content marketing, one social channel

### Stage 3: 100 → 1,000 Users ($500-5,000/month)
Double down on what's working. Cut what isn't.

**Tactics:**
1. **Paid acquisition testing** — Small budget A/B tests across 2-3 channels
2. **SEO ramp-up** — Publish 2-4 blog posts/week, build backlinks
3. **Email marketing** — Welcome sequence, newsletter, lead magnets
4. **Referral program** — Give users incentive to invite others
5. **Content marketing** — Case studies, comparison pages, templates/tools
6. **GEO (AI search)** — Optimize content to be cited by AI assistants

**Now invest in:** Analytics infrastructure, UTM discipline, CRM setup

### Stage 4: 1,000 → 10,000 Users ($5,000+/month)
This is scaling, not experimenting. Systematic growth.

**Tactics:**
1. **Paid ads at scale** — Proven channels, proven creative, scale budget
2. **Content engine** — Programmatic SEO, content hub, video content
3. **Affiliate program** — Formalize with tracking, payouts, partner materials
4. **Brand marketing** — Thought leadership, PR, conference speaking
5. **Marketing automation** — Sophisticated nurture, segmentation, scoring
6. **Retention marketing** — Reduce churn, increase LTV, upsell sequences

---

## Launch Platforms & Directories

### Tier 1: High-Impact Launches
| Platform | Best For | Tips |
|----------|----------|------|
| Product Hunt | SaaS, developer tools, consumer apps | Launch Tuesday-Thursday, engage all day, rally supporters |
| Hacker News (Show HN) | Technical products, open-source | Authentic, technical description, be ready for criticism |
| Reddit | Niche communities | Be genuine, add value, don't spam. Find your subreddit. |
| IndieHackers | Bootstrapped products | Share journey, milestones, revenue numbers |
| Twitter/X | Any tech product | Thread format, tag relevant people, launch day engagement |

### Tier 2: Directory Submissions
Submit to relevant directories in your niche. Some examples:
- **SaaS:** G2, Capterra, GetApp, SaaSHub, AlternativeTo, ToolFinder
- **AI tools:** There's an AI For That, FutureTools, AI Tool Directory
- **Open source:** Awesome lists on GitHub, OpenSourceAlternative.to
- **Dev tools:** StackShare, LibHunt, BuiltWith
- **Design:** Dribbble, Behance, CSS Design Awards

### Launch Day Checklist
- [ ] Landing page live and tested (mobile + desktop)
- [ ] Analytics and conversion tracking verified
- [ ] Social posts scheduled for launch morning
- [ ] Email blast to existing list ready
- [ ] Personal network alerted (DMs, not just posts)
- [ ] Monitoring mentions and comments (respond to everything)
- [ ] Thank-you email to early supporters prepped
- [ ] Post-launch survey ready (capture early feedback)

---

## Referral & Affiliate Programs

### Program Design Framework

**Referral (User → User)**
- Incentive: credit, extended trial, premium features, cash
- Both sides should benefit (referrer + referred)
- Make sharing friction-free (1-click link, pre-written messages)
- Track: referral rate, conversion rate, viral coefficient

**Affiliate (Partner → Users)**
- Commission: 20-30% recurring for SaaS is standard
- Cookie window: 30-90 days
- Provide: landing pages, swipe copy, banners, email templates
- Track: clicks, signups, revenue, commission payouts
- Payment: monthly via PayPal, Stripe, or partner platform

### Viral Coefficient Calculation
```
Viral Coefficient (K) = Invitations per user × Conversion rate of invitations

K > 1 = Viral growth (each user brings more than 1 new user)
K = 0.5 = Good referral contribution
K < 0.2 = Referral isn't a meaningful growth channel yet
```

---

## Outreach & Direct Sales

### Cold Email Framework

**Subject line:** Short, specific, no clickbait
**Structure:**
```
Line 1: Personalized observation about them (shows you did homework)
Line 2: The problem you solve (relevant to their situation)
Line 3: How you solve it (one sentence, specific)
Line 4: Social proof (one data point or customer name)
Line 5: CTA (one clear ask — reply, book a call, try the product)
```

**Example:**
```
Subject: Quick question about {their company's} checkout flow

Hi {Name},

I noticed {specific observation about their product/business}.
A lot of {their industry} teams struggle with {problem you solve}.

We built {product} to {how you solve it} — {customer name}
saw a {specific result} within {timeframe}.

Would you be open to a 15-min call this week to see if it'd help?

{Your name}
```

### Cold Email Rules
- Maximum 5 sentences
- Personalize the first line (ALWAYS)
- One CTA, not multiple options
- Follow up 3-4 times over 2 weeks, then stop
- Never lie or use deceptive subjects
- Comply with CAN-SPAM/GDPR (unsubscribe option, real address)

---

## Community-Led Growth

### Building in Public Strategy
- Share revenue milestones (MRR updates)
- Document failures and learnings (authenticity builds trust)
- Show behind-the-scenes of building (code, design, decisions)
- Ask for feedback publicly (makes people invested in your success)
- Celebrate user wins (makes your community feel valued)

### Community Channels
| Channel | Best For | Effort |
|---------|----------|--------|
| Discord server | Developer communities, real-time support | High (needs moderation) |
| Slack group | B2B communities, professional groups | Medium |
| GitHub Discussions | Open-source projects | Low |
| Subreddit | Niche topic communities | Medium |
| Newsletter | Thought leadership, content distribution | Medium |
| WhatsApp group | Local/regional communities, quick engagement | Low |

### Social Listening Strategy
- Monitor brand mentions (Google Alerts, Mention, Brand24)
- Track competitor mentions on social and forums
- Join conversations where your target audience asks questions
- Respond helpfully without being salesy
- Track which communities send the most qualified traffic
