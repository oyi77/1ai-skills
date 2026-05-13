# CRO Mode Reference

## Table of Contents
1. [Landing Page Audit](#landing-page-audit)
2. [A/B Testing Framework](#ab-testing-framework)
3. [Funnel Analysis](#funnel-analysis)
4. [Form Optimization](#form-optimization)
5. [Pricing Page Optimization](#pricing-page-optimization)
6. [Psychology & Persuasion](#psychology--persuasion)

---

## Landing Page Audit

### 50-Point Conversion Audit

**Above the Fold (Critical)**
1. Headline clearly states the value proposition
2. Headline matches the ad/source that brought them here
3. Sub-headline adds specificity or addresses the "how"
4. Primary CTA visible without scrolling
5. CTA button text is action-oriented (not "Submit")
6. Page loads in under 3 seconds
7. Hero image/video supports the message (not generic stock)
8. Social proof visible (logos, rating, user count)
9. No navigation links competing with CTA (for dedicated landing pages)
10. Mobile-responsive above the fold

**Value Proposition**
11. Clear what they GET (outcome, not features)
12. Clear WHO it's for
13. Clear HOW it's different from alternatives
14. Benefits > Features in messaging hierarchy
15. Unique mechanism or method highlighted

**Social Proof**
16. Customer testimonials with names and photos
17. Specific results mentioned (numbers, not vague praise)
18. Company logos if B2B
19. Review/rating scores displayed
20. Case study summary or link
21. User count or community size

**Trust & Credibility**
22. SSL certificate (https)
23. Privacy policy linked
24. Money-back guarantee or free trial offered
25. Industry certifications or awards
26. Security badges (if collecting payment)
27. Real contact information available

**CTA & Conversion Path**
28. One primary CTA per viewport
29. CTA color contrasts with page background
30. CTA button large enough to tap on mobile
31. Friction-reducing copy near CTA ("No credit card required")
32. Urgency/scarcity elements (only if genuine)
33. Alternative CTA for not-ready visitors (download guide, watch demo)

**Content Flow**
34. Logical progression: Problem → Solution → Proof → Action
35. Scannable formatting (headings, bullets, bold key points)
36. Appropriate content length for complexity of decision
37. FAQ section addressing top 5 objections
38. Visual hierarchy guides eye toward CTA

**Technical**
39. Page speed: Core Web Vitals passing
40. Mobile-first design (not just responsive)
41. No broken images or links
42. Forms work correctly (test submission)
43. Analytics/tracking installed and firing
44. Heatmap/session recording active (recommendation)

**Copy Quality**
45. Written for the reader, not the company
46. Active voice predominant
47. Jargon-free (or explained when necessary)
48. Emotional drivers addressed (fear, desire, belonging)
49. Specific > vague ("Save 10 hours/week" > "Save time")
50. Consistent voice throughout

### Scoring
Each item scored: Pass (1) / Partial (0.5) / Fail (0)
- **40-50:** Excellent — focus on testing and iteration
- **30-39:** Good — clear optimization opportunities
- **20-29:** Needs work — structural improvements needed
- **Below 20:** Major rebuild recommended

---

## A/B Testing Framework

### Test Prioritization (ICE Score)
- **Impact** (1-10): How much could this move the needle?
- **Confidence** (1-10): How sure are you it'll work?
- **Ease** (1-10): How quick/cheap to implement?
- **ICE Score** = (Impact + Confidence + Ease) / 3

### What to Test (Priority Order)
1. **Headline** — highest impact, easy to test
2. **CTA** — text, color, placement, size
3. **Social proof** — type, placement, specificity
4. **Page layout** — long vs short, section order
5. **Pricing presentation** — anchoring, plan names, feature emphasis
6. **Form fields** — number of fields, order, labels
7. **Images/video** — product vs person, static vs motion
8. **Copy length** — short vs detailed

### Test Plan Template
```markdown
# A/B Test Plan: {Test Name}

**Hypothesis:** Changing {element} from {current} to {proposed}
will increase {metric} by {estimated %}
because {rationale based on evidence/psychology}.

**Primary metric:** {Conversion rate / CTR / Revenue per visitor}
**Secondary metrics:** {Bounce rate, time on page, etc.}
**Minimum sample size:** {Calculate at 95% confidence, 80% power}
**Estimated duration:** {Based on traffic and conversion rate}

**Control (A):** {Current version description}
**Variant (B):** {New version description}

**Segmentation:** {Test all visitors or specific segment}

**Success criteria:** Statistical significance at 95% confidence
AND practical significance (>5% lift for most tests)
```

### Statistical Significance Rules
- Minimum 95% confidence level
- Run for at least 7 days (capture day-of-week variance)
- Minimum 100 conversions per variant (more for subtle changes)
- Don't peek and call winners early — commit to the sample size
- Account for multiple comparisons if testing 3+ variants

---

## Funnel Analysis

### Standard Funnel Stages

```
Awareness (Impressions, Reach)
    ↓ [Click-through rate]
Interest (Clicks, Page Views)
    ↓ [Engagement rate]
Consideration (Time on site, Pages/session)
    ↓ [Lead capture rate]
Intent (Add to cart, Start trial, Form fill)
    ↓ [Conversion rate]
Purchase (Transaction, Subscription)
    ↓ [Retention rate]
Loyalty (Repeat purchase, Referral)
```

### Funnel Leak Analysis
For each stage transition:
1. What's the current conversion rate?
2. What's the benchmark for this industry/stage?
3. Where are people dropping off (specific pages/steps)?
4. What's the potential revenue impact of a 10% improvement here?
5. What are the likely causes of drop-off?
6. What are the top 3 fixes to test?

### SaaS Pirate Metrics (AARRR)
- **Acquisition:** How do users find you? (channels, CAC)
- **Activation:** Do they have a great first experience? (activation rate)
- **Retention:** Do they come back? (D1, D7, D30 retention)
- **Revenue:** How do you make money? (ARPU, LTV)
- **Referral:** Do they tell others? (viral coefficient, NPS)

---

## Form Optimization

### Field Reduction Strategy
Every additional field reduces conversion by approximately 5-10%.

| Form Purpose | Ideal Fields | Maximum |
|-------------|-------------|---------|
| Newsletter signup | Email only | Email + Name |
| Lead magnet download | Email + Name | + Company + Role |
| Demo request | Email + Name + Company | + Role + Budget |
| Contact form | Name + Email + Message | + Phone + Company |

### Form UX Best Practices
- Single column layout (no side-by-side fields on mobile)
- Inline validation (real-time, not after submit)
- Clear error messages explaining what to fix
- Progress indicators for multi-step forms
- Autofill compatible (proper input types and names)
- Smart defaults where possible
- Placeholder text should NOT replace labels
- Submit button text = what they GET ("Get My Free Guide" not "Submit")

---

## Pricing Page Optimization

### Pricing Psychology Tactics
- **Anchoring:** Show the highest plan first (or highlight "most popular")
- **Decoy effect:** Add a plan that makes the target plan look like best value
- **Charm pricing:** $49 vs $50 (still works for lower price points)
- **Annual savings:** Show monthly equivalent and annual discount prominently
- **Free tier:** Reduces risk perception, creates upgrade path
- **Feature comparison:** Table format, check marks, highlight differences

### Pricing Page Elements
1. Clear plan names (not just "Basic/Pro/Enterprise")
2. Price displayed prominently per plan
3. "Most Popular" or "Recommended" badge on target plan
4. Feature comparison table with tooltips for unclear features
5. FAQ specifically addressing pricing questions
6. Social proof near pricing (testimonials about value)
7. Money-back guarantee or free trial CTA
8. Annual vs monthly toggle with savings percentage

---

## Psychology & Persuasion

### Cialdini's 6 Principles Applied to CRO

| Principle | Application |
|-----------|------------|
| **Reciprocity** | Give value first (free tool, guide, trial) before asking |
| **Commitment** | Start with small asks (email) before big ones (purchase) |
| **Social proof** | Testimonials, user counts, logos, reviews |
| **Authority** | Expert endorsements, certifications, media mentions |
| **Liking** | Relatable brand voice, behind-the-scenes, team photos |
| **Scarcity** | Limited spots, countdown timers (only if genuine) |

### Cognitive Biases for CRO
- **Loss aversion:** "Don't miss out" > "Get this benefit"
- **Default effect:** Pre-select the recommended option
- **Endowment effect:** Free trial makes them feel ownership
- **Bandwagon effect:** "Join 50,000+ marketers"
- **Framing:** "$1/day" feels cheaper than "$365/year"
- **Peak-end rule:** Make the checkout/signup experience smooth + celebratory
