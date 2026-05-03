# Competitor Intelligence & Business Espionage

Full competitive intelligence on any business — social media, revenue estimation,
tech stack, funnel, ad strategy, business model, and clone blueprint.

---

## 📦 Dependencies & Tools Required

### External CLIs (must be installed & configured)

| Tool | Required For | Install | Config |
|------|-------------|---------|--------|
| `twitter` (twitter-cli) | Social spy, content spy | `pip install twitter-cli` | Set `TWITTER_AUTH_TOKEN` + `TWITTER_CT0` env vars (from browser cookies) |
| `whois` | Domain age, registrar | `apt install whois` | None |
| `oracle` CLI | LLM summarization (competitor_intel.py) | Pre-installed in OpenClaw | Needs `OMNIROUTE_KEY` or `OPENAI_API_KEY` |

### Python Packages

```bash
pip install telethon          # bot_spy module (Telegram bot extraction)
# urllib, subprocess, re, json, asyncio — stdlib (no install needed)
```

### Environment Variables

```bash
# Twitter-CLI auth (get from browser DevTools → Cookies → twitter.com)
export TWITTER_AUTH_TOKEN="your_auth_token"
export TWITTER_CT0="your_ct0_token"

# For competitor_intel.py LLM
export OPENAI_API_KEY="sk-..."         # or use omniroute
# OR
export OMNIROUTE_KEY="omniroute"       # default if using OpenClaw
```

### Telethon Sessions (for bot_spy module)

Pre-configured sessions at `/home/openclaw/.openclaw/workspace/.vilona/sessions/`:
- `paijo.session` → @codergaboets
- `alwayscuanbos.session` → @alwayscuanbos

Add new session:
```bash
python3 /home/openclaw/.openclaw/workspace/scripts/telethon_add_session.py \
  request-code +62xxx    # Step 1: request OTP
python3 ... add <name> +62xxx <otp> [2fa_password]  # Step 2: sign in
```

---

## 🚀 Scripts

### `biz_spy.py` — Main Business Espionage Engine

**What it does:** Full intelligence on any business via 9 modules

```bash
# Quick start — social + tech + funnel + revenue + model
python3 scripts/biz_spy.py --target "@targetbot" --modules social,tech,funnel,revenue,model

# All modules (takes 2-5 min)
python3 scripts/biz_spy.py --target "competitor.com" --all

# Bot intelligence only
python3 scripts/biz_spy.py --target "@somebot" --modules bot

# Save to file
python3 scripts/biz_spy.py --target "@targetbot" --all --output reports/target_intel.json
```

**Available modules:**

| Module | What it does | Tools Used | Speed |
|--------|-------------|------------|-------|
| `social` | Twitter/X posts, views, hooks, engagement | twitter-cli | ~5s |
| `ads` | Facebook Ad Library active ads count | urllib | ~3s |
| `funnel` | Landing page pricing, payment, trust signals | urllib | ~5s |
| `revenue` | Monthly revenue estimate (traffic × CVR × AOV) | calculation | instant |
| `bot` | Full Telegram bot architecture (calls bot-extractor) | Telethon | ~60s |
| `tech` | Framework, hosting, CDN, pixels, WHOIS | urllib + whois | ~5s |
| `content` | Content themes, hooks, formats (alias for social) | twitter-cli | ~5s |
| `seo` | Traffic estimate, keywords (basic) | urllib | ~5s |
| `model` | Synthesize business model from all data | calculation | instant |

**Output:** Markdown intelligence report + JSON data file

**Known limitations:**
- Social spy: Twitter only (no TikTok/Instagram scrape yet — need logged-in browser)
- Ads spy: Facebook Ad Library count only (no creative details without browser)
- Revenue: estimate only (±50% accuracy), based on traffic model
- Tech spy: works on websites only (not Telegram bots)

---

### `competitor_intel.py` — Quick LLM-powered Research

**What it does:** Web search + LLM summary of competitor

```bash
# Research by name
python3 scripts/competitor_intel.py --name "Vidabot"

# Research by URL
python3 scripts/competitor_intel.py --url "https://vidabot.com"

# Focus areas
python3 scripts/competitor_intel.py --name "Vidabot" --focus "pricing,features,marketing"
```

**Requires:** `openai` package + API key or OmniRoute

---

## 🔄 Full Workflow

```
1. IDENTIFY target
   └── Get: website URL, @telegrambot, social handles

2. QUICK SCAN (~30 sec)
   python3 scripts/biz_spy.py --target "@bot" --modules social,tech,revenue,model

3. DEEP DIVE (if needed, ~5 min)
   python3 scripts/biz_spy.py --target "@bot" --all

4. READ REPORT
   └── reports/<target>_<timestamp>.json

5. ACT
   ├── Clone → use bot-extractor skill for Telegram bots
   ├── Improve own → extract gaps, apply to BerkahKarya
   └── Counter → find weaknesses, exploit in own strategy
```

---

## 📊 Case Studies

### @vidabot_generator_bot (2026-03-21)

| Intel | Value |
|-------|-------|
| Twitter avg views | 59,160/post |
| Engagement rate | 0.7% |
| Revenue estimate | IDR 88M - 1B/month |
| Bot UX score | 90/100 |
| Clone effort | 2-3 weeks |
| Main weakness | Dead buttons, no /help, no /cancel |
| Opportunity | Subscription model, better UX |

---

## ⚠️ Gaps & Roadmap

### Not Yet Implemented
- [ ] TikTok content spy (needs logged-in browser session)
- [ ] Instagram spy (needs login)
- [ ] Facebook Ad Library creative scraping (needs browser)
- [ ] Similarweb traffic data (needs API key or browser)
- [ ] Shopee/Tokopedia product sales scraping
- [ ] LYNK.id product analysis
- [ ] YouTube channel analysis
- [ ] Automated comparison report (own vs competitor)

### Partially Implemented
- [~] Ads spy — count only, no creative details
- [~] SEO spy — basic only, no keyword data
- [~] Revenue spy — estimate only, ±50% accuracy

### Fully Working
- [x] Social spy (Twitter)
- [x] Bot spy (Telegram, via Telethon)
- [x] Tech spy (websites)
- [x] Funnel spy (public websites)
- [x] Model synthesis
- [x] Report generation
- [x] Revenue estimation

---

## 📁 File Structure

```
research/competitor-intel/
├── README.md                    ← This file
├── SKILL.md                     ← Skill spec
├── scripts/
│   ├── biz_spy.py              ← Main espionage engine (9 modules)
│   └── competitor_intel.py     ← Quick LLM research
├── references/
│   └── vidabot_generator_bot_arch.json  ← Example extracted architecture
└── reports/                     ← Generated intelligence reports (gitignored)
```
