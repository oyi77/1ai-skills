# Lead Generation Pipeline — BerkahKarya

**Skill:** `lead-gen-pipeline`  
**Version:** 1.0.0  
**Brand:** BerkahKarya Digital Agency  
**Target:** Indonesian SMBs needing AI/digital marketing services  

---

## Overview

Automated B2B lead generation pipeline that:
1. **Searches** for Indonesian SMBs via web search
2. **Scrapes** basic company info from search results
3. **Qualifies** each lead with a score 0–100
4. **Generates** personalized outreach (WhatsApp + Email) in Bahasa Indonesia
5. **Tracks** all leads in CSV + daily markdown summary

No API keys required — uses built-in `web_search` tool for discovery.

---

## Quick Start

```bash
cd /home/openclaw/.openclaw/workspace/skills/lead-gen-pipeline

# Dry run — see what would happen, no file writes
python3 leadgen.py --dry-run --industry fnb --location jakarta --limit 5

# Live run — scrape + qualify + generate outreach
python3 leadgen.py --industry retail --location bandung --limit 10

# Run all industries at once
python3 leadgen.py --all-industries --location surabaya --limit 5

# Different locations
python3 leadgen.py --industry fashion --location yogyakarta --limit 20
```

---

## CLI Flags

| Flag | Options | Default | Description |
|------|---------|---------|-------------|
| `--industry` | `fnb`, `retail`, `fashion`, `beauty`, `education` | `fnb` | Target industry |
| `--all-industries` | — | off | Run all 5 industries sequentially |
| `--location` | any string | `jakarta` | City/region to search |
| `--limit` | integer | `10` | Max leads per industry run |
| `--dry-run` | — | off | Parse + score but do NOT write CSV/files |
| `--output` | file path | `output/leads.csv` | Custom CSV output path |
| `--min-score` | 0–100 | `40` | Only save leads above this score |
| `--summary` | — | off | Print daily markdown summary to stdout |

---

## Lead Scoring (0–100)

Leads are scored across 4 dimensions:

| Dimension | Max Score | What We Check |
|-----------|-----------|---------------|
| **Company Size** | 25 pts | Employee count signals, branch mentions |
| **Social Presence** | 25 pts | Instagram/TikTok/Facebook mention in search snippets |
| **Digital Maturity** | 25 pts | Has website, uses online ordering, e-commerce presence |
| **Industry Fit** | 25 pts | Industry keyword alignment, growth signals |

**Tiers:**
- 🟢 **Hot (75–100):** Immediate outreach — strong fit, ready to buy
- 🟡 **Warm (50–74):** Nurture sequence — some digital presence, educate first
- 🟠 **Cold (25–49):** Long-term nurture — early digital adopters
- 🔴 **Skip (0–24):** Not qualified — likely offline-only or too small

---

## Output Files

### `output/leads.csv`
Columns:
```
timestamp, name, industry, location, website, phone, instagram, source_url,
score, tier, size_score, social_score, digital_score, industry_score,
notes, outreach_channel, outreach_status, follow_up_date
```

### `output/summary_YYYY-MM-DD.md`
Daily markdown summary with:
- Total leads found/qualified
- Score distribution by tier
- Top 5 leads by score
- Industry breakdown
- Suggested outreach priorities

---

## Industry Targeting

### FnB (Restoran, Kafe, Catering)
- Query: `resto kafe catering [location] instagram tiktok`
- Pain points: menu digital, pesan online, viral konten
- Key signal: has Instagram but no website

### Retail (Toko, Minimarket, Oleh-oleh)
- Query: `toko retail oleh-oleh [location] online shop`
- Pain points: katalog digital, marketplace presence, promo automation
- Key signal: mentions Tokopedia/Shopee but no own website

### Fashion (Butik, Distro, Konveksi)
- Query: `butik distro konveksi fashion [location] online`
- Pain points: lookbook digital, influencer marketing, size guide automation
- Key signal: Instagram active, no TikTok

### Beauty (Salon, Spa, Klinik Kecantikan)
- Query: `salon spa klinik kecantikan [location] booking online`
- Pain points: booking system, before-after content, loyalty program
- Key signal: WhatsApp booking, no automated system

### Education (Kursus, Bimbel, Pelatihan)
- Query: `kursus bimbel pelatihan [location] daftar online`
- Pain points: lead gen automation, student tracking, content marketing
- Key signal: WhatsApp group for registrations

---

## Outreach Templates

### WhatsApp (Indonesian)
Located at: `templates/whatsapp_templates.md`
- Industry-specific opening hooks
- Pain-point-focused messaging
- Social proof (BerkahKarya portfolio)
- CTA: Free audit consultation

### Email (Indonesian + English headers)
Located at: `templates/email_templates.md`
- Cold outreach (first contact)
- Warm follow-up (after engagement)
- Follow-up #2 (7 days after first contact)
- Proposal send (after discovery call)
- Nurture (monthly value-add)

---

## Rate Limiting

The pipeline includes built-in rate limiting:
- **Search:** 2-second delay between queries
- **Scrape:** 3-second delay between page fetches
- **Batch:** 10-second pause after every 10 leads

Configurable via `RATE_LIMIT_SEARCH`, `RATE_LIMIT_SCRAPE` constants in `leadgen.py`.

---

## File Structure

```
skills/lead-gen-pipeline/
├── SKILL.md                        ← This file
├── leadgen.py                      ← Main pipeline script
├── output/
│   ├── leads.csv                   ← Accumulated leads database
│   └── summary_YYYY-MM-DD.md       ← Daily summaries (auto-generated)
└── templates/
    ├── whatsapp_templates.md       ← WA outreach per industry
    └── email_templates.md          ← 5 email templates
```

---

## Integration with BerkahKarya Workflow

1. **Run daily:** `python3 leadgen.py --all-industries --location jakarta --limit 10`
2. **Review summary:** Check `output/summary_YYYY-MM-DD.md`
3. **Hot leads first:** Send WA to score ≥ 75 within same day
4. **Warm leads:** Add to 7-day email nurture sequence
5. **Track responses:** Update `outreach_status` column in CSV

---

## Error Handling

- Network errors → retry 3x with exponential backoff
- Search quota → graceful skip with warning
- Malformed results → log and continue (no crash)
- CSV write errors → fallback to stdout JSON dump

---

## Dependencies

- Python 3.8+
- Standard library only: `csv`, `json`, `re`, `time`, `datetime`, `argparse`, `urllib`
- Uses OpenClaw `web_search` tool via subprocess or direct API call (auto-detected)
- No pip installs required

---

*BerkahKarya — Turning Searches into Revenue* 🔥
