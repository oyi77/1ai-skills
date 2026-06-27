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
# Agent Reach

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

## Overview

Agent Reach implements a Model Context Protocol server for Model Context Protocol.

## Architecture

- **Server** — MCP-compliant server exposing tools and resources
- **Transport** — stdio or HTTP transport layer
- **Tools** — Callable functions with JSON Schema definitions
- **Resources** — Readable data sources with URI-based access

## Setup

1. Install the MCP server package
2. Configure environment variables and credentials
3. Register the server in MCP client configuration
4. Test tool invocations and resource access

## Configuration

- Server name and version
- Transport type (stdio, SSE, HTTP)
- Tool definitions with input/output schemas
- Resource URI patterns
- Authentication and rate limiting

## Integration

- Compatible with Claude, Cursor, and other MCP clients
- Supports streaming responses for large payloads
- Handles errors with standard MCP error codes

