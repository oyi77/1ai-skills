---
name: cold-email
description: Use when outbound email with personalization, deliverability optimization,
  follow-up sequences, and compliance. Use when building cold email campaigns, improving
  email deliverability, or designing outreach sequences.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- cold
- compliance
- email
- growth
- marketing
- seo
version: 1.0.0
category: marketing
---

# Cold Email

## When to Use

**Trigger phrases:**
- "cold email"
- "Building outbound sales campaigns"
- "Improving email deliverability rates"
- "Designing multi-touch sequences"


- Building outbound sales campaigns
- Improving email deliverability rates
- Designing multi-touch sequences
- A/B testing outreach copy


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Cold email is a B2B outreach channel where you send targeted, personalized emails to prospects who have not previously opted in. Done correctly, it generates qualified leads, books meetings, and drives pipeline at a fraction of the cost of paid advertising. The cold email lifecycle spans five phases: audience research, deliverability infrastructure, copywriting, sending and follow-up, and continuous optimization based on metrics.

Success depends on three interlocking factors. First, **technical deliverability** — properly configured SPF, DKIM, and DMARC DNS records ensure your emails reach the inbox instead of spam. Second, **personalization at depth** — referencing the prospect's industry, role, company news, or a shared connection drives reply rates 3–5× higher than generic blasts. Third, **systematic follow-up** — 80% of replies come after the third touch, so a structured 4–5 step sequence is non-negotiable.

The modern cold email stack combines lead sourcing tools (Apollo, LinkedIn Sales Navigator, ZoomInfo), email verification services (ZeroBounce, NeverBounce), sending platforms (SendGrid, AWS SES, Mailgun), and analytics for A/B testing subject lines, opening lines, and CTAs at statistical significance. Compliance with CAN-SPAM (US), GDPR (EU), and CASL (Canada) is mandatory — each email must identify the sender, include a physical address, and offer a one-click unsubscribe.

## Workflow

1. **Define ICP & Build Lead List** — Identify your ideal customer profile: industry, role, company size, pain point. Source leads from Apollo, LinkedIn Sales Navigator, Crunchbase, or ZoomInfo. Verify every email address with ZeroBounce or NeverBounce — target a bounce rate below 2%.
2. **Set Up Deliverability Infrastructure** — Configure a dedicated sending subdomain (e.g., `mail.yourdomain.com`). Add SPF, DKIM, and DMARC DNS records. Choose a sending platform (SendGrid, AWS SES, Mailgun, SMTP2GO) and warm up the domain over 2–4 weeks, starting at 5 emails/day and increasing by 20% daily.
3. **Write Personalized Copy** — Use the 4-part cold email structure: **Hook** (personalized observation — "Saw your recent Series A"), **Value** (specific benefit — "We helped SimilarCo cut CAC by 30%"), **Proof** (credential — "Backed by Y Combinator"), **CTA** (low-friction ask — "15-min call this Thursday?"). Achieve >80% personalization coverage with merge tags.
4. **A/B Test Variables** — For each campaign, test 2–3 subject lines, 2 opening lines, and 2 CTAs. Use a 95% statistical significance threshold to pick winners. Track opens, replies, and positive reply rates separately. Kill underperforming variants after 100 sends.
5. **Launch with Throttled Sending** — Send 50–100 emails/day per inbox, ramping volume by 20% daily. Schedule sends Tuesday through Thursday, 6–10 AM in the recipient's time zone. Never send from an unwarmed domain.
6. **Execute Follow-up Sequence** — Design a 5-touch sequence: Day 0 (initial email), Day 3 (value-add — case study or relevant article), Day 7 (social proof — "We're working with three companies in your space"), Day 14 (direct ask — "Is this a priority?"), Day 21 (breakup — "I'll assume the timing isn't right"). Each touch introduces new content — never resend the same email.
7. **Analyze, Report & Iterate** — Track key metrics per campaign: open rate (target >40%), reply rate (>5%), bounce rate (<2%), spam complaint rate (<0.1%). Pause any campaign that falls below thresholds. Rotate sending domains quarterly. Archive winning copy patterns into a swipe file for reuse.

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Personalization means using the first name" | Real personalization references industry, role, company news, or a shared connection. First-name-only is transparent token stuffing. |
| "Send as many emails as possible — it's a numbers game" | Volume without quality destroys sender reputation. A focused list of 500 verified leads outperforms 5000 unverified. |
| "Follow-ups are annoying — one email is enough" | 80% of replies come from follow-ups 3+. A single touch is invisibility, not respect for their inbox. |
| "GDPR means I can't cold email at all" | GDPR allows legitimate interest for B2B outreach if you identify yourself, provide opt-out, and respect suppression lists. |
| "Buy a pre-scraped list to save time" | Purchased lists deliver 0.1% reply rates, get you blacklisted, and violate CAN-SPAM. Build your own with verification. |
| "I'll set up SPF and DKIM later if there's a problem" | Without authentication, most inboxes auto-spam you. Configure DNS records before the first send — retroactive fix is too late. |


## Setup & Configuration

### Email Infrastructure (DNS Records)
Before sending cold emails, configure these DNS records on your sending domain:

```dns
; SPF — authorize sending servers
yourdomain.com.  TXT  "v=spf1 include:spf.sendgrid.net include:amazonses.com ~all"

; DKIM — sign emails for authentication
yourdomain.com.  TXT  "v=DKIM1; h=sha256; k=rsa; p=MIGfMA0GCSqGSIb4..."

; DMARC — policy for unauthenticated email
_dmarc.yourdomain.com.  TXT  "v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com"
```

Verify records with `dig TXT yourdomain.com`, `dig TXT _dmarc.yourdomain.com`, and tools like MXToolbox or mail-tester.com.

### Sending Platforms
- **SendGrid / Twilio** — Best for high-volume. Built-in analytics, suppression management, and sub-user isolation.
- **AWS SES** — Low cost ($0.10/1000 emails). Requires domain verification and production access request.
- **Mailgun** — Good deliverability. Includes email validation API and A/B testing support.
- **SMTP2GO** — Simple SMTP relay. Free tier (1000 emails/month).
- **MailerSend** — Modern platform with variable warmup and deliverability reports.

### Client Libraries
- Python: `smtplib` (SMTP), `sendgrid` (API), `boto3` (AWS SES), `sdk/mailgun` (Mailgun API)
- Node.js: `nodemailer` (SMTP), `@sendgrid/mail` (API), `@aws-sdk/client-ses` (AWS SES)

## Common Issues & Troubleshooting

| Problem | Root Cause | Solution |
|---|---|---|
| Emails landing in spam | Missing or misconfigured SPF/DKIM/DMARC | Verify DNS records with `dig` and mail-tester.com. Add missing records. Check blacklists at MXToolbox. |
| Low open rates (<20%) | Weak subject lines or poor sender reputation | A/B test subject lines with personalization and curiosity gaps. Warm up domain for 2 weeks before scaling. |
| High bounce rate (>5%) | Stale or unverified lead list | Verify emails with ZeroBounce or NeverBounce before sending. Remove role-based addresses (info@, sales@). |
| No replies to follow-ups | Sequence is too aggressive or adds no new value | Space touches 3–4 days apart. Each touch must offer fresh value — case study, article link, or social proof. |
| Domain blacklisted | Sending too fast or excessive spam complaints | Throttle to 50–100/day per inbox. Monitor blacklists. Implement one-click unsubscribe in every email. |
| Low personalization depth | Inadequate data enrichment | Enrich leads with industry, company size, recent funding, tech stack before writing. Use merge tags beyond first name. |

## Process

### Preparation
1. **Audience & Infrastructure** — Define ICP, source leads from Apollo/LinkedIn, verify emails with ZeroBounce or NeverBounce. Set up sending domain with SPF/DKIM/DMARC. Warm up domain for 2–4 weeks at 5–20 emails/day.
2. **Copy & Personalization** — Write the 4-part cold email (Hook → Value → Proof → CTA). Build merge tags for company, role, industry, and pain point. Draft 4–5 follow-up touches, each with unique value.

### Execution
3. **Launch & Throttle** — Send in batches of 50–100/day per inbox, ramping by 20% daily. Schedule Tuesday–Thursday, 6–10 AM recipient time zone.
4. **Follow-up Sequence** — Deploy touches on a Day 0, 3, 7, 14, 21 cadence. Never resend the same email — each touch adds a case study, article, or social proof.

### Stewardship
5. **Monitor & Iterate** — Target open rate >40%, reply rate >5%, bounce <2%, spam complaint rate <0.1%. A/B test continuously. Kill underperforming variants at 100 sends. Rotate domains if deliverability drops.

## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Cold Email Agency | 3-6 months | Full-service B2B cold email campaigns. Includes list building, copywriting, deliverability setup, sending, and optimization. Charge $2K–5K/month per client. |
| Lead Generation Service | 1-3 months | Source and verify B2B lead lists. Charge per lead ($0.10–0.50) or per list ($500–2000). Enrich with Apollo, ZoomInfo, Lusha data. |
| Deliverability Consulting | 1-2 months | Audit email infrastructure for deliverability issues. $2K–5K per audit including SPF/DKIM/DMARC review, blacklist check, and warmup plan. |
| SaaS — Domain Warmup & Monitor | 6-12 months | Build a tool that automates domain warmup and monitors deliverability health (reputation, blacklists, SPF/DKIM/DMARC status). |
| Template Packs & Courses | Immediate | Sell industry-specific cold email sequences on Gumroad ($29–97/pack). Or create a video course on cold email fundamentals. |

## Verification
- [ ] Target audience defined (ICP, industry, role, company size)
- [ ] Lead list sourced with verified emails (bounce rate <2%)
- [ ] Sending infrastructure configured — SPF, DKIM, DMARC verified via MXToolbox
- [ ] Copy drafted with personalization tokens and a clear CTA
- [ ] Follow-up sequence designed (minimum 4 touches with unique value each)
- [ ] A/B test variants created for subject line, opening line, and CTA
- [ ] Compliance checked — CAN-SPAM unsubscribe link, GDPR data processing notice, company address
- [ ] Campaign sent and metrics tracked (open rate, reply rate, bounce rate, spam complaints)