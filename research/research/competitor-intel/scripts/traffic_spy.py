#!/usr/bin/env python3
"""Similarweb traffic spy — scrape website analytics data."""

import argparse
import json
import re
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print(
        "[!] playwright not installed. Run: pip install playwright && playwright install chromium"
    )
    sys.exit(1)


def _launch_browser(pw):
    """Launch headless Chromium."""
    return pw.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-dev-shm-usage"],
    )


def _parse_number(text):
    """Parse human-readable numbers like '1.2M', '500K', '3.5B'."""
    if not text:
        return text
    text = text.strip().replace(",", "")
    multipliers = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}
    for suffix, mult in multipliers.items():
        if text.upper().endswith(suffix):
            try:
                return str(int(float(text[:-1]) * mult))
            except ValueError:
                pass
    return text


def spy_traffic(domain):
    """Scrape Similarweb for traffic data."""
    domain = domain.replace("https://", "").replace("http://", "").rstrip("/")
    url = f"https://www.similarweb.com/website/{domain}/"

    result = {
        "domain": domain,
        "url": url,
        "monthly_visits": None,
        "bounce_rate": None,
        "pages_per_visit": None,
        "avg_duration": None,
        "traffic_sources": {
            "direct": None,
            "organic": None,
            "social": None,
            "referral": None,
            "paid": None,
        },
        "top_countries": [],
        "error": None,
    }

    try:
        with sync_playwright() as pw:
            browser = _launch_browser(pw)
            page = browser.new_page(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page.goto(url, timeout=30000, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            content = page.content()

            # --- Engagement metrics ---
            # Monthly visits
            visits_el = page.query_selector(
                '[data-test="total-visits"] .engagement-list__item-value, [class*="engagement-list"] .engagement-list__item-value'
            )
            if visits_el:
                result["monthly_visits"] = _parse_number(visits_el.inner_text())

            # Try structured selectors for engagement metrics
            engagement_items = page.query_selector_all(".engagement-list__item")
            for item in engagement_items:
                label_el = item.query_selector(".engagement-list__item-name")
                value_el = item.query_selector(".engagement-list__item-value")
                if not label_el or not value_el:
                    continue
                label = label_el.inner_text().strip().lower()
                value = value_el.inner_text().strip()

                if "total visit" in label or "monthly" in label:
                    result["monthly_visits"] = _parse_number(value)
                elif "bounce" in label:
                    result["bounce_rate"] = value
                elif "pages" in label or "page" in label:
                    result["pages_per_visit"] = value
                elif "duration" in label or "time" in label:
                    result["avg_duration"] = value

            # Fallback: regex from page source
            if not result["monthly_visits"]:
                m = re.search(r'"visits":\s*"?(\d[\d,.]*[KMB]?)"?', content)
                if m:
                    result["monthly_visits"] = _parse_number(m.group(1))

            if not result["bounce_rate"]:
                m = re.search(r'"bounceRate":\s*"?([\d.]+%?)"?', content)
                if m:
                    result["bounce_rate"] = m.group(1)

            if not result["pages_per_visit"]:
                m = re.search(r'"pagesPerVisit":\s*"?([\d.]+)"?', content)
                if m:
                    result["pages_per_visit"] = m.group(1)

            if not result["avg_duration"]:
                m = re.search(r'"avgVisitDuration":\s*"?([^",}]+)"?', content)
                if m:
                    result["avg_duration"] = m.group(1)

            # --- Traffic sources ---
            source_mapping = {
                "direct": ["direct"],
                "organic": ["organic", "search"],
                "social": ["social"],
                "referral": ["referral", "referrals"],
                "paid": ["paid", "display", "ads"],
            }

            # Try structured elements
            source_items = page.query_selector_all(
                '[class*="traffic-sources"] [class*="item"], [class*="channel-data"]'
            )
            for item in source_items:
                label_el = item.query_selector('[class*="name"], [class*="label"]')
                value_el = item.query_selector('[class*="value"], [class*="percent"]')
                if not label_el or not value_el:
                    continue
                label = label_el.inner_text().strip().lower()
                value = value_el.inner_text().strip()

                for key, keywords in source_mapping.items():
                    if any(kw in label for kw in keywords):
                        result["traffic_sources"][key] = value
                        break

            # Fallback: regex
            for key in result["traffic_sources"]:
                if not result["traffic_sources"][key]:
                    pattern = rf'"{key}":\s*\{{\s*[^}}]*?"share":\s*"?([\d.]+%?)"?'
                    m = re.search(pattern, content, re.IGNORECASE)
                    if m:
                        result["traffic_sources"][key] = m.group(1)

            # --- Top countries ---
            country_items = page.query_selector_all(
                '[class*="countries"] [class*="item"], [data-test*="country"]'
            )
            for item in country_items[:10]:
                name_el = item.query_selector('[class*="name"], [class*="country"]')
                pct_el = item.query_selector(
                    '[class*="value"], [class*="percent"], [class*="traffic"]'
                )
                if name_el:
                    country = {
                        "name": name_el.inner_text().strip(),
                        "share": pct_el.inner_text().strip() if pct_el else "",
                    }
                    if country["name"]:
                        result["top_countries"].append(country)

            # Fallback: try to get countries from JSON data in page
            if not result["top_countries"]:
                country_matches = re.findall(
                    r'"countryName":\s*"([^"]+)"[^}]*?"trafficShare":\s*"?([\d.]+)',
                    content,
                )
                for name, share in country_matches[:10]:
                    result["top_countries"].append({"name": name, "share": f"{share}%"})

            browser.close()

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description="Similarweb traffic spy")
    parser.add_argument(
        "--domain", required=True, help="Domain to analyze (e.g. berkahkarya.org)"
    )
    args = parser.parse_args()

    data = spy_traffic(args.domain)
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
