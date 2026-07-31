---
name: market-research
description: Conduct market research, competitive analysis, and industry insights with Exa and Firecrawl. Use when conducting market research, competitive analysis, and industry insights with exa.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- growth
- market
- marketing
- research
- seo
allowed-tools: "|\n  - MCP(exa:*)\n    - MCP(firecrawl:*)\n    - MCP(notion:*)\n"
version: 1.0.0
---
# Market Research

## When to Use

**Trigger phrases:**
- "market research"
- "Help me with market research"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope


## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel


## Overview

Market Research is the systematic process of gathering, analyzing, and interpreting information about a market, its customers, and competitors. It transforms assumptions into evidence, gut feelings into data, and uncertainty into actionable strategy. For growth marketers and product teams, market research is the foundation that every campaign, feature, and positioning decision should rest on.

The full research lifecycle spans five phases: framing the problem, designing the approach, collecting data, analyzing findings, and delivering recommendations. Modern tools like Exa (for web-scale search and content discovery) and Firecrawl (for structured website extraction) make secondary research dramatically faster, enabling analysts to surface competitive intelligence, pricing data, and customer sentiment in minutes instead of weeks.

Key capabilities include market sizing (TAM, SAM, SOM), competitive landscaping, customer segmentation, trend analysis, and positioning analysis. The output feeds directly into product strategy, go-to-market planning, messaging frameworks, and growth experiments. Without disciplined research, marketing becomes guesswork with high spend and low signal.

A mature research practice balances secondary research (existing data from reports, databases, web scraping) with primary research (surveys, interviews, experiments). The best analysts triangulate across at least two independent sources before drawing conclusions and document methodology rigorously so decisions can be revisited as new data emerges.

## Workflow

```python
# Example: SEO keyword analysis
def analyze_keywords(keywords: list[str]) -> list[dict]:
    results = []
    for kw in keywords:
        volume = get_search_volume(kw)
        difficulty = get_difficulty(kw)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "opportunity": volume / max(difficulty, 1),
        })
    return sorted(results, key=lambda x: x["opportunity"], reverse=True)
```

1. **Frame the Problem** — Translate the business question into a research hypothesis. Define the unit of analysis (market, segment, competitor, customer persona) and the decision this research will inform.
1. **Design the Methodology** — Choose between exploratory (qualitative) and confirmatory (quantitative) approaches. Select tools: Exa for web-scale surfacing, Firecrawl for structured extraction, survey platforms for primary data collection.
1. **Collect Secondary Data** — Run Exa searches for competitive intelligence, industry trends, and customer sentiment. Use Firecrawl to extract pricing pages, feature tables, and review data from competitor sites. Gather analyst reports and government statistics.
1. **Collect Primary Data** — Design surveys, interview guides, or controlled experiments. Recruit participants matching the target customer profile. Aim for 5-10 interviews per segment for qualitative depth or 100+ survey responses for statistical significance.
1. **Analyze and Synthesize** — Compute TAM/SAM/SOM using both bottom-up and top-down approaches. Build competitive positioning maps. Code qualitative responses into themes. Identify whitespace opportunities where customer needs are underserved.
1. **Draw Conclusions** — Triangulate findings across independent sources. Rate confidence in each conclusion (high, medium, low) based on evidence strength. Map each finding back to the original research question.
1. **Deliver and Act** — Produce a structured report with executive summary, methodology, findings, and prioritized recommendations. Archive raw data and methodology for reproducibility.

## Key Metrics

- Reach and impressions
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks → leads → customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel

## Common Pitfalls

- **Confirmation bias** — Seeking data that confirms existing beliefs rather than challenging them. Always include a disconfirming evidence section in every research brief.
- **Over-reliance on secondary data** — Existing reports and databases may be outdated or biased. Validate key findings with at least one primary source.
- **Sampling that does not represent the market** — Convenience samples (Twitter followers, existing customers) skew results. Use stratified sampling or panel data for defensible conclusions.
- **Ignoring market sizing tiers** — A large TAM is meaningless without computing SAM and SOM. Always present and explain all three layers.
- **Analysis paralysis** — Gathering more data when existing data already supports a decision. Set a decision threshold before starting research and stop when you reach it.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good products sell themselves" | They do not. Marketing is how people discover your product. |
| "I will start marketing after launch" | Build audience before launch. Pre-launch momentum is critical. |
| "SEO is dead" | SEO evolves. GEO (Generative Engine Optimization) is the new frontier. |
| "Secondary research is good enough" | Without primary validation, you are basing decisions on someone else's assumptions and blind spots. |
| "TAM tells me if this is worth doing" | TAM is aspirational. SAM and SOM determine whether you can capture enough market to be viable. |
| "Competitors are the enemy" | Competitor analysis reveals gaps, benchmarks, and partnership opportunities. Ignore them at your own risk. |



## Monetization

| Approach | Timeframe | Description |
|---|---|---|
| Research-as-a-Service | Short-term (1-3 months) | Offer custom market research reports for startups validating product-market fit. Use Exa and Firecrawl for automated data collection. |
| Competitive Intelligence Subscription | Medium-term (3-6 months) | Monthly competitor tracking reports delivered to SaaS and e-commerce clients. Include pricing changes, feature launches, and ad strategy analysis. |
| Industry Insight Reports | Medium-term (3-6 months) | Publish in-depth TAM/SAM/SOM analysis for specific sectors. Sell as premium PDFs or subscription access to datasets. |
| Consulting and Strategy Engagements | Long-term (6-12 months) | Full-service engagements: define research questions, execute primary and secondary research, deliver actionable GTM recommendations. |
| Data Product or API | Long-term (12+ months) | Package automated market intelligence into a SaaS dashboard or API. Recurring revenue from subscribers monitoring their competitive landscape. |

## Process

1. **Define and Scope** — Translate business questions into testable research hypotheses. Identify which data sources (primary vs secondary, qualitative vs quantitative) will answer each question. Set budget and timeline constraints.
1. **Collect Secondary Data** — Gather existing intelligence via Exa (web and social search), Firecrawl (site scraping), industry reports, analyst briefs, government statistics, and public databases.
1. **Collect Primary Data** — Design and execute surveys, user interviews, focus groups, or controlled experiments. Recruit participants matching the target customer profile.
1. **Analyze and Synthesize** — Triangulate findings across sources. Compute TAM/SAM/SOM using both bottom-up and top-down approaches. Build competitive positioning maps. Code qualitative responses into themes and identify whitespace opportunities.
1. **Report and Recommend** — Produce an actionable report with executive summary, methodology, key findings, and prioritized recommendations mapped to the original research questions.

## Verification

- [ ] Research questions clearly defined and documented
- [ ] TAM/SAM/SOM computed with source citations
- [ ] At least one primary source validates each key finding
- [ ] Competitor analysis covers at least 3 direct competitors
- [ ] Findings triangulated across 2+ independent data sources
- [ ] Report includes methodology section with known limitations
- [ ] Recommendations mapped back to original research questions
- [ ] Executive summary written for non-expert stakeholders