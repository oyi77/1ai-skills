---
name: marketing-ops
description: |
  >
    Complete AI-powered marketing & sales operating system for solo founders.
    Covers the full revenue lifecycle: customer research, content creation,
    SEO/GEO/SMO optimization, paid ads, email sequences, sales enablement,
    CRO, pricing, retention, analytics, automation, and global expansion.
    Includes stage-based playbooks ($0→$100K MRR), AI agent orchestration,
    PLG frameworks, Indonesia e-commerce, and decision-making infrastructure.
    Use whenever the user mentions marketing, ads, SEO, content strategy,
    campaigns, social media, email, copywriting, landing pages, conversions,
    growth, funnels, brand voice, ad copy, ROAS, CPC, CTR, lead gen,
    sales, pricing, churn, retention, partnerships, or any revenue task.
    Triggers on: "write a blog post," "plan a campaign," "audit my landing page,"
    "create email sequence," "keyword research," "ad copy," "content calendar,"
    "help me get customers," "grow my business," "increase revenue."
---


# Marketing Ops — AI CMO for Solo Founders

One AI-powered system that runs your entire marketing & sales operation
so you can focus on building product. 4-layer architecture with shared
context, auto-chaining orchestrator, and feedback loops that learn.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 0: OPERATING SYSTEM                               │
│  Stage playbook · Decision engine · AI agent orchestration│
├──────────────────────────────────────────────────────────┤
│  LAYER 1: FOUNDATION                                     │
│  marketing-profile.yml · brand-voice.md · persona.md     │
├──────────────────────────────────────────────────────────┤
│  LAYER 2: RESEARCH                                       │
│  Customer research · Keywords · Competitors · Psychology │
├──────────────────────────────────────────────────────────┤
│  LAYER 3: EXECUTION                                      │
│  Create · Optimize · Sell · Scale                        │
├──────────────────────────────────────────────────────────┤
│  LAYER 3.5: EXECUTION ENGINE (AUTO-REVIEW + SEND)        │
│  AI drafts → AI quality-gate reviews → AI executes       │
│  Gmail auto-drafts · Calendar auto-scheduling ·          │
│  Ad auto-optimization · Content auto-publishing          │
├──────────────────────────────────────────────────────────┤
│  LAYER 4: FEEDBACK & RETENTION                           │
│  Analytics · Attribution · Retention · RevOps · Reviews  │
└──────────────────────────────────────────────────────────┘
```

**Critical principle:** Every mode ends with DOING, not just MAKING.
The execution engine auto-reviews every draft against quality gates
(brand voice, personalization, CTA, spam check, platform fit).
If it passes → auto-execute. If it fails → flag for human review.
Read `references/execution-engine.md` for the full auto-review framework.

---

## First Use: Start Here

Say `/marketing-ops setup`. The onboarding guide (`references/onboarding.md`)
walks you through an interactive conversation:

1. **Business Identity** (2 min) — name, product, ICP, differentiator
2. **Brand Voice** (1 min) — personality, tone, formality level
3. **Stage Assessment** (1 min) — MRR, customers, current channels
4. **Auto-Send Setup** (5 min) — configure Gmail auto-sender
5. **Lead Sources** (2 min) — where to find prospects

Generates: `marketing-profile.yml`, `brand-voice.md`, `persona.md`
Then recommends your first actions based on your stage.

If unsure where to start, say `/marketing-ops help` for guided paths.

---

## Command Reference

- Configure agent, analytics, audit, automation, based settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Layer 0 — Operating System
| Command | Reference | Purpose |
|---------|-----------|---------|
| `setup` | `onboarding.md` | Guided first-time setup: profile, voice, auto-send config |
| `help` | `onboarding.md` | Show all commands and guided workflow paths |
| `stage` | `stage-playbook.md` | What to do NOW at your MRR stage |
| `decide` | `decision-engine.md` | Channel selection, ICE scoring, priority matrix |
| `agents` | `ai-agents.md` | Configure AI agent team architecture |
| `review` | templates/`review-template.md` | Weekly/monthly/quarterly reviews |
| `execute` | `execution-engine.md` | Run daily marketing routine (auto-review + auto-send) |
| `daily` | `execution-engine.md` | Full auto-pilot: prospect → draft → review → SEND |

### Layer 2 — Research
| Command | Reference | Purpose |
|---------|-----------|---------|
| `research` | `customer-research.md` | Interviews, review mining, JTBD, surveys |
| `compete` | `compete.md` | Competitor profiling, SWOT, content gaps |
| `seo keywords` | `seo.md` | Keyword research with intent mapping |
| `psychology` | `psychology.md` | 50+ mental models for persuasion |
| `pmf` | `pmf-validation.md` | Product-market fit: signal detection, demand tests, Sean Ellis, pivot framework |

### Layer 3 — Create
| Command | Reference | Purpose |
|---------|-----------|---------|
| `content` | `content.md` | Blog, landing pages, video scripts |
| `copywrite` | `copywriting.md` | 8 formulas, 30 headlines, CTA optimization |
| `email` | `email.md` | Welcome/nurture/launch/winback sequences |
| `social` | `social.md` | Calendars, posts, video strategy |
| `ads` | `ads.md` | Paid campaign strategy |
| `adcopy` | `adcopy-optimization.md` | Ad copy testing (3×3×3 framework) |
| `campaign` | `campaign.md` | Plans, briefs, launch playbooks |
| `brand` | `brand.md` | Voice, messaging, taglines |
| `influencer` | `influencer.md` | KOL, UGC, creator partnerships |
| `calendar` | scripts/`content_calendar.py` | Generate content calendar CSV |

### Layer 3 — Optimize
| Command | Reference | Purpose |
|---------|-----------|---------|
| `seo` | `seo.md` | Technical audits, on-page, schema |
| `geo` | `ai-optimization.md` | AI citation optimization (GEO/AEO) |
| `smo` | `smo.md` | Algorithm-level social optimization |
| `cro` | `cro.md` | 50-point page audit, A/B testing |
| `pseo` | `programmatic-seo.md` | Scaled content from templates |
| `plg` | `plg.md` | Product-led growth, activation, viral loops |

### Layer 3 — Sell
| Command | Reference | Purpose |
|---------|-----------|---------|
| `sales` | `sales.md` | Outbound, demos, objections, proposals |
| `pricing` | `pricing.md` | Models, tiers, value-based, testing |
| `crm` | `crm-pipeline.md` | Pipeline, lead scoring, handoff |
| `prospect` | `prospecting.md` | Auto-find leads: web scrape, social mine, qualify, enrich |
| `partnerships` | `partnerships.md` | Affiliates, co-marketing, integrations |

### Layer 3 — Scale
| Command | Reference | Purpose |
|---------|-----------|---------|
| `growth` | `growth-attribution.md` | $0-budget tactics, outreach |
| `global` | `global-markets.md` | 20+ market guides, international SEO |
| `localize` | `localization-compliance.md` | WhatsApp, compliance, UMKM |
| `indonesia` | `indonesia-ecommerce.md` | Shopee/Tokopedia/TikTok Shop, Ramadan |
| `community` | `community-growth.md` | CLG, Reddit, dark social, BIP |
| `launch` | `developer-launch.md` | Product Hunt, GitHub, HN, AppSumo |
| `automate` | `automation.md` | Workflows, tech stack |
| `tracking` | `tracking.md` | GA4, GTM, UTMs, pixels |
| `calculate` | scripts/`ad_calculator.py`, `unit_economics.py` | ROI + unit economics |

### Layer 4 — Feedback & Retention
| Command | Reference | Purpose |
|---------|-----------|---------|
| `analytics` | `analytics.md` | KPI dashboards, attribution, reporting |
| `retention` | `retention.md` | Churn prevention, NPS, win-back |
| `revops` | `revops.md` | Lead scoring, deliverability, stack audit |

**Before any mode: read the corresponding reference file.**

---

## Orchestrator: Auto-Chaining

- Configure agent, analytics, audit, automation, based settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### "Set up my revenue engine from scratch"
```
1. stage → Assess current stage, set priorities
2. research → Customer interviews + review mining
3. brand → Voice, positioning, messaging
4. pricing → Model, tiers, packaging
5. content → Landing page + 5 blog posts
6. seo + geo → Optimize for search + AI citations
7. email → Welcome + nurture + sales sequences
8. sales → Outbound templates, demo script, proposals
9. tracking → GA4, UTMs, conversion events
10. automate → Lead processing + follow-up workflows
11. retention → Onboarding + churn prevention + referral
```

### "Launch this product"
```
compete → campaign → content → email → adcopy → social → tracking
```

### "I need more customers"
```
stage → decide (pick channel) → growth → content → seo → community
```

### "My conversions are low"
```
cro → psychology → adcopy → copywrite → pricing
```

### "Expand to Indonesia"
```
localize → indonesia → global → pricing (IDR) → social (WhatsApp/IG)
```

---

## Feedback Loop

When user shares results:
1. Record what was tested and what happened
2. Identify the insight (why it worked/failed)
3. Apply forward to next similar task
4. Suggest updating Layer 1 files if learning is significant

---

## Adaptive Behavior

- **Language:** Generate in profile/user language
- **Stage:** Recommendations filtered by MRR stage
- **Industry:** Tone, compliance, channels adapt to industry
- **Funnel:** Content tagged TOFU/MOFU/BOFU/Post-purchase
- **Framework auto-select:** PAS for ads, AIDA for landing pages, BAB for
  case studies, PASTOR for long-form sales

---

## Scripts & Templates

**Scripts** (`scripts/`):
- `content_calendar.py` — CSV content calendar
- `ad_calculator.py` — Ad spend & ROI projections
- `seo_audit.py` — SEO audit report template
- `unit_economics.py` — LTV, CAC, payback, PLG funnel calculator

**Templates** (`templates/`):
- `marketing-profile.yml` — Business context (Layer 1)
- `brand-voice.md` — Voice guidelines
- `persona.md` — Audience persona
- `review-template.md` — Weekly/monthly/quarterly review + OKRs

---

## Quick Start

```
/marketing-ops setup          # 5-min onboarding (do this once)
/marketing-ops stage          # What should I focus on right now?
/marketing-ops daily          # Full auto-pilot: draft → review → SEND
```

### Setup Auto-Send (One-Time, 10 Minutes)

The skill auto-reviews every draft. To make it also auto-SEND,
set up one of these (see execution-engine.md for full instructions):

1. **Google Apps Script** (free) — auto-sends any Gmail draft with
   "[AUTO-SEND]" in the subject. Skill adds the prefix, script sends it.
2. **MailerLite MCP** (connect from MCP registry) — direct send for
   email sequences and campaigns.
3. **Zapier/Make** — "new draft with label → send → delete draft"

### After Setup: The Fully Autonomous Daily Routine

```
/marketing-ops daily

→ AI searches web for 10-15 prospects matching your ICP
→ AI auto-qualifies and picks top 5 (scored against persona.md)
→ AI finds their email/contact (pattern matching + web research)
→ AI drafts personalized outreach for each prospect
→ AI self-reviews against 8-point quality gate
→ Passed emails auto-sent via [AUTO-SEND] (zero clicks)
→ Failed emails held as drafts for your review
→ Follow-ups auto-sent on schedule (Day 3, Day 7 breakup)
→ Hot lead replies auto-responded with calendar link
→ Social posts prepared, ads optimized, pipeline tracked
→ You get a summary: "5 sent, 2 follow-ups, 1 demo booked"

YOUR TIME: 3 minutes reading summary + demo calls.
AI does: prospecting, researching, writing, reviewing, sending.
```

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Verification

- Run A/B test with control group before full rollout
- Verify tracking pixels fire correctly on all conversion pages
- Check UTM parameters parse correctly in analytics dashboard
- Confirm email deliverability via seed list test
- Validate landing page speed (target < 3s load time)
