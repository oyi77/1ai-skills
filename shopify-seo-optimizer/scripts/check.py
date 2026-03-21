#!/usr/bin/env python3
"""
Shopify SEO Optimizer — Capability check and status script.

Shopify integration requires store credentials (API key + store URL).
This script shows what the skill can do and checks readiness.

Usage:
    python check.py
    python check.py --output json
"""

import argparse
import json
import os
import sys

SKILL_NAME = "shopify-seo-optimizer"
SKILL_DESCRIPTION = "专为 Shopify 店铺设计的 SEO 优化工具"

CAPABILITIES = [
    {"feature": "Product page optimization", "description": "优化产品页标题、描述、meta标签"},
    {"feature": "Collection page optimization", "description": "优化集合页SEO元素"},
    {"feature": "Meta tag generation", "description": "自动生成SEO友好的元标签"},
    {"feature": "Image ALT optimization", "description": "批量优化图片ALT文本"},
    {"feature": "URL structure optimization", "description": "优化URL结构和handle"},
    {"feature": "Internal linking suggestions", "description": "提供内链优化建议"},
    {"feature": "Speed optimization tips", "description": "页面速度优化建议"},
    {"feature": "Structured data (Schema)", "description": "生成结构化数据标记"},
    {"feature": "SEO audit", "description": "全站SEO审计报告"},
    {"feature": "Bulk optimization", "description": "批量处理最多50个页面"},
]

REQUIRED_ENV = {
    "SHOPIFY_STORE_URL": "Shopify store URL (e.g., your-store.myshopify.com)",
    "SHOPIFY_API_KEY": "Shopify Admin API access token",
}


def check_readiness():
    """Check if Shopify credentials are configured."""
    status = {}
    all_ready = True

    for var, desc in REQUIRED_ENV.items():
        value = os.environ.get(var)
        if value:
            status[var] = {"configured": True, "description": desc}
        else:
            status[var] = {"configured": False, "description": desc}
            all_ready = False

    return {
        "ready": all_ready,
        "credentials": status
    }


def main():
    parser = argparse.ArgumentParser(description=f"{SKILL_NAME} — capability check")
    parser.add_argument("--output", choices=["json", "text"], default="text")
    args = parser.parse_args()

    readiness = check_readiness()

    result = {
        "skill": SKILL_NAME,
        "description": SKILL_DESCRIPTION,
        "capabilities": CAPABILITIES,
        "readiness": readiness,
        "setup_instructions": [
            "1. Get Shopify Admin API access token from your store admin",
            "2. Set environment variables:",
            f"   export SHOPIFY_STORE_URL=your-store.myshopify.com",
            f"   export SHOPIFY_API_KEY=shpat_xxxxx",
            "3. Re-run this check to verify configuration",
        ]
    }

    if args.output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"{'='*50}")
        print(f"  {SKILL_NAME}")
        print(f"  {SKILL_DESCRIPTION}")
        print(f"{'='*50}\n")

        print("Capabilities:")
        for cap in CAPABILITIES:
            print(f"  ✓ {cap['feature']}: {cap['description']}")

        print(f"\nReadiness: {'✓ READY' if readiness['ready'] else '✗ NOT CONFIGURED'}\n")

        if not readiness["ready"]:
            print("Missing credentials:")
            for var, info in readiness["credentials"].items():
                status = "✓" if info["configured"] else "✗"
                print(f"  {status} {var}: {info['description']}")

            print("\nSetup:")
            for step in result["setup_instructions"]:
                print(f"  {step}")


if __name__ == "__main__":
    main()
