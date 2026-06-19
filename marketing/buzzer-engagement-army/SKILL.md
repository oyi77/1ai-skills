---
name: buzzer-engagement-army
description: "Multi-account engagement booster across TikTok, Instagram, and Facebook — automates likes, comments, and warmup schedules to beat algorithm suppression on new posts."
domain: marketing
---
# SKILL: buzzer-engagement-army

> Multi-account engagement system for BerkahKarya social media.
> Boosts initial post engagement to beat algorithm suppression.
> 12 accounts: 7 TikTok + 1 Instagram + 4 Facebook.

## When to Use

- New post just went live → needs initial engagement in first 30 min
- Posts getting buried with zero reach → emergency boost
- Launching a campaign → prime the algorithm pump
- Routine daily maintenance → keep all posts getting signal

## Architecture

```
engagement_coordinator.py  ← MAIN ENTRY POINT
      ↓ coordinates
  like_bot.py              ← handles like actions
  comment_bot.py           ← handles comment actions (with comment_library.py)
      ↓ both use
  account_manager.py       ← tracks limits, warmup state
  warmup_manager.py        ← enforces warmup schedule
  engagement_scheduler.py  ← generates staggered timing
      ↓ reads
  comment_library.py       ← 200+ natural Indonesian comments
```

## Quick Start

```bash
cd ~/.openclaw/workspace/skills/1ai-skills/marketing/buzzer-engagement-army/scripts/

# 1. Check system status
python engagement_coordinator.py --status

# 2. Run tests first (always!)
python test_buzzer.py

# 3. Dry run to preview
python engagement_coordinator.py --boost-latest --dry-run

# 4. PRODUCTION: Boost latest posts
python engagement_coordinator.py --boost-latest

# 5. Boost specific post
python engagement_coordinator.py --post-id POST_ID --platform tiktok
```

## PostBridge API

```
Base: https://api.post-bridge.com/v1
Key:  REDACTED_ROTATED_CREDENTIAL
Auth: Bearer token in Authorization header

Endpoints used:
  GET /posts           → fetch published posts
  GET /post-results    → get platform post IDs
  GET /social-accounts → verify account connections
  POST /analytics/sync → refresh engagement counts
```

## Connected Accounts

| Platform  | Count | Account IDs                                    |
|-----------|-------|------------------------------------------------|
| TikTok    | 7     | 48374, 48373, 48372, 48338, 48337, 48336, 48335|
| Instagram | 1     | 48186                                          |
| Facebook  | 4     | 48178, 48177, 48176, 48175                     |

## Engagement Pattern (Natural)

```
T+0:00   Account D → LIKE
T+2:37   Account A → LIKE (2m37s gap)
T+3:09   Account A → COMMENT (30-90s after like)
T+5:52   Account C → LIKE
T+6:41   Account C → COMMENT
T+8:11   Account B → LIKE
...
```

**Rules:**
- 2-5 minute gap between ACCOUNTS
- 30-90 second gap between LIKE and COMMENT from same account
- Never simultaneous (same-second) engagement
- Random jitter ±30% on all delays

## Warmup Schedule

| Phase  | Days | Actions/Day |
|--------|------|-------------|
| COLD   | 1-3  | 5           |
| WARM   | 4-7  | 15          |
| ACTIVE | 8+   | 30          |

State tracked in: `state/account_state.json`

## Comment Library

**200+ natural Indonesian comments across 7 niches:**
- health / lifestyle / tech / food / fashion / business / general

```python
from comment_library import get_comments_for_post
comments = get_comments_for_post("tips kesehatan harian", count=7)
# Returns 7 unique, niche-appropriate comments
```

## Files

| File                        | Purpose                                |
|-----------------------------|----------------------------------------|
| `engagement_coordinator.py` | Main orchestrator — run this           |
| `like_bot.py`               | Like action handler                    |
| `comment_bot.py`            | Comment action handler                 |
| `comment_library.py`        | 200+ Indonesian comments per niche     |
| `account_manager.py`        | Account state, warmup limits           |
| `warmup_manager.py`         | Warmup schedule enforcement            |
| `engagement_scheduler.py`   | Staggered timing generator             |
| `test_buzzer.py`            | Full test suite                        |
| `state/account_state.json`  | Per-account action tracking (auto-created) |
| `logs/coordinator.log`      | Action audit trail (auto-created)      |

## Production Workflow

1. **New post goes live** (via PostBridge)
2. Run: `python engagement_coordinator.py --boost-latest`
3. System fetches latest posts, identifies un-boosted ones
4. Generates staggered schedule across all 12 accounts
5. Executes: like → wait → comment per account
6. Logs everything to `logs/`
7. Triggers PostBridge analytics sync

## Automation (Cron)

```bash
# Boost new posts every 15 minutes during business hours
*/15 9-22 * * * cd ~/.openclaw/workspace/skills/1ai-skills/marketing/buzzer-engagement-army/scripts && python engagement_coordinator.py --boost-latest >> ../logs/cron.log 2>&1
```

## Testing

```bash
# Unit tests (fast, no API)
python test_buzzer.py

# With API connectivity tests
python test_buzzer.py --api

# Expected: All tests pass ✅
```

## Troubleshooting

**Account hit daily limit:**
→ Check `state/account_state.json` → reset if corrupted
→ Wait until midnight for auto-reset

**PostBridge API error:**
→ Check API key in env or hardcoded
→ Verify at https://api.post-bridge.com/reference

**Comments duplicating on same post:**
→ Check `logs/used_comments.json`
→ Library has 200+ comments, should rotate

**All accounts skipped:**
→ Warmup limits hit → normal behavior
→ Wait until next day or reduce action frequency

## References

- `references/engagement-strategies.md` — Full strategy guide
- PostBridge API: https://api.post-bridge.com/reference

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels
