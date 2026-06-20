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
## Smart Scraper

AI-powered web scraper

### Usage

```
/smart-scraper <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## When NOT to Use

- When the target website explicitly blocks scraping in robots.txt and terms of service
- When scraped data is used for purposes the site owner has not consented to
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Scraper ignores robots.txt directives and rate limits
- Agent does not handle JavaScript-rendered content properly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Scraper respects robots.txt and implements polite crawling
- [ ] Data is deduplicated and freshness is tracked
- [ ] All required outputs generated
- [ ] Success criteria met

## Agent Reach Integration

For social media scraping (Twitter, Reddit, YouTube, XiaoHongShu, Bilibili, LinkedIn), prefer `skill://agent-reach` over custom scrapers:

```bash
# Twitter scraping
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

## Additional Notes

### Best Practices
- Combine with related skills for comprehensive coverage
- Review the verification checklist after applying this skill
- Document patterns you discover for future use

### Troubleshooting
- If output quality is low, provide more context in your input
- If the skill does not cover your use case, check related skills
- For integration issues, verify prerequisites and dependencies are met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
