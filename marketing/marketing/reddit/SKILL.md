---
name: reddit
description: Post, comment, search, and monitor Reddit via browser CDP automation. No API key needed — uses existing browser session cookies. Use when posting to Reddit, reading hot posts, checking inbox, searching subreddits, or replying to comments. Parallel-safe (each call uses isolated tab).
---
persona:
  name: "Domain Expert"
  title: "Master of Reddit"
  expertise: ['Marketing Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# Reddit CLI Skill

Automates Reddit via the OpenClaw browser CDP session. No OAuth app, no API key — auth via browser session cookies + modhash.

## Architecture

```
reddit-cli → CDP WebSocket → browser tab (isolated, auto-created + closed) → reddit.com fetch() with credentials
```

**Why CDP instead of direct HTTP:**
Reddit's Cloudflare blocks server-side TLS connections (SSL handshake failure from server IP).
All requests must go through the browser which has a legitimate TLS fingerprint.

**Parallel safety:**
Each `reddit-cli` invocation opens a DEDICATED new tab (PUT /json/new), navigates to reddit.com,
runs all operations, then closes the tab in a `finally` block. Multiple agents can run simultaneously.

## Auth Flow
1. Open fresh tab → navigate to `https://www.reddit.com/api/me.json`
2. Extract `name` + `modhash` from JSON response (session cookies auto-attached by browser)
3. Use `modhash` as `X-Modhash` header for write operations (POST/vote)
4. All fetch() calls use `credentials: 'include'` to attach session cookies

**Note:** `token_v2` is HttpOnly — not accessible via JS. modhash is sufficient for all API operations.

## Requirements
- OpenClaw browser running with Reddit logged in (`u/berkahkarya_dev`)
- `websocket-client` pip package (system-wide)
- Python 3.x

## Binary & Files
- Binary: `~/.npm-global/bin/reddit-cli` → calls `skills/reddit/reddit_cli.py`
- Script: `~/.openclaw/workspace/skills/reddit/reddit_cli.py`

## Commands

```bash
# Account info
reddit-cli me

# Submit text post
reddit-cli post LocalLLaMA \
  --title "My post title" \
  --body "Post body here" \
  --flair "Resources"

# Submit link post
reddit-cli post LocalLLaMA --title "Check this" --link "https://example.com"

# Comment on a post
reddit-cli comment "https://reddit.com/r/LocalLLaMA/comments/abc123/..." --body "Great post!"

# Reply to a comment (by comment ID or t1_ ID)
reddit-cli reply t1_abc123 --body "Thanks!"

# Search a subreddit
reddit-cli search LocalLLaMA --query "Qwen abliterated" --sort top --limit 10

# Hot posts
reddit-cli hot MachineLearning --limit 5

# Check inbox/mentions
reddit-cli inbox --limit 10

# Upvote a post
reddit-cli upvote "https://reddit.com/r/LocalLLaMA/comments/abc123/..."
```

## CDP Key Notes
- WebSocket: `websocket.create_connection(url, suppress_origin=True)` — required, any origin header = 403
- New tab: `PUT http://127.0.0.1:18810/json/new`
- Close tab: `GET http://127.0.0.1:18810/json/close/{targetId}`
- CDP port: 18810 (OpenClaw browser)

## Active Reddit Account
- Username: `u/berkahkarya_dev`
- Active subreddits: r/LocalLLaMA, r/MachineLearning

## Good Subreddits for AI/ML Posting
| Subreddit | Focus | Members |
|-----------|-------|---------|
| r/LocalLLaMA | Local models, Ollama, GGUF, abliteration | 1M |
| r/MachineLearning | Research, papers | 2.8M |
| r/ArtificialIntelligence | General AI | 1M |
| r/deeplearning | DL research | 200K |
| r/learnmachinelearning | Beginner-friendly | 300K |
| r/singularity | AGI/future AI | 900K |

## Posting Best Practices
- Always set flair (required in most technical subs)
- Post 9AM–12PM EST on weekdays for max visibility
- r/LocalLLaMA loves: model releases, hardware benchmarks, "I built X on Y GPU"
- Mention exact GPU model and VRAM — community cares about accessibility
- Link HuggingFace/GitHub directly in post body
- Respond to comments within first hour (affects algorithmic boost)
