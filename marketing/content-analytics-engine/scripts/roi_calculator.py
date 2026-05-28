"""
roi_calculator.py — Cost per content vs revenue generated
Tracks ROI for each content piece and overall campaign
"""

from datetime import datetime
from collections import defaultdict


# Cost assumptions (IDR) — update these as actuals are known
COST_CONFIG = {
    "api_cost_per_post_idr": 0,        # PostBridge free tier
    "ai_generation_cost_per_post": 500, # Estimated OpenAI/Claude cost per post
    "time_cost_per_post_minutes": 2,    # Agent time to generate + schedule
    "hourly_rate_idr": 50000,           # Operator time cost IDR/hour
    "platform_fee_pct": 0,             # PostBridge no rev share
    "lynk_fee_pct": 5,                 # LYNK affiliate platform fee (est)
}

# Product prices (IDR)
PRODUCT_PRICES = {
    "MOVA": 0,
    "paid_1": 49000,
    "paid_2": 49000,
    "paid_3": 49000,
    "paid_4": 59000,
    "paid_5": 89000,
}


def cost_per_post(num_posts: int, config: dict = None) -> dict:
    """Calculate cost breakdown per post."""
    c = config or COST_CONFIG
    api_cost = c["api_cost_per_post_idr"]
    ai_cost = c["ai_generation_cost_per_post"]
    time_cost = (c["time_cost_per_post_minutes"] / 60) * c["hourly_rate_idr"]

    per_post = api_cost + ai_cost + time_cost
    total = per_post * num_posts

    return {
        "cost_per_post_idr": round(per_post),
        "total_cost_idr": round(total),
        "breakdown": {
            "api_cost": api_cost,
            "ai_generation": ai_cost,
            "time_cost": round(time_cost),
        },
        "num_posts": num_posts
    }


def revenue_summary(lynk_sales: int = 0, avg_product_price: int = 49000) -> dict:
    """Summarize revenue generated."""
    gross_revenue = lynk_sales * avg_product_price
    lynk_fee = round(gross_revenue * COST_CONFIG["lynk_fee_pct"] / 100)
    net_revenue = gross_revenue - lynk_fee

    return {
        "sales": lynk_sales,
        "avg_price_idr": avg_product_price,
        "gross_revenue_idr": gross_revenue,
        "platform_fee_idr": lynk_fee,
        "net_revenue_idr": net_revenue
    }


def compute_roi(analytics: list, posts: list, lynk_sales: int = 0,
                lynk_clicks: int = 196, config: dict = None) -> dict:
    """
    Full ROI calculation for the content campaign.

    Returns:
    - Total cost invested
    - Revenue generated
    - ROI %
    - Cost per view
    - Cost per click
    - Revenue per post
    - Break-even analysis
    """
    c = config or COST_CONFIG
    num_posts = len(posts)
    total_views = sum(a.get("view_count", 0) or 0 for a in analytics)
    total_engagement = sum(
        (a.get("like_count", 0) or 0)
        + (a.get("comment_count", 0) or 0)
        + (a.get("share_count", 0) or 0)
        for a in analytics
    )

    costs = cost_per_post(num_posts, c)
    revenue = revenue_summary(lynk_sales)

    total_cost = costs["total_cost_idr"]
    net_rev = revenue["net_revenue_idr"]
    profit = net_rev - total_cost
    roi_pct = round((profit / max(total_cost, 1)) * 100, 1)

    # Unit economics
    cost_per_view = round(total_cost / max(total_views, 1), 2)
    cost_per_click = round(total_cost / max(lynk_clicks, 1), 0)
    cost_per_engagement = round(total_cost / max(total_engagement, 1), 0)
    revenue_per_post = round(net_rev / max(num_posts, 1), 0)

    # Break-even: how many sales needed to cover cost?
    avg_price = 49000  # Avg paid product price
    lynk_fee = round(avg_price * c["lynk_fee_pct"] / 100)
    net_per_sale = avg_price - lynk_fee
    break_even_sales = max(1, round(total_cost / net_per_sale))
    break_even_views = round(break_even_sales / max(lynk_sales / max(total_views, 1), 0.001))

    # Current status
    if roi_pct > 0:
        status = "PROFITABLE ✅"
    elif net_rev > 0:
        status = "REVENUE BUT UNPROFITABLE ⚠️"
    else:
        status = "NO REVENUE — INVESTMENT STAGE 🔴"

    return {
        "status": status,
        "investment": {
            "total_cost_idr": total_cost,
            "cost_per_post_idr": costs["cost_per_post_idr"],
            "num_posts": num_posts,
            "cost_breakdown": costs["breakdown"]
        },
        "revenue": revenue,
        "profitability": {
            "profit_idr": profit,
            "roi_pct": roi_pct,
        },
        "unit_economics": {
            "cost_per_view_idr": cost_per_view,
            "cost_per_click_idr": int(cost_per_click),
            "cost_per_engagement_idr": int(cost_per_engagement),
            "revenue_per_post_idr": int(revenue_per_post),
        },
        "break_even": {
            "sales_needed": break_even_sales,
            "views_needed_est": break_even_views,
            "explanation": f"Need {break_even_sales} sales at avg IDR {avg_price:,} to cover IDR {total_cost:,} investment"
        },
        "totals": {
            "views": total_views,
            "engagement": total_engagement,
            "lynk_clicks": lynk_clicks,
        },
        "calculated_at": datetime.now().isoformat()
    }


def platform_roi_breakdown(analytics: list, post_results: list,
                           social_accounts: list) -> dict:
    """Break down ROI investment by platform."""
    account_map = {a["id"]: a for a in social_accounts}

    platform_posts = defaultdict(set)
    for r in post_results:
        if r.get("success"):
            acct = account_map.get(r.get("social_account_id"), {})
            platform = acct.get("platform", "unknown")
            platform_posts[platform].add(r["post_id"])

    platform_analytics = defaultdict(list)
    for a in analytics:
        p = a.get("platform", "unknown")
        platform_analytics[p].append(a)

    result = {}
    for platform in set(list(platform_posts.keys()) + list(platform_analytics.keys())):
        p_posts = len(platform_posts.get(platform, set()))
        p_analytics = platform_analytics.get(platform, [])
        p_views = sum(a.get("view_count", 0) or 0 for a in p_analytics)
        p_cost = cost_per_post(p_posts)["total_cost_idr"]

        result[platform] = {
            "posts_published": p_posts,
            "analytics_tracked": len(p_analytics),
            "total_views": p_views,
            "estimated_cost_idr": p_cost,
            "cost_per_view_idr": round(p_cost / max(p_views, 1), 2),
            "views_per_post": round(p_views / max(len(p_analytics), 1), 1),
        }

    return dict(sorted(result.items(), key=lambda x: x[1]["total_views"], reverse=True))


if __name__ == "__main__":
    import sys, json
    sys.path.insert(0, ".")
    from analytics_collector import collect_all

    data = collect_all(use_cache=True)
    roi = compute_roi(data["analytics"], data["posts"])

    print("💰 ROI ANALYSIS")
    print(f"Status: {roi['status']}")
    print(f"Total Cost: IDR {roi['investment']['total_cost_idr']:,}")
    print(f"Revenue: IDR {roi['revenue']['net_revenue_idr']:,}")
    print(f"ROI: {roi['profitability']['roi_pct']}%")
    print(f"\nBreak-even: {roi['break_even']['explanation']}")
