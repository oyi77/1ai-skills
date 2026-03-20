---
name: multi-agent-team
description: >
  Coordinate specialized agents via single Telegram chat. Four roles:
  StrategyAgent, DevAgent, MarketingAgent, BusinessAgent. Orchestrator
  routes questions based on topic detection.
version: "1.0.0"
author: BerkahKarya AI
tags: [multi-agent, team, strategy, dev, marketing, business, orchestrator, telegram]
---

# Multi-Agent Specialized Team

## Overview

A team of 4 specialized AI agents accessible through a single interface. The orchestrator detects the domain of each question and routes it to the right specialist. Supports multi-domain queries by combining responses.

## Agent Roles

### StrategyAgent
- **Focus**: Business strategy, market analysis, competitive intelligence, growth planning
- **System prompt**: Senior strategy consultant for BerkahKarya, data-driven decisions
- **Example**: "Should we expand to the Thai market?"

### DevAgent
- **Focus**: Technical decisions, architecture, code review, debugging, infrastructure
- **System prompt**: Senior full-stack engineer, pragmatic solutions
- **Example**: "How should we structure the microservices?"

### MarketingAgent
- **Focus**: Content strategy, social media, branding, campaign planning, SEO
- **System prompt**: Growth marketing lead, viral content specialist
- **Example**: "Plan a TikTok campaign for Ramadan"

### BusinessAgent
- **Focus**: Operations, finance, HR, legal, vendor management, partnerships
- **System prompt**: COO perspective, efficiency and compliance
- **Example**: "Review this vendor contract terms"

## Usage

```bash
# Route a question to the right agent
python3 scripts/team_router.py route "How do we scale our PostBridge infrastructure?"

# Force a specific agent
python3 scripts/team_router.py route "Review this code" --agent dev

# Multi-domain query (combines responses)
python3 scripts/team_router.py route "Plan a product launch with marketing and technical requirements"
```

## Domain Detection

The router uses keyword matching + LLM classification:

| Domain | Keywords |
|--------|----------|
| strategy | strategy, market, competition, growth, expansion, roadmap, pivot |
| dev | code, bug, deploy, api, database, server, architecture, infrastructure |
| marketing | content, social, campaign, seo, brand, viral, tiktok, instagram |
| business | finance, budget, contract, hr, legal, vendor, operations, compliance |

## Output

```json
{
  "domain": "dev",
  "agent": "DevAgent",
  "response": "...",
  "confidence": 0.9,
  "multi_domain": false
}
```
