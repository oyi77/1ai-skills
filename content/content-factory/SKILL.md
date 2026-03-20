---
name: multi-agent-content-factory
description: >
  3-agent content factory: ResearchAgent (trending topics via duckduckgo + twitter),
  WritingAgent (articles/captions via OmniRoute LLM), ThumbnailAgent (image prompts
  for NanoBanana/Seedream). Orchestrated pipeline outputs content + PostBridge payload.
version: "1.0.0"
author: BerkahKarya AI
tags: [content, multi-agent, research, writing, thumbnail, postbridge, automation]
parent: content-kingdom
---

# Multi-Agent Content Factory

## Overview

Three specialized subagents orchestrated by a coordinator to produce publish-ready content:

1. **ResearchAgent** — Finds trending topics via DuckDuckGo search + twitter-cli
2. **WritingAgent** — Generates articles, captions, and scripts via OmniRoute LLM
3. **ThumbnailAgent** — Creates image generation prompts for NanoBanana/Seedream

## Pipeline

```
Research → Writing → Thumbnail → PostBridge Payload
```

## Usage

```bash
# Full pipeline — topic research → content → thumbnail prompt
python3 scripts/content_factory.py run --topic "AI trading bots"

# Research only
python3 scripts/content_factory.py research --topic "crypto trends"

# Write content from research
python3 scripts/content_factory.py write --input research_output.json

# Generate thumbnail prompt
python3 scripts/content_factory.py thumbnail --title "5 AI Trading Secrets"
```

## Configuration

- **LLM**: OmniRoute at `http://localhost:20128/v1` (api_key: `omniroute`)
- **Twitter**: Uses twitter-cli via `TWITTER_AUTH_TOKEN` / `TWITTER_CT0`
- **Image Gen**: Prompts formatted for NanoBanana / Seedream pipelines

## Output

JSON with all artifacts:

```json
{
  "research": { "trending_topics": [...], "sources": [...] },
  "content": { "title": "...", "body": "...", "caption": "...", "hashtags": [...] },
  "thumbnail": { "prompt": "...", "style": "..." },
  "postbridge_payload": { "text": "...", "media_prompt": "...", "schedule": "..." }
}
```
