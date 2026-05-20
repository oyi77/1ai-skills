#!/usr/bin/env python3
"""
BerkahKarya Revenue Generator -- Ranked Revenue Playbook
Uses LLM (OmniRoute) to generate actionable revenue opportunities.
"""

import json
import os
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
REPORTS_DIR = SKILL_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# --- BerkahKarya Assets (hardcoded, configurable via JSON) -------------------

BERKAHKARYA_ASSETS = {
    "tools": {
        "postbridge": "Social media posting automation (12 accounts: 7 TikTok, 1 IG, 4 FB)",
        "bot_extractor": "Can clone any Telegram bot architecture",
        "biz_spy": "Full competitor intelligence",
        "ai_video": "Access to Kling AI, PixVerse for video generation",
        "content_library": "162 videos/images ready for upload (JENDRALBOT campaign)",
    },
    "audience": {
        "telegram": "Active account, network of contacts",
        "tiktok": "7 accounts via PostBridge (0 followers currently)",
        "instagram": "1 account via PostBridge (0 followers currently)",
    },
    "products": {
        "jendralbot": "6 digital products on LYNK (IDR 0-89K), 0 sales so far",
        "potential": "Can build AI video generator bot (vidabot clone capability)",
    },
    "skills": [
        "Python dev",
        "AI automation",
        "Telegram bot development",
        "Content creation",
    ],
    "budget": "near_zero",  # < IDR 500K liquid
    "time": "urgent",  # need revenue this week
}

# --- Hardcoded Fallback Opportunities ----------------------------------------

FALLBACK_OPPORTUNITIES = [
    {
        "name": "TikTok Content Grind with PostBridge",
        "category": "immediate",
        "revenue_estimate_idr": 500000,
        "revenue_period": "per_month",
        "effort": "medium",
        "time_to_first_revenue": "1 week",
        "budget_needed_idr": 0,
        "risk": "low",
        "why": "7 TikTok accounts already connected to PostBridge with 162 videos ready. Volume posting across multiple accounts maximizes viral chance.",
        "how": [
            "Upload 162 existing videos across 7 TikTok accounts via PostBridge",
            "Schedule 3-5 posts per account per day for maximum reach",
            "Add trending hashtags and sounds to each post",
            "Include LYNK link in bio for JENDRALBOT products",
            "Monitor analytics and double down on what gets traction",
        ],
        "first_action": "Schedule first batch of 20 videos across all 7 TikTok accounts via PostBridge right now",
        "tools_needed": ["postbridge", "content_library"],
        "why_we_can_win": "Volume advantage: 7 accounts posting simultaneously gives 7x the chance of virality vs single account",
    },
    {
        "name": "Sell Biz Spy Intelligence Reports as a Service",
        "category": "immediate",
        "revenue_estimate_idr": 2000000,
        "revenue_period": "per_month",
        "effort": "low",
        "time_to_first_revenue": "3 days",
        "budget_needed_idr": 0,
        "risk": "low",
        "why": "Business intelligence is high-value. Competitors charge IDR 500K+ per report. We can generate them automatically with biz_spy.",
        "how": [
            "Create 3 sample competitor intelligence reports using biz_spy",
            "Post on Telegram, TikTok showing sample insights",
            "Price at IDR 150K-300K per report",
            "Offer custom competitor analysis for businesses",
            "Upsell to monthly monitoring subscriptions",
        ],
        "first_action": "Generate 3 sample biz_spy reports for popular Indonesian brands and post screenshots to Telegram",
        "tools_needed": ["biz_spy"],
        "why_we_can_win": "Automated intelligence generation means near-zero marginal cost per report while competitors do manual research",
    },
    {
        "name": "Sell JENDRALBOT Products via TikTok Traffic",
        "category": "immediate",
        "revenue_estimate_idr": 800000,
        "revenue_period": "per_month",
        "effort": "low",
        "time_to_first_revenue": "1 week",
        "budget_needed_idr": 0,
        "risk": "low",
        "why": "6 products already listed on LYNK. Just need traffic. TikTok accounts + PostBridge can drive free traffic.",
        "how": [
            "Create short demo videos for each JENDRALBOT product",
            "Post across all 7 TikTok accounts with product links",
            "Use AI video tools to create engaging product showcases",
            "Pin LYNK link in TikTok bios",
            "Create urgency with limited-time pricing",
        ],
        "first_action": "Create 3 short demo videos for top JENDRALBOT products using AI video tools",
        "tools_needed": ["postbridge", "ai_video", "content_library"],
        "why_we_can_win": "Products already exist and are listed. Zero additional development needed, just marketing execution.",
    },
    {
        "name": "Affiliate Marketing via PostBridge Accounts",
        "category": "immediate",
        "revenue_estimate_idr": 1000000,
        "revenue_period": "per_month",
        "effort": "medium",
        "time_to_first_revenue": "1 week",
        "budget_needed_idr": 0,
        "risk": "low",
        "why": "12 social media accounts is a distribution network. Affiliate programs like Shopee, Tokopedia, TikTok Shop pay commissions on referrals.",
        "how": [
            "Sign up for TikTok Shop affiliate program on all 7 accounts",
            "Join Shopee and Tokopedia affiliate programs",
            "Create product review content using AI video generation",
            "Post affiliate content across all 12 accounts via PostBridge",
            "Focus on trending products with high commission rates",
        ],
        "first_action": "Register for TikTok Shop affiliate program on the first TikTok account",
        "tools_needed": ["postbridge", "ai_video"],
        "why_we_can_win": "12 accounts provide massive distribution leverage that individual affiliates cannot match",
    },
    {
        "name": "Clone Vidabot and Sell Subscriptions",
        "category": "short_term",
        "revenue_estimate_idr": 5000000,
        "revenue_period": "per_month",
        "effort": "high",
        "time_to_first_revenue": "2 weeks",
        "budget_needed_idr": 500000,
        "risk": "medium",
        "why": "Vidabot architecture already extracted. AI video generation bots are in high demand. Can undercut competitors on pricing.",
        "how": [
            "Use bot_extractor data to replicate vidabot architecture",
            "Build Telegram bot with AI video generation (Kling AI / PixVerse)",
            "Price at IDR 50K-100K per month subscription",
            "Market via TikTok accounts showing generated videos",
            "Offer free trial to first 50 users for testimonials",
        ],
        "first_action": "Review bot_extractor vidabot architecture report and create development plan",
        "tools_needed": ["bot_extractor", "ai_video"],
        "why_we_can_win": "Already have the architecture blueprint. Development time is halved compared to building from scratch.",
    },
    {
        "name": "Build Custom Telegram Bots for Clients",
        "category": "short_term",
        "revenue_estimate_idr": 3000000,
        "revenue_period": "per_month",
        "effort": "medium",
        "time_to_first_revenue": "2 weeks",
        "budget_needed_idr": 0,
        "risk": "medium",
        "why": "Telegram bot development skill + bot_extractor means we can build bots fast. Indonesian SMEs need bots for customer service and sales.",
        "how": [
            "Create portfolio with 2-3 demo bots showcasing capabilities",
            "List bot development services on freelance platforms (Fastwork, Sribulancer)",
            "Post demo videos on TikTok showing bot capabilities",
            "Price at IDR 1M-5M per custom bot depending on complexity",
            "Offer maintenance packages for recurring revenue",
        ],
        "first_action": "Build 2 demo bots (customer service bot + order bot) as portfolio pieces",
        "tools_needed": ["bot_extractor"],
        "why_we_can_win": "Bot extractor gives us templates to start from, reducing delivery time to days instead of weeks",
    },
    {
        "name": "AI Video Generation Service",
        "category": "short_term",
        "revenue_estimate_idr": 2000000,
        "revenue_period": "per_month",
        "effort": "medium",
        "time_to_first_revenue": "1 week",
        "budget_needed_idr": 0,
        "risk": "low",
        "why": "Access to Kling AI and PixVerse. Many Indonesian SMEs want AI-generated video content but do not know how to use the tools.",
        "how": [
            "Create sample AI videos for different niches (food, fashion, tech)",
            "Offer video generation packages: 5 videos for IDR 200K, 20 for IDR 500K",
            "Market on TikTok with before/after content",
            "Build simple order bot on Telegram for intake",
            "Batch process orders for efficiency",
        ],
        "first_action": "Generate 5 sample AI videos across different niches and post to TikTok",
        "tools_needed": ["ai_video", "postbridge"],
        "why_we_can_win": "Direct access to AI video tools while most Indonesian SMEs still use manual video editors",
    },
    {
        "name": "White-Label Bot Service for Agencies",
        "category": "medium_term",
        "revenue_estimate_idr": 10000000,
        "revenue_period": "per_month",
        "effort": "high",
        "time_to_first_revenue": "3 months",
        "budget_needed_idr": 2000000,
        "risk": "high",
        "why": "Digital agencies need bot solutions for their clients but lack technical capability. We can be their backend provider.",
        "how": [
            "Build a white-label bot platform with customizable templates",
            "Create partnership pitch deck for digital agencies",
            "Reach out to 20 Indonesian digital agencies",
            "Offer revenue share or monthly retainer model",
            "Scale with standardized bot templates using bot_extractor",
        ],
        "first_action": "Research and list 20 Indonesian digital agencies that serve SME clients",
        "tools_needed": ["bot_extractor", "biz_spy"],
        "why_we_can_win": "Technical capability gap in the agency market. Most agencies outsource bot dev at high cost.",
    },
]

# --- LLM Integration ---------------------------------------------------------


def get_llm_client():
    """Get OmniRoute LLM client."""
    from openai import OpenAI

    return OpenAI(
        base_url=os.environ.get("OMNIROUTE_BASE_URL", "http://localhost:20128/v1"),
        api_key=os.environ.get("OMNIROUTE_KEY", "omniroute"),
    )


def llm_generate(
    prompt: str,
    system: str = "You are a ruthless business strategist focused on immediate revenue generation for a near-zero budget Indonesian digital business.",
) -> str:
    """Call LLM to generate text."""
    try:
        client = get_llm_client()
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=3000,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"  LLM error: {e}")
        return None


# --- Core Functions -----------------------------------------------------------


def load_assets(custom_path=None) -> dict:
    """Load BerkahKarya assets from hardcoded defaults or custom JSON file."""
    if custom_path:
        custom = Path(custom_path)
        if custom.exists():
            print(f"  Loading custom assets from: {custom}")
            with open(custom, "r") as f:
                return json.load(f)
        else:
            print(f"  Warning: custom assets file not found: {custom}")
            print("  Falling back to hardcoded assets.")
    return BERKAHKARYA_ASSETS.copy()


def generate_opportunities(assets: dict) -> list:
    """Use LLM to generate revenue opportunities based on current assets."""
    print("  Calling LLM to generate opportunities...")
    prompt = f"""Analyze these business assets and generate 10-15 revenue opportunities.

ASSETS:
{json.dumps(assets, indent=2)}

Return ONLY a JSON array (no markdown, no explanation) where each element has this exact structure:
{{
    "name": "opportunity name",
    "category": "immediate|short_term|medium_term|skip",
    "revenue_estimate_idr": 500000,
    "revenue_period": "per_month",
    "effort": "low|medium|high",
    "time_to_first_revenue": "3 days|1 week|2 weeks|1 month|3 months",
    "budget_needed_idr": 0,
    "risk": "low|medium|high",
    "why": "reason this works for this specific business",
    "how": ["step 1", "step 2", "step 3", "step 4", "step 5"],
    "first_action": "exact next step to do RIGHT NOW",
    "tools_needed": ["postbridge"],
    "why_we_can_win": "specific competitive advantage"
}}

Rules:
- At least 4 opportunities must have budget_needed_idr = 0
- At least 3 must be "immediate" category
- Focus on Indonesian market (prices in IDR)
- Be specific about tools from the assets list
- "first_action" must be something doable in the next 30 minutes
- Revenue estimates should be realistic, not optimistic
"""

    raw = llm_generate(prompt)
    if raw:
        try:
            # Try to extract JSON from the response
            text = raw.strip()
            # Handle markdown code blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()

            opportunities = json.loads(text)
            if isinstance(opportunities, list) and len(opportunities) > 0:
                print(f"  LLM generated {len(opportunities)} opportunities.")
                return opportunities
            else:
                print("  LLM returned invalid structure. Using fallback.")
        except (json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"  Failed to parse LLM response: {e}")
            print("  Using fallback opportunities.")

    print("  Using hardcoded fallback opportunities.")
    return FALLBACK_OPPORTUNITIES.copy()


def score_opportunities(opportunities: list) -> list:
    """Score each opportunity and sort descending."""
    effort_scores = {"low": 1, "medium": 2, "high": 3}
    time_scores = {
        "3 days": 1,
        "1 week": 2,
        "2 weeks": 3,
        "1 month": 4,
        "3 months": 6,
    }
    risk_scores = {"low": 1, "medium": 2, "high": 3}

    scored = []
    for opp in opportunities:
        try:
            revenue = opp.get("revenue_estimate_idr", 0)
            effort = effort_scores.get(opp.get("effort", "high"), 3)
            time_val = time_scores.get(opp.get("time_to_first_revenue", "3 months"), 6)
            risk = risk_scores.get(opp.get("risk", "high"), 3)

            score = (revenue / 100000) * (1 / effort) * (1 / time_val) * (1 / risk)
            opp["score"] = round(score, 2)
            scored.append(opp)
        except (TypeError, ZeroDivisionError) as e:
            print(f"  Skipping opportunity due to scoring error: {e}")
            continue

    scored.sort(key=lambda x: x.get("score", 0), reverse=True)
    return scored


def categorize_opportunities(scored: list) -> dict:
    """Group scored opportunities into time-based categories."""
    time_order = {"3 days": 1, "1 week": 2, "2 weeks": 3, "1 month": 4, "3 months": 6}

    categories = {
        "immediate": [],
        "short_term": [],
        "medium_term": [],
        "skip": [],
    }

    for opp in scored:
        budget = opp.get("budget_needed_idr", 0)
        time_val = time_order.get(opp.get("time_to_first_revenue", "3 months"), 6)
        cat = opp.get("category", "")

        # Override category based on rules
        if budget == 0 and time_val <= 2:
            final_cat = "immediate"
        elif budget <= 2000000 and time_val <= 4:
            final_cat = "short_term"
        elif time_val <= 6:
            final_cat = "medium_term"
        else:
            final_cat = "skip"

        # If the LLM marked it as skip, respect that
        if cat == "skip":
            final_cat = "skip"

        categories[final_cat].append(opp)

    return categories


def generate_playbook_md(categorized: dict, assets: dict) -> str:
    """Generate a formatted Markdown playbook."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []

    lines.append("=== BERKAHKARYA REVENUE PLAYBOOK ===")
    lines.append(f"Generated: {now}")
    lines.append(f"Budget: {assets.get('budget', 'unknown')}")
    lines.append(f"Urgency: {assets.get('time', 'unknown')}")
    lines.append("")

    section_headers = {
        "immediate": "IMMEDIATE (This Week, 0 budget needed)",
        "short_term": "SHORT-TERM (This Month, low budget)",
        "medium_term": "MEDIUM-TERM (3 months, requires investment)",
        "skip": "SKIP FOR NOW (too slow/risky)",
    }

    for cat_key in ["immediate", "short_term", "medium_term", "skip"]:
        opps = categorized.get(cat_key, [])
        header = section_headers[cat_key]
        lines.append(header)

        separator = "\u2501" * 38
        lines.append(separator)

        if not opps:
            lines.append("  (none)")
            lines.append("")
            continue

        for idx, opp in enumerate(opps, 1):
            name = opp.get("name", "Unnamed")
            revenue = opp.get("revenue_estimate_idr", 0)
            period = opp.get("revenue_period", "per_month")
            score = opp.get("score", 0)
            why = opp.get("why", "N/A")
            how = opp.get("how", [])
            first_action = opp.get("first_action", "N/A")
            time_to_rev = opp.get("time_to_first_revenue", "N/A")
            risk = opp.get("risk", "N/A").upper()
            tools = opp.get("tools_needed", [])
            budget = opp.get("budget_needed_idr", 0)

            lines.append(f"{idx}. [{name}] -- Est: IDR {revenue:,.0f}/{period}")
            lines.append(f"   Score: {score}")
            if budget > 0:
                lines.append(f"   Budget needed: IDR {budget:,.0f}")
            lines.append(f"   Why: {why}")
            lines.append("   How:")
            for step_idx, step in enumerate(how, 1):
                lines.append(f"     {step_idx}. {step}")
            lines.append(f"   First action: {first_action}")
            lines.append(f"   Time to first IDR: {time_to_rev}")
            lines.append(f"   Risk: {risk}")
            lines.append(f"   Tools: {', '.join(tools) if tools else 'none'}")
            lines.append("")

        lines.append("")

    return "\n".join(lines)


def generate_playbook_json(categorized: dict, assets: dict) -> dict:
    """Return full structured playbook data."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "meta": {
            "generated": now,
            "generator": "BerkahKarya Revenue Generator v1.0.0",
            "budget": assets.get("budget", "unknown"),
            "urgency": assets.get("time", "unknown"),
        },
        "assets": assets,
        "playbook": categorized,
        "summary": {
            "immediate_count": len(categorized.get("immediate", [])),
            "short_term_count": len(categorized.get("short_term", [])),
            "medium_term_count": len(categorized.get("medium_term", [])),
            "skip_count": len(categorized.get("skip", [])),
            "total_opportunities": sum(len(v) for v in categorized.values()),
            "total_immediate_revenue_estimate_idr": sum(
                o.get("revenue_estimate_idr", 0)
                for o in categorized.get("immediate", [])
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="BerkahKarya Revenue Generator -- Ranked Revenue Playbook"
    )
    parser.add_argument(
        "--assets",
        type=str,
        default=None,
        help="Path to custom assets JSON file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(REPORTS_DIR / "berkahkarya_playbook.md"),
        help="Output markdown file path",
    )
    parser.add_argument(
        "--json",
        type=str,
        default=str(REPORTS_DIR / "berkahkarya_playbook.json"),
        help="Output JSON file path",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("  BERKAHKARYA REVENUE GENERATOR")
    print("=" * 50)
    print()

    # 1. Load assets
    print("[1/6] Loading assets...")
    assets = load_assets(args.assets)
    print(f"  Tools: {len(assets.get('tools', {}))}")
    print(f"  Products: {len(assets.get('products', {}))}")
    print(f"  Budget: {assets.get('budget', 'unknown')}")
    print()

    # 2. Generate opportunities
    print("[2/6] Generating revenue opportunities...")
    opportunities = generate_opportunities(assets)
    print(f"  Total opportunities: {len(opportunities)}")
    print()

    # 3. Score and sort
    print("[3/6] Scoring and ranking opportunities...")
    scored = score_opportunities(opportunities)
    if scored:
        print(
            f"  Top opportunity: {scored[0].get('name', 'N/A')} (score: {scored[0].get('score', 0)})"
        )
    print()

    # 4. Categorize
    print("[4/6] Categorizing opportunities...")
    categorized = categorize_opportunities(scored)
    for cat, opps in categorized.items():
        print(f"  {cat}: {len(opps)} opportunities")
    print()

    # 5. Generate and save markdown
    print("[5/6] Generating markdown playbook...")
    md_content = generate_playbook_md(categorized, assets)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(md_content)
    print(f"  Saved: {output_path}")
    print()

    # 6. Generate and save JSON
    print("[6/6] Generating JSON playbook...")
    json_data = generate_playbook_json(categorized, assets)
    json_path = Path(args.json)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {json_path}")
    print()

    # Print summary
    print("=" * 50)
    print("  PLAYBOOK SUMMARY")
    print("=" * 50)
    summary = json_data.get("summary", {})
    print(f"  Immediate actions:  {summary.get('immediate_count', 0)}")
    print(f"  Short-term plays:   {summary.get('short_term_count', 0)}")
    print(f"  Medium-term bets:   {summary.get('medium_term_count', 0)}")
    print(f"  Skipped:            {summary.get('skip_count', 0)}")
    print(f"  Total:              {summary.get('total_opportunities', 0)}")
    print(
        f"  Immediate revenue potential: IDR {summary.get('total_immediate_revenue_estimate_idr', 0):,.0f}/month"
    )
    print()

    # Print the playbook to stdout
    print("=" * 50)
    print(md_content)

    print()
    print("Done. Files saved:")
    print(f"  Markdown: {output_path}")
    print(f"  JSON:     {json_path}")


if __name__ == "__main__":
    main()
