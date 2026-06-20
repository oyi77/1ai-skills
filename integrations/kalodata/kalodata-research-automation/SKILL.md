---
name: kalodata-research-automation
description: End-to-end competitive analysis automation that combines product research, video analysis, and storyboard extraction
  into a single workflow. Accepts product search criteria and returns complete competitive analysis with viral product insights,
  video breakdowns, and content replication guides.
domain: integrations
tags:
- api
- integrations
- kalodata
- research
- third-party
- video
- workflow
metadata:
  model: sonnet
---

# Kalodata Research Automation Skill

End-to-end competitive analysisautomation that combines product research, video analysis, and storyboard extraction into a single workflow.

## Overview

Enables end-to-end competitive analysis automation that combines product research, video analysis, and storyboard extraction into a single workflow. Accepts product search criteria and returns complete competitive analysis with viral product insights, video breakdowns, and content replication guides.

## When to Use

- User wants comprehensive competitive analysis for TikTok Shop products
- User needs end-to-end research: products → videos → storyboards → actionable insights
- User specifies research goal (emerging, trending, bestsellers, etc.) with category
- User wants structured markdown report for business decisions
- User needs scene-by-scene video breakdown for content replication

## The Process

1. **Extract research parameters** – Identify category, goal, date range, and analysis depth
2. **Initialize research automation** – Set up with API cookies configuration
3. **Run research workflow** – Execute with parameters and wait for results
4. **Generate competitive analysis report** – Create structured markdown output
5. **Review and act** – Analyze insights and make business decisions

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Red Flags

- Using this skill when you only need one component (use specific skills instead)
- Missing required parameters (category or goal must be specified)
- Setting unrealistic date ranges (can lead to empty or irrelevant results)
- Expecting real-time analysis (this is batch processing)

## Verification

- End-to-end workflow completes without intermediate errors
- Product research returns valid TikTok Shop product data
- Video analysis identifies top-performing videos for each product
- Storyboard extraction provides scene breakdowns and content ideas
- Generated report follows markdown format and contains all required sections

## Do not use this skill when

- User only needs product data (use kalodata-product-research)
- User only needs video analysis (use kalodata-video-analysis)
- User only needs storyboard extraction (use kalodata-storyboard-extract)
- Task is unrelated to TikTok Shop Indonesia market research

## Instructions

1. Extract research parameters from user request:
   - **category**: Product category (Fashion, Beauty, Electronics, etc.)
   - **goal**: Research goal (emerging, trending, bestsellers, low competition, etc.)
   - **dateRange**: Optional date range for analysis (defaults to last 30 days)
   - **depth**: Analysis depth (products | videos | full)

2. Initialize the research automation:
   ```typescript
   import { createResearchAutomation } from './index.js';
   
   const research = createResearchAutomation({
     cookies: 'SESSION=xxx; cf_clearance=yyy; ...',
   });
   // Or: export KALODATA_COOKIES="your_cookies"
   ```

3. Run research with parameters:
   ```typescript
   const result = await research.runResearch({
     category: 'Beauty',
     goal: 'trending',
     dateRange: { start: '2026-01-01', end: '2026-02-01' },
     depth: 'full',
   });
   ```

4. Generate and return the competitive analysis report:
   ```typescript
   const report = research.generateReport(result);
   console.log(report);
   ```

## Capabilities
This section covers capabilities for the kalodata-research-automation skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Product Research Integration
- Queries TikTok Shop Indonesia products by category
- AI-powered goal detection (emerging, trending, bestsellers, low competition)
- Calculates opportunity scores, competition levels, trend directions
- Returns processed products with revenue, creators, conversion rates

### Video Analysis Integration
- Enriches products with associated viral videos
- Identifies top-performing videos per product
- Extracts downloadable video URLs for further analysis
- Provides content type detection (original vs autocut)

### Storyboard Extraction Integration
- Triggers AI storyboard generation for top videos
- Extracts scene-by-scene breakdowns with timing
- Analyzes camera work and key success factors
- Auto-generates 5 content angles for replication

### Competitive Analysis Report Generation
- Structured markdown output for business users
- Executive summary with top recommendations
- Product-by-product analysis with opportunity scores
- Video success factors and replication guidelines
- Scene-by-scene breakdown with camera work recommendations
- Auto-generated content ideas for each product

## Research Goals

| Goal | Description | Best For |
|------|-------------|----------|
| emerging | New products with rising trends | Finding the next big thing |
| trending | Currently popular products | Quick wins |
| bestsellers | Proven top performers | Low-risk decisions |
| low competition | Niche products with few creators | Easy ranking opportunities |
| high margin | Best commission rates | Maximizing earnings |

## Analysis Depth

| Depth | Products | Videos | Storyboards | Use Case |
|-------|----------|--------|-------------|----------|
| products | ✓ | ✗ | ✗ | Quick market overview |
| videos | ✓ | ✓ | ✗ | Video marketing insights |
| full | ✓ | ✓ | ✓ | Complete competitive analysis |

## Output Format

The skill generates a structured markdown report containing:

1. **Executive Summary** - Top 3 product recommendations
2. **Product Analysis** - Each product with metrics and scores
3. **Video Insights** - What made videos successful (key_to_success)
4. **Scene Breakdown** - Step-by-step video structure for replication
5. **Camera Recommendations** - Specific techniques to use
6. **Content Ideas** - Auto-generated angles for each product

## Environment Variables

- `KALODATA_SESSION` - Kalodata session cookie
- `KALODATA_CF_CLEARANCE` - Cloudflare clearance token

## Dependencies

This skill combines and extends:
- kalodata-product-research: Product discovery and analysis
- kalodata-video-analysis: Video intelligence extraction  
- kalodata-storyboard-extract: Scene breakdown and content ideas

## Example Usage

```typescript
// Full competitive analysis
const result = await research.runResearch({
  category: 'Beauty',
  goal: 'trending',
  depth: 'full',
  topProducts: 5,
});

const report = research.generateReport(result);
// Returns comprehensive markdown report
```

## API Reference
| Endpoint/Method | Description |
|----------------|-------------|
| `GET /status` | Check service health and availability |
| `POST /execute` | Run the primary operation |
| `GET /results` | Retrieve operation results |
| `DELETE /cache` | Clear cached data |


### ResearchAutomation

**`createResearchAutomation(options)`** - Factory function
- `options.session`: Kalodata session cookie
- `options.cfClearance`: Cloudflare clearance token
- `options.country`: Country code (default: ID)
- `options.currency`: Currency code (default: IDR)

**`runResearch(params)`** - Main research entry point
- `params.category`: Product category name or ID
- `params.goal`: Research goal (emerging, trending, etc.)
- `params.dateRange`: Optional date range
- `params.depth`: Analysis depth (products | videos | full)
- `params.topProducts`: Number of products to analyze (default: 5)

**`generateReport(data)`** - Generate markdown report
- `data`: Result from runResearch
- Returns formatted markdown string

**`updateCredentials(session, cfClearance)`** - Update auth credentials

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
