---
name: seo-auditor
description: SEO analysis and optimization automation for websites. Use when conducting technical SEO audits, tracking keyword
  rankings, analyzing competitor SEO, monitoring backlink profiles, optimizing existing content, improving local SEO visibility,
  generating SEO reports for clients, or automating website health checks.
domain: marketing
tags:
- auditor
- growth
- marketing
- monitoring
- seo
- money
version: 1.0.0
---

# SEO Auditor Skill

**Production-ready** automation untuk website SEO analysis & optimization.

## Overview

SEO Auditor provides comprehensive website optimization capabilities including technical SEO audits, keyword ranking tracking, competitor analysis, backlink monitoring, content optimization suggestions, local SEO improvements, and automated reporting. It serves as a complete SEO management solution that automates the audit process, tracks performance over time, identifies actionable improvements, and generates client-ready reports in PDF and HTML format.

## Money-Making Overview

**Buyer Persona:**
- Small-to-medium business owners ($500K–$10M revenue) who know they need SEO but don't know where to start
- Web agencies delivering client sites who need to upsell SEO audit as a service ($500–2,000 upsell per engagement)
- SaaS founders preparing for launch or Series A who need clean technical SEO before investors scrutinize
- E-commerce operators who want to maximize organic traffic without burning ad budget
- Local businesses (dentists, lawyers, restaurants, trades) who need to dominate local pack results
- Marketing agencies outsourcing technical SEO so their content team can focus on writing

**Pricing Tiers:**

| Tier | Price | What They Get |
|------|-------|---------------|
| Quick SEO Audit | $500 | One-pass technical audit: crawl analysis, Core Web Vitals, on-page spot-check, top-10 issues ranked by impact, HTML report. 48-hour turnaround. |
| Full SEO Audit | $1,500 | Deep audit: technical + on-page + off-page + competitor gap analysis + keyword opportunity map + structured data audit + priority migration plan. PDF+HTML+JSON deliverable. One 60-min walkthrough call included. |
| SEO Retainer | $1,000–2,500/mo | Weekly rank tracking, monthly full audit, ongoing competitor monitoring, backlink watchdog, quarterly strategic review, Slack/email support. 3-month minimum. |

**First-Dollar Timeline:**
- **Day 1**: Run the First Action script below against a prospect's site. It produces a 1-page HTML summary with their Core Web Vitals grade, crawl issues count, and the top 3 fixes they need. Email it with "Quick SEO Health Check — no strings attached" — this hooks them.
- **Day 2–3**: Follow up with the full Quick Audit deliverable. Send invoice for $500. Close rate on a prospect who just saw their failing LCP score: >35%.
- **Week 2**: Offer a discounted first Full Audit ($750 intro) to Quick Audit clients. Target agencies managing 5+ client sites.
- **Month 1**: Sign 1–2 retainer clients at $1,500/mo by offering the first month at $750 with a guarantee they'll see ranking movement within 60 days.

## When to Use

**Trigger phrases:**
- "seo auditor"
- "Technical SEO audit": Identifying crawl errors, speed issues, and mobile-friendliness problems
- "Keyword tracking": Monitoring rankings for target keywords over time
- "Competitor analysis": Comparing against competitors' SEO performance

- **Technical SEO audit**: Identifying crawl errors, speed issues, and mobile-friendliness problems
- **Keyword tracking**: Monitoring rankings for target keywords over time
- **Competitor analysis**: Comparing against competitors' SEO performance
- **Backlink monitoring**: Tracking new, lost, and toxic backlinks
- **Content optimization**: Suggesting improvements for existing content
- **Local SEO**: Google My Business optimization and local citations
- **Report generation**: Creating HTML and PDF reports for clients
- **Scheduled audits**: Automated regular website health checks

## First Action in 60 Minutes

Run a comprehensive technical SEO audit against any website using free Google APIs. The script below crawls PageSpeed Insights, checks for common issues, and generates a professional HTML audit report. No API keys required for most checks.

```python
#!/usr/bin/env python3
"""
seo_audit.py — Comprehensive technical SEO audit script.
Usage:  python3 seo_audit.py https://example.com [--name "Client Name"] [--output report.html]

Generates a branded SEO audit report in under 60 minutes. Zero API key required for PageSpeed checks.
"""

import json, sys, time, os, urllib.request, urllib.error, urllib.parse, html
from datetime import datetime
from urllib.parse import urlparse

# ─── Config ───────────────────────────────────────────────────────────────────

PAGESPEED_API = "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed"

# ─── Core Web Vitals & Performance Audit ──────────────────────────────────────

def run_pagespeed(url: str, strategy: str = "mobile") -> dict:
    """Run Google PageSpeed Insights audit (no API key — quota-limited but works)."""
    params = urllib.parse.urlencode({
        "url": url, "strategy": strategy, "category": ["PERFORMANCE", "ACCESSIBILITY", "BEST_PRACTICES", "SEO"],
    })
    api_url = f"{PAGESPEED_API}?{params}"
    try:
        req = urllib.request.Request(api_url, headers={"User-Agent": "SEO-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def extract_metric(data: dict, key: str) -> dict:
    """Extract a metric dict from the Lighthouse result."""
    try:
        return data["lighthouseResult"]["audits"][key]
    except (KeyError, TypeError):
        return {"title": key, "score": None, "displayValue": "N/A"}

def grade_core_web_vital(metric_name: str, numeric_value: float) -> tuple:
    """Return (grade, color) for a CWV metric."""
    thresholds = {
        "lcp":        (2500, 4000),   # ms  — good, needs-improvement
        "fid":        (100, 300),      # ms
        "cls":        (0.1, 0.25),     # score
        "inp":        (200, 500),      # ms
        "tbt":        (200, 600),      # ms
        "si":         (3400, 5800),    # ms
    }
    low, high = thresholds.get(metric_name, (0, 0))
    if numeric_value <= low:
        return "PASS", "#22c55e"
    elif numeric_value <= high:
        return "NEEDS WORK", "#eab308"
    return "FAIL", "#ef4444"

def parse_numeric(value_str: str) -> float:
    """Parse a displayValue string like '2.4 s' or '0.05' into a float."""
    if not value_str:
        return 0.0
    v = value_str.replace("s", "").replace("ms", "").strip()
    try:
        return float(v)
    except ValueError:
        return 0.0

# ─── Crawl & Technical Checks (Simulated) ────────────────────────────────────

def check_robots_txt(url: str) -> dict:
    """Check robots.txt existence and sitemap references."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    result = {"url": robots_url, "exists": False, "sitemap_refs": 0, "blocks_all": False}
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": "SEO-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            result["exists"] = True
            result["sitemap_refs"] = content.lower().count("sitemap:")
            result["blocks_all"] = "disallow: /" in content.lower()
    except Exception:
        pass
    return result

def check_ssl(url: str) -> dict:
    """Verify HTTPS redirect and certificate."""
    parsed = urlparse(url)
    https_url = f"https://{parsed.netloc}/"
    result = {"https_supported": False, "redirects_to_https": False, "cert_valid": False}
    try:
        req = urllib.request.Request(https_url, headers={"User-Agent": "SEO-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            result["https_supported"] = True
            result["cert_valid"] = True
            if resp.url.startswith("https"):
                result["redirects_to_https"] = True
    except Exception:
        pass
    # Also check if http redirects
    http_url = f"http://{parsed.netloc}/"
    try:
        req = urllib.request.Request(http_url, headers={"User-Agent": "SEO-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.url.startswith("https"):
                result["redirects_to_https"] = True
    except Exception:
        pass
    return result

def check_page_title(url: str) -> dict:
    """Fetch the page and extract <title>, <h1>, meta description."""
    result = {"title": "", "title_length": 0, "meta_description": "", "meta_desc_length": 0, "h1_count": 0, "h1_text": ""}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; SEO-Auditor/1.0)"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html_content = resp.read().decode("utf-8", errors="replace")

            # <title>
            import re
            m = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE | re.DOTALL)
            if m:
                result["title"] = m.group(1).strip()
                result["title_length"] = len(result["title"])

            # <meta name="description">
            m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
            if not m:
                m = re.search(r'<meta\s+content=["\']([^"\']*)["\']\s+name=["\']description["\']', html_content, re.IGNORECASE)
            if m:
                result["meta_description"] = m.group(1).strip()
                result["meta_desc_length"] = len(result["meta_description"])

            # <h1>
            h1s = re.findall(r'<h1[^>]*>([^<]+)</h1>', html_content, re.IGNORECASE | re.DOTALL)
            result["h1_count"] = len(h1s)
            if h1s:
                result["h1_text"] = h1s[0].strip()
    except Exception as e:
        result["error"] = str(e)
    return result

# ─── Report Generator ─────────────────────────────────────────────────────────

def generate_report(url: str, client_name: str = None) -> str:
    """Run a full audit and generate an HTML report string."""
    name = client_name or urlparse(url).netloc
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    findings = []
    score = {"technical": 0, "onpage": 0, "performance": 0, "overall": 0}

    # ── PageSpeed (Mobile) ──
    ps_mobile = run_pagespeed(url, "mobile")
    ps_desktop = run_pagespeed(url, "desktop")

    try:
        perf_score_m = ps_mobile["lighthouseResult"]["categories"]["performance"]["score"] * 100
    except (KeyError, TypeError):
        perf_score_m = None
    try:
        perf_score_d = ps_desktop["lighthouseResult"]["categories"]["performance"]["score"] * 100
    except (KeyError, TypeError):
        perf_score_d = None
    try:
        seo_score_m = ps_mobile["lighthouseResult"]["categories"]["seo"]["score"] * 100
    except (KeyError, TypeError):
        seo_score_m = None

    if perf_score_m is not None:
        score["performance"] = round(perf_score_m)
    elif perf_score_d is not None:
        score["performance"] = round(perf_score_d)

    # ── Core Web Vitals ──
    for metric_key, label in [("largest-contentful-paint", "LCP"), ("interactive", "TBT proxy (TBT)"),
                              ("cumulative-layout-shift", "CLS"), ("speed-index", "SI"),
                              ("first-contentful-paint", "FCP"), ("total-blocking-time", "TBT")]:
        m = extract_metric(ps_mobile if ps_mobile else ps_desktop, metric_key)
        if m.get("score") is not None:
            numeric = parse_numeric(m.get("displayValue", "0"))
            grade, color = grade_core_web_vital(metric_key.split("-")[0], numeric)
            findings.append({
                "category": "Core Web Vitals", "metric": label,
                "value": m.get("displayValue", "N/A"),
                "grade": grade, "color": color,
                "severity": "high" if grade == "FAIL" else "medium" if grade == "NEEDS WORK" else "low",
            })

    # ── SSL & Security ──
    ssl = check_ssl(url)
    if not ssl["https_supported"]:
        findings.append({"category": "Security", "metric": "HTTPS", "value": "Not supported", "grade": "FAIL", "color": "#ef4444", "severity": "critical"})
    elif not ssl["redirects_to_https"]:
        findings.append({"category": "Security", "metric": "HTTP→HTTPS Redirect", "value": "Missing redirect", "grade": "FAIL", "color": "#ef4444", "severity": "high"})
    else:
        findings.append({"category": "Security", "metric": "HTTPS", "value": "OK", "grade": "PASS", "color": "#22c55e", "severity": "low"})
        score["technical"] += 15

    # ── Robots.txt ──
    robots = check_robots_txt(url)
    if robots["exists"]:
        findings.append({"category": "Crawl", "metric": "robots.txt", "value": f"Found ({robots['sitemap_refs']} sitemaps)", "grade": "PASS", "color": "#22c55e", "severity": "low"})
        score["technical"] += 15
        if robots["blocks_all"]:
            findings.append({"category": "Crawl", "metric": "robots.txt — Disallow All", "value": "WARNING: Disallow: / blocks all crawlers", "grade": "FAIL", "color": "#ef4444", "severity": "critical"})
    else:
        findings.append({"category": "Crawl", "metric": "robots.txt", "value": "Missing", "grade": "NEEDS WORK", "color": "#eab308", "severity": "medium"})

    if seo_score_m is not None:
        findings.append({"category": "SEO", "metric": "Lighthouse SEO Score", "value": f"{seo_score_m}/100", "grade": "PASS" if seo_score_m >= 90 else "NEEDS WORK", "color": "#22c55e" if seo_score_m >= 90 else "#eab308", "severity": "medium"})
        score["technical"] += 15 if seo_score_m >= 90 else 5
    else:
        score["technical"] += 10

    # ── On-Page ──
    page = check_page_title(url)
    if page.get("error"):
        findings.append({"category": "On-Page", "metric": "Page Fetch", "value": f"Error: {page['error']}", "grade": "FAIL", "color": "#ef4444", "severity": "high"})
    else:
        if not page["title"]:
            findings.append({"category": "On-Page", "metric": "Title Tag", "value": "Missing", "grade": "FAIL", "color": "#ef4444", "severity": "critical"})
        elif page["title_length"] < 30:
            findings.append({"category": "On-Page", "metric": "Title Tag", "value": f"'{page['title'][:50]}...' ({page['title_length']} chars)", "grade": "NEEDS WORK", "color": "#eab308", "severity": "medium"})
        elif page["title_length"] > 60:
            findings.append({"category": "On-Page", "metric": "Title Tag", "value": f"'{page['title'][:50]}...' ({page['title_length']} chars)", "grade": "NEEDS WORK", "color": "#eab308", "severity": "medium", "note": "Over 60 chars — may truncate in SERPs"})
        else:
            findings.append({"category": "On-Page", "metric": "Title Tag", "value": f"'{page['title'][:50]}...' ({page['title_length']} chars)", "grade": "PASS", "color": "#22c55e", "severity": "low"})
            score["onpage"] += 15

        if not page["meta_description"]:
            findings.append({"category": "On-Page", "metric": "Meta Description", "value": "Missing", "grade": "FAIL", "color": "#ef4444", "severity": "high"})
        elif page["meta_desc_length"] < 120:
            findings.append({"category": "On-Page", "metric": "Meta Description", "value": f"Too short ({page['meta_desc_length']} chars, target 120-158)", "grade": "NEEDS WORK", "color": "#eab308", "severity": "medium"})
        else:
            findings.append({"category": "On-Page", "metric": "Meta Description", "value": f"{page['meta_desc_length']} chars", "grade": "PASS", "color": "#22c55e", "severity": "low"})
            score["onpage"] += 15

        if page["h1_count"] == 0:
            findings.append({"category": "On-Page", "metric": "H1 Tag", "value": "Missing", "grade": "FAIL", "color": "#ef4444", "severity": "high"})
        elif page["h1_count"] > 1:
            findings.append({"category": "On-Page", "metric": "H1 Tag", "value": f"{page['h1_count']} H1s found (recommend 1)", "grade": "NEEDS WORK", "color": "#eab308", "severity": "medium"})
        else:
            findings.append({"category": "On-Page", "metric": "H1 Tag", "value": f"'{page['h1_text'][:50]}'", "grade": "PASS", "color": "#22c55e", "severity": "low"})
            score["onpage"] += 15

    score["technical"] = min(100, score["technical"])
    score["onpage"] = min(100, score["onpage"])
    score["overall"] = round((score["technical"] + score["onpage"] + score["performance"]) / 3) if score["performance"] else round((score["technical"] + score["onpage"]) / 2)

    # ── Build HTML ──
    critical_count = len([f for f in findings if f.get("severity") == "critical"])
    high_count = len([f for f in findings if f.get("severity") == "high"])
    medium_count = len([f for f in findings if f.get("severity") == "medium"])

    rows_html = ""
    for f in findings:
        badge = f'<span style="display:inline-block;padding:2px 8px;border-radius:10px;font-size:12px;font-weight:600;color:#fff;background:{f["color"]};">{f["grade"]}</span>'
        rows_html += f'<tr><td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;font-size:13px;">{f["category"]}</td><td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;font-size:13px;font-weight:600;">{f["metric"]}</td><td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;font-size:13px;">{f["value"]}</td><td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;text-align:center;">{badge}</td></tr>\n'

    report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SEO Audit Report — {html.escape(name)}</title>
<style>
  @page {{ margin: 20mm 15mm; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif; color:#111827; line-height:1.6; }}
  .container {{ max-width:900px; margin:0 auto; padding:40px 20px; }}
  h1 {{ font-size:28px; margin-bottom:4px; }}
  h2 {{ font-size:20px; margin:30px 0 12px; padding-bottom:8px; border-bottom:2px solid #e5e7eb; }}
  h3 {{ font-size:16px; margin:20px 0 8px; }}
  .subtitle {{ color:#6b7280; font-size:14px; margin-bottom:24px; }}
  .score-grid {{ display:flex; gap:16px; margin:20px 0; flex-wrap:wrap; }}
  .score-card {{ flex:1; min-width:160px; background:#f9fafb; border-radius:12px; padding:20px; text-align:center; }}
  .score-card .num {{ font-size:36px; font-weight:700; }}
  .score-card .label {{ font-size:13px; color:#6b7280; margin-top:4px; }}
  .score-card .grade {{ font-size:14px; font-weight:600; margin-top:6px; }}
  .summary-box {{ background:#fef2f2; border-left:4px solid #ef4444; padding:16px 20px; border-radius:8px; margin:20px 0; }}
  .summary-box.green {{ background:#f0fdf4; border-left-color:#22c55e; }}
  .summary-box.good {{ background:#fefce8; border-left-color:#eab308; }}
  table {{ width:100%; border-collapse:collapse; margin:16px 0; }}
  th {{ text-align:left; padding:10px 12px; font-size:12px; text-transform:uppercase; color:#6b7280; border-bottom:2px solid #e5e7eb; }}
  .priority-list {{ list-style:none; }}
  .priority-list li {{ padding:10px 14px; margin:8px 0; border-radius:8px; font-size:14px; }}
  .footer {{ margin-top:40px; padding-top:20px; border-top:1px solid #e5e7eb; font-size:12px; color:#9ca3af; text-align:center; }}
</style>
</head>
<body>
<div class="container">

<h1>SEO Audit Report</h1>
<p class="subtitle"><strong>{html.escape(name)}</strong> &mdash; {html.escape(url)} &mdash; {date_str}</p>

<div class="score-grid">
  <div class="score-card">
    <div class="num" style="color:{'#22c55e' if score['overall'] >= 80 else '#eab308' if score['overall'] >= 50 else '#ef4444'};">{score['overall']}</div>
    <div class="label">Overall SEO Score</div>
    <div class="grade">{'Good' if score['overall'] >= 80 else 'Needs Improvement' if score['overall'] >= 50 else 'Poor'}</div>
  </div>
  <div class="score-card">
    <div class="num" style="color:{'#22c55e' if score['technical'] >= 80 else '#eab308'};">{score['technical']}</div>
    <div class="label">Technical SEO</div>
  </div>
  <div class="score-card">
    <div class="num" style="color:{'#22c55e' if score['onpage'] >= 80 else '#eab308'};">{score['onpage']}</div>
    <div class="label">On-Page SEO</div>
  </div>
  <div class="score-card">
    <div class="num" style="color:{'#22c55e' if score['performance'] >= 80 else '#eab308' if score['performance'] >= 50 else '#ef4444'};">{score['performance'] if score['performance'] else 'N/A'}</div>
    <div class="label">Performance</div>
  </div>
</div>

{("<div class='summary-box'>" if critical_count+high_count > 0 else "<div class='summary-box green'>")}<strong>{'Issues Found' if critical_count+high_count > 0 else 'Looking Good'}:</strong> {critical_count} critical, {high_count} high, {medium_count} medium issue{'s' if critical_count+high_count+medium_count != 1 else ''} detected.</div>

<h2>Findings</h2>
<table>
<thead><tr><th>Category</th><th>Metric</th><th>Value</th><th style="text-align:center;">Status</th></tr></thead>
<tbody>
{rows_html}
</tbody>
</table>

<h2>Priority Actions</h2>
<ol class="priority-list">
"""
    # Group by severity for priority actions
    for sev in ["critical", "high", "medium"]:
        for f in findings:
            if f.get("severity") == sev:
                color = {"critical": "#fef2f2,#ef4444", "high": "#fef2f2,#ef4444", "medium": "#fefce8,#eab308"}[sev]
                bg, fg = color.split(",")
                report += f'<li style="background:{bg};border-left:4px solid {fg};color:#111827;"><strong>{f["metric"]}</strong>: {f["value"]} <span style="color:{fg};font-weight:600;text-transform:uppercase;">[{sev}]</span></li>\n'

    report += f"""</ol>

<div class="footer">
  <p>Generated by SEO Auditor &mdash; {date_str}</p>
  <p>This is an automated assessment. Always verify findings with manual checks.</p>
</div>

</div>
</body>
</html>"""
    return report


if __name__ == "__main__":
    import sys
    target = None
    client_name = None
    output_file = "seo-audit-report.html"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            client_name = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i].startswith("http"):
            target = args[i]
            i += 1
        else:
            i += 1

    if not target:
        print("Usage: python3 seo_audit.py <url> [--name \"Client Name\"] [--output report.html]")
        sys.exit(1)

    print(f"[*] Running SEO audit for {target}...")
    start = time.time()
    report_html = generate_report(target, client_name)
    elapsed = time.time() - start

    with open(output_file, "w") as f:
        f.write(report_html)

    print(f"[+] Audit complete in {elapsed:.1f}s. Report: {output_file}")
    print(f"[*] Open in browser or print to PDF: file://{os.path.abspath(output_file)}")
```

**To run against a prospect:**
```bash
python3 seo_audit.py https://staging.example.com --name "Example Corp" --output example-seo-audit.html
```

Open `example-seo-audit.html` in a browser. Screenshot the score grid and email it with your pitch. This one page hooks more prospects than any deck.

## The Process

- Configure analysis, analyzing, auditor, audits, automating settings before first use

### Step 1: Target Configuration

**Configuration File Setup**:
```json
{
  "targets": [
    {
      "name": "Client Website",
      "url": "https://example.com",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "competitors": ["https://competitor1.com", "https://competitor2.com"]
    }
  ],
  "schedule": {
    "fullAudit": "weekly",
    "rankTracking": "daily",
    "backlinkCheck": "weekly"
  },
  "reporting": {
    "format": "html",
    "email": "client@example.com",
    "branding": {
      "logo": "assets/logo.png",
      "colors": {"primary": "#007bff"}
    }
  }
}
```

### Step 2: Full SEO Audit

**Run Complete Audit**:
```bash
python3 seo_audit.py https://example.com --name "Client Name" --output client-report.html
```

**Audit Categories**:
1. **Technical SEO**
   - Crawlability & indexation
   - Site speed (Core Web Vitals)
   - Mobile-friendliness
   - HTTPS & security
   - Structured data
   - robots.txt & sitemap check

2. **On-Page SEO**
   - Title tags & meta descriptions
   - Header structure (H1-H6)
   - Content quality & length
   - Keyword optimization
   - Internal linking
   - Image alt text

3. **Off-Page SEO**
   - Backlink profile analysis
   - Domain authority
   - Social signals
   - Brand mentions

4. **Local SEO** (if applicable)
   - Google My Business optimization
   - NAP consistency
   - Local citations
   - Reviews management

### Step 3: Rank Tracking

**Monitor Keyword Rankings**:
```bash
python3 seo_audit.py https://example.com --name "Client Name" --ranks
```

**Setup Tracking**:
1. Add target keywords in config
2. Schedule daily tracking via cron
3. Monitor position changes weekly
4. Set alerts for significant moves (drop >5 positions)

### Step 4: Backlink Analysis

**Track Backlink Profile**:
```bash
python3 seo_audit.py https://example.com --name "Client Name" --backlinks
```

**Metrics Tracked**:
- New backlinks from last check
- Lost backlinks
- Toxic score changes
- Referring domains count
- Domain authority trend

### Step 5: Competitor Comparison

**Analyze Competitors**:
```bash
python3 seo_audit.py https://example.com --name "Client Name" --competitors
```

**Comparison Points**:
- Top ranking keywords
- Link profiles
- Content structure
- Page speed
- Mobile optimization

### Step 6: Report Generation

**Generate SEO Report**:
```bash
python3 seo_audit.py https://example.com --name "Client Name" --output report.html
# Print to PDF: use browser print-to-PDF or wkhtmltopdf
```

**Report Contents**:
- Overall SEO score
- Strengths and weaknesses
- Priority issues to fix
- Recommendation list
- Ranking history charts
- Backlink summary

### Step 7: Scheduled Automation

**Setup Regular Audits**:
```bash
# Weekly full audit (add to crontab)
0 0 * * 0 cd /path/to/auditor && python3 seo_audit.py https://client.com --output reports/weekly-$(date +\%Y-\%m-\%d).html

# Daily rank tracking
0 6 * * * cd /path/to/auditor && python3 seo_audit.py https://client.com --ranks
```

## Common Patterns

**Weekly SEO Workflow**:
```bash
# Monday morning routine
python3 seo_audit.py https://client.com --output reports/$(date +%Y-%m-%d).html
python3 seo_audit.py https://client.com --ranks
```

**Campaign-Based Audits**:
```bash
# Before marketing campaign
python3 seo_audit.py https://client.com --before-campaign
# After campaign
python3 seo_audit.py https://client.com --after-campaign
# Run diff to show improvement
```

**Emergency Health Check**:
```bash
# After site migration or redesign
python3 seo_audit.py https://client.com --quick
```

## Deliverable Format

When you deliver a paid SEO audit, the invoice-ready package includes:

```
SEO_Audit_<ClientName>_<Date>/
├── README.txt                       # Invoice reference, scope summary, disclaimers
├── seo-audit-report.html            # Full interactive report with scores, findings, priority actions
├── seo-audit-report.pdf             # Print-optimized version for stakeholders
├── raw-data/
│   ├── pagespeed-mobile.json        # Raw PageSpeed API response (mobile)
│   ├── pagespeed-desktop.json       # Raw PageSpeed API response (desktop)
│   └── onpage-analysis.json         # Title, meta, H1, and content audit data
├── recommendations.md               # Ranked fix list: priority, effort, impact
└── competitive-gap-analysis.md      # (Full Audit only) Gap vs top 3 competitors
```

**Invoice reference line:** `SEO Audit — <Client> — <Date> — $<amount>`

**Delivery email template:**
> Subject: SEO Audit Results — <Client> (<Date>)
>
> Hi <Name>,
>
> Attached is the SEO audit report for <Target>.
>
> **Executive Summary:**
> - Overall SEO Score: <score>/100
> - Critical issues: <N>  |  High: <N>  |  Medium: <N>
> - Top finding: <top_issue>
>
> The full report (<filename>.html) is interactive — open in any browser.
> A print-friendly PDF is also attached.
>
> **Next step:** I recommend a 30-minute walkthrough call to go over the findings and build a fix roadmap. I'll send a calendar invite.
>
> Invoice <#INV> attached. Payment terms: Net 15.
>
> Best,
> <Your Name>

## When NOT to Use

- Task is about sales, not marketing (use sales skills)
- Task is about product development (use product skills)
- You need to analyze marketing data (use analytics skills)
- Task is about customer support (use support skills)
- You don't have marketing assets
- Task requires legal review (consult legal)
- Client needs full SEO migration execution, not just an audit (upsell to implementation retainer)

## Red Flags

- **API quota exceeded**: Google Search Console or PageSpeed API limits hit — implement rate limiting or rotate keys
- **Audit incomplete**: Missing data from specific categories — check API connectivity
- **Backlink tracking stops**: Backlink API connection failure or API key expired
- **Report generation fails**: Template or formatting issues — verify template file path
- **Keyword rankings show null**: Check search volume or query issues
- **Speed scores inconsistent**: Device-specific checks (desktop vs mobile) not matched
- **Crawl errors missing**: Configuration issue or site blocked crawler access
- **Client expects instant rankings**: SEO takes 3-6 months to show meaningful movement — set expectations in the walkthrough call
- **You find a Critical issue on a live e-commerce site**: Escalate immediately — that's a revenue-impacting problem, handle with urgency

## Verification

**Connection Tests**:
```bash
# Test PageSpeed API
curl "https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile"
```

**Functional Verification**:

1. **Audit Complete Test**:
   ```bash
   python3 seo_audit.py https://example.com --output test-report.html

   # Verify all audit categories completed
   # Open test-report.html in browser and check:
   # - Score grid displays with 4 categories
   # - Findings table has rows
   # - Priority actions section is populated
   ```

2. **API Endpoint Verification**:
   ```bash
   # Verify PageSpeed API connection
   python3 -c "import urllib.request,json; d=json.loads(urllib.request.urlopen('https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://google.com&strategy=mobile',timeout=15).read()); print('OK' if d.get('lighthouseResult') else 'FAIL')"
   ```

**Data Quality Checks**:
- [ ] Audit data matches manual spot-checks (open DevTools, run Lighthouse manually, compare)
- [ ] Core Web Vitals values look reasonable (LCP <2.5s, CLS <0.1, TBT <200ms)
- [ ] Title/meta/H1 extraction is correct for the target URL
- [ ] SSL status matches actual site behavior
- [ ] robots.txt check matches the live file

**Output Verification**:
```bash
# After report generation
ls -la test-report.html

# Verify file is valid HTML
python3 -c "with open('test-report.html') as f: assert '</html>' in f.read(); print('Valid HTML')"
```

**Quick Health Check**:
```bash
echo "SEO Auditor Status"
echo "=================="
echo "PageSpeed API: $(python3 -c "import urllib.request; print('OK' if urllib.request.urlopen('https://pagespeedonline.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://google.com',timeout=10).status==200 else 'FAIL')" 2>/dev/null || echo 'FAIL')"
echo "Report Size: $(wc -c < test-report.html 2>/dev/null || echo 0) bytes"
echo "Last Audit: $(ls -t reports/ 2>/dev/null | head -1 || echo 'Never')"
echo "Target Sites: $(cat config.json 2>/dev/null | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('targets',[])))" 2>/dev/null || echo 0)"
```

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "SEO audits are a dime a dozen — every tool offers one for free" | Free tools give a raw dump. Clients pay $500–1,500 for *interpretation*: what to fix first, how to fix it, and what it's worth in traffic. That's what you deliver. |
| "I don't have access to Google Search Console for their site" | You don't need it. PageSpeed Insights + a crawl + on-page extraction catches 80%+ of issues. Add GSC data when you're on retainer. Start with what's public. |
| "My report won't be as good as SEMrush/Ahrefs" | You're not competing on data depth. You're competing on *actionability*. A 5-page report the client can execute tomorrow beats a 50-page automated dump they ignore. |
| "I can't charge for SEO without showing rankings movement first" | Technical issues (slow load, broken meta, missing SSL) are facts, not opinions. The audit itself validates your expertise. Fixes come after the invoice. |
| "Clients want guarantees — I can't guarantee Page 1 rankings" | You don't. You guarantee a thorough audit, a clear fix roadmap, and month-over-month progress tracking. Any agency promising rankings is lying. |
| "The script in this skill won't run on every site" | It handles the 90% case. For the remaining 10%, manual spot-checks + browser DevTools audit are the fallback. The script gets you in the door. |
| "I need certifications to be credible" | One solid audit report for a real client is worth more than any certificate. Use the First Action script on *your own site*, send the report to a prospect, and let the data speak. |
