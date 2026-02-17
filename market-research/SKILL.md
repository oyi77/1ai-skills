---
name: market-research
description: Use when gathering browser-based market intelligence for competitor analysis, SEO positioning, customer insight discovery, keyword opportunity mapping, and product feedback synthesis.
---

# market-research Skill

## What It Does

Runs end-to-end market research using browser workflows only. This wrapper coordinates `competitor-alternatives` for competitor breakdowns, `seo-audit` for market positioning, and custom workflows for customer research, keyword research, and product feedback analysis.

## When to Use

- Evaluate direct and indirect competitors before launching or repricing.
- Understand positioning gaps before writing copy, ads, or landing pages.
- Collect real customer pain points from reviews, forums, and communities.
- Discover keyword clusters for content strategy and demand capture.
- Translate feedback into prioritized product and messaging improvements.

## Core Inputs

- Product URL and one-line value proposition.
- Customer segment (ICP), geography, and pricing tier.
- 3-10 known competitors (or "discover competitors" mode).
- Optional seed keywords and target outcomes (traffic, signups, trials).

## How It Works

```
Input: "Research [MARKET] for [PRODUCT] and return opportunities"
   ↓
Scope: define ICP, geography, competitor set, and timeframe
   ↓
Competitor Layer: run competitor-alternatives workflow via browser
   ↓
Positioning Layer: run seo-audit workflow for SERP and content gaps
   ↓
Custom Research:
  - customer research
  - keyword research
  - product feedback analysis
   ↓
Synthesis: score opportunities by impact, confidence, and effort
   ↓
Output: research brief + action plan + evidence links
```

## Browser Automation Workflows

### 1) Competitor Research (via `competitor-alternatives`)

1. Navigate: competitor homepages and pricing pages.
2. Extract: plans, feature claims, proof points, and CTA patterns.
3. Validate: review platforms (G2, Capterra, Trustpilot, Reddit threads).
4. Compare: feature parity, positioning angle, pricing psychology.
5. Output: competitor matrix with strengths, weaknesses, and openings.

### 2) Market Positioning (via `seo-audit`)

1. Navigate: Google search for core problem-intent queries.
2. Capture: top ranking pages by intent type (guide, comparison, product page).
3. Extract: recurring positioning language and differentiation claims.
4. Map: content gaps and weak SERP segments by intent.
5. Output: positioning recommendations and content opportunities.

### 3) Customer Research (custom)

1. Navigate: Reddit, Quora, YouTube comments, app stores, review sites.
2. Search: "how do I", "alternative to", "frustrated with", "best tool for".
3. Extract: jobs-to-be-done, blockers, desired outcomes, switching triggers.
4. Cluster: pain points into onboarding, workflow, pricing, and support buckets.
5. Output: customer insight map with direct quote snippets.

### 4) Keyword Research (custom)

1. Start: seed list from customer language and competitor pages.
2. Validate: keyword ideas in browser tools (Google autocomplete, related searches, keyword platforms).
3. Classify: intent (informational, commercial, transactional, navigational).
4. Prioritize: high relevance + attainable difficulty + business value.
5. Output: keyword clusters with landing page/content recommendations.

### 5) Product Feedback Analysis (custom)

1. Gather: reviews, support transcripts, changelog comments, social mentions.
2. Tag: sentiment, feature area, severity, frequency, and user segment.
3. Identify: repeated complaints, unmet expectations, and delight moments.
4. Translate: each pattern into product fixes and messaging updates.
5. Output: prioritized feedback backlog with evidence references.

## Deliverables Format

- `Executive Brief`: market summary, key risks, biggest opportunities.
- `Competitor Matrix`: pricing/features/positioning comparison table.
- `Keyword Cluster Sheet`: topic cluster, intent, priority, page type.
- `Customer Insight Map`: pains, desired outcomes, and decision triggers.
- `Feedback Backlog`: issue, severity, frequency, proposed response.

## Research Quality Rubric

| Criterion | Weight | 1 (Weak) | 5 (Acceptable) | 10 (Excellent) |
|-----------|--------|----------|----------------|----------------|
| Evidence quality | 30% | Claims without sources | Some sources, uneven quality | Strong sources and traceable links |
| Actionability | 25% | Generic observations | Some practical next steps | Clear prioritized actions with owners |
| Coverage | 20% | Misses major segments | Covers core areas | Comprehensive across competitors/customers/keywords/feedback |
| Strategic clarity | 15% | Contradictory or vague | Mostly coherent | Clear positioning narrative and decisions |
| Reproducibility | 10% | Steps undocumented | Partial method notes | Full method and repeatable workflow |

Pass threshold: weighted score >= 7.5/10. If below threshold, rerun weak sections with additional sources.

## Usage Examples

### Example 1: Competitor + Positioning Sprint
```text
User: "Run market research for AI note-taking tools in the US SMB market."
Skill: Runs competitor-alternatives + seo-audit workflows, then outputs a positioning gap report and 90-day opportunity plan.
```

### Example 2: Customer and Feedback Deep Dive
```text
User: "Analyze customer pain points for project management apps and suggest product improvements."
Skill: Scrapes review/community evidence, clusters pain themes, ranks fixes by impact, and proposes product + messaging updates.
```

### Example 3: Keyword Opportunity Mapping
```text
User: "Find keyword opportunities for a B2B workflow automation SaaS."
Skill: Builds seed set from customer language, validates intent and difficulty, and returns cluster-to-page recommendations.
```

## Skills It Coordinates

- `competitor-alternatives` (skills.sh): competitor discovery and alternative mapping.
- `seo-audit` (skills.sh): SERP, visibility, and market positioning analysis.
- `mckinsey-research`: structured synthesis and strategic recommendation framing.

## Guardrails

- Browser-based only. Do not rely on private APIs.
- Keep every conclusion tied to observable evidence.
- Separate facts, assumptions, and recommendations.
- Flag uncertainty explicitly when source quality is weak.

## Troubleshooting

- If sources conflict, note disagreement and collect two additional confirmations.
- If SERP is too broad, narrow by geography, persona, and intent modifier.
- If evidence is stale, prioritize pages updated in last 12 months.
- If findings are generic, rerun with stricter ICP and JTBD framing.
