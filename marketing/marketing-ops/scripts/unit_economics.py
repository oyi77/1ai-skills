#!/usr/bin/env python3
"""
SaaS Unit Economics Calculator
Calculate LTV, CAC, payback period, and PLG funnel metrics.

Usage:
    python unit_economics.py --arpu 79 --churn 5 --cac 150
    python unit_economics.py --visitors 10000 --signup-rate 3 --activation 40 --conversion 5 --arpu 49 --churn 6 --spend 2000
"""

import argparse
import json
import sys


def calculate_unit_economics(arpu, churn_rate, cac, expansion_rate=0):
    """Calculate core SaaS unit economics."""
    ltv = arpu / (churn_rate / 100) if churn_rate > 0 else arpu * 100
    ltv_cac = ltv / cac if cac > 0 else float('inf')
    payback_months = cac / arpu if arpu > 0 else float('inf')
    nrr = (100 - churn_rate + expansion_rate)

    health = "HEALTHY" if ltv_cac >= 3 and payback_months <= 12 else (
        "WARNING" if ltv_cac >= 1.5 else "CRITICAL"
    )

    return {
        "inputs": {
            "monthly_arpu": f"${arpu:.2f}",
            "monthly_churn": f"{churn_rate}%",
            "customer_acquisition_cost": f"${cac:.2f}",
            "monthly_expansion_rate": f"{expansion_rate}%"
        },
        "metrics": {
            "ltv": f"${ltv:,.2f}",
            "ltv_cac_ratio": f"{ltv_cac:.1f}:1",
            "payback_months": f"{payback_months:.1f} months",
            "net_revenue_retention": f"{nrr:.1f}%",
            "annual_revenue_per_customer": f"${arpu * 12:,.2f}"
        },
        "health": health,
        "recommendations": get_recommendations(ltv_cac, payback_months, churn_rate, nrr)
    }


def calculate_plg_funnel(visitors, signup_rate, activation_rate, conversion_rate,
                          arpu, churn_rate, monthly_spend):
    """Calculate full PLG funnel metrics."""
    signups = visitors * (signup_rate / 100)
    activated = signups * (activation_rate / 100)
    customers = activated * (conversion_rate / 100)
    new_mrr = customers * arpu
    cac = monthly_spend / customers if customers > 0 else float('inf')
    ltv = arpu / (churn_rate / 100) if churn_rate > 0 else arpu * 100
    ltv_cac = ltv / cac if cac > 0 else float('inf')

    return {
        "funnel": {
            "visitors": f"{visitors:,.0f}",
            "signups": f"{signups:,.0f} ({signup_rate}% signup rate)",
            "activated": f"{activated:,.0f} ({activation_rate}% activation)",
            "customers": f"{customers:,.0f} ({conversion_rate}% free-to-paid)",
            "new_mrr": f"${new_mrr:,.2f}",
        },
        "economics": {
            "cac": f"${cac:,.2f}",
            "ltv": f"${ltv:,.2f}",
            "ltv_cac": f"{ltv_cac:.1f}:1",
            "payback": f"{cac/arpu:.1f} months" if arpu > 0 else "N/A",
        },
        "to_reach_targets": {
            "$5k_mrr": f"Need {5000/arpu:.0f} customers → {5000/arpu/conversion_rate*100/activation_rate*100/signup_rate*100:.0f} visitors/mo" if arpu > 0 else "N/A",
            "$10k_mrr": f"Need {10000/arpu:.0f} customers" if arpu > 0 else "N/A",
            "$50k_mrr": f"Need {50000/arpu:.0f} customers" if arpu > 0 else "N/A",
        }
    }


def get_recommendations(ltv_cac, payback, churn, nrr):
    recs = []
    if ltv_cac < 1:
        recs.append("CRITICAL: Losing money per customer. Reduce CAC or increase pricing immediately.")
    elif ltv_cac < 3:
        recs.append("LTV:CAC below 3:1. Focus on reducing CAC (organic channels) or increasing LTV (pricing, upsells).")
    else:
        recs.append("LTV:CAC healthy. Could invest more in growth.")

    if payback > 12:
        recs.append("Payback >12 months. Consider annual billing discounts to accelerate cash recovery.")
    if churn > 8:
        recs.append(f"Churn at {churn}% is high. Prioritize retention before acquisition.")
    if nrr < 100:
        recs.append("NRR below 100% — revenue is shrinking. Add expansion revenue (upsells, add-ons).")
    return recs


def main():
    parser = argparse.ArgumentParser(description="SaaS Unit Economics Calculator")
    parser.add_argument("--arpu", type=float, required=True, help="Monthly ARPU ($)")
    parser.add_argument("--churn", type=float, required=True, help="Monthly churn rate (%)")
    parser.add_argument("--cac", type=float, default=0, help="Customer acquisition cost ($)")
    parser.add_argument("--expansion", type=float, default=0, help="Monthly expansion rate (%)")
    parser.add_argument("--visitors", type=float, default=0, help="Monthly visitors (PLG mode)")
    parser.add_argument("--signup-rate", type=float, default=0, help="Visitor to signup rate (%)")
    parser.add_argument("--activation", type=float, default=0, help="Signup to activated rate (%)")
    parser.add_argument("--conversion", type=float, default=0, help="Free to paid rate (%)")
    parser.add_argument("--spend", type=float, default=0, help="Monthly marketing spend ($)")

    args = parser.parse_args()

    if args.visitors > 0 and args.signup_rate > 0:
        result = calculate_plg_funnel(
            args.visitors, args.signup_rate, args.activation,
            args.conversion, args.arpu, args.churn, args.spend
        )
    else:
        cac = args.cac if args.cac > 0 else (args.spend / 10 if args.spend > 0 else 100)
        result = calculate_unit_economics(args.arpu, args.churn, cac, args.expansion)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
