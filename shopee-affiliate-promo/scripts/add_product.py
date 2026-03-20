#!/usr/bin/env python3
"""
Add product to promotion list with affiliate link.
Usage: python3 add_product.py "https://shopee.co.id/product/123/456" "Product Name" "99000"
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

# Affiliate ID for griyadalaman
AFFILIATE_ID = "11392860738"
DATA_DIR = Path(__file__).parent.parent / "data"

def extract_product_ids(url):
    """Extract shop_id and item_id from Shopee URL."""
    # Pattern: https://shopee.co.id/product/{shop_id}/{item_id}
    # Or: https://shopee.co.id/{product-name}-i.{shop_id}.{item_id}
    
    patterns = [
        r'shopee\.co\.id/product/(\d+)/(\d+)',
        r'shopee\.co\.id/[^/]+-i\.(\d+)\.(\d+)',
        r'shope\.ee/([A-Za-z0-9]+)',  # Short URL
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            if len(match.groups()) == 2:
                return match.group(1), match.group(2)
            else:
                return None, match.group(1)  # Short URL
    return None, None

def generate_affiliate_link(shop_id, item_id):
    """Generate Shopee affiliate link."""
    if shop_id and item_id:
        return f"https://s.shopee.co.id/affiliate/{AFFILIATE_ID}/{shop_id}/{item_id}"
    return None

def load_products():
    """Load existing products."""
    products_file = DATA_DIR / "products.json"
    if products_file.exists():
        with open(products_file) as f:
            return json.load(f)
    return []

def save_products(products):
    """Save products to file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    products_file = DATA_DIR / "products.json"
    with open(products_file, 'w') as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

def add_product(url, name, price, category="general"):
    """Add a product to the promotion list."""
    shop_id, item_id = extract_product_ids(url)
    
    product = {
        "id": f"{shop_id}_{item_id}" if shop_id else url,
        "name": name,
        "price": price,
        "category": category,
        "original_url": url,
        "affiliate_link": generate_affiliate_link(shop_id, item_id) or url,
        "shop_id": shop_id,
        "item_id": item_id,
        "added_at": datetime.now().isoformat(),
        "posted_count": 0
    }
    
    products = load_products()
    
    # Check if already exists
    existing = [p for p in products if p["id"] == product["id"]]
    if existing:
        print(f"Product already exists: {name}")
        return False
    
    products.append(product)
    save_products(products)
    
    print(f"✅ Product added: {name}")
    print(f"   Affiliate link: {product['affiliate_link']}")
    return True

def list_products():
    """List all products."""
    products = load_products()
    print(f"\n📦 Total products: {len(products)}\n")
    for i, p in enumerate(products, 1):
        print(f"{i}. {p['name']} - Rp{p['price']}")
        print(f"   Link: {p['affiliate_link']}")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Add product: python3 add_product.py <url> <name> <price> [category]")
        print("  List products: python3 add_product.py --list")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_products()
    else:
        url = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else "Unknown Product"
        price = sys.argv[3] if len(sys.argv) > 3 else "0"
        category = sys.argv[4] if len(sys.argv) > 4 else "general"
        
        add_product(url, name, price, category)
