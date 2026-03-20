#!/usr/bin/env python3
"""
Post affiliate products to social media via PostBridge API.
Usage: python3 post_to_social.py --platform facebook --account "WARZ" --product-file products.json
"""

import argparse
import json
import random
import requests
from datetime import datetime, timedelta
from pathlib import Path

# Config
POSTBRIDGE_API_KEY = "pb_live_AT9Xm4PKaYBzAvFZYGgexi"
POSTBRIDGE_BASE_URL = "https://api.post-bridge.com/v1"

def load_captions():
    """Load caption templates."""
    template_file = Path(__file__).parent.parent / "templates" / "captions.json"
    with open(template_file) as f:
        return json.load(f)

def load_products():
    """Load products to promote."""
    products_file = Path(__file__).parent.parent / "data" / "products.json"
    if products_file.exists():
        with open(products_file) as f:
            return json.load(f)
    return []

def generate_caption(product, templates):
    """Generate viral caption for product."""
    hook = random.choice(templates["viral_hooks"])
    cta = random.choice(templates["cta_variants"])
    
    # Format caption
    caption = hook.format(
        product=product.get("name", "Produk Keren"),
        price=product.get("price", "???"),
        category=product.get("category", "produk"),
        discount=product.get("discount", "50")
    )
    
    # Add hashtags
    hashtags = templates["hashtags"]["general"][:5]
    if product.get("category") in templates["hashtags"]:
        hashtags += templates["hashtags"][product["category"]][:3]
    
    return f"{caption}\n\n{cta}\n\n{' '.join(hashtags)}"

def get_account_id(platform, username):
    """Get PostBridge account ID by username."""
    headers = {"Authorization": f"Bearer {POSTBRIDGE_API_KEY}"}
    resp = requests.get(
        f"{POSTBRIDGE_BASE_URL}/social-accounts",
        headers=headers,
        params={"limit": 100}
    )
    
    if resp.status_code == 200:
        accounts = resp.json().get("data", [])
        for acc in accounts:
            if acc["platform"] == platform and acc["username"] == username:
                return acc["id"]
    return None

def schedule_post(account_ids, caption, media_urls=None, scheduled_time=None):
    """Schedule a post via PostBridge."""
    headers = {
        "Authorization": f"Bearer {POSTBRIDGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    if scheduled_time is None:
        scheduled_time = datetime.now() + timedelta(minutes=5)
    
    payload = {
        "caption": caption,
        "scheduled_at": scheduled_time.isoformat(),
        "social_accounts": account_ids,
    }
    
    if media_urls:
        payload["media"] = media_urls
    
    resp = requests.post(
        f"{POSTBRIDGE_BASE_URL}/posts",
        headers=headers,
        json=payload
    )
    
    return resp.json()

def main():
    parser = argparse.ArgumentParser(description="Post to social media via PostBridge")
    parser.add_argument("--platform", default="facebook", help="Platform: facebook, instagram, tiktok")
    parser.add_argument("--account", required=True, help="Account username")
    parser.add_argument("--caption", help="Custom caption (optional)")
    parser.add_argument("--schedule", help="Schedule time (ISO format)")
    
    args = parser.parse_args()
    
    templates = load_captions()
    products = load_products()
    
    if not products:
        print("No products found. Add products first with add_product.py")
        return
    
    # Get random product
    product = random.choice(products)
    
    # Generate caption
    caption = args.caption or generate_caption(product, templates)
    
    # Get account ID
    account_id = get_account_id(args.platform, args.account)
    if not account_id:
        print(f"Account {args.account} not found on {args.platform}")
        return
    
    # Schedule post
    result = schedule_post([account_id], caption)
    print(f"Post scheduled: {json.dumps(result, indent=2)}")

if __name__ == "__main__":
    main()
