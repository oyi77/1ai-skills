#!/usr/bin/env python3
"""
generate-site.py — Generate docs/index.html from SKILLS.json.

Run: python3 scripts/generate-site.py
"""

import json
import html
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
SKILLS_JSON = ROOT / 'SKILLS.json'
OUTPUT = ROOT / 'docs' / 'index.html'

# Category metadata
CAT_META = {
    'agents': {'icon': '🤖', 'color': '#8b5cf6', 'desc': 'AI agent orchestration, coding, research, and autonomous task execution'},
    'automation': {'icon': '⚡', 'color': '#fbbf24', 'desc': 'Bots, workflows, scrapers, and process automation'},
    'content': {'icon': '🎨', 'color': '#f472b6', 'desc': 'Video, audio, design, writing, and media generation'},
    'core': {'icon': '🧠', 'color': '#06d6a0', 'desc': 'AI infrastructure, memory, self-improvement, and model routing'},
    'cybersecurity': {'icon': '🛡️', 'color': '#ef4444', 'desc': 'Threat hunting, forensics, pen testing, SOC ops, and incident response'},
    'data': {'icon': '📊', 'color': '#38bdf8', 'desc': 'Data pipelines, analysis, visualization, and ETL'},
    'development': {'icon': '💻', 'color': '#a78bfa', 'desc': 'TDD, debugging, code review, PRD, and engineering workflows'},
    'devops': {'icon': '🚀', 'color': '#fb923c', 'desc': 'Docker, Kubernetes, CI/CD, cloud ops, and GitOps'},
    'financial': {'icon': '💰', 'color': '#34d399', 'desc': 'Finance analysis, valuation, tax, and portfolio management'},
    'integrations': {'icon': '🔗', 'color': '#60a5fa', 'desc': 'GitHub, Discord, Notion, Slack, Stripe, and platform integrations'},
    'marketing': {'icon': '📢', 'color': '#e879f9', 'desc': 'SEO, viral content, email, ads, and growth marketing'},
    'mcp': {'icon': '🔌', 'color': '#2dd4bf', 'desc': 'Model Context Protocol servers and tool integrations'},
    'meta': {'icon': '🔄', 'color': '#c084fc', 'desc': 'Self-evolving meta-skills, performance monitoring, and skill creation'},
    'mindset': {'icon': '🎯', 'color': '#fbbf24', 'desc': 'Negotiation, leadership, critical thinking, and productivity'},
    'operations': {'icon': '⚙️', 'color': '#94a3b8', 'desc': 'Business ops, governance, HR, legal, and project management'},
    'productivity': {'icon': '📋', 'color': '#22d3ee', 'desc': 'Calendars, email, meetings, and workspace management'},
    'research': {'icon': '🔬', 'color': '#4ade80', 'desc': 'Deep research, market analysis, competitive intelligence'},
    'sales': {'icon': '💼', 'color': '#f97316', 'desc': 'Lead generation, CRM, outreach, and sales automation'},
    'trading': {'icon': '📈', 'color': '#10b981', 'desc': 'Crypto, DeFi, Polymarket, and trading strategies'},
}

def load_skills():
    with open(SKILLS_JSON) as f:
        data = json.load(f)
    return data

def generate_html(data):
    total = data['total_skills']
    cats = data['categories']
    skills = data['skills']

    # Group skills by category
    by_cat = defaultdict(list)
    for s in skills:
        by_cat[s['category']].append(s)

    # New skills (latest 18)
    new_skills = [
        'docx-creator', 'pdf-creator', 'pptx-creator', 'xlsx-creator',
        'canvas-design', 'frontend-ui-design', 'theme-factory',
        'gemini-api-dev', 'replicate-runner', 'model-router',
        'stripe-integration', 'supabase-integration', 'firebase-integration', 'bigquery-integration',
        'spec-driven-development', 'context-engineering', 'browser-testing-devtools', 'git-workflow-mastery',
    ]
    new_skill_data = [s for s in skills if s['name'] in new_skills]

    # Build category cards HTML
    cat_cards = []
    for cat_name in CAT_META:
        meta = CAT_META[cat_name]
        count = cats.get(cat_name, 0)
        cat_cards.append(f'''
      <div class="cat-card fade-in" data-cat="{cat_name}">
        <div class="cat-head">
          <h3>{meta['icon']} {cat_name.replace('-', ' ').title()}</h3>
          <span class="count">{count}</span>
        </div>
        <p>{meta['desc']}</p>
      </div>''')

    # Build new skills cards HTML
    new_cards = []
    for s in new_skill_data:
        icon = CAT_META.get(s['category'], {}).get('icon', '📦')
        tags = ', '.join(s.get('tags', [])[:3])
        desc = html.escape(s.get('description', '')[:120])
        new_cards.append(f'''
      <div class="new-card fade-in">
        <span class="badge-new">New</span>
        <span class="new-icon">{icon}</span>
        <h3>{html.escape(s['name'].replace('-', ' ').title())}</h3>
        <p>{desc}</p>
        <div class="new-meta">
          <span>{s['category']}</span>
          <span>{tags}</span>
        </div>
      </div>''')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1ai-Skills — {total}+ Open-Source AI Agent Skills</title>
<meta name="description" content="The world's largest open-source AI skill ecosystem. {total}+ skills across {len(cats)} categories for Claude Code, Cursor, Windsurf, and more.">
<meta property="og:title" content="1ai-Skills — {total}+ Open-Source AI Agent Skills">
<meta property="og:description" content="The world's largest open-source AI skill ecosystem with self-evolving meta-skills.">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary_large_image">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --bg:#06060e;--bg2:#0c0c1a;--bg3:#111128;
  --surface:rgba(255,255,255,.03);--surface2:rgba(255,255,255,.06);--surface3:rgba(255,255,255,.08);
  --text:#e8e8f0;--text2:#9898b8;--text3:#5a5a78;
  --accent:#8b5cf6;--accent2:#06d6a0;--accent3:#38bdf8;--accent4:#f472b6;--accent5:#fbbf24;
  --grad:linear-gradient(135deg,#8b5cf6,#38bdf8,#06d6a0);
  --border:rgba(255,255,255,.06);--border2:rgba(255,255,255,.12);
  --glass:rgba(12,12,26,.6);--glass2:rgba(12,12,26,.8);
  --radius:16px;--radius-sm:10px;--radius-xs:6px;
  --shadow:0 8px 32px rgba(0,0,0,.4);
  --font:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;
  --mono:'SF Mono','Fira Code','Cascadia Code',Consolas,monospace;
}}
html{{scroll-behavior:smooth}}
body{{font-family:var(--font);background:var(--bg);color:var(--text);line-height:1.65;overflow-x:hidden}}
a{{color:var(--accent3);text-decoration:none;transition:color .2s}}
a:hover{{color:#7dd3fc}}
.container{{max-width:1240px;margin:0 auto;padding:0 24px}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:var(--glass2);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}
nav .container{{display:flex;align-items:center;justify-content:space-between;height:64px}}
nav .logo{{font-size:1.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
nav .links{{display:flex;gap:8px;align-items:center}}
nav .links a{{color:var(--text2);font-size:.85rem;font-weight:500;padding:6px 14px;border-radius:8px;transition:all .2s}}
nav .links a:not(.btn):hover{{color:#fff;background:var(--surface2)}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:10px 24px;border-radius:var(--radius-sm);font-weight:600;font-size:.875rem;cursor:pointer;border:none;transition:all .25s}}
.btn-primary{{background:var(--grad);color:#fff}}
.btn-primary:hover{{opacity:.92;transform:translateY(-1px);box-shadow:0 4px 24px rgba(139,92,246,.4)}}
.btn-ghost{{background:var(--surface);color:var(--text);border:1px solid var(--border2)}}
.btn-ghost:hover{{border-color:var(--accent);color:#fff;background:rgba(139,92,246,.08)}}

/* HERO */
.hero{{padding:140px 0 80px;text-align:center;position:relative;overflow:hidden;min-height:85vh;display:flex;align-items:center}}
.hero-bg{{position:absolute;inset:0;z-index:0}}
.hero-bg .orb{{position:absolute;border-radius:50%;filter:blur(80px);opacity:.35;animation:orbFloat 20s ease-in-out infinite}}
.hero-bg .orb-1{{width:500px;height:500px;background:var(--accent);top:-10%;left:10%}}
.hero-bg .orb-2{{width:400px;height:400px;background:var(--accent3);bottom:-5%;right:5%;animation-delay:-7s}}
.hero-bg .orb-3{{width:300px;height:300px;background:var(--accent4);top:30%;right:25%;animation-delay:-13s}}
@keyframes orbFloat{{0%,100%{{transform:translate(0,0) scale(1)}}25%{{transform:translate(30px,-40px) scale(1.05)}}50%{{transform:translate(-20px,20px) scale(.95)}}75%{{transform:translate(40px,10px) scale(1.02)}}}}
.hero-grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.015) 1px,transparent 1px);background-size:60px 60px;mask-image:radial-gradient(ellipse 70% 60% at 50% 40%,black,transparent)}}
.hero-content{{position:relative;z-index:1}}
.hero-badge{{display:inline-flex;align-items:center;gap:8px;padding:6px 16px;border-radius:999px;background:var(--surface2);border:1px solid var(--border2);font-size:.8rem;color:var(--accent2);margin-bottom:28px}}
.hero-badge .dot{{width:8px;height:8px;border-radius:50%;background:var(--accent2);animation:pulse 2s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.5;transform:scale(.8)}}}}
.hero h1{{font-size:clamp(2.6rem,6vw,4.4rem);font-weight:800;line-height:1.08;margin-bottom:24px;letter-spacing:-.03em}}
.hero h1 .grad{{background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero .tagline{{font-size:clamp(1.05rem,2vw,1.3rem);color:var(--text2);max-width:680px;margin:0 auto 16px;line-height:1.6}}
.typing-wrap{{display:inline-block;min-height:1.6em}}
.typing-cursor{{display:inline-block;width:2px;height:1.1em;background:var(--accent2);margin-left:2px;vertical-align:text-bottom;animation:blink 1s step-end infinite}}
@keyframes blink{{50%{{opacity:0}}}}
.hero .actions{{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:36px}}

/* STATS */
.stats{{padding:0;position:relative;z-index:1}}
.stats-inner{{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:var(--border);border-radius:var(--radius);overflow:hidden;margin-top:-40px;position:relative;box-shadow:var(--shadow)}}
.stat{{background:var(--glass2);backdrop-filter:blur(20px);padding:32px 20px;text-align:center}}
.stat .num{{font-size:clamp(1.8rem,3.5vw,2.6rem);font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}}
.stat .label{{font-size:.8rem;color:var(--text2);margin-top:6px;text-transform:uppercase;letter-spacing:.08em;font-weight:500}}

/* SECTIONS */
section{{padding:100px 0}}
.section-header{{text-align:center;margin-bottom:56px}}
.section-tag{{display:inline-block;font-size:.75rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.12em;margin-bottom:12px;background:rgba(139,92,246,.08);padding:5px 14px;border-radius:999px}}
.section-title{{font-size:clamp(1.8rem,4vw,2.6rem);font-weight:800;letter-spacing:-.02em;margin-bottom:14px}}
.section-sub{{color:var(--text2);max-width:620px;margin:0 auto;font-size:1.05rem;line-height:1.6}}

/* NEW SKILLS */
.new-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}}
.new-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px;position:relative;overflow:hidden;transition:all .3s}}
.new-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--grad);opacity:.6}}
.new-card:hover{{border-color:var(--border2);transform:translateY(-4px);box-shadow:0 12px 40px rgba(139,92,246,.12)}}
.new-card .badge-new{{position:absolute;top:16px;right:16px;background:rgba(244,114,182,.15);color:var(--accent4);font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:999px;text-transform:uppercase}}
.new-card .new-icon{{font-size:2rem;margin-bottom:14px;display:block}}
.new-card h3{{font-size:1.1rem;font-weight:700;margin-bottom:8px;color:#fff}}
.new-card p{{font-size:.88rem;color:var(--text2);line-height:1.6}}
.new-card .new-meta{{display:flex;gap:12px;margin-top:14px;flex-wrap:wrap}}
.new-card .new-meta span{{font-size:.75rem;padding:3px 10px;border-radius:999px;background:var(--surface2);color:var(--text2)}}

/* CATEGORY */
.search-wrap{{max-width:480px;margin:0 auto 40px;position:relative}}
.search-wrap input{{width:100%;padding:14px 20px 14px 48px;border-radius:var(--radius-sm);border:1px solid var(--border2);background:var(--surface);color:var(--text);font-size:.95rem;font-family:var(--font);outline:none;transition:border-color .2s}}
.search-wrap input::placeholder{{color:var(--text3)}}
.search-wrap input:focus{{border-color:var(--accent);box-shadow:0 0 0 3px rgba(139,92,246,.15)}}
.search-wrap .search-icon{{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:var(--text3);font-size:1.1rem;pointer-events:none}}
.cat-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.cat-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:24px;transition:all .3s;cursor:default}}
.cat-card:hover{{border-color:rgba(139,92,246,.3);transform:translateY(-3px);box-shadow:0 8px 32px rgba(139,92,246,.1)}}
.cat-card .cat-head{{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}}
.cat-card h3{{font-size:1rem;font-weight:700}}
.cat-card .count{{font-size:.75rem;font-weight:700;color:var(--accent2);background:rgba(6,214,160,.1);padding:3px 10px;border-radius:999px;min-width:40px;text-align:center}}
.cat-card p{{font-size:.85rem;color:var(--text2);line-height:1.6}}
.cat-card.hidden{{display:none}}
.no-results{{grid-column:1/-1;text-align:center;padding:48px 0;color:var(--text3);font-size:1rem}}

/* INSTALL */
.install-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:20px}}
.install-card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;transition:all .3s}}
.install-card:hover{{border-color:var(--border2);transform:translateY(-2px)}}
.install-card-header{{padding:20px 24px 12px;display:flex;align-items:center;justify-content:space-between}}
.install-card-header h3{{font-size:1rem;font-weight:700}}
.install-card-header .method{{font-size:.7rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:.08em;background:rgba(139,92,246,.1);padding:3px 10px;border-radius:999px}}
.install-card-body{{padding:0 24px 20px}}
.install-card-body .desc{{font-size:.85rem;color:var(--text2);margin-bottom:14px;line-height:1.5}}
.code-block{{position:relative;background:var(--bg);border:1px solid var(--border);border-radius:var(--radius-xs);overflow:hidden}}
.code-block pre{{padding:16px 52px 16px 18px;font-family:var(--mono);font-size:.85rem;color:var(--accent2);overflow-x:auto;line-height:1.7;white-space:pre-wrap;word-break:break-all}}
.copy-btn{{position:absolute;top:8px;right:8px;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-xs);color:var(--text2);padding:6px 10px;cursor:pointer;font-size:.75rem;font-family:var(--font);transition:all .2s}}
.copy-btn:hover{{background:var(--surface3);color:#fff;border-color:var(--border2)}}

/* FOOTER */
footer{{padding:48px 0;border-top:1px solid var(--border)}}
.footer-inner{{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:20px}}
.footer-left{{display:flex;align-items:center;gap:16px}}
.footer-left .logo-sm{{font-weight:800;font-size:1rem;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.footer-left .copy{{color:var(--text3);font-size:.82rem}}
.footer-links{{display:flex;gap:8px;align-items:center}}
.footer-links a{{color:var(--text2);font-size:.82rem;padding:6px 12px;border-radius:6px;transition:all .2s}}
.footer-links a:hover{{color:#fff;background:var(--surface2)}}

/* FADE IN */
.fade-in{{opacity:0;transform:translateY(24px);transition:opacity .6s ease-out,transform .6s ease-out}}
.fade-in.visible{{opacity:1;transform:translateY(0)}}
.fade-in-delay-1{{transition-delay:.1s}}
.fade-in-delay-2{{transition-delay:.2s}}
.fade-in-delay-3{{transition-delay:.3s}}

/* RESPONSIVE */
@media(max-width:900px){{.stats-inner{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:768px){{
  nav .links a:not(.btn){{display:none}}
  .hero{{min-height:auto;padding:120px 0 60px}}
  .hero h1{{font-size:2.2rem}}
  section{{padding:72px 0}}
  .cat-grid,.new-grid,.install-grid{{grid-template-columns:1fr}}
  footer .footer-inner{{flex-direction:column;text-align:center}}
}}
@media(max-width:480px){{
  .stats-inner{{grid-template-columns:1fr}}
  .hero .actions{{flex-direction:column;align-items:center}}
  .hero .actions .btn{{width:100%;justify-content:center}}
}}
</style>
</head>
<body>

<nav>
  <div class="container">
    <a href="#" class="logo">1ai-Skills</a>
    <div class="links">
      <a href="#new">New Skills</a>
      <a href="#categories">Categories</a>
      <a href="#quickstart">Install</a>
      <a href="https://github.com/oyi77/1ai-skills" class="btn btn-ghost" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        GitHub
      </a>
    </div>
  </div>
</nav>

<section class="hero">
  <div class="hero-bg">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="hero-grid"></div>
  </div>
  <div class="container hero-content">
    <div class="hero-badge fade-in">
      <span class="dot"></span>
      {total} skills and growing
    </div>
    <h1 class="fade-in fade-in-delay-1">
      The <span class="grad">Largest</span> Open-Source<br>AI Agent Skill Ecosystem
    </h1>
    <p class="tagline fade-in fade-in-delay-2">
      <span class="typing-wrap" id="typingTarget"></span><span class="typing-cursor" id="typingCursor"></span>
    </p>
    <div class="actions fade-in fade-in-delay-3">
      <a href="#quickstart" class="btn btn-primary">Get Started Free</a>
      <a href="https://github.com/oyi77/1ai-skills" class="btn btn-ghost" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        Star on GitHub
      </a>
    </div>
  </div>
</section>

<section class="stats">
  <div class="container">
    <div class="stats-inner">
      <div class="stat fade-in">
        <div class="num" data-target="{total}">0</div>
        <div class="label">Total Skills</div>
      </div>
      <div class="stat fade-in fade-in-delay-1">
        <div class="num" data-target="{len(cats)}">0</div>
        <div class="label">Categories</div>
      </div>
      <div class="stat fade-in fade-in-delay-2">
        <div class="num" data-target="{cats.get('cybersecurity', 0)}">0</div>
        <div class="label">Cybersecurity</div>
      </div>
      <div class="stat fade-in fade-in-delay-3">
        <div class="num" data-target="{cats.get('meta', 0)}">0</div>
        <div class="label">Self-Evolving</div>
      </div>
    </div>
  </div>
</section>

<section id="new">
  <div class="container">
    <div class="section-header">
      <div class="section-tag fade-in">Just Added</div>
      <h2 class="section-title fade-in">New Skills</h2>
      <p class="section-sub fade-in">Production-grade skills with anti-rationalization tables and code examples</p>
    </div>
    <div class="new-grid">
      {''.join(new_cards)}
    </div>
  </div>
</section>

<section id="categories">
  <div class="container">
    <div class="section-header">
      <div class="section-tag fade-in">Explore</div>
      <h2 class="section-title fade-in">{len(cats)} Categories</h2>
      <p class="section-sub fade-in">Skills organized by domain for easy discovery</p>
    </div>
    <div class="search-wrap fade-in">
      <span class="search-icon">&#128269;</span>
      <input type="text" id="catSearch" placeholder="Search categories...">
    </div>
    <div class="cat-grid" id="catGrid">
      {''.join(cat_cards)}
    </div>
    <div class="no-results" id="noResults" style="display:none">No categories match your search</div>
  </div>
</section>

<section id="quickstart">
  <div class="container">
    <div class="section-header">
      <div class="section-tag fade-in">Get Started</div>
      <h2 class="section-title fade-in">Install in Seconds</h2>
      <p class="section-sub fade-in">Works with Claude Code, Cursor, Gemini CLI, and more</p>
    </div>
    <div class="install-grid">
      <div class="install-card fade-in">
        <div class="install-card-header">
          <h3>Claude Code</h3>
          <span class="method">Recommended</span>
        </div>
        <div class="install-card-body">
          <p class="desc">Install via plugin marketplace for automatic skill discovery</p>
          <div class="code-block">
            <pre>/plugin marketplace add oyi77/1ai-skills
/plugin install 1ai-skills@1ai-skills</pre>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent)">Copy</button>
          </div>
        </div>
      </div>
      <div class="install-card fade-in fade-in-delay-1">
        <div class="install-card-header">
          <h3>Cursor</h3>
          <span class="method">Manual</span>
        </div>
        <div class="install-card-body">
          <p class="desc">Copy SKILL.md files into .cursor/rules/ directory</p>
          <div class="code-block">
            <pre>git clone https://github.com/oyi77/1ai-skills.git
cp -r 1ai-skills/cybersecurity/* .cursor/rules/</pre>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent)">Copy</button>
          </div>
        </div>
      </div>
      <div class="install-card fade-in fade-in-delay-2">
        <div class="install-card-header">
          <h3>Gemini CLI</h3>
          <span class="method">CLI</span>
        </div>
        <div class="install-card-body">
          <p class="desc">Install skills directly via Gemini CLI commands</p>
          <div class="code-block">
            <pre>gemini skills install https://github.com/oyi77/1ai-skills.git --path skills</pre>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(this.previousElementSibling.textContent)">Copy</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<footer>
  <div class="container footer-inner">
    <div class="footer-left">
      <span class="logo-sm">1ai-Skills</span>
      <span class="copy">&copy; 2026 1ai. MIT License.</span>
    </div>
    <div class="footer-links">
      <a href="https://github.com/oyi77/1ai-skills" target="_blank" rel="noopener">GitHub</a>
      <a href="https://github.com/oyi77/1ai-skills/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Contributing</a>
      <a href="https://github.com/oyi77/1ai-skills/blob/main/SECURITY.md" target="_blank" rel="noopener">Security</a>
    </div>
  </div>
</footer>

<script>
// Counter animation
const counters = document.querySelectorAll('.num[data-target]');
const observer = new IntersectionObserver(entries => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      const el = entry.target;
      const target = +el.dataset.target;
      const duration = 1500;
      const start = performance.now();
      const animate = now => {{
        const progress = Math.min((now - start) / duration, 1);
        el.textContent = Math.floor(progress * target).toLocaleString();
        if (progress < 1) requestAnimationFrame(animate);
        else el.textContent = target.toLocaleString();
      }};
      requestAnimationFrame(animate);
      observer.unobserve(el);
    }}
  }});
}}, {{threshold: 0.5}});
counters.forEach(c => observer.observe(c));

// Fade in
const fadeObserver = new IntersectionObserver(entries => {{
  entries.forEach(e => {{ if (e.isIntersecting) {{ e.target.classList.add('visible'); fadeObserver.unobserve(e.target); }} }});
}}, {{threshold: 0.1}});
document.querySelectorAll('.fade-in').forEach(el => fadeObserver.observe(el));

// Category search
const searchInput = document.getElementById('catSearch');
const catGrid = document.getElementById('catGrid');
const noResults = document.getElementById('noResults');
if (searchInput) {{
  searchInput.addEventListener('input', () => {{
    const q = searchInput.value.toLowerCase();
    let visible = 0;
    catGrid.querySelectorAll('.cat-card').forEach(card => {{
      const text = card.textContent.toLowerCase();
      const show = !q || text.includes(q);
      card.classList.toggle('hidden', !show);
      if (show) visible++;
    }});
    noResults.style.display = visible === 0 ? 'block' : 'none';
  }});
}}

// Typing effect
const phrases = [
  '{total}+ production-ready skills for AI agents',
  'Cybersecurity, trading, marketing, and more',
  'Works with Claude Code, Cursor, Gemini CLI',
  'Self-evolving meta-skills that improve over time',
  'The largest open-source skill library in the ecosystem',
];
let phraseIdx = 0, charIdx = 0, deleting = false;
const target = document.getElementById('typingTarget');
const cursor = document.getElementById('typingCursor');
function type() {{
  const phrase = phrases[phraseIdx];
  if (!deleting) {{
    target.textContent = phrase.slice(0, ++charIdx);
    if (charIdx === phrase.length) {{ deleting = true; setTimeout(type, 2000); return; }}
  }} else {{
    target.textContent = phrase.slice(0, --charIdx);
    if (charIdx === 0) {{ deleting = false; phraseIdx = (phraseIdx + 1) % phrases.length; }}
  }}
  setTimeout(type, deleting ? 30 : 60);
}}
type();

// Copy button feedback
document.querySelectorAll('.copy-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 2000);
  }});
}});
</script>
</body>
</html>'''

def main():
    data = load_skills()
    html_content = generate_html(data)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html_content, encoding='utf-8')
    print(f"Generated {OUTPUT} ({len(html_content)} bytes)")
    print(f"Skills: {data['total_skills']}, Categories: {data['category_count']}")

if __name__ == '__main__':
    main()
