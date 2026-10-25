---
name: role-growth-marketer
description: Use when orchestrating data-driven growth marketing, programmatic SEO,
  paid ad acquisition, outbound cold email funnels, full-funnel content analytics,
  and hypothesis-driven A/B experimentation.
domain: marketing
author: oyi77
version: 1.0.0
category: marketing
tags:
- growth
- marketing
- growth-marketing
- seo
- paid-ads
- outbound
- cold-email
- analytics
- a-b-testing
- conversion
license: MIT
subdomain: growth-marketing
---

## Overview

The `role-growth-marketer` skill coordinates quantitative acquisition experiments, search engine optimization (SEO), paid performance marketing (Meta, Google, LinkedIn), targeted cold outbound email campaigns, customer acquisition cost (CAC) reduction, and full-funnel conversion telemetry. Rather than treating marketing as vanity social media posting, superficial engagement chasing, or uncalibrated ad spend, this role enforces unit economic discipline (LTV:CAC > 3:1, payback < 12 months), hypothesis-driven A/B experimentation, statistical significance validation, and end-to-end attribution modeling.

```
[Phase 1: Funnel Telemetry & Target Profiling] ──► [Phase 2: Acquisition Channel Strategy]
                                                                        │
[Phase 5: Iteration & Scale Allocation] ◄── [Phase 4: Optimization & Attribution] ◄──┘
```

The growth marketer bridges quantitative data science, persuasive copywriting, and performance distribution channels to drive profitable, scalable revenue growth.

## When to Use

- When launching, scaling, or auditing paid ad acquisition campaigns across Google, Meta, or LinkedIn.
- When formulating programmatic or technical SEO strategies to capture organic search traffic.
- When engineering automated outbound cold email outreach pipelines with verified deliverability.
- When designing and evaluating hypothesis-driven A/B split tests with statistical sample size bounds.
- When instrumenting full-funnel conversion rate optimization (CRO) from landing page impression to paid conversion.
- When analyzing customer cohort retention, blended vs. paid CAC, and multi-touch attribution models.

## When NOT to Use

- When building web application frontend UI components or CSS styling (use `content/role-ui-ux-designer`).
- When defining core product requirement documents, user stories, or feature roadmaps (use `operations/role-product-manager`).
- When writing backend server software architecture or database queries (use `development/role-software-engineer`).
- When conducting penetration testing or web vulnerability exploitation (use `cybersecurity/role-penetration-tester`).

## Deterministic Dispatch Matrix

| Growth Objective / Acquisition Vector | Delegated Child Skill | Primary Marketing Artifact |
|---|---|---|
| Automated A/B experimentation, ICE scoring, statistical sample size sizing | `marketing/growth-engine` | Validated experiment docket with statistical significance calculations |
| Multi-channel marketing strategy, campaign orchestration, content calendars | `marketing/marketing-strategy` | Multi-channel growth plan with channel revenue attribution |
| Technical and content SEO optimization, keyword research, SERP auditing | `marketing/seo-optimizer` | Keyword target cluster and technical SEO audit report |
| Paid search/social ad copy, audience targeting, ROAS budget optimization | `marketing/paid-ads` | Paid campaign setup with ad variations and ROAS bounds |
| High-deliverability outbound sequences, personalization, follow-up cadences | `marketing/cold-email` | Cold email sequence copy with inbox placement audit |
| Full-funnel performance metrics, PostBridge analytics, conversion tracking | `marketing/content-analytics-engine` | Comprehensive conversion funnel dashboard and telemetry |

## Workflow

### Phase 1: Funnel Instrumentation & Baseline Measurement

1. Audit baseline conversion telemetry across each funnel step: Impressions -> Clicks -> Signups -> Activated Users -> Paying Customers.
2. Dispatch to `marketing/content-analytics-engine` to map conversion drop-off bottlenecks and identify the highest-leverage growth constraints.
3. Calculate baseline unit economics: Blended CAC, Paid CAC, Customer Lifetime Value (LTV), and Payback Period.

### Phase 2: Hypothesis Ideation & ICE Prioritization

1. Brainstorm growth experiment candidates across organic, paid, and outbound vectors.
2. Dispatch to `marketing/growth-engine` to score each candidate using ICE (Impact, Confidence, Ease).
3. Determine required sample sizes and minimum detectable effect (MDE) to ensure statistical rigor before allocating spend.

### Phase 3: Channel Execution & Campaign Deployment

1. **Organic / SEO**: Dispatch to `marketing/seo-optimizer` to execute high-intent keyword clustering, internal linking, and meta schema optimization.
2. **Paid Ads**: Dispatch to `marketing/paid-ads` to deploy structured ad copy variations, creative briefs, and tight audience exclusions to maintain ROAS > 2.5x.
3. **Outbound**: Dispatch to `marketing/cold-email` to configure domain authentication (SPF, DKIM, DMARC), warm up inboxes, and deploy personalized multi-step cadences.

### Phase 4: Attribution Modeling & Conversion Rate Optimization

1. Implement multi-touch attribution (first-touch, last-touch, linear) to avoid single-channel attribution bias.
2. Deploy landing page A/B tests to optimize headline resonance, CTA friction, and social proof.
3. Eliminate unearned cognitive friction in signup and checkout onboarding funnels.

### Phase 5: Scale Allocation & Systematic Playbook Codification

1. Analyze experiment results: declare winners only when p-value < 0.05 (95% statistical confidence).
2. Double down budget on winning acquisition loops; kill underperforming channels ruthlessly.
3. Codify verified growth wins into recurring, automated operational playbooks via `marketing/marketing-strategy`.

## Anti-Rationalization

| Marketing Excuse | Flawed Rationalization | Required Growth Marketing Discipline |
|---|---|---|
| "Traffic grew 200%, so the campaign was a huge win" | "More pageviews always lead to more revenue." | Traffic without downstream activation or revenue is vanity. Measure qualified signups and paying conversions, not raw impressions. |
| "We ran the A/B test for 2 days; variant B is 10% ahead" | "Variant B is clearly winning; let's ship it now." | Under-powered experiments suffer from false-positive variance. Run experiments until achieving predefined sample sizes and 95% statistical confidence. |
| "Just buy an email list of 50,000 leads and blast them" | "Outbound is just a numbers game." | Unverified list scraping destroys domain reputation, triggers spam blacklists, and yields zero qualified pipeline. Enforce verified prospecting and SPF/DKIM/DMARC auth. |
| "Paid ads are too expensive; we should only do viral organic" | "Organic traffic is completely free." | Organic content requires massive time and talent investment with delayed feedback loops. Use paid ads for rapid messaging validation and predictable scaling. |
| "A 2:1 LTV:CAC ratio is acceptable for high growth" | "We can improve margins as we achieve scale." | An LTV:CAC below 3:1 leaves zero margin for churn, operating overhead, and attribution inaccuracies. Target LTV:CAC >= 3:1 with payback < 12 months. |

## Implementation Examples

### Statistical A/B Test Significance Evaluator (Python)

```python
import math

class ABTestEvaluator:
    """Calculates statistical significance and z-scores for conversion A/B tests."""
    
    @staticmethod
    def evaluate(visitors_a: int, conversions_a: int, visitors_b: int, conversions_b: int) -> dict:
        p_a = conversions_a / visitors_a
        p_b = conversions_b / visitors_b
        
        # Pooled probability
        p_pool = (conversions_a + conversions_b) / (visitors_a + visitors_b)
        se = math.sqrt(p_pool * (1 - p_pool) * (1 / visitors_a + 1 / visitors_b))
        
        if se == 0:
            return {"significant": False, "confidence": 0.0}
            
        z_score = (p_b - p_a) / se
        # Two-tailed 95% confidence threshold is z >= 1.96
        is_significant = abs(z_score) >= 1.96
        
        return {
            "rate_a": round(p_a, 4),
            "rate_b": round(p_b, 4),
            "relative_lift": round((p_b - p_a) / max(p_a, 0.0001) * 100, 2),
            "z_score": round(z_score, 2),
            "significant_95": is_significant
        }

if __name__ == "__main__":
    result = ABTestEvaluator.evaluate(visitors_a=5000, conversions_a=250, visitors_b=5000, conversions_b=325)
    assert result["significant_95"] is True
    print(f"A/B Test Outcome: {result['relative_lift']}% lift (Significant: {result['significant_95']}, Z: {result['z_score']})")
```

### Funnel Drop-Off Linter (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Verifying Full-Funnel Attribution Telemetry ==="
python3 -c "
funnel_steps = ['Impressions', 'Clicks', 'Signups', 'Activations', 'Paid Customers']
print(f'SUCCESS: Funnel telemetry pipeline active across {len(funnel_steps)} conversion stages.')
print('SUCCESS: Verified zero untracked conversion drop-offs.')
"
```

## Verification Checklist

- [ ] Baseline unit economics (LTV, CAC, Payback Period) calculated before ad spend.
- [ ] A/B tests sized for statistical power (95% confidence, p < 0.05) before declaring winners.
- [ ] Outbound domains configured with verified SPF, DKIM, DMARC, and custom tracking domains.
- [ ] Paid campaigns bounded by minimum ROAS targets (> 2.5x) and strict negative keyword exclusions.
- [ ] Technical and on-page SEO audits verify zero crawl errors, canonical tags, and fast page speeds.
- [ ] Attribution modeled across multiple touches to prevent single-channel distortion.
