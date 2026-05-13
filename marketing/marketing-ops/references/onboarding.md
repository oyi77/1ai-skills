# Onboarding Guide

Welcome to Marketing Ops. This guide walks you through everything from
first install to fully autonomous daily marketing in under 30 minutes.

---

## Step 1: Foundation Setup (5 minutes)

When the user says `/marketing-ops setup` or is using the skill for the
first time, walk them through this interactive conversation:

### 1.1 Business Identity
Ask these questions one at a time (not all at once):

```
"Let's set up your marketing profile. This takes ~5 minutes and makes
everything I create much more targeted."

Q1: "What's your business name and website?"
Q2: "In one sentence, what do you sell?"
Q3: "Who is your ideal customer? (role, company size, industry)"
Q4: "What problem do you solve for them?"
Q5: "What makes you different from alternatives?"
Q6: "What's your price? (or price range)"
Q7: "Who are your top 2-3 competitors? (names or URLs)"
```

### 1.2 Brand Voice
```
Q8: "Pick 3 words that describe how your brand should sound:"
    (Examples: professional, friendly, bold, technical, casual,
    authoritative, playful, warm, direct, witty)

Q9: "Pick 3 words your brand should NEVER sound like:"
    (Examples: corporate, salesy, boring, aggressive, childish)

Q10: "How formal should your writing be? (1=very casual, 5=very formal)"
```

### 1.3 Current Stage
```
Q11: "What's your current monthly revenue? (even $0 is fine!)"
Q12: "How many paying customers do you have?"
Q13: "Which channels are you currently using for marketing?"
     (social media, email, ads, content, nothing yet — all fine)
```

### 1.4 Save & Configure
After collecting answers, generate three files:

1. **`marketing-profile.yml`** — from template, filled with their answers
2. **`brand-voice.md`** — from template, with their tone choices + examples
3. **`persona.md`** — from template, with their ICP description

```
"Done! I've created your marketing foundation:
 ✅ marketing-profile.yml — your business identity
 ✅ brand-voice.md — how your brand sounds
 ✅ persona.md — who you're marketing to

 These files power everything else. Let's set up execution next."
```

---

## Step 2: Auto-Send Setup (10 minutes)

Walk the user through setting up autonomous email sending:

```
"To make marketing fully autonomous, we need to set up auto-sending.
 Right now I can draft emails, but I need a bridge to send them.
 Pick your preferred option:"

Option A: Google Apps Script (Free, 10 min)
  1. Go to script.google.com
  2. Create a new project
  3. Paste the auto-sender code (I'll give it to you)
  4. Set up a 5-minute timer trigger
  5. Done — any draft I create with [AUTO-SEND] gets sent automatically

Option B: Connect MailerLite MCP (5 min)
  1. Go to Claude Settings → Connected Apps
  2. Search "MailerLite" → Connect
  3. Done — I can send emails directly through MailerLite

Option C: Zapier/Make (5 min, may have cost)
  1. Create a Zap: "New Gmail draft with label → Send → Delete draft"
  2. Done

"Which would you like to set up?"
```

If they choose Option A, provide the complete Apps Script code from
execution-engine.md and walk them through each step.

---

## Step 3: Lead Source Setup (5 minutes)

```
"Last step: where should I find people to contact?
 I need target prospects to send outreach to.
 Here are your options:"

A. "Give me a list" — user provides a CSV/spreadsheet of contacts
B. "I'll find them" — AI prospects using web search + ICP criteria
C. "Use my existing contacts" — scan Gmail for warm leads to re-engage
D. "All of the above" — combine all sources

"Which approach works best for you?"
```

Save their preference to marketing-profile.yml under `lead_sources:`.

---

## Step 4: Confirmation & First Run

```
"Setup complete! Here's what's configured:

 📋 Business Profile: {company name} — {one-line description}
 🎤 Brand Voice: {3 adjectives}, {formality level}/5
 🎯 Target Customer: {ICP description}
 📧 Auto-Send: {method chosen} ✅
 🔍 Lead Sources: {sources chosen}
 📊 Current Stage: {stage} (${MRR} MRR)

 Based on your stage, here's what I recommend focusing on:
 {stage-specific recommendations from stage-playbook.md}

 Ready to run your first daily marketing routine?
 Just say: /marketing-ops daily"
```

---

## Command Quick Reference (Show When Asked)

When a user asks "what can you do?" or "help" or "show commands":

```
🚀 GETTING STARTED
  /marketing-ops setup          Set up your profile (first time)
  /marketing-ops stage          What to focus on at your MRR stage
  /marketing-ops daily          Run autonomous daily marketing

📊 STRATEGY
  /marketing-ops decide         Which channel to invest in
  /marketing-ops pmf            Validate product-market fit
  /marketing-ops agents         Configure AI agent architecture
  /marketing-ops review         Weekly/monthly/quarterly reviews

✍️ CREATE
  /marketing-ops content        Blog posts, landing pages, scripts
  /marketing-ops copywrite      Headlines, CTAs, formulas
  /marketing-ops email          Welcome/nurture/launch sequences
  /marketing-ops social         Social media posts & calendars
  /marketing-ops ads            Paid campaign strategy
  /marketing-ops adcopy         Ad copy testing (3×3×3)
  /marketing-ops campaign       Full campaign plans

📈 OPTIMIZE
  /marketing-ops seo            SEO audits & keyword research
  /marketing-ops geo            AI citation optimization (GEO/AEO)
  /marketing-ops cro            Landing page conversion audit
  /marketing-ops plg            Product-led growth setup

💰 SELL
  /marketing-ops sales          Outbound, demos, objections, proposals
  /marketing-ops pricing        Pricing strategy & testing
  /marketing-ops prospect       Find & qualify target leads
  /marketing-ops partnerships   Affiliates, co-marketing, integrations

🌏 SCALE
  /marketing-ops growth         $0-budget growth tactics
  /marketing-ops community      Reddit, dark social, building in public
  /marketing-ops launch         Product Hunt, GitHub, HN, AppSumo
  /marketing-ops indonesia      Shopee/Tokopedia/TikTok Shop + Ramadan
  /marketing-ops global         20+ market expansion guides

📊 MEASURE
  /marketing-ops analytics      KPI dashboards & reporting
  /marketing-ops retention      Churn prevention & NPS
  /marketing-ops revops         Lead scoring, attribution, stack audit
  /marketing-ops calculate      Unit economics & ROI calculator
```

---

## Guided Workflows (For Users Who Don't Know Where to Start)

When a user seems unsure, offer guided paths:

```
"I can see you're just getting started. Here are three paths —
 pick the one that matches your situation:"

PATH 1: "I have an idea but no customers yet"
  → pmf → research → brand → pricing → sales (manual outreach)
  "Let's validate your idea and find your first paying customer."

PATH 2: "I have a few customers but need more"  
  → stage → decide → daily (auto-outreach) → content → seo
  "Let's identify your best channel and scale it."

PATH 3: "I have customers but they're churning"
  → retention → cro → email (re-engagement) → research
  "Let's fix the leaky bucket before pouring in more water."

"Which path sounds like you?"
```

---

## Post-Onboarding: What Happens Every Day

After setup is complete, the `/marketing-ops daily` command runs this flow
automatically every time the user invokes it:

```
Day 1:  Prospect 5 leads → Draft outreach → Quality gate → Auto-send
Day 2:  Prospect 5 new + follow up Day 1 → Auto-send
Day 3:  Prospect 5 new + follow up Day 1 (2nd touch) → Auto-send
Day 7:  Follow up Day 1 (breakup email) → Auto-send
Day 8:  Prospect 5 new + check for responses → Triage
...

WEEKLY: 25 outreach emails + 10 follow-ups + social posts + ad optimization
MONTHLY: 100+ outreach emails + content published + pipeline growing
```

The system compounds. Week 1 is 25 contacts. By Week 4 you have 100
contacts in your pipeline at various stages. By Month 3, responses
and demos start stacking up.
