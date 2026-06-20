---
name: social-intelligence
description: Cross-platform social media intelligence gathering using Agent Reach. Research trends, sentiment, competitive intel, and user insights from Twitter, Reddit, YouTube, XiaoHongShu across 35+ platforms. Use when researching social proof, market sentiment, viral content patterns, or competitive positioning.
domain: research
tags: [social-media, research, sentiment-analysis, competitive-intelligence, trend-monitoring, agent-reach]
---

# Social Intelligence

Cross-platform social media intelligence gathering. Research trends, sentiment, competitive intel, and user insights from Twitter, Reddit, YouTube, XiaoHongShu, and 30+ more platforms using Agent Reach as the data backbone.

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

## Prerequisites

1. **Agent Reach MCP server** — see `skill://agent-reach`
2. Configured platforms (run `agent-reach setup`)
3. Platform-specific auth cookies (for Twitter, XiaoHongShu, LinkedIn)

## Workflow

### 1. Define Intelligence Goal

```markdown
What are we researching?
- [ ] Brand sentiment (positive/negative/neutral breakdown)
- [ ] Competitive positioning (feature comparison, pricing mentions)
- [ ] User pain points (complaints, feature requests)
- [ ] Viral content patterns (hooks, formats, engagement drivers)
- [ ] Trend validation (is this real or noise?)
- [ ] Influencer landscape (who drives conversation?)
```

### 2. Platform Selection Matrix

| Goal | Primary | Secondary | Tertiary |
|------|---------|-----------|----------|
| US consumer sentiment | Twitter/X | Reddit | YouTube |
| Chinese market intel | XiaoHongShu | Bilibili | Weibo |
| Developer feedback | Reddit | HackerNews | GitHub |
| Visual product reviews | YouTube | Instagram | TikTok |
| Tech early adopters | Twitter/X | ProductHunt | HackerNews |
| Enterprise feedback | LinkedIn | Twitter/X | G2 Crowd |

### 3. Data Collection

**Cross-platform search:**
```bash
agent-reach search "your query" \
  --platforms twitter,reddit,youtube \
  --limit 50 \
  --format json \
  --output data.json
```

**Platform-specific deep dive:**
```bash
# Twitter - real-time sentiment
agent-reach twitter search "product name" --limit 100

# Reddit - detailed user discussions
agent-reach reddit search "product name" --subreddit technology,Entrepreneur

# YouTube - video sentiment and transcript analysis
agent-reach youtube search "product review" --limit 20
```

### 4. Sentiment Analysis

For each platform's data:
1. Categorize: positive / neutral / negative / mixed
2. Extract themes: what are people saying?
3. Quantify: volume, engagement, reach
4. Identify influencers: who drives the conversation?

**Example aggregation:**
```python
# Pseudo-code for sentiment breakdown
results = {
    "twitter": {"positive": 45, "neutral": 30, "negative": 25, "total": 100},
    "reddit": {"positive": 35, "neutral": 40, "negative": 25, "total": 80},
    "youtube": {"positive": 60, "neutral": 25, "negative": 15, "total": 40}
}

# Weighted average by platform reach
overall_sentiment = calculate_weighted_sentiment(results)
```

### 5. Intelligence Report

**Template:**

```markdown
# Social Intelligence Report: [Topic/Product]
Date: [YYYY-MM-DD]
Platforms: Twitter, Reddit, YouTube
Sample: [N posts/videos/comments]

## Executive Summary
- Overall sentiment: [Positive/Negative/Mixed] ([X]% positive)
- Key finding: [One-sentence insight]
- Recommendation: [Action item]

## Sentiment Breakdown
| Platform | Positive | Neutral | Negative | Volume |
|----------|----------|---------|----------|--------|
| Twitter  | 45%      | 30%     | 25%      | 100    |
| Reddit   | 35%      | 40%     | 25%      | 80     |
| YouTube  | 60%      | 25%     | 15%      | 40     |

## Top Themes
1. **[Theme 1]** — mentioned [N] times
   - Quote: "[representative quote]"
   - Platforms: Twitter, Reddit
2. **[Theme 2]** — mentioned [M] times
   - Quote: "[representative quote]"
   - Platforms: YouTube, Reddit

## Pain Points
- [Pain point 1] — [frequency]
- [Pain point 2] — [frequency]

## Competitive Positioning
- [Competitor A]: mentioned [N] times, [sentiment]
- [Competitor B]: mentioned [M] times, [sentiment]
- Your Product: mentioned [X] times, [sentiment]

## Viral Content Patterns
- Hook type: [e.g., "Before/After transformation"]
- Format: [e.g., "Short-form video with captions"]
- Engagement driver: [e.g., "Relatable pain point"]

## Influencers
1. [@username] — [follower count], [engagement rate], [relevance score]
2. [@username] — [follower count], [engagement rate], [relevance score]

## Recommendations
1. [Actionable insight based on findings]
2. [Actionable insight based on findings]

## Raw Data
[Link to JSON export or artifact://]
```

## Platform-Specific Strategies

### Twitter/X Intelligence
**Best for:** Real-time sentiment, viral hooks, influencer discovery
```bash
# Competitive mentions
agent-reach twitter search "competitor OR 'competitor name'" --limit 200

# Trend validation
agent-reach twitter search "#trendingtopic" --since 24h --limit 100

# Influencer discovery
agent-reach twitter search "niche keyword" --min-followers 10000
```

**Analysis focus:**
- Engagement patterns (retweets, likes, quote tweets)
- Sentiment velocity (positive/negative shift over time)
- Influencer amplification (who drives reach?)

### Reddit Deep Research
**Best for:** Detailed user feedback, pain points, community sentiment
```bash
# Subreddit sentiment
agent-reach reddit subreddit ProductName --sort hot --limit 50

# Problem discovery
agent-reach reddit search "frustrated with [category]" --limit 100

# Feature requests
agent-reach reddit search "wish [product] had" --limit 100
```

**Analysis focus:**
- Comment depth (how much discussion?)
- Upvote/downvote ratio (community agreement?)
- Recurring themes across threads

### YouTube Content Analysis
**Best for:** In-depth product reviews, tutorial quality, video sentiment
```bash
# Review roundup
agent-reach youtube search "product review" --limit 20 --transcript

# Tutorial landscape
agent-reach youtube search "how to use product" --limit 15 --transcript

# Competitor comparison
agent-reach youtube search "product A vs product B" --transcript
```

**Analysis focus:**
- Transcript sentiment (positive/negative language)
- Pain points mentioned in reviews
- Feature requests in comments
- Video engagement (views, likes, comment count)

### XiaoHongShu (Chinese Market Intel)
**Best for:** Chinese consumer sentiment, visual product discovery, lifestyle trends
```bash
# Product sentiment in China
agent-reach xhs search "产品名称" --limit 50

# Category research
agent-reach xhs search "类别 推荐" --limit 100
```

**Analysis focus:**
- Visual content patterns (what photos/videos work?)
- Comment sentiment (Chinese consumer preferences)
- Price sensitivity mentions
- KOL (Key Opinion Leader) influence

## Integration with Other Skills

### Content Creation Pipeline
1. **Social Intelligence** (this skill) → identify viral hooks
2. `skill://viral-content-creator` → generate content variations
3. `skill://content-scheduler` → schedule across platforms
4. `skill://analytics-dashboard` → track performance

### Market Research Stack
1. **Social Intelligence** → qualitative sentiment
2. `skill://mckinsey-research` → quantitative market analysis
3. `skill://competitive-intelligence` → structured competitor analysis
4. Report synthesis → strategic recommendations

### Product Development Feedback Loop
1. **Social Intelligence** → user pain points
2. `skill://triage-issue` → file GitHub issues
3. `skill://to-prd` → convert to PRD
4. `skill://subagent-driven-development` → delegate implementation

## Advanced Patterns

### Sentiment Trend Tracking
Monitor sentiment over time (weekly snapshots):
```bash
# Week 1
agent-reach search "product" --platforms twitter,reddit --output week1.json

# Week 2
agent-reach search "product" --platforms twitter,reddit --output week2.json

# Compare: sentiment shift? volume change? new themes?
```

### Competitive Moat Analysis
```bash
# Your product mentions
agent-reach search "your product" --limit 200 > yours.json

# Competitor mentions
agent-reach search "competitor" --limit 200 > competitor.json

# Compare: sentiment, feature mentions, pricing discussions
```

### Influencer Outreach List
```bash
# Find influencers talking about your niche
agent-reach twitter search "niche keyword" --min-followers 5000 --limit 50

# Export to CSV: username, followers, engagement, recent tweets
# Use with skill://influencer-outreach for personalized DMs
```

## Red Flags

- **Bot spam detected** — filter out automated/fake accounts before analysis
- **Small sample size** (<50 mentions) — sentiment unreliable, need more data
- **Echo chamber** — single subreddit/community dominates, not representative
- **Outdated data** — social trends decay fast, data >1 week old loses value
- **Platform bias** — Reddit skews tech-savvy, Twitter skews early adopters, adjust interpretation

## Verification Checklist

- [ ] Agent Reach MCP server running (`agent-reach doctor` passes)
- [ ] Platform auth configured (Twitter cookies, XHS login if needed)
- [ ] Sample size >50 per platform for reliable sentiment
- [ ] Sentiment categorization consistent across platforms
- [ ] Raw data exported and linked in report
- [ ] Influencers validated (real accounts, not bots)
- [ ] Recommendations actionable and specific

## Related Skills

- `skill://agent-reach` — MCP server installation and config
- `skill://trendradar` — 35+ platform trend monitoring (complementary)
- `skill://competitive-intelligence` — structured competitor analysis
- `skill://mckinsey-research` — market sizing and TAM analysis
- `skill://viral-content-creator` — convert insights to content
- `skill://twitter-automation` — automate Twitter engagement
- `skill://seo-optimizer` — convert social insights to SEO keywords
