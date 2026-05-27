---
name: ai-seo
description: Optimize for AI search engines — Perplexity, ChatGPT Search, Google AI Overviews, answer engine optimization. Use when adapting SEO strategy for AI-powered search, optimizing for featured snippets, or building AI-friendly content.
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

## Pseudo Code

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
