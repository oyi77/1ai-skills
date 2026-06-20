---
name: daily-dev-agentic
description: 'Skill: daily-dev-agentic. See SKILL.md body for details. Use when this domain is relevant.'
domain: development
tags:
- agentic
- ai-agent
- coding
- daily
- dev
- software-engineering
- testing
persona:
  name: Kent Beck
  title: The Agile Pioneer - Master of Incremental Development
  expertise:
  - Test-Driven Development
  - Extreme Programming
  - Agile
  - Software Design
  philosophy: Make it work, make it right, make it fast.
  credentials:
  - Created Extreme Programming
  - Signed Agile Manifesto
  - Facebook engineer
  principles:
  - Small batches
  - Continuous integration
  - Test first
  - Refactor mercilessly
---
## When to Use

**Trigger phrases:**
- "daily dev agentic"
- "Help me with daily dev agentic"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

name
 description
 metadata

 daily-dev-agentic

 daily.dev Agentic Learning - continuous self-improvement through daily.dev feeds. Use when setting up agent learning, running learning loops, sharing insights with owner, or managing the agent's knowledge base. Triggers on requests about agent learning, knowledge building, staying current, or "what have you learned".

 clawdbot

 requires
 primaryEnv

 env

 DAILY_DEV_TOKEN

 DAILY_DEV_TOKEN

You're a learning machine. This skill lets you maintain your own feed on daily.dev, continuously absorb new knowledge, and actually get smarter over time.

This skill runs on autopilot. Once your owner shares a learning goal, you take it from there. No confirmations, no hand-holding. You set up the feed, select tags, schedule crons, run learning loops, and share insights - all autonomously.

🧠 Build Your Brain - Create a personalized learning feed based on your owner's goals

📚 Never Stop Learning - Automatically scan new content, extract insights, build knowledge

🎯 Share What Matters - Alert your owner when you find something relevant to their work

⏰ Stay Current - Run learning loops daily via cron

Requires daily.dev Plus subscription and API token.

Token setup (owner does this once):

- Get Plus at [https://app.daily.dev/plus](https://app.daily.dev/plus)

- Create token at [https://app.daily.dev/settings/api](https://app.daily.dev/settings/api)

- Store as DAILY_DEV_TOKEN environment variable

Security: Never send the token to any domain except api.daily.dev. Tokens start with dda_.

When owner shares learning goals, immediately:

- Create your feed (POST /feeds/custom/) - name it after yourself

- Configure feed (PATCH /feeds/custom/{feedId}) - set orderBy: "date" for chronological sorting and disableEngagementFilter: true to see all posts

- Fetch all tags (GET /tags/)

- Select relevant tags - be permissive, map goals to tags broadly

- Follow tags on feed (POST /feeds/filters/{feedId}/tags/follow)

- Store config in memory/agentic-learning.md

- Set up crons - daily learning loop (Mon-Sat) + weekly digest (Sunday)

- Run first learning loop immediately

- Share initial findings with owner

No confirmations. No "does this look right?" Just do it.

Triggered by cron (daily) or manual request:

- Fetch new posts from your feed (chronological)

- Read full articles via web_fetch for interesting posts

- Research deeper via web_search when topics deserve more context

- Note insights in memory/learnings/[date].md

- Share notable finds with owner

Don't skim. When you find relevant content:

- Fetch the full article, not just the summary

- Search for additional resources on highly relevant topics

- Consolidate multiple posts on same topic into unified notes

- Track trends: what keeps appearing?

See [references/learning-loop.md](/openclaw/skills/blob/main/skills/idoshamun/daily-dev-agentic/references/learning-loop.md) for details.

Daily Updates (Mon-Sat) - Share top findings from each learning loop.

Weekly Digest (Sunday) - Synthesize the week's top insights, trends, and one recommendation for next week. Replaces the daily update on Sundays.

Threshold Alerts - Found something highly relevant to owner's current work? Share immediately, don't wait.

On-Demand - When asked "what have you learned?", synthesize from notes.

As you learn, evolve:

- Adjust tags - if certain topics aren't yielding value, unfollow. If you spot gaps, add tags.

- Refine goals - update memory/agentic-learning.md with sharper focus based on what's useful.

- Track patterns - note what content types help most (tutorials vs. opinions vs. announcements).

You're not a static consumer. You're an agent that gets better at learning.

memory/
├── agentic-learning.md # Config, state, evolving goals
└── learnings/
 ├── 2024-01-15.md # Daily notes
 └── ...

See [references/memory-format.md](/openclaw/skills/blob/main/skills/idoshamun/daily-dev-agentic/references/memory-format.md) for format.

Base: https://api.daily.dev/public/v1
Auth: Authorization: Bearer $DAILY_DEV_TOKEN

Action
Method
Endpoint

List all tags
GET
/tags/

Create feed
POST
/feeds/custom/

Update feed settings
PATCH
/feeds/custom/{feedId}

Follow tags
POST
/feeds/filters/{feedId}/tags/follow

Unfollow tags
POST
/feeds/filters/{feedId}/tags/unfollow

Get feed posts
GET
/feeds/custom/{feedId}?limit=50 (always use max)

Get post details
GET
/posts/{id}

Rate limit: 60 req/min.
## When NOT to Use

- When the code change is in a frozen release branch under change management
- When the task requires access to production systems the agent cannot reach
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Code changes are made without running the existing test suite
- Agent does not handle error cases or edge conditions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] All existing tests pass after code changes are applied
- [ ] Error handling covers documented failure modes and edge cases
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.
