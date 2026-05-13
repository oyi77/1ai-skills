# Product-Led Growth (PLG) Reference

Your product IS your marketing. PLG companies trade at 2x the revenue multiples
of sales-led companies because growth is built into the product itself.

---

## PLG vs Sales-Led

| Dimension | Product-Led | Sales-Led |
|-----------|-----------|-----------|
| How users start | Self-serve (free trial/freemium) | Talk to sales |
| Conversion driver | Product experience | Sales team |
| CAC | Lower (product does the selling) | Higher (human sales cost) |
| Growth ceiling | Higher (scales with product) | Lower (scales with headcount) |
| Time to value | Minutes to hours | Days to weeks |
| Best for | <$500/mo ACV, wide audience | >$1000/mo ACV, enterprise |

### Can You Do PLG?
PLG works best when: product solves an immediate pain, value is obvious quickly,
users can self-onboard, and the market is large enough for volume.

---

## The PLG Funnel

```
ACQUIRE        ACTIVATE         ENGAGE          MONETIZE        EXPAND
──────         ────────         ──────          ────────        ──────
Free trial  →  "Aha moment" →  Regular use  →  Convert to   →  Upgrade /
or freemium    (first value)    (habit)         paid plan       Team / Refer
```

### Key Metrics Per Stage

| Stage | Metric | Formula | Good Target |
|-------|--------|---------|-------------|
| Acquire | Signup rate | Signups ÷ Visitors | 3-8% |
| Activate | Activation rate | Activated ÷ Signups | 25-40% |
| Engage | DAU/MAU | Daily users ÷ Monthly users | >20% |
| Monetize | Free-to-paid | Paid ÷ Free users | 3-7% (freemium), 15-25% (trial) |
| Expand | NRR | (Start MRR + Expansion - Churn) ÷ Start | >110% |

---

## Activation (The Most Important Metric)

### Define Your "Aha Moment"
The moment a user first experiences the core value of your product.

**How to find it:**
1. List 10 actions users can take in your product
2. Check which actions correlate with 30-day retention
3. The action with the highest correlation = your activation event
4. Build your entire onboarding around getting users to that action FAST

**Examples:**
- Slack: Sent 2,000 messages as a team
- Dropbox: Put one file in one folder on one device
- Zoom: Completed first video call
- Your product: {define this — it's critical}

### Time to Value (TTV)
How quickly a new user reaches the "aha moment."

```
TTV < 5 minutes  → Excellent (product-led winners)
TTV < 1 hour     → Good (most SaaS)
TTV < 1 day      → Acceptable (complex products)
TTV > 1 week     → Problem (users churn before experiencing value)
```

**Reduce TTV by:**
- Removing signup friction (social login, no credit card)
- Pre-populating with sample data (don't start with empty state)
- Interactive product tour for first 3 critical actions
- Templates and presets that give instant value
- Progress indicators showing how close they are to value

---

## Freemium Strategy

### What Goes Free vs Paid

| Free | Paid |
|------|------|
| Core value (enough to hook) | Advanced features |
| Creates habit + switching cost | Measurable business value |
| Demonstrates product quality | Higher usage limits |
| Generates word-of-mouth | Team/collaboration features |
| Builds audience for upsell | Priority support |

### Freemium Design Rules
1. Free must be genuinely useful (not crippled)
2. Free users should hit natural limits that make upgrading obvious
3. Upgrade path should feel like unlocking, not unblocking
4. Free users are your marketing — they tell others
5. Track: what % of free users hit the upgrade trigger?

---

## Viral Loops

### Types of Virality Built Into Product

**Inherent virality:** Product requires others to use it
- Collaboration tools, messaging, team features
- Example: "Invite your team to this workspace"

**Word-of-mouth virality:** Product is so good people tell others
- Remarkable experience, unexpected delight
- Example: Loom — every video shared exposes new viewers to the product

**Artificial virality:** Incentivized sharing
- "Invite 3 friends, get premium free for a month"
- Referral credits, dual-sided rewards

**Content virality:** Product output gets shared publicly
- "Made with {Product}" watermark on free tier
- Public profiles, shareable reports, embeddable widgets

### Viral Coefficient (K-Factor)
```
K = (Invitations per user) × (Conversion rate of invitations)

K > 1 = Viral growth (each user brings >1 new user)
K = 0.5 = Good supplement to other channels
K < 0.2 = Not a meaningful growth driver

Example:
  Each user invites 5 people × 20% accept = K of 1.0 (viral!)
  Each user invites 2 people × 10% accept = K of 0.2 (not viral)
```

---

## In-Product Growth Levers

### Expansion Revenue Triggers

| Trigger | Upsell Message |
|---------|---------------|
| Hit usage limit | "You've used 90% of your free limit this month" |
| Team growth | "Add team members to collaborate (Team plan)" |
| Advanced feature attempted | "This feature is available on Pro" |
| Success milestone | "You've saved 50 hours! Power users love {feature}" |
| Competitive moment | "Export this report to impress your stakeholders (Pro)" |

### Product-Qualified Leads (PQLs)

PQLs are users whose product behavior indicates buying intent.

**PQL scoring model:**
```
+20  Used product 5+ days in a row
+15  Invited a team member
+15  Hit a usage limit
+10  Viewed pricing page
+10  Used advanced feature (free trial)
+5   Connected an integration
-10  No login in 7 days
-20  No login in 14 days

Score > 50 → Route to sales/upgrade prompt
Score 25-50 → Automated nurture
Score < 25 → Keep in free tier, monitor
```

---

## PLG Unit Economics Calculator

```
Revenue Model:
  Monthly visitors:        {X}
  Signup rate:             {Y}%
  Free signups:            X × Y
  Activation rate:         {Z}%
  Activated users:         Signups × Z
  Free-to-paid rate:       {W}%
  New paid customers:      Activated × W
  Average revenue/user:    ${ARPU}/mo
  New MRR:                 Customers × ARPU
  Monthly churn:           {C}%
  Net new MRR:             New MRR - (Total MRR × C)

Target check:
  CAC = Marketing spend ÷ New paid customers
  LTV = ARPU ÷ Churn rate
  LTV:CAC = should be > 3:1
  Payback = CAC ÷ ARPU (months) — should be < 12
```
