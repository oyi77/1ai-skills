---
name: lead-magnets
description: "Lead magnet design and creation — ebooks, templates, calculators, quizzes matched to audience intent. Use when building lead generation funnels."
domain: marketing
license: Apache-2.0
tags: [growth, lead, magnets, marketing, money, conversions, funnels]
version: "2.0.0"
author: ""
subdomain: ""
type: marketing
---

# Money-Making Overview

A single lead magnet can generate 50-500 new leads/month for years. At 2-10% email-to-customer conversion and $50-500 average order, that's $50-25,000/month from one magnet. Sell lead magnet creation as a $500-5K service to businesses.

## Revenue Streams
1. Lead Magnet Creation ($500-5K/magnet) — design + build for clients
2. Lead Gen Funnels ($2K-10K) — full landing page + email sequence
3. Template Packs ($27-97/set) — sell pre-made magnet templates

## First Action in 60 Minutes
```bash
#!/usr/bin/env bash
# Create a checklist lead magnet in 60 minutes
MAGNET_NAME="10-Point [Topic] Audit Checklist"

echo "# $MAGNET_NAME" > ~/lead-magnet.md
echo "" >> ~/lead-magnet.md
echo "## Point 1: [First thing to check]" >> ~/lead-magnet.md
echo "- [ ] Action item 1" >> ~/lead-magnet.md
echo "- [ ] Action item 2" >> ~/lead-magnet.md
echo "" >> ~/lead-magnet.md
echo "## Point 2: [Second checklist area]" >> ~/lead-magnet.md
echo "- [ ] Action item 1" >> ~/lead-magnet.md
echo "- [ ] Action item 2" >> ~/lead-magnet.md
echo "" >> ~/lead-magnet.md
# Add points 3-10
for i in $(seq 3 10); do
  echo "## Point $i: [Checklist area]" >> ~/lead-magnet.md
  echo "- [ ] Action item" >> ~/lead-magnet.md
  echo "- [ ] Action item" >> ~/lead-magnet.md
  echo "" >> ~/lead-magnet.md
done

echo "=== Lead Magnet Created ==="
echo "Format: Markdown checklist (convert to PDF/Canva)"
echo "Gate: Require email to download"
echo "Expected conversion: 20-40% of visitors → leads"
```

# Lead Magnet Types

## Type Selection

Choose the format that matches your audience's intent:

| Type | Best For | Difficulty | Conversion |
|------|----------|------------|------------|
| Checklist | Quick wins, action-oriented audiences | Low | 20-40% |
| Ebook / Guide | Deep education, complex topics | Medium | 10-25% |
| Template | Practical application, saves time | Low-Medium | 15-35% |
| Calculator / Tool | Interactive value, high perceived worth | High | 25-50% |
| Quiz / Assessment | Personalization, self-discovery | Medium | 30-60% |
| Cheat Sheet | Reference value, learners | Low | 15-30% |
| Email Course | Gradual nurture, relationship building | Low | 20-40% |
| Swipe File | Copywriters, marketers, sales teams | Low | 20-35% |
| Workbook | Implementation, deep engagement | Medium | 10-20% |
| Case Study | Social proof, B2B decision makers | Medium | 15-25% |


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use

**Trigger phrases:**
- "lead magnets"
- "Building marketing campaigns and funnels"
- "Optimizing conversion and retention"
- "Scaling acquisition channels"

- Building marketing campaigns and funnels
- Optimizing conversion and retention
- Scaling acquisition channels

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)

# Creation Workflow

## Content Creation Frameworks

1. Choose magnet type based on audience intent (see type selection table)
2. Outline core value — what specific problem does it solve?
3. Write in 1-2 hours using existing knowledge or curated research
4. Design simple layout (Canva template, Google Doc, or markdown)
5. Create landing page with headline, bullet benefits, email capture form
6. Set up delivery automation (email, download page, or both)
7. Launch to existing audience or $20-50 Facebook traffic test

## Landing Page Design

- Headline states the specific outcome (e.g. "Get Your 10-Point SEO Audit Checklist")
- 3-5 bullet points of what's inside
- Single field email capture (minimize friction)
- Social proof if available (download count, testimonials)
- Clear call-to-action button

## Delivery Automation

- Email autoresponder (Mailchimp, ConvertKit, ActiveCampaign, or similar)
- Download page with direct link
- Optional: drip-feed multi-part magnets over several days
- Tag subscribers by magnet downloaded for future segmentation

## Process

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

```python
# Example: Lead magnet conversion analysis
def analyze_magnet_performance(downloads: int, visitors: int, email_to_sale: float, avg_order: float) -> dict:
    conversion = downloads / max(visitors, 1)
    leads_per_month = downloads
    customers_per_month = int(leads_per_month * email_to_sale)
    monthly_revenue = customers_per_month * avg_order
    return {
        "visitor_to_lead": f"{conversion:.1%}",
        "leads_per_month": leads_per_month,
        "customers_per_month": customers_per_month,
        "monthly_revenue": f"${monthly_revenue:,.0f}",
    }

# Example usage
result = analyze_magnet_performance(
    downloads=200, visitors=1000,
    email_to_sale=0.05, avg_order=75
)
print(result)
```

# Testing & Optimization

## Common Patterns

1. Test with small budgets before scaling
2. Track attribution and ROI religiously
3. A/B test everything — headlines, CTAs, offers

## Conversion Tracking

- Set up tracking pixels on download page
- Tag leads by source magnet
- Monitor email open and click rates for magnet follow-ups
- Track downstream sales attributed to each magnet
- Calculate cost per lead and cost per acquisition per magnet type

## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

# Verification

- [ ] Skill output matches expected behavior

# Additional Resources

- Review the 1ai-skills repository for related marketing skills
- Check the references/ directory for checklists and templates
- Join the community for best practices and support
- Contribute improvements via pull requests

# Anti-Rationalization

| Excuse | Truth |
|---|---|
| "I need a perfect design first" | A markdown checklist works day 1 |
| "Nobody will download it" | Test with $20 Facebook traffic. If <5% convert, iterate |
| "I'll create it when I have more time" | 60 minutes = done. Right now. |

# Output Format

On completion: "[Type] lead magnet created, expected [N]% conversion on [N] visitors = [N] leads/month"
