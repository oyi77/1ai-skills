# RevOps-Lite for Solo Founders

Revenue Operations connects marketing → sales → customer success into
one unified revenue system. Companies with aligned RevOps grow 12-15% faster.
This is the simplified solo-founder version.

---

## The RevOps Funnel (Unified View)

```
MARKETING              SALES                 CUSTOMER SUCCESS
─────────              ─────                 ────────────────
Visitor → Lead → MQL → SQL → Opportunity → Customer → Expand → Advocate
                  ↑                           ↑
            Lead scoring              Retention workflows
            auto-qualifies            prevent churn
```

**The problem without RevOps:** 20-30% of qualified leads never receive
follow-up due to routing failures, handoff gaps, or data issues.
That's revenue evaporating.

---

## Lead Scoring Model (Simplified)

### Demographic Score (0-50 points)
| Signal | Points |
|--------|--------|
| Job title = decision maker (CEO, VP, Director) | +15 |
| Job title = influencer (Manager, Lead) | +10 |
| Company size in target range | +10 |
| Target industry | +10 |
| Target geography | +5 |
| Personal email (gmail, yahoo) | -10 |
| Student / intern title | -15 |
| Competitor email domain | -20 |

### Behavioral Score (0-50 points)
| Action | Points | Decay |
|--------|--------|-------|
| Visited pricing page | +15 | -5 after 14 days |
| Requested demo / free trial | +20 | -5 after 7 days |
| Downloaded lead magnet | +10 | -3 after 30 days |
| Opened 3+ emails in 7 days | +8 | Reset if inactive 14 days |
| Returned to site 3+ times | +10 | -3 after 14 days |
| Viewed comparison/vs page | +12 | -5 after 14 days |
| Filled contact form | +15 | No decay |
| Attended webinar/event | +8 | -3 after 30 days |
| Unsubscribed from email | -15 | Permanent |
| No engagement 30 days | -10 | Resets on re-engagement |

### Score → Action Routing
```
80-100 (HOT):   → Immediate personal outreach (within 1 hour)
50-79 (WARM):   → Automated sales sequence + alert to you
25-49 (COOL):   → Marketing nurture sequence
0-24 (COLD):    → Long-term nurture or dormant
Negative:        → Remove from active lists
```

---

## Pipeline Stage Definitions

Each stage needs clear entry criteria and exit actions:

| Stage | Entry Criteria | Exit Action | Max Days |
|-------|---------------|-------------|----------|
| **Lead** | Provided contact info | Score ≥ 25 → MQL | 7 |
| **MQL** | Score ≥ 50 OR high-intent action | You review → Accept/Reject | 3 |
| **SQL** | You confirmed: real need + budget + authority | Discovery call scheduled | 5 |
| **Opportunity** | Discovery done, mutual interest | Proposal sent | 14 |
| **Proposal** | Proposal delivered | Accepted or declined | 10 |
| **Closed Won** | Contract signed / payment received | Onboarding starts | — |
| **Closed Lost** | Deal declined or went silent | Record reason, add to win-back | — |

**Stale deal rule:** If a deal sits in any stage past its max days with no
activity, auto-flag for attention or move to next review.

---

## Email Deliverability Management

### Setup Checklist (Do Once)
- [ ] **SPF record** — authorize your email sending domains
- [ ] **DKIM record** — sign outgoing emails cryptographically
- [ ] **DMARC record** — policy for handling auth failures
- [ ] **Custom sending domain** — send from you@yourdomain.com, not @gmail
- [ ] **Warm-up new domain** — start with 20 emails/day, increase 20% daily for 2 weeks
- [ ] **Dedicated IP** — only if sending 50K+ emails/month

### Ongoing Maintenance
- [ ] Monitor bounce rate weekly (hard bounces > 2% = problem)
- [ ] Check spam complaint rate (> 0.1% = danger zone)
- [ ] Clean list monthly (remove 90-day inactives)
- [ ] Use double opt-in for new subscribers
- [ ] Never buy email lists (destroys deliverability)
- [ ] Segment sends by engagement (don't email cold subscribers)
- [ ] Check domain reputation: Google Postmaster Tools

### Deliverability Metrics
| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Delivery rate | >98% | 95-98% | <95% |
| Bounce rate | <1% | 1-3% | >3% |
| Spam complaint rate | <0.05% | 0.05-0.1% | >0.1% |
| Inbox placement | >85% | 70-85% | <70% |

---

## MarTech Stack Governance

### The Stack Audit (Run Quarterly)

For every tool in your stack, evaluate:

```
| Tool | Monthly Cost | How Often Used | Could AI Replace? | Action |
|------|-------------|---------------|-------------------|--------|
| {tool} | ${cost} | Daily/Weekly/Rarely | Yes/No/Partially | Keep/Cut/Replace |
```

### Decision Matrix
| | Used Frequently | Used Rarely |
|---|---|---|
| **High Value** | KEEP and optimize | EVALUATE — are you using it right? |
| **Low Value** | REPLACE with cheaper/AI option | CUT immediately |

### Solo Founder Stack Ceiling
- Total tool spend should be < 5% of MRR
- If MRR = $5K, max tool spend = $250/month
- Free tiers exist for almost everything until $10K MRR
- Count the tools: if you have >10 paid tools at Stage 1-2, you have too many

---

## Unit Economics Dashboard

### The 7 Numbers Every Solo Founder Must Know

```
1. MRR (Monthly Recurring Revenue)
   = Sum of all active subscriptions

2. CAC (Customer Acquisition Cost)
   = Total marketing + sales spend ÷ New customers
   Target: < LTV/3

3. LTV (Customer Lifetime Value)
   = ARPU ÷ Monthly churn rate
   Example: $79/mo ÷ 5% churn = $1,580 LTV

4. LTV:CAC Ratio
   = LTV ÷ CAC
   Target: > 3:1

5. Payback Period
   = CAC ÷ Monthly ARPU
   Target: < 12 months

6. Monthly Churn Rate
   = Customers lost ÷ Customers at start of month
   Target: < 5% (B2B SaaS), < 8% (B2C)

7. Net Revenue Retention (NRR)
   = (Start MRR + Expansion - Contraction - Churn) ÷ Start MRR
   Target: > 100% (>110% = excellent)
```

### Quick Health Check
```
□ LTV:CAC > 3:1?          YES → Healthy  |  NO → Fix CAC or churn
□ Payback < 12 months?    YES → Healthy  |  NO → Raise prices or lower CAC
□ Monthly churn < 5%?     YES → Healthy  |  NO → Focus on retention
□ NRR > 100%?             YES → Growing  |  NO → Add expansion revenue
```

---

## Multi-Touch Attribution (Simplified)

### For Solo Founders: Self-Reported + UTM Hybrid

Don't overcomplicate attribution. Use this pragmatic approach:

**1. UTM tracking on everything** (free, accurate for click-through)
**2. "How did you hear about us?" field** on signup/purchase form
**3. Correlate the two** — UTM shows last click, self-reported shows true source

### Common Attribution Findings
| What UTM Says | What Customer Says | Real Attribution |
|--------------|-------------------|-----------------|
| Google organic | "I saw your post on LinkedIn" | LinkedIn → Google search → Signup |
| Direct | "A friend told me" | Word of mouth (dark social) |
| facebook/cpc | "I've been following you for months" | Long nurture → ad triggered action |

**The lesson:** First touch matters more than last click for understanding
what's actually driving awareness. Track both.
