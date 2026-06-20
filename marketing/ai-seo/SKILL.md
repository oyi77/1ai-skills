---
name: ai-seo
description: Optimize for AI search engines — Perplexity, ChatGPT Search, Google AI Overviews, answer engine optimization.
  Use when adapting SEO strategy for AI-powered search, optimizing for featured snippets, or building AI-friendly content.
domain: marketing
tags:
- growth
- marketing
- seo
---



# AI SEO

Optimize content for AI-powered search engines and answer engines.

## Capabilities

- AI Overview optimization
- Answer engine optimization (Perplexity, ChatGPT Search)
- Structured data for AI consumption
- Content formatting for LLM extraction
- Entity-based SEO
- Citation and source optimization

## When to Use

- Adapting SEO strategy for AI search
- Optimizing for Google AI Overviews
- Building content that AI engines cite
- Implementing structured data markup

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The ai-seo workflow follows a standard pipeline pattern.

Core flow:
```
# ai-seo primary flow
input = prepare(raw_data)
result = process(input, config={adapting, answer, building, chatgpt, content})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# ai-seo primary flow
input = prepare(raw_data)
result = process(input, config={adapting, answer, building, chatgpt, content})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### AI-Friendly Content Structure

```markdown
# [Primary Question as H1]

## Direct Answer (first 2-3 sentences)
[Concise answer that AI can extract as a snippet]

## Detailed Explanation
[Supporting details, examples, data]

## Key Takeaways
- Point 1
- Point 2
- Point 3

## Sources
- [Source 1](url)
- [Source 2](url)
```

### Structured Data

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What is RAG?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "RAG (Retrieval-Augmented Generation) is a pattern that grounds LLM responses in factual data by retrieving relevant documents before generating answers."
    }
  }]
}
```

### Entity Optimization

```python
def optimize_for_entities(content, target_entities):
    """Ensure content mentions key entities AI engines look for."""
    for entity in target_entities:
        if entity not in content:
            content = add_entity_context(content, entity)
    return content
```

## Common Patterns

- **Question-based headings**: H2/H3 as questions users ask
- **Direct answers first**: First 2 sentences should answer the question
- **Structured data**: FAQ, HowTo, Article schema on every page
- **Source citations**: Link to authoritative sources AI engines trust
- **Entity richness**: Mention related entities, not just keywords

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels

## Overview

> Section content — see SKILL.md body for full details.

## Verification

- [ ] Skill output matches expected behavior
