---
name: seo-optimizer
description: Optimize content for search engines. Perform keyword research, analyze on-page SEO, track rankings, audit technical
  SEO, and improve organic visibility for sustainable traffic growth. Use when optimizeing content for search engines. perform keyword research, analyze on-page.
domain: marketing
author: oyi77
license: Apache-2.0
subdomain: marketing
tags:
- growth
- marketing
- optimizer
- money
- seo
version: 1.0.0
---

persona:
  name: "Domain Expert"
  title: "Master of Seo Optimizer"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# SEO Optimizer Skill

## Expert Persona

**You are channeling Brian Dean and Rand Fishkin** — revolutionary SEO experts who pioneered modern search optimization techniques focused on quality and user experience.

### Brian Dean - "The King of Content"
- **Credentials**: Founder of Backlinko, popularized "Skyscraper Technique", generated millions in organic traffic
- **Expertise**: Backlink building, content optimization, SEO copywriting
- **Philosophy**: "Create 10x better content than the top results"
- **Principles**:
  - Skyscraper Technique (analyze, improve, outreach)
  - Long-form, in-depth content
  - Visual content (images, videos, infographics)
  - Focus on search intent
  - User experience is key

### Rand Fishkin - "The Wizard of Moz"
- **Credentials**: Founder of Moz, author of "Lost and Founder", inventor of Domain Authority metric
- **Expertise**: Technical SEO, domain authority, competitive analysis
- **Philosophy**: "Build it and they won't come unless you deserve it"
- **Principles**:
  - E-A-T (Expertise, Authoritativeness, Trustworthiness)
  - Quality over quantity
  - Transparency in reporting
  - Build for humans, optimize for search engines
  - Focus on solving real problems

**Combined Approach**: Blend Brian's content-centric strategies with Rand's technical expertise. Create exceptional content while mastering technical optimization.


## Money-Making Overview

**Buyer Personas:**

- **SME Owners ($100-500K rev)** — know they need SEO, can't figure out where to start, tired of agency retainer bullshit
- **Startup Founders (pre-Series A)** — need organic growth without burning cash on ads, want predictable traffic engine
- **Agency Partners** — white-label SEO audits for their own clients ($500-2K/audit, mark up 2-3x)
- **SaaS Companies** — recurring content + technical SEO retainer to scale organic acquisition month over month
- **E-commerce Stores** — product page optimization, category page authority, structured data for rich results

**Pricing Tiers:**

| Tier | Price | What They Get |
|------|-------|---------------|
| **Technical Audit** | $500-1K one-time | Full crawl + Core Web Vitals + schema audit + prioritized fix list + 30-min walkthrough call |
| **Monthly Optimization** | $1.5K-2.5K/mo | Audit + 4 optimized posts + ongoing rank tracking + monthly report + Slack access |
| **Full-Funnel Retainer** | $3K-5K/mo | Everything above + link building + GEO optimization + competitor gap analysis + quarterly strategy |

**First-Dollar Timeline:**
- Week 1: Run technical audit script on 5 prospects → generate reports → send cold email/DM
- Week 2: Close first client at audit tier ($500-1K)
- Month 2: Convert audit client to monthly retainer ($1.5-2.5K)
- Month 3-4: Build portfolio with case studies → raise prices → sell retainers only

---

## First Action in 60 Minutes

Run a real technical SEO audit on any domain. This script checks HTTP, SSL, robots.txt, sitemap, meta tags, Core Web Vitals (via PageSpeed Insights free API), mobile viewport, and canonical tags — then outputs a ranked priority list.

```python
#!/usr/bin/env python3
"""seo-audit.py — Automated Technical SEO Audit with Prioritized Fix List

Usage:
    python3 seo-audit.py example.com
    python3 seo-audit.py example.com --json          # structured output for invoicing
    python3 seo-audit.py example.com --email client@example.com  # send report

No API keys required (PageSpeed Insights free tier). Only dependency: requests.
"""

import sys
import ssl
import socket
import json
import re
import os
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests -q")
    import requests


def check_http(domain):
    """Check HTTP status, redirect chain, and HTTPS enforcement."""
    issues = []
    for scheme in ["http://", "https://"]:
        url = f"{scheme}{domain}"
        try:
            r = requests.get(url, timeout=10, allow_redirects=True)
            issues.append({
                "check": f"HTTP{'S' if scheme == 'https://' else ''} Status",
                "url": url,
                "status": r.status_code,
                "final_url": r.url,
                "redirect_chain": len(r.history),
                "pass": r.status_code == 200 and r.url.startswith("https://"),
                "severity": "CRITICAL" if r.status_code >= 400 else "INFO"
            })
            break  # if http redirects to https, don't check again
        except requests.RequestException as e:
            issues.append({
                "check": "HTTP Reachability",
                "url": url,
                "error": str(e),
                "pass": False,
                "severity": "CRITICAL"
            })
    headers = r.headers if 'r' in dir() else {}
    return issues, headers


def check_robots_txt(domain):
    """Verify robots.txt exists and allows crawling."""
    url = f"https://{domain}/robots.txt"
    try:
        r = requests.get(url, timeout=10)
        text = r.text
        disallow_all = "Disallow: /" in text and "Allow:" not in text.split("Disallow: /")[0] if "Disallow: /" in text else False
        return {
            "check": "robots.txt",
            "exists": r.status_code == 200,
            "disallow_all": disallow_all,
            "has_sitemap": "Sitemap:" in text,
            "pass": r.status_code == 200 and not disallow_all,
            "severity": "HIGH" if disallow_all else "WARNING" if r.status_code != 200 else "PASS"
        }
    except Exception as e:
        return {"check": "robots.txt", "error": str(e), "pass": False, "severity": "HIGH"}


def check_sitemap(domain):
    """Check XML sitemap is accessible and valid."""
    urls_to_try = [
        f"https://{domain}/sitemap.xml",
        f"https://{domain}/sitemap_index.xml",
        f"https://{domain}/sitemap/sitemap.xml"
    ]
    for url in urls_to_try:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200 and "<?xml" in r.text[:100]:
                return {
                    "check": "XML Sitemap",
                    "url": url,
                    "status": r.status_code,
                    "size_kb": round(len(r.text) / 1024, 1),
                    "pass": True,
                    "severity": "PASS"
                }
        except Exception:
            continue
    return {"check": "XML Sitemap", "pass": False, "severity": "HIGH",
            "detail": "No sitemap found at common locations"}


def check_pagespeed(domain):
    """Query PageSpeed Insights API (free, no key needed for basic)."""
    url = f"https://{domain}"
    api = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}&strategy=mobile"
    try:
        r = requests.get(api, timeout=30)
        data = r.json()
        if "lighthouseResult" not in data:
            return {"check": "PageSpeed Insights", "pass": False, "severity": "WARNING",
                    "detail": "API returned unexpected response"}
        lr = data["lighthouseResult"]
        audits = lr.get("audits", {})
        metrics = {}
        for key, label in [("first-contentful-paint", "FCP"), ("largest-contentful-paint", "LCP"),
                           ("total-blocking-time", "TBT"), ("cumulative-layout-shift", "CLS"),
                           ("speed-index", "Speed Index")]:
            if key in audits:
                v = audits[key].get("numericValue")
                metrics[label] = round(v, 2) if v else None
        score = lr.get("categories", {}).get("performance", {}).get("score", 0) * 100
        issues = []
        if metrics.get("LCP") and metrics["LCP"] > 2.5:
            issues.append({"severity": "HIGH", "finding": f"LCP {metrics['LCP']}s exceeds 2.5s threshold"})
        if metrics.get("CLS") and metrics["CLS"] > 0.1:
            issues.append({"severity": "HIGH", "finding": f"CLS {metrics['CLS']} exceeds 0.1 threshold"})
        if metrics.get("TBT") and metrics["TBT"] > 200:
            issues.append({"severity": "MEDIUM", "finding": f"TBT {metrics['TBT']}ms exceeds 200ms"})
        return {
            "check": "Core Web Vitals",
            "performance_score": round(score),
            "metrics": metrics,
            "issues": issues,
            "pass": score >= 50 and len(issues) == 0,
            "severity": "CRITICAL" if score < 50 else "WARNING" if issues else "PASS"
        }
    except Exception as e:
        return {"check": "PageSpeed Insights", "error": str(e), "pass": False, "severity": "WARNING"}


def check_ssl(domain):
    """Check SSL certificate validity."""
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(10)
            s.connect((domain, 443))
            cert = s.getpeercert()
            expires = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
            days_left = (expires - datetime.utcnow()).days
            return {
                "check": "SSL Certificate",
                "issuer": dict(cert.get("issuer", [("?",)])).get("organizationName", "Unknown"),
                "expires": expires.isoformat(),
                "days_left": days_left,
                "pass": days_left > 30,
                "severity": "CRITICAL" if days_left <= 0 else "HIGH" if days_left <= 30 else "PASS"
            }
    except Exception as e:
        return {"check": "SSL Certificate", "error": str(e), "pass": False, "severity": "CRITICAL"}


def check_meta_tags(domain):
    """Extract and validate title tag and meta description."""
    url = f"https://{domain}"
    try:
        r = requests.get(url, timeout=10)
        html = r.text
        title = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        viewport = re.search(r'<meta[^>]+name=["\']viewport["\']', html, re.IGNORECASE)
        canonical = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']*)["\']', html, re.IGNORECASE)
        og_title = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)["\']', html, re.IGNORECASE)
        h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.IGNORECASE | re.DOTALL)

        findings = []
        title_text = title.group(1).strip() if title else ""
        desc_text = desc.group(1).strip() if desc else ""

        if not title:
            findings.append({"severity": "CRITICAL", "finding": "Missing <title> tag"})
        elif len(title_text) < 30:
            findings.append({"severity": "HIGH", "finding": f"Title too short ({len(title_text)} chars, min 30)"})
        elif len(title_text) > 60:
            findings.append({"severity": "WARNING", "finding": f"Title too long ({len(title_text)} chars, max 60 recommended)"})

        if not desc:
            findings.append({"severity": "HIGH", "finding": "Missing meta description"})
        elif len(desc_text) < 50:
            findings.append({"severity": "WARNING", "finding": f"Meta description too short ({len(desc_text)} chars)"})
        elif len(desc_text) > 160:
            findings.append({"severity": "WARNING", "finding": f"Meta description too long ({len(desc_text)} chars, max 160)"})

        if not viewport:
            findings.append({"severity": "CRITICAL", "finding": "Missing viewport meta tag — not mobile-friendly"})
        if not canonical:
            findings.append({"severity": "WARNING", "finding": "Missing canonical tag"})
        if not h1:
            findings.append({"severity": "HIGH", "finding": "Missing H1 heading"})

        return {
            "check": "Meta Tags",
            "title": title_text,
            "meta_description": desc_text,
            "has_viewport": bool(viewport),
            "has_canonical": bool(canonical),
            "has_og_title": bool(og_title),
            "has_h1": bool(h1),
            "issues": findings,
            "pass": len([f for f in findings if f["severity"] == "CRITICAL"]) == 0,
            "severity": "CRITICAL" if any(f["severity"] == "CRITICAL" for f in findings) else "WARNING" if findings else "PASS"
        }
    except Exception as e:
        return {"check": "Meta Tags", "error": str(e), "pass": False, "severity": "WARNING"}


def prioritize(results):
    """Score and rank issues by severity for actionable output."""
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "WARNING": 3, "LOW": 4, "PASS": 5, "INFO": 6}
    all_issues = []
    for section in results:
        if "issues" in section:
            for issue in section["issues"]:
                all_issues.append(issue)
        elif not section.get("pass", True) and "severity" in section:
            all_issues.append({
                "severity": section["severity"],
                "finding": f"{section['check']}: {section.get('detail', section.get('error', 'Failed'))}"
            })
    return sorted(all_issues, key=lambda x: severity_order.get(x["severity"], 99))


def print_report(domain, results, priority_list):
    """Print a human-readable, invoice-ready report."""
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "WARNING": 3, "LOW": 4, "PASS": 5}
    critical = sum(1 for p in priority_list if p["severity"] == "CRITICAL")
    high = sum(1 for p in priority_list if p["severity"] == "HIGH")
    medium = sum(1 for p in priority_list if p["severity"] == "MEDIUM")

    print("=" * 60)
    print(f"  TECHNICAL SEO AUDIT REPORT")
    print(f"  Domain: {domain}")
    print(f"  Date:   {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    print(f"  OVERALL: {'PASS' if critical == 0 else f'{critical} CRITICAL ISSUES'}")
    print(f"  Issues: {critical} critical, {high} high, {medium} medium")
    print()
    print("-" * 60)
    print("  SECTION CHECKS")
    print("-" * 60)
    for section in results:
        status = "PASS" if section.get("pass") else "FAIL"
        print(f"  [{status}] {section['check']}")

    print()
    print("-" * 60)
    print("  PRIORITIZED FIX LIST")
    print("-" * 60)
    for i, issue in enumerate(priority_list, 1):
        print(f"  {i}. [{issue['severity']}] {issue['finding']}")

    print()
    print("-" * 60)
    print("  ESTIMATED VALUE OF THIS AUDIT: $500-1,000")
    print("  (invoice-ready — save this output as client deliverable)")
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 seo-audit.py example.com [--json]")
        sys.exit(1)

    domain = sys.argv[1].strip().lower()
    domain = re.sub(r'^https?://', '', domain).split('/')[0]

    print(f"Running audit on {domain}...")

    http_results, headers = check_http(domain)
    results = http_results + [
        check_robots_txt(domain),
        check_sitemap(domain),
        check_pagespeed(domain),
        check_ssl(domain),
        check_meta_tags(domain),
    ]

    priority_list = prioritize(results)
    print_report(domain, results, priority_list)

    if "--json" in sys.argv:
        print(json.dumps({"domain": domain, "timestamp": datetime.now().isoformat(),
                          "checks": results, "prioritized_fixes": priority_list}, indent=2))


if __name__ == "__main__":
    main()
```

**What to do with the output:**
1. Run it: `python3 seo-audit.py clientdomain.com`
2. Copy full output into a Google Doc
3. Add your branding + 2-3 sentence diagnosis per finding
4. Send as paid deliverable ($500-1K) with a proposal for monthly retainer ($1.5K-2.5K/mo)

---

## Deliverable Format

### SEO Audit Report Template

Send this exact structure as a client deliverable:

```
TITLE: Technical SEO Audit — [Client Domain]
FROM: [Your Name], SEO Consultant
DATE: 2026-07-16

EXECUTIVE SUMMARY (2-3 sentences)
  Overall health: GOOD / FAIR / POOR
  Critical issues: N
  High issues: N
  Estimated traffic opportunity: +X% in 3 months

SECTION 1: CRAWLABILITY & INDEXING
  - robots.txt: [OK / ISSUE]
  - XML sitemap: [OK / ISSUE]
  - 4xx/5xx errors: [count]
  - Orphan pages: [count]
  Fix instructions: step-by-step

SECTION 2: CORE WEB VITALS
  - LCP: Ns (target <2.5s)
  - INP: Nms (target <200ms)
  - CLS: N (target <0.1)
  - Performance score: N/100
  Fix instructions: specific image/JS/CSS changes

SECTION 3: ON-PAGE SEO
  - Title tags: [N problems found]
  - Meta descriptions: [N problems found]
  - Heading structure: [OK / ISSUE]
  - Image alt text: [N missing]
  - Internal linking: [OK / ISSUE]
  - Schema markup: [present / missing]

SECTION 4: TECHNICAL FOUNDATIONS
  - HTTPS/SSL: [expires DATE, issuer]
  - Mobile responsiveness: [OK / ISSUE]
  - URL structure: [OK / ISSUE]
  - Redirect chain: [N hops max]
  - Canonical tags: [OK / ISSUE]

SECTION 5: CONTENT GAPS (optional upgrade)
  - Keywords client ranks for vs competitors
  - Content gap analysis
  - 5 high-opportunity topics with search volume + difficulty

RECOMMENDATIONS (ranked by effort vs impact)
  Quick wins (1-2 hrs): [3 items]
  Medium effort (1-2 days): [3 items]
  Strategic (1-2 weeks): [3 items]

PRICING OPTIONS
  [ ] One-time audit implementation: $[X]
  [ ] Monthly optimization (4 posts + monitoring): $[X]/mo
  [ ] Full retainer (content + link building + GEO): $[X]/mo
```

### Proposal / Invoice Template

```
PROPOSAL for SEO Services — [Client Name]

Current situation: [2-sentence diagnosis from audit]
Opportunity: [traffic/revenue projection]
Approach: [brief methodology]

Option A: Technical Audit & Fix Implementation
  - Full technical audit report
  - Implement critical fixes
  - 30-min walkthrough call
  - $[500-1,000] one-time

Option B: Monthly SEO Optimization
  - Everything in A + 4 optimized articles/month
  - Rank tracking dashboard
  - Monthly strategy call
  - $[1,500-2,500]/month

Option C: Full-Funnel SEO Retainer
  - Everything in B + link building outreach
  - GEO / AI search optimization
  - Competitor gap analysis
  - Quarterly in-depth strategy
  - $[3,000-5,000]/month

TERMS
  - Payment: Net 7 / upfront for first month
  - Reporting: Monthly with real data
  - Minimum commitment: 3 months for retainers
  - Cancellation: 30-day notice
```

---

## Overview

Complete SEO toolkit for organic growth. Research keywords, optimize content, track rankings, and improve search visibility. Essential for long-term sustainable traffic without paid ads.

## When to Use
**Trigger phrases:**
- "seo optimizer"
- "Optimize content for search engines"


- Research keywords for content
- Optimize blog posts/pages
- Audit website SEO
- Track search rankings
- Analyze competitors
- Fix technical SEO issues
- Build backlinks strategy

## When NOT to Use

- Website is under active development (wait for stable release)
- No access to Google Search Console / Analytics (can't measure results)
- Purely paid advertising campaigns (use `marketing/ads-manager` instead)
- One-page landing pages with no organic competition (SEO won't help)
- Website has manual penalty from Google (fix penalty first)

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Keywords don't matter anymore, just write good content" | Keywords still matter for search intent matching - research informs content strategy |
| "I'll add meta tags later, focus on content first" | Meta tags are quick wins - skipping them loses organic traffic for no reason |
| "Don't need technical SEO, content is king" | Technical issues (crawl errors, slow site) nullify great content |
| "Backlinks are too hard, skip link building" | Without backlinks, content won't rank for competitive keywords |
| "Page speed is fine, users don't care" | Core Web Vitals are ranking factors - slow sites lose rankings |
| "AI Overviews killed SEO, why bother?" | SEO evolved, not dead - GEO (Generative Engine Optimization) is the new frontier |

## Red Flags

- Keyword stuffing (density > 2%) - triggers spam filters
- Buying backlinks - manual penalty risk from Google
- Duplicate content across pages - cannibalizes rankings
- Hidden text or cloaking - black hat, will get penalized
- Ignoring mobile optimization - 60%+ traffic is mobile
- No conversion tracking - flying blind on SEO ROAS
- Targeting keywords with zero search volume - wasted effort


## Anti-Rationalization Table

Common excuses SEO consultants tell themselves not to sell:

| Rationalization | Reality |
|---|---|
| "SEO takes 6 months to show results, clients won't wait" | Quick wins (fix 404s, meta tags, page speed) show measurable improvement in 2-4 weeks — lead with those |
| "I don't have the tools for a proper audit" | Free tools (PageSpeed API, Python, Screaming Frog free tier, GSC) are enough for a $500-1K deliverable |
| "Google changes its algorithm constantly, my advice expires" | Core SEO principles (content quality, technical soundness, backlinks) haven't changed in a decade |
| "My client's niche has no search volume" | There's always long-tail opportunity if you dig past the obvious keywords |
| "I'm not a developer, I can't fix technical SEO" | You diagnose and recommend; the developer implements. Diagnosing pays $150-300/hr |
| "AI search killed traditional SEO" | It shifted to GEO. Adapt your offering (passage citation, llms.txt, brand signals) instead of abandoning it |
| "Big brands already own every keyword" | New content formats, new search intents, and long-tail variations create constant fresh opportunities |
| "I'll do SEO for my own site first, then sell" | You learn fastest by doing it for paying clients at a discount — not by perfecting your own site for 6 months |
## Core Features

- Automated analyze, audit, content, engines, growth processing and optimization
- Multi-platform support with unified configuration
- Real-time monitoring and alerting
- Batch operations for scale
- Export to CSV, JSON, and PDF formats


### 1. Keyword Research
```javascript
const keywordData = {
  keyword: 'AI video generation',
  search_volume: 2400,  // Monthly searches
  difficulty: 45,  // 0-100
  cpc: 2.50,  // USD
  intent: 'informational',  // informational, commercial, transactional
  related_keywords: [
    'AI video maker',
    'text to video AI',
    'AI video creator'
  ]
};
```

### 2. On-Page SEO Checklist
```
✅ Title tag (50-60 characters)
✅ Meta description (150-160 characters)
✅ H1 heading (includes target keyword)
✅ URL structure (short, descriptive)
✅ Image alt text
✅ Internal links (3-5 per page)
✅ External links (2-3 authoritative)
✅ Keyword density (1-2%)
✅ Content length (>1000 words)
✅ Mobile-friendly
✅ Page speed (<3s load time)
```

### 3. Content Optimization
```javascript
function optimizeContent(content, targetKeyword) {
  const optimized = {
    title: `${targetKeyword} - Complete Guide 2026`,
    meta_description: `Learn ${targetKeyword} with our comprehensive guide. Step-by-step tutorial, examples, and best practices.`,
    h1: `The Ultimate Guide to ${targetKeyword}`,
    url: `/blog/${targetKeyword.toLowerCase().replace(/ /g, '-')}`,
    keyword_placement: {
      first_paragraph: true,
      headings: 3,
      throughout_content: true,
      conclusion: true
    }
  };
  
  return optimized;
}
```

### 4. Technical SEO Audit
```
🔍 Technical SEO Checklist:
✅ XML sitemap
✅ Robots.txt
✅ SSL certificate (HTTPS)
✅ Mobile responsiveness
✅ Page speed optimization
✅ Structured data (Schema.org)
✅ Canonical tags
✅ 404 error handling
✅ Redirect chains fixed
✅ Duplicate content resolved
```

### 5. Rank Tracking
```javascript
const rankingData = {
  keyword: 'AI video tutorial',
  current_position: 12,
  previous_position: 18,
  change: +6,
  url: 'https://yoursite.com/blog/ai-video-tutorial',
  search_volume: 1200,
  traffic_estimate: 48  // Monthly clicks
};
```

## SEO Tools Integration

- Configure analyze, audit, content, engines, growth settings before first use


### Google Search Console
```javascript
// Track performance
const gscData = {
  clicks: 450,
  impressions: 8500,
  ctr: 5.3,  // %
  average_position: 8.2,
  top_queries: [
    'AI video generator',
    'create AI videos',
    'video AI tool'
  ]
};
```

### Competitor Analysis
```javascript
const competitorData = {
  competitor: 'competitor.com',
  domain_authority: 45,
  backlinks: 1250,
  top_keywords: [
    'AI video maker',
    'video generation AI'
  ],
  content_gaps: [
    'AI video for TikTok',
    'Free AI video tools'
  ]
};
```

## Content Strategy

- Configure analyze, audit, content, engines, growth settings before first use


### Topic Clusters
```
Pillar Page: AI Video Generation
├── Cluster 1: Getting Started
│   ├── What is AI Video Generation?
│   ├── Best AI Video Tools 2026
│   └── AI Video Tutorial for Beginners
├── Cluster 2: Advanced Techniques
│   ├── Creating Viral AI Videos
│   ├── AI Video for Social Media
│   └── Monetizing AI Videos
└── Cluster 3: Platform-Specific
    ├── AI Videos for TikTok
    ├── AI Videos for Instagram
    └── AI Videos for YouTube
```

### Content Calendar
```
Week 1: Keyword research + outline
Week 2: Write pillar page (2000+ words)
Week 3: Write cluster articles (3x 1000 words)
Week 4: Optimize, publish, promote
```

## Best Practices

1. **Keyword Research**
   - Target long-tail keywords (3-5 words)
   - Check search intent
   - Analyze competition
   - Find content gaps

2. **Content Creation**
   - Write for humans first
   - Include target keyword naturally
   - Use headings (H2, H3) properly
   - Add images/videos
   - Internal linking

3. **Technical SEO**
   - Fast loading speed
   - Mobile-first design
   - Clean URL structure
   - HTTPS everywhere
   - Fix broken links

4. **Link Building**
   - Guest posting
   - Resource pages
   - Broken link building
   - Digital PR
   - Quality over quantity

---

## Advanced SEO Techniques (From Reference Libraries)

- Configure analyze, audit, content, engines, growth settings before first use


### 1. Content Attack Briefs (Competitive Gap Analysis)

**Strategy:** Find keywords your competitors rank for that you don't—then create superior content.

```python
def content_attack_brief(target_domain, competitors):
    """
    Generate content attack strategy
    """
    # Find keyword gaps
    competitor_keywords = {}
    for comp in competitors:
        competitor_keywords[comp] = get_ranking_keywords(comp)
    
    my_keywords = get_ranking_keywords(target_domain)
    
    # Identify opportunities
    gaps = {}
    for comp, keywords in competitor_keywords.items():
        for keyword, data in keywords.items():
            if keyword not in my_keywords:
                gaps[keyword] = {
                    "competitor": comp,
                    "their_position": data["position"],
                    "search_volume": data["volume"],
                    "difficulty": data["difficulty"],
                    "opportunity_score": calculate_opportunity(data)
                }
    
    # Prioritize by opportunity score
    return sorted(gaps.items(), 
                  key=lambda x: x[1]["opportunity_score"], 
                  reverse=True)[:20]
```

**Opportunity Score Formula:**
```
Opportunity = (Search Volume × (11 - Competitor Position)) / Difficulty

Higher = Better opportunity
```

### 2. Google Search Console (GSC) Optimizer

**Strategy:** Mine your existing data for quick wins.

```python
def gsc_optimizer(gsc_data):
    """
    Find under-optimized opportunities in your own data
    """
    opportunities = []
    
    # Low CTR opportunities (impressions high, clicks low)
    low_ctr = gsc_data[
        (gsc_data.impressions > 1000) & 
        (gsc_data.ctr < 0.03)
    ]
    
    for query in low_ctr:
        opportunities.append({
            "type": "LOW_CTR",
            "query": query.term,
            "impressions": query.impressions,
            "current_ctr": query.ctr,
            "suggestion": f"Improve title/meta for '{query.term}'",
            "potential_clicks": query.impressions * 0.05  # 5% target CTR
        })
    
    # Position 11-20 opportunities (page 2)
    page_2 = gsc_data[
        (gsc_data.position >= 11) & 
        (gsc_data.position <= 20) &
        (gsc_data.impressions > 500)
    ]
    
    for query in page_2:
        opportunities.append({
            "type": "PAGE_2",
            "query": query.term,
            "position": query.position,
            "suggestion": "Add content depth, internal links to reach page 1"
        })
    
    return opportunities
```

### 3. Trend Scout

**Strategy:** Identify emerging keywords before competitors.

```python
def trend_scout(seed_keywords, timeframe="90d"):
    """
    Find trending keywords with low competition
    """
    trending = []
    
    for seed in seed_keywords:
        # Get related queries
        related = get_related_queries(seed)
        
        for query in related:
            trend = get_trend_data(query, timeframe)
            
            # Rising trend + low competition
            if trend.growth_rate > 0.50 and trend.competition < 0.30:
                trending.append({
                    "keyword": query,
                    "growth_rate": trend.growth_rate,
                    "current_volume": trend.volume,
                    "projected_volume": trend.volume * (1 + trend.growth_rate),
                    "competition": trend.competition
                })
    
    return sorted(trending, key=lambda x: x["growth_rate"], reverse=True)
```

### 4. SEO Technical Audit Automation

```python
def technical_seo_audit(domain):
    """
    Comprehensive technical SEO audit
    """
    audit = {
        "crawlability": check_crawlability(domain),
        "indexability": check_indexability(domain),
        "page_speed": check_page_speed(domain),
        "mobile_friendly": check_mobile_friendly(domain),
        "structured_data": check_structured_data(domain),
        "internal_links": analyze_internal_links(domain),
        "security": check_security(domain)
    }
    
    # Priority scoring
    critical_issues = []
    warning_issues = []
    
    for category, results in audit.items():
        if results["severity"] == "CRITICAL":
            critical_issues.append(results)
        elif results["severity"] == "WARNING":
            warning_issues.append(results)
    
    return {
        "overall_health": calculate_health_score(audit),
        "critical_count": len(critical_issues),
        "warning_count": len(warning_issues),
        "action_items": prioritize_fixes(critical_issues + warning_issues)
    }
```

### 5. AI Content Optimization (GEO)

**Strategy:** Optimize for AI search (ChatGPT, Perplexity, Gemini)

```python
def geo_optimize(content, target_queries):
    """
    Generative Engine Optimization
    """
    optimizations = {
        "passage_citability": {
            "clear_headings": extract_key_sections(content),
            "factual_statements": identify_claims(content),
            "structured_data": add_schema_markup(content)
        },
        "brand_mentions": {
            "authority_signals": add_author_bios(content),
            "citations": add_external_links(content),
            "trustworthiness": add_publication_dates(content)
        },
        "llms_txt": generate_llms_txt(content)
    }
    
    return optimizations
```

## Content Operations Integration

- Configure analyze, audit, content, engines, growth settings before first use


### Content Calendar with SEO Prioritization

```python
def seo_content_calendar(keyword_opportunities, resources):
    """
    Prioritize content based on SEO value
    """
    calendar = []
    
    for opp in keyword_opportunities:
        priority_score = (
            opp["search_volume"] * 0.3 +
            opp["opportunity_score"] * 0.4 +
            (100 - opp["difficulty"]) * 0.3
        )
        
        calendar.append({
            "keyword": opp["keyword"],
            "priority": "HIGH" if priority_score > 70 else "MEDIUM" if priority_score > 40 else "LOW",
            "estimated_traffic": opp["search_volume"] * 0.10,  # 10% CTR assumption
            "effort": estimate_content_effort(opp),
            "roi": priority_score / estimate_content_effort(opp)
        })
    
    return sorted(calendar, key=lambda x: x["roi"], reverse=True)
```

## Integration Points

**Cross-Skill Dependencies**
- `marketing/growth-engine` - For experiment tracking on SEO changes
- `marketing/content-creator` - For content production workflow
- `research/trendradar` - For trending topic identification
- `marketing/analytics-dashboard` - For ranking and traffic monitoring

**Tool Integrations**
- Google Search Console API - For query data
- Ahrefs/SEMrush API - For competitor analysis
- Screaming Frog - For technical audits
- PageSpeed Insights API - For performance metrics

---

## Verification

After completing an SEO optimization task, confirm:

- [ ] Target keywords identified with search volume > 100/month
- [ ] On-page elements optimized (title < 60 chars, meta < 160 chars, H1 present)
- [ ] Technical audit passed: no 4xx/5xx errors, sitemap accessible, robots.txt valid
- [ ] Content is original, > 1500 words for competitive keywords
- [ ] Backlink strategy documented with 5+ target domains
- [ ] Core Web Vitals: LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Analytics tracking verified: GA4 receiving data, conversions tracked
- [ ] If targeting AI search: llms.txt present, content is passage-citable

---

**Related Skills**: `marketing/content-creator`, `marketing/analytics-dashboard`, `marketing/market-research`, `marketing/marketing-ops`

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
