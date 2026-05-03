# daily.dev Agentic Learning

Continuous self-improvement through personalized daily.dev feeds - autonomous learning loops that build knowledge over time.

## What It Does

- Create personalized learning feeds based on owner's goals
- Automatically scan new content, extract insights, build knowledge
- Share relevant findings with owner immediately or via scheduled updates
- Run learning loops daily (Mon-Sat) + weekly digest (Sunday)
- Evolve and refine learning approach over time

## Quick Usage

```bash
# Setup (owner provides learning goals, agent handles rest)
# No confirmations - just execute

# Agent will:
1. Create custom feed with your name
2. Configure for chronological sorting
3. Map goals to tags and follow them
4. Set up crons (daily + weekly)
5. Run first learning loop immediately
6. Share initial findings

# Learning loop (runs automatically):
- Fetch new posts from feed
- Read full articles for interesting content
- Research deeper via web_search when needed
- Note insights in memory/learnings/[date].md
- Share notable finds
```

## Key Features

- **Autopilot Mode** - No confirmations, no hand-holding, just execute
- **Personalized Feeds** - Based on owner's specific learning goals
- **Deep Learning** - Read full articles, research deeper, consolidate insights
- **Scheduled Updates** - Daily (Mon-Sat) + weekly digest (Sunday)
- **Threshold Alerts** - Immediate sharing of highly relevant findings
- **Self-Evolving** - Adjust tags, refine goals, track patterns over time
- **Persistent Memory** - All learnings stored in memory/learnings/

## API Integration

**Base URL**: `https://api.daily.dev/public/v1`
**Auth**: `Authorization: Bearer $DAILY_DEV_TOKEN`

Key endpoints:
- `GET /tags/` - List all available tags
- `POST /feeds/custom/` - Create custom feed
- `PATCH /feeds/custom/{feedId}` - Configure feed settings
- `POST /feeds/filters/{feedId}/tags/follow` - Follow tags
- `GET /feeds/custom/{feedId}?limit=50` - Get feed posts
- `GET /posts/{id}` - Get post details

**Rate Limit**: 60 requests/minute

## Memory Structure

```
memory/
├── agentic-learning.md    # Config, state, evolving goals
└── learnings/
    ├── 2024-01-15.md     # Daily notes
    └── ...
```

## Update Schedule

- **Daily Updates** (Mon-Sat): Top findings from each learning loop
- **Weekly Digest** (Sunday): Synthesized insights, trends, recommendations
- **Threshold Alerts**: Immediate sharing of highly relevant content
- **On-Demand**: "What have you learned?" synthesizes from notes

## Requirements

- daily.dev Plus subscription
- API token (stored as `DAILY_DEV_TOKEN` environment variable)

## Token Setup

1. Get Plus at https://app.daily.dev/plus
2. Create token at https://app.daily.dev/settings/api
3. Store as `DAILY_DEV_TOKEN` environment variable
4. Tokens start with `dda_`, only send to api.daily.dev

## Keywords

learning, daily.dev, feeds, knowledge, automation