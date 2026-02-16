# MCP Setup Guide

Complete guide for installing and configuring Model Context Protocol (MCP) servers for the 1ai-skills repository.

## Overview

This guide covers the installation and configuration of 20+ MCP servers organized by division to enhance AI agent capabilities across Marketing, Sales, Productivity, and Research functions.

## Quick Start

### 1. Install High-Priority MCPs

```bash
# Marketing - Ads MCP (Remote)
# No installation needed, configure in MCP config

# Sales - HubSpot MCP
npx @sheffieldp/mcp-hubspot

# Productivity - Notion MCP
npx @makenotion/mcp-server

# Research - Apify MCP (Remote)
# No installation needed, configure in MCP config
```

### 2. Configure MCP Config File

Create or edit `~/.config/mcp/config.json`:

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
    },
    "apify": {
      "url": "https://mcp.apify.com",
      "transport": "http"
    },
    "hubspot": {
      "command": "npx",
      "args": ["@sheffieldp/mcp-hubspot"]
    },
    "notion": {
      "command": "npx",
      "args": ["@makenotion/mcp-server"]
    },
    "slack": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-slack"]
    },
    "firecrawl": {
      "command": "npx",
      "args": ["@firecrawl/mcp-server"]
    },
    "exa": {
      "command": "npx",
      "args": ["@exa/mcp-server"]
    }
  }
}
```

### 3. Set Environment Variables

Create `~/.mcp_env` file:

```bash
# Marketing MCPs
export GOOGLE_ADS_API_KEY="your-google-ads-key"
export META_ADS_API_KEY="your-meta-ads-key"
export TIKTOK_API_KEY="your-tiktok-key"
export LINKEDIN_ADS_API_KEY="your-linkedin-key"
export BING_ADS_API_KEY="your-bing-key"
export QUANTI_API_KEY="your-quanti-key"

# Sales MCPs
export HUBSPOT_API_KEY="your-hubspot-key"
export ATTIO_API_KEY="your-attio-key"
export GHL_API_KEY="your-gohighlevel-key"

# Productivity MCPs
export NOTION_API_KEY="your-notion-key"
export SLACK_BOT_TOKEN="your-slack-token"
export GOOGLE_CLOUD_CREDENTIALS="/path/to/credentials.json"

# Research MCPs
export APIFY_API_TOKEN="your-apify-token"
export FIRECRAWL_API_KEY="your-firecrawl-key"
export EXA_API_KEY="your-exa-key"
export SERPAPI_KEY="your-serpapi-key"
```

Then source it:
```bash
echo "source ~/.mcp_env" >> ~/.zshrc
source ~/.mcp_env
```

## Installation by Division

### Marketing Division

#### 1. Ads MCP (High Priority)
**Platforms**: Google Ads, TikTok  
**Type**: Remote Server  
**Installation**: No local installation required

```json
{
  "ads-mcp": {
    "url": "https://ads-mcp.up.railway.app/mcp",
    "transport": "http",
    "env": {
      "GOOGLE_ADS_API_KEY": "${GOOGLE_ADS_API_KEY}",
      "TIKTOK_API_KEY": "${TIKTOK_API_KEY}"
    }
  }
}
```

**Verification**:
```bash
curl https://ads-mcp.up.railway.app/mcp/health
```

#### 2. Quanti Connectors (High Priority)
**Platforms**: Google Ads, Meta, TikTok, Google Analytics  
**Type**: Remote Server

```json
{
  "quanti": {
    "url": "https://ai.quanti.io/mcp",
    "transport": "http",
    "env": {
      "QUANTI_API_KEY": "${QUANTI_API_KEY}"
    }
  }
}
```

**Verification**:
```bash
curl https://ai.quanti.io/mcp/health
```

#### 3. CData LinkedIn Ads (Medium Priority)
**Platform**: LinkedIn  
**Use Case**: B2B advertising research

#### 4. CData Bing Ads (Low Priority)
**Platform**: Microsoft Advertising  
**Use Case**: Alternative search platform insights

---

### Sales Division

#### 1. HubSpot MCP (High Priority)
**Installation**:
```bash
npx @sheffieldp/mcp-hubspot
```

**Configuration**:
```json
{
  "hubspot": {
    "command": "npx",
    "args": ["@sheffieldp/mcp-hubspot"],
    "env": {
      "HUBSPOT_API_KEY": "${HUBSPOT_API_KEY}"
    }
  }
}
```

**Use Cases**:
- CRM automation
- Contact management
- Deal pipeline tracking
- Sales workflow automation

#### 2. Attio MCP (Medium Priority)
**Platform**: AI-native CRM  
**Use Cases**: Modern CRM integration, relationship management

#### 3. Nineteen Blocks Sales Automation (Medium Priority)
**Integrations**: Gmail, Google Sheets, Streak CRM, Notion, Google Drive  
**Use Cases**: Multi-tool workflow automation

#### 4. GoHighLevel MCP (Medium Priority)
**Platform**: All-in-one business platform  
**Use Cases**: CRM, marketing automation, client management

---

### Productivity Division

#### 1. Notion MCP (High Priority)
**Installation**:
```bash
npx @makenotion/mcp-server
```

**Configuration**:
```json
{
  "notion": {
    "command": "npx",
    "args": ["@makenotion/mcp-server"],
    "env": {
      "NOTION_API_KEY": "${NOTION_API_KEY}"
    }
  }
}
```

**Use Cases**:
- Knowledge base management
- Project documentation
- Database automation
- Team wiki integration

#### 2. Slack MCP (High Priority)
**Installation**:
```bash
npx @modelcontextprotocol/server-slack
```

**Configuration**:
```json
{
  "slack": {
    "command": "npx",
    "args": ["@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}"
    }
  }
}
```

**Use Cases**:
- Team communication automation
- Message analysis
- Channel management
- Workflow automation

#### 3. Google Cloud MCP (Medium Priority)
**Use Cases**: Cloud resource management, infrastructure automation

#### 4. Tldv MCP (Medium Priority)
**Platforms**: Google Meet, Zoom, Microsoft Teams  
**Use Cases**: Meeting transcription, action item extraction, automated note-taking

#### 5. Linear MCP (Medium Priority)
**Use Cases**: Issue tracking, sprint planning, project management

---

### Research Division

#### 1. Apify MCP (High Priority)
**Type**: Remote Server  
**Installation**: No local installation required

```json
{
  "apify": {
    "url": "https://mcp.apify.com",
    "transport": "http",
    "env": {
      "APIFY_API_TOKEN": "${APIFY_API_TOKEN}"
    }
  }
}
```

**Use Cases**:
- Web scraping and automation
- Social media monitoring
- Competitive intelligence
- Data extraction

**Verification**:
```bash
curl https://mcp.apify.com/health
```

#### 2. Firecrawl MCP (High Priority)
**Installation**:
```bash
npx @firecrawl/mcp-server
```

**Configuration**:
```json
{
  "firecrawl": {
    "command": "npx",
    "args": ["@firecrawl/mcp-server"],
    "env": {
      "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
    }
  }
}
```

**Use Cases**:
- Website data extraction
- Content scraping
- Automated research

#### 3. Exa MCP (Medium Priority)
**Installation**:
```bash
npx @exa/mcp-server
```

**Use Cases**:
- AI-powered search
- Research automation
- Content discovery

#### 4. SerpApi MCP (Medium Priority)
**Use Cases**: SERP analysis, keyword research, competitor tracking

#### 5. Scrapeless MCP (Low Priority)
**Platforms**: Google Search, Flight, Map, Jobs  
**Use Cases**: Real-time search data, local search analysis

---

## Obtaining API Keys

### Marketing Platforms

#### Google Ads API
1. Go to [Google Ads API Center](https://ads.google.com/home/tools/api-center/)
2. Create a developer token
3. Set up OAuth 2.0 credentials
4. Enable Google Ads API

#### Meta Ads API
1. Visit [Meta for Developers](https://developers.facebook.com/)
2. Create an app
3. Add Marketing API product
4. Generate access token

#### TikTok Ads API
1. Go to [TikTok for Business](https://ads.tiktok.com/marketing_api/docs)
2. Apply for API access
3. Create app and get credentials

#### LinkedIn Ads API
1. Visit [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Create an app
3. Request Marketing API access
4. Generate access token

### Sales Platforms

#### HubSpot API
1. Log in to [HubSpot](https://app.hubspot.com/)
2. Go to Settings → Integrations → API Key
3. Generate private app access token

### Productivity Platforms

#### Notion API
1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Create new integration
3. Copy Internal Integration Token
4. Share pages with integration

#### Slack API
1. Visit [Slack API](https://api.slack.com/apps)
2. Create new app
3. Add bot token scopes
4. Install app to workspace
5. Copy Bot User OAuth Token

### Research Platforms

#### Apify API
1. Sign up at [Apify](https://apify.com/)
2. Go to Settings → Integrations
3. Generate API token

#### Firecrawl API
1. Sign up at [Firecrawl](https://firecrawl.dev/)
2. Go to API Keys section
3. Generate new API key

#### Exa API
1. Sign up at [Exa](https://exa.ai/)
2. Navigate to API section
3. Generate API key

---

## Verification & Testing

### Test MCP Connectivity

```bash
# Test remote MCPs
curl https://ads-mcp.up.railway.app/mcp/health
curl https://ai.quanti.io/mcp/health
curl https://mcp.apify.com/health

# Test local MCPs (if running)
# They should respond when invoked by the AI agent
```

### Test with AI Agent

```
Test the ads-mcp integration:
1. Search for Nike ads on Google Ads
2. Return the top 5 ads
3. Analyze their messaging patterns
```

### Common Issues

#### Issue: MCP server not found
**Solution**: Verify MCP config path and JSON syntax

#### Issue: API key not working
**Solution**: Check environment variables are set and exported

#### Issue: Permission denied
**Solution**: Verify API key has required scopes/permissions

#### Issue: Rate limit exceeded
**Solution**: Implement rate limiting in your requests

---

## Best Practices

### 1. Security
- Store API keys in environment variables, never in code
- Use separate keys for development and production
- Rotate keys regularly
- Limit API key permissions to minimum required

### 2. Performance
- Cache MCP responses when appropriate
- Implement retry logic for transient failures
- Monitor API usage and quotas
- Use batch operations when available

### 3. Maintenance
- Document which skills use which MCPs
- Keep track of API key expiration dates
- Monitor MCP server health
- Update MCP packages regularly

### 4. Cost Management
- Understand pricing for each MCP/API
- Set up billing alerts
- Monitor usage patterns
- Optimize API calls

---

## Skill-to-MCP Mapping

| Skill | Required MCPs | Optional MCPs |
|-------|---------------|---------------|
| `marketing/ads-manager` | Ads MCP, Quanti | CData LinkedIn, CData Bing |
| `sales/sales-strategy` | HubSpot | Attio, GoHighLevel |
| `productivity/google-workspace` | Google Cloud | - |
| `productivity/email-automation` | - | Nineteen Blocks |
| `productivity/calendar-management` | - | Tldv |
| `research/mckinsey-research` | Apify, Firecrawl | Exa, SerpApi |

---

## Troubleshooting

### Enable Debug Logging

```bash
export MCP_DEBUG=true
export MCP_LOG_LEVEL=debug
```

### Check MCP Logs

```bash
# View MCP server logs
tail -f ~/.mcp/logs/mcp-server.log
```

### Validate Configuration

```bash
# Validate MCP config JSON
cat ~/.config/mcp/config.json | jq .
```

---

## Support Resources

- [MCP Servers Directory](https://mcpservers.org)
- [MCP Protocol Documentation](https://modelcontextprotocol.io)
- Platform-specific API documentation (see links above)
- Skill-specific SKILL.md files for detailed integration guides

---

## Next Steps

1. ✅ Install high-priority MCPs (Ads, HubSpot, Notion, Apify)
2. ✅ Configure MCP config file
3. ✅ Set environment variables
4. ✅ Obtain required API keys
5. ✅ Test connectivity
6. ✅ Test with AI agent
7. ✅ Install medium-priority MCPs as needed
8. ✅ Document any custom configurations

---

**Last Updated**: 2026-02-16  
**Version**: 1.0.0
