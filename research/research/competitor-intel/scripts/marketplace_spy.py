#!/usr/bin/env python3
"""LYNK.id, TikTok profile, and Facebook Ads Library scraper."""

import argparse
import json
import os
import sys
import re

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[!] playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)


def _launch_browser(pw):
    """Launch headless Chromium with no-sandbox."""
    return pw.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )


def spy_lynk(username):
    """Scrape LYNK.id profile for products and contact info."""
    url = f"https://lynk.id/{username}"
    result = {
        "platform": "lynk.id",
        "username": username,
        "url": url,
        "products": [],
        "contact": {},
        "error": None,
    }

    try:
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            page = browser.new_page()
            page.goto(url, timeout=30000, wait_until="networkidle")
            page.wait_for_timeout(2000)

            # Scrape product/link items
            items = page.query_selector_all('[class*="product"], [class*="link-item"], [class*="card"]')
            for item in items:
                name_el = item.query_selector('[class*="title"], [class*="name"], h3, h4, p')
                price_el = item.query_selector('[class*="price"], [class*="amount"]')

                name = name_el.inner_text().strip() if name_el else ""
                price = price_el.inner_text().strip() if price_el else ""

                if name:
                    result["products"].append({"name": name, "price": price})

            # If no structured products found, try all links
            if not result["products"]:
                links = page.query_selector_all('a[href]')
                for link in links:
                    text = link.inner_text().strip()
                    href = link.get_attribute("href") or ""
                    if text and len(text) > 2 and not href.startswith("javascript"):
                        result["products"].append({"name": text, "price": "", "url": href})

            # Contact info
            page_text = page.content()
            email_match = re.findall(r'[\w.+-]+@[\w-]+\.[\w.]+', page_text)
            if email_match:
                result["contact"]["email"] = list(set(email_match))

            phone_match = re.findall(r'(?:\+62|08)\d[\d\-\s]{7,14}', page_text)
            if phone_match:
                result["contact"]["phone"] = list(set(phone_match))

            wa_match = re.findall(r'wa\.me/(\d+)', page_text)
            if wa_match:
                result["contact"]["whatsapp"] = list(set(wa_match))

            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def spy_tiktok_profile(username):
    """Scrape TikTok profile stats."""
    username = username.lstrip("@")
    url = f"https://www.tiktok.com/@{username}"
    result = {
        "platform": "tiktok",
        "username": username,
        "url": url,
        "followers": None,
        "following": None,
        "likes": None,
        "bio": None,
        "error": None,
    }

    try:
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            # Try to extract stats from data attributes or text
            stats_selectors = [
                '[data-e2e="followers-count"]',
                '[data-e2e="following-count"]',
                '[data-e2e="likes-count"]',
            ]
            stat_keys = ["followers", "following", "likes"]

            for sel, key in zip(stats_selectors, stat_keys):
                el = page.query_selector(sel)
                if el:
                    result[key] = el.inner_text().strip()

            # Bio
            bio_el = page.query_selector('[data-e2e="user-bio"], [class*="bio"], h2[class*="desc"]')
            if bio_el:
                result["bio"] = bio_el.inner_text().strip()

            # Fallback: parse from page source
            if not result["followers"]:
                content = page.content()
                follower_match = re.search(r'"followerCount"\s*:\s*(\d+)', content)
                following_match = re.search(r'"followingCount"\s*:\s*(\d+)', content)
                likes_match = re.search(r'"heartCount"\s*:\s*(\d+)', content)
                bio_match = re.search(r'"signature"\s*:\s*"([^"]*)"', content)

                if follower_match:
                    result["followers"] = follower_match.group(1)
                if following_match:
                    result["following"] = following_match.group(1)
                if likes_match:
                    result["likes"] = likes_match.group(1)
                if bio_match and not result["bio"]:
                    result["bio"] = bio_match.group(1)

            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def spy_facebook_ads(search_term):
    """Scrape Facebook Ads Library for active ads."""
    import urllib.parse
    encoded = urllib.parse.quote(search_term)
    url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ID&q={encoded}"
    result = {
        "platform": "facebook_ads_library",
        "search_term": search_term,
        "url": url,
        "active_ads_count": 0,
        "sample_ads": [],
        "error": None,
    }

    try:
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)

            # Try to get result count
            count_el = page.query_selector('[class*="total"], [class*="count"], [class*="result"]')
            if count_el:
                count_text = count_el.inner_text().strip()
                nums = re.findall(r'[\d,]+', count_text)
                if nums:
                    result["active_ads_count"] = int(nums[0].replace(",", ""))

            # Scrape ad cards
            ad_cards = page.query_selector_all('[class*="ad-card"], [class*="_7jvw"], div[role="article"]')
            if not ad_cards:
                # Broader fallback
                ad_cards = page.query_selector_all('div[class*="x1dr75xp"], div[class*="xrvj5dj"]')

            for card in ad_cards[:10]:  # Sample max 10
                text_el = card.query_selector('[class*="text"], [class*="body"], p, span')
                ad_text = text_el.inner_text().strip() if text_el else card.inner_text().strip()[:300]
                if ad_text:
                    result["sample_ads"].append(ad_text[:500])

            if not result["active_ads_count"] and result["sample_ads"]:
                result["active_ads_count"] = len(result["sample_ads"])

            # Fallback count from page
            if not result["active_ads_count"]:
                page_text = page.inner_text("body")
                count_match = re.search(r'(\d[\d,]*)\s*(?:results?|ads?|iklan)', page_text, re.IGNORECASE)
                if count_match:
                    result["active_ads_count"] = int(count_match.group(1).replace(",", ""))

            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Marketplace & social media spy tool")
    parser.add_argument("--target", required=True,
                        help='Target: "lynk:username", "tiktok:@user", "fbads:search term"')
    args = parser.parse_args()

    target = args.target
    if ":" not in target:
        print(f"[!] Invalid target format. Use platform:identifier")
        sys.exit(1)

    platform, identifier = target.split(":", 1)
    platform = platform.lower().strip()
    identifier = identifier.strip()

    if platform == "lynk":
        data = spy_lynk(identifier)
    elif platform == "tiktok":
        data = spy_tiktok_profile(identifier)
    elif platform == "fbads":
        data = spy_facebook_ads(identifier)
    else:
        print(f"[!] Unknown platform: {platform}")
        print("Supported: lynk, tiktok, fbads")
        sys.exit(1)

    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
