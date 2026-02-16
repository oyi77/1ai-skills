---
name: market-research
description: Use when gathering market intelligence - competitor research, customer insights, keyword analysis, and trend monitoring.
---

# market-research Skill

## What It Does

Market intelligence gathering and analysis - competitor research, customer insights, keyword analysis, trend monitoring, and strategic recommendations.

## When to Use

- Research competitors and alternatives
- Analyze market trends
- Understand customer needs
- Identify growth opportunities
- Support product decisions

## Key Capabilities

- **Competitor Analysis**: Pricing, features, positioning
- **Keyword Research**: SEO and content opportunities
- **Customer Research**: Needs, pain points, behaviors
- **Trend Analysis**: Emerging patterns and opportunities
- **Report Generation**: Structured insights and recommendations

## Browser Workflows

### Competitor Research

1. Navigate: competitor website
2. Extract: pricing, features, positioning
3. Search: reviews and feedback (G2, Capterra, TrustRadius)
4. Analyze: strengths and weaknesses
5. Report: in structured format

### Keyword Research

1. Navigate: Google Keyword Planner or Ubersuggest
2. Input: seed keywords
3. Extract: volume, difficulty, related terms
4. Analyze: opportunities
5. Export: to spreadsheet

### Customer Research

1. Navigate: review sites, forums, social media
2. Extract: customer feedback and complaints
3. Categorize: by topic and sentiment
4. Identify: patterns and opportunities
5. Summarize: key insights

## Usage Examples

### Analyze Competitor
```
User: "Research our competitor 'Company X' in the SaaS space"
Skill: Scrapes website → analyzes pricing → reviews features → generates report
```

### Find Market Opportunities
```
User: "What are the top opportunities in the AI tools market?"
Skill: Researches trends → analyzes keywords → identifies gaps → recommends
```

### Understand Customer Needs
```
User: "What do customers complain about in project management software?"
Skill: Scrapes reviews → categorizes complaints → identifies themes → reports
```

## Skills It Coordinates

- `agent-browser` - Browser automation
- `competitor-alternatives` (skills.sh) - Competitor analysis
- `seo-audit` (skills.sh) - Keyword research
- `mckinsey-research` - Framework analysis

## Research Quality Rubric

| Criterion | Weight | Threshold |
|-----------|--------|-----------|
| Comprehensiveness | 30% | Covers all major aspects |
| Accuracy | 30% | Data verified |
| Relevance | 25% | Actionable insights |
| Presentation | 15% | Clear and structured |

## Files Created

- `research-reports/` - Generated reports
- `competitor-data/` - Competitor information
- `keyword-data/` - Keyword research
- `customer-insights/` - Customer research
