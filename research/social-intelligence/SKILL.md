---
name: social-intelligence
description: Cross-platform social media intelligence gathering using Agent Reach. Research trends, sentiment, competitive
  intel, and user insights from Twitter, Reddit, YouTube, XiaoHongShu across 35+ platforms. Use when researching social proof,
  market sentiment, viral content patterns, or competitive positioning.
domain: research
tags:
- social-media
- research
- sentiment-analysis
- competitive-intelligence
- trend-monitoring
- agent-reach
---
# Social Intelligence

## When to Use

**Trigger phrases:**
- "What are people saying about X on social media?"
- "Research sentiment around [product/topic]"
- "Find viral content patterns in [niche]"
- "What's trending on Twitter/Reddit/YouTube?"
- "Competitive intelligence on [competitor]"
- "User pain points in [category]"
- "Social proof for [feature/product]"

**Use cases:**
- Pre-launch market research
- Competitor positioning analysis
- Content ideation from social trends
- Brand sentiment monitoring
- Product feedback aggregation
- Influencer discovery
- Viral hook mining

**When NOT to use:** Simple single-platform queries (use native tools), when ethical scraping boundaries crossed, when historical data >6 months old (use archived datasets instead)


## When NOT to Use

- When the answer is already known and documented
- For time-sensitive decisions that cannot wait for thorough research
- When the topic is outside your domain of competence


## Overview

Social Intelligence enables thorough investigation with structured methodology.

## Workflow

```python
# Example: Source evaluation
def evaluate_source(url: str) -> dict:
    return {
        "authority": check_domain_authority(url),
        "currency": get_last_updated(url),
        "objectivity": detect_bias(url),
        "accuracy": cross_reference(url),
    }
```

1. **Define question** — Clarify the research objective
2. **Gather sources** — Collect primary and secondary data
3. **Analyze** — Apply analytical frameworks to findings
4. **Synthesize** — Combine insights into actionable conclusions
5. **Present** — Deliver findings in clear, compelling format
6. **Archive** — Store research for future reference

## Source Evaluation

- **Authority** — Is the source credible and expert?
- **Currency** — Is the information recent and relevant?
- **Objectivity** — Is there bias or conflict of interest?
- **Accuracy** — Can claims be verified independently?

## Output Format

- Executive summary (1-2 paragraphs)
- Key findings (bullet points)
- Detailed analysis (sections with evidence)
- Recommendations (actionable next steps)
- Sources and methodology

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "First result is good enough" | Deep research finds better answers. Keep digging. |
| "I do not need to verify sources" | Unverified sources lead to wrong conclusions. Always cross-check. |
| "Research is a one-time thing" | Markets change. Research needs to be continuous, not one-off. |


## Process

1. **Research** — Analyze target audience, competitors, and trending topics
1. **Create** — Generate content following brand guidelines and best practices
1. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings