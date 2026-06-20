---
name: revenue-engine
description: Manage revenue pipelines, track Stripe/analytics metrics, and automate financial reporting for SaaS businesses.
domain: core
tags:
- engine
- infrastructure
- memory
- pipeline
- revenue
- self-improvement
---
# Revenue Engine

Vilona's revenue generation brain. Knows all income streams, their status, and exactly what to do when they underperform.

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Revenue Stream Map
This section covers revenue stream map for the revenue-engine skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### Stream 1: Affiliate Marketing (LYNK + platforms)
```
Products:     lynk.id/jendralbot (12 products, IDR 49K-89K)
Channels:     TikTok (7 accounts) + Instagram (1) + YouTube + Facebook
Tool:         PostBridge API (REDACTED_ROTATED_CREDENTIAL)
Schedule:     18 posts/day (6/platform)
Target:       IDR 5M/month (56+ sales)
Current:      IDR 0 (Day 5 crisis)
```

**Daily action:**
1. Check scheduled posts count (`GET /v1/posts?status=scheduled`)
2. If <18 posts today → schedule immediately
3. Check analytics (`GET /v1/analytics`) → optimize top performing

### Stream 2: Digital Products (Gumroad)
```
Product:      Python Automation Pack $15 → dizzuddi.gumroad.com/l/nvadun
Dashboard:    gumroad.com/dashboard
Account:      dizzuddi (muchammadizzuddin@gmail.com)
Target:       5 sales/week ($75 = IDR 1.2M/week)
Current:      0 sales
```

**Growth levers:**
- Drive traffic from TikTok content (30K-100K views/video)
- Add 2-3 more products at $7, $25, $49 price points
- Build email list from buyers for upsells
- Cross-promote on Twitter/X (@this_is_paijo)

**Product pipeline (build these):**
1. Trading Journal Template (Excel) — $7
2. Social Media Content Calendar 2025 — $9
3. AI Prompt Library (500 prompts) — $19
4. Complete Automation Business Kit — $49

### Stream 3: Trading (XAUUSD)
```
Strategy:     7-candle breakout, Asia session
Entry time:   15:00 UTC+7 (08:00 UTC)
Win rate:     61.4% (backtested)
Risk/trade:   $10 (paper) → $100 (live when verified)
Target:       $528/month = IDR 8.4M
Current:      Paper trading (not started yet)
```

**Daily action (Asia session):**
1. 07:00-14:50 UTC+7: Monitor 15min candles
2. 14:50: Calculate 7-candle range
3. 15:00: If range ≥5 pips → enter breakout
4. Log to .vilona/knowledge/trading/trading_log.json

### Stream 4: Software House Services
```
Services:     AI automation, web apps, bots, data pipelines
Pricing:      IDR 5M (small), 15M (medium), 50M (enterprise)
Pipeline:     0 clients
Target:       1 client/month @ IDR 15M avg
```

**Lead sources:**
- Facebook Groups: "Komunitas Developer Indonesia", "Jasa Pembuatan Website"
- LinkedIn: Indonesian SME owners
- Referrals from existing network
- Cold DM via telegram-userbot

### Stream 5: Talent Agency Commissions
```
Model:        20-30% commission on creator deals
Deal size:    IDR 1M-50M per brand deal
Target:       IDR 50M pipeline, IDR 10M commission/month
Current:      0 talent signed
```

**Talent pipeline:**
1. Scout creators (10K-500K followers, ER >3%)
2. Pitch partnership → sign talent agreement
3. Connect with brands → negotiate deal
4. Execute → collect commission

---

## Revenue Dashboard (Terminal)

```
╔══════════════════════════════════════════════════════╗
║         BERKAHKARYA REVENUE DASHBOARD                ║
║         {date} | Gap: {gap}h                         ║
╠══════════════════════════════════════════════════════╣
║ STREAM          TODAY    WEEK     MONTH   TARGET     ║
╠══════════════════════════════════════════════════════╣
║ Affiliate       {aff}    {aff_w}  {aff_m} IDR 5M    ║
║ Products        {prd}    {prd_w}  {prd_m} IDR 10M   ║
║ Trading         {trd}    {trd_w}  {trd_m} IDR 8.4M  ║
║ Software        {sft}    {sft_w}  {sft_m} IDR 15M   ║
║ Talent          {tal}    {tal_w}  {tal_m} IDR 10M   ║
╠══════════════════════════════════════════════════════╣
║ TOTAL           {tot}    {tot_w}  {tot_m} IDR 48.4M ║
╠══════════════════════════════════════════════════════╣
║ Cash balance:   {cash}                               ║
║ Burn rate:      {burn}/day                           ║
║ Runway:         {runway} days                        ║
╚══════════════════════════════════════════════════════╝
```

---

## Revenue Recovery Playbook
This section covers revenue recovery playbook for the revenue-engine skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### If zero revenue for 24h:
```
1. Check PostBridge: are posts going out?
   - If no → schedule 25 posts immediately
   - If yes → check LYNK analytics (are links getting clicks?)

2. Check Gumroad: any abandoned carts?
   - If yes → create urgency email (no email list yet → create one)
   - If no → create new TikTok video driving to product

3. Activate emergency lead gen:
   - Post in 5 Facebook groups
   - Send 10 cold DMs via telegram to warm contacts
   - Create time-limited discount on Gumroad (15% off → $12.75)

4. Alert Veris and get marketing help
```

### If PostBridge fails:
```
1. Test API directly: curl -H "Authorization: Bearer pb_live_..." https://api.post-bridge.com/v1/posts
2. If API down → post manually to 3 most important accounts
3. Create backup scheduler (simple Python cron)
4. Report to PostBridge support: support@post-bridge.com
```

### New product creation (when stuck):
```
Research (30 min):
- Check trending on TikTok: digital products Indonesia
- Check Gumroad bestsellers: gumroad.com/discover
- Check Tokopedia digital: what's selling

Create (2 hours):
- Write product in Notion/Google Doc
- Export as PDF
- Create cover image (Canva)
- Upload to Gumroad
- Write product description (SEO optimized)
- Create 3 TikTok videos promoting

Launch same day.
```

---

## Automated Revenue Scripts
This section covers automated revenue scripts for the revenue-engine skill.
Key operations include input validation, core processing, and output verification.
Refer to the skill overview for detailed usage instructions.


### scripts/revenue_monitor.py
```python
#!/usr/bin/env python3
"""Run every 2h via cron. Checks all revenue streams. Alerts if gap detected."""
import requests, json, datetime

POSTBRIDGE_KEY = "REDACTED_ROTATED_CREDENTIAL"

def check_postbridge():
    r = requests.get("https://api.post-bridge.com/v1/posts",
                     headers={"Authorization": f"Bearer {POSTBRIDGE_KEY}"},
                     params={"status": "scheduled", "limit": 1})
    scheduled = r.json().get('meta', {}).get('total', 0)
    return scheduled > 0, scheduled

def check_gap():
    # Read from daily memory file
    today = datetime.date.today().strftime("%Y-%m-%d")
    try:
        with open(f"memory/{today}.md") as f:
            content = f.read()
        # Simple heuristic: look for last revenue mention
        return 0  # TODO: implement real gap calc
    except:
        return 999

def main():
    has_posts, count = check_postbridge()
    gap = check_gap()
    
    status = "✅ OK" if has_posts and gap < 4 else "⚠️ WARNING" if gap < 8 else "🚨 CRITICAL"
    print(f"{status} | Scheduled: {count} posts | Gap: {gap}h")
    
    if not has_posts:
        print("ACTION: Schedule posts immediately!")
    if gap >= 8:
        print("ACTION: Contact Veris - marketing emergency!")

if __name__ == "__main__":
    main()
```

### Cron setup:
```cron
# Revenue monitor every 2 hours
0 */2 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/revenue_monitor.py >> logs/revenue_monitor.log 2>&1

# Daily revenue report 9AM
0 9 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/daily_report.py >> logs/daily_report.log 2>&1

# Schedule posts daily 06:00 (before morning peak)
0 6 * * * cd /home/openclaw/.openclaw/workspace && python3 scripts/schedule_daily_posts.py >> logs/scheduler.log 2>&1
```

---

## Business Kingdom Revenue Milestones

| Milestone | Revenue/Month | Timeline | Key Lever |
|-----------|--------------|----------|-----------|
| Survival | IDR 5M | Month 1 | Affiliate + products |
| Stable | IDR 20M | Month 3 | + 1 software client |
| Growing | IDR 50M | Month 6 | + Talent agency |
| Scaling | IDR 200M | Year 1 | All 5 lines |
| Kingdom | IDR 1B | Year 2 | Scaled systems |
| Empire | IDR 10B | Year 5 | Business Kingdom complete |

---

## Integration Points

```
revenue-engine →  finance-tracker      (track & report)
              →  content-generator     (create driving content)
              →  postbridge-social-manager  (schedule & post)
              →  telegram-userbot      (alert escalation)
              →  talent-crm            (talent revenue tracking)
              →  b2b-sales-automation  (software house revenue)
```

## When to Use

- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
