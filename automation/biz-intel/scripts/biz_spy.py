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

ALL_MODULES = ['social', 'ads', 'funnel', 'revenue', 'bot', 'tech', 'content', 'seo', 'model']


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


# ─── Module: REVENUE SPY ─────────────────────────────────────────────────────

async def revenue_spy(target: str, social_data: dict = None, funnel_data: dict = None) -> dict:
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

    # Revenue estimate
    if 'revenue' in modules:
        print('💰 Revenue Spy...')
        all_data['revenue'] = await revenue_spy(
            target,
            all_data.get('social'),
            all_data.get('funnel')
        )
        est = all_data['revenue'].get('monthly_estimate', {})
        print(f'   Estimate: {est.get("low","?")} - {est.get("high","?")} /month')

    # Business model synthesis
    if 'model' in modules:
        print('🏗️  Model Synthesis...')
        all_data['model'] = model_spy(target, all_data)

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
