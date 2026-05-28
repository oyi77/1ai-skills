---
name: b2b-sales-automation
version: "1.0.0"
description: >
  Full B2B sales pipeline automation for BerkahKarya — from cold prospect to onboarded client.
  Covers ICP definition, lead sourcing, outreach sequences, proposal generation, CRM tracking,
  and deal alerts via Telegram. Targets Indonesian SMEs needing AI automation, digital products,
  and content services.
author: Vilona / BerkahKarya
language: id-ID / en
tags: [sales, b2b, crm, outreach, proposal, pipeline, indonesian]
scripts:
  - scripts/lead_scorer.py
  - scripts/proposal_gen.py
  - scripts/outreach_sequencer.py
---

# B2B Sales Automation Skill 🔥

Complete B2B sales pipeline: **Prospect → Qualify → Demo → Proposal → Negotiate → Close → Onboard**

---

## 1. Ideal Customer Profile (ICP)

### Primary ICP: Indonesian SME AI Adopter

| Attribute | Target |
|-----------|--------|
| Company size | 5–200 karyawan |
| Revenue | IDR 500M – 50B/year |
| Industry | E-commerce, F&B, Retail, Jasa, Konsultan |
| Pain point | Manual processes, kurang konten, butuh otomasi |
| Decision maker | Owner, Direktur, Manager Ops, HRD |
| Tech readiness | Punya WA Business, pakai Google Workspace/Tokopedia |
| Budget range | IDR 5M – 50M/project |

### Secondary ICP: Digital Business Owner

| Attribute | Target |
|-----------|--------|
| Type | Personal brand, online store, agency kecil |
| Need | Konten viral, lead gen, AI tools |
| Budget | IDR 5M – 15M/project |
| Channel | Instagram, TikTok, WhatsApp |

### Disqualification Criteria (DQ)
- Budget < IDR 5M (too small, low ROI effort)
- No decision-making authority (hanya staff)
- Strictly price-shopping / always asking for free
- Competitor in the same niche (content/AI)
- Government project (procurement process too slow)

---

## 2. Lead Sources

### 2A. LinkedIn
```bash
# Search filters
- Industry: IT, Marketing, Retail, Consulting (Indonesia)
- Title: Owner, Direktur, CEO, Founder, GM Operasional
- Company size: 11–200 employees
- Location: Jakarta, Surabaya, Bandung, Bali, Medan

# Action steps
1. Connect with personalized note (see template below)
2. Wait 3 days → send intro DM
3. Move to outreach sequence if responded
```

### 2B. Google Maps (Local Business)
```bash
# Search queries
"konsultan digital marketing Jakarta"
"toko online Surabaya"
"klinik kecantikan Bandung"
"restoran franchise Jakarta"
"jasa akuntansi Bali"

# Data to capture per lead
- Business name
- Phone / WA number
- Website (if any)
- Google rating + review count
- Owner name (from Google Business)
```

### 2C. Industry Directories
- **Tokopedia/Shopee:** Official stores with high review counts
- **Glints/LinkedIn Jobs:** Companies actively hiring (growing = budget)
- **KADIN / HIPMI:** Member directories
- **Clutch.co:** Companies seeking digital services
- **Yellow Pages Indonesia:** Traditional businesses going digital

### 2D. Referrals
```
Referral request template (WA/Telegram):
"Hei [Nama], ada ga temen/kolega lo yang lagi butuh 
bantuan AI automation atau konten digital? 
Kita lagi buka 3 slot klien baru bulan ini. 
Ada komisi 10% dari deal yang jadi 🔥"
```

---

## 3. Pipeline Stages

```
PROSPECT → QUALIFY → DEMO → PROPOSAL → NEGOTIATE → CLOSE → ONBOARD
   🔍          📋       🎯       📄          💬         🤝       🚀
```

### Stage Definitions & Criteria

| Stage | Entry Criteria | Exit Criteria | Target Duration |
|-------|---------------|---------------|-----------------|
| **Prospect** | Lead identified, contact info captured | First outreach sent | Day 1 |
| **Qualify** | Responded to outreach | BANT confirmed (Budget, Authority, Need, Timeline) | Day 2–7 |
| **Demo** | Meeting scheduled | Demo/discovery call completed | Day 7–14 |
| **Proposal** | Demo done, interest confirmed | Proposal sent | Day 14–17 |
| **Negotiate** | Proposal reviewed | Final price/scope agreed | Day 17–25 |
| **Close** | Agreement reached | Contract signed, DP received | Day 25–30 |
| **Onboard** | Deal closed | Kickoff done, deliverables started | Day 30–45 |

### Probability by Stage

| Stage | Win Probability |
|-------|----------------|
| Prospect | 5% |
| Qualify | 20% |
| Demo | 40% |
| Proposal | 60% |
| Negotiate | 75% |
| Close | 95% |
| Onboard | 100% |

---

## 4. Cold Outreach Templates (Bahasa Indonesia)

### 4A. Email Cold Outreach

**Subject options:**
- `[Nama Perusahaan] — 1 ide untuk tingkatkan penjualan 30%`
- `Bisa kita ngobrol 15 menit, [Nama]?`
- `Solusi AI untuk [industri] — cocok ga untuk [Nama Perusahaan]?`

**Email Body (Template 1 — Pain-focused):**
```
Halo [Nama],

Saya [Nama Anda] dari BerkahKarya.

Tim kami baru selesai bantu [klien sejenis] otomasi proses 
[operasional/konten/customer service] mereka — hasilnya hemat 
40 jam kerja/bulan dan closing rate naik 25%.

Relevan ga untuk [Nama Perusahaan]? 

Kalau iya, boleh minta 15 menit untuk sharing caranya?

Salam,
[Nama]
BerkahKarya | AI & Digital Solutions
WA: +62xxx
```

**Email Body (Template 2 — Curiosity-hook):**
```
Halo [Nama],

Satu pertanyaan singkat:

Kalau ada cara untuk [bisnis Anda] dapat 50 leads baru per bulan 
secara otomatis — tanpa tambah tim — mau tau caranya?

Kami baru bantu [industri sejenis] di [kota] lakukan ini.

Boleh 15 menit call minggu ini?

— [Nama Anda], BerkahKarya
```

### 4B. WhatsApp Cold Outreach

**Template 1 — Warm intro:**
```
Halo [Nama] 👋

Saya [Nama] dari BerkahKarya. Ketemu profil [Nama Perusahaan] 
di [sumber] dan tertarik dengan bisnis Anda.

Kami bantu bisnis di [industri] otomasi proses pakai AI — 
khususnya untuk [pain point relevan].

Boleh sharing singkat pengalaman klien kami yang relevan? 
Cuma 5 menit aja 🙏
```

**Template 2 — Direct value:**
```
Halo [Nama]!

Quick question: sekarang [Nama Perusahaan] handle berapa 
inquiry/hari secara manual?

Kami punya sistem AI yang bisa otomasi sampai 80% dari 
proses itu. Hemat waktu + biaya signifikan.

Mau lihat demo singkatnya? 15 menit aja ✅
```

**Template 3 — Referral mention:**
```
Halo [Nama], perkenalkan saya [Nama] 👋

Dapat kontak Anda dari [nama referral]. Beliau bilang 
[Nama Perusahaan] lagi butuh solusi untuk [problem].

Kami spesialis di situ. Boleh ngobrol sebentar?
```

### 4C. Telegram DM

```
Hey [Nama] 👋

Ketemu profil lo di [grup/channel]. Gue [Nama] dari BerkahKarya.

Kita bantu bisnis kayak [jenis bisnis lo] scale pakai AI automation.
Yang terbaru: bantu [klien] dari 0 ke [result] dalam [timeframe].

Lo lagi ngejar target apa sekarang? Mungkin bisa gue kasih 
1-2 ide yang langsung bisa lo implement 🔥
```

---

## 5. Follow-Up Sequences

### 5A. 3-Touch Sequence (Cold → Lukewarm)

```
Day 1:  📧 First outreach (email/WA/TG)
Day 4:  📞 Follow-up #1 — value-add (kirim artikel/case study relevan)
Day 9:  🔥 Follow-up #2 — last attempt ("Mau tutup thread ini, 
             tapi sebelumnya mau kasih tau satu hal...")
```

**Touch 2 Template:**
```
Halo [Nama],

Follow up dari pesan saya [X] hari lalu 🙏

Sambil nunggu, saya mau share case study singkat:
[Klien sejenis] berhasil [hasil spesifik] dalam [waktu] 
dengan pendekatan yang sama yang bisa kami terapkan 
untuk [Nama Perusahaan].

[Link/attachment case study]

Masih relevan untuk dibahas? 15 menit saja ✅
```

**Touch 3 Template (Break-up):**
```
Halo [Nama],

Saya paham Anda pasti sibuk. Ini pesan terakhir dari saya.

Sebelum saya tutup thread ini — ada 1 hal yang mau saya 
sampaikan khusus untuk [Nama Perusahaan]:

[Insight spesifik tentang industri mereka + opportunity]

Kalau timing-nya belum tepat sekarang, tidak apa-apa. 
Tapi kalau Anda mau ngobrol di masa depan, 
saya tetap ada di sini.

Salam,
[Nama]
```

### 5B. 5-Touch Sequence (Warm Lead)

```
Day 1:   📧 Initial outreach
Day 3:   💬 WA/Telegram follow-up (multi-channel)
Day 7:   🎁 Value delivery (free audit/insight)
Day 12:  📞 Phone call attempt
Day 18:  🔥 Final "break-up" message + special offer
```

**Touch 3 — Free Value (Audit Offer):**
```
Halo [Nama] 👋

Gimana kalau saya kasih FREE digital readiness audit 
untuk [Nama Perusahaan]? 

Prosesnya: 30 menit Zoom, kita review proses bisnis Anda,
saya kasih 3-5 rekomendasi konkret yang bisa langsung dijalankan.

No strings attached. Pure value dulu.

Mau jadwalin? 🙏
```

---

## 6. Pricing Tiers & Proposal Generator

### Pricing Architecture

| Tier | Package | Price | Target Client | Deliverables |
|------|---------|-------|---------------|--------------|
| **Starter** | AI Jumpstart | IDR 5M | Solopreneur/startup | Audit + 1 automation tool + 1 month support |
| **Growth** | AI Growth Engine | IDR 15M | SME 10-50 karyawan | Full audit + 3 automations + konten strategy + 3 bulan support |
| **Scale** | AI Business Transformation | IDR 50M | SME 50-200 karyawan | Custom AI system + integrasi + training + 6 bulan support |

### Proposal Structure
```markdown
# PROPOSAL KERJASAMA
## [Nama Perusahaan] × BerkahKarya

**Tanggal:** [Date]
**Valid until:** [Date + 14 days]
**Prepared by:** [Nama], BerkahKarya

---

### Executive Summary
[2-3 kalimat tentang pain point klien dan solusi kita]

### Pemahaman Kami tentang [Nama Perusahaan]
- Situasi saat ini: [problem]
- Dampak ke bisnis: [cost/opportunity lost]
- Yang Anda butuhkan: [solution in their words]

### Solusi yang Kami Rekomendasikan
**[Nama Package]** — IDR [harga]

Deliverables:
1. [Item 1]
2. [Item 2]
3. [Item 3]

Timeline: [X minggu/bulan]

### Investasi
| Item | Harga |
|------|-------|
| [Deliverable 1] | IDR X |
| [Deliverable 2] | IDR X |
| **TOTAL** | **IDR X** |

**Syarat Pembayaran:** 50% DP, 50% setelah delivery

### Mengapa BerkahKarya?
- [Credibility point 1]
- [Credibility point 2]
- [Case study result]

### Next Steps
1. Setujui proposal ini
2. Tanda tangan MOU
3. Transfer DP 50%
4. Kickoff meeting [tanggal]

---
*Questions? WA: +62xxx | Email: xxx@berkahkarya.com*
```

---

## 7. CRM Tracking Schema

### Deal Record (JSON/CSV)

```json
{
  "deal_id": "BK-2026-001",
  "company": "PT Maju Bersama",
  "contact_name": "Budi Santoso",
  "contact_title": "Owner",
  "contact_wa": "+62812xxxxxxx",
  "contact_email": "budi@majubersama.com",
  "lead_source": "LinkedIn",
  "icp_score": 8.5,
  "stage": "Proposal",
  "package": "AI Growth Engine",
  "deal_value": 15000000,
  "probability": 60,
  "next_action": "Follow up proposal - Day 3",
  "next_action_date": "2026-03-16",
  "close_date_target": "2026-03-30",
  "created_at": "2026-03-01",
  "last_updated": "2026-03-13",
  "notes": "Interested in WA automation. Decision by end March.",
  "stage_history": [
    {"stage": "Prospect", "date": "2026-03-01"},
    {"stage": "Qualify", "date": "2026-03-05"},
    {"stage": "Demo", "date": "2026-03-10"},
    {"stage": "Proposal", "date": "2026-03-13"}
  ]
}
```

### CRM Commands

```bash
# View pipeline
python3 scripts/lead_scorer.py --list --stage all

# Score new lead
python3 scripts/lead_scorer.py --score --company "PT ABC" --data lead_data.json

# Update deal stage
python3 scripts/lead_scorer.py --update --deal-id BK-2026-001 --stage Negotiate

# Pipeline report
python3 scripts/lead_scorer.py --report --format telegram
```

---

## 8. Scripts Reference

### 8A. `scripts/lead_scorer.py`

**Purpose:** Score leads based on ICP criteria, manage CRM records

```python
# Usage
python3 scripts/lead_scorer.py [OPTIONS]

Options:
  --score           Score a new lead (interactive or --data file)
  --list            List all deals [--stage STAGE] [--min-score N]
  --update          Update deal stage/info
  --report          Generate pipeline report [--format telegram|csv|json]
  --alert           Send overdue action alerts to Telegram

# ICP Scoring Criteria (0-10)
scoring_weights = {
    "company_size": 0.20,      # 5-200 karyawan = ideal
    "budget_range": 0.25,      # IDR 5M+ = qualified
    "authority": 0.20,         # Owner/Director = high
    "need_fit": 0.20,          # AI/digital need = high
    "timeline": 0.15           # <90 days = urgent
}

# Score thresholds
# 8-10: HOT — Prioritize immediately
# 5-7:  WARM — Nurture with value content
# 3-4:  COLD — Low effort only
# 0-2:  DQ — Do not pursue
```

### 8B. `scripts/proposal_gen.py`

**Purpose:** Generate customized proposals from templates

```python
# Usage
python3 scripts/proposal_gen.py [OPTIONS]

Options:
  --tier            Pricing tier: starter|growth|scale
  --company         Company name
  --contact         Contact name
  --pain-points     Comma-separated pain points
  --output          Output format: pdf|docx|md [default: md]
  --send-wa         Auto-send via WA after generation

# Example
python3 scripts/proposal_gen.py \
  --tier growth \
  --company "PT Maju Bersama" \
  --contact "Budi Santoso" \
  --pain-points "manual-ops,no-content,low-leads" \
  --output pdf
```

### 8C. `scripts/outreach_sequencer.py`

**Purpose:** Manage and automate outreach sequences

```python
# Usage
python3 scripts/outreach_sequencer.py [OPTIONS]

Options:
  --add-lead        Add new lead to sequence [--sequence 3|5]
  --run-today       Execute all due touches today
  --status          Show sequence status for all leads
  --pause           Pause sequence for a lead
  --completed       Mark sequence as completed

# Sequence management
python3 scripts/outreach_sequencer.py --add-lead \
  --name "Budi Santoso" \
  --wa "+62812xxxxxxx" \
  --sequence 5 \
  --first-touch-date "2026-03-14"

# Run today's touches (schedule via cron)
# 0 9 * * 1-6 python3 /path/to/outreach_sequencer.py --run-today
```

---

## 9. Telegram Integration (Deal Alerts)

### Alert Types

```python
# In scripts/lead_scorer.py — Telegram notifications

ALERT_TEMPLATES = {
    "new_hot_lead": """
🔥 HOT LEAD MASUK!
Company: {company}
Contact: {contact} ({title})
Score: {score}/10
Source: {source}
Deal Value: IDR {value:,}
Action: {next_action}
→ /deal_{deal_id}
""",

    "deal_advanced": """
✅ DEAL MAJU STAGE!
{company}
{prev_stage} → {new_stage}
Value: IDR {value:,}
Probability: {probability}%
Close target: {close_date}
""",

    "overdue_action": """
⚠️ OVERDUE ACTION!
Deal: {company} ({stage})
Action yang belum: {action}
Seharusnya: {due_date} ({days_late} hari terlambat)
Deal value at risk: IDR {value:,}
""",

    "deal_closed": """
🎉 DEAL CLOSED!
Company: {company}
Value: IDR {value:,}
Package: {package}
Source: {source}
Time to close: {days} hari
Monthly closed total: IDR {monthly_total:,}
"""
}
```

### Setup Telegram Alerts

```bash
# In .env or config
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_SALES_CHAT_ID=your_chat_id

# Test alert
python3 scripts/lead_scorer.py --alert --test
```

---

## 10. Calendar Integration (Follow-up Reminders)

```python
# Google Calendar reminder creation
# Called automatically by outreach_sequencer.py

def create_followup_reminder(deal, action, due_date):
    """Create Google Calendar event for follow-up"""
    event = {
        "summary": f"[SALES] Follow up: {deal['company']} — {action}",
        "description": f"""
Deal ID: {deal['deal_id']}
Stage: {deal['stage']}
Value: IDR {deal['deal_value']:,}
Contact: {deal['contact_name']} ({deal['contact_wa']})
Action: {action}
Notes: {deal['notes']}
        """,
        "start": {"dateTime": f"{due_date}T09:00:00+07:00"},
        "end": {"dateTime": f"{due_date}T09:30:00+07:00"},
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "popup", "minutes": 30},
                {"method": "email", "minutes": 60}
            ]
        }
    }
    return event
```

---

## 11. KPIs & Weekly Reporting

### KPI Targets

| KPI | Weekly Target | Monthly Target |
|-----|--------------|----------------|
| New leads added | 20 | 80 |
| Qualified leads | 8 | 32 |
| Demo/calls booked | 4 | 16 |
| Proposals sent | 2 | 8 |
| Deals closed | 1 | 4 |
| Pipeline value | IDR 50M | IDR 200M |
| ACV (Avg Contract Value) | — | IDR 20M |
| Conversion rate (lead→close) | — | 5% |
| Monthly closed revenue | — | IDR 80M |

### Weekly Report Template

```bash
# Generate weekly report
python3 scripts/lead_scorer.py --report --period weekly --format telegram

# Output format:
📊 SALES REPORT — WEEK [W] [YEAR]

Pipeline:
  Prospect:  [N] leads  (IDR [X])
  Qualify:   [N] leads  (IDR [X])
  Demo:      [N] leads  (IDR [X])
  Proposal:  [N] leads  (IDR [X])
  Negotiate: [N] leads  (IDR [X])

Total Pipeline: IDR [X]
Expected Close (30d): IDR [X]

This Week:
  New leads: [N] / 20 target
  Demos done: [N] / 4 target
  Deals closed: [N] / 1 target
  Revenue closed: IDR [X]

Action Items:
  [N] overdue follow-ups ⚠️
  [N] proposals expiring soon ⏰
  [N] hot leads not contacted 🔥
```

---

## 12. Standard Operating Procedures (SOPs)

### SOP: New Lead Entry
1. Identify lead (source: LinkedIn/GMaps/referral)
2. Run `lead_scorer.py --score` → get ICP score
3. If score ≥ 5: add to pipeline + outreach sequence
4. If score < 5: add to cold nurture list
5. Calendar reminder created automatically
6. Telegram alert sent to sales channel

### SOP: After Demo/Discovery Call
1. Fill call notes in CRM within 1 hour
2. Update stage to "Proposal" if interest confirmed
3. Run `proposal_gen.py` with their pain points
4. Send proposal within 24 hours
5. Schedule follow-up call in 3 days

### SOP: Proposal Follow-up
1. Day 3: "Sudah sempat baca proposal kami?"
2. Day 7: "Ada pertanyaan? Saya siap diskusi"
3. Day 14: "Proposal ini expire [tanggal] — mau perpanjang?"

### SOP: Deal Closing
1. Verbal agreement → send MOU via email
2. DP invoice (50%) sent same day
3. Calendar kickoff meeting scheduled
4. Telegram alert: Deal closed! 🎉
5. Hand off to operations team

---

## 13. Quick Reference Card

```
PIPELINE SHORTCUTS:
  Score new lead:     python3 scripts/lead_scorer.py --score
  View pipeline:      python3 scripts/lead_scorer.py --list
  Today's actions:    python3 scripts/outreach_sequencer.py --run-today
  Generate proposal:  python3 scripts/proposal_gen.py --tier growth --company "X"
  Weekly report:      python3 scripts/lead_scorer.py --report --period weekly

PRICING TIERS:
  Starter:  IDR  5,000,000  (1-month engagement)
  Growth:   IDR 15,000,000  (3-month engagement)
  Scale:    IDR 50,000,000  (6-month engagement)

PIPELINE TARGETS:
  20 new leads/week → 8 qualified → 4 demos → 2 proposals → 1 close
  Monthly: IDR 80M revenue target
```

---

*Skill version 1.0 — BerkahKarya Sales Engine 🔥*
*Last updated: 2026-03-13*
