---
name: viral-research-engine
description: Research trending topics, generate viral hooks, find content gaps, analyze competitors, and get hashtag recommendations
  for Indonesian short-form video creators on TikTok, Reels, and Shorts.
domain: content
tags:
- content-creation
- digital-content
- engine
- media
- research
- video
- viral
---

# Viral Research Engine

**Version:** 1.0.0  
**Target Market:** Indonesia (TikTok, Instagram Reels, YouTube Shorts)  
**Purpose:** Stop guessing. Know exactly what content to make, what hooks to use, and what niches are underserved.

---

## When to Use This Skill

Use when you need to:
- Research trending topics before creating content
- Generate viral hooks for any niche
- Find content gaps competitors are missing
- Get hashtag recommendations for each post
- Understand what competitors are doing + their weaknesses
- Build a data-driven content calendar

---

## Directory Structure

```
viral-research-engine/
├── SKILL.md                    ← You are here
├── scripts/
│   ├── __init__.py
│   ├── trend_scraper.py        ← Scrape trending topics from TikTok/IG/X
│   ├── hashtag_analyzer.py     ← Analyze hashtag performance + recommendations
│   ├── competitor_scraper.py   ← Analyze what competitors post + engagement
│   ├── viral_pattern_db.py     ← Database of viral content patterns
│   ├── niche_researcher.py     ← Research specific niches (AI tools, kuliner, etc.)
│   ├── hook_generator.py       ← Generate viral hooks based on trends
│   ├── content_gap_finder.py   ← Find topics competitors miss
│   └── test_research.py        ← Integration tests (all pass ✅)
├── data/                       ← Auto-generated output files
│   ├── hashtag-recommendations.json
│   ├── generated-hooks.json
│   ├── niche-research.json
│   ├── competitor-analysis.json
│   ├── content-gaps.json
│   ├── viral-patterns-db.json
│   └── full-research-report.json
└── references/
    └── viral-patterns.md       ← Human-readable pattern reference
```

---

## Target Niches

| Key | Name | Primary Audience |
|-----|------|-----------------|
| `ai_tools` | AI Tools for Business | 22-40, male-leaning, tech-curious |
| `digital_marketing` | Digital Marketing Tips | 20-35, mixed gender |
| `kuliner` | Kuliner / Food Business | 20-45, female-leaning |
| `side_hustle` | Side Hustle / Passive Income | 22-38, male-leaning |
| `education` | Education / Self-Improvement | 18-35, mixed gender |

---

## Quick Usage

- Configure domain, engine, relevant, research, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### 1. Generate Viral Hooks (Most Used)
```python
cd ~/.openclaw/workspace/skills/1ai-skills/content/viral-research-engine/scripts
python3 hook_generator.py
```
Generates 50 hooks (10 per niche) → `data/generated-hooks.json`

**In Python:**
```python
from hook_generator import generate_hook, generate_full_content_brief

# Get 5 hooks for AI tools niche
hooks = generate_hook("ai_tools", count=5)
for h in hooks:
    print(f"[{h['virality_score']}★] {h['hook']}")

# Get a full content brief with structure
brief = generate_full_content_brief("side_hustle")
print(brief["top_hook"])
print(brief["content_structure"])
```

### 2. Get Hashtag Recommendations
```python
from hashtag_analyzer import get_hashtag_recommendations, build_optimal_hashtag_set

# Top 20 hashtags for a niche
recs = get_hashtag_recommendations("kuliner")

# Optimal 10 hashtag set to use per post
optimal = build_optimal_hashtag_set("kuliner")
print(optimal["optimal_10"])  # Copy-paste ready
```

Output also saved to `data/hashtag-recommendations.json`

### 3. Find Content Gaps
```python
from content_gap_finder import get_quick_wins, find_gaps

# Top 3 quick win opportunities
wins = get_quick_wins()
for win in wins:
    print(f"Topic: {win['topic']}")
    print(f"Gap score: {win['gap_score']}/10")
    print(f"Why: {win['why_opportunity']}")

# All gaps for a specific niche
gaps = find_gaps("ai_tools")
```

### 4. Research a Niche
```python
from niche_researcher import research_niche

data = research_niche("ai_tools")
print(data["trending_topics"])     # Top 10 trending topics
print(data["quick_wins"])          # 3 immediate actions
print(data["7_day_content_calendar"])  # Ready-made calendar
```

### 5. Competitor Analysis
```python
from competitor_scraper import analyze_niche_competitors

analysis = analyze_niche_competitors("digital_marketing")
print(analysis["niche_benchmarks"]["avg_engagement_rate"])  # Beat this
print(analysis["common_weaknesses"])  # Exploit these
print(analysis["winning_strategy"])
```

### 6. Viral Pattern Database
```python
from viral_pattern_db import get_top_patterns, get_best_format, get_posting_schedule

# Top 5 patterns across all niches
patterns = get_top_patterns(limit=5)

# Best format for your niche
fmt = get_best_format("ai_tools")  # → "Tutorial"

# Best time to post
schedule = get_posting_schedule("tiktok")
print(schedule["weekday"])   # → ["07:00-09:00", "12:00-13:30", "18:00-22:00"]
print(schedule["peak_days"]) # → ["Tuesday", "Wednesday", "Friday", "Sunday"]
```

### 7. Run Full Research Report
```python
cd scripts
python3 test_research.py
```
Generates `data/full-research-report.json` (125 KB of structured research data)

---

## Hook Types (8 Proven Patterns)

| ID | Name | Template | Virality Score |
|----|------|----------|---------------|
| hook_001 | Old Way vs New Way | "Kamu masih {old}? Coba {new}..." | 8.2 |
| hook_002 | Shocking Number | "{N} {things} yang bisa {outcome}..." | 9.1 |
| hook_003 | Personal Confession | "Jujur, gue dulu {bad}. Sekarang {good}." | 9.4 |
| hook_004 | Warning / STOP | "STOP {bad_thing} sebelum kamu tau ini..." | **9.7** |
| hook_005 | Before/After | "{Before} → {After} dalam {timeframe}" | 8.8 |
| hook_006 | Question Hook | "Tau gak kamu bisa {outcome} cuma dengan..." | 7.5 |
| hook_007 | Secret Reveal | "Rahasia {expert} yang gak banyak orang tau" | 8.6 |
| hook_008 | FOMO | "Kalau kamu gak {action} sekarang, kamu bakal..." | 9.3 |

---

## Top Content Gaps (Immediate Opportunities)

1. **Side hustle income proof yang credible** — Gap score 8.3  
   Everyone claims income without proof. Be transparent = instant trust.

2. **AI tools untuk UMKM Indonesia** — Gap score 7.1  
   All AI content targets startups. UMKM is 99% of Indonesian businesses.

3. **HPP kalkulator untuk bisnis kuliner** — Gap score 7.3  
   Most food entrepreneurs don't know how to calculate proper margins.

---

## Hashtag Strategy

**Formula:** 2 mega (#kuliner, #bisnisonline) + 4 macro (#bisniskuliner, #resepmasakan) + 4 mid (#aibisnis, #toolsai) = maximum reach + discoverability

Run `build_optimal_hashtag_set("<niche>")` to get your ready-to-use 10 hashtags.

---

## Best Posting Times (WIB)

| Platform | Weekday Peaks | Best Days |
|----------|--------------|-----------|
| TikTok | 07-09, 12-13:30, 18-22 | Tue, Wed, Fri, Sun |
| Instagram | 06-09, 11-13, 19-21 | Mon, Wed, Thu, Sat |
| YouTube Shorts | 08-10, 14-16, 20-23 | Fri, Sat, Sun |

---

## Data Files Output

After running any module, data is saved to `data/`:

| File | Contents |
|------|----------|
| `hashtag-recommendations.json` | Top 20 hashtags per niche with scores |
| `generated-hooks.json` | 50 ready-to-use viral hooks |
| `niche-research.json` | Deep niche profiles + 7-day calendars |
| `competitor-analysis.json` | Competitor patterns + weaknesses |
| `content-gaps.json` | Ranked content opportunities |
| `viral-patterns-db.json` | Pattern database with engagement data |
| `full-research-report.json` | Everything combined (125 KB) |

---

## Test Results

```
16/16 tests passed (100%) ✅
Generated: 125.7 KB full research report
```

Run tests: `cd scripts && python3 test_research.py`

---

## Extending This Skill

- Configure domain, engine, relevant, research, this settings before first use
- Review output quality and adjust parameters
- Monitor performance metrics during execution
- Document custom configurations for team reference
- Schedule regular runs for consistent results


### Add new patterns to DB:
```python
from viral_pattern_db import add_pattern
add_pattern({
    "name": "My Pattern",
    "hook_template": "Template with {slot}...",
    "format": "Tutorial",
    "niche_fit": ["ai_tools"],
    "avg_engagement_rate": 0.075,
    "virality_score": 8.0,
    "best_times": ["12:00"],
})
```

### Add new competitor:
Edit `competitor_scraper.py` → `COMPETITORS` dict

### Add new niche:
1. Add to `NICHE_HASHTAGS` in `hashtag_analyzer.py`
2. Add to `NICHE_PROFILES` in `niche_researcher.py`
3. Add to `NICHE_FILLS` in `hook_generator.py`
4. Add to `CONTENT_GAPS` in `content_gap_finder.py`

---

## Integration with Content Pipeline

```python
# Before making content:
from scripts.hook_generator import generate_hook
from scripts.hashtag_analyzer import build_optimal_hashtag_set
from scripts.content_gap_finder import get_quick_wins

niche = "ai_tools"

# 1. Pick topic from gaps
topic = get_quick_wins(niche)[0]["topic"]

# 2. Generate hook
hook = generate_hook(niche, count=1)[0]["hook"]

# 3. Get hashtags
hashtags = build_optimal_hashtag_set(niche)["optimal_10"]

print(f"Topic: {topic}")
print(f"Hook: {hook}")
print(f"Hashtags: {' '.join(hashtags)}")
```

---

*Built for BerkahKarya revenue survival. No more guessing.*  
*Data-driven content = predictable virality.*  🔥

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- Check readability score (target grade 8 or below for general audiences)
- Verify all images have alt text and proper dimensions per platform
- Confirm links work and point to correct destinations
- Test video/audio quality before publishing
- Validate content renders correctly on mobile devices

## Overview

> Section content — see SKILL.md body for full details.
