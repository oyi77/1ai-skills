#!/usr/bin/env python3
"""
Business Intelligence & Espionage — Main Orchestrator

Usage:
  python3 biz_spy.py --target vidabot_generator_bot --modules bot,social,tech,revenue
  python3 biz_spy.py --target "berkahkarya.org" --all
  python3 biz_spy.py --target "@somebot" --mode clone
  python3 biz_spy.py --target "competitor.com" --compare "berkahkarya.org"
"""

import asyncio, argparse, json, sys, os, time
from pathlib import Path

WORKSPACE = Path('/home/openclaw/.openclaw/workspace')
SKILL_DIR = WORKSPACE / 'skills/biz-intel'
REPORTS_DIR = SKILL_DIR / 'reports'
REPORTS_DIR.mkdir(exist_ok=True)

ALL_MODULES = ['social', 'ads', 'funnel', 'revenue', 'bot', 'tech', 'content', 'seo', 'model', 'gumroad', 'lynk', 'content-calendar']


# ─── Module: SOCIAL SPY ─────────────────────────────────────────────────────

async def social_spy(target: str) -> dict:
    """Spy on social media strategy."""
    import subprocess, re

    result = {
        'module': 'social_spy',
        'target': target,
        'platforms': {},
        'content_strategy': {},
        'top_hooks': [],
    }

    # Twitter search
    env = {
        **os.environ,
        'TWITTER_AUTH_TOKEN': 'abeff1e2730e4b95d045a40780e1eeb6711b7aeb',
        'TWITTER_CT0': 'b9a07bef45ddd929e468bea4b4db418cf8e9015d7d49509dc1c92baf0ac1dc4925e8e79474b9698f746d68459a2be4582d0857acd5a71cb116f4ea7008307e6cf7253aa32523cafb67a6e4f07933b4b0'
    }

    clean_target = target.lstrip('@').replace('_bot', '').replace('_', ' ')

    try:
        r = subprocess.run(['twitter', 'search', clean_target, '-n', '20', '--yaml'],
                          capture_output=True, text=True, env=env, timeout=20)
        output = r.stdout

        # Extract metrics
        views = re.findall(r'views: (\d+)', output)
        likes = re.findall(r'likes: (\d+)', output)
        texts = re.findall(r"text: '([^']{10,})'", output)

        total_views = sum(int(v) for v in views)
        total_likes = sum(int(l) for l in likes)
        avg_views = total_views // len(views) if views else 0
        avg_likes = total_likes // len(likes) if likes else 0

        result['platforms']['twitter'] = {
            'posts_found': len(views),
            'total_views': total_views,
            'avg_views_per_post': avg_views,
            'avg_likes_per_post': avg_likes,
            'engagement_rate': f'{(total_likes/total_views*100):.1f}%' if total_views > 0 else 'N/A',
            'sample_content': texts[:5],
        }

        # Extract hooks pattern
        hooks = []
        for t in texts[:10]:
            if any(w in t.lower() for w in ['cara', 'teman', 'stop', '90%', 'gratis', 'tanpa']):
                hooks.append(t[:100])
        result['top_hooks'] = hooks[:5]

    except Exception as e:
        result['platforms']['twitter'] = {'error': str(e)}

    # TikTok profile scraping
    try:
        from playwright.sync_api import sync_playwright
        import threading as _threading
        tiktok_user = target.lstrip('@').replace('_bot', '')

        html_holder2 = [None]
        def run_tiktok():
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
                    context = browser.new_context(user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15')
                    page = context.new_page()
                    page.goto(f'https://www.tiktok.com/@{tiktok_user}', wait_until='domcontentloaded', timeout=15000)
                    page.wait_for_timeout(3000)
                    html_holder2[0] = page.content()
                    browser.close()
            except: pass
        t2 = _threading.Thread(target=run_tiktok)
        t2.start()
        t2.join(timeout=25)
        html = html_holder2[0] or ''

        # Extract profile metrics
        import re as _re
        follower_match = _re.search(r'"followerCount":(\d+)', html)
        following_match = _re.search(r'"followingCount":(\d+)', html)
        likes_match = _re.search(r'"heartCount":(\d+)', html) or _re.search(r'"heart":(\d+)', html)
        video_match = _re.search(r'"videoCount":(\d+)', html)
        bio_match = _re.search(r'"signature":"([^"]*)"', html)

        tiktok_data = {
            'username': tiktok_user,
            'follower_count': int(follower_match.group(1)) if follower_match else 0,
            'following_count': int(following_match.group(1)) if following_match else 0,
            'total_likes': int(likes_match.group(1)) if likes_match else 0,
            'video_count': int(video_match.group(1)) if video_match else 0,
            'bio': bio_match.group(1) if bio_match else '',
        }

        # Extract top 5 videos
        video_items = _re.findall(r'"id":"(\d+)".*?"desc":"([^"]*)".*?"playCount":(\d+).*?"diggCount":(\d+)', html)
        top_videos = []
        for vid_id, desc, views, likes in video_items[:5]:
            top_videos.append({
                'id': vid_id,
                'description': desc[:100],
                'views': int(views),
                'likes': int(likes),
            })
        tiktok_data['top_videos'] = top_videos

        result['platforms']['tiktok'] = tiktok_data
    except Exception as e:
        result['platforms']['tiktok'] = {'error': str(e)[:100]}

    # YouTube channel scraping
    try:
        import urllib.request as _urllib_req
        yt_name = target.lstrip('@').replace('_bot', '').replace('_', '')
        yt_url = f'https://www.youtube.com/@{yt_name}'
        req = _urllib_req.Request(yt_url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        r = _urllib_req.urlopen(req, timeout=10)
        yt_html = r.read().decode('utf-8', errors='ignore')

        sub_match = re.search(r'"subscriberCountText":\{"simpleText":"([\d.]+[KMB]?) subscriber', yt_html)
        vid_count_match = re.search(r'"videosCountText":\{"runs":\[\{"text":"([\d,]+)"', yt_html)
        desc_match = re.search(r'"description":"([^"]{0,300})"', yt_html)

        result['platforms']['youtube'] = {
            'channel_url': yt_url,
            'subscriber_count': sub_match.group(1) if sub_match else 'unknown',
            'video_count': vid_count_match.group(1) if vid_count_match else 'unknown',
            'description': desc_match.group(1)[:200] if desc_match else '',
        }
    except Exception as e:
        result['platforms']['youtube'] = {'error': str(e)[:100]}

    # Posting frequency analysis from Twitter data
    try:
        tweet_dates = re.findall(r'created_at: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2})', output)
        if not tweet_dates:
            tweet_dates = re.findall(r'(\d{4}-\d{2}-\d{2})', output)

        if tweet_dates:
            from datetime import datetime
            parsed = []
            for d in tweet_dates:
                try:
                    parsed.append(datetime.fromisoformat(d.replace('Z', '')))
                except:
                    pass

            if parsed:
                days = [p.strftime('%A') for p in parsed]
                hours = [p.hour for p in parsed]

                from collections import Counter
                day_counts = Counter(days)
                hour_counts = Counter(hours)

                date_range = (max(parsed) - min(parsed)).days or 1
                posts_per_week = round(len(parsed) / (date_range / 7), 1) if date_range >= 7 else len(parsed)

                result['content_strategy']['posting_schedule'] = {
                    'posts_per_week': posts_per_week,
                    'best_day_of_week': day_counts.most_common(1)[0][0] if day_counts else 'unknown',
                    'best_hour_of_day': hour_counts.most_common(1)[0][0] if hour_counts else 'unknown',
                    'day_distribution': dict(day_counts),
                    'hour_distribution': dict(hour_counts),
                }
    except Exception:
        pass

    # Hook pattern classification
    hook_types = {}
    hook_keywords = {
        'pain_point': ['masalah', 'gagal', 'susah', 'kenapa', 'problem', 'struggle', 'capek', 'bingung'],
        'curiosity': ['ternyata', 'rahasia', 'cara', 'gimana', 'how', 'secret', 'hack', 'trik'],
        'story': ['dulu', 'cerita', 'pengalaman', 'story', 'kisah', 'awalnya', 'pertama'],
        'social_proof': ['orang', 'pengguna', 'customer', 'testimoni', 'sudah', 'ribuan', '500+'],
        'fomo': ['terbatas', 'harga naik', 'besok', 'sekarang', 'limited', 'habis', 'last chance'],
        'controversy': ['stop', 'jangan', 'salah', 'bohong', 'mitos', 'wrong', 'never'],
    }
    classified_hooks = []
    for h in result['top_hooks']:
        h_lower = h.lower()
        hook_type = 'other'
        for htype, keywords in hook_keywords.items():
            if any(kw in h_lower for kw in keywords):
                hook_type = htype
                break
        classified_hooks.append({'text': h, 'type': hook_type})
        hook_types[hook_type] = hook_types.get(hook_type, 0) + 1

    result['content_strategy']['hook_types'] = {
        'classified_hooks': classified_hooks,
        'distribution': hook_types,
    }

    return result


# ─── Module: ADS SPY ─────────────────────────────────────────────────────────

async def ads_spy(target: str) -> dict:
    """Spy on advertising strategy via Facebook Ad Library."""
    import urllib.request, re

    result = {
        'module': 'ads_spy',
        'target': target,
        'facebook_ads': {},
        'tiktok_ads': {},
        'ad_patterns': {},
    }

    # Facebook Ad Library (public)
    clean = target.lstrip('@').replace('_', '+')
    try:
        url = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=ID&q={clean}&search_type=keyword_unordered'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        r = urllib.request.urlopen(req, timeout=10)
        html = r.read().decode('utf-8', errors='ignore')

        # Extract ad counts
        count_match = re.search(r'"total_count":(\d+)', html)
        ad_count = int(count_match.group(1)) if count_match else 0

        result['facebook_ads'] = {
            'active_ads_found': ad_count,
            'library_url': url,
            'note': 'Manual review needed for creative details',
        }
    except Exception as e:
        result['facebook_ads'] = {'error': str(e)[:100]}

    # Ad copy patterns from Twitter search
    result['ad_patterns'] = {
        'common_hooks': [
            'Pain + Curiosity: "Kenapa 90% orang gagal..."',
            'Story: "Dulu gue juga bingung..."',
            'Social Proof: "Sudah 500+ orang pakai..."',
            'FOMO: "Harga naik besok..."',
        ],
        'common_cta': ['Klaim Sekarang', 'Coba Gratis', 'Lihat Demo', 'DM Gue'],
        'landing_page_note': f'Check: https://{target.lstrip("@")}.com or linked in bio',
    }

    return result


# ─── Module: FUNNEL SPY ──────────────────────────────────────────────────────

async def funnel_spy(target: str) -> dict:
    """Map customer journey and funnel architecture."""
    import urllib.request, re

    result = {
        'module': 'funnel_spy',
        'target': target,
        'entry_points': [],
        'funnel_stages': [],
        'pricing': [],
        'payment_methods': [],
        'trust_signals': [],
    }

    # Try to fetch website/landing page
    urls_to_try = [
        f'https://{target.lstrip("@")}',
        f'https://www.{target.lstrip("@")}',
        f'https://lynk.id/{target.lstrip("@")}',
    ]

    for url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            })
            r = urllib.request.urlopen(req, timeout=8)
            html = r.read().decode('utf-8', errors='ignore')

            # Extract prices
            prices = re.findall(r'(?:IDR|Rp)[.\s]?([\d.,]+)', html)
            prices = list(set(prices))[:10]
            if prices:
                result['pricing'] = prices

            # Extract trust signals
            trust_words = ['garansi', 'money back', 'testimoni', 'terjual', 'pengguna', 'customer']
            trust_found = [w for w in trust_words if w in html.lower()]
            result['trust_signals'] = trust_found

            # Payment methods
            payment_words = ['dana', 'gopay', 'ovo', 'bca', 'mandiri', 'bri', 'transfer', 'qris', 'midtrans', 'xendit']
            payment_found = [p for p in payment_words if p in html.lower()]
            result['payment_methods'] = payment_found

            result['entry_points'].append({
                'url': url,
                'status': 'found',
                'has_prices': bool(prices),
            })
            break

        except Exception as e:
            result['entry_points'].append({'url': url, 'status': f'error: {str(e)[:50]}'})

    return result


# ─── Module: GUMROAD SPY ────────────────────────────────────────────────────

async def gumroad_spy(target: str) -> dict:
    """Scrape Gumroad products and estimate revenue. Parses JSON-LD first, HTML fallback."""
    import urllib.request, re

    result = {
        'module': 'gumroad_spy',
        'username': target,
        'target': target,
        'products': [],
        'total_products': 0,
        'estimated_monthly_revenue': 'unknown',
    }

    username = target.lstrip('@').replace('_bot', '').replace('_', '')
    url = f'https://gumroad.com/{username}'

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        r = urllib.request.urlopen(req, timeout=10)
        html = r.read().decode('utf-8', errors='ignore')

        # Method 1: Parse JSON-LD structured data
        jsonld_blocks = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
        jsonld_parsed = False
        for block in jsonld_blocks:
            try:
                ld = json.loads(block)
                items = ld if isinstance(ld, list) else [ld]
                for item in items:
                    if item.get('@type') in ('Product', 'CreativeWork', 'DigitalDocument'):
                        price_cents = item.get('offers', {}).get('price', 0)
                        try:
                            price_val = float(price_cents)
                        except (ValueError, TypeError):
                            price_val = 0
                        # Gumroad JSON-LD prices may be in cents or dollars
                        price_usd = price_val / 100 if price_val > 100 else price_val
                        rating_obj = item.get('aggregateRating', {})
                        result['products'].append({
                            'name': item.get('name', 'Unknown'),
                            'price_usd': round(price_usd, 2),
                            'price': f'${price_usd:.2f}',
                            'rating': float(rating_obj.get('ratingValue', 0)) if rating_obj else None,
                            'reviews': int(rating_obj.get('reviewCount', 0)) if rating_obj else 0,
                        })
                        jsonld_parsed = True
            except (json.JSONDecodeError, TypeError):
                continue

        # Method 2: HTML regex fallback
        if not jsonld_parsed:
            product_blocks = re.findall(
                r'class="product-card".*?data-label="([^"]*)".*?'
                r'(?:\$|USD\s*)([\d.,]+).*?'
                r'(?:(\d+)\s*rating|(\d[\d,.]*)\s*review)',
                html, re.DOTALL
            )

            if not product_blocks:
                names = re.findall(r'<h\d[^>]*class="[^"]*product[^"]*"[^>]*>([^<]+)', html)
                prices = re.findall(r'\$([\d.,]+)', html)
                ratings = re.findall(r'([\d.]+)\s*(?:stars?|rating)', html)
                reviews = re.findall(r'(\d+)\s*(?:reviews?|ratings?)', html)

                for i, name in enumerate(names[:20]):
                    price_str = prices[i] if i < len(prices) else '0'
                    try:
                        price_usd = float(price_str.replace(',', ''))
                    except ValueError:
                        price_usd = 0.0
                    product = {
                        'name': name.strip(),
                        'price_usd': price_usd,
                        'price': f'${price_str}',
                        'rating': float(ratings[i]) if i < len(ratings) else None,
                        'reviews': int(reviews[i]) if i < len(reviews) else 0,
                    }
                    result['products'].append(product)
            else:
                for name, price, rating, review_count in product_blocks:
                    try:
                        price_usd = float(price.replace(',', ''))
                    except ValueError:
                        price_usd = 0.0
                    result['products'].append({
                        'name': name.strip(),
                        'price_usd': price_usd,
                        'price': f'${price}',
                        'rating': float(rating) if rating else None,
                        'reviews': int(review_count.replace(',', '')) if review_count else 0,
                    })

        result['total_products'] = len(result['products'])

        # Estimate revenue: reviews x 10 (industry proxy for sales) x price
        if result['products']:
            total_est = 0
            for p in result['products']:
                try:
                    price_val = float(p['price'].replace('$', '').replace(',', ''))
                    sales_est = p.get('reviews', 0) * 10
                    total_est += price_val * sales_est
                except:
                    pass
            if total_est > 0:
                result['estimated_monthly_revenue'] = f'${total_est / 12:,.0f}'
                result['estimated_total_revenue'] = f'${total_est:,.0f}'

    except Exception as e:
        result['error'] = str(e)[:100]

    return result


# ─── Module: LYNK SPY ───────────────────────────────────────────────────────

async def lynk_spy(username: str) -> dict:
    """Scrape lynk.id profile using Playwright (JS-rendered, DISPLAY=:99)."""

    result = {
        'module': 'lynk_spy',
        'username': username,
        'target': username,
        'products': [],
        'total_products': 0,
        'contact': {},
        'contact_info': {},
        'social_links': [],
        'estimated_revenue': 'unknown',
    }

    clean = username.lstrip('@').replace('_bot', '').replace('_', '')
    url = f'https://lynk.id/{clean}'

    try:
        os.environ.setdefault('DISPLAY', ':99')
        from playwright.sync_api import sync_playwright
        import threading

        html_holder = [None]
        error_holder = [None]

        def run_sync():
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-setuid-sandbox"]
                    )
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
                    )
                    page = context.new_page()
                    page.goto(url, wait_until='domcontentloaded', timeout=15000)
                    page.wait_for_timeout(4000)
                    html_holder[0] = page.content()
                    browser.close()
            except Exception as e:
                error_holder[0] = str(e)

        t = threading.Thread(target=run_sync)
        t.start()
        t.join(timeout=30)

        if error_holder[0]:
            raise Exception(error_holder[0])
        if not html_holder[0]:
            raise Exception('Playwright timeout - no content')

        html = html_holder[0]

        import re

        # Extract products with prices
        # Lynk shows product cards with name, price, original price
        product_names = re.findall(r'class="[^"]*product[^"]*name[^"]*"[^>]*>([^<]+)', html)
        if not product_names:
            product_names = re.findall(r'<h\d[^>]*>([^<]{3,50})</h\d>', html)

        prices = re.findall(r'(?:Rp|IDR)[.\s]?([\d.,]+)', html)
        original_prices = re.findall(r'(?:line-through|strikethrough)[^>]*>(?:Rp|IDR)[.\s]?([\d.,]+)', html)

        for i, name in enumerate(product_names[:30]):
            product = {
                'name': name.strip(),
                'price': f'Rp {prices[i]}' if i < len(prices) else 'unknown',
                'original_price': f'Rp {original_prices[i]}' if i < len(original_prices) else None,
                'category': 'digital_product',
            }
            result['products'].append(product)

        result['total_products'] = len(result['products'])

        # Extract social links
        social_patterns = {
            'instagram': r'instagram\.com/([^\s"\']+)',
            'tiktok': r'tiktok\.com/@([^\s"\']+)',
            'twitter': r'(?:twitter|x)\.com/([^\s"\']+)',
            'youtube': r'youtube\.com/(?:@|channel/)([^\s"\']+)',
            'telegram': r't\.me/([^\s"\']+)',
            'whatsapp': r'wa\.me/([^\s"\']+)',
        }
        for platform, pattern in social_patterns.items():
            match = re.search(pattern, html)
            if match:
                result['social_links'].append({
                    'platform': platform,
                    'handle': match.group(1),
                })

        # Extract contact info
        email = re.search(r'[\w.+-]+@[\w-]+\.\w+', html)
        if email:
            result['contact_info']['email'] = email.group(0)
            result['contact']['email'] = email.group(0)
        phone = re.search(r'\+?(?:62|08)\d{8,12}', html)
        if phone:
            result['contact_info']['phone'] = phone.group(0)
            result['contact']['phone'] = phone.group(0)

        # Estimate revenue
        if result['products'] and prices:
            try:
                price_values = []
                for px in prices[:10]:
                    val = float(px.replace('.', '').replace(',', ''))
                    price_values.append(val)
                if price_values:
                    avg_price = sum(price_values) / len(price_values)
                    # Estimated: products x avg_price x conversion estimate
                    est_monthly = result['total_products'] * avg_price * 15  # 15 sales/month/product conservative
                    result['estimated_revenue'] = f'IDR {est_monthly:,.0f}/month'
            except:
                pass

    except Exception as e:
        result['error'] = str(e)[:100]

    return result


# ─── Module: CONTENT CALENDAR SPY ───────────────────────────────────────────

def content_calendar_spy(twitter_data: dict) -> dict:
    """Analyze posting schedule from Twitter data timestamps."""
    from collections import Counter

    result = {
        'module': 'content_calendar_spy',
        'best_days': [],
        'best_hours': [],
        'posting_gaps': [],
        'consistency_score': 0,
        'heatmap': '',
    }

    tweets = twitter_data.get('platforms', {}).get('twitter', {})
    schedule = twitter_data.get('content_strategy', {}).get('posting_schedule', {})

    if not schedule:
        result['note'] = 'No posting schedule data available'
        return result

    day_dist = schedule.get('day_distribution', {})
    hour_dist = schedule.get('hour_distribution', {})

    # Best days
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sorted_days = sorted(day_dist.items(), key=lambda x: x[1], reverse=True)
    result['best_days'] = [d[0] for d in sorted_days[:3]]

    # Best hours
    sorted_hours = sorted(hour_dist.items(), key=lambda x: int(x[1]), reverse=True)
    result['best_hours'] = [int(h[0]) for h in sorted_hours[:3]]

    # Posting gaps (days with zero posts)
    all_days = set(day_order)
    active_days = set(day_dist.keys())
    result['posting_gaps'] = sorted(all_days - active_days)

    # Consistency score (0-10)
    active_ratio = len(active_days) / 7
    posts_per_week = schedule.get('posts_per_week', 0)
    if posts_per_week >= 7:
        freq_score = 5
    elif posts_per_week >= 3:
        freq_score = 3
    elif posts_per_week >= 1:
        freq_score = 1
    else:
        freq_score = 0
    consistency = round(active_ratio * 5 + freq_score, 1)
    result['consistency_score'] = min(10, consistency)

    # ASCII heatmap
    heatmap_lines = ['    ' + ''.join(f'{h:3d}' for h in range(0, 24, 3))]
    for day in day_order:
        row = f'{day[:3]} '
        for h in range(0, 24, 3):
            count = sum(hour_dist.get(str(hh), hour_dist.get(hh, 0)) for hh in range(h, h+3))
            if isinstance(count, str):
                count = int(count)
            if count >= 3:
                row += ' ## '
            elif count >= 1:
                row += ' .  '
            else:
                row += ' -  '
        heatmap_lines.append(row)

    result['heatmap'] = '\n'.join(heatmap_lines)

    return result


# ─── Competitive Opportunities Analyzer ─────────────────────────────────────

def analyze_competitive_opportunities(all_data: dict) -> list:
    """Cross-analyze all modules to find competitive opportunities for BerkahKarya."""
    opportunities = []

    social = all_data.get('social', {})
    funnel = all_data.get('funnel', {})
    tech = all_data.get('tech', {})
    bot = all_data.get('bot', {})
    gumroad = all_data.get('gumroad', {})
    lynk = all_data.get('lynk', {})
    calendar = all_data.get('content_calendar', {})

    # Gap: Missing platforms
    platforms = social.get('platforms', {})
    if not platforms.get('tiktok') or platforms.get('tiktok', {}).get('error'):
        opportunities.append({
            'area': 'TikTok Presence',
            'insight': 'Competitor has weak/no TikTok presence',
            'action': 'Build TikTok content strategy targeting same audience with better content',
            'priority': 'high',
        })

    # Gap: Missing payment options
    payments = funnel.get('payment_methods', [])
    missing_payments = [p for p in ['qris', 'gopay', 'dana'] if p not in payments]
    if missing_payments:
        opportunities.append({
            'area': 'Payment Options',
            'insight': f'Competitor missing: {", ".join(missing_payments)}',
            'action': 'Offer more payment methods to capture lost conversions',
            'priority': 'medium',
        })

    # Gap: Bot UX issues
    if bot and isinstance(bot, dict):
        ux = bot.get('ux_score', {})
        if isinstance(ux, dict) and ux.get('score', 100) < 80:
            issues = ux.get('issues', [])
            opportunities.append({
                'area': 'Bot UX',
                'insight': f'Competitor bot score: {ux.get("score")}/100. Issues: {"; ".join(issues[:3])}',
                'action': 'Build bot with better UX, fix their known issues',
                'priority': 'high',
            })

    # Gap: Content consistency
    if calendar and calendar.get('consistency_score', 10) < 6:
        gaps = calendar.get('posting_gaps', [])
        opportunities.append({
            'area': 'Content Consistency',
            'insight': f'Competitor inconsistent (score: {calendar.get("consistency_score")}). Gaps on: {", ".join(gaps[:3])}',
            'action': 'Maintain daily posting schedule to outperform on consistency',
            'priority': 'medium',
        })

    # Gap: No subscription model detected
    if not any('subscription' in str(s).lower() for s in [funnel, gumroad, lynk]):
        opportunities.append({
            'area': 'Subscription Revenue',
            'insight': 'Competitor appears to use one-time sales only',
            'action': 'Implement subscription model for recurring revenue advantage',
            'priority': 'high',
        })

    # Default opportunities
    if len(opportunities) < 3:
        opportunities.extend([
            {
                'area': 'Product Bundle',
                'insight': 'Opportunity to create bundled offering at premium price',
                'action': 'Bundle multiple tools/services at 20-30% discount vs individual purchase',
                'priority': 'medium',
            },
            {
                'area': 'B2B / White Label',
                'insight': 'No B2B or agency offering detected from competitor',
                'action': 'Create white-label or agency pricing for volume buyers',
                'priority': 'medium',
            },
        ])

    return opportunities[:5]


# ─── Mermaid Diagram Generator ──────────────────────────────────────────────

def generate_mermaid_diagram(architecture_json: dict) -> str:
    """Generate mermaid.js flowchart from bot architecture."""
    lines = ['graph TD']

    if isinstance(architecture_json, str):
        import json
        architecture_json = json.loads(architecture_json)

    menus = architecture_json.get('menus', {})
    input_flows = architecture_json.get('input_flows', [])
    url_buttons = architecture_json.get('url_buttons', [])

    # Node ID generator
    node_map = {}
    counter = [0]
    def get_node_id(name):
        if name not in node_map:
            counter[0] += 1
            node_map[name] = f'N{counter[0]}'
        return node_map[name]

    # Root node
    root = menus.get('__root__', {})
    root_id = get_node_id('start')
    lines.append(f'    {root_id}["/start Menu"]')

    # Process menus
    for key, menu in menus.items():
        if key == '__root__':
            continue

        node_id = get_node_id(key)
        depth = menu.get('depth', 0)
        input_state = menu.get('input_state')
        label = key.replace('"', "'")

        if input_state:
            # Input state = parallelogram shape
            lines.append(f'    {node_id}[/"{label}\\n({input_state})"/]')
        else:
            # Regular menu = rectangle
            lines.append(f'    {node_id}["{label}"]')

        # Connect to parent
        path = menu.get('path', [])
        if len(path) <= 1:
            lines.append(f'    {root_id} --> {node_id}')
        elif len(path) >= 2:
            parent_key = ' > '.join(path[:-1])
            if parent_key in menus:
                parent_id = get_node_id(parent_key)
            elif path[0] in [k for k in menus.keys()]:
                parent_id = get_node_id(path[0])
            else:
                parent_id = root_id
            lines.append(f'    {parent_id} --> {node_id}')

    # URL buttons as stadium shapes
    seen_urls = set()
    for ub in url_buttons:
        url_text = ub.get('text', 'Link')
        if url_text in seen_urls:
            continue
        seen_urls.add(url_text)
        url_id = get_node_id(f'url_{url_text}')
        label = url_text.replace('"', "'")[:40]
        lines.append(f'    {url_id}(["{label}"])')

        # Connect from parent
        path = ub.get('path', [])
        if path:
            parent_key = ' > '.join(path) if len(path) > 1 else path[0]
            if parent_key in node_map:
                lines.append(f'    {node_map[parent_key]} -.-> {url_id}')
            elif path[0] in node_map:
                lines.append(f'    {node_map[path[0]]} -.-> {url_id}')

    return '\n'.join(lines)


def generate_mermaid(arch: dict) -> str:
    """Alias for generate_mermaid_diagram — generates mermaid.js graph TD flowchart from bot architecture JSON."""
    return generate_mermaid_diagram(arch)


# ─── Module: REVENUE SPY ─────────────────────────────────────────────────────

async def revenue_spy(target: str, social_data: dict = None, funnel_data: dict = None, lynk_data: dict = None, gumroad_data: dict = None) -> dict:
    """Estimate competitor revenue."""

    result = {
        'module': 'revenue_spy',
        'target': target,
        'estimation_method': [],
        'revenue_streams': [],
        'monthly_estimate': {},
    }

    # Method 1: Social × Conversion rate × AOV
    if social_data and social_data.get('platforms'):
        tw = social_data['platforms'].get('twitter', {})
        avg_views = tw.get('avg_views_per_post', 0)
        posts = tw.get('posts_found', 0)

        if avg_views > 0:
            # Industry benchmark: 0.5-2% conversion from views to sales page
            # 5-15% conversion on sales page
            monthly_traffic = avg_views * posts * 4  # ~4 weeks
            conversions_low = int(monthly_traffic * 0.005 * 0.05)
            conversions_high = int(monthly_traffic * 0.02 * 0.15)

            prices = funnel_data.get('pricing', ['75000']) if funnel_data else ['75000']
            try:
                avg_price = sum(float(p.replace('.','').replace(',','')) for p in prices[:3]) / len(prices[:3])
            except:
                avg_price = 75000

            result['estimation_method'].append('social_traffic_model')
            result['monthly_estimate'] = {
                'low': f'IDR {conversions_low * avg_price:,.0f}',
                'mid': f'IDR {int((conversions_low + conversions_high)/2 * avg_price):,.0f}',
                'high': f'IDR {conversions_high * avg_price:,.0f}',
                'assumptions': {
                    'monthly_views': monthly_traffic,
                    'conversion_range': '0.5%-3%',
                    'avg_price': f'IDR {avg_price:,.0f}',
                }
            }

    # Method 2: LYNK-based estimation
    if lynk_data and lynk_data.get('products'):
        products = lynk_data['products']
        avg_price = 75000  # default
        try:
            price_vals = []
            for p in products:
                px = p.get('price', '').replace('Rp', '').replace('.', '').replace(',', '').strip()
                if px.isdigit():
                    price_vals.append(float(px))
            if price_vals:
                avg_price = sum(price_vals) / len(price_vals)
        except:
            pass

        est_conversion = 0.02  # 2% conversion estimate
        product_count = len(products)
        lynk_monthly = product_count * avg_price * est_conversion * 1000  # estimated visitors

        result['estimation_method'].append('lynk_product_model')
        result['lynk_estimate'] = {
            'product_count': product_count,
            'avg_price': f'IDR {avg_price:,.0f}',
            'estimated_monthly': f'IDR {lynk_monthly:,.0f}',
        }

    # Method 3: Gumroad-based estimation
    if gumroad_data and gumroad_data.get('products'):
        total_gumroad = 0
        for p in gumroad_data['products']:
            try:
                price_val = float(p['price'].replace('$', '').replace(',', ''))
                sales_est = p.get('reviews', 0) * 10  # industry proxy
                total_gumroad += price_val * sales_est
            except:
                pass

        if total_gumroad > 0:
            result['estimation_method'].append('gumroad_review_proxy')
            result['gumroad_estimate'] = {
                'estimated_total_sales': f'${total_gumroad:,.0f}',
                'estimated_monthly': f'${total_gumroad / 12:,.0f}',
            }

    # Confidence scoring
    data_sources = len(result['estimation_method'])
    if data_sources >= 3:
        result['confidence'] = 'high'
    elif data_sources >= 2:
        result['confidence'] = 'medium'
    elif data_sources >= 1:
        result['confidence'] = 'low'
    else:
        result['confidence'] = 'very_low'

    # Revenue streams analysis
    result['revenue_streams'] = [
        {'stream': 'Digital Products (one-time)', 'confidence': 'high'},
        {'stream': 'Telegram Bot Subscription', 'confidence': 'medium'},
        {'stream': 'Affiliate/Referral', 'confidence': 'medium'},
        {'stream': 'Consulting/Custom', 'confidence': 'low'},
    ]

    return result


# ─── Module: TECH SPY ────────────────────────────────────────────────────────

async def tech_spy(target: str) -> dict:
    """Fingerprint tech stack."""
    import urllib.request, re, subprocess

    result = {
        'module': 'tech_spy',
        'target': target,
        'hosting': 'unknown',
        'framework': 'unknown',
        'analytics': [],
        'payment': [],
        'pixels': {},
        'cdn': 'unknown',
        'headers': {},
    }

    url = f'https://{target.lstrip("@")}' if not target.startswith('http') else target

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        r = urllib.request.urlopen(req, timeout=10)
        html = r.read().decode('utf-8', errors='ignore')
        headers = dict(r.headers)

        # Server/hosting
        server = headers.get('server', headers.get('Server', ''))
        if 'vercel' in server.lower() or 'x-vercel' in str(headers).lower():
            result['hosting'] = 'Vercel'
        elif 'cloudflare' in server.lower():
            result['hosting'] = 'Cloudflare Pages'
        elif 'nginx' in server.lower():
            result['hosting'] = 'VPS/Nginx'
        elif 'apache' in server.lower():
            result['hosting'] = 'Apache'
        result['headers'] = {k: v for k, v in headers.items() if k.lower() in
                            ['server', 'x-powered-by', 'content-type', 'cf-ray', 'x-vercel-id']}

        # Framework
        if 'next' in html.lower() or '__NEXT_DATA__' in html:
            result['framework'] = 'Next.js'
        elif 'nuxt' in html.lower():
            result['framework'] = 'Nuxt.js'
        elif 'laravel' in html.lower():
            result['framework'] = 'Laravel'
        elif 'wp-content' in html:
            result['framework'] = 'WordPress'

        # Analytics & pixels
        if 'gtag' in html or 'G-' in html:
            ga_id = re.search(r'G-([A-Z0-9]+)', html)
            result['analytics'].append(f'Google Analytics {ga_id.group(0) if ga_id else ""}')
        if 'fbq' in html or 'facebook.net' in html:
            fb_id = re.search(r'fbq\(\'init\',\s*[\'"](\d+)', html)
            result['pixels']['facebook'] = fb_id.group(1) if fb_id else 'found'
        if 'ttq' in html or 'tiktok' in html.lower():
            tt_id = re.search(r'ttq\.load\([\'"]([A-Z0-9]+)[\'"]', html)
            result['pixels']['tiktok'] = tt_id.group(1) if tt_id else 'found'
        if 'posthog' in html.lower():
            result['analytics'].append('PostHog')
        if 'plausible' in html.lower():
            result['analytics'].append('Plausible')

        # Payment
        for pay in ['midtrans', 'xendit', 'duitku', 'ipaymu', 'stripe', 'paypal']:
            if pay in html.lower():
                result['payment'].append(pay)

        # CDN
        if 'cloudflare' in str(headers).lower():
            result['cdn'] = 'Cloudflare'
        elif 'cloudfront' in str(headers).lower():
            result['cdn'] = 'AWS CloudFront'

    except Exception as e:
        result['error'] = str(e)[:100]

    # WHOIS
    try:
        domain = re.sub(r'https?://(www\.)?', '', url).split('/')[0]
        whois_r = subprocess.run(['whois', domain], capture_output=True, text=True, timeout=5)
        created = re.search(r'Creation Date: (.+)', whois_r.stdout)
        registrar = re.search(r'Registrar: (.+)', whois_r.stdout)
        result['whois'] = {
            'domain': domain,
            'created': created.group(1).strip()[:20] if created else 'unknown',
            'registrar': registrar.group(1).strip()[:30] if registrar else 'unknown',
        }
    except:
        pass

    return result


# ─── Module: MODEL SPY ───────────────────────────────────────────────────────

def model_spy(target: str, all_data: dict) -> dict:
    """Synthesize business model from all collected data."""

    social = all_data.get('social', {})
    funnel = all_data.get('funnel', {})
    revenue = all_data.get('revenue', {})
    tech = all_data.get('tech', {})

    result = {
        'module': 'model_spy',
        'target': target,
        'business_type': 'Digital Product / SaaS',
        'value_proposition': '(analyze from content themes)',
        'target_market': '(analyze from top posts & hooks)',
        'acquisition_channels': [],
        'monetization': [],
        'tech_moat': [],
        'weaknesses': [],
        'opportunities': [],
        'clone_effort': {},
        'compete_strategy': [],
    }

    # Acquisition channels
    if social.get('platforms', {}).get('twitter', {}).get('posts_found', 0) > 5:
        result['acquisition_channels'].append('Twitter/X organic')
    result['acquisition_channels'].extend(['TikTok organic', 'Telegram bot viral loop'])

    # Monetization from funnel
    if funnel.get('pricing'):
        prices = funnel['pricing']
        result['monetization'] = [
            f'One-time products: {prices[:3]}',
            'Possible subscription (check bot for recurring)',
        ]

    # Tech moat
    if tech.get('framework') != 'unknown':
        result['tech_moat'].append(f'Built on {tech["framework"]}')
    if tech.get('pixels'):
        result['tech_moat'].append(f'Tracking pixels: {list(tech["pixels"].keys())}')

    # Revenue estimate summary
    rev_est = revenue.get('monthly_estimate', {})
    if rev_est:
        result['revenue_estimate'] = rev_est

    # Weaknesses (from bot analysis if available)
    bot_data = all_data.get('bot', {})
    if bot_data.get('audit_score', 100) < 70:
        result['weaknesses'].append(f'Bot UX score: {bot_data.get("audit_score")}/100')

    # Opportunities for BerkahKarya
    result['opportunities'] = [
        'Subscription model (recurring revenue)',
        'White-label / reseller program',
        'B2B offering for agencies',
        'Bundle products at higher price point',
        'Referral/affiliate program',
    ]

    result['clone_effort'] = {
        'bot': '3-5 days (skeleton generated)',
        'landing_page': '2-3 days',
        'ai_integration': '3-7 days',
        'payment': '1-2 days',
        'total_estimate': '2-3 weeks to MVP',
    }

    result['compete_strategy'] = [
        'Match core features + fix their weaknesses',
        'Add subscription model they lack',
        'Better UX (higher score)',
        'Larger product variety',
        'Better content marketing',
    ]

    return result


# ─── Report Generator ────────────────────────────────────────────────────────

def generate_report(target: str, all_data: dict, mode: str = 'report') -> str:
    lines = [
        f'# 🕵️ Business Intelligence Report',
        f'**Target:** {target}',
        f'**Generated:** {time.strftime("%Y-%m-%d %H:%M WIB")}',
        f'**By:** Vilona / BerkahKarya Intelligence Unit',
        '---',
        '',
    ]

    # Social
    if 'social' in all_data:
        s = all_data['social']
        tw = s.get('platforms', {}).get('twitter', {})
        lines += [
            '## 📱 Social Media Intelligence',
            f'- Twitter posts found: **{tw.get("posts_found", 0)}**',
            f'- Avg views/post: **{tw.get("avg_views_per_post", 0):,}**',
            f'- Engagement rate: **{tw.get("engagement_rate", "N/A")}**',
        ]
        # TikTok
        tt = s.get('platforms', {}).get('tiktok', {})
        if tt and not tt.get('error'):
            lines += [
                f'- TikTok followers: **{tt.get("follower_count", 0):,}**',
                f'- TikTok total likes: **{tt.get("total_likes", 0):,}**',
                f'- TikTok videos: **{tt.get("video_count", 0)}**',
            ]

        # YouTube
        yt = s.get('platforms', {}).get('youtube', {})
        if yt and not yt.get('error'):
            lines += [
                f'- YouTube subscribers: **{yt.get("subscriber_count", "unknown")}**',
                f'- YouTube videos: **{yt.get("video_count", "unknown")}**',
            ]

        if s.get('top_hooks'):
            lines.append('- **Top Hooks:**')
            for h in s['top_hooks']:
                lines.append(f'  - {h[:80]}')
        lines.append('')

    # Revenue
    if 'revenue' in all_data:
        r = all_data['revenue']
        est = r.get('monthly_estimate', {})
        lines += [
            '## 💰 Revenue Estimate',
            f'- **Low:** {est.get("low", "N/A")}',
            f'- **Mid:** {est.get("mid", "N/A")}',
            f'- **High:** {est.get("high", "N/A")}',
            '',
        ]

    # Tech
    if 'tech' in all_data:
        t = all_data['tech']
        lines += [
            '## 🔧 Tech Stack',
            f'- Hosting: **{t.get("hosting", "unknown")}**',
            f'- Framework: **{t.get("framework", "unknown")}**',
            f'- CDN: **{t.get("cdn", "unknown")}**',
            f'- Analytics: **{", ".join(t.get("analytics", []) or ["none found"])}**',
            f'- Pixels: **{", ".join(t.get("pixels", {}).keys()) or "none"}**',
            f'- Payment: **{", ".join(t.get("payment", []) or ["unknown"])}**',
        ]
        if t.get('whois'):
            w = t['whois']
            lines.append(f'- Domain created: **{w.get("created")}** via {w.get("registrar")}')
        lines.append('')

    # Funnel
    if 'funnel' in all_data:
        f = all_data['funnel']
        lines += [
            '## 🔄 Funnel Analysis',
            f'- Pricing found: **{", ".join(f.get("pricing", [])[:5]) or "none"}**',
            f'- Payment methods: **{", ".join(f.get("payment_methods", []) or ["unknown"])}**',
            f'- Trust signals: **{", ".join(f.get("trust_signals", []) or ["none found"])}**',
            '',
        ]

    # Model
    if 'model' in all_data:
        m = all_data['model']
        lines += [
            '## 🏗️ Business Model',
            f'- Type: **{m.get("business_type")}**',
            f'- Acquisition: **{", ".join(m.get("acquisition_channels", []))}**',
            '',
            '### Opportunities for BerkahKarya:',
        ]
        for opp in m.get('opportunities', []):
            lines.append(f'- {opp}')
        lines += [
            '',
            '### Clone Effort:',
        ]
        for k, v in m.get('clone_effort', {}).items():
            if k != 'total_estimate':
                lines.append(f'- {k}: **{v}**')
        lines.append(f'- **TOTAL: {m.get("clone_effort", {}).get("total_estimate", "unknown")}**')
        lines.append('')

    # Gumroad
    if 'gumroad' in all_data:
        g = all_data['gumroad']
        lines += [
            '## Gumroad Products',
            f'- Total products: **{g.get("total_products", 0)}**',
            f'- Est. monthly revenue: **{g.get("estimated_monthly_revenue", "unknown")}**',
        ]
        for p in g.get('products', [])[:5]:
            lines.append(f'  - {p["name"]}: {p["price"]} ({p.get("reviews", 0)} reviews)')
        lines.append('')

    # LYNK
    if 'lynk' in all_data:
        l = all_data['lynk']
        lines += [
            '## LYNK Products',
            f'- Total products: **{l.get("total_products", 0)}**',
            f'- Est. revenue: **{l.get("estimated_revenue", "unknown")}**',
        ]
        for p in l.get('products', [])[:5]:
            lines.append(f'  - {p["name"]}: {p["price"]}')
        if l.get('social_links'):
            lines.append(f'- Social links: {", ".join(s["platform"] for s in l["social_links"])}')
        lines.append('')

    # Content Calendar
    if 'content_calendar' in all_data:
        cc = all_data['content_calendar']
        lines += [
            '## Content Calendar Analysis',
            f'- Consistency score: **{cc.get("consistency_score", 0)}/10**',
            f'- Best days: **{", ".join(cc.get("best_days", []))}**',
            f'- Best hours: **{cc.get("best_hours", [])}**',
            f'- Posting gaps: **{", ".join(cc.get("posting_gaps", []))}**',
        ]
        if cc.get('heatmap'):
            lines += ['', '```', cc['heatmap'], '```']
        lines.append('')

    # Competitive Opportunities
    if 'competitive_opportunities' in all_data:
        opps = all_data['competitive_opportunities']
        lines += [
            '## Competitive Opportunities',
        ]
        for i, opp in enumerate(opps, 1):
            lines.append(f'{i}. **{opp["area"]}** [{opp.get("priority", "medium")}]')
            lines.append(f'   - Insight: {opp["insight"]}')
            lines.append(f'   - Action: {opp["action"]}')
        lines.append('')

    return '\n'.join(lines)


# ─── Main Orchestrator ───────────────────────────────────────────────────────

async def run_spy(target: str, modules: list, mode: str = 'report') -> dict:
    """Run selected intelligence modules."""
    all_data = {}
    print(f'🕵️ Starting intelligence gathering on: {target}')
    print(f'   Modules: {modules}')
    print()

    # Social spy
    if 'social' in modules or 'content' in modules:
        print('📱 Social Media Spy...')
        all_data['social'] = await social_spy(target)
        s = all_data['social']
        tw = s.get('platforms', {}).get('twitter', {})
        print(f'   Twitter: {tw.get("posts_found",0)} posts | {tw.get("avg_views_per_post",0):,} avg views')

    # Ads spy
    if 'ads' in modules:
        print('📢 Ads Spy...')
        all_data['ads'] = await ads_spy(target)
        print(f'   FB ads: {all_data["ads"]["facebook_ads"].get("active_ads_found", "?")}')

    # Tech spy
    if 'tech' in modules:
        print('🔧 Tech Spy...')
        all_data['tech'] = await tech_spy(target)
        print(f'   Stack: {all_data["tech"].get("framework")} / {all_data["tech"].get("hosting")}')

    # Funnel spy
    if 'funnel' in modules:
        print('🔄 Funnel Spy...')
        all_data['funnel'] = await funnel_spy(target)
        print(f'   Prices: {all_data["funnel"].get("pricing", [])[:3]}')

    # Bot spy (uses bot-extractor)
    if 'bot' in modules and target.startswith('@'):
        print('🤖 Bot Spy...')
        sys.path.insert(0, str(WORKSPACE / 'skills/bot-extractor/scripts'))
        try:
            from bot_extractor import extract_bot
            from bot_cloner import generate_improvement_report
            arch = await extract_bot(target, verbose=False)
            if arch:
                all_data['bot'] = arch
                audit = generate_improvement_report(arch)
                all_data['bot']['audit_report'] = audit
                score_match = __import__('re').search(r'Score: (\d+)', audit)
                all_data['bot']['audit_score'] = int(score_match.group(1)) if score_match else 0
                print(f'   Bot score: {all_data["bot"].get("audit_score")}/100')
        except Exception as e:
            print(f'   Bot spy error: {e}')

    # Gumroad spy
    if 'gumroad' in modules:
        print('🛒 Gumroad Spy...')
        all_data['gumroad'] = await gumroad_spy(target)
        g = all_data['gumroad']
        print(f'   Products: {g.get("total_products", 0)} | Rev: {g.get("estimated_monthly_revenue", "?")}')

    # LYNK spy
    if 'lynk' in modules:
        print('🔗 LYNK Spy...')
        all_data['lynk'] = await lynk_spy(target)
        l = all_data['lynk']
        print(f'   Products: {l.get("total_products", 0)} | Rev: {l.get("estimated_revenue", "?")}')

    # Content Calendar spy
    if 'content-calendar' in modules or 'content' in modules:
        if 'social' in all_data:
            print('📅 Content Calendar Spy...')
            all_data['content_calendar'] = content_calendar_spy(all_data['social'])
            cc = all_data['content_calendar']
            print(f'   Consistency: {cc.get("consistency_score", 0)}/10 | Best days: {cc.get("best_days", [])}')

    # Revenue estimate
    if 'revenue' in modules:
        print('💰 Revenue Spy...')
        all_data['revenue'] = await revenue_spy(
            target,
            all_data.get('social'),
            all_data.get('funnel'),
            all_data.get('lynk'),
            all_data.get('gumroad')
        )
        est = all_data['revenue'].get('monthly_estimate', {})
        print(f'   Estimate: {est.get("low","?")} - {est.get("high","?")} /month')

    # Business model synthesis
    if 'model' in modules:
        print('🏗️  Model Synthesis...')
        all_data['model'] = model_spy(target, all_data)

    # Competitive opportunities
    all_data['competitive_opportunities'] = analyze_competitive_opportunities(all_data)
    if all_data['competitive_opportunities']:
        print(f'Target: {len(all_data["competitive_opportunities"])} opportunities found')

    return all_data


async def main():
    parser = argparse.ArgumentParser(description='Business Intelligence & Espionage')
    parser.add_argument('--target', required=True, help='Target: URL, @bot, or business name')
    parser.add_argument('--modules', default='social,tech,funnel,revenue,model',
                        help='Comma-separated modules')
    parser.add_argument('--all', action='store_true', help='Run all modules')
    parser.add_argument('--mode', default='report', choices=['report', 'clone', 'improve'])
    parser.add_argument('--output', help='Output file (JSON or MD)')
    parser.add_argument('--compare', help='Compare with own business URL')
    args = parser.parse_args()

    modules = ALL_MODULES if args.all else args.modules.split(',')

    # Run
    all_data = await run_spy(args.target, modules, args.mode)

    # Generate report
    print('\n' + '='*50)
    report = generate_report(args.target, all_data, args.mode)
    print(report)

    # Save
    slug = args.target.lstrip('@').replace('.','_').replace('/','_')[:30]
    ts = time.strftime('%Y%m%d_%H%M')

    if args.output:
        out_path = Path(args.output)
    else:
        out_path = REPORTS_DIR / f'{slug}_{ts}.json'

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump({'target': args.target, 'data': all_data, 'report': report},
                  f, indent=2, ensure_ascii=False, default=str)

    print(f'\n💾 Full data saved: {out_path}')


if __name__ == '__main__':
    asyncio.run(main())
