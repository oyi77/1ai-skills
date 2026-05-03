#!/usr/bin/env python3
"""SEO Audit Script — fetches a URL, analyzes on-page SEO factors,
sends findings to OmniRoute LLM for recommendations, and outputs JSON."""

import argparse
import json
import re
import sys
import time
from collections import Counter
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ── helpers ──────────────────────────────────────────────────────────────────

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "is", "it", "as", "be", "are", "was", "were",
    "this", "that", "from", "not", "your", "you", "we", "our", "can",
    "will", "has", "have", "had", "do", "does", "did", "so", "if", "no",
    "all", "its", "than", "more", "also", "about", "up", "out", "just",
    "into", "over", "after", "been", "would", "could", "should", "may",
    "might", "must", "shall", "each", "which", "their", "them", "then",
    "when", "what", "how", "who", "where", "why", "any", "some", "very",
    "own", "same", "other", "such", "only", "new", "one", "two", "he",
    "she", "his", "her", "my", "me", "us",
}


def _visible_text(soup: BeautifulSoup) -> str:
    """Extract visible body text, stripping scripts/styles."""
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def _keyword_density(text: str, top_n: int = 10) -> list[dict]:
    words = re.findall(r"[a-z]{3,}", text.lower())
    filtered = [w for w in words if w not in STOP_WORDS]
    total = len(filtered) or 1
    counts = Counter(filtered).most_common(top_n)
    return [
        {"word": w, "count": c, "density_pct": round(c / total * 100, 2)}
        for w, c in counts
    ]


# ── core audit ───────────────────────────────────────────────────────────────

def audit_url(url: str) -> dict:
    """Fetch *url* and return a structured SEO audit dict."""
    parsed_base = urlparse(url)
    base_domain = parsed_base.netloc

    # -- fetch page & measure load time --
    start = time.perf_counter()
    resp = requests.get(url, timeout=30, headers={
        "User-Agent": "OpenClaw-SEO-Audit/1.0"
    })
    load_time_ms = round((time.perf_counter() - start) * 1000)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # 1. Title tag
    title_tag = soup.find("title")
    title_text = title_tag.get_text(strip=True) if title_tag else ""
    title_len = len(title_text)
    if not title_text:
        title_status = "missing"
    elif 50 <= title_len <= 60:
        title_status = "good"
    elif title_len < 50:
        title_status = "warning_short"
    else:
        title_status = "warning_long"

    # 2. Meta description
    meta_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    meta_text = meta_tag.get("content", "").strip() if meta_tag else ""
    meta_len = len(meta_text)
    if not meta_text:
        meta_status = "missing"
    elif 150 <= meta_len <= 160:
        meta_status = "good"
    elif meta_len < 150:
        meta_status = "warning_short"
    else:
        meta_status = "warning_long"

    # 3. Heading structure
    headings = {}
    for level in ("h1", "h2", "h3"):
        headings[level] = len(soup.find_all(level))

    # 4. Keyword density
    body_text = _visible_text(BeautifulSoup(resp.text, "html.parser"))
    keywords = _keyword_density(body_text)

    # 5. Image alt tags
    images = soup.find_all("img")
    total_images = len(images)
    with_alt = sum(1 for img in images if img.get("alt", "").strip())
    missing_alt = total_images - with_alt

    # 6. Internal vs external links
    anchors = soup.find_all("a", href=True)
    internal_count = 0
    external_count = 0
    for a in anchors:
        href = a["href"]
        link_parsed = urlparse(href)
        if link_parsed.scheme in ("http", "https"):
            if link_parsed.netloc == base_domain:
                internal_count += 1
            else:
                external_count += 1
        elif href.startswith("/") or href.startswith("#"):
            internal_count += 1

    # -- assemble findings --
    findings = {
        "url": url,
        "title": {
            "value": title_text,
            "length": title_len,
            "status": title_status,
        },
        "meta_description": {
            "value": meta_text,
            "length": meta_len,
            "status": meta_status,
        },
        "headings": headings,
        "keyword_density": keywords,
        "images": {
            "total": total_images,
            "with_alt": with_alt,
            "missing_alt": missing_alt,
        },
        "links": {
            "internal": internal_count,
            "external": external_count,
        },
        "load_time_ms": load_time_ms,
    }
    return findings


# ── LLM analysis via OmniRoute ──────────────────────────────────────────────

def llm_analyze(findings: dict) -> dict:
    """Send audit findings to OmniRoute LLM and return score + recommendations."""
    client = OpenAI(
        base_url="http://localhost:20128/v1",
        api_key="omniroute",
    )

    prompt = (
        "You are an expert SEO analyst. Given the following on-page SEO audit "
        "data for a webpage, provide:\n"
        "1. An overall SEO score from 0-100.\n"
        "2. A list of actionable recommendations to improve the page's SEO.\n\n"
        "Return your answer as valid JSON with exactly two keys:\n"
        '  "score": <int>,\n'
        '  "recommendations": [<string>, ...]\n\n'
        "Audit data:\n"
        f"```json\n{json.dumps(findings, indent=2)}\n```"
    )

    try:
        completion = client.chat.completions.create(
            model="auto",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        raw = completion.choices[0].message.content.strip()
        # Extract JSON from possible markdown fences
        json_match = re.search(r"\{[\s\S]*\}", raw)
        if json_match:
            analysis = json.loads(json_match.group())
        else:
            analysis = json.loads(raw)
        return {
            "score": int(analysis.get("score", 0)),
            "recommendations": analysis.get("recommendations", []),
        }
    except Exception as exc:
        return {
            "score": 0,
            "recommendations": [f"LLM analysis unavailable: {exc}"],
        }


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="On-page SEO audit tool")
    parser.add_argument("--url", required=True, help="URL to audit")
    args = parser.parse_args()

    url = args.url
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        findings = audit_url(url)
    except requests.RequestException as exc:
        print(json.dumps({"error": f"Failed to fetch URL: {exc}"}, indent=2))
        sys.exit(1)

    analysis = llm_analyze(findings)

    output = {
        "url": findings["url"],
        "score": analysis["score"],
        "title": findings["title"],
        "meta_description": findings["meta_description"],
        "headings": findings["headings"],
        "keyword_density": findings["keyword_density"],
        "images": findings["images"],
        "links": findings["links"],
        "load_time_ms": findings["load_time_ms"],
        "recommendations": analysis["recommendations"],
    }

    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
