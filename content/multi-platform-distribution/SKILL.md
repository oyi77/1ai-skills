---
name: multi-platform-distribution
description: One piece of content becomes 10 — blog to Twitter thread, LinkedIn article, YouTube script, newsletter, TikTok script, podcast outline, Reddit post
---



## Overview

Transform a single piece of content into platform-specific formats, schedule distribution across channels, and track performance. Saves 80% of content marketing time by automating the repurposing pipeline. One blog post becomes a Twitter thread, LinkedIn article, YouTube script, newsletter edition, TikTok script, podcast outline, Reddit post, and Hacker News submission — each optimized for its platform's audience and format.

## Required Tools

- `pandoc` for format conversion
- Python with `markdown` / `jinja2` for templating
- Twitter API v2 (now X API) for thread posting
- LinkedIn API for article publishing
- YouTube Data API for video metadata
- Substack/Beehiiv API for newsletter
- TikTok Content Posting API
- Reddit API for post submission
- Buffer/Hootsuite API for scheduling
- Google Analytics / Plausible for tracking

## Capabilities

- Parse source content into semantic blocks (intro, key points, examples, conclusion)
- Generate platform-specific versions respecting character limits, tone, and format
- Auto-generate Twitter threads with proper numbering and hooks
- Create LinkedIn posts with engagement-optimized structure
- Generate YouTube scripts with timestamps and B-roll suggestions
- Produce TikTok scripts with hook, value, CTA structure
- Schedule posts at optimal times per platform
- Track cross-platform performance in unified dashboard

## When to Use

- "I wrote a blog post, distribute it everywhere"
- "Turn this article into a Twitter thread and LinkedIn post"
- "Repurpose our latest podcast episode into 10 pieces of content"
- "Create a content calendar from our existing content library"
- "This newsletter issue should also go on LinkedIn and as a blog"

## Pseudo Code

The multi-platform-distribution workflow follows a standard pipeline pattern.

Core flow:
```
# multi-platform-distribution primary flow
input = prepare(raw_data)
result = process(input, config={article, becomes, blog, content, distribution})
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
# multi-platform-distribution primary flow
input = prepare(raw_data)
result = process(input, config={article, becomes, blog, content, distribution})
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


### Content Parsing

```python
def parse_content(source):
    """Break source content into semantic blocks."""
    blocks = {
        'title': extract_title(source),
        'hook': extract_first_paragraph(source),
        'key_points': extract_key_points(source),  # headings + first para
        'examples': extract_code_blocks_or_examples(source),
        'quotes': extract_notable_quotes(source),
        'stats': extract_statistics(source),
        'conclusion': extract_conclusion(source),
        'cta': extract_call_to_action(source),
        'word_count': count_words(source),
        'reading_time': count_words(source) // 200,
    }
    return blocks
```

### Platform Matrix

```python
PLATFORMS = {
    'twitter': {
        'char_limit': 280,
        'thread_max': 25,
        'format': 'thread',
        'tone': 'punchy, conversational',
        'best_time': '9am, 12pm, 5pm EST',
        'hashtags': 2,
    },
    'linkedin': {
        'char_limit': 3000,
        'format': 'post',
        'tone': 'professional, insightful',
        'best_time': 'Tuesday-Thursday 8-10am',
        'hashtags': 5,
        'line_breaks': True,  # LinkedIn needs double newlines
    },
    'youtube': {
        'format': 'script',
        'tone': 'educational, engaging',
        'optimal_length': '8-15 minutes',
        'sections': ['hook (0-30s)', 'intro (30s-2min)', 'main (2-10min)', 'outro (10-12min)'],
    },
    'tiktok': {
        'format': 'script',
        'tone': 'casual, fast-paced',
        'max_length': '60 seconds',
        'structure': ['hook (0-3s)', 'value (3-50s)', 'cta (50-60s)'],
    },
    'newsletter': {
        'format': 'email',
        'tone': 'personal, value-dense',
        'sections': ['subject_line', 'preview_text', 'intro', 'main', 'resources', 'cta'],
    },
    'reddit': {
        'format': 'post',
        'tone': 'authentic, no self-promotion',
        'subreddits': 'auto-detect relevant communities',
        'rules': 'no links in main post, provide full value inline',
    },
    'podcast': {
        'format': 'outline',
        'tone': 'conversational',
        'sections': ['cold_open', 'intro', 'talking_points', 'examples', 'takeaway', 'outro'],
    },
}
```

### Twitter Thread Generator

```python
def generate_twitter_thread(blocks):
    """Convert content blocks into a Twitter thread."""
    tweets = []

    # Hook tweet (first tweet gets engagement)
    hook = blocks['hook'][:250]
    tweets.append(f"🧵 {hook}\n\nA thread 👇")

    # Key points as individual tweets
    for i, point in enumerate(blocks['key_points'], 1):
        # Each tweet: number + point + supporting detail
        tweet = f"{i}/ {point['title']}\n\n{point['detail'][:200]}"

        # Add stats if available
        if blocks['stats'] and i <= len(blocks['stats']):
            tweet += f"\n\n📊 {blocks['stats'][i-1]}"

        tweets.append(tweet[:280])

    # Conclusion tweet
    tweets.append(f"TL;DR: {blocks['conclusion'][:250]}")

    # CTA tweet
    if blocks['cta']:
        tweets.append(blocks['cta'][:280])

    return tweets
```

### LinkedIn Post Generator

```python
def generate_linkedin_post(blocks):
    """Generate LinkedIn-optimized post with engagement hooks."""
    post = ""

    # Hook (first 2 lines are visible before "see more")
    post += blocks['hook'][:150] + "\n\n"

    # Key points with emoji bullets
    for point in blocks['key_points']:
        post += f"→ {point['title']}\n"
        post += f"  {point['detail'][:200]}\n\n"

    # Stats block
    if blocks['stats']:
        post += "📊 Key numbers:\n"
        for stat in blocks['stats'][:3]:
            post += f"• {stat}\n"
        post += "\n"

    # Conclusion + CTA
    post += blocks['conclusion'][:300] + "\n\n"

    # Hashtags (LinkedIn likes 3-5)
    post += "#startup #ai #productivity #growth #content"

    return post
```

### YouTube Script Generator

```python
def generate_youtube_script(blocks):
    """Generate YouTube video script with timestamps."""
    script = f"""# {blocks['title']}

## HOOK (0:00 - 0:30)
{blocks['hook']}

## INTRO (0:30 - 2:00)
- Problem statement
- Why this matters
- What viewers will learn

## MAIN CONTENT (2:00 - 10:00)
"""
    for i, point in enumerate(blocks['key_points']):
        script += f"""
### Point {i+1}: {point['title']} ({2 + i*2}:00 - {4 + i*2}:00)
- {point['detail']}
- Example: {blocks['examples'][i] if i < len(blocks['examples']) else 'Add specific example'}
- B-roll suggestion: [Show relevant screen/demo]
"""

    script += f"""
## CONCLUSION (10:00 - 11:00)
{blocks['conclusion'][:500]}

## CTA (11:00 - 11:30)
- Subscribe + notification bell
- Link in description
- {blocks['cta']}

## DESCRIPTION TEMPLATE
{blocks['title']}

Timestamps:
0:00 - Intro
2:00 - Key Point 1
...

Links mentioned:
- [relevant links]

#youtube #tutorial #howto
"""
    return script
```

### TikTok Script Generator

```python
def generate_tiktok_script(blocks):
    """Generate 60-second TikTok script."""
    script = {
        'hook': f"Stop scrolling. {blocks['hook'][:50]}",  # 0-3 seconds
        'value': [],  # 3-50 seconds
        'cta': blocks['cta'] or "Follow for more tips",  # 50-60 seconds
    }

    # Pack 3 key points into 47 seconds
    for point in blocks['key_points'][:3]:
        script['value'].append({
            'text': point['title'],
            'duration': '15s',
            'visual': f"[Show {point['title'].lower()} on screen]",
        })

    return script
```

### Scheduling

```python
from datetime import datetime, timedelta

def schedule_distribution(content_id, platforms, start_date):
    """Schedule posts across platforms at optimal times."""
    schedule = {}

    # Stagger releases — don't post everywhere at once
    offsets = {
        'twitter': 0,           # Day 0
        'linkedin': 0,          # Day 0 (different time)
        'newsletter': 1,        # Day 1
        'reddit': 2,            # Day 2
        'youtube': 3,           # Day 3
        'tiktok': 3,            # Day 3
        'podcast': 7,           # Day 7
    }

    best_times = {
        'twitter': '09:00',
        'linkedin': '08:30',
        'newsletter': '10:00',
        'reddit': '14:00',
        'youtube': '15:00',
        'tiktok': '19:00',
    }

    for platform in platforms:
        day = start_date + timedelta(days=offsets.get(platform, 0))
        time = best_times.get(platform, '12:00')
        schedule[platform] = f"{day.strftime('%Y-%m-%d')}T{time}:00"

    return schedule
```

### Performance Tracking

```python
def track_performance(content_id):
    """Aggregate performance metrics across platforms."""
    metrics = {}

    # Twitter
    metrics['twitter'] = {
        'impressions': get_twitter_impressions(content_id),
        'engagement_rate': get_twitter_engagement(content_id),
        'link_clicks': get_twitter_clicks(content_id),
    }

    # LinkedIn
    metrics['linkedin'] = {
        'views': get_linkedin_views(content_id),
        'reactions': get_linkedin_reactions(content_id),
        'comments': get_linkedin_comments(content_id),
    }

    # Website (from UTM parameters)
    metrics['website'] = {
        'sessions': get_analytics_sessions(f"utm_content={content_id}"),
        'conversions': get_analytics_conversions(f"utm_content={content_id}"),
    }

    # Total reach
    total_reach = sum(m.get('impressions', m.get('views', 0)) for m in metrics.values())
    metrics['summary'] = {
        'total_reach': total_reach,
        'best_platform': max(metrics.items(), key=lambda x: x[1].get('impressions', x[1].get('views', 0)))[0],
    }

    return metrics
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| API rate limit | Posted too frequently | Queue and retry with backoff |
| Content too long | Exceeded platform limit | Auto-truncate with "read more" link |
| Media upload failed | File too large / wrong format | Compress, convert, retry |
| Scheduling conflict | Same time as another post | Auto-adjust to next best slot |
| Platform API changed | Breaking API update | Pin API version, alert on deprecation |
| Character encoding | Special chars break formatting | Sanitize to ASCII/UTF-8 before posting |

## Common Patterns

- **Hub-and-spoke**: One long-form piece as hub, platform-specific versions as spokes
- **Staggered release**: Twitter Day 0 → Newsletter Day 1 → Reddit Day 2 → YouTube Day 3
- **UTM tracking**: Append `?utm_source={platform}&utm_content={content_id}` to all links
- **A/B testing**: Generate 2 hooks for Twitter, post at different times, measure engagement
- **Content library**: Store all generated versions in a structured folder for reuse
- **Template reuse**: Save platform-specific templates, apply to new content automatically

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing
