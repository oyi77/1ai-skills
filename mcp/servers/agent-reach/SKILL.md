---
name: agent-reach
description: Universal internet scraper for AI agents. Read and search Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu,
  LinkedIn, V2EX, RSS, web pages. Zero API fees. Use when agents need real-time social media data, content research, or trend
  monitoring.
domain: mcp
tags:
- agent
- ai-agent
- api
- github
- mcp-server
- model-context-protocol
- monitoring
- reach
---

# Agent Reach MCP

Universal internet access for AI agents — Twitter, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, LinkedIn, V2EX, RSS, web pages. One CLI, zero API fees. 35K+ GitHub stars.

**Source**: [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)

## When to Use

- Scrape Twitter tweets, threads, search results without API keys
- Read Reddit posts, comments, subreddit feeds
- Get YouTube video transcripts and metadata
- Scrape XiaoHongShu (Little Red Book) posts
- Monitor Bilibili video content
- Search across platforms for competitive intelligence
- Gather social proof and sentiment data
- Research trending content for viral creation
- **When NOT to use**: When you already have API access (use native tools), when the platform blocks scraping ethically, when data doesn't need real-time freshness

## Install

```bash
# Via pipx (recommended)
pipx install https://github.com/Panniantong/agent-reach/archive/main.tar.gz

# Verify
agent-reach --version
```

**Supported platforms**: Python 3.10+

## Quick Setup

```bash
# First-time setup (installs upstream tools automatically)
agent-reach setup

# Health check
agent-reach doctor

# Configure specific platforms
agent-reach config twitter  # Twitter/X setup
agent-reach config reddit   # Reddit setup
agent-reach config youtube  # YouTube setup
```

## MCP Client Configuration

Add to your MCP client config (`~/.omp/mcp.json`, `~/.cursor/mcp.json`, etc.):

```json
{
  "mcpServers": {
    "agent-reach": {
      "command": "agent-reach",
      "args": ["mcp", "--stdio"]
    }
  }
}
```

## Available Tools

| Tool | Platform | Description |
|------|----------|-------------|
| `twitter_search` | Twitter/X | Search tweets by keyword, hashtag, or user |
| `twitter_user` | Twitter/X | Get user profile and recent tweets |
| `twitter_thread` | Twitter/X | Read full thread/conversation |
| `reddit_subreddit` | Reddit | Get posts from a subreddit |
| `reddit_search` | Reddit | Search Reddit for keywords |
| `reddit_post` | Reddit | Read full post with comments |
| `youtube_video` | YouTube | Get video metadata + transcript |
| `youtube_search` | YouTube | Search YouTube videos |
| `youtube_channel` | YouTube | Get channel info and recent videos |
| `github_repo` | GitHub | Get repo info, README, issues |
| `github_search` | GitHub | Search repos, code, issues |
| `xhs_search` | XiaoHongShu | Search Little Red Book posts |
| `xhs_post` | XiaoHongShu | Read full post content |
| `bilibili_video` | Bilibili | Get video metadata + transcript |
| `linkedin_profile` | LinkedIn | Get public profile info |
| `v2ex_topic` | V2EX | Read forum topic and replies |
| `rss_feed` | RSS | Read RSS/Atom feeds |
| `web_page` | Web | Read any web page as clean text |
| `web_search` | Web | Multi-engine web search |

## Usage Patterns

### Twitter Research
```bash
agent-reach twitter search "AI agent framework" --limit 20
agent-reach twitter user @OpenAI
agent-reach twitter thread https://x.com/user/status/123456
```

### Reddit Deep Dive
```bash
agent-reach reddit subreddit MachineLearning --sort hot --limit 25
agent-reach reddit search "vector database" --subreddit LocalLLaMA
agent-reach reddit post https://reddit.com/r/MachineLearning/comments/abc123
```

### YouTube Transcript Extraction
```bash
agent-reach youtube video "https://youtube.com/watch?v=abc123" --transcript
agent-reach youtube search "LLM fine-tuning tutorial" --limit 10
agent-reach youtube channel "@AndrejKarpathy" --recent 10
```

### Cross-Platform Search
```bash
agent-reach search "prompt engineering best practices" --platforms twitter,reddit,youtube
```

## Data Output

All tools output structured JSON by default. For agent-friendly text:
```bash
agent-reach twitter search "query" --format text
agent-reach youtube video "url" --transcript --format markdown
```

## Common Workflows

### Competitive Intelligence
1. `twitter_search` for competitor brand mentions
2. `reddit_subreddit` for product discussions
3. `youtube_search` for review videos
4. Aggregate sentiment across platforms

### Content Research
1. `twitter_search` for trending hooks in niche
2. `reddit_subreddit` for pain points and questions
3. `youtube_video` for transcript analysis of top videos
4. Feed findings into content creation skills

### Market Research
1. `web_search` for industry reports
2. `twitter_search` for real-time sentiment
3. `reddit_search` for user feedback
4. `xhs_search` for Chinese market intel (XiaoHongShu)

## Platform-Specific Notes

| Platform | Auth Required | Rate Limits | Notes |
|----------|---------------|-------------|-------|
| Twitter | Cookie-based | ~50 req/min | Uses OpenCLI, no API key needed |
| Reddit | Optional | 60 req/min | Works without auth for public content |
| YouTube | No | Generous | yt-dlp backend, transcripts via API |
| XiaoHongShu | Cookie-based | ~30 req/min | Requires login cookies |
| Bilibili | No | Generous | Public content accessible |
| GitHub | Optional | 60/hr unauthenticated | Use `gh` CLI for authenticated access |
| LinkedIn | Cookie-based | Strict | Public profiles only |
| Web | No | Varies | Uses readability for clean extraction |

## Upstream Tools

Agent-reach is an installer/router — it sets up these upstream tools:
- **OpenCLI** — Twitter scraping
- **twitter-cli** — Alternative Twitter client
- **rdt-cli** — Reddit CLI
- **yt-dlp** — YouTube downloader
- **bili-cli** — Bilibili CLI
- **mcporter** — XiaoHongShu scraper
- **gh CLI** — GitHub access

Agent-reach installs, health-checks, and routes to these tools. After setup, you can use them directly.

## Verification

- [ ] `agent-reach --version` works
- [ ] `agent-reach doctor` passes platform checks
- [ ] MCP server configured in client
- [ ] `agent-reach twitter search "test"` returns results
- [ ] `agent-reach youtube video "url" --transcript` works

## Overview

> Section content — see SKILL.md body for full details.
