#!/usr/bin/env python3
"""
social_scraper.py — Real web scraping for social platforms, no API keys needed.

Supports: Twitter/X (via Nitter), TikTok, Instagram (via Picuki), YouTube.

Usage:
    from scrapers.social_scraper import SocialScraper

    scraper = SocialScraper()
    results = scraper.search("productivity hacks", platform="twitter", limit=20)
    trending = scraper.get_trending(platform="tiktok", category="tech")
"""

import json
import logging
import os
import re
import random
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus, urlparse

import requests
from bs4 import BeautifulSoup

log = logging.getLogger("social_scraper")

# ─── User-Agent Pool ──────────────────────────────────────────────────────────

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Android 14; Mobile; rv:125.0) Gecko/125.0 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0",
]

# ─── Nitter instances (fallback order) ────────────────────────────────────────

NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.privacydev.net",
    "https://nitter.1d4.us",
    "https://nitter.cz",
    "https://nitter.nl",
]

# ─── Cache helpers ────────────────────────────────────────────────────────────

CACHE_TTL_MINUTES = 30


def _cache_path(platform: str, keyword: str) -> Path:
    safe_kw = re.sub(r"[^a-zA-Z0-9_-]", "_", keyword)[:40]
    return Path(f"/tmp/scraper_cache_{platform}_{safe_kw}.json")


def _cache_load(platform: str, keyword: str) -> Optional[list]:
    path = _cache_path(platform, keyword)
    if not path.exists():
        return None
    try:
        with open(path) as f:
            data = json.load(f)
        cached_at = datetime.fromisoformat(data["cached_at"])
        if (datetime.now() - cached_at).total_seconds() < CACHE_TTL_MINUTES * 60:
            log.debug(f"Cache hit: {platform}/{keyword}")
            return data["results"]
    except Exception:
        pass
    return None


def _cache_save(platform: str, keyword: str, results: list):
    path = _cache_path(platform, keyword)
    try:
        with open(path, "w") as f:
            json.dump({"cached_at": datetime.now().isoformat(), "results": results}, f)
    except Exception as e:
        log.warning(f"Cache write failed: {e}")


# ─── Request helpers ──────────────────────────────────────────────────────────

def _make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
    })
    return s


def _get_with_retry(
    session: requests.Session,
    url: str,
    *,
    max_retries: int = 3,
    timeout: int = 15,
    extra_headers: dict = None,
) -> Optional[requests.Response]:
    """GET with exponential backoff on 429/503."""
    headers = extra_headers or {}
    for attempt in range(max_retries):
        try:
            resp = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
            if resp.status_code in (429, 503, 502):
                wait = (2 ** attempt) * 5 + random.uniform(1, 3)
                log.warning(f"Rate limited ({resp.status_code}) on {url}, retrying in {wait:.1f}s...")
                time.sleep(wait)
                # Rotate UA on retry
                session.headers["User-Agent"] = random.choice(USER_AGENTS)
                continue
            return resp
        except requests.RequestException as e:
            log.warning(f"Request error ({attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None


def _human_delay(min_s: float = 2.0, max_s: float = 8.0):
    """Random human-like delay between requests."""
    delay = random.uniform(min_s, max_s)
    time.sleep(delay)


def _parse_count(text: str) -> int:
    """Parse '1.2K', '3.4M', '500' → int."""
    if not text:
        return 0
    text = text.strip().replace(",", "")
    try:
        if text.endswith("K") or text.endswith("k"):
            return int(float(text[:-1]) * 1000)
        if text.endswith("M") or text.endswith("m"):
            return int(float(text[:-1]) * 1_000_000)
        return int(float(text))
    except (ValueError, TypeError):
        return 0


def _post_id(platform: str, url: str, text: str = "") -> str:
    raw = f"{platform}:{url}:{text[:40]}"
    return hashlib.md5(raw.encode()).hexdigest()[:16]


# ─── Twitter/X via Nitter ─────────────────────────────────────────────────────

def _scrape_twitter(keyword: str, limit: int = 20) -> list[dict]:
    """Scrape tweets from Nitter instances."""
    cached = _cache_load("twitter", keyword)
    if cached is not None:
        return cached[:limit]

    session = _make_session()
    session.headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"

    results = []
    for base_url in NITTER_INSTANCES:
        try:
            search_url = f"{base_url}/search?q={quote_plus(keyword)}&f=tweets"
            log.info(f"[Twitter] Trying {base_url}...")
            resp = _get_with_retry(session, search_url, timeout=12)
            if resp is None or resp.status_code != 200:
                log.warning(f"[Twitter] {base_url} returned {getattr(resp, 'status_code', 'no response')}")
                continue

            soup = BeautifulSoup(resp.text, "lxml")

            # Nitter timeline items
            items = soup.select(".timeline-item") or soup.select(".tweet-body")
            if not items:
                log.warning(f"[Twitter] No timeline items found on {base_url}")
                continue

            for item in items[:limit]:
                try:
                    # Text
                    content_el = item.select_one(".tweet-content") or item.select_one(".tweet-text")
                    text = content_el.get_text(" ", strip=True) if content_el else ""

                    # Author
                    author_el = item.select_one(".username") or item.select_one(".tweet-header .username")
                    author = author_el.get_text(strip=True) if author_el else "unknown"
                    author = author.lstrip("@")

                    # Stats
                    likes = _parse_count(
                        (item.select_one(".icon-heart + span") or item.select_one(".like-count") or
                         item.select_one("[title='Likes']")).get_text(strip=True)
                        if item.select_one(".icon-heart + span") or item.select_one(".like-count") else "0"
                    )
                    retweets = _parse_count(
                        (item.select_one(".icon-retweet + span") or item.select_one(".retweet-count") or
                         item.select_one("[title='Retweets']")).get_text(strip=True)
                        if item.select_one(".icon-retweet + span") or item.select_one(".retweet-count") else "0"
                    )

                    # Timestamp
                    time_el = item.select_one(".tweet-date a") or item.select_one("time")
                    timestamp = ""
                    tweet_url = ""
                    if time_el:
                        timestamp = time_el.get("title") or time_el.get("datetime") or ""
                        href = time_el.get("href", "")
                        tweet_url = f"{base_url}{href}" if href.startswith("/") else href

                    if not text:
                        continue

                    results.append({
                        "id": _post_id("twitter", tweet_url, text),
                        "text": text,
                        "author": author,
                        "author_id": author,
                        "author_handle": f"@{author}",
                        "likes": likes,
                        "retweets": retweets,
                        "comments": 0,
                        "shares": retweets,
                        "timestamp": timestamp,
                        "url": tweet_url,
                        "platform": "twitter",
                        "content": text,  # alias for compatibility
                        "created_at": timestamp or datetime.now().isoformat(),
                    })
                except Exception as e:
                    log.debug(f"[Twitter] Parse error on item: {e}")
                    continue

            if results:
                log.info(f"[Twitter] Scraped {len(results)} tweets from {base_url}")
                break  # Success — stop trying other instances

            _human_delay(1, 3)

        except Exception as e:
            log.warning(f"[Twitter] Error with {base_url}: {e}")
            continue

    if results:
        _cache_save("twitter", keyword, results)
    else:
        log.warning(f"[Twitter] All Nitter instances failed for '{keyword}' — returning empty")

    return results[:limit]


# ─── TikTok ───────────────────────────────────────────────────────────────────

def _scrape_tiktok(keyword: str, limit: int = 20) -> list[dict]:
    """Scrape TikTok search results (best-effort, heavy JS site)."""
    cached = _cache_load("tiktok", keyword)
    if cached is not None:
        return cached[:limit]

    session = _make_session()
    # TikTok-specific headers
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.tiktok.com/",
        "sec-ch-ua": '"Google Chrome";v="124", "Chromium";v="124", "Not-A.Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
    })

    results = []
    urls_to_try = [
        f"https://www.tiktok.com/search?q={quote_plus(keyword)}",
        f"https://www.tiktok.com/tag/{quote_plus(keyword.replace(' ', ''))}",
    ]

    for url in urls_to_try:
        try:
            log.info(f"[TikTok] Scraping {url}...")
            resp = _get_with_retry(session, url, timeout=15)
            if resp is None or resp.status_code != 200:
                continue

            html = resp.text

            # Try to extract from embedded JSON (__UNIVERSAL_DATA_FOR_REHYDRATION__ or SIGI_STATE)
            json_patterns = [
                r'<script id="__UNIVERSAL_DATA_FOR_REHYDRATION__"[^>]*>(.*?)</script>',
                r'window\[\'SIGI_STATE\'\]\s*=\s*(\{.*?\});',
                r'<script>window\.__INIT_PROPS__\s*=\s*(.*?)</script>',
            ]

            data = None
            for pattern in json_patterns:
                m = re.search(pattern, html, re.DOTALL)
                if m:
                    try:
                        data = json.loads(m.group(1))
                        break
                    except json.JSONDecodeError:
                        continue

            if data:
                # Flatten video items from whatever path we can find
                def find_videos(obj, depth=0):
                    if depth > 8 or not isinstance(obj, (dict, list)):
                        return []
                    videos = []
                    if isinstance(obj, list):
                        for item in obj:
                            videos.extend(find_videos(item, depth + 1))
                    elif isinstance(obj, dict):
                        # TikTok stores video info with various key names
                        if any(k in obj for k in ("videoId", "id", "aweme_id")):
                            stats = obj.get("stats", obj.get("statsV2", {}))
                            desc = obj.get("desc", obj.get("description", obj.get("caption", "")))
                            author = obj.get("author", {})
                            if isinstance(author, dict):
                                author_name = author.get("uniqueId", author.get("nickname", "unknown"))
                            else:
                                author_name = str(author)
                            vid_id = str(obj.get("videoId", obj.get("id", obj.get("aweme_id", ""))))
                            vid_url = f"https://www.tiktok.com/@{author_name}/video/{vid_id}"
                            if desc:
                                videos.append({
                                    "id": _post_id("tiktok", vid_url, desc),
                                    "text": desc,
                                    "author": author_name,
                                    "author_id": author_name,
                                    "author_handle": f"@{author_name}",
                                    "likes": _parse_count(str(stats.get("diggCount", stats.get("likeCount", 0)))),
                                    "comments": _parse_count(str(stats.get("commentCount", 0))),
                                    "shares": _parse_count(str(stats.get("shareCount", 0))),
                                    "views": _parse_count(str(stats.get("playCount", stats.get("viewCount", 0)))),
                                    "timestamp": datetime.fromtimestamp(
                                        obj.get("createTime", time.time())
                                    ).isoformat(),
                                    "url": vid_url,
                                    "platform": "tiktok",
                                    "content": desc,
                                    "created_at": datetime.fromtimestamp(
                                        obj.get("createTime", time.time())
                                    ).isoformat(),
                                })
                        else:
                            for v in obj.values():
                                videos.extend(find_videos(v, depth + 1))
                    return videos

                results = find_videos(data)
                if results:
                    log.info(f"[TikTok] Extracted {len(results)} videos from JSON data")
                    break

            # Fallback: parse HTML for video metadata in data-attributes or schema
            soup = BeautifulSoup(html, "lxml")
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    ld = json.loads(script.string or "")
                    if isinstance(ld, list):
                        for item in ld:
                            if item.get("@type") == "VideoObject":
                                text = item.get("description", item.get("name", ""))
                                url_val = item.get("url", item.get("embedUrl", ""))
                                author = item.get("author", {})
                                author_name = (author.get("name", "unknown") if isinstance(author, dict)
                                               else str(author))
                                results.append({
                                    "id": _post_id("tiktok", url_val, text),
                                    "text": text,
                                    "author": author_name,
                                    "author_id": author_name,
                                    "author_handle": f"@{author_name}",
                                    "likes": 0,
                                    "comments": 0,
                                    "shares": 0,
                                    "views": 0,
                                    "timestamp": item.get("uploadDate", datetime.now().isoformat()),
                                    "url": url_val,
                                    "platform": "tiktok",
                                    "content": text,
                                    "created_at": item.get("uploadDate", datetime.now().isoformat()),
                                })
                except Exception:
                    continue

            if results:
                break
            _human_delay(2, 5)

        except Exception as e:
            log.warning(f"[TikTok] Error scraping {url}: {e}")
            continue

    if results:
        _cache_save("tiktok", keyword, results)
    else:
        log.warning(f"[TikTok] Could not scrape TikTok for '{keyword}' (heavy JS — results may be empty)")

    return results[:limit]


# ─── Instagram via Picuki ─────────────────────────────────────────────────────

def _scrape_instagram(keyword: str, limit: int = 20) -> list[dict]:
    """Scrape Instagram posts via Picuki public viewer."""
    cached = _cache_load("instagram", keyword)
    if cached is not None:
        return cached[:limit]

    session = _make_session()
    session.headers["Referer"] = "https://www.picuki.com/"

    hashtag = keyword.lstrip("#").replace(" ", "").lower()
    urls_to_try = [
        f"https://www.picuki.com/tag/{quote_plus(hashtag)}",
    ]

    results = []
    for url in urls_to_try:
        try:
            log.info(f"[Instagram] Scraping {url}...")
            resp = _get_with_retry(session, url, timeout=15)
            if resp is None or resp.status_code != 200:
                log.warning(f"[Instagram] {url} returned {getattr(resp, 'status_code', 'error')}")
                continue

            soup = BeautifulSoup(resp.text, "lxml")

            # Picuki uses .box-photo or .item-photo divs
            items = (soup.select(".box-photo") or soup.select(".item-photo")
                     or soup.select("article") or soup.select(".photo-description"))

            for item in items[:limit]:
                try:
                    # Caption / description
                    caption_el = (item.select_one(".photo-description") or
                                  item.select_one(".caption") or
                                  item.select_one("p"))
                    text = caption_el.get_text(" ", strip=True) if caption_el else ""

                    # Post URL
                    link_el = item.select_one("a[href]")
                    post_url = ""
                    if link_el:
                        href = link_el.get("href", "")
                        post_url = href if href.startswith("http") else f"https://www.picuki.com{href}"

                    # Author
                    author_el = (item.select_one(".owner-info .username") or
                                 item.select_one(".user") or
                                 item.select_one(".username"))
                    author = author_el.get_text(strip=True).lstrip("@") if author_el else "unknown"

                    # Counts
                    likes_el = (item.select_one(".likes") or item.select_one("[class*='like']"))
                    comments_el = (item.select_one(".comments") or item.select_one("[class*='comment']"))
                    likes = _parse_count(likes_el.get_text(strip=True) if likes_el else "0")
                    comments = _parse_count(comments_el.get_text(strip=True) if comments_el else "0")

                    # Timestamp
                    time_el = item.select_one("time") or item.select_one(".time")
                    timestamp = ""
                    if time_el:
                        timestamp = time_el.get("datetime", time_el.get_text(strip=True))

                    results.append({
                        "id": _post_id("instagram", post_url, text),
                        "text": text,
                        "author": author,
                        "author_id": author,
                        "author_handle": f"@{author}",
                        "likes": likes,
                        "comments": comments,
                        "shares": 0,
                        "timestamp": timestamp or datetime.now().isoformat(),
                        "url": post_url,
                        "platform": "instagram",
                        "content": text,
                        "created_at": timestamp or datetime.now().isoformat(),
                    })
                except Exception as e:
                    log.debug(f"[Instagram] Parse error: {e}")
                    continue

            if results:
                log.info(f"[Instagram] Scraped {len(results)} posts")
                break
            _human_delay(2, 5)

        except Exception as e:
            log.warning(f"[Instagram] Error scraping {url}: {e}")
            continue

    if results:
        _cache_save("instagram", keyword, results)
    else:
        log.warning(f"[Instagram] Could not scrape Instagram for '{keyword}'")

    return results[:limit]


# ─── YouTube ──────────────────────────────────────────────────────────────────

def _scrape_youtube(keyword: str, limit: int = 20) -> list[dict]:
    """Scrape YouTube search via ytInitialData embedded JSON."""
    cached = _cache_load("youtube", keyword)
    if cached is not None:
        return cached[:limit]

    session = _make_session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    })

    url = f"https://www.youtube.com/results?search_query={quote_plus(keyword)}&hl=en"
    results = []

    try:
        log.info(f"[YouTube] Scraping: {url}")
        resp = _get_with_retry(session, url, timeout=15)
        if resp is None or resp.status_code != 200:
            log.warning(f"[YouTube] Request failed: {getattr(resp, 'status_code', 'no response')}")
            return results

        html = resp.text

        # Extract ytInitialData JSON
        m = re.search(r"var ytInitialData\s*=\s*(\{.*?\});\s*</script>", html, re.DOTALL)
        if not m:
            m = re.search(r"ytInitialData\s*=\s*(\{.*?\});", html, re.DOTALL)
        if not m:
            log.warning("[YouTube] Could not find ytInitialData in page")
            return results

        data = json.loads(m.group(1))

        # Navigate to video results
        def extract_videos(obj, depth=0):
            if depth > 12 or not isinstance(obj, (dict, list)):
                return []
            videos = []
            if isinstance(obj, list):
                for item in obj:
                    videos.extend(extract_videos(item, depth + 1))
            elif isinstance(obj, dict):
                if "videoRenderer" in obj:
                    vr = obj["videoRenderer"]
                    title_runs = vr.get("title", {}).get("runs", [])
                    title = " ".join(r.get("text", "") for r in title_runs)
                    vid_id = vr.get("videoId", "")
                    vid_url = f"https://www.youtube.com/watch?v={vid_id}" if vid_id else ""
                    channel_runs = vr.get("longBylineText", vr.get("shortBylineText", {})).get("runs", [])
                    channel = " ".join(r.get("text", "") for r in channel_runs)
                    view_count_txt = (vr.get("viewCountText", {}).get("simpleText", "") or
                                      vr.get("shortViewCountText", {}).get("simpleText", ""))
                    published = (vr.get("publishedTimeText", {}).get("simpleText", "") or
                                 vr.get("videoInfo", {}).get("runs", [{}])[0].get("text", ""))
                    desc_runs = vr.get("descriptionSnippet", {}).get("runs", [])
                    description = " ".join(r.get("text", "") for r in desc_runs)

                    if title:
                        videos.append({
                            "id": _post_id("youtube", vid_url, title),
                            "text": title,
                            "author": channel,
                            "author_id": channel,
                            "author_handle": channel,
                            "views": _parse_count(re.sub(r"[^0-9KMB.]", "", view_count_txt)),
                            "likes": 0,
                            "comments": 0,
                            "timestamp": published,
                            "url": vid_url,
                            "platform": "youtube",
                            "content": description or title,
                            "created_at": datetime.now().isoformat(),
                            "description": description,
                            "view_count_text": view_count_txt,
                            "published_text": published,
                        })
                else:
                    for v in obj.values():
                        videos.extend(extract_videos(v, depth + 1))
            return videos

        results = extract_videos(data)
        log.info(f"[YouTube] Extracted {len(results)} videos")

    except Exception as e:
        log.warning(f"[YouTube] Error: {e}")

    if results:
        _cache_save("youtube", keyword, results)

    return results[:limit]


# ─── Trending helpers ─────────────────────────────────────────────────────────

_TRENDING_KEYWORDS = {
    "general": ["viral", "trending", "fyp"],
    "tech": ["AI", "ChatGPT", "coding", "tech news"],
    "business": ["entrepreneur", "startup", "solopreneur", "make money"],
    "fitness": ["workout", "gym", "fitness tips", "weight loss"],
    "food": ["recipe", "cooking", "foodie", "eats"],
    "fashion": ["fashion", "style", "ootd", "streetwear"],
    "gaming": ["gaming", "stream", "twitch", "esports"],
    "crypto": ["crypto", "bitcoin", "defi", "web3"],
}


def _get_trending_tiktok(category: str = "general", limit: int = 20) -> list[dict]:
    keywords = _TRENDING_KEYWORDS.get(category, _TRENDING_KEYWORDS["general"])
    all_results = []
    for kw in keywords:
        results = _scrape_tiktok(kw, limit=max(5, limit // len(keywords)))
        all_results.extend(results)
        if all_results:
            _human_delay(1, 3)
    return all_results[:limit]


def _get_trending_twitter(category: str = "general", limit: int = 20) -> list[dict]:
    keywords = _TRENDING_KEYWORDS.get(category, _TRENDING_KEYWORDS["general"])
    all_results = []
    for kw in keywords:
        results = _scrape_twitter(kw, limit=max(5, limit // len(keywords)))
        all_results.extend(results)
        if all_results:
            _human_delay(1, 3)
    return all_results[:limit]


def _get_trending_instagram(category: str = "general", limit: int = 20) -> list[dict]:
    keywords = _TRENDING_KEYWORDS.get(category, _TRENDING_KEYWORDS["general"])
    all_results = []
    for kw in keywords:
        results = _scrape_instagram(kw, limit=max(5, limit // len(keywords)))
        all_results.extend(results)
        if all_results:
            _human_delay(1, 3)
    return all_results[:limit]


def _get_trending_youtube(category: str = "general", limit: int = 20) -> list[dict]:
    keywords = _TRENDING_KEYWORDS.get(category, _TRENDING_KEYWORDS["general"])
    all_results = []
    for kw in keywords:
        results = _scrape_youtube(kw, limit=max(5, limit // len(keywords)))
        all_results.extend(results)
        if all_results:
            _human_delay(1, 3)
    return all_results[:limit]


# ─── Main SocialScraper class ─────────────────────────────────────────────────

class SocialScraper:
    """
    Scrape social posts without API keys.

    Usage:
        scraper = SocialScraper()
        posts = scraper.search("productivity", platform="twitter", limit=20)
        trending = scraper.get_trending(platform="tiktok", category="tech")
    """

    PLATFORM_SCRAPERS = {
        "twitter": _scrape_twitter,
        "x": _scrape_twitter,
        "tiktok": _scrape_tiktok,
        "instagram": _scrape_instagram,
        "youtube": _scrape_youtube,
    }

    TRENDING_SCRAPERS = {
        "twitter": _get_trending_twitter,
        "x": _get_trending_twitter,
        "tiktok": _get_trending_tiktok,
        "instagram": _get_trending_instagram,
        "youtube": _get_trending_youtube,
    }

    def search(self, keyword: str, platform: str = "all", limit: int = 20) -> list[dict]:
        """
        Search for posts matching `keyword` on one or all platforms.

        Args:
            keyword:  Search term or hashtag
            platform: One of twitter/tiktok/instagram/youtube/all
            limit:    Max results per platform (or total if platform="all")

        Returns:
            List of post dicts with normalized fields.
        """
        platforms = (
            list(self.PLATFORM_SCRAPERS.keys())
            if platform.lower() == "all"
            else [platform.lower()]
        )
        # Deduplicate (x == twitter)
        seen = set()
        unique_platforms = []
        for p in platforms:
            canonical = "twitter" if p == "x" else p
            if canonical not in seen:
                seen.add(canonical)
                unique_platforms.append(p)

        all_results = []
        per_platform = max(5, limit // len(unique_platforms)) if platform == "all" else limit

        for plat in unique_platforms:
            scraper_fn = self.PLATFORM_SCRAPERS.get(plat)
            if not scraper_fn:
                log.warning(f"Unknown platform: {plat}")
                continue
            try:
                log.info(f"[SocialScraper] Searching '{keyword}' on {plat}...")
                results = scraper_fn(keyword, per_platform)
                all_results.extend(results)
                if plat != unique_platforms[-1]:
                    _human_delay(2, 6)
            except Exception as e:
                log.error(f"[SocialScraper] Platform {plat} failed: {e}")
                continue

        return all_results[:limit]

    def get_trending(self, platform: str = "tiktok", category: str = "general", limit: int = 20) -> list[dict]:
        """
        Get trending posts for a platform and category.

        Args:
            platform: twitter/tiktok/instagram/youtube
            category: general/tech/business/fitness/food/fashion/gaming/crypto
            limit:    Max results

        Returns:
            List of post dicts sorted by engagement.
        """
        trending_fn = self.TRENDING_SCRAPERS.get(platform.lower())
        if not trending_fn:
            log.warning(f"[SocialScraper] No trending scraper for {platform}")
            return []

        try:
            results = trending_fn(category=category, limit=limit)
            # Sort by likes desc
            results.sort(key=lambda p: p.get("likes", 0) + p.get("views", 0), reverse=True)
            return results[:limit]
        except Exception as e:
            log.error(f"[SocialScraper] get_trending failed for {platform}: {e}")
            return []


# ─── CLI test mode ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    parser = argparse.ArgumentParser(description="SocialScraper CLI")
    parser.add_argument("--search", help="Search keyword")
    parser.add_argument("--trending", action="store_true")
    parser.add_argument("--platform", default="twitter")
    parser.add_argument("--category", default="general")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()

    scraper = SocialScraper()
    if args.trending:
        results = scraper.get_trending(platform=args.platform, category=args.category, limit=args.limit)
    else:
        results = scraper.search(args.search or "python", platform=args.platform, limit=args.limit)

    print(json.dumps(results, indent=2, default=str))
