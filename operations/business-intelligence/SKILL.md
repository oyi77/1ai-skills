---
name: business-intelligence
description: Business Intelligence. Use when relevant to this domain.
---
# Business Intelligence

BerkahKarya's single source of truth for all metrics that matter.

## KPI Framework

### North Star Metric
**Monthly Recurring Revenue (MRR)** → path to IDR 1B/year

### Level 1: Company Health (Weekly)
| Metric | Formula | Target | Current |
|--------|---------|--------|---------|
| Total Revenue | Sum all streams | IDR 50M/mo | IDR 0 |
| Revenue per Employee | Revenue / Team size | IDR 10M/person | IDR 0 |
| Burn Rate | Monthly expenses | < Revenue | Unknown |
| Runway | Cash / Burn rate | >90 days | 0 days |
| Revenue Growth | MoM % change | +20%/month | - |

### Level 2: Stream Performance (Daily)
| Stream | KPI | Target |
|--------|-----|--------|
| Affiliate | Click → Purchase rate | >2% |
| Digital Products | Sales/day | 1+/day |
| Trading | Win rate | >60% |
| Software | Pipeline value | IDR 100M |
| Talent | Active talents | 10+ |

### Level 3: Marketing Funnel (Daily)
| Stage | Metric | Target |
|-------|--------|--------|
| Awareness | Video views/day | 10K+ |
| Interest | Profile visits | 500+ |
| Consideration | Link clicks | 200+ |
| Purchase | Conversions | 5+ |
| Retention | Repeat buyers | 20% |

### Level 4: Content Performance (Per post)
| Metric | TikTok | Instagram | YouTube |
|--------|--------|-----------|---------|
| Views target | 10K | 1K | 500 |
| ER target | >5% | >3% | >4% |
| Click-through | >1% | >0.5% | >2% |

---

## Weekly Business Review Template

```markdown
# BerkahKarya Weekly Review — Week {N}, {Year}
**Review Date:** {date}
**Reviewed by:** Vilona (AI GM)

## Revenue Summary
- Total: IDR {total} ({vs_last_week} vs last week)
- Affiliate: IDR {affiliate}
- Products: IDR {products}  
- Trading: IDR {trading}
- Software: IDR {software}
- Talent: IDR {talent}

## Key Wins
1. {win_1}
2. {win_2}

## Key Problems
1. {problem_1} → Action: {action_1}
2. {problem_2} → Action: {action_2}

## Next Week Priorities
1. {priority_1} (Owner: {person})
2. {priority_2} (Owner: {person})
3. {priority_3} (Owner: {person})

## Business Kingdom Progress
- Milestone: {current_milestone}
- % to next milestone: {pct}%
- ETA: {eta}
```

---

## Data Collection Scripts

### scripts/weekly_metrics.py
```python
#!/usr/bin/env python3
"""Collect and report weekly metrics from all streams."""

import requests, json, datetime
from pathlib import Path

def get_postbridge_analytics():
    """Get social media post performance."""
    r = requests.get(
        "https://api.post-bridge.com/v1/analytics",
        headers={"Authorization": "Bearer REDACTED_ROTATED_CREDENTIAL"}
    )
    return r.json() if r.ok else {}

def get_gumroad_sales():
    """Check Gumroad sales (manual check via browser or API if available)."""
    # Gumroad API: https://gumroad.com/api#sales
    # Note: Requires OAuth token from Gumroad dashboard
    return {"sales": 0, "revenue_usd": 0}  # Update manually

def generate_report():
    postbridge = get_postbridge_analytics()
    gumroad = get_gumroad_sales()
    
    report = f"""
=== BERKAHKARYA WEEKLY METRICS ===
Date: {datetime.date.today()}

SOCIAL MEDIA (PostBridge):
  Posts scheduled this week: {postbridge.get('scheduled_count', 'N/A')}
  
DIGITAL PRODUCTS (Gumroad):
  Sales: {gumroad['sales']}
  Revenue: ${gumroad['revenue_usd']} USD

TRADING: Manual — check .vilona/knowledge/trading/trading_log.json

NEXT ACTIONS:
  - Check LYNK dashboard: https://lynk.id/v2/admin/dashboard
  - Check Gumroad: https://gumroad.com/dashboard
  - Review trading log
===================================
"""
    print(report)
    
    # Save to notes
    Path("logs").mkdir(exist_ok=True)
    with open(f"logs/weekly_metrics_{datetime.date.today()}.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    generate_report()
```

---

## Business Kingdom Scoreboard

```
🏆 BUSINESS KINGDOM PROGRESS TRACKER

Business Lines:
  ✅ Affiliate Marketing    Active (0 revenue — crisis)
  ✅ Digital Products       Active (1 product live, 0 sales)  
  🔄 Software House         Building (0 clients)
  🔄 Talent Agency          Building (0 talents signed)
  🔄 Quant Fund             Building (paper trading)

Infrastructure:
  ✅ Content automation     90% complete
  ✅ Social scheduling      Active (PostBridge)
  ✅ AI GM (Vilona)         Operational
  ✅ Telegram automation    Active
  🔄 Finance tracking       Building
  🔄 CRM system             Building
  ❌ Live trading           Not started
  ❌ Client portal          Not started

Team:
  Paijo (CEO)    ✅ Active
  Veris (Mkt)    ✅ Active
  Sony (Ops)     ✅ Active
  Nuno (Trade)   ✅ Active
  Vilona (AI GM) ✅ 24/7 Active

Overall Progress: 35% → Business Kingdom
Current Phase: SURVIVAL → STABILITY → GROWTH → SCALE → KINGDOM
```

---

## Competitor Intelligence

Track these companies monthly:
- **Kompas Gramedia**: Media empire model
- **KumparanBusiness**: Digital media playbook
- **GDP Venture**: Multi-portfolio approach
- **East Ventures**: Scale-up strategies

Key questions:
1. How fast did they grow from IDR 0 to IDR 1B?
2. What was their first profitable product?
3. What systems did they build early?
4. What mistakes can we avoid?
