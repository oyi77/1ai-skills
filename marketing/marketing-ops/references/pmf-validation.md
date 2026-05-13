# Product-Market Fit Validation Reference

Stop building what nobody wants. This reference uses real-time community signals,
demand testing, and customer evidence to validate product-market fit BEFORE and
DURING product development.

Inspired by: last30days-skill's approach of researching what communities are
actually upvoting, sharing, and discussing — not what you assume they want.

---

## The PMF Validation Stack

```
SIGNAL DETECTION        →  DEMAND TESTING      →  PMF MEASUREMENT
─────────────────          ─────────────          ────────────────
What are people            Will they pay          Are they staying
complaining about?         for a solution?        and telling others?
(community research)       (pre-sell tests)       (retention + referral)
```

---

## Phase 1: Signal Detection (Before Building)

### Real-Time Community Research

The best product ideas come from real people expressing real pain in public.
Use web search to scan these sources for your problem domain:

**Reddit — The Highest-Signal Source**
```
Search queries to run:
  "{problem domain} frustrating"
  "{problem domain} alternative to"
  "{problem domain} wish there was"
  "{problem domain} anyone built"
  "{competitor name} sucks"
  "{competitor name} alternative"

What to extract:
  - Posts with 100+ upvotes = validated pain (many people feel this)
  - Comments with specific feature requests = product roadmap gold
  - "I'd pay for this" comments = direct demand signal
  - Complaints about existing solutions = competitive opportunity
```

**Hacker News — Technical Demand Signals**
```
Search: "Show HN" posts in your category
  - What got traction (100+ points)?
  - What got killed (low engagement)?
  - Read the comments — HN comments reveal real objections
  - "Ask HN: Anyone know a tool for {X}?" = unmet demand
```

**X/Twitter — Real-Time Frustration**
```
Search: "{problem} is broken" OR "{competitor} problem" OR "need a better {tool}"
  - Tweets with high engagement = resonant pain point
  - Reply threads = detailed feature requirements
  - Founders building in public in your space = competitor intelligence
```

**YouTube — Depth Signals**
```
Search: "{problem domain} tutorial" OR "{competitor} review"
  - Videos with high views but bad ratings = underserved market
  - Comment sections = feature requests and complaints
  - Tutorial videos for workarounds = pain point confirmation
```

### The Signal Scoring Matrix

For each pain point discovered, score:

| Signal | Score | Meaning |
|--------|-------|---------|
| Reddit post 500+ upvotes about this pain | 5 | Strong validated demand |
| Multiple Reddit threads about same problem | 4 | Persistent unmet need |
| "I'd pay for this" comments (3+) | 5 | Direct willingness to pay |
| Competitor complaints (consistent pattern) | 4 | Market gap exists |
| HN "Ask HN" with 50+ points | 4 | Technical audience demand |
| YouTube tutorial with 10K+ views for workaround | 3 | People need solutions |
| Twitter complaints with engagement | 2 | Real-time frustration |
| Blog posts about the problem | 2 | Awareness exists |
| Nobody is talking about this anywhere | -5 | Either too niche or not a real problem |

**Score > 15:** Strong signal — this problem is worth solving
**Score 8-15:** Moderate — validate with direct conversations
**Score < 8:** Weak — find a different problem or angle

---

## Phase 2: Demand Testing (Before Building Product)

### The 5 Demand Tests (Pick 2-3)

**Test 1: Landing Page + Waitlist**
```
Create a simple landing page explaining the solution:
  - What problem you solve (1 sentence)
  - How you solve it differently (3 bullet points)
  - Email capture: "Join the waitlist"
  - Drive traffic: share in communities where you found signals

PASS:  100+ signups in 2 weeks (or 5%+ conversion rate)
FAIL:  <20 signups after meaningful traffic → problem or message issue
```

**Test 2: Fake Door / Pre-sell**
```
Create a "Buy Now" or "Start Free Trial" page:
  - When clicked → "We're launching soon! Enter email to get early access + discount"
  - Measures: how many people try to BUY, not just sign up

PASS:  3%+ click "buy" button
FAIL:  <1% → people don't want to pay for this
```

**Test 3: Manual Concierge MVP**
```
Instead of building the product, do it manually for 5-10 people:
  - Offer to solve their problem by hand (email, spreadsheet, manual work)
  - Charge a small fee (even Rp 50,000 / $10)
  - Observe: do they actually USE the solution? Do they come back?

PASS:  People pay AND come back AND refer others
FAIL:  People don't engage even when it's free/cheap
```

**Test 4: Cold DM Validation**
```
DM 50 people from your ICP (found in Reddit/Twitter research):
  "Hey, I noticed you mentioned {pain point}. I'm exploring building
   a solution for {specific problem}. Would you have 10 minutes to
   chat about how you currently handle this?"

PASS:  10+ people agree to talk (20%+ response rate)
FAIL:  <5 people respond → wrong audience or wrong problem framing
```

**Test 5: Community Post Test**
```
Post in relevant community (Reddit, IndieHackers, Facebook Group):
  "I'm considering building {product} because I keep seeing {problem}.
   Would anyone actually use/pay for this?"

PASS:  20+ upvotes AND 5+ comments saying "yes, please build this"
FAIL:  Crickets or "just use {existing solution}"
```

---

## Phase 3: PMF Measurement (After First Customers)

### The Sean Ellis Test
Ask every user: "How would you feel if you could no longer use {product}?"

| Answer | % of Users | PMF Status |
|--------|-----------|-----------|
| "Very disappointed" | **>40%** | ✅ **You have PMF** |
| "Very disappointed" | 25-40% | 🟡 Close — iterate on the 25-40% |
| "Very disappointed" | <25% | ❌ **No PMF** — pivot or reposition |

### PMF Evidence Checklist
Score each indicator (0-2 points):

```
DEMAND SIGNALS (Can you get customers?)
□ Organic word-of-mouth (users refer without being asked)
□ Inbound inquiries growing month-over-month
□ Waitlist/demand exceeds capacity to deliver
□ Low CAC relative to LTV (people come easily)

RETENTION SIGNALS (Do customers stay?)
□ Monthly churn < 5% (SaaS)
□ Users return without reminders
□ Usage depth increasing over time (more features, more frequently)
□ Users complain when service is down (it matters to them)

VALUE SIGNALS (Are they getting value?)
□ Customers report specific outcomes ("saved 10 hours/week")
□ Customers resist switching even when cheaper alternatives appear
□ NPS score > 40
□ Customers willing to pay more for premium features

GROWTH SIGNALS (Is it compounding?)
□ Revenue growing 15%+ month-over-month
□ Viral coefficient > 0.3 (users bring in new users)
□ Competitive "moat" emerging (switching costs, network effects, data)
□ Users defending product in public forums

TOTAL: /24
  20-24: Strong PMF — scale aggressively
  14-19: PMF emerging — keep iterating, don't scale yet
  8-13:  Weak PMF — major changes needed
  <8:    No PMF — consider pivoting
```

---

## Phase 4: Continuous PMF Monitoring

### The Weekly PMF Pulse

Run these checks weekly to ensure you haven't lost PMF:

```
□ Are new signups growing, flat, or declining?
□ Is churn increasing? (PMF regression = churn spike)
□ Are customers requesting features OR complaining about missing ones?
  (Requests = engaged. Silence = indifferent. Indifference kills.)
□ What are people saying in communities right now?
  → Search Reddit/X for your product name monthly
□ Are competitors launching similar features? Are customers comparing?
□ Is your NPS trending up or down?
```

### The Pivot-or-Persevere Framework

```
IF: No PMF after 3 months of active selling (not building)
    AND: <10 paying customers
    AND: Churn > 50% (people try and leave immediately)
THEN: Consider pivoting

PIVOT OPTIONS:
  1. Same audience, different problem (you know them, find a better pain)
  2. Same problem, different audience (your solution works, for different people)
  3. Same problem, different solution (rebuild the approach, not the mission)
  4. Different everything (last resort — only if data is overwhelming)
```

---

## Integration with Marketing-Ops

### How PMF Validation Connects to Marketing

**BEFORE PMF (Stage 0-1):**
```
marketing-ops research   → Mine Reddit/X for pain points
marketing-ops sales      → Manual outreach to validate demand
marketing-ops pricing    → Test willingness to pay
marketing-ops tracking   → Set up basic metrics
→ 90% of time on VALIDATION, 10% on marketing
```

**DURING PMF Search (Stage 1-2):**
```
marketing-ops content    → Write about the problem (attracts ICP)
marketing-ops email      → Capture interested people
marketing-ops cro        → Optimize signup/conversion
marketing-ops retention  → Track if first users stay
→ 50% validation, 50% growth experiments
```

**AFTER PMF Confirmed (Stage 2+):**
```
marketing-ops stage      → What to scale now
marketing-ops decide     → Which channel to invest in
marketing-ops execute    → Run daily marketing routine
→ 10% validation (ongoing monitoring), 90% scaling
```

### The Golden Rule
**Do NOT use advanced marketing modes (paid ads, programmatic SEO, affiliate
programs, influencer campaigns) until you have PMF evidence.**
Those are scaling tools. If you scale a product nobody wants,
you just lose money faster.

The right order is always:
1. Validate demand (this reference)
2. Get 10 paying customers manually
3. THEN scale with marketing-ops
