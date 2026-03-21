#!/usr/bin/env python3
"""
Clean Content Fetch — Extract readable content from any URL.
Strips ads, navigation, footers, and noise. Returns structured output.

Usage:
    python clean_fetch.py --url https://example.com
    python clean_fetch.py --url https://example.com --json
    python clean_fetch.py --url https://example.com --max-chars 5000
"""

import argparse
import json
import sys

def fetch_and_clean(url, max_chars=30000):
    """Fetch URL and extract clean readable content."""
    try:
        import requests
    except ImportError:
        print("Missing dependency: pip install requests", file=sys.stderr)
        sys.exit(1)

    try:
        from readability import Document
    except ImportError:
        Document = None

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("Missing dependency: pip install beautifulsoup4", file=sys.stderr)
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; OpenClaw/1.0; +https://openclaw.com)"
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    html = resp.text

    title = ""
    text = ""

    # Try readability-lxml first (best extraction)
    if Document is not None:
        try:
            doc = Document(html)
            title = doc.title()
            summary_html = doc.summary()
            soup = BeautifulSoup(summary_html, "html.parser")
            text = soup.get_text(separator="\n", strip=True)
        except Exception:
            Document = None  # fall through to BeautifulSoup

    # Fallback: BeautifulSoup manual extraction
    if not text:
        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        if soup.title:
            title = soup.title.get_text(strip=True)

        # Remove noise elements
        for tag in soup.find_all(["nav", "header", "footer", "aside", "script",
                                   "style", "noscript", "iframe", "form"]):
            tag.decompose()

        # Remove common ad/nav classes
        noise_patterns = ["sidebar", "menu", "nav", "footer", "header", "ad",
                          "banner", "popup", "modal", "cookie", "social"]
        for pattern in noise_patterns:
            for el in soup.find_all(class_=lambda c: c and pattern in str(c).lower()):
                el.decompose()
            for el in soup.find_all(id=lambda i: i and pattern in str(i).lower()):
                el.decompose()

        # Try content selectors in priority order
        content = None
        for selector in ["article", "main", "[role='main']",
                         ".post-content", ".article-content", ".entry-content",
                         ".content", "#content"]:
            content = soup.select_one(selector)
            if content:
                break

        if not content:
            content = soup.body or soup

        text = content.get_text(separator="\n", strip=True)

    # Truncate
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[truncated]"

    word_count = len(text.split())

    return {
        "title": title,
        "text": text,
        "url": url,
        "word_count": word_count
    }


def main():
    parser = argparse.ArgumentParser(description="Fetch clean readable content from a URL")
    parser.add_argument("--url", required=True, help="URL to fetch")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    parser.add_argument("--max-chars", type=int, default=30000, help="Max characters (default: 30000)")
    args = parser.parse_args()

    result = fetch_and_clean(args.url, args.max_chars)

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Title: {result['title']}")
        print(f"URL: {result['url']}")
        print(f"Words: {result['word_count']}")
        print(f"\n{'='*60}\n")
        print(result["text"])


if __name__ == "__main__":
    main()
