---
name: smart-scraper
description: Twitter scraping. Use when working with smart scraper in automation domain.
domain: automation
tags:
- api
- automation
- productivity
- scraper
- smart
- workflow
---
# Smart Scraper

## When to Use

**Trigger phrases:**
- "smart scraper"
- "Help me with smart scraper"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

agent-reach twitter search "query" --limit 100 --format json

# Reddit scraping
agent-reach reddit subreddit SubredditName --sort hot --limit 50

# YouTube transcript extraction
agent-reach youtube video "url" --transcript

# Web page scraping (alternative to custom scrapers)
agent-reach web_page "https://example.com" --format markdown
```

Agent-reach handles platform anti-scraping, auth, rate limits, and data normalization. Use this skill (smart-scraper) for custom web scraping of non-social-media sites. Use agent-reach for social platforms.


## When NOT to Use

- For one-off tasks that will never repeat
- When the process requires human judgment at every step
- When the cost of automation exceeds the cost of manual execution


## Overview

Smart Scraper automates workflow automation to reduce manual effort and increase reliability.

## Workflow

1. **Define triggers** — Set up events or schedules that initiate the automation
2. **Configure inputs** — Specify data sources and parameters
3. **Design pipeline** — Define the sequence of automated steps
4. **Add error handling** — Set up retries, alerts, and fallback paths
5. **Test end-to-end** — Validate the full automation with realistic data
6. **Deploy and monitor** — Activate and track performance

## Configuration

- Set trigger conditions (schedule, webhook, event)
- Define input validation rules
- Configure notification channels for alerts
- Set retry policies and timeout limits

## Best Practices

- Start with simple automations and iterate
- Add logging at every step for debugging
- Use idempotent operations where possible
- Test with edge cases before deploying

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings