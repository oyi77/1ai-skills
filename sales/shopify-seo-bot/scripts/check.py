#!/usr/bin/env python3
"""
Shopify SEO Bot — Capability check and status script.

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

SKILL_NAME = "shopify-seo-bot"
SKILL_DESCRIPTION = "自动优化 Shopify 店铺 SEO"

CAPABILITIES = [
    {"feature": "Product title optimization", "description": "优化产品标题以包含目标关键词"},
    {"feature": "Meta description generation", "description": "为产品和集合页生成SEO友好的meta描述"},
    {"feature": "Image ALT text optimization", "description": "自动生成图片ALT标签"},
    {"feature": "Keyword research", "description": "针对产品类别进行关键词研究"},
    {"feature": "Bulk optimization", "description": "批量优化最多100个产品"},
    {"feature": "Ranking tracking", "description": "追踪关键词排名变化"},
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
