---
name: email-sequences
description: Automated email sequence design — welcome series, nurture funnels, re-engagement,
  transactional flows. Use when building email automation systems.
domain: marketing
license: Apache-2.0
tags:
- email
- growth
- marketing
- sequences
- money
- automation
- conversions
version: 2.0.0
author: oyi77
subdomain: ''
type: marketing
category: marketing
---


# Money-Making Overview

Email sequences directly drive revenue. A welcome sequence converts 3-10% of new subscribers. A nurture sequence turns 2-5% of leads into customers. Re-engagement reclaims 10-15% of dormant subscribers. For a 10K subscriber list at $50 average order, a 5% conversion sequence = $25,000.

## Revenue Streams
1. **Email Sequence Setup ($1K-5K/client)** — build automations for businesses
2. **Sequence Templates ($47-197/set)** — sell pre-built sequences
3. **Managed Email ($500-2K/mo)** — run their sequences

## First Action in 60 Minutes
```bash
#!/usr/bin/env bash
# Create a 5-email welcome sequence in 60 minutes
mkdir -p ~/email-sequences/welcome

cat > ~/email-sequences/welcome/01-welcome.md << 'EMAILEOF'
Subject: Welcome to [Brand] — here's your [lead magnet]
Body: Thank you for joining! Here's the [resource] you requested.
CTA: [Link to best content/product]
EMAILEOF

cat > ~/email-sequences/welcome/02-story.md << 'EMAILEOF'
Subject: The story behind [Brand]
Body: How we started, why we do this, and what we believe.
CTA: Read our manifesto
EMAILEOF

cat > ~/email-sequences/welcome/03-value.md << 'EMAILEOF'
Subject: 3 ways to get the most out of [product]
Body: Quick wins your customers use.
CTA: [Product link]
EMAILEOF

cat > ~/email-sequences/welcome/04-social.md << 'EMAILEOF'
Subject: Join our community
Body: Connect with [N] other [audience] on [platform].
CTA: Join community
EMAILEOF

cat > ~/email-sequences/welcome/05-offer.md << 'EMAILEOF'
Subject: Exclusive offer for new members
Body: Limited-time discount on [product].
CTA: Get [X]% off — expires [date]
EMAILEOF

echo "=== Welcome sequence created ==="
echo "Day 1: Welcome + lead magnet"
echo "Day 3: Brand story"
echo "Day 5: Value/quick wins"
echo "Day 7: Community"
echo "Day 10: Offer"
```

## Sequence Mapping and Automation Triggers

Every sequence needs three things: a trigger (what starts it), a goal (what it should do), and an exit (when to stop).

### Sequence Types and Triggers

| Sequence | Trigger | Goal | Timing |
|----------|---------|------|--------|
| **Welcome Series** | Signup / opt-in | Convert to first purchase | 5-10 emails over 14 days |
| **Nurture Funnel** | Lead magnet download | Book call / purchase | 4-8 emails over 2-4 weeks |
| **Re-engagement** | 60-90 days inactive | Re-activate or tag for cleanup | 3-5 emails over 2 weeks |
| **Transactional** | Purchase / event | Upsell, cross-sell, feedback | 1-5 emails triggered by action |
| **Abandoned Cart** | Cart created, no purchase | Recover sale | 3 emails over 72 hours |
| **Win-back** | 6+ months no purchase | Win back lapsed customer | 3 emails over 10 days |
| **Onboarding** | Product signup / trial start | Activate core feature usage | 5-7 emails over 14 days |
| **Post-Purchase** | Order confirmed | Upsell, review request, repeat | 3-5 emails over 30 days |

### Trigger Rules

- **Behavioral triggers** outperform time-based sends 3:1
- A trigger fires only once per contact unless re-added via a new event
- Delay between triggered emails: minimum 24 hours, maximum 7 days between touches
- Exit logic: if contact converts or unsubscribes, remove from all active sequences

## Welcome Series

The highest-converting sequence in any email program. New subscribers are warm — they just opted in. Capitalize immediately.

### 5-Email Welcome Series Blueprint

| # | Timing | Subject Line Angle | Goal |
|---|--------|---------------------|------|
| 1 | Immediately | Deliver lead magnet / confirm signup | Deliver promise, establish sender |
| 2 | Day 2-3 | Brand story / origin | Build connection and trust |
| 3 | Day 4-5 | Value / quick wins | Demonstrate product value |
| 4 | Day 6-7 | Social proof / community | Reduce perceived risk |
| 5 | Day 8-10 | Offer / discount | Convert to first purchase |

### Welcome Series Best Practices

- **Single CTA per email** — one link, one button, one ask
- **Lead magnet in email 1** — deliver what was promised immediately
- **No hard sell before email 3** — earn trust before asking for money
- **Discount escalates** — start with social proof, close with offer
- **Remove from welcome after purchase** — transition to onboarding

## Nurture Funnels

Lead nurturing moves cold subscribers toward a purchase decision. The sequence replaces the role of a salesperson: educate, build trust, present offer.

### 6-Email Nurture Blueprint

| # | Angle | Content | Goal |
|---|-------|---------|------|
| 1 | Problem awareness | The cost of inaction | Create urgency |
| 2 | Education | How to solve [problem] | Establish authority |
| 3 | Social proof | Case study / testimonial | Reduce skepticism |
| 4 | Solution | Your product/service as answer | Present the option |
| 5 | Objection handling | FAQ / comparison | Remove barriers |
| 6 | Offer | Limited-time / bonus | Close |

### Nurture Rules

- Use 70% value / 30% promotion ratio
- Each email should give away a piece of your methodology for free
- Track click-through to score leads (3+ clicks = sales-ready)
- Add lead scoring: download + click + page visit = alert sales
- A contact who clicks every email but never buys needs a different angle, not more emails

## Re-engagement Sequences

Dormant subscribers cost money (platform fees), hurt deliverability (low engagement), and distort metrics. Either re-activate them or remove them.

### 4-Email Re-engagement Blueprint

| # | Timing | Angle | Subject Line Example | Goal |
|---|--------|-------|----------------------|------|
| 1 | Immediately | We miss you | "Haven't seen you in a while" | Trigger recognition |
| 2 | Day 3 | New value | "Here's what you missed" | Show fresh content |
| 3 | Day 7 | Win-back offer | "Come back with [X]% off" | Offer incentive |
| 4 | Day 14 | Last chance | "We'll stop emailing after this" | Clean or convert |

### Re-engagement Rules

- Set a clear re-engagement threshold (60 days no open, 90 days no click)
- Email 4 is make-or-break: those who don't engage get tagged `dormant` and removed from active list
- Tag re-engaged contacts separately to track recovery rate
- A 10-15% reactivation rate is healthy; below 5% means list quality is degrading

## Transactional Flows

Transactional emails have 4-8x higher open and click rates than marketing emails. Use that attention.

### Key Transactional Emails

| Type | Open Rate | CTA | Goal |
|------|-----------|-----|------|
| Order confirmation | 60-80% | Track order, browse related | Upsell |
| Shipping update | 70-90% | Track, share with friend | Referral |
| Password reset | 50-70% | Reset link | Security (no upsell) |
| Receipt / invoice | 50-65% | Review request, repeat | Retention |
| Account expiration | 60-80% | Renew / extend | Retention |
| Abandoned cart (1h) | 40-50% | Complete purchase | Recovery |
| Abandoned cart (24h) | 30-40% | Reminder + social proof | Recovery |
| Abandoned cart (72h) | 25-35% | Discount offer | Last-chance recovery |

### Transactional Best Practices

- Include a single, relevant marketing CTA in every transactional email
- Never hide the transactional purpose — the core message must come first
- Monitor delivery separately: transactional routes bypass marketing filters
- Keep HTML minimal to avoid landing in promotions tab

## Abandoned Cart Sequences

Abandoned cart emails recover 10-15% of lost revenue on average.

### 3-Email Cart Recovery Blueprint

| # | Timing | Angle | Goal |
|---|--------|-------|------|
| 1 | 1 hour | Reminder with product image | Simple nudge |
| 2 | 24 hours | Social proof / urgency | "Only [N] left" |
| 3 | 72 hours | Discount (10-15% off) | Incentive close |

### Cart Recovery Rules

- Email 1: no discount — many people just forgot
- Email 2: add reviews, ratings, low-stock alerts
- Email 3: offer discount only if margins allow
- Remove from cart sequence immediately on purchase
- Track recovery rate: 10%+ is healthy

## Personalization Patterns

Beyond `{first_name}`. Personalization drives 6x higher transaction rates.

### Levels of Personalization

| Level | Example | Effort | Lift |
|-------|---------|--------|------|
| **L1: Basic merge tags** | `Hi {first_name}` | Minutes | 10-20% |
| **L2: Segment-based** | "As a [plan] subscriber..." | Hours | 20-40% |
| **L3: Behavior-triggered** | "You viewed [product]" | Days | 40-80% |
| **L4: Predictive/content** | "Based on your browsing..." | Weeks | 2-5x |

### Personalization Data Sources

- **CRM fields**: name, company, role, plan tier, signup date
- **Behavioral**: pages viewed, emails clicked, purchases, support tickets
- **Transactional**: order history, AOV, LTV, churn risk score
- **Survey/enrichment**: industry, goals, challenges (from onboarding)

### Merge Tag Inventory

```
{first_name}       — Required. Always have a fallback ("Friend").
{company}          — B2B sequences.
{product_name}     — Referenced product or last purchased item.
{order_value}      — Transactional and upsell sequences.
{account_created}  — Number of days since signup.
{last_login}       — Number of days since last activity.
{plan_name}        — Current pricing tier.
{lead_magnet}      — What they downloaded.
{city}             — For localized events.
```

## A/B Testing Emails

Test one variable per experiment. Let statistical significance (95% confidence) decide.

### What to Test (Ranked by Impact)

| Variable | Typical Lift | Sample Size Needed | Notes |
|----------|-------------|-------------------|-------|
| Subject line | 10-40% | 500-1000 per variant | Test 2-3 variants |
| Preview text | 5-15% | 300-500 | Most underused lever |
| CTA copy / button | 10-25% | 500-1000 | "Get started" vs "Claim now" |
| Send time | 5-20% | 1000+ | Timezone-aware |
| From name | 5-15% | 500 | Person vs brand |
| Offer / discount | 20-50% | 2000+ | 10% vs 20% off |
| Body copy length | 5-10% | 500 | Short vs long |
| Images | 5-15% | 500 | With vs without images |

### A/B Testing Rules

- **Statistical significance**: 95% confidence minimum before declaring a winner
- **Sample size**: minimum 100 opens per variant for subject lines, 500 for body tests
- **Traffic split**: 50/50 for initial split, then 10-20% test / 80-90% control for champion/challenger
- **Duration**: run for at least one full business cycle (7 days) to account for day-of-week effects
- **One variable at a time**: testing subject line AND CTA simultaneously means you don't know what moved the needle
- **Document results**: keep a testing log with hypothesis, result, and next action
- **Winner gets promoted** to control; loser gets archived

## Deliverability Optimization

Your sequence is worthless if it lands in spam. Deliverability is infrastructure, not strategy.

### Core Deliverability Checklist

- [ ] Domain authenticated with SPF, DKIM, and DMARC
- [ ] Custom sending domain (not shared) for transactional and marketing
- [ ] Dedicated IP or reputable shared pool
- [ ] Warm-up schedule for new sending infrastructure (2-4 weeks)
- [ ] List hygiene: remove hard bounces immediately, soft bounces after 3 tries
- [ ] Engagement-based sunset policy: 90 days no open = suppress
- [ ] Plain-text version included in every email
- [ ] Text-to-image ratio: 60%+ text
- [ ] Link-to-text ratio: no more than 1 link per 100 words
- [ ] Spam score: below 4 on mail-tester.com before every major send
- [ ] Seed testing: send to Gmail, Outlook, Yahoo, and Apple before blast

### Common Blocking Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| Low sender reputation | Spam folder placement | Warm IP, reduce volume, clean list |
| Spam trap hits | Hard bounces on clean addresses | Remove stale/inactive contacts |
| Poor engagement | Gmail tab placement | Re-engagement or sunset sequence |
| DMARC policy | Emails quarantined | Start with p=none, move to p=quarantine |
| List source quality | High unsubscribe rate | Double opt-in, verification gate |
| Too many images | Spam folder | 60%+ text ratio, 1 image per 500 words |

### Sending Infrastructure Decisions

| Volume | Setup | Monthly Cost |
|--------|-------|-------------|
| <10K/mo | Transactional provider (SendGrid free, Amazon SES) | $0-15 |
| 10K-100K/mo | Dedicated email service (Klaviyo, Mailchimp) | $30-150 |
| 100K-1M/mo | Dedicated IP + ESP (SendGrid Pro, Postmark) | $150-500 |
| 1M+/mo | Private infrastructure + deliverability consultant | $2K-10K |

## Segmentation Strategies

Segmentation turns one-size-fits-all sequences into personalized revenue machines.

### Core Segments

| Segment | Criteria | Strategy | Revenue Impact |
|---------|----------|----------|---------------|
| New subscribers | <30 days since signup | Welcome sequence | Immediate conversion |
| Active engaged | Open rate >30%, click rate >5% | Core nurture, cross-sell | Baseline revenue |
| Moderate engaged | Open 15-30%, click 2-5% | Re-engagement or frequency increase | Recovery |
| Dormant | No open in 60+ days | Re-engagement or suppress | List quality |
| Buyers | Completed purchase | Upsell, replenish, loyalty | Repeat revenue |
| Cart abandoners | Cart created, no purchase | Cart recovery | Recovery revenue |
| High-value (VIP) | Top 20% by LTV | Exclusive content, early access | Retention |
| Trial users | Active trial, not converted | Trial conversion | Activation |

### Segmentation Rules

- Start with 3 segments and expand as data grows
- Tag from day one: source, interest, behavior, plan tier
- Re-evaluate segments quarterly against actual performance
- A segment must be at least 500 contacts to justify a dedicated sequence
- Over-segmentation kills action: if you can't write a different email, you don't need a different segment

## Automation Triggers

### Trigger Types

| Type | Example | When to Use |
|------|---------|-------------|
| Time-delayed | "3 days after signup" | Welcome, onboarding |
| Behavioral | "Viewed pricing page" | Nurture, sales alert |
| Transactional | "Order confirmed" | Post-purchase |
| Date-based | "Birthday, anniversary" | Loyalty, retention |
| Score-based | "Lead score >50" | Sales handoff |
| Event-based | "Webinar attended" | Event follow-up |
| Inactivity | "90 days no open" | Re-engagement |

### Trigger Sequencing

```
Signup → Welcome series (time-delayed)
  ├── [If purchase] → Post-purchase → Onboarding
  ├── [If 60 days no purchase] → Abandonment / re-engagement
  └── [If 90 days no open] → Re-engagement → Suppress

Cart create → Cart recovery (time-delayed)
  └── [If purchase] → Post-purchase → Upsell

Form submit → Nurture funnel (time-delayed)
  ├── [If 3+ clicks] → Sales alert → Call booked → Post-call
  └── [If 90 days inactive] → Re-engagement → Suppress
```

## Output Format

On completion: "[N]-email sequence created for [goal], expected [N]% conversion on [N] subscribers = $[N] revenue"

## When to Use

**Trigger phrases:**
- "email sequences"
- "Building marketing campaigns and funnels"
- "Optimizing conversion and retention"
- "Scaling acquisition channels"
- "Welcome series / nurture funnel / re-engagement"

## When NOT to Use

- Task is about ad campaigns, not email (use paid-ads or marketing-ops)
- Task is about landing page copy or content (use content-creator)
- Task requires SMS or push notifications (use other skills)
- You need ESP/platform setup (use SaaS documentation)

## Common Patterns

1. **Lead magnet → nurture → sale**: The foundational funnel. Free content → relationship → offer.
2. **Trial → onboarding → conversion**: SaaS standard. Activate → demonstrate value → upgrade.
3. **Purchase → upsell → loyalty**: Post-purchase sequence that builds LTV.
4. **Webinar/event → follow-up → sale**: Capitalize on event momentum within 24 hours.
5. **Inactivity → re-engagement → suppress**: Clean out the dead weight quarterly.

## Red Flags

- **Open rates below 15%**: Subject lines or sender reputation issue — check deliverability fundamentals
- **Click rates below 1%**: Offer or CTA disconnect — review value proposition
- **Unsubscribe rate above 0.5% per send**: Audience targeting or frequency problem
- **Spam complaints above 0.1%**: List quality or permission issue — investigate source
- **Deliverability below 95%**: Authentication, reputation, or content issues
- **Sequence conversion flat for 30+ days**: Refresh creative or segment
- **No re-engagement running**: Dormant list growing — start a cleanup today

## Anti-Rationalization Table

| Excuse | Truth |
|--------|-------|
| "I need a bigger list first" | Start with 100 emails today |
| "I'll write the emails later" | Templates above work NOW |
| "Email is dead" | $42 ROI per $1 spent — highest of any channel |
| "I don't know how to segment" | Start with buyers vs non-buyers |
| "Automation is too complex" | One trigger → one email → one goal |
| "I'll design sequences after launch" | Build sequences before you have subscribers |

## Verification

- Sequence fires correctly from each trigger condition
- All merge tags render with fallback values
- Unsubscribe link present and functional in every email
- Plain-text version matches HTML content
- Links resolve to correct destinations with UTM parameters
- Email renders in Gmail, Outlook, and Apple Mail
- Spam score below 4 on mail-tester.com
- Exit/removal logic terminates sequences on conversion
- Test sends reach inbox, not spam
- Re-engagement sequence leads to suppression, not infinite emails


## Workflow
See the parent skill for authoritative workflow documentation.
