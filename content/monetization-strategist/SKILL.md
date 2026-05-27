---
name: monetization-strategist
description: Turn content into revenue — newsletter businesses, YouTube automation, affiliate sites, digital product creation, funnel design, audience building
---

## Overview

Monetization orchestration layer that turns content creation skills into revenue-generating businesses. Covers newsletter businesses (Beehiiv/Substack), YouTube automation channels, affiliate content sites, digital product creation, and full funnel design. The content skills handle creation — this skill handles the money.

## Required Tools

- **Newsletter Platforms**: Beehiiv API, Substack API, Ghost API
- **YouTube**: YouTube Data API, yt-dlp, ffmpeg
- **Affiliate Networks**: Amazon Associates API, ShareASale, Impact, CJ Affiliate
- **Digital Products**: Gumroad API, Lemon Squeezy API, Stripe API
- **Analytics**: Google Analytics API, Plausible API, Beehiiv analytics
- **SEO**: Ahrefs API, SEMrush API, Google Search Console API
- **Email**: ConvertKit API, Beehiiv built-in, SendGrid

## Capabilities

- Select optimal monetization model based on niche, audience size, and content type
- Build newsletter businesses with paid tiers, sponsorships, and affiliate integration
- Automate YouTube channels with AI-generated scripts, thumbnails, and scheduling
- Create and sell digital products (courses, templates, tools, ebooks)
- Design and optimize conversion funnels from content to purchase
- Track revenue across all channels with unified reporting

## When to Use

- You have content creation skills but no monetization strategy
- Want to turn a newsletter into a revenue stream
- Building a YouTube automation channel (faceless/AI-generated)
- Creating digital products to sell alongside content
- Need a unified view of content revenue across platforms
- Scaling from hobby content to content business

## Pseudo Code

### Niche Selection & Validation

```python
import requests

def validate_niche(niche_keyword):
    """Check if a niche has monetization potential."""
    scores = {}

    # 1. Search volume (via Google Trends or Ahrefs)
    trends = requests.get(f"https://trends.google.com/trends/api/widgetdata/multiline?req=%7B%22keyword%22:%22{niche_keyword}%22%7D")
    scores["search_demand"] = analyze_trend(trends.json())

    # 2. Affiliate programs available
    amazon_results = requests.get(f"https://webservices.amazon.com/paapi5/searchitems?Keywords={niche_keyword}")
    scores["affiliate_potential"] = len(amazon_results.json()["SearchResult"]["Items"])

    # 3. Existing monetization (are others making money?)
    # Check Substack/Beehiiv top newsletters in niche
    scores["proven_market"] = check_competitor_revenue(niche_keyword)

    # 4. Content gap analysis
    scores["content_gaps"] = find_underserved_topics(niche_keyword)

    total = sum(scores.values()) / len(scores)
    return {
        "niche": niche_keyword,
        "score": total,
        "viable": total >= 60,
        "breakdown": scores,
        "recommendation": "GO" if total >= 70 else "MAYBE" if total >= 50 else "SKIP"
    }
```

### Newsletter Business Setup (Beehiiv)

```bash
# Create newsletter on Beehiiv
curl -X POST "https://api.beehiiv.com/v2/publications" \
  -H "Authorization: Bearer $BEEHIIV_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Business Weekly",
    "referral_program_enabled": true,
    "custom_domain": "aibusiness.co"
  }'

# Set up paid tiers
curl -X POST "https://api.beehiiv.com/v2/publications/$PUB_ID/premium_tiers" \
  -H "Authorization: Bearer $BEEHIIV_TOKEN" \
  -d '{
    "name": "Pro",
    "price_monthly": 15,
    "price_yearly": 120,
    "benefits": ["Deep dives", "Templates", "Private community"]
  }'

# Schedule automated content
python3 <<'PY'
import beehiiv

publication = beehiiv.Publication(pub_id)

# Monday: Curated industry news (free tier)
publication.create_post(
    title="This Week in AI Business",
    content=curate_weekly_news(),
    tier="free",
    schedule="next_monday_9am"
)

# Thursday: Deep dive analysis (paid tier)
publication.create_post(
    title="Deep Dive: " + get_trending_topic(),
    content=generate_deep_dive(),
    tier="premium",
    schedule="next_thursday_9am"
)
PY
```

### YouTube Automation Channel

```python
def create_automated_video(topic, niche):
    """Full pipeline: research → script → voiceover → edit → upload."""

    # 1. Research trending topics in niche
    trending = youtube_search(f"{niche} trending", order="viewCount", days=7)
    competitor_analysis = analyze_top_videos(trending[:10])

    # 2. Generate script with AI
    script = generate_script(
        topic=topic,
        style="educational",
        length="8-12 minutes",
        hooks=competitor_analysis["winning_hooks"],
        structure=competitor_analysis["common_structure"]
    )

    # 3. Generate voiceover (ElevenLabs / PlayHT)
    audio = elevenlabs_generate(
        text=script["narration"],
        voice_id="professional_male_01",
        stability=0.7
    )

    # 4. Generate visuals (stock footage + AI images)
    visuals = match_visuals_to_script(
        script["scenes"],
        sources=["pexels", "pixabay", "dalle"]
    )

    # 5. Edit video (ffmpeg)
    final_video = ffmpeg_compose(
        audio=audio,
        visuals=visuals,
        transitions="smooth",
        background_music="lo-fi_ambient",
        subtitles=True
    )

    # 6. Generate thumbnail (AI)
    thumbnail = generate_thumbnail(
        title=script["title"],
        style="high_contrast_face",
        a_b_test=True
    )

    # 7. Upload to YouTube
    youtube_upload(
        file=final_video,
        title=script["title"],
        description=script["description"],
        tags=script["tags"],
        thumbnail=thumbnail,
        schedule="optimal_time",
        category="Education"
    )

    return {"video_id": video_id, "scheduled_for": schedule_time}
```

### Digital Product Creation

```python
def create_digital_product(product_type, topic, audience):
    """Create and list a digital product for sale."""

    products = {
        "template": {
            "format": "Notion/Google Sheets/Cursor",
            "price_range": (9, 49),
            "creation_time": "2-4 hours"
        },
        "ebook": {
            "format": "PDF + EPUB",
            "price_range": (19, 49),
            "creation_time": "1-2 days"
        },
        "course": {
            "format": "Video + PDF + Community",
            "price_range": (49, 299),
            "creation_time": "1-2 weeks"
        },
        "tool": {
            "format": "Web app / CLI / Spreadsheet",
            "price_range": (29, 99),
            "creation_time": "3-5 days"
        }
    }

    config = products[product_type]

    # Generate product content
    content = generate_product_content(product_type, topic, audience)

    # Create product on Gumroad/Lemon Squeezy
    product = gumroad_create_product(
        name=f"{topic} {product_type.title()}",
        description=content["description"],
        price=config["price_range"][1],
        files=content["files"],
        preview=content["preview"]
    )

    # Create landing page
    landing_page = create_landing_page(
        product=product,
        testimonials=generate_testimonial_placeholder(),
        faq=content["faq"]
    )

    # Set up payment
    stripe_create_product(
        name=product["name"],
        price=config["price_range"][1],
        payment_link=True
    )

    return {
        "product_id": product["id"],
        "url": product["url"],
        "landing_page": landing_page["url"],
        "price": config["price_range"][1]
    }
```

### Funnel Design & Optimization

```
Content Funnel Architecture:

[AWARENESS]
├── Blog posts / YouTube videos (free, SEO-optimized)
├── Social media content (Twitter threads, LinkedIn posts)
└── Guest posts / Podcast appearances
         │
         ▼
[INTEREST]
├── Lead magnet (free template, checklist, mini-course)
├── Newsletter signup (free tier)
└── Webinar / Live workshop
         │
         ▼
[CONSIDERATION]
├── Paid newsletter (low ticket: $5-15/mo)
├── Digital product (mid ticket: $29-99)
└── Free trial of premium content
         │
         ▼
[PURCHASE]
├── Course / Program (high ticket: $99-499)
├── Community membership (recurring: $29-99/mo)
└── Done-for-you service (premium: $500+)
         │
         ▼
[RETENTION]
├── Exclusive content for buyers
├── Community access
└── Upsell to higher tiers
```

```python
def optimize_funnel(funnel_id):
    """Analyze and optimize conversion at each funnel stage."""
    metrics = get_funnel_metrics(funnel_id)

    for stage in ["awareness", "interest", "consideration", "purchase", "retention"]:
        conversion = metrics[stage]["conversion_rate"]

        if conversion < BENCHMARKS[stage]:
            # Identify bottleneck
            analysis = analyze_bottleneck(stage, metrics)

            # Generate optimization suggestions
            suggestions = generate_optimization_plan(stage, analysis)

            # A/B test top suggestion
            ab_test = setup_ab_test(
                stage=stage,
                variant=suggestions[0],
                traffic_split=0.5,
                duration_days=7
            )

            print(f"Stage {stage}: {conversion:.1f}% → testing: {suggestions[0]}")
```

### Revenue Dashboard

```bash
#!/bin/bash
# Generate unified revenue report across all channels

python3 <<'PY'
from datetime import datetime, timedelta
import sqlite3

db = sqlite3.connect("revenue.db")
week_ago = (datetime.now() - timedelta(days=7)).isoformat()

# Revenue by channel
channels = db.execute("""
    SELECT source, SUM(amount) as revenue, COUNT(*) as transactions
    FROM transactions
    WHERE created_at > ?
    GROUP BY source
    ORDER BY revenue DESC
""", [week_ago]).fetchall()

print("=" * 50)
print(f"Weekly Revenue Report ({week_ago[:10]} to now)")
print("=" * 50)

total = 0
for source, revenue, count in channels:
    print(f"  {source:20s} ${revenue:>8,.2f}  ({count} txns)")
    total += revenue

print("-" * 50)
print(f"  {'TOTAL':20s} ${total:>8,.2f}")

# Top products
print("\nTop Products:")
for product, revenue in db.execute("""
    SELECT product_name, SUM(amount) as revenue
    FROM transactions WHERE created_at > ?
    GROUP BY product_name ORDER BY revenue LIMIT 5
""", [week_ago]):
    print(f"  {product:30s} ${revenue:>8,.2f}")
PY
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| Platform API rate limit | Too many API calls to Beehiiv/YouTube/Gumroad | Implement request queuing with backoff, batch operations |
| Content rejection | Platform policy violation (YouTube, Substack) | Review guidelines before publishing, have backup content ready |
| Low conversion rate | Poor funnel design or weak offer | A/B test landing pages, survey audience for feedback |
| Payment failure | Stripe/Gumroad webhook issues | Implement idempotent payment processing, retry logic |
| Email deliverability | Cold domain, spam triggers | Warm up domain gradually, authenticate SPF/DKIM/DMARC |
| Affiliate link expiration | Programs change terms or expire | Monitor link health weekly, have backup programs ready |

## Common Patterns

### Content-to-Revenue Pipeline

```bash
#!/bin/bash
# Weekly content monetization pipeline

# 1. Create content
python3 create_content.py --type newsletter --topic "weekly_roundup"

# 2. Cross-post to platforms
python3 distribute.py --source newsletter --targets "twitter,linkedin,blog"

# 3. Add affiliate links where relevant
python3 inject_affiliates.py --content newsletter --niche "saas_tools"

# 4. Schedule social promotion
python3 schedule_social.py --promote newsletter --platforms "twitter,linkedin"

# 5. Track revenue attribution
python3 track_revenue.py --source newsletter --period weekly
```

### Multi-Revenue Stream Setup

```yaml
revenue_streams:
  newsletter:
    platform: beehiiv
    free_tier: true
    paid_tier: $15/month
    sponsorship_rate: $50 CPM
    affiliate_integration: true

  youtube:
    type: automation
    frequency: 2x/week
    monetization: ads + affiliate + sponsors
    estimated_rpm: $5-15

  digital_products:
    templates:
      price: $29
      platform: gumroad
    course:
      price: $199
      platform: teachable
    community:
      price: $49/month
      platform: circle

  affiliate:
    programs: [amazon, impact, shareasale]
    integration: content_links + dedicated_reviews
    tracking: utm_parameters
```
