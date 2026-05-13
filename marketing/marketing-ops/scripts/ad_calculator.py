#!/usr/bin/env python3
"""
Ad Spend & ROI Calculator
Calculates expected results from advertising budget inputs.

Usage:
    python ad_calculator.py --budget 5000 --cpc 1.50 --conv-rate 3.0 --avg-order 50
    python ad_calculator.py --budget 10000 --cpl 25 --close-rate 20 --ltv 500
"""

import argparse
import json
import sys


def calculate_ecommerce(budget, cpc, conv_rate, avg_order_value, margin_pct=50):
    """Calculate e-commerce ad performance projections."""
    clicks = budget / cpc
    conversions = clicks * (conv_rate / 100)
    revenue = conversions * avg_order_value
    gross_profit = revenue * (margin_pct / 100)
    roas = revenue / budget if budget > 0 else 0
    cpa = budget / conversions if conversions > 0 else 0
    net_profit = gross_profit - budget

    return {
        "model": "E-commerce",
        "inputs": {
            "monthly_budget": f"${budget:,.2f}",
            "cost_per_click": f"${cpc:.2f}",
            "conversion_rate": f"{conv_rate}%",
            "avg_order_value": f"${avg_order_value:.2f}",
            "profit_margin": f"{margin_pct}%"
        },
        "projections": {
            "clicks": f"{clicks:,.0f}",
            "conversions": f"{conversions:,.0f}",
            "revenue": f"${revenue:,.2f}",
            "roas": f"{roas:.1f}x",
            "cost_per_acquisition": f"${cpa:.2f}",
            "gross_profit": f"${gross_profit:,.2f}",
            "net_profit_after_ads": f"${net_profit:,.2f}",
        },
        "verdict": "PROFITABLE" if net_profit > 0 else "UNPROFITABLE",
        "breakeven_roas": f"{1/(margin_pct/100):.1f}x" if margin_pct > 0 else "N/A"
    }


def calculate_leadgen(budget, cost_per_lead, close_rate, ltv):
    """Calculate lead generation ad performance projections."""
    leads = budget / cost_per_lead if cost_per_lead > 0 else 0
    customers = leads * (close_rate / 100)
    total_revenue = customers * ltv
    cac = budget / customers if customers > 0 else 0
    ltv_cac_ratio = ltv / cac if cac > 0 else 0
    roi_pct = ((total_revenue - budget) / budget * 100) if budget > 0 else 0

    return {
        "model": "Lead Generation",
        "inputs": {
            "monthly_budget": f"${budget:,.2f}",
            "cost_per_lead": f"${cost_per_lead:.2f}",
            "close_rate": f"{close_rate}%",
            "customer_ltv": f"${ltv:,.2f}"
        },
        "projections": {
            "leads_generated": f"{leads:,.0f}",
            "new_customers": f"{customers:,.0f}",
            "total_ltv_revenue": f"${total_revenue:,.2f}",
            "customer_acquisition_cost": f"${cac:.2f}",
            "ltv_to_cac_ratio": f"{ltv_cac_ratio:.1f}:1",
            "roi": f"{roi_pct:.0f}%"
        },
        "verdict": "HEALTHY" if ltv_cac_ratio >= 3 else ("MARGINAL" if ltv_cac_ratio >= 1 else "UNSUSTAINABLE"),
        "benchmark_notes": {
            "below_1_to_1": "Losing money on every customer. Fix urgently.",
            "1_to_2": "Unsustainable. Reduce CAC or increase LTV.",
            "3_to_1": "Healthy. Standard target.",
            "5_plus": "Very efficient. Could spend more to grow faster."
        }
    }


def calculate_funnel_math(target_revenue, avg_deal_size, close_rate, lead_rate, cpc):
    """Reverse-engineer from revenue target to required ad spend."""
    target_customers = target_revenue / avg_deal_size if avg_deal_size > 0 else 0
    required_leads = target_customers / (close_rate / 100) if close_rate > 0 else 0
    required_clicks = required_leads / (lead_rate / 100) if lead_rate > 0 else 0
    required_budget = required_clicks * cpc

    return {
        "model": "Funnel Math (Reverse)",
        "target": f"${target_revenue:,.2f} revenue",
        "funnel": {
            "target_customers": f"{target_customers:,.0f}",
            "required_leads": f"{required_leads:,.0f} (at {close_rate}% close rate)",
            "required_clicks": f"{required_clicks:,.0f} (at {lead_rate}% lead capture rate)",
            "required_budget": f"${required_budget:,.2f}/month (at ${cpc:.2f} CPC)",
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Ad Spend & ROI Calculator")
    subparsers = parser.add_subparsers(dest="mode", help="Calculation mode")

    # E-commerce mode
    ecom = subparsers.add_parser("ecom", help="E-commerce ROAS calculation")
    ecom.add_argument("--budget", type=float, required=True, help="Monthly ad budget")
    ecom.add_argument("--cpc", type=float, required=True, help="Cost per click")
    ecom.add_argument("--conv-rate", type=float, required=True, help="Conversion rate (%)")
    ecom.add_argument("--avg-order", type=float, required=True, help="Average order value")
    ecom.add_argument("--margin", type=float, default=50, help="Profit margin (%)")

    # Lead gen mode
    lead = subparsers.add_parser("leadgen", help="Lead generation ROI calculation")
    lead.add_argument("--budget", type=float, required=True, help="Monthly ad budget")
    lead.add_argument("--cpl", type=float, required=True, help="Cost per lead")
    lead.add_argument("--close-rate", type=float, required=True, help="Lead-to-customer rate (%)")
    lead.add_argument("--ltv", type=float, required=True, help="Customer lifetime value")

    # Funnel math mode
    funnel = subparsers.add_parser("funnel", help="Reverse funnel calculation")
    funnel.add_argument("--target", type=float, required=True, help="Target monthly revenue")
    funnel.add_argument("--deal-size", type=float, required=True, help="Average deal size")
    funnel.add_argument("--close-rate", type=float, required=True, help="Close rate (%)")
    funnel.add_argument("--lead-rate", type=float, required=True, help="Click-to-lead rate (%)")
    funnel.add_argument("--cpc", type=float, required=True, help="Cost per click")

    args = parser.parse_args()

    if args.mode == "ecom":
        result = calculate_ecommerce(args.budget, args.cpc, args.conv_rate, args.avg_order, args.margin)
    elif args.mode == "leadgen":
        result = calculate_leadgen(args.budget, args.cpl, args.close_rate, args.ltv)
    elif args.mode == "funnel":
        result = calculate_funnel_math(args.target, args.deal_size, args.close_rate, args.lead_rate, args.cpc)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
