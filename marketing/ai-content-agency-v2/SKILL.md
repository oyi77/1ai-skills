---
name: ai-content-agency-v2
description: 9-workflow, 6-phase AI content agency blueprint — generates ads, videos, images, and landing pages from product
  info using LLM ideation through multi-provider rendering.
domain: marketing
author: mahipal
license: Apache-2.0
subdomain: marketing
tags:
- agency
- content
- growth
- marketing
- seo
- video
- workflow
- money
version: 1.0.0
---
# AI Content Agency V2

## Money-Making Overview

**Buyer:** Agency owners, freelancers, and marketing teams who need to deliver content production at scale without hiring a full creative team. They sell "full-funnel content packages" to SME/startup clients but bottleneck on production speed.

**How you make money:** You run the 9-workflow, 6-phase pipeline end-to-end. Your leverage is AI-assisted production — one operator produces what a 5-person agency team would. Deliverables are white-label ready.

**Pricing (monthly retainer):**

| Tier | Price | Deliverables |
|---|---|---|
| **Starter** | $2,000–$4,000/mo | 2–3 workflows (ads + images), 2 revision rounds, 1 channel |
| **Growth** | $4,000–$7,000/mo | All 9 workflows, unlimited revisions, 3 channels, weekly reporting |
| **White-Label** | $7,000–$10,000+/mo | Full agency partnership, priority turnaround, co-branded deliverables, profit-share on scale |

**First-dollar timeline:** Day 1 — prospect accepts proposal. Day 2 — run the First Action script on their product URL. Day 3 — deliver a full asset pack (hooks, ad copy, image briefs). Day 5 — first paid invoice clears.

---

## When to Use

**Trigger phrases:**
- "ai content agency v2"
- "Help me with ai content agency v2"
- "generate content assets"
- "need ad creatives for client"
- "agency deliverables workflow"
- "content production pipeline"
- "scale content output"

**Use cases:**
- Producing a full content campaign from a single product URL
- Generating ad copy variants, video scripts, image briefs, and landing page outlines in one pass
- Running a retainer-based content agency with AI-assisted tooling
- White-label content production for marketing agencies

**When NOT to use:**
- For tasks outside this skill's scope
- When the audience is too small to justify the effort
- For regulated industries without compliance review
- When the campaign budget does not support the channel
- When the client refuses AI-assisted production (rare, but happens)

---

## Overview

AI Content Agency V2 is a 9-workflow, 6-phase production blueprint. Each workflow is a standalone deliverable. The phases sequence them into a campaign. You can run individual workflows for one-off projects or the full pipeline for retainer clients.

**6 Phases:**
1. **Research & Strategy** — Product analysis, audience definition, competitor content audit
2. **Ideation & Scripting** — Hook generation, ad copy, video scripts, CTA frameworks
3. **Asset Production** — Image generation, video rendering, landing page building
4. **Multi-Platform Publishing** — Channel-optimized distribution, scheduling
5. **Performance Optimization** — A/B testing, metric tracking, creative refresh
6. **Reporting & Scaling** — Client report pack, iteration planning, upsell identification

**9 Workflows:**
1. **Product Research & Audience Analysis** — Extract product specs, USP, target demographics, competitor positioning from URL or brief
2. **Ad Copy & Hook Generation** — Generate 20+ headline/hook variants, pain-point driven ad copy, CTA frameworks per platform
3. **Video Script & Storyboard Creation** — Short-form (15-60s) scripts with scene-by-scene breakdowns, visual directions, hook-first structures
4. **AI Image Generation** — Product shots, lifestyle scenes, ad creatives using provider chains (SDXL, DALL-E, Flux)
5. **AI Video Production** — Short-form ads via Runway, Kling, or Seedance; TTS voiceover; caption overlays
6. **Landing Page Generation** — One-page campaign landing pages with hero, social proof, CTA, and form
7. **Multi-Platform Scheduling & Publishing** — Platform-optimized resizing, captioning, and batch scheduling
8. **A/B Testing & Performance Tracking** — Variant generation, UTM tagging, metric collection, winning creative identification
9. **Retainer Reporting & Iteration** — Weekly/monthly performance packs, creative fatigue detection, next-cycle recommendations

---

## Workflow: Full Pipeline Script

Run this from a product URL to generate the first deliverable set:

```python
#!/usr/bin/env python3
"""ai_content_agency_v2.py — Generate client deliverable pack from product URL.

Usage:
    python3 ai_content_agency_v2.py https://example.com/product [--output-dir ./deliverables]

Requires: requests, openai (or any LLM provider SDK), pillow
"""

import argparse, json, os, sys, textwrap, urllib.parse
from typing import Any

# ── Configuration ──────────────────────────────────────────
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_MODEL  = os.environ.get("LLM_MODEL",  "gpt-4o")
IMAGE_API  = os.environ.get("IMAGE_API",  "https://api.stability.ai/v2beta/stable-image/generate/sd3")
# ────────────────────────────────────────────────────────────

PROMPT_TEMPLATE = textwrap.dedent("""\
You are a senior agency content strategist. A client sells: {product_name}
Landing page / URL content: {page_text}
Target audience (from client): {audience}

## Task
Generate a structured content plan with exactly these sections:

### 1. USP & Positioning (3 sentences)
### 2. Audience Detail (demographic, psychographic, pain points)
### 3. Top 5 Hooks (one-liners for TikTok/Reels/YouTube Shorts)
### 4. Top 5 Ad Copy Variants (headline + body + CTA, for Meta/Google)
### 5. Top 3 Video Concepts (15-30s each, scene breakdowns)
### 6. Top 3 Image Briefs (subject, mood, composition — usable as image gen prompts)
### 7. Landing Page Outline (hero, sections, CTA)
### 8. Platform Strategy (which platform, format, frequency)

Return valid JSON with keys: usp, audience, hooks, ad_copy, video_concepts, image_briefs, landing_page, platform_strategy
Each value is a dict or list of dicts. hooks is a list of strings. ad_copy is list of dicts with headline, body, cta.
""")


def fetch_page_text(url: str) -> str:
    """Scrape product page for text content."""
    try:
        import requests
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        from html.parser import HTMLParser
        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self._text = []
                self._skip = False
            def handle_starttag(self, tag, attrs):
                if tag in ("script", "style"): self._skip = True
            def handle_endtag(self, tag):
                if tag in ("script", "style"): self._skip = False
            def handle_data(self, data):
                if not self._skip:
                    cleaned = data.strip()
                    if cleaned: self._text.append(cleaned)
        extractor = TextExtractor()
        extractor.feed(resp.text)
        return "\n".join(extractor._text[:200])  # first 200 lines
    except Exception as exc:
        return f"[Could not fetch URL: {exc}]"


def call_llm(prompt: str) -> dict[str, Any]:
    """Call LLM and parse JSON response."""
    import requests
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"},
        json={
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
        },
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def generate_image_briefs(briefs: list[dict]) -> list[str]:
    """Generate placeholder image files per brief — or just write prompt files."""
    paths = []
    for i, brief in enumerate(briefs, 1):
        prompt_text = brief.get("prompt", brief.get("description", f"Image brief {i}"))
        path = f"image_brief_{i}.txt"
        with open(path, "w") as f:
            f.write(prompt_text + "\n")
        paths.append(path)
    return paths


def format_report(plan: dict[str, Any], product_name: str) -> str:
    """Format the content plan as a Markdown report."""
    lines = [f"# Content Plan: {product_name}", ""]
    lines.append("## USP & Positioning")
    lines.append(plan.get("usp", ""))
    lines.append("")
    lines.append("## Target Audience")
    lines.append(str(plan.get("audience", "")))
    lines.append("")
    lines.append("## Top Hooks")
    for i, h in enumerate(plan.get("hooks", []), 1):
        lines.append(f"{i}. {h}")
    lines.append("")
    lines.append("## Ad Copy Variants")
    for i, ad in enumerate(plan.get("ad_copy", []), 1):
        lines.append(f"### Variant {i}")
        lines.append(f"**Headline:** {ad.get('headline', '')}")
        lines.append(f"**Body:** {ad.get('body', '')}")
        lines.append(f"**CTA:** {ad.get('cta', '')}")
        lines.append("")
    lines.append("## Video Concepts")
    for i, vc in enumerate(plan.get("video_concepts", []), 1):
        lines.append(f"### Concept {i}")
        lines.append(str(vc))
        lines.append("")
    lines.append("## Image Briefs")
    for i, ib in enumerate(plan.get("image_briefs", []), 1):
        lines.append(f"### Brief {i}")
        lines.append(str(ib))
        lines.append("")
    lines.append("## Landing Page Outline")
    lines.append(str(plan.get("landing_page", "")))
    lines.append("")
    lines.append("## Platform Strategy")
    lines.append(str(plan.get("platform_strategy", "")))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI Content Agency V2 — First Client Deliverable")
    parser.add_argument("url", help="Product URL")
    parser.add_argument("--output-dir", default="./deliverables", help="Output directory")
    parser.add_argument("--audience", default="Small business owners, 25-45, US market", help="Target audience description")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    product_url = args.url
    product_name = urllib.parse.urlparse(product_url).netloc.replace("www.", "")

    print(f"[1/4] Fetching product page: {product_url}")
    page_text = fetch_page_text(product_url)

    print("[2/4] Generating content plan with LLM...")
    prompt = PROMPT_TEMPLATE.format(product_name=product_name, page_text=page_text[:3000], audience=args.audience)
    plan = call_llm(prompt)

    print("[3/4] Generating image briefs...")
    brief_paths = generate_image_briefs(plan.get("image_briefs", []))

    print("[4/4] Writing deliverable pack...")
    report = format_report(plan, product_name)
    report_path = os.path.join(args.output_dir, "content_plan.md")
    with open(report_path, "w") as f:
        f.write(report)

    manifest = {"product_url": product_url, "product_name": product_name, "report": report_path, "image_briefs": brief_paths, "plan": plan}
    manifest_path = os.path.join(args.output_dir, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDone. Deliverables in {args.output_dir}/")
    print(f"  Report:     {report_path}")
    print(f"  Image briefs: {', '.join(brief_paths)}")
    print(f"  Manifest:   {manifest_path}")
    print("\nNext step: Run each image brief through your image gen workflow.")


if __name__ == "__main__":
    main()
```

---

## Deliverable Format

**Agency Service Menu Template** — send this to prospects after the intro call. Fill the `[brackets]` fields.

```
# AI Content Agency Service Menu
## Client: [Client Name]
## Prepared: [Date]

### Retainer Options

**Starter — $2,500/mo**
- 5 ad copy variants (2 platforms)
- 3 image creatives
- 2 video scripts + storyboards
- 1 landing page outline
- 2 revision rounds
- Weekly Slack check-in

**Growth — $5,000/mo**
- 15 ad copy variants (3 platforms)
- 8 image creatives
- 5 video scripts + 2 produced short-form videos
- 1 landing page (built, not just outline)
- Multi-platform scheduling (3 channels)
- Bi-weekly performance report
- Unlimited revisions

**White-Label — $8,500/mo**
- 25+ ad copy variants (all relevant platforms)
- 15 image creatives
- 10 video scripts + 5 produced videos
- Full campaign landing page + A/B variants
- Full funnel: awareness → retarget → conversion
- Weekly performance pack with recommendations
- Priority turnaround (24h on urgent)
- Co-branded deliverables (your logo)

### What We Need From You
- Product URL or brief
- Brand guidelines (colors, fonts, tone)
- Past content examples (if any)
- Target audience description
- Platform preferences

### Timeline
- Day 1–2: Research & Strategy
- Day 3–4: Content Production (batch)
- Day 5: Review & Revisions
- Day 6: Publishing
- Day 7: Report

---

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll build the pipeline first, then find clients" | You find clients by selling, not by building. Use the First Action script on a real prospect's URL today. |
| "My clients don't need all 9 workflows" | Sell the full pipeline, deliver incrementally. Upsell unused workflows next month. |
| "I can't compete with established agencies" | You don't need to — your cost structure is 5x lower. Compete on speed and price, then on quality. |
| "AI content looks generic" | Generic output = generic prompts. The 9-workflow pipeline with client-specific briefs produces distinct, on-brand work. |
| "I need a portfolio first" | Your first client IS your portfolio. Run the script on a product you know, polish the output, and show it as a sample. |
| "Retainers are hard to close" | Start with a single project at Starter pricing. Prove ROI, then convert to monthly retainer. |
| "I don't have design skills" | You're not designing — you're directing AI. Image briefs, video concepts, and copy are all prompt-based. The AI renders. |
| "Clients want human-made content" | Clients want results. If AI-generated content converts better, they don't care. Show the metrics. |

---

## Process

1. **Research** — Analyze target audience, competitors, and trending topics
2. **Create** — Generate content following brand guidelines and best practices
3. **Publish & Optimize** — Distribute to target platforms, track performance, iterate

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
