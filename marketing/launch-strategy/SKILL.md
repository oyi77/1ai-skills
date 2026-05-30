---
name: launch-strategy
description: Go-to-market planning — launch sequencing, channel strategy, audience building, PR outreach. Use when planning product launches, building launch checklists, or coordinating multi-channel campaigns.
---



# Launch Strategy

Plan and execute product launches with maximum impact.

## Capabilities

- Launch timeline and sequencing
- Channel strategy (social, email, PR, communities)
- Audience building pre-launch
- PR outreach and media kits
- Launch day checklist
- Post-launch optimization

## When to Use

- Planning a product launch
- Building a go-to-market strategy
- Coordinating multi-channel campaigns
- Creating launch checklists

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)


## Pseudo Code

The launch-strategy workflow follows a standard pipeline pattern.

Core flow:
```
# launch-strategy primary flow
input = prepare(raw_data)
result = process(input, config={audience, building, campaigns, channel, checklists})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# launch-strategy primary flow
input = prepare(raw_data)
result = process(input, config={audience, building, campaigns, channel, checklists})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Launch Timeline

```python
launch_plan = {
    "T-30": ["Build waitlist", "Create landing page", "Start content marketing"],
    "T-14": ["Seed to communities", "Prepare PR kit", "Schedule social posts"],
    "T-7": ["Beta user outreach", "Finalize launch assets", "Test all links"],
    "T-0": ["Launch on Product Hunt", "Send email blast", "Social blitz"],
    "T+1": ["Respond to all comments", "Share early metrics", "Thank supporters"],
    "T+7": ["Analyze metrics", "Follow up with leads", "Plan iteration"],
}
```

### Channel Strategy

```python
channels = {
    "product_hunt": {"prep": "7 days", "expected_traffic": "5K-50K"},
    "twitter": {"prep": "14 days", "strategy": "thread + engagement"},
    "email": {"prep": "3 days", "segment": "warm_leads"},
    "reddit": {"prep": "30 days", "strategy": "value_first_then_launch"},
    "hacker_news": {"prep": "0 days", "strategy": "Show HN post"},
}
```

### PR Kit

```markdown
## Press Kit
- One-liner: [What it does in 10 words]
- 3 bullet value prop
- Founder bio (2 sentences)
- High-res screenshots (3-5)
- Demo video (60s)
- Early traction metrics
```

## Common Patterns

- **Build audience first**: Waitlist before launch
- **Stack channels**: Product Hunt + Twitter + Email same day
- **Community seeding**: Reddit, Indie Hackers, niche forums 2 weeks before
- **Engagement**: Reply to every comment on launch day

## How to Use

1. Define campaign objective and target KPIs
2. Set up tracking and attribution (UTMs, pixels, events)
3. Create campaign assets (copy, creatives, landing pages)
4. Launch with small budget for testing
5. Monitor metrics daily, optimize underperformers
6. Scale winners, pause losers, document learnings

## Red Flags

- **Metrics declining 3+ days**: Investigate funnel leaks or audience fatigue
- **Ad spend with zero conversions**: Pause and review targeting/creative
- **Email open rates below 15%**: Subject lines or sender reputation issue
- **Bounce rate above 70%**: Landing page mismatch or slow load times
- **Attribution gaps**: Missing UTM parameters or broken tracking pixels
