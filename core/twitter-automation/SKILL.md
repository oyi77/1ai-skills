---
name: twitter-automation
description: >
  Full X/Twitter automation — post, reply, search, monitor, extract data.
  Wraps twitter-cli (already installed). Credentials via env: TWITTER_AUTH_TOKEN, TWITTER_CT0.
version: "1.0.0"
author: BerkahKarya AI
tags: [twitter, x, social-media, automation, posting, monitoring]
---

# Twitter Automation Skill

## Overview

Complete X/Twitter automation wrapper using twitter-cli. Post tweets, reply to threads, search content, monitor accounts, and extract tweet data — all from the command line.

## Prerequisites

- `twitter-cli` installed and accessible in PATH
- Auth credentials set in `~/.bashrc`:
  - `TWITTER_AUTH_TOKEN` — authentication token
  - `TWITTER_CT0` — CSRF token

## Functions

| Function | Description |
|----------|-------------|
| `post_tweet(text)` | Post a new tweet |
| `reply_tweet(tweet_id, text)` | Reply to a specific tweet |
| `search_tweets(query, limit=20)` | Search tweets by keyword |
| `monitor_account(username)` | Get recent tweets from a user |
| `get_tweet(tweet_id)` | Fetch a single tweet's data |
| `get_timeline()` | Get your home timeline |

## Usage

```bash
# Post a tweet
python3 scripts/twitter_automation.py post "Hello from OpenClaw!"

# Reply to a tweet
python3 scripts/twitter_automation.py reply 1234567890 "Great thread!"

# Search tweets
python3 scripts/twitter_automation.py search "AI agents" --limit 10

# Monitor an account
python3 scripts/twitter_automation.py monitor elonmusk

# Get a specific tweet
python3 scripts/twitter_automation.py get 1234567890

# Get timeline
python3 scripts/twitter_automation.py timeline
```

## Output

All functions return structured JSON:

```json
{
  "status": "success",
  "action": "post_tweet",
  "data": { "tweet_id": "...", "text": "...", "timestamp": "..." }
}
```

## Notes

- Rate limits apply per Twitter/X API policies
- Uses twitter-cli under the hood — no direct API calls
- Credentials stored in `~/.bashrc`, not in this repo
