---
name: content-creator
description: Use when generating multi-platform content via browser automation - social media, blogs, articles, video scripts,
  and images.
domain: marketing
tags:
- content
- creator
- growth
- marketing
- seo
- social-media
- video
- money
---
# Content Creator

## When to Use

**Trigger phrases:**
- "content creator"
- "Create social media content (TikTok, Instagram, LinkedIn, Twitter)"
- "Generate blog posts and articles"
- "Create video scripts"
- "Design images"
- "Write marketing copy"
- "Generate a blog post about [topic]"
- "Write social posts for [product]"
- "Create a content package"
- "Turn this article into posts"
- "Content repurposing"
- "Schedule content calendar"
- "Any content creation task"

Multi-platform content generation service for SMEs, agencies, and startups. Turns one topic into a full content package: blog post, social posts, and images.

## When NOT to Use

- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel
- When client expects design-heavy assets (use a designer skill instead)
- For long-form journalism or research papers (use long-form skill)

## Money-Making Overview

**Buyer persona:** SME owners, startup founders, and agencies who need consistent content but lack in-house writers or the time to produce it themselves. They search for "content writer for hire," "social media content package," or "blog writing service."

**Pricing tiers:**

| Tier | Price | What they get |
|------|-------|---------------|
| Starter Pack | $300-500 | 1 blog post (800-1200 words) + 5 social posts + 1 image per platform |
| Growth Retainer | $1,000-2,000/mo | 4 blog posts + 20 social posts + 4 images + monthly strategy call |
| Full Pipeline | $2,000-5,000/mo | 8 blog posts + 40 social posts + 8 images + weekly strategy + performance reporting + ad copy |

**First-dollar timeline:** Pitch 3 local businesses or agencies on day 1. Close 1 starter pack within the first week. Use the deliverable template below to look professional from the first client. Cash in hand in 7 days.

**Pro tip:** Offer a "Content Audit" as a loss leader ($97) — review their existing content, identify gaps, then upsell the Starter Pack to fill those gaps.

## First Action in 60 Minutes

Save this as `content-package.py` and run it:

```python
#!/usr/bin/env python3
"""
Content Package Generator — turn one topic into a full content pack.
Usage: python3 content-package.py "Your Topic Here"
"""

import json, os, sys, textwrap
from datetime import datetime, timedelta

TOPIC = sys.argv[1] if len(sys.argv) > 1 else "Why Small Businesses Need AI Automation"
CLIENT = sys.argv[2] if len(sys.argv) > 2 else "Your Client Name"
OUTPUT_DIR = f"content-package-{TOPIC.lower().replace(' ', '-')[:40]}"

# ------------------------------------------------
# Topic analysis (replace with real AI API call in production)
# ------------------------------------------------
def generate_content(topic):
    """Generates a blog post + social posts from a topic.
    Swap the body of this function with an OpenAI/Anthropic API call:
        import openai
        resp = openai.chat.completions.create(model="gpt-4", messages=[...])
        return resp.choices[0].message.content
    """
    # Template fallback — works offline, no API key needed
    blog = textwrap.dedent(f"""
        # {topic}

        ## The Problem

        Every business owner hits the same wall: too much work, too few hours.
        The ones who grow are the ones who automate.

        ## Why Most Solutions Fail

        Teams jump into automation without a plan. They buy five tools, connect nothing,
        and end up more overwhelmed than before. The key is to start small, measure everything,
        and scale what works.

        ## The Framework: Automate One Thing at a Time

        **Step 1: Find the bottleneck.** Look at your weekly calendar. What task eats
        the most time? That is your first automation target.

        **Step 2: Map the workflow.** Write down every step. Who does what? Where does
        the handoff happen? You cannot automate what you have not documented.

        **Step 3: Pick the right tool.** One tool per problem. Do not buy a suite
        before you have validated the workflow.

        **Step 4: Measure before and after.** Track hours saved, error rate, and
        customer satisfaction. If the number does not move, the automation is not working.

        ## Real Results from Real Businesses

        A local accounting firm automated invoice follow-ups and cut AR from 45 days to 12.
        A dental clinic automated appointment reminders and reduced no-shows by 60%.
        A real estate agency automated lead responses and closed 3x more deals in the first month.

        ## Start Today

        You do not need a six-figure budget. You need one bottleneck, one tool, and one week.
        Pick your biggest time-waster. Automate it. Measure the result. Repeat.

        *Ready to automate? Reply to this post and we will map your first workflow for free.*
    """).strip()

    social = {
        "twitter": f"Most businesses waste 20+ hours/week on repetitive tasks.\n\nThe fix? Automate one thing at a time.\n\nHere is a 4-step framework that works:\n\n1. Find the bottleneck\n2. Map the workflow\n3. Pick the right tool\n4. Measure before & after\n\nStart small, scale fast. {topic}",
        "linkedin": f"**The Automation Trap**\n\nI see it every week: a business owner buys 5 tools, connects nothing, and gets more overwhelmed.\n\nAutomation is not about buying software. It is about finding ONE bottleneck, fixing it, measuring the result, and repeating.\n\nA local accounting firm automated invoice follow-ups and cut AR from 45 days to 12. No new software — they just fixed the workflow first.\n\n**Start here:**\n1. What task eats the most time?\n2. Can I document every step?\n3. What is the simplest tool for this one problem?\n4. How will I measure success?\n\nOne bottleneck. One week. One tool. That is all it takes.\n\nWhat is your biggest time-waster? Drop it in the comments.",
        "instagram": f"3 steps to automate your business this week:\n\nStep 1: Find the bottleneck\nWhat task eats the most time?\n\nStep 2: Map the workflow\nDocument every step before buying a tool\n\nStep 3: Measure before & after\nHours saved? Error rate down?\n\nOne bottleneck, one week, one tool.\n\nSave this for when you are ready to automate. {topic}",
        "facebook": f"**Automate Without the Overwhelm**\n\nEvery business owner I talk to wants to automate more. But most jump in wrong — they buy everything at once and end up with a mess of disconnected tools.\n\nHere is what actually works:\n\n1. Pick ONE task that frustrates you most\n2. Map every step of the current workflow\n3. Find the simplest tool for that ONE problem\n4. Measure hours saved before calling it done\n\nOne of our clients automated invoice follow-ups and cut payment collection from 45 days to 12. No complex system — just a targeted fix for a specific pain point.\n\nWhat is ONE thing you would automate if you could?",
        "tiktok_script": f"Business owners: stop buying every automation tool you see.\n\nHere is the framework that actually works:\n\n1. Find your biggest time waster\n2. Map the exact workflow\n3. Pick ONE tool for that ONE problem\n4. Measure the result\n\nA client automated invoice reminders and cut payment time by 70%.\n\nOne bottleneck. One week. Start there.\n\n#automation #smallbusiness #businesstips #productivityhacks"
    }

    return blog, social


def render_content_package(topic, blog, social):
    now = datetime.now()
    cal = []
    for i in range(5):
        day = now + timedelta(days=i)
        platform = ["LinkedIn", "Instagram", "Twitter", "Facebook", "TikTok"][i]
        cal.append(f"  {day.strftime('%a %b %d')}: {platform} — \"{social[platform.lower().replace('tiktok_script','tiktok')][:60]}...\"")

    return f"""# Content Package: {topic}
# Client: {CLIENT}
# Date: {now.strftime('%B %d, %Y')}

---

## BLOG POST

{blog}

---

## SOCIAL MEDIA POSTS

### Twitter/X
{social['twitter']}

### LinkedIn
{social['linkedin']}

### Instagram
{social['instagram']}

### Facebook
{social['facebook']}

### TikTok Script
{social['tiktok_script']}

---

## PUBLICATION SCHEDULE
{chr(10).join(cal)}

---

## NEXT STEPS
- [ ] Review blog post for brand voice alignment
- [ ] Add images/graphics to social posts
- [ ] Schedule in social media dashboard
- [ ] Set tracking UTM parameters
- [ ] Post and monitor engagement for 48 hours
"""


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    blog, social = generate_content(TOPIC)
    output = render_content_package(TOPIC, blog, social)
    path = os.path.join(OUTPUT_DIR, "content-package.md")
    with open(path, "w") as f:
        f.write(output)
    print(f"Done. Content package saved to {OUTPUT_DIR}/content-package.md")
    print(f"\n--- Preview ---")
    print(f"Blog: {len(blog)} chars")
    for k, v in social.items():
        print(f"{k}: {len(v)} chars")
```

**Run it:**
```bash
python3 content-package.py "How AI Changes Small Business Accounting"
```

Deliver the `content-package.md` file to the client. Charge $300-500 for this.

**To level up:** Swap the template with an OpenAI/Anthropic API call. The script is designed for it — replace the `generate_content` function body with an API call.

## Deliverable Format

Send this to the client as a markdown file or Google Doc:

```
CONTENT PACKAGE — [Client Name]
Topic: [Topic]
Date: [Date]

1. BLOG POST
   - 800-1200 words
   - SEO-optimized (H2/H3 structure, meta description)
   - 1 CTA at the end
   - Ready for WordPress/Medium/Substack

2. SOCIAL POSTS (5)
   - Twitter/X: 1 thread or post
   - LinkedIn: 1 long-form post
   - Instagram: 1 caption with hashtags
   - Facebook: 1 community-style post
   - TikTok/Reels: 1 script (30-60 sec)

3. PUBLICATION SCHEDULE
   - Day-by-day: which platform, which post, when
   - Best posting times per platform

4. OPTIONAL UPSELLS
   - +$200: 5 custom images (Canva/Adobe Express)
   - +$300: Schedule and publish all posts
   - +$500/mo: Monthly retainer (4 packages/month)
```

Invoice line item:
```
Content Package — 1 blog post + 5 social posts + schedule | $XXX
```

## Workflow

```python
# Example: SEO keyword analysis
def analyze_keywords(keywords: list[str]) -> list[dict]:
    results = []
    for kw in keywords:
        volume = get_search_volume(kw)
        difficulty = get_difficulty(kw)
        results.append({
            "keyword": kw,
            "volume": volume,
            "difficulty": difficulty,
            "opportunity": volume / max(difficulty, 1),
        })
    return sorted(results, key=lambda x: x["opportunity"], reverse=True)
```

1. **Brief** — Collect topic, audience, tone, platform list from client
2. **Research** — Analyze market, competitors, and trending angles
3. **Create** — Write blog post + adapt for each platform
4. **Review** — Client feedback round (include 1 revision in price)
5. **Deliver** — Send content package + publication schedule
6. **Upsell** — Offer scheduling, images, or monthly retainer

## Key Metrics

- Reach and impressions per post
- Engagement rate (likes, shares, comments)
- Conversion rate (clicks -> leads -> customers)
- Customer acquisition cost (CAC)
- Return on ad spend (ROAS)
- Time saved for client (hours/week)
- Content output velocity (pieces/week)

## Best Practices

- Test everything — headlines, images, CTAs, timing
- Focus on one channel at a time, then expand
- Build organic before scaling paid
- Track attribution across the full funnel
- Repurpose: one blog post = 5 social posts = 1 newsletter = 1 podcast outline
- Always include a CTA in every piece of content
- Keep a swipe file of proven hooks and formats

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I do not have a portfolio yet" | Offer 1 free content pack to a local business in exchange for a testimonial. Now you have a portfolio. |
| "SMEs cannot afford content services" | SMEs spend $500-2000/mo on content. They just need to see ROI. Show them the math: 1 blog post = 500 visits = $X in leads. |
| "AI-generated content is a race to zero" | Clients pay for strategy, editing, and multi-platform adaptation — not raw AI output. The AI is your assistant, not your product. |
| "I need to be an expert in their industry" | You do not. You are a content professional. Interview them for 30 minutes, record it, and write from their expertise. |
| "I will build the pipeline first, then sell" | Sell first, build second. Pitch today. Deliver tomorrow. A sold package forces you to produce faster than any planning phase. |
| "They will just take my content and use it themselves" | That is fine. If they can execute without you, they were never a retainer client. Your real value is consistency and speed. |
| "I need a website and branding before I pitch" | A Google Doc and a Loom video explaining your process is enough for the first 10 clients. Perfection delays revenue. |

## Process

1. **Research** — Analyze target audience, competitors, and trending topics
2. **Create** — Generate content following brand guidelines and best practices
3. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
- [ ] Money-Making Overview reviewed against pricing tiers
