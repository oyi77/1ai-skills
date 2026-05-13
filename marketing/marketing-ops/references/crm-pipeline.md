# CRM & Lead Pipeline Reference

Inspired by open-source CRM/marketing automation platforms (Twenty, erxes, Mautic).
This reference covers CRM strategy, pipeline design, lead management, and marketing-to-sales handoff.

## Table of Contents
1. [Pipeline Design](#pipeline-design)
2. [Lead Scoring](#lead-scoring)
3. [Contact Segmentation](#contact-segmentation)
4. [Marketing-to-Sales Handoff](#marketing-to-sales-handoff)
5. [Automation Workflows](#automation-workflows)
6. [CRM Hygiene](#crm-hygiene)
7. [Open-Source CRM Options](#open-source-crm-options)

---

## Pipeline Design

### Sales Pipeline Template
Every business needs a pipeline tailored to how their customers actually buy.
Don't copy someone else's pipeline — design yours from how deals actually progress.

**Standard SaaS Pipeline:**
```
Lead → MQL → SQL → Discovery → Demo → Proposal → Negotiation → Closed Won/Lost
```

**E-commerce Pipeline:**
```
Visitor → Browser → Cart → Checkout → Purchased → Repeat → Advocate
```

**Service Business Pipeline:**
```
Inquiry → Qualification → Consultation → Proposal Sent → Follow-up → Contract → Onboarding
```

**Freelancer/Agency Pipeline:**
```
Lead In → Qualifying → Proposal → Negotiation → Signed → In Progress → Invoiced → Paid
```

### Pipeline Design Rules
- Every stage must have a clear **entry criteria** and **exit criteria**
- Stages should represent the buyer's journey, not your internal process
- Keep stages to 5-8 maximum — more causes confusion and stale deals
- Each stage needs a **default action** (what the rep does next)
- Set maximum time limits per stage — deals that stall get flagged or removed
- Track win rate per stage to identify where deals die

### Deal Stage Metrics
| Stage | Measure | Target |
|-------|---------|--------|
| Lead → MQL | Qualification rate | 20-30% |
| MQL → SQL | Acceptance rate | 40-60% |
| SQL → Opportunity | Discovery completion | 50-70% |
| Opportunity → Proposal | Proposal sent rate | 60-80% |
| Proposal → Close | Close rate | 20-40% |
| Overall pipeline | Win rate | 15-25% |

---

## Lead Scoring

### Point-Based Lead Scoring Model

**Demographic/Firmographic Fit (0-50 points)**
| Attribute | High Fit (+10-15) | Medium (+5-8) | Low (+1-3) |
|-----------|-------------------|---------------|------------|
| Job title | Decision maker | Influencer | Individual |
| Company size | Target range | Adjacent | Outside |
| Industry | Target vertical | Related | Unrelated |
| Budget | Stated + sufficient | Unknown | Insufficient |
| Location | Target market | Nearby | Outside |

**Behavioral Signals (0-50 points)**
| Action | Points |
|--------|--------|
| Visited pricing page | +15 |
| Requested demo | +20 |
| Downloaded case study | +10 |
| Opened 3+ emails in 7 days | +8 |
| Returned to site 3+ times | +10 |
| Viewed comparison/vs page | +12 |
| Filled out contact form | +15 |
| Attended webinar | +8 |
| Downloaded whitepaper | +5 |
| Social media engagement | +3 |

**Negative Scoring**
| Signal | Points |
|--------|--------|
| Unsubscribed from email | -15 |
| Competitor email domain | -20 |
| No engagement 30 days | -10 |
| Student/personal email | -5 |
| Job title = student/intern | -10 |

**Lead Grade Thresholds**
- **Hot (80-100):** Route to sales immediately, respond within 1 hour
- **Warm (50-79):** Nurture with sales-ready content, weekly check-in
- **Cool (25-49):** Automated nurture sequence, monthly touchpoint
- **Cold (<25):** Long-term nurture or remove from active pipeline

---

## Contact Segmentation

### Segmentation Dimensions

**By Lifecycle Stage**
- Subscriber → Lead → MQL → SQL → Opportunity → Customer → Evangelist

**By Engagement Level**
- Active (engaged in last 30 days)
- Warm (engaged 30-90 days ago)
- Cold (90-180 days no engagement)
- Dead (180+ days, candidate for removal)

**By Source**
- Organic (SEO, direct)
- Paid (ads, sponsored)
- Referral (word of mouth, affiliate)
- Outbound (cold email, sales outreach)
- Event (webinar, conference, workshop)

**By Behavior**
- Content consumers (blog readers, video watchers)
- Product explorers (free trial, demo requesters)
- Comparison shoppers (pricing page, competitor pages)
- Ready to buy (cart abandoners, proposal viewers)

### Segmentation for Campaign Targeting
```
Segment: "High-Intent Trial Users"
Criteria:
  - Lifecycle = Lead or MQL
  - Signed up for free trial in last 14 days
  - Used product 3+ times
  - NOT yet on paid plan
Action: Send "Why upgrade" email sequence + sales outreach
```

---

## Marketing-to-Sales Handoff

### MQL to SQL Qualification Framework (BANT)
| Criteria | Question | MQL Threshold | SQL Threshold |
|----------|----------|--------------|--------------|
| **Budget** | Can they afford it? | Unknown OK | Confirmed |
| **Authority** | Decision maker? | Influencer OK | Decision maker identified |
| **Need** | Real pain point? | Expressed interest | Articulated specific need |
| **Timeline** | When buying? | No urgency OK | Within quarter |

### Handoff Process
1. Marketing qualifies lead to MQL (scoring threshold reached)
2. Sales Development Rep (SDR) reviews and validates → accepts or rejects
3. If accepted → SQL, assigned to Account Executive
4. If rejected → back to marketing nurture with feedback
5. AE conducts discovery → becomes Opportunity or disqualified

### Handoff SLA
| Step | SLA |
|------|-----|
| MQL notification to sales | Within 5 minutes (automated) |
| SDR first contact attempt | Within 1 hour during business hours |
| SDR qualification complete | Within 48 hours |
| AE first meeting | Within 5 business days |
| Rejection feedback to marketing | Within 24 hours with reason |

---

## Automation Workflows

### Essential Marketing Automations

**1. Welcome & Onboarding**
```
Trigger: New signup
→ Send welcome email (immediate)
→ Wait 2 days → Send getting started guide
→ If activated product → Congrats email
→ If NOT activated in 5 days → Re-engagement email
→ If NOT activated in 14 days → Flag for manual follow-up
```

**2. Lead Nurture (Drip)**
```
Trigger: Downloaded lead magnet
→ Deliver asset (immediate)
→ Wait 3 days → Related content email
→ Wait 4 days → Case study email
→ If clicked → Add to "engaged" segment, increase lead score
→ Wait 5 days → Soft CTA email
→ If lead score > 50 → Route to sales
```

**3. Cart/Trial Abandonment**
```
Trigger: Started checkout/trial, didn't complete
→ Wait 1 hour → "Did something go wrong?" email
→ Wait 24 hours → "Here's what you're missing" email
→ Wait 72 hours → Incentive email (discount/extended trial)
→ If no action → Tag as "abandoned," nurture list
```

**4. Re-engagement**
```
Trigger: No email opens in 60 days
→ "We miss you" email
→ Wait 7 days → "What's new" email with best content
→ Wait 14 days → "Last chance to stay" email
→ If no action → Remove from active list, suppress
```

**5. Deal Stage Notifications**
```
Trigger: Deal moves to "Proposal Sent"
→ Notify sales manager
→ Set reminder: follow-up in 3 days
→ If no response in 7 days → Auto-send follow-up email
→ If no response in 14 days → Flag as at-risk
```

---

## CRM Hygiene

### Monthly CRM Cleanup Checklist
- [ ] Remove/merge duplicate contacts
- [ ] Update stale deals (no activity 30+ days → mark stale or close)
- [ ] Verify email validity for bounced contacts
- [ ] Standardize data fields (company names, job titles, sources)
- [ ] Remove test records and internal contacts from reports
- [ ] Review and update pipeline stages if conversion patterns changed
- [ ] Audit automation workflows for errors or low performance
- [ ] Clean up unused tags, lists, and segments
- [ ] Check integration sync health (email, calendar, forms)

### Data Quality Rules
- Every contact must have: email, name, source, lifecycle stage
- Every deal must have: amount, close date, stage, assigned owner
- No deal should sit in same stage for more than 30 days without activity
- Company names should be standardized (no duplicates like "Acme" and "Acme Inc")
- Phone numbers in international format
- Tags used consistently (not ad-hoc spelling variations)

---

## Open-Source CRM Options

For founders and SMBs who want full control over their customer data:

| Platform | Best For | Key Strength |
|----------|----------|-------------|
| **Twenty** | Modern sales teams (1-50 users) | Beautiful UI, GraphQL API, custom objects |
| **erxes** | Full-stack experience management | Plugin ecosystem (CRM + marketing + support) |
| **Mautic** | Marketing automation + email | Campaign builder, lead scoring, email at scale |
| **Odoo** | All-in-one ERP + CRM | Comprehensive but complex |
| **SuiteCRM** | Enterprise CRM replacement | Salesforce-like feature depth |

### When to Recommend Self-Hosted CRM
- Data sovereignty is required (GDPR, regulated industry)
- Team has developer resources for setup and maintenance
- SaaS CRM costs are prohibitive at scale ($50-300/user/month × team)
- Custom workflows needed that SaaS platforms can't accommodate
- Integration requirements beyond standard connectors
