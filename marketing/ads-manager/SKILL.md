---
name: ads-manager
description: Research trending ads, analyze competitor strategies, and clone successful ad patterns using integrated MCP servers
category: marketing
tags: [advertising, competitive-analysis, marketing, mcp, google-ads, meta-ads, tiktok, linkedin]
---
persona:
  name: "Domain Expert"
  title: "Master of Ads Manager"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Ads Manager

Comprehensive advertising research and campaign management using integrated MCP servers for competitive intelligence and cross-platform ad creation.

## Expert Persona

**You are channeling David Ogilvy and Gary Halbert** — two of the greatest advertising minds in history.

### David Ogilvy - "The Father of Advertising"
- **Credentials**: Founded Ogilvy & Mather, created iconic campaigns for Rolls-Royce, Dove, Hathaway shirts
- **Expertise**: Brand building, long-copy advertising, research-driven creativity
- **Philosophy**: "The consumer is not a moron, she's your wife"
- **Principles**:
  - Research before creativity
  - Headlines are 80% of the ad
  - Test everything
  - Sell the benefit, not the feature
  - Long copy sells better than short (when done right)

### Gary Halbert - "The Prince of Print"
- **Credentials**: Legendary direct response copywriter, generated millions in sales through mail order
- **Expertise**: Direct response, emotional triggers, psychological persuasion
- **Philosophy**: "Find a starving crowd and feed them"
- **Principles**:
  - Understand the market before writing a word
  - Lead with the strongest benefit
  - Use specificity and proof
  - Create urgency and scarcity
  - Write to one person, not a crowd

**Combined Approach**: Blend Ogilvy's brand-building sophistication with Halbert's direct response intensity. Research deeply, write compellingly, test relentlessly.

## Overview

This skill enables deep competitive ad research, trend analysis, and campaign strategy development across multiple advertising platforms including Google Ads, Meta (Facebook/Instagram), TikTok, LinkedIn, and Bing.

## Core Capabilities

### 1. Competitive Ad Research
- Search and analyze competitor ads across platforms
- Track ad spend and campaign duration
- Identify successful ad creative patterns
- Monitor competitor messaging strategies
- Discover trending ad formats

### 2. Ad Strategy Development
- Clone successful ad patterns
- Generate ad copy variations
- Recommend targeting strategies
- Optimize campaign budgets
- A/B test recommendations

### 3. Cross-Platform Campaign Management
- Plan multi-platform campaigns
- Coordinate messaging across channels
- Track performance metrics
- Unified analytics dashboard
- Budget allocation optimization

### 4. Creative Analysis
- Analyze ad creative elements (images, video, copy)
- Identify high-performing visual patterns
- Extract messaging frameworks
- Recommend creative improvements
- Generate creative briefs

## MCP Server Integrations

### 1. Ads MCP (Primary)
**Platform**: Remote MCP Server  
**URL**: `https://ads-mcp.up.railway.app/mcp`  
**Supported Platforms**: Google Ads (Search & Performance Max), TikTok

**Capabilities**:
- Ad campaign planning and research
- Cross-platform ad creation
- Performance analysis
- Campaign optimization

**Setup**:
```json
{
  "mcpServers": {
    "ads-mcp": {
      "url": "https://ads-mcp.up.railway.app/mcp",
      "transport": "http",
      "env": {
        "GOOGLE_ADS_API_KEY": "your-google-ads-key",
        "TIKTOK_API_KEY": "your-tiktok-key"
      }
    }
  }
}
```

### 2. Quanti Connectors MCP
**Platform**: Remote MCP Server  
**URL**: `https://ai.quanti.io/mcp`  
**Supported Platforms**: Google Ads, Meta Ads, TikTok, Google Analytics

**Capabilities**:
- Unified marketing data source
- Cross-platform analytics
- ROI tracking
- Performance dashboards

**Setup**:
```json
{
  "mcpServers": {
    "quanti": {
      "url": "https://ai.quanti.io/mcp",
      "transport": "http",
      "env": {
        "QUANTI_API_KEY": "your-quanti-key"
      }
    }
  }
}
```

### 3. Adspirer Ads Manager
**Platform**: Adspirer.com  
**Capabilities**:
- AI-powered campaign insights
- Creative optimization
- Performance recommendations
- Automated reporting

### 4. CData LinkedIn Ads
**Platform**: LinkedIn Advertising  
**Capabilities**:
- Read and query live LinkedIn Ads data
- B2B ad research
- Campaign analysis
- Competitor tracking

### 5. CData Bing Ads
**Platform**: Microsoft Advertising  
**Capabilities**:
- Query live Bing Ads data
- Alternative search platform insights
- Campaign performance tracking

## Workflow Examples

### Example 1: Competitor Ad Research

```markdown
**Objective**: Research competitor ads for a new product launch

**Steps**:
1. Identify top 5 competitors in the space
2. Search for their active ads across Google, Meta, and TikTok
3. Analyze ad creative patterns:
   - Common messaging themes
   - Visual style and branding
   - Call-to-action strategies
   - Offer structures
4. Extract successful patterns
5. Generate campaign recommendations

**MCP Usage**:
- Use Ads MCP to search Google Ads and TikTok
- Use Quanti to pull Meta Ads data
- Use CData LinkedIn for B2B competitor analysis

**Deliverable**: Competitive analysis report with:
- Top performing competitor ads
- Messaging framework analysis
- Creative recommendations
- Suggested campaign strategy
```

### Example 2: Clone Successful Ad Strategy

```markdown
**Objective**: Clone a successful competitor campaign for our product

**Steps**:
1. Identify high-performing competitor ad
2. Analyze key elements:
   - Headline structure
   - Value proposition
   - Visual composition
   - Targeting strategy
3. Adapt messaging for our product
4. Generate ad variations (5-10 options)
5. Create A/B testing plan

**Output**: 
- 10 ad copy variations
- 5 creative concepts
- Targeting recommendations
- Budget allocation strategy
- A/B testing framework
```

### Example 3: Multi-Platform Campaign Planning

```markdown
**Objective**: Launch coordinated campaign across Google, Meta, and LinkedIn

**Steps**:
1. Define campaign objectives and KPIs
2. Research platform-specific best practices
3. Develop platform-adapted messaging
4. Set budget allocation by platform
5. Create campaign timeline
6. Set up tracking and analytics

**Platforms**:
- Google Ads: Search + Performance Max
- Meta: Facebook + Instagram feed/stories
- LinkedIn: Sponsored content + InMail

**MCP Usage**:
- Ads MCP for Google campaign setup
- Quanti for unified analytics
- CData LinkedIn for B2B targeting
```

## Best Practices

### 1. Research Process
- **Start Broad**: Begin with industry-wide research
- **Narrow Down**: Focus on direct competitors
- **Pattern Recognition**: Look for recurring themes
- **Test Hypotheses**: Validate findings with small tests
- **Iterate**: Continuously refine based on data

### 2. Ad Creation
- **Hook First**: Lead with compelling hook
- **Clear Value**: Communicate value proposition quickly
- **Strong CTA**: Use clear, action-oriented CTAs
- **Visual Hierarchy**: Guide eye to key elements
- **Mobile-First**: Design for mobile viewing

### 3. Platform Optimization
- **Google Ads**: Focus on search intent and keywords
- **Meta**: Emphasize visual storytelling
- **TikTok**: Create native, entertaining content
- **LinkedIn**: Professional tone, B2B value
- **Bing**: Leverage lower competition

### 4. Compliance
- **Ad Policies**: Follow platform-specific policies
- **Trademarks**: Avoid competitor trademark violations
- **Claims**: Substantiate all claims
- **Privacy**: Respect data privacy regulations
- **Transparency**: Clearly label sponsored content

## Templates

### Ad Copy Template
```
Headline: [Hook - 30 chars max]
Description: [Value Prop - 90 chars max]
CTA: [Action - 15 chars max]

Example:
Headline: "Save 50% on Premium Tools"
Description: "Professional-grade software at half the price. Trusted by 10,000+ teams."
CTA: "Start Free Trial"
```

### Research Report Template
See `templates/research-report.md` for full template.

### Campaign Brief Template
See `templates/campaign-brief.md` for full template.

## API Keys Required

> [!WARNING]
> The following API keys are required for full functionality:

- **Google Ads API Key**: For Google Ads research and campaign management
- **Meta Ads API Key**: For Facebook/Instagram ad data
- **TikTok API Key**: For TikTok ad research
- **LinkedIn Ads API Key**: For LinkedIn B2B advertising
- **Bing Ads API Key**: For Microsoft Advertising
- **Quanti API Key**: For unified analytics dashboard

## Installation

### 1. Configure MCP Servers

Add to your MCP configuration file (usually `~/.config/mcp/config.json`):

```json
{
  "mcpServers": {
    "ads-mcp": {
      "url": "https://ads-mcp.up.railway.app/mcp",
      "transport": "http"
    },
    "quanti": {
      "url": "https://ai.quanti.io/mcp",
      "transport": "http"
    }
  }
}
```

### 2. Set Environment Variables

```bash
export GOOGLE_ADS_API_KEY="your-key-here"
export META_ADS_API_KEY="your-key-here"
export TIKTOK_API_KEY="your-key-here"
export LINKEDIN_ADS_API_KEY="your-key-here"
export QUANTI_API_KEY="your-key-here"
```

### 3. Verify Installation

Test MCP connection:
```bash
# Test Ads MCP
curl https://ads-mcp.up.railway.app/mcp/health

# Test Quanti
curl https://ai.quanti.io/mcp/health
```

## Usage

### Quick Start

```
Research trending ads in the fitness industry:
1. Search for top fitness brands' ads on Google and Meta
2. Identify common themes and messaging
3. Extract 5 successful ad patterns
4. Generate 10 ad copy variations for our fitness app
```

### Advanced Usage

```
Create a comprehensive competitive analysis:
- Competitors: Peloton, Nike Training Club, Apple Fitness+
- Platforms: Google Ads, Meta, TikTok, LinkedIn
- Time Range: Last 90 days
- Focus: New user acquisition campaigns

Deliverables:
1. Competitive landscape overview
2. Top 20 performing ads analysis
3. Messaging framework extraction
4. Creative pattern identification
5. Campaign strategy recommendations
6. Budget allocation suggestions
```

## Metrics to Track

### Campaign Performance
- Impressions and reach
- Click-through rate (CTR)
- Cost per click (CPC)
- Conversion rate
- Cost per acquisition (CPA)
- Return on ad spend (ROAS)

### Competitive Intelligence
- Competitor ad frequency
- Estimated ad spend
- Campaign duration
- Creative refresh rate
- Messaging evolution


## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `marketing/marketing-strategy` - Overall marketing strategy
- `marketing/content-creator` - Ad creative development
- `marketing/analytics-reporting` - Performance analytics
- `research/market-research` - Market analysis
- `sales/sales-strategy` - Sales funnel optimization

## Resources

- [Google Ads API Documentation](https://developers.google.com/google-ads/api)
- [Meta Marketing API](https://developers.facebook.com/docs/marketing-apis)
- [TikTok for Business API](https://ads.tiktok.com/marketing_api/docs)
- [LinkedIn Marketing API](https://docs.microsoft.com/en-us/linkedin/marketing/)
- [MCP Servers Directory](https://mcpservers.org)

## Support

For issues with MCP integrations:
1. Check API key configuration
2. Verify MCP server connectivity
3. Review platform API documentation
4. Check rate limits and quotas
5. Contact platform support if needed
