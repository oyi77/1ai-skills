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

ALL_MODULES = ['social', 'ads', 'funnel', 'revenue', 'bot', 'tech', 'content', 'seo', 'model', 'gumroad', 'lynk', 'content-calendar',
               'business_model', 'ads_intel', 'landing_page', 'content_intel', 'promotion', 'revenue_intel', 'market_opportunity']


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
        'TWITTER_AUTH_TOKEN': 'REDACTED_TWITTER_AUTH_TOKEN',
        'TWITTER_CT0': 'REDACTED_TWITTER_CT0'
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

    # Landing Page Deep Analysis
    if 'landing_page' in all_data:
        lp = all_data['landing_page']
        lines += [
            '## Landing Page Deep Analysis',
            f'- URL: **{lp.get("url", "N/A")}**',
            f'- H1: **{lp.get("h1", "N/A")}**',
            f'- H2s: {", ".join(lp.get("h2s", [])[:5]) or "none"}',
            f'- CTA Buttons: {", ".join(lp.get("cta_buttons", [])[:5]) or "none"}',
            f'- Funnel Type: **{lp.get("funnel_guess", "unknown")}**',
            f'- Price Display: **{lp.get("price_display_type", "unknown")}**',
            f'- Page Load: **{lp.get("page_load_time_ms", 0)}ms**',
            f'- Mobile Optimized: **{lp.get("mobile_optimized", False)}**',
            f'- Video Present: **{lp.get("video_present", False)}**',
            f'- Popup Detected: **{lp.get("popup_detected", False)}**',
        ]
        trust = lp.get('trust_signals', {})
        if trust:
            lines.append(f'- Testimonials: **{trust.get("testimonials_count", 0)}** | Reviews: **{trust.get("review_count", 0)}** | Badges: {", ".join(trust.get("badges", []))}')
        urgency = lp.get('urgency', {})
        if urgency.get('scarcity_text') or urgency.get('fomo_triggers'):
            lines.append(f'- Urgency: Scarcity={urgency.get("scarcity_text", [])}, FOMO={urgency.get("fomo_triggers", [])}')
        if lp.get('screenshot_path'):
            lines.append(f'- Screenshot: `{lp["screenshot_path"]}`')
        lines.append('')

    # Business Model Analysis
    if 'business_model' in all_data:
        bm = all_data['business_model']
        lines += [
            '## Business Model Intelligence',
            f'- Model Type: **{bm.get("business_model_type", "unknown")}**',
            f'- Value Proposition: **{bm.get("value_proposition", "N/A")}**',
            f'- Target Audience: **{bm.get("target_audience", "N/A")}**',
            f'- Primary CTA: **{bm.get("primary_cta", "N/A")}**',
            f'- Free Tier: **{bm.get("free_tier", False)}** {bm.get("free_tier_details", "")}',
            f'- Trial: **{bm.get("trial", False)}** {bm.get("trial_duration", "")}',
            f'- Refund: **{bm.get("refund_policy", False)}** {bm.get("refund_duration", "")}',
            f'- Revenue Model Score: **{bm.get("revenue_model_score", 0)}/10**',
        ]
        if bm.get('pricing_tiers'):
            lines.append('- **Pricing Tiers:**')
            for tier in bm['pricing_tiers'][:5]:
                if isinstance(tier, dict):
                    lines.append(f'  - {tier.get("name", "?")} : {tier.get("price", "?")} / {tier.get("period", "?")}')
        lines.append('')

    # Ads Intelligence
    if 'ads_intel' in all_data:
        ai = all_data['ads_intel']
        fb = ai.get('fb_ads', {})
        lines += [
            '## Ads Intelligence',
            f'- FB Ads Count: **{fb.get("count", 0)}**',
            f'- FB Estimated Spend: **IDR {fb.get("estimated_spend_idr", 0):,}**',
            f'- TikTok Hooks Found: **{ai.get("tiktok_ads", {}).get("count", 0)}**',
            f'- Budget Estimate: **{ai.get("budget_estimate", "unknown")}**',
        ]
        wp = ai.get('winning_patterns', {})
        if wp.get('top_ctas'):
            lines.append(f'- Top CTAs: {", ".join(wp["top_ctas"][:5])}')
        if wp.get('emotional_triggers'):
            lines.append(f'- Emotional Triggers: {", ".join(wp["emotional_triggers"])}')
        lines.append('')

    # Content Intelligence
    if 'content_intel' in all_data:
        ci = all_data['content_intel']
        cs = ci.get('content_strategy', {})
        lines += [
            '## Content Intelligence',
            f'- Primary Platform: **{cs.get("primary_platform", "unknown")}**',
            f'- Top Content Type: **{cs.get("top_content_type", "unknown")}**',
        ]
        if cs.get('viral_hooks'):
            lines.append('- **Viral Hooks:**')
            for h in cs['viral_hooks'][:5]:
                lines.append(f'  - {h}')
        if cs.get('hashtags_used'):
            lines.append(f'- Top Hashtags: {", ".join("#" + h for h in cs["hashtags_used"][:10])}')
        # Per-platform summary
        tt = ci.get('tiktok', {})
        if tt and not tt.get('error'):
            lines.append(f'- TikTok: **{tt.get("followers", 0):,}** followers, **{tt.get("video_count", 0)}** videos, ER={tt.get("engagement_rate", "N/A")}')
        ig = ci.get('instagram', {})
        if ig and not ig.get('error'):
            lines.append(f'- Instagram: **{ig.get("followers", 0):,}** followers, **{ig.get("posts_count", 0)}** posts')
        yt = ci.get('youtube', {})
        if yt and not yt.get('error'):
            lines.append(f'- YouTube: **{yt.get("subscribers", "?")}** subscribers, **{yt.get("total_videos", "?")}** videos')
        lines.append('')

    # Promotion Strategy
    if 'promotion' in all_data:
        ps = all_data['promotion']
        lines += [
            '## Promotion Strategy',
            f'- Paid vs Organic: **{ps.get("paid_vs_organic", "unknown")}**',
            f'- Active Channels: **{", ".join(ps.get("active_channels", []))}**',
            f'- Growth Strategy: **{ps.get("growth_strategy", "unknown")}**',
            f'- Affiliate Program: **{ps.get("has_affiliate_program", False)}**',
            f'- Telegram Community: **{ps.get("has_telegram_community", False)}**',
            f'- Email List: **{ps.get("has_email_list", False)}**',
            f'- SEO Presence: **{ps.get("seo_presence", "none")}**',
            f'- Budget Estimate: **{ps.get("promotion_budget_estimate", "unknown")}**',
            '',
        ]

    # Revenue Intelligence
    if 'revenue_intel' in all_data:
        ri = all_data['revenue_intel']
        est = ri.get('total_revenue_estimate', {})
        lines += [
            '## Revenue Intelligence (Deep)',
            f'- **Low:** {est.get("low", "N/A")}',
            f'- **Mid:** {est.get("mid", "N/A")}',
            f'- **High:** {est.get("high", "N/A")}',
            f'- Revenue Model Score: **{ri.get("revenue_model_score", 0)}/10**',
        ]
        if ri.get('revenue_sources'):
            lines.append('- **Revenue Sources:**')
            for src in ri['revenue_sources'][:5]:
                lines.append(f'  - {src.get("source", "?")}: IDR {src.get("estimated_monthly_idr", 0):,}/mo [{src.get("confidence", "?")}]')
        ue = ri.get('unit_economics', {})
        if ue.get('cac_estimate_idr'):
            lines.append(f'- Unit Economics: CAC=IDR {ue["cac_estimate_idr"]:,} | LTV=IDR {ue.get("ltv_estimate_idr", 0):,} | Ratio={ue.get("ltv_cac_ratio", 0)}')
        if ri.get('key_revenue_drivers'):
            lines.append(f'- Key Drivers: {", ".join(ri["key_revenue_drivers"])}')
        if ri.get('revenue_risks'):
            lines.append('- **Risks:**')
            for risk in ri['revenue_risks']:
                lines.append(f'  - {risk}')
        lines.append('')

    # Market Opportunities
    if 'market_opportunity' in all_data:
        mo = all_data['market_opportunity']
        opps = mo.get('opportunities', [])
        if opps:
            lines += [
                '## Market Opportunities (AI-Generated)',
            ]
            for i, opp in enumerate(opps, 1):
                lines.append(f'{i}. **{opp.get("opportunity", "?")}**')
                lines.append(f'   - Effort: {opp.get("effort", "?")} | Time: {opp.get("time_to_revenue", "?")} | Revenue: IDR {opp.get("revenue_potential_idr", 0):,}/mo')
                lines.append(f'   - Risk: {opp.get("risk", "?")}')
                lines.append(f'   - Why we win: {opp.get("why_we_can_win", "?")}')
                lines.append(f'   - Next action: {opp.get("next_action", "?")}')
            lines.append('')

    return '\n'.join(lines)


# ─── Module: BUSINESS MODEL SPY ──────────────────────────────────────────────

async def business_model_spy(url: str, target_name: str) -> dict:
    """Scrape landing page + social profiles to classify business model and pricing."""
    result = {
        'module': 'business_model_spy',
        'target': target_name,
        'url': url,
        'business_model_type': 'unknown',
        'pricing_tiers': [],
        'free_tier': False,
        'free_tier_details': '',
        'trial': False,
        'trial_duration': '',
        'refund_policy': False,
        'refund_duration': '',
        'primary_cta': '',
        'value_proposition': '',
        'target_audience': '',
        'revenue_model_score': 0,
    }

    try:
        os.environ.setdefault('DISPLAY', ':99')
        from playwright.sync_api import sync_playwright
        import threading

        page_data_holder = [None]
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
                    page.goto(url, wait_until='domcontentloaded', timeout=20000)
                    page.wait_for_timeout(3000)

                    # Extract headings
                    headings = []
                    for tag in ['h1', 'h2', 'h3']:
                        els = page.query_selector_all(tag)
                        for el in els[:10]:
                            txt = el.inner_text().strip()
                            if txt:
                                headings.append({'tag': tag, 'text': txt})

                    # Extract price elements
                    price_texts = []
                    for sel in ['[class*="price"]', '[class*="Price"]', '[class*="plan"]', '[class*="Plan"]',
                                '[class*="tier"]', '[class*="Tier"]', '[class*="pricing"]']:
                        els = page.query_selector_all(sel)
                        for el in els[:10]:
                            txt = el.inner_text().strip()
                            if txt and len(txt) < 500:
                                price_texts.append(txt)

                    # Extract CTA buttons
                    cta_texts = []
                    for sel in ['button', 'a[class*="cta"]', 'a[class*="btn"]', 'a[class*="button"]',
                                '[class*="CTA"]', '[class*="action"]']:
                        els = page.query_selector_all(sel)
                        for el in els[:15]:
                            txt = el.inner_text().strip()
                            if txt and 2 < len(txt) < 100:
                                cta_texts.append(txt)

                    full_text = page.inner_text('body')[:5000]

                    page_data_holder[0] = {
                        'headings': headings,
                        'price_texts': price_texts,
                        'cta_texts': cta_texts,
                        'full_text': full_text,
                    }
                    browser.close()
            except Exception as e:
                error_holder[0] = str(e)

        t = threading.Thread(target=run_sync)
        t.start()
        t.join(timeout=35)

        if error_holder[0]:
            raise Exception(error_holder[0])
        if not page_data_holder[0]:
            raise Exception('Playwright timeout - no content')

        page_data = page_data_holder[0]

        # Use LLM to classify business model
        try:
            from openai import OpenAI
            client = OpenAI(
                base_url="http://localhost:20128/v1",
                api_key=os.environ.get('OMNIROUTE_KEY', 'omniroute')
            )

            prompt_content = (
                f"Analyze this landing page data for '{target_name}' and return a JSON object.\n\n"
                f"Headings: {json.dumps(page_data['headings'][:15])}\n"
                f"Price elements: {json.dumps(page_data['price_texts'][:10])}\n"
                f"CTA buttons: {json.dumps(page_data['cta_texts'][:10])}\n"
                f"Page text excerpt: {page_data['full_text'][:2000]}\n\n"
                "Return ONLY valid JSON with these keys:\n"
                '- business_model_type: "bot_subscription" | "one_time_product" | "freemium" | "affiliate" | "course" | "saas"\n'
                '- pricing_tiers: [{name, price, period, features}] (up to 5)\n'
                '- free_tier: true/false\n- free_tier_details: string\n'
                '- trial: true/false\n- trial_duration: string\n'
                '- refund_policy: true/false\n- refund_duration: string\n'
                '- primary_cta: string\n- value_proposition: string\n'
                '- target_audience: string\n- revenue_model_score: 1-10'
            )

            resp = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[
                    {'role': 'system', 'content': 'You are a business analyst. Return only valid JSON, no markdown.'},
                    {'role': 'user', 'content': prompt_content}
                ],
                temperature=0.3,
                max_tokens=1500,
            )

            raw = resp.choices[0].message.content.strip()
            # Strip markdown code fences if present
            if raw.startswith('```'):
                raw = raw.split('\n', 1)[1] if '\n' in raw else raw[3:]
                if raw.endswith('```'):
                    raw = raw[:-3]
            parsed = json.loads(raw)
            result.update(parsed)

        except Exception as e:
            result['llm_error'] = str(e)[:200]

        # Store raw scraped data for reference
        result['_scraped'] = {
            'headings_count': len(page_data['headings']),
            'price_elements_count': len(page_data['price_texts']),
            'cta_count': len(page_data['cta_texts']),
        }

    except Exception as e:
        result['error'] = str(e)[:200]

    return result


# ─── Module: ADS INTELLIGENCE SPY ───────────────────────────────────────────

async def ads_intelligence_spy(target_name: str, page_id: str = None) -> dict:
    """Full ad creative intelligence from Facebook Ad Library and TikTok Creative Center."""
    result = {
        'module': 'ads_intelligence_spy',
        'target': target_name,
        'fb_ads': {'count': 0, 'ads': [], 'estimated_spend_idr': 0},
        'tiktok_ads': {'count': 0, 'top_hooks': []},
        'winning_patterns': {'top_ctas': [], 'top_hooks': [], 'emotional_triggers': []},
        'budget_estimate': 'unknown',
    }

    # --- Facebook Ad Library ---
    try:
        os.environ.setdefault('DISPLAY', ':99')
        from playwright.sync_api import sync_playwright
        import threading

        fb_data_holder = [None]
        fb_error_holder = [None]

        def run_fb():
            try:
                clean = target_name.lstrip('@').replace('_', '+')
                fb_url = f'https://www.facebook.com/ads/library/?q={clean}&search_type=keyword_unordered&active_status=active'

                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        slow_mo=500,
                        args=["--no-sandbox", "--disable-setuid-sandbox"]
                    )
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    )
                    page = context.new_page()
                    page.goto(fb_url, wait_until='domcontentloaded', timeout=25000)
                    page.wait_for_timeout(5000)

                    html = page.content()

                    # Try to extract ad cards
                    import re as _re
                    ads = []
                    # Look for ad container divs
                    ad_cards = page.query_selector_all('[class*="xrvj5dj"], [class*="ad-card"], [data-testid*="ad"]')
                    if not ad_cards:
                        ad_cards = page.query_selector_all('div._7jvw') or []

                    for i, card in enumerate(ad_cards[:20]):
                        try:
                            text = card.inner_text().strip()
                            lines = [l.strip() for l in text.split('\n') if l.strip()]
                            headline = lines[0] if lines else ''
                            body = lines[1] if len(lines) > 1 else ''
                            cta = lines[-1] if len(lines) > 2 else ''

                            # Try to extract start date
                            date_match = _re.search(r'Started running on\s*(\w+ \d+,?\s*\d{4})', text)
                            start_date = date_match.group(1) if date_match else ''

                            # Estimate days running
                            days_running = 30  # default
                            if start_date:
                                try:
                                    from datetime import datetime
                                    sd = datetime.strptime(start_date.replace(',', ''), '%b %d %Y')
                                    days_running = max(1, (datetime.now() - sd).days)
                                except Exception:
                                    pass

                            ads.append({
                                'headline': headline[:150],
                                'body': body[:300],
                                'cta': cta[:80],
                                'start_date': start_date,
                                'days_running': days_running,
                                'platform': 'facebook',
                                'media_type': 'image',  # default
                            })
                        except Exception:
                            continue

                    # Count from page
                    count_match = _re.search(r'"total_count":(\d+)', html)
                    ad_count = int(count_match.group(1)) if count_match else len(ads)
                    if ad_count == 0:
                        ad_count = len(ads)

                    fb_data_holder[0] = {'count': ad_count, 'ads': ads}
                    browser.close()
            except Exception as e:
                fb_error_holder[0] = str(e)

        t = threading.Thread(target=run_fb)
        t.start()
        t.join(timeout=45)

        if fb_data_holder[0]:
            fb = fb_data_holder[0]
            result['fb_ads']['count'] = fb['count']
            result['fb_ads']['ads'] = fb['ads']

            # Estimate spend: ad_count * 300000 IDR * avg_days_running / 30
            if fb['ads']:
                avg_days = sum(a.get('days_running', 30) for a in fb['ads']) / len(fb['ads'])
            else:
                avg_days = 30
            result['fb_ads']['estimated_spend_idr'] = int(fb['count'] * 300000 * avg_days / 30)
        elif fb_error_holder[0]:
            result['fb_ads']['error'] = fb_error_holder[0][:200]

    except Exception as e:
        result['fb_ads']['error'] = str(e)[:200]

    # --- TikTok Creative Center ---
    try:
        from playwright.sync_api import sync_playwright
        import threading

        tt_data_holder = [None]
        tt_error_holder = [None]

        def run_tt():
            try:
                tt_url = 'https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en'
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-setuid-sandbox"]
                    )
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    )
                    page = context.new_page()
                    page.goto(tt_url, wait_until='domcontentloaded', timeout=20000)
                    page.wait_for_timeout(4000)

                    # Try to search for keyword
                    clean_kw = target_name.lstrip('@').replace('_', ' ')
                    search_input = page.query_selector('input[type="text"], input[placeholder*="Search"]')
                    if search_input:
                        search_input.fill(clean_kw)
                        page.keyboard.press('Enter')
                        page.wait_for_timeout(3000)

                    html = page.content()
                    import re as _re

                    # Extract top hooks from visible ad copy
                    hooks = []
                    ad_texts = page.query_selector_all('[class*="title"], [class*="desc"], [class*="caption"]')
                    for el in ad_texts[:20]:
                        txt = el.inner_text().strip()
                        if txt and 5 < len(txt) < 200:
                            hooks.append(txt)

                    tt_data_holder[0] = {'count': len(hooks), 'top_hooks': hooks[:10]}
                    browser.close()
            except Exception as e:
                tt_error_holder[0] = str(e)

        t2 = threading.Thread(target=run_tt)
        t2.start()
        t2.join(timeout=35)

        if tt_data_holder[0]:
            result['tiktok_ads'] = tt_data_holder[0]
        elif tt_error_holder[0]:
            result['tiktok_ads']['error'] = tt_error_holder[0][:200]

    except Exception as e:
        result['tiktok_ads']['error'] = str(e)[:200]

    # --- Synthesize winning patterns ---
    try:
        all_ctas = [a.get('cta', '') for a in result['fb_ads'].get('ads', []) if a.get('cta')]
        all_hooks = [a.get('headline', '') for a in result['fb_ads'].get('ads', []) if a.get('headline')]
        all_hooks += result['tiktok_ads'].get('top_hooks', [])

        from collections import Counter
        result['winning_patterns']['top_ctas'] = [c for c, _ in Counter(all_ctas).most_common(5)]
        result['winning_patterns']['top_hooks'] = all_hooks[:10]

        # Emotional triggers
        triggers_map = {
            'fear': ['jangan', 'bahaya', 'rugi', 'stop', 'awas'],
            'greed': ['gratis', 'bonus', 'diskon', 'hemat', 'murah', 'free'],
            'urgency': ['terbatas', 'sekarang', 'hari ini', 'terakhir', 'limited'],
            'curiosity': ['ternyata', 'rahasia', 'cara', 'trik', 'hack'],
            'social_proof': ['ribuan', 'orang', 'testimoni', 'pengguna', 'terbukti'],
        }
        detected_triggers = []
        combined_text = ' '.join(all_hooks + all_ctas).lower()
        for trigger, keywords in triggers_map.items():
            if any(kw in combined_text for kw in keywords):
                detected_triggers.append(trigger)
        result['winning_patterns']['emotional_triggers'] = detected_triggers

    except Exception:
        pass

    # --- Budget estimate ---
    try:
        spend = result['fb_ads'].get('estimated_spend_idr', 0)
        if spend < 5000000:
            result['budget_estimate'] = 'low (<5M/month)'
        elif spend < 20000000:
            result['budget_estimate'] = 'medium (5-20M)'
        else:
            result['budget_estimate'] = 'high (>20M)'
    except Exception:
        pass

    return result


# ─── Module: LANDING PAGE DEEP SPY ──────────────────────────────────────────

async def landing_page_deep_spy(url: str) -> dict:
    """Full landing page intelligence with screenshot capture."""
    import re as _re
    from urllib.parse import urlparse

    result = {
        'module': 'landing_page_deep_spy',
        'url': url,
        'h1': '',
        'h2s': [],
        'cta_buttons': [],
        'trust_signals': {
            'testimonials_count': 0,
            'star_ratings': [],
            'review_count': 0,
            'badges': [],
        },
        'urgency': {
            'countdown_timer': False,
            'scarcity_text': [],
            'fomo_triggers': [],
        },
        'lead_magnets': [],
        'popup_detected': False,
        'price_display_type': 'unknown',
        'social_proof_numbers': [],
        'video_present': False,
        'mobile_optimized': False,
        'page_load_time_ms': 0,
        'funnel_guess': 'unknown',
        'screenshot_path': '',
    }

    try:
        os.environ.setdefault('DISPLAY', ':99')
        from playwright.sync_api import sync_playwright
        import threading

        page_data_holder = [None]
        error_holder = [None]

        screenshots_dir = Path(__file__).parent.parent / 'reports' / 'screenshots'
        screenshots_dir.mkdir(parents=True, exist_ok=True)
        domain = urlparse(url).netloc.replace('www.', '') or 'unknown'
        screenshot_path = str(screenshots_dir / f'{domain}.png')

        def run_sync():
            try:
                with sync_playwright() as p:
                    browser = p.chromium.launch(
                        headless=True,
                        args=["--no-sandbox", "--disable-setuid-sandbox"]
                    )
                    context = browser.new_context(
                        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
                        viewport={'width': 390, 'height': 844},
                        is_mobile=True,
                    )
                    page = context.new_page()

                    start_time = time.time()
                    page.goto(url, wait_until='domcontentloaded', timeout=25000)
                    page.wait_for_timeout(3000)
                    load_time_ms = int((time.time() - start_time) * 1000)

                    # Full page screenshot
                    try:
                        page.screenshot(path=screenshot_path, full_page=True, timeout=15000)
                    except Exception:
                        pass

                    html = page.content()

                    # Extract h1
                    h1_el = page.query_selector('h1')
                    h1_text = h1_el.inner_text().strip() if h1_el else ''

                    # Extract h2s
                    h2_els = page.query_selector_all('h2')
                    h2_texts = [el.inner_text().strip() for el in h2_els[:5] if el.inner_text().strip()]

                    # CTA buttons
                    cta_texts = []
                    for sel in ['button', 'a[class*="btn"]', 'a[class*="cta"]', 'a[class*="button"]',
                                '[class*="CTA"]', '[role="button"]']:
                        for el in page.query_selector_all(sel)[:15]:
                            txt = el.inner_text().strip()
                            if txt and 2 < len(txt) < 100:
                                cta_texts.append(txt)

                    # Check for video
                    video_present = bool(page.query_selector('video, iframe[src*="youtube"], iframe[src*="vimeo"]'))

                    # Check mobile meta viewport
                    viewport_meta = page.query_selector('meta[name="viewport"]')
                    mobile_opt = bool(viewport_meta)

                    # Popup detection
                    popup_detected = False
                    try:
                        popup_sels = ['[class*="popup"]', '[class*="modal"]', '[class*="overlay"]',
                                      '[id*="popup"]', '[id*="modal"]']
                        for sel in popup_sels:
                            el = page.query_selector(sel)
                            if el and el.is_visible():
                                popup_detected = True
                                break
                    except Exception:
                        pass

                    body_text = page.inner_text('body')[:8000]

                    page_data_holder[0] = {
                        'html': html,
                        'h1': h1_text,
                        'h2s': h2_texts,
                        'cta_texts': list(set(cta_texts))[:10],
                        'video_present': video_present,
                        'mobile_optimized': mobile_opt,
                        'popup_detected': popup_detected,
                        'load_time_ms': load_time_ms,
                        'body_text': body_text,
                    }
                    browser.close()
            except Exception as e:
                error_holder[0] = str(e)

        t = threading.Thread(target=run_sync)
        t.start()
        t.join(timeout=45)

        if error_holder[0]:
            raise Exception(error_holder[0])
        if not page_data_holder[0]:
            raise Exception('Playwright timeout - no content')

        pd = page_data_holder[0]
        html = pd['html']
        body_text = pd['body_text']

        result['h1'] = pd['h1']
        result['h2s'] = pd['h2s']
        result['cta_buttons'] = pd['cta_texts']
        result['video_present'] = pd['video_present']
        result['mobile_optimized'] = pd['mobile_optimized']
        result['popup_detected'] = pd['popup_detected']
        result['page_load_time_ms'] = pd['load_time_ms']

        if Path(screenshot_path).exists():
            result['screenshot_path'] = screenshot_path

        # Trust signals
        body_lower = body_text.lower()
        testimoni_keywords = ['testimoni', 'testimonial', 'review', 'kata mereka', 'customer say']
        for kw in testimoni_keywords:
            count = body_lower.count(kw)
            if count > 0:
                result['trust_signals']['testimonials_count'] += count

        star_matches = _re.findall(r'(\d(?:\.\d)?)\s*(?:/5|stars?|bintang)', body_lower)
        result['trust_signals']['star_ratings'] = star_matches[:5]

        review_match = _re.search(r'(\d[\d,.]*)\s*(?:review|ulasan|rating)', body_lower)
        if review_match:
            result['trust_signals']['review_count'] = int(review_match.group(1).replace(',', '').replace('.', ''))

        badge_keywords = ['verified', 'certified', 'official', 'trusted', 'secure', 'ssl', 'garansi']
        result['trust_signals']['badges'] = [b for b in badge_keywords if b in body_lower]

        # Urgency signals
        result['urgency']['countdown_timer'] = bool(_re.search(r'countdown|timer|hour.*minute.*second', html.lower()))
        scarcity_keywords = ['terbatas', 'limited', 'sisa', 'hanya', 'only', 'habis', 'slot']
        result['urgency']['scarcity_text'] = [s for s in scarcity_keywords if s in body_lower]
        fomo_keywords = ['orang sedang melihat', 'baru saja membeli', 'people viewing', 'just purchased',
                         'jangan sampai', 'harga naik', 'besok']
        result['urgency']['fomo_triggers'] = [f for f in fomo_keywords if f in body_lower]

        # Lead magnets
        lead_keywords = ['download gratis', 'free download', 'ebook gratis', 'free ebook', 'lead magnet',
                         'free template', 'template gratis', 'checklist', 'cheat sheet']
        result['lead_magnets'] = [lm for lm in lead_keywords if lm in body_lower]

        # Price display type
        if _re.search(r'(?:Rp|IDR|USD|\$)\s*[\d.,]+', body_text):
            if _re.search(r'(?:per\s*(?:bulan|month|tahun|year))|(?:/(?:mo|month|yr|year|bulan))', body_lower):
                result['price_display_type'] = 'subscription'
            else:
                result['price_display_type'] = 'one_time'
        elif 'gratis' in body_lower or 'free' in body_lower:
            result['price_display_type'] = 'free'
        else:
            result['price_display_type'] = 'hidden'

        # Social proof numbers
        sp_matches = _re.findall(r'(\d[\d,.]*)\+?\s*(?:pengguna|user|customer|pelanggan|orang|member|download|subscriber)',
                                 body_lower)
        result['social_proof_numbers'] = sp_matches[:5]

        # Funnel guess
        if result['lead_magnets']:
            result['funnel_guess'] = 'lead_magnet'
        elif any(kw in body_lower for kw in ['demo', 'jadwalkan', 'schedule', 'book a call']):
            result['funnel_guess'] = 'demo_call'
        elif result['price_display_type'] == 'free' or 'freemium' in body_lower:
            result['funnel_guess'] = 'freemium'
        elif any(kw in body_lower for kw in ['affiliate', 'afiliasi', 'referral', 'komisi']):
            result['funnel_guess'] = 'affiliate'
        elif result['price_display_type'] in ('one_time', 'subscription'):
            result['funnel_guess'] = 'direct_sales'
        else:
            result['funnel_guess'] = 'unknown'

    except Exception as e:
        result['error'] = str(e)[:200]

    return result


# ─── Module: CONTENT INTELLIGENCE SPY ───────────────────────────────────────

async def content_intelligence_spy(handles: dict) -> dict:
    """Deep content intelligence across TikTok, Instagram, YouTube, and Twitter."""
    import re as _re

    result = {
        'module': 'content_intelligence_spy',
        'handles': handles,
        'tiktok': {},
        'instagram': {},
        'youtube': {},
        'twitter': {},
        'content_strategy': {
            'primary_platform': 'unknown',
            'posting_frequency': {},
            'top_content_type': 'unknown',
            'viral_hooks': [],
            'engagement_rate': {},
            'content_calendar': {'days': [], 'times': []},
            'hashtags_used': [],
        },
    }

    # --- TikTok ---
    tiktok_handle = handles.get('tiktok', '').lstrip('@')
    if tiktok_handle:
        try:
            os.environ.setdefault('DISPLAY', ':99')
            from playwright.sync_api import sync_playwright
            import threading

            tt_holder = [None]
            def run_tiktok():
                try:
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
                        context = browser.new_context(
                            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15'
                        )
                        page = context.new_page()
                        page.goto(f'https://www.tiktok.com/@{tiktok_handle}', wait_until='domcontentloaded', timeout=15000)
                        page.wait_for_timeout(4000)
                        html = page.content()
                        tt_holder[0] = html
                        browser.close()
                except Exception:
                    pass

            t = threading.Thread(target=run_tiktok)
            t.start()
            t.join(timeout=30)

            html = tt_holder[0] or ''
            if html:
                followers = _re.search(r'"followerCount":(\d+)', html)
                following = _re.search(r'"followingCount":(\d+)', html)
                likes = _re.search(r'"heartCount":(\d+)', html) or _re.search(r'"heart":(\d+)', html)
                video_count = _re.search(r'"videoCount":(\d+)', html)
                bio = _re.search(r'"signature":"([^"]*)"', html)

                result['tiktok'] = {
                    'username': tiktok_handle,
                    'followers': int(followers.group(1)) if followers else 0,
                    'following': int(following.group(1)) if following else 0,
                    'total_likes': int(likes.group(1)) if likes else 0,
                    'video_count': int(video_count.group(1)) if video_count else 0,
                    'bio': bio.group(1) if bio else '',
                }

                # Top 12 videos
                video_items = _re.findall(
                    r'"id":"(\d+)".*?"desc":"([^"]*)".*?"playCount":(\d+).*?"diggCount":(\d+).*?"commentCount":(\d+).*?"shareCount":(\d+)',
                    html
                )
                if not video_items:
                    video_items = _re.findall(
                        r'"id":"(\d+)".*?"desc":"([^"]*)".*?"playCount":(\d+).*?"diggCount":(\d+)', html
                    )
                    video_items = [(v[0], v[1], v[2], v[3], '0', '0') for v in video_items]

                top_videos = []
                viral_hooks = []
                for vid_id, desc, views, lks, comments, shares in video_items[:12]:
                    top_videos.append({
                        'desc': desc[:120],
                        'views': int(views),
                        'likes': int(lks),
                        'comments': int(comments) if comments else 0,
                        'shares': int(shares) if shares else 0,
                    })
                    if desc.strip():
                        hook = desc.split('.')[0].split('!')[0].split('?')[0][:80]
                        if hook:
                            viral_hooks.append(hook)

                result['tiktok']['top_videos'] = top_videos
                result['tiktok']['viral_hooks'] = viral_hooks[:5]

                # Posting frequency estimate
                if result['tiktok'].get('video_count', 0) > 0:
                    result['tiktok']['posting_frequency'] = 'active' if result['tiktok']['video_count'] > 50 else 'moderate'

                # Best content type inference
                if top_videos:
                    avg_views = sum(v['views'] for v in top_videos) / len(top_videos)
                    result['tiktok']['avg_views'] = int(avg_views)
                    total_followers = result['tiktok'].get('followers', 1) or 1
                    result['tiktok']['engagement_rate'] = f'{(sum(v["likes"] for v in top_videos) / len(top_videos) / total_followers * 100):.2f}%'

        except Exception as e:
            result['tiktok'] = {'error': str(e)[:150]}

    # --- Instagram ---
    ig_handle = handles.get('instagram', '').lstrip('@')
    if ig_handle:
        try:
            from playwright.sync_api import sync_playwright
            import threading

            ig_holder = [None]
            def run_ig():
                try:
                    with sync_playwright() as p:
                        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
                        context = browser.new_context(
                            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
                            viewport={'width': 390, 'height': 844},
                            is_mobile=True,
                        )
                        page = context.new_page()
                        page.goto(f'https://www.instagram.com/{ig_handle}/', wait_until='domcontentloaded', timeout=15000)
                        page.wait_for_timeout(4000)
                        ig_holder[0] = page.content()
                        browser.close()
                except Exception:
                    pass

            t2 = threading.Thread(target=run_ig)
            t2.start()
            t2.join(timeout=30)

            html = ig_holder[0] or ''
            if html:
                followers = _re.search(r'"edge_followed_by":\{"count":(\d+)', html) or _re.search(r'"follower_count":(\d+)', html)
                following = _re.search(r'"edge_follow":\{"count":(\d+)', html) or _re.search(r'"following_count":(\d+)', html)
                posts = _re.search(r'"edge_owner_to_timeline_media":\{"count":(\d+)', html) or _re.search(r'"media_count":(\d+)', html)
                bio = _re.search(r'"biography":"([^"]*)"', html)

                result['instagram'] = {
                    'username': ig_handle,
                    'followers': int(followers.group(1)) if followers else 0,
                    'following': int(following.group(1)) if following else 0,
                    'posts_count': int(posts.group(1)) if posts else 0,
                    'bio': bio.group(1) if bio else '',
                }

                # Bio links
                bio_link = _re.search(r'"external_url":"([^"]*)"', html)
                if bio_link:
                    result['instagram']['bio_link'] = bio_link.group(1)

                # Story highlights
                highlight_count = len(_re.findall(r'"highlight_reel_count":(\d+)', html))
                result['instagram']['story_highlights'] = highlight_count

        except Exception as e:
            result['instagram'] = {'error': str(e)[:150]}

    # --- YouTube ---
    yt_handle = handles.get('youtube', '').lstrip('@')
    if yt_handle:
        try:
            import urllib.request
            yt_url = f'https://www.youtube.com/@{yt_handle}'
            req = urllib.request.Request(yt_url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            r = urllib.request.urlopen(req, timeout=12)
            html = r.read().decode('utf-8', errors='ignore')

            sub_match = _re.search(r'"subscriberCountText":\{"simpleText":"([\d.]+[KMB]?) subscriber', html)
            vid_count = _re.search(r'"videosCountText":\{"runs":\[\{"text":"([\d,]+)"', html)
            desc = _re.search(r'"description":"([^"]{0,500})"', html)

            result['youtube'] = {
                'channel': yt_handle,
                'subscribers': sub_match.group(1) if sub_match else 'unknown',
                'total_videos': vid_count.group(1) if vid_count else 'unknown',
                'description': desc.group(1)[:200] if desc else '',
            }

            # Recent videos
            video_entries = _re.findall(
                r'"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"viewCountText":\{"simpleText":"([\d,.]+ views?)".*?"publishedTimeText":\{"simpleText":"([^"]+)"',
                html
            )
            recent_videos = []
            for title, views_str, pub_date in video_entries[:10]:
                views_clean = _re.sub(r'[^\d]', '', views_str)
                recent_videos.append({
                    'title': title[:100],
                    'views': int(views_clean) if views_clean else 0,
                    'date': pub_date,
                })
            result['youtube']['recent_videos'] = recent_videos

        except Exception as e:
            result['youtube'] = {'error': str(e)[:150]}

    # --- Twitter (from handles if provided) ---
    tw_handle = handles.get('twitter', '').lstrip('@')
    if tw_handle:
        result['twitter'] = {'handle': tw_handle, 'note': 'Use social_spy for detailed Twitter data'}

    # --- Synthesize content_strategy ---
    try:
        # Determine primary platform by follower count
        platform_followers = {}
        if result['tiktok'].get('followers', 0) > 0:
            platform_followers['tiktok'] = result['tiktok']['followers']
        if result['instagram'].get('followers', 0) > 0:
            platform_followers['instagram'] = result['instagram']['followers']
        yt_subs = result.get('youtube', {}).get('subscribers', '0')
        if yt_subs and yt_subs != 'unknown':
            # Parse K/M/B
            yt_num = yt_subs.replace('K', '000').replace('M', '000000').replace('B', '000000000').replace('.', '')
            try:
                platform_followers['youtube'] = int(yt_num)
            except ValueError:
                pass

        if platform_followers:
            result['content_strategy']['primary_platform'] = max(platform_followers, key=platform_followers.get)
            result['content_strategy']['engagement_rate'] = {}
            if 'tiktok' in result and result['tiktok'].get('engagement_rate'):
                result['content_strategy']['engagement_rate']['tiktok'] = result['tiktok']['engagement_rate']

        # Viral hooks
        hooks = result.get('tiktok', {}).get('viral_hooks', [])
        result['content_strategy']['viral_hooks'] = hooks[:5]

        # Hashtags from TikTok videos
        all_descs = ' '.join(v.get('desc', '') for v in result.get('tiktok', {}).get('top_videos', []))
        hashtags = _re.findall(r'#(\w+)', all_descs)
        if hashtags:
            from collections import Counter
            result['content_strategy']['hashtags_used'] = [h for h, _ in Counter(hashtags).most_common(10)]

    except Exception:
        pass

    return result


# ─── Module: PROMOTION STRATEGY SPY ─────────────────────────────────────────

def promotion_strategy_spy(target: str, all_data: dict) -> dict:
    """Cross-analyze all data to infer promotion strategy."""
    result = {
        'module': 'promotion_strategy_spy',
        'target': target,
        'paid_vs_organic': 'unknown',
        'active_channels': [],
        'has_affiliate_program': False,
        'has_telegram_community': False,
        'has_email_list': False,
        'seo_presence': 'none',
        'influencer_marketing': False,
        'promotion_budget_estimate': 'unknown',
        'growth_strategy': 'unknown',
    }

    try:
        social = all_data.get('social', {})
        ads = all_data.get('ads', {}) or all_data.get('ads_intel', {})
        funnel = all_data.get('funnel', {})
        tech = all_data.get('tech', {})
        lynk = all_data.get('lynk', {})
        landing = all_data.get('landing_page', {})
        content_intel = all_data.get('content_intel', {})

        # Active channels
        platforms = social.get('platforms', {})
        for plat, data in platforms.items():
            if isinstance(data, dict) and not data.get('error'):
                result['active_channels'].append(plat)

        # Check content intel platforms
        for plat in ['tiktok', 'instagram', 'youtube']:
            ci_data = content_intel.get(plat, {})
            if ci_data and not ci_data.get('error') and ci_data.get('followers', ci_data.get('subscribers', 0)):
                if plat not in result['active_channels']:
                    result['active_channels'].append(plat)

        # Lynk social links
        for sl in lynk.get('social_links', []):
            plat = sl.get('platform', '')
            if plat and plat not in result['active_channels']:
                result['active_channels'].append(plat)

        # Paid vs organic
        fb_ad_count = 0
        if isinstance(ads, dict):
            fb_ads = ads.get('fb_ads', ads.get('facebook_ads', {}))
            if isinstance(fb_ads, dict):
                fb_ad_count = fb_ads.get('count', fb_ads.get('active_ads_found', 0))

        has_pixels = bool(tech.get('pixels'))
        if fb_ad_count > 5 or has_pixels:
            result['paid_vs_organic'] = 'mostly_paid' if fb_ad_count > 10 else 'balanced'
        else:
            result['paid_vs_organic'] = 'mostly_organic'

        # Affiliate program detection
        combined_text = json.dumps(all_data, default=str).lower()
        result['has_affiliate_program'] = any(kw in combined_text for kw in ['affiliate', 'afiliasi', 'referral', 'komisi'])

        # Telegram community
        result['has_telegram_community'] = any(kw in combined_text for kw in ['t.me/', 'telegram', 'join group'])

        # Email list
        result['has_email_list'] = any(kw in combined_text for kw in ['newsletter', 'email list', 'subscribe', 'berlangganan'])

        # SEO presence
        if tech.get('framework') in ('WordPress', 'Next.js', 'Nuxt.js'):
            result['seo_presence'] = 'strong'
        elif tech.get('hosting') != 'unknown':
            result['seo_presence'] = 'weak'
        else:
            result['seo_presence'] = 'none'

        # Influencer marketing
        result['influencer_marketing'] = any(kw in combined_text for kw in ['collab', 'kolaborasi', 'influencer', 'kol', 'endorsement'])

        # Budget estimate from ads data
        ads_intel = all_data.get('ads_intel', {})
        if ads_intel.get('budget_estimate'):
            result['promotion_budget_estimate'] = ads_intel['budget_estimate']
        elif fb_ad_count > 10:
            result['promotion_budget_estimate'] = 'medium (5-20M)'
        elif fb_ad_count > 0:
            result['promotion_budget_estimate'] = 'low (<5M/month)'
        else:
            result['promotion_budget_estimate'] = 'low (<5M/month)'

        # Growth strategy inference
        if result['paid_vs_organic'] == 'mostly_paid':
            result['growth_strategy'] = 'paid_acquisition'
        elif result['has_affiliate_program']:
            result['growth_strategy'] = 'affiliate_viral'
        elif result['has_telegram_community']:
            result['growth_strategy'] = 'community_led'
        elif len(result['active_channels']) >= 3:
            result['growth_strategy'] = 'multi_channel_organic'
        else:
            result['growth_strategy'] = 'single_channel_organic'

    except Exception as e:
        result['error'] = str(e)[:200]

    return result


# ─── Module: REVENUE INTELLIGENCE ───────────────────────────────────────────

def revenue_intelligence(all_data: dict, target_name: str) -> dict:
    """Synthesize revenue intelligence from all modules."""
    result = {
        'module': 'revenue_intelligence',
        'target': target_name,
        'revenue_sources': [],
        'total_revenue_estimate': {'low': 0, 'mid': 0, 'high': 0},
        'unit_economics': {
            'cac_estimate_idr': 0,
            'ltv_estimate_idr': 0,
            'ltv_cac_ratio': 0,
        },
        'revenue_model_score': 0,
        'key_revenue_drivers': [],
        'revenue_risks': [],
    }

    try:
        social = all_data.get('social', {})
        funnel = all_data.get('funnel', {})
        lynk = all_data.get('lynk', {})
        gumroad = all_data.get('gumroad', {})
        ads = all_data.get('ads', {}) or all_data.get('ads_intel', {})
        bm = all_data.get('business_model', {})
        content_intel = all_data.get('content_intel', {})
        revenue_old = all_data.get('revenue', {})

        total_low = 0
        total_mid = 0
        total_high = 0

        # --- Source 1: Ads-based traffic estimation ---
        fb_ads = {}
        if isinstance(ads, dict):
            fb_ads = ads.get('fb_ads', ads.get('facebook_ads', {}))
        fb_count = fb_ads.get('count', fb_ads.get('active_ads_found', 0)) if isinstance(fb_ads, dict) else 0

        if fb_count > 0:
            # Estimate: each ad generates ~500-2000 clicks/month
            traffic_low = fb_count * 500
            traffic_high = fb_count * 2000
            avg_price = 75000  # IDR default

            # Try to get real price from funnel/bm
            if funnel.get('pricing'):
                try:
                    prices = funnel['pricing']
                    vals = [float(p.replace('.', '').replace(',', '')) for p in prices[:5] if p.replace('.', '').replace(',', '').isdigit()]
                    if vals:
                        avg_price = sum(vals) / len(vals)
                except Exception:
                    pass

            cvr = 0.005  # 0.5% CVR
            rev_low = int(traffic_low * cvr * avg_price)
            rev_high = int(traffic_high * cvr * avg_price)
            result['revenue_sources'].append({
                'source': 'paid_ads_traffic',
                'estimated_monthly_idr': int((rev_low + rev_high) / 2),
                'confidence': 'medium',
            })
            total_low += rev_low
            total_high += rev_high

        # --- Source 2: LYNK products ---
        if lynk.get('products'):
            products = lynk['products']
            avg_price = 75000
            try:
                price_vals = []
                for p in products:
                    px = p.get('price', '').replace('Rp', '').replace('.', '').replace(',', '').strip()
                    if px.isdigit():
                        price_vals.append(float(px))
                if price_vals:
                    avg_price = sum(price_vals) / len(price_vals)
            except Exception:
                pass

            # Conservative: 50 sales/month per product
            sales_per_product = 50
            rev = int(len(products) * sales_per_product * avg_price)
            result['revenue_sources'].append({
                'source': 'lynk_products',
                'estimated_monthly_idr': rev,
                'confidence': 'low',
            })
            total_low += int(rev * 0.5)
            total_high += int(rev * 2)

        # --- Source 3: Gumroad ---
        if gumroad.get('products'):
            for p in gumroad['products']:
                try:
                    price_usd = float(p.get('price', '$0').replace('$', '').replace(',', ''))
                    reviews = p.get('reviews', 0)
                    sales_est = reviews * 10
                    rev_usd = price_usd * sales_est
                    rev_idr = int(rev_usd * 16000)  # approx IDR conversion
                    result['revenue_sources'].append({
                        'source': f'gumroad_{p.get("name", "unknown")[:30]}',
                        'estimated_monthly_idr': int(rev_idr / 12),
                        'confidence': 'medium',
                    })
                    total_low += int(rev_idr / 12 * 0.5)
                    total_high += int(rev_idr / 12 * 2)
                except Exception:
                    pass

        # --- Source 4: Bot subscriptions ---
        bot = all_data.get('bot', {})
        if bot and isinstance(bot, dict):
            # Estimate subscribers from social engagement
            tt_data = content_intel.get('tiktok', {}) or social.get('platforms', {}).get('tiktok', {})
            followers = tt_data.get('followers', tt_data.get('follower_count', 0))
            if followers > 0:
                # Rough: followers / 5 = potential bot users
                bot_users = max(followers // 5, 100)
                # Assume subscription ~50K IDR/month, 10% conversion
                rev = int(bot_users * 0.1 * 50000)
                result['revenue_sources'].append({
                    'source': 'bot_subscriptions',
                    'estimated_monthly_idr': rev,
                    'confidence': 'low',
                })
                total_low += int(rev * 0.3)
                total_high += int(rev * 3)

        # Total
        total_mid = int((total_low + total_high) / 2)
        result['total_revenue_estimate'] = {
            'low': f'IDR {total_low:,.0f}',
            'mid': f'IDR {total_mid:,.0f}',
            'high': f'IDR {total_high:,.0f}',
        }

        # Unit economics
        ads_spend = 0
        if isinstance(fb_ads, dict):
            ads_spend = fb_ads.get('estimated_spend_idr', 0)
        if ads_spend > 0 and fb_count > 0:
            traffic = fb_count * 1000  # mid estimate
            conversions = int(traffic * 0.005)
            cac = int(ads_spend / max(conversions, 1))
            avg_price_val = 75000
            if funnel.get('pricing'):
                try:
                    vals = [float(p.replace('.', '').replace(',', '')) for p in funnel['pricing'][:5]
                            if p.replace('.', '').replace(',', '').isdigit()]
                    if vals:
                        avg_price_val = sum(vals) / len(vals)
                except Exception:
                    pass
            ltv = int(avg_price_val * 3)  # assume 3 purchases lifetime
            result['unit_economics'] = {
                'cac_estimate_idr': cac,
                'ltv_estimate_idr': ltv,
                'ltv_cac_ratio': round(ltv / max(cac, 1), 2),
            }

        # Revenue model score
        score = 0
        if len(result['revenue_sources']) >= 3:
            score += 3
        elif len(result['revenue_sources']) >= 1:
            score += 1
        if total_mid > 10000000:
            score += 3
        elif total_mid > 1000000:
            score += 2
        if result['unit_economics'].get('ltv_cac_ratio', 0) > 3:
            score += 2
        elif result['unit_economics'].get('ltv_cac_ratio', 0) > 1:
            score += 1
        bm_type = bm.get('business_model_type', '')
        if bm_type in ('saas', 'bot_subscription'):
            score += 2  # recurring revenue
        elif bm_type == 'freemium':
            score += 1
        result['revenue_model_score'] = min(10, score)

        # Key revenue drivers
        drivers = []
        sorted_sources = sorted(result['revenue_sources'], key=lambda x: x.get('estimated_monthly_idr', 0), reverse=True)
        for s in sorted_sources[:3]:
            drivers.append(s['source'])
        result['key_revenue_drivers'] = drivers

        # Revenue risks
        risks = []
        if result['paid_vs_organic'] if 'paid_vs_organic' in result else all_data.get('promotion', {}).get('paid_vs_organic') == 'mostly_paid':
            risks.append('Heavy reliance on paid ads - vulnerable to ad cost increases')
        if len(result['revenue_sources']) <= 1:
            risks.append('Single revenue source - no diversification')
        if total_mid < 5000000:
            risks.append('Low estimated revenue - may not be sustainable')
        if not risks:
            risks = ['No critical risks identified from available data']
        result['revenue_risks'] = risks[:3]

    except Exception as e:
        result['error'] = str(e)[:200]

    return result


# ─── Module: MARKET OPPORTUNITY SPY ─────────────────────────────────────────

def market_opportunity_spy(target_data: dict, our_assets: dict = None) -> dict:
    """Identify top market opportunities based on competitor data and our assets."""
    if our_assets is None:
        our_assets = {
            "tools": ["PostBridge", "Kling AI", "KlingBot", "vidabot clone capability"],
            "skills": ["bot development", "AI video gen", "content creation", "Telegram bots"],
            "audience": ["TikTok", "Telegram", "Instagram"],
            "budget": "low (< IDR 5M/month)",
        }

    result = {
        'module': 'market_opportunity_spy',
        'our_assets': our_assets,
        'opportunities': [],
    }

    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="http://localhost:20128/v1",
            api_key=os.environ.get('OMNIROUTE_KEY', 'omniroute')
        )

        # Build a summary of competitor data for the prompt
        data_summary = {}
        for key in ['social', 'funnel', 'lynk', 'gumroad', 'business_model', 'ads_intel',
                     'landing_page', 'content_intel', 'promotion', 'revenue_intel', 'revenue', 'tech', 'bot']:
            val = target_data.get(key)
            if val and isinstance(val, dict):
                # Trim large nested data
                trimmed = {}
                for k, v in val.items():
                    if k.startswith('_') or k == 'html':
                        continue
                    if isinstance(v, str) and len(v) > 300:
                        trimmed[k] = v[:300]
                    elif isinstance(v, list) and len(v) > 10:
                        trimmed[k] = v[:10]
                    else:
                        trimmed[k] = v
                data_summary[key] = trimmed

        prompt = (
            f"Based on this competitor intelligence data and our assets, identify the TOP 5 market opportunities.\n\n"
            f"COMPETITOR DATA:\n{json.dumps(data_summary, indent=2, default=str)[:6000]}\n\n"
            f"OUR ASSETS:\n{json.dumps(our_assets, indent=2)}\n\n"
            "Return ONLY a valid JSON array of 5 objects, each with:\n"
            '- opportunity: string (short description)\n'
            '- effort: "low" | "medium" | "high"\n'
            '- time_to_revenue: "1 week" | "1 month" | "3 months"\n'
            '- revenue_potential_idr: number (monthly IDR estimate)\n'
            '- risk: "low" | "medium" | "high"\n'
            '- why_we_can_win: string\n'
            '- next_action: string\n\n'
            'Sort by: highest revenue_potential * (1/effort) * (1/time). Return ONLY the JSON array.'
        )

        resp = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'system', 'content': 'You are a business strategist for an Indonesian digital product company. Return only valid JSON arrays.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.4,
            max_tokens=2000,
        )

        raw = resp.choices[0].message.content.strip()
        if raw.startswith('```'):
            raw = raw.split('\n', 1)[1] if '\n' in raw else raw[3:]
            if raw.endswith('```'):
                raw = raw[:-3]
        opportunities = json.loads(raw)

        if isinstance(opportunities, list):
            # Sort by score: revenue_potential * (1/effort_score) * (1/time_score)
            effort_map = {'low': 1, 'medium': 2, 'high': 3}
            time_map = {'1 week': 1, '1 month': 2, '3 months': 3}

            for opp in opportunities:
                rev = opp.get('revenue_potential_idr', 0)
                eff = effort_map.get(opp.get('effort', 'high'), 3)
                tm = time_map.get(opp.get('time_to_revenue', '3 months'), 3)
                opp['_score'] = rev / max(eff * tm, 1)

            opportunities.sort(key=lambda x: x.get('_score', 0), reverse=True)

            # Remove internal score
            for opp in opportunities:
                opp.pop('_score', None)

            result['opportunities'] = opportunities[:5]

    except Exception as e:
        result['error'] = str(e)[:200]
        # Fallback static opportunities
        result['opportunities'] = [
            {
                'opportunity': 'Clone competitor bot with improvements',
                'effort': 'medium',
                'time_to_revenue': '1 month',
                'revenue_potential_idr': 5000000,
                'risk': 'low',
                'why_we_can_win': 'We have bot development skills and can fix their UX issues',
                'next_action': 'Use bot-extractor to map their bot, then build improved version',
            }
        ]

    return result


# ─── Main Orchestrator ───────────────────────────────────────────────────────

async def run_spy(target: str, modules: list, mode: str = 'report', url: str = None) -> dict:
    """Run selected intelligence modules."""
    all_data = {}
    print(f'🕵️ Starting intelligence gathering on: {target}')
    print(f'   Modules: {modules}')
    if url:
        print(f'   URL: {url}')
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

    # ── New deep intelligence modules ──

    # Infer URL if not provided
    target_url = url
    if not target_url:
        clean = target.lstrip('@').replace('_bot', '').replace('_', '')
        # Try to infer from lynk or funnel entry points
        if all_data.get('lynk', {}).get('products'):
            target_url = f'https://lynk.id/{clean}'
        elif all_data.get('funnel', {}).get('entry_points'):
            for ep in all_data['funnel']['entry_points']:
                if ep.get('status') == 'found':
                    target_url = ep.get('url', '')
                    break
        if not target_url:
            target_url = f'https://{clean}'

    # Landing Page Deep Spy
    if 'landing_page' in modules:
        print('🔍 Landing Page Deep Spy...')
        try:
            all_data['landing_page'] = await landing_page_deep_spy(target_url)
            lp = all_data['landing_page']
            print(f'   H1: {lp.get("h1", "?")[:60]} | Funnel: {lp.get("funnel_guess", "?")} | Load: {lp.get("page_load_time_ms", 0)}ms')
        except Exception as e:
            print(f'   Landing page spy error: {e}')
            all_data['landing_page'] = {'error': str(e)[:200]}

    # Business Model Spy
    if 'business_model' in modules:
        print('🏢 Business Model Spy...')
        try:
            all_data['business_model'] = await business_model_spy(target_url, target)
            bm = all_data['business_model']
            print(f'   Type: {bm.get("business_model_type", "?")} | Score: {bm.get("revenue_model_score", 0)}/10')
        except Exception as e:
            print(f'   Business model spy error: {e}')
            all_data['business_model'] = {'error': str(e)[:200]}

    # Ads Intelligence Spy
    if 'ads_intel' in modules:
        print('📊 Ads Intelligence Spy...')
        try:
            all_data['ads_intel'] = await ads_intelligence_spy(target)
            ai = all_data['ads_intel']
            print(f'   FB ads: {ai.get("fb_ads", {}).get("count", 0)} | Budget: {ai.get("budget_estimate", "?")}')
        except Exception as e:
            print(f'   Ads intelligence spy error: {e}')
            all_data['ads_intel'] = {'error': str(e)[:200]}

    # Content Intelligence Spy
    if 'content_intel' in modules:
        print('📝 Content Intelligence Spy...')
        try:
            # Build handles from social data and lynk data
            handles = {}
            clean_target = target.lstrip('@').replace('_bot', '')
            handles['tiktok'] = f'@{clean_target}'

            # Try to get handles from lynk social links
            for sl in all_data.get('lynk', {}).get('social_links', []):
                plat = sl.get('platform', '')
                handle = sl.get('handle', '')
                if plat and handle:
                    handles[plat] = f'@{handle.lstrip("@")}'

            # Defaults if not found
            if 'instagram' not in handles:
                handles['instagram'] = f'@{clean_target}'
            if 'youtube' not in handles:
                handles['youtube'] = f'@{clean_target}'

            all_data['content_intel'] = await content_intelligence_spy(handles)
            ci = all_data['content_intel']
            cs = ci.get('content_strategy', {})
            print(f'   Primary: {cs.get("primary_platform", "?")} | Hooks: {len(cs.get("viral_hooks", []))}')
        except Exception as e:
            print(f'   Content intelligence spy error: {e}')
            all_data['content_intel'] = {'error': str(e)[:200]}

    # Promotion Strategy Spy
    if 'promotion' in modules:
        print('📣 Promotion Strategy Spy...')
        try:
            all_data['promotion'] = promotion_strategy_spy(target, all_data)
            ps = all_data['promotion']
            print(f'   Strategy: {ps.get("growth_strategy", "?")} | Channels: {", ".join(ps.get("active_channels", []))}')
        except Exception as e:
            print(f'   Promotion spy error: {e}')
            all_data['promotion'] = {'error': str(e)[:200]}

    # Revenue Intelligence
    if 'revenue_intel' in modules:
        print('💎 Revenue Intelligence...')
        try:
            all_data['revenue_intel'] = revenue_intelligence(all_data, target)
            ri = all_data['revenue_intel']
            est = ri.get('total_revenue_estimate', {})
            print(f'   Estimate: {est.get("low", "?")} - {est.get("high", "?")} | Score: {ri.get("revenue_model_score", 0)}/10')
        except Exception as e:
            print(f'   Revenue intelligence error: {e}')
            all_data['revenue_intel'] = {'error': str(e)[:200]}

    # Market Opportunity Spy
    if 'market_opportunity' in modules:
        print('🎯 Market Opportunity Spy...')
        try:
            all_data['market_opportunity'] = market_opportunity_spy(all_data)
            mo = all_data['market_opportunity']
            opps = mo.get('opportunities', [])
            print(f'   Opportunities found: {len(opps)}')
            for i, opp in enumerate(opps[:3], 1):
                print(f'   {i}. {opp.get("opportunity", "?")[:60]} (IDR {opp.get("revenue_potential_idr", 0):,}/mo)')
        except Exception as e:
            print(f'   Market opportunity spy error: {e}')
            all_data['market_opportunity'] = {'error': str(e)[:200]}

    return all_data


async def main():
    parser = argparse.ArgumentParser(description='Business Intelligence & Espionage')
    parser.add_argument('--target', required=True, help='Target: URL, @bot, or business name')
    parser.add_argument('--modules', default='social,tech,funnel,revenue,model',
                        help='Comma-separated modules')
    parser.add_argument('--all', action='store_true', help='Run all modules')
    parser.add_argument('--mode', default='report', choices=['report', 'clone', 'improve'])
    parser.add_argument('--output', help='Output file (JSON or MD)')
    parser.add_argument('--url', help='Landing page URL for deep analysis')
    parser.add_argument('--compare', help='Compare with own business URL')
    args = parser.parse_args()

    modules = ALL_MODULES if args.all else args.modules.split(',')

    # Run
    all_data = await run_spy(args.target, modules, args.mode, url=getattr(args, 'url', None))

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
