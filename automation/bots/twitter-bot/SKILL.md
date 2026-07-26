---
name: twitter-bot
description: Use when twitter/X bot automation for content posting, engagement, and lead generation. See parent skill for full docs.
domain: automation
tags:
- automation
- bot
- twitter
- social-media
version: 1.0.0
---
# Twitter Bot

## Quick Reference

Twitter/X bots automate posting, engagement (like/retweet/follow), DM responses, and content curation via the Twitter API v2. The key distinction from the parent bots skill is focus: this skill covers *only* Twitter/X — its unique API constraints, rate limits, monetization patterns, and growth mechanics.

## Overview

A Twitter bot is an automated account that publishes tweets, engages with followers, and runs campaigns 24/7. Unlike Telegram or WhatsApp bots (covered in the parent skill), Twitter bots face write limits (300/day for most accounts), short content (280-4000 chars via API), and growth challenges without media attachment boosts. The money comes from automated affiliate threads, lead magnet DMs, and engagement farming — all driven by the Twitter API v2 via OAuth 2.0.

## Quick Start

**Prerequisites:** Twitter Developer Account (Elevated access), project created in Developer Portal, OAuth 2.0 credentials with PKCE.

1. **Generate credentials** — Go to Developer Portal → your project → "Keys and tokens" → generate OAuth 2.0 Client ID + Client Secret, then generate Access Token + Secret for a single-account bot.

2. **Install & authenticate** — `pip install tweepy` then set environment variables for `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`.

3. **Post first tweet** — Run the one-shot script below. If you get 403 Forbidden, check that your app has `tweet.write` scope and the access token was regenerated after scoping.

```python
import tweepy, os

client = tweepy.Client(
    bearer_token=os.environ.get("TWITTER_BEARER_TOKEN"),
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"]
)

# Post tweet with media (higher engagement)
media = client.media_upload(filename="deal.png")
tweet = client.create_tweet(
    text="🔥 Deal alert: 50% off automation tools!\n\nGrab it here: https://lynk.id/deal123",
    media_ids=[media.media_id]
)
print(f"Posted: https://twitter.com/user/status/{tweet.data['id']}")

# Reply to @mentions with auto-DM redirect
mentions = client.get_users_mentions(
    id=os.environ["TWITTER_USER_ID"],
    max_results=10
)
if mentions.data:
    for m in mentions.data:
        client.create_tweet(
            text="Thanks! DM me for exclusive deals →",
            in_reply_to_tweet_id=m.id
        )
```

## Checklist

- [ ] Twitter Developer Account has **Elevated** (not Essential) access — Essential cannot read mentions or DM
- [ ] OAuth 2.0 app has `tweet.write`, `tweet.read`, `users.read`, `dm.read`, `dm.write` scopes enabled
- [ ] Rate limits tracked: 300 tweets/day account-level, 15 requests/15 min per endpoint; use `tweepy.Paginator` with `max_results` to avoid 429s
- [ ] Media uploaded via `media_upload()` before tweeting (tweets with images get 3x more engagement)
- [ ] DM automation uses `create_dm()` with explicit user opt-in — Twitter bans aggressive auto-DM within hours

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll grow organically then automate" | Without automation, growth takes 6-12 months to reach monetization scale; a good bot pipeline achieves the same in weeks |
| "Auto-DM is fine for lead gen" | Twitter's spam detection flags DMs sent to non-followers immediately; always DM only users who interacted first (liked/RT'd) |
| "Twitter API v2 is too restrictive" | v2 gives you 500K tweets/month at the Basic tier ($100/mo) — cheaper than a VA; the free Essential tier handles lead-gen scale for most solo bots |

## When to Use
Use this skill when working with twitter bot.

## Workflow
See the parent skill for authoritative workflow documentation.
