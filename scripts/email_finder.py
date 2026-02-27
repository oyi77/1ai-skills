#!/usr/bin/env python3
"""
Email Finder - Extract email addresses from Shopee shops and social media
"""

import re
import json
import asyncio
from typing import List, Dict, Optional
from pathlib import Path
import sys

# Add skills to path
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/skills/1ai-skills')

try:
    from web_fetch import web_fetch
except:
    # Fallback: use requests
    import requests
    def web_fetch(url: str, extractMode: str = 'text', maxChars: int = 50000) -> str:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }, timeout=30)
        return response.text[:maxChars]

# Email regex pattern
EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from text"""
    emails = EMAIL_PATTERN.findall(text)
    # Deduplicate and filter common non-business emails
    seen = set()
    result = []
    for email in emails:
        email_lower = email.lower()
        # Filter out common non-business emails
        if any(x in email_lower for x in ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']):
            # Still include if it looks professional
            if any(x in email_lower for x in ['official', 'store', 'shop', 'business', 'sales', 'contact']):
                if email_lower not in seen:
                    seen.add(email_lower)
                    result.append(email)
        else:
            # Business emails (domain-based)
            if email_lower not in seen:
                seen.add(email_lower)
                result.append(email)
    return result

def find_email_shopee_shop(shop_url: str) -> Optional[str]:
    """Try to find email in Shopee shop page"""
    try:
        print(f"  Fetching {shop_url}...")
        content = web_fetch(shop_url, extractMode='text', maxChars=100000)
        emails = extract_emails(content)
        if emails:
            print(f"  Found {len(emails)} email(s): {emails}")
            return emails[0]  # Return first found email
    except Exception as e:
        print(f"  Error: {e}")
    return None

def find_email_in_description(description: str) -> Optional[str]:
    """Try to find email in shop description"""
    if not description:
        return None
    emails = extract_emails(description)
    if emails:
        return emails[0]
    return None

async def find_emails_for_sellers(sellers_file: str, output_file: str):
    """Find emails for all sellers"""
    print(f"Loading sellers from {sellers_file}...")

    with open(sellers_file, 'r') as f:
        sellers = json.load(f)

    print(f"Found {len(sellers)} sellers")
    print("\nSearching for emails...")

    results = []
    for seller in sellers:
        print(f"\n[{seller['shop_name']}]")

        email = None
        source = None

        # Method 1: Try Shopee shop page
        email = find_email_shopee_shop(seller['shop_url'])
        if email:
            source = 'shopee_shop'

        # Method 2: Try extracting from products (if any have description)
        if not email and 'products' in seller:
            for product in seller['products']:
                if 'description' in product:
                    email = find_email_in_description(product['description'])
                    if email:
                        source = 'product_description'
                        break

        # Update seller with found email
        seller['email'] = email
        seller['email_source'] = source

        print(f"  Email: {email if email else 'NOT FOUND'}")
        if source:
            print(f"  Source: {source}")

        results.append(seller)

        # Rate limiting - wait a bit between requests
        await asyncio.sleep(2)

    # Save results
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"{'='*60}")

    found_emails = [s for s in results if s.get('email')]
    print(f"Total sellers: {len(results)}")
    print(f"Emails found: {len(found_emails)}")
    print(f"No emails: {len(results) - len(found_emails)}")

    if found_emails:
        print(f"\nSellers with emails:")
        for s in found_emails:
            print(f"  • {s['shop_name']}: {s['email']} (source: {s['email_source']})")

    print(f"\nResults saved to: {output_file}")

async def main():
    sellers_file = '/home/openclaw/.openclaw/workspace/output/market_research/sellers.json'
    output_file = '/home/openclaw/.openclaw/workspace/output/market_research/sellers_with_emails.json'

    await find_emails_for_sellers(sellers_file, output_file)

if __name__ == '__main__':
    asyncio.run(main())
