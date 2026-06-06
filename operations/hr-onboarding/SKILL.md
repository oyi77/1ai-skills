---
name: hr-onboarding
version: 1.0.0
description: >
  End-to-end HR and onboarding system for BerkahKarya. Covers hiring workflow
  (JD → sourcing → screening → interview → offer → onboard), role-specific frameworks
  for content creators, developers, sales, and trading analysts. Includes PKWT templates,
  Indonesia rate benchmarks, 30/60/90 day reviews, offboarding, and Telegram-based
  team communication structure.
author: Vilona / BerkahKarya
language: id-ID / en
tags: [hr, hiring, onboarding, pkwt, indonesia, team, operations, offboarding]
scripts:
  - scripts/onboarding_checklist.py
  - scripts/payroll_calc.py
---

# HR & Onboarding Skill 🚀

Build and operate the BerkahKarya team — from job description to first 90 days.

---

## 1. Hiring Workflow Overview

```
JD CREATION → SOURCING → SCREENING → INTERVIEW → OFFER → ONBOARD
     📝           🔍         📋          🎯          📩       🚀

Duration targets:
  JD Creation:   1 day
  Sourcing:      3–7 days (collect 10+ candidates)
  Screening:     2–3 days (shortlist 3–5)
  Interview:     3–5 days (2 rounds)
  Offer:         1–2 days
  Onboard:       30 days (ramp period)
  
Total time-to-hire target: 2–3 weeks
```

---

## 2. Role Types & Job Description Templates

Ready-to-use templates for common scenarios.


### 2A. Content Creator

**Job Description Template:**
```markdown
# [LOKER] Content Creator — BerkahKarya

Kami (BerkahKarya) cari Content Creator yang bisa bikin konten 
viral di TikTok, Instagram, dan YouTube Shorts untuk brand 
digital product kami.

**Yang Lo Bakal Kerjain:**
- Produksi 3–5 video/hari (TikTok + Reels + YT Shorts)
- Script + shooting + editing (simple, template-based)
- Follow viral trend dan adapt ke niche bisnis digital
- Maintain JENDRALBOT channel dan brand lainnya

**Lo Cocok Kalau:**
- Punya HP yang decent (kamera bagus)
- Ngerti basic video editing (CapCut/VN/Premiere)
- Up-to-date sama trend TikTok/IG
- Target-oriented, bisa kerja autonomous
- Bonus: Pernah punya channel sendiri

**Tipe Kerjasama:** Freelance (project-based) atau Part-time
**Rate:** IDR 1.5M–5M/bulan (tergantung output volume)
**Remote:** 100% WFH
**Start:** ASAP
```

**Skill Test:**
```
Task: Buat 1 video TikTok tentang [topik produk digital kami]
Duration: 30–60 detik
Deadline: 48 jam
Criteria:
  - Hook pertama 3 detik (apakah menarik?)
  - Script flow (problem → solution → CTA)
  - Editing quality (cut, caption, music)
  - Thumbnail/cover image
```

### 2B. Developer (Fullstack / AI Engineer)

**Job Description Template:**
```markdown
# [LOKER] Developer (Fullstack / AI Engineer) — BerkahKarya

BerkahKarya butuh developer yang bisa build dan maintain 
sistem otomasi AI untuk operasional bisnis kami.

**Tech Stack:**
- Python (wajib) — scripting, automation, AI integration
- Node.js / FastAPI — backend services
- OpenAI / Anthropic API — AI features
- Telegram Bot API — internal tools
- Google Cloud / basic DevOps

**Yang Lo Bakal Kerjain:**
- Build automation scripts (social media, sales, ops)
- Maintain dan improve existing tools
- Integrate AI APIs ke workflow bisnis
- Build internal dashboards (simple)

**Lo Cocok Kalau:**
- Solid di Python (scripting, async, APIs)
- Pernah build Telegram bot
- Suka problem-solving dan autonomous work
- Bisa deliver MVP dalam hitungan hari, bukan bulan

**Tipe Kerjasama:** Freelance / Part-time / Full-time
**Rate:** IDR 3M–15M/bulan (sesuai scope)
**Remote:** 100% WFH
```

**Skill Test:**
```
Task: Build a Python script that:
1. Accepts a list of Instagram usernames (CSV)
2. Fetches public profile data (followers, bio)
3. Scores each account (simple scoring: followers range, has link in bio)
4. Outputs ranked CSV

Time limit: 3 hours
Evaluation:
  - Code quality (clean, readable, commented)
  - Error handling
  - Completeness
  - Bonus: Add Telegram notification when done
```

### 2C. Sales (B2B Account Executive)

**Job Description Template:**
```markdown
# [LOKER] Sales / Business Development — BerkahKarya

Kami cari closer yang bisa prospect, qualify, dan close 
klien B2B untuk layanan AI automation dan digital content.

**Yang Lo Bakal Kerjain:**
- Cold outreach via LinkedIn, WA, email
- Discovery call + demo dengan calon klien
- Proposal presentation dan negosiasi
- CRM update dan pipeline management
- Target: 4 deals/bulan (IDR 80M pipeline)

**Lo Cocok Kalau:**
- Punya pengalaman B2B sales (minimal 1 tahun)
- Comfortable cold outreach dan rejection
- Bisa explain tech solutions ke non-tech audience
- Driven oleh komisi, bukan gaji tetap

**Kompensasi:**
- Base: IDR 2M–3M/bulan
- Komisi: 8–12% dari deal value yang closed
- OTE (On-target earnings): IDR 10M–20M/bulan
- Remote-first, flexible hours
```

**Skill Test:**
```
Scenario: Kamu dapat lead: Owner UMKM makanan frozen, 50 karyawan, 
omset IDR 5M/bulan, keluhan: manual order tracking = chaos.

Task:
1. Tulis cold WA message untuk approach mereka (max 5 kalimat)
2. List 3 pertanyaan discovery yang akan kamu tanyakan
3. Rekomendasikan package kami yang paling sesuai + alasannya

Evaluation:
  - Relevance of hook (pain-based vs generic?)
  - Discovery questions (BANT approach?)
  - Package recommendation logic
```

### 2D. Trading Analyst

**Job Description Template:**
```markdown
# [LOKER] Trading Analyst — BerkahKarya Quant Division

Kami build divisi trading XAUUSD (Gold) berbasis data dan AI.
Butuh analyst yang bisa develop, backtest, dan monitor strategi.

**Yang Lo Bakal Kerjain:**
- Develop dan backtest trading strategies (XAUUSD, Asia session)
- Build trading automation scripts (Python + broker API)
- Monitor live trades dan risk management
- Weekly performance reporting

**Tech/Knowledge Stack:**
- Python (pandas, numpy, backtrader/zipline)
- Technical analysis (price action, support/resistance)
- Risk management principles
- Bonus: Algorithmic trading experience

**Kompensasi:**
- Base: IDR 3M–5M/bulan
- Profit sharing: 10–20% dari net profit divisi trading
- Remote, flexible hours (Asia session monitoring)
```

**Skill Test:**
```
Task: Backtest this XAUUSD strategy on 2024 data:
- Entry: First 15-min candle breakout after Asia open (07:00 UTC+7)
- SL: 10 pips below entry
- TP: 20 pips
- Condition: Only trade if 7-candle range > 5 pips

Deliver:
1. Python backtest code
2. Results: Win rate, avg R:R, max drawdown, Sharpe ratio
3. Your assessment: Is this strategy worth live testing?

Data: Can use Yahoo Finance or any public XAUUSD data
```

---

## 3. Sourcing Channels

| Channel | Best For | Cost |
|---------|----------|------|
| Telegram groups (loker Indonesia) | General | Free |
| Glints.com | Developer, Sales | Free (basic) |
| LinkedIn (post + DM) | Developer, Sales, Analyst | Free |
| Jobstreet | All roles | IDR 500K–2M/post |
| Karyawan.com | Operations | Free |
| Instagram/TikTok (konten creator loker) | Content Creator | Free |
| Referral network | All roles | Reward IDR 500K |

---

## 4. Screening Framework

Structured framework for approaching this domain.


### Resume/Portfolio Screening Checklist

```python
# Minimum pass criteria per role

SCREENING_CRITERIA = {
    "content_creator": {
        "required": ["portfolio/channel link", "output volume", "editing tools"],
        "nice_to_have": ["own channel >1K followers", "viral content example"],
        "auto_reject": ["no portfolio at all", "asking only about salary"]
    },
    "developer": {
        "required": ["GitHub link OR code sample", "Python listed", "API experience"],
        "nice_to_have": ["bot projects", "AI/ML experience", "deployed projects"],
        "auto_reject": ["no code samples", "only frontend skills", "no async experience"]
    },
    "sales": {
        "required": ["B2B experience", "mention of targets achieved", "communication clarity"],
        "nice_to_have": ["tech sales background", "CRM experience"],
        "auto_reject": ["only B2C retail", "vague about results", "spelling errors in cover"]
    },
    "trading_analyst": {
        "required": ["trading knowledge demonstrated", "Python", "backtest experience"],
        "nice_to_have": ["live trading results", "algo trading", "risk management mention"],
        "auto_reject": ["no quantitative background", "claims huge returns without proof"]
    }
}
```

---

## 5. Interview Frameworks

Structured framework for approaching this domain.


### Round 1: Culture Fit (30 minutes, Telegram voice/Zoom)

**Universal questions:**
```
1. "Ceritain tentang diri lo dan kenapa lo mau kerja di BerkahKarya."
   → Looking for: Alignment with mission, genuine interest

2. "Kapan terakhir lo stuck di suatu problem dan gimana lo solve?"
   → Looking for: Problem-solving, resourcefulness, not giving up

3. "Lo lebih prefer kerja dengan instruksi detail atau dikasih kebebasan?"
   → Looking for: Autonomous worker preference (we need this)

4. "Kalau lo punya 3 prioritas kerja hari ini tapi waktu cuma cukup untuk 2, 
   lo milih gimana?"
   → Looking for: Prioritization skills, communication

5. "Apa target lo 1 tahun dari sekarang?"
   → Looking for: Ambition fit, growth mindset

PASS criteria:
  - Clear communicator ✅
  - Autonomous mindset ✅
  - Growth-oriented ✅
  - No entitlement attitude ✅
  - Genuine interest in BerkahKarya mission ✅
```

### Round 2: Skill Test (async or live)

```
See role-specific skill tests in Section 2 above.

Evaluation rubric:
  - Completeness (did they deliver everything asked?): 30%
  - Quality (how good is the output?): 40%
  - Speed (did they hit deadline?): 15%
  - Communication during test (did they ask smart questions?): 15%

Score: 0-10
  8-10: Strong hire
  6-7:  Conditional hire (address gaps)
  4-5:  Not now (keep in pipeline)
  0-3:  Reject
```

---

## 6. Offer & Contract

Key aspects of hr-onboarding relevant to this section.


### Freelancer vs Employee Decision Matrix

| Factor | Freelancer (PKWT/Project) | Employee (PKWT Fixed) |
|--------|--------------------------|----------------------|
| Work scope | Project-based, deliverable-focused | Ongoing, role-based |
| Hours | Flexible | Fixed (8h/day) |
| Benefits | None (factored into rate) | BPJS + benefits |
| Termination | End of project | Notice period required |
| Tax | Handled by them | PPh 21 deducted by company |
| Best for | Content Creator, Dev (project) | Sales, Ops (full-time) |

### Rate Benchmarks Indonesia 2025

| Role | Freelance/Month | Full-time/Month |
|------|----------------|-----------------|
| Content Creator (volume) | IDR 1.5M–5M | IDR 3M–6M |
| Developer (mid-level) | IDR 5M–15M | IDR 7M–15M |
| Developer (senior) | IDR 15M–30M | IDR 15M–25M |
| Sales (Base only) | IDR 2M–3M | IDR 3M–5M + commission |
| Trading Analyst | IDR 3M–8M | IDR 5M–10M + profit share |
| Operations/Admin | IDR 2M–3.5M | IDR 3M–4M |

### PKWT Template (Perjanjian Kerja Waktu Tertentu)

```markdown
# PERJANJIAN KERJA WAKTU TERTENTU (PKWT)

Dibuat di Jakarta, pada tanggal: [TANGGAL]

PARA PIHAK:

Pihak Pertama (Perusahaan):
  Nama: BerkahKarya Digital
  Diwakili oleh: [Nama Direktur]
  Alamat: [Alamat]

Pihak Kedua (Pekerja):
  Nama: [Nama Pekerja]
  KTP: [NIK]
  Alamat: [Alamat]

---

PASAL 1: JANGKA WAKTU
Perjanjian ini berlaku selama [X] bulan, 
terhitung mulai [tanggal mulai] sampai [tanggal selesai].

PASAL 2: POSISI DAN PEKERJAAN
Pihak Kedua bekerja sebagai [Jabatan] dengan tugas utama:
1. [Tugas 1]
2. [Tugas 2]
3. [Tugas 3]

PASAL 3: KOMPENSASI
- Gaji pokok: IDR [X]/bulan
- Tunjangan [jika ada]: IDR [X]/bulan
- Komisi/bonus: [sesuai ketentuan terpisah]
- Dibayarkan setiap tanggal [X]

PASAL 4: WAKTU KERJA
[Senin–Jumat, 09:00–17:00 WIB / Remote / Flexible]

PASAL 5: KERAHASIAAN
Pihak Kedua wajib menjaga kerahasiaan informasi perusahaan, 
termasuk data klien, strategi bisnis, dan kode program.

PASAL 6: KEPEMILIKAN INTELEKTUAL
Semua karya yang dibuat dalam lingkup pekerjaan ini 
adalah milik Pihak Pertama.

PASAL 7: PENGAKHIRAN
Perjanjian dapat diakhiri lebih awal dengan pemberitahuan 
[14/30] hari atau atas kesepakatan kedua pihak.

---

Pihak Pertama                    Pihak Kedua
[Tanda Tangan]                   [Tanda Tangan]
[Nama]                           [Nama]
[Tanggal]                        [Tanggal]
```

---

## 7. Onboarding Checklist

Systematic checklist for validation.


### Pre-Start (Before Day 1)

```
□ Send welcome message via Telegram
□ Share company overview doc (Google Drive link)
□ Create Google Workspace account (nama@berkahkarya.com)
□ Add to relevant Telegram groups (see Section 8)
□ Prepare task brief for first week
□ Assign onboarding buddy (existing team member)
□ Send PKWT for review + signing
□ Collect KTP copy, NPWP, bank account info
```

### Day 1: Account Setup

```
□ Google Workspace: Gmail, Drive, Calendar, Meet
□ Telegram: Add to all relevant groups
□ Password manager: Add to company 1Password/Bitwarden
□ Notion/ClickUp: Add to workspace (if used)
□ GitHub: Add as collaborator (if developer)
□ PostBridge: Add account (if content-related)
□ LYNK dashboard: Create affiliate account (if sales/content)
□ Briefing call: 30–60 minute intro with team lead
□ Share SOUL.md, USER.md, AGENTS.md (our operating principles)
```

### Week 1: Foundation

```
□ Read all onboarding docs in Drive
□ Review SOUL.md (company culture/values)
□ Complete role-specific training material
□ Shadow existing team member for 2 hours
□ Complete first small task independently
□ Daily check-in (15 min) with lead
□ Set up workspace/tools to personal preference
□ Submit first deliverable (even if small)
```

### Week 2–4: Ramp Up

```
□ Increasing autonomy on tasks
□ Full ownership of 1 recurring responsibility
□ Weekly 1:1 with team lead (30 min)
□ Document any questions/blockers in team Telegram
□ Review progress against 30-day targets
□ Feedback session at end of Week 4
```

### 30-Day Milestone Checklist (by Role)

| Role | 30-Day Goal |
|------|------------|
| Content Creator | 50+ videos produced, at least 1 viral (>10K views) |
| Developer | 2+ scripts shipped, 0 critical bugs in production |
| Sales | 20 leads qualified, 5 demos booked, 1 deal in proposal |
| Trading Analyst | 1 backtest completed, strategy documented |

---

## 8. Team Communication Structure (Telegram)

Key aspects of hr-onboarding relevant to this section.


### Group Architecture

```
BERKAHKARYA TELEGRAM GROUPS:

📌 [BK HQ] — Main Operations
  Members: All team + Vilona (AI)
  Content: Announcements, decisions, blockers
  Rules: Keep it professional, no spam

📌 [BK Dev] — Development Team
  Members: Developers + CTO
  Content: Code updates, bugs, deploy logs
  Rules: Technical only, link to relevant code

📌 [BK Sales] — Sales Team
  Members: Sales team + sales lead
  Content: Lead updates, deal alerts, proposals
  Rules: Update CRM first, then Telegram

📌 [BK Content] — Content Team
  Members: Content creators + content lead
  Content: Post schedules, feedback, viral ideas
  Rules: Daily report of posts published

📌 [BK Trading] — Trading Division
  Members: Analysts + lead trader
  Content: Trade logs, analysis, weekly results
  Rules: Log every trade, no FOMO sharing

📌 [BK Alerts] — Automated Alerts (Bot only)
  Members: All team + automation bots
  Content: System alerts, revenue gaps, deal closed
  Rules: Read-only for humans

📌 [BK HR] — Private HR Channel
  Members: Founders + HR lead only
  Content: Salary, contracts, sensitive HR matters
  Rules: Strictly confidential
```

### Communication Norms

```
Daily standup format (post in relevant group, 9:00 AM):
  Yesterday: [what was done]
  Today: [what will be done]
  Blocker: [if any, tag relevant person]

Response time SLA:
  HQ channel: 4 hours
  Direct DM: 2 hours
  Urgent (🚨 tagged): 30 minutes

After hours (21:00–08:00): Only for genuine emergencies
```

---

## 9. Performance Reviews

Key aspects of hr-onboarding relevant to this section.


### 30-Day Check-in

```markdown
# 30-DAY REVIEW — [Nama] — [Role]

## Performance vs Goals
| Goal | Target | Actual | Status |
|------|--------|--------|--------|
| [Goal 1] | [X] | [Y] | ✅/⚠️/❌ |
| [Goal 2] | [X] | [Y] | ✅/⚠️/❌ |

## Culture Fit Assessment (1-5)
- Autonomy: [score] — [comment]
- Communication: [score] — [comment]
- Speed of delivery: [score] — [comment]
- Problem-solving: [score] — [comment]

## Feedback from Team

Key aspects of hr-onboarding relevant to this section.


## Decision
[ ] Continue as planned
[ ] Continue with adjustments: [describe]
[ ] Performance Improvement Plan (PIP)
[ ] Contract not extended

## Next 30-Day Goals
1. [Goal]
2. [Goal]
3. [Goal]
```

### 60-Day Check-in

```markdown
# 60-DAY REVIEW — [Nama] — [Role]

## Performance Trend (30d vs 60d)
[Comparison table]

## Ownership Level Assessment
- Can they work fully autonomously? Y/N
- Are they proactive or reactive? 
- Have they contributed beyond their role?

## Compensation Review
- Current: IDR [X]
- Market rate check: IDR [X]
- Recommendation: Keep / Adjust to IDR [X]

## Decision
[ ] Continue — strong performer
[ ] Extend contract (if fixed-term)
[ ] Convert freelancer to part-time/full-time
[ ] PIP — specific improvements needed
[ ] Part ways — not the right fit
```

### 90-Day Final Ramp Review

```markdown
# 90-DAY REVIEW — [Nama] — [Role]

## Full Performance Scorecard
[Complete metrics for 90 days]

## Cultural Alignment Score: [X]/10

Key aspects of hr-onboarding relevant to this section.


## Long-term Fit Assessment
- Do they live the BerkahKarya values?
- Are they growing or plateauing?
- What's their ceiling in this role?

## Decision
[ ] Permanent/extended contract — strong hire ✅
[ ] Role adjustment — different fit
[ ] Part ways — mismatch confirmed ❌
[ ] Promote/expand scope — exceeding expectations 🔥

## Annual Compensation Plan
Base: IDR [X]
Bonus structure: [describe]
Next review: [date]
```

---

## 10. Off-boarding Process

Step-by-step workflow for this skill.


### Voluntary Resignation

```
Week 1 (Notice period):
  □ Knowledge transfer sessions (daily 1h)
  □ Document all processes they own
  □ Hand off ongoing projects with status notes
  □ Update passwords/access they held

Last Day:
  □ Final knowledge transfer sign-off
  □ Revoke Google Workspace access
  □ Remove from all Telegram groups
  □ Revoke GitHub access / transfer repos
  □ Revoke PostBridge / LYNK access
  □ Revoke any API keys they held
  □ Final salary payment confirmation
  □ Reference letter (if deserved)
  □ Exit interview (optional but valuable)
```

### Knowledge Transfer Template

```markdown
# KNOWLEDGE TRANSFER DOC — [Nama] — [Role]

Date: [Date]
Prepared by: [Nama]
Reviewed by: [Team Lead]

## My Responsibilities (Complete List)
1. [Responsibility] — Daily/Weekly/Monthly
   - How it's done: [Process steps]
   - Tools used: [Tool + access location]
   - Common issues: [Known problems + solutions]
   - Time required: [Hours/week]

## Active Projects I'm Handling
1. [Project name]
   - Status: [%] complete
   - Next steps: [Immediate actions needed]
   - Files: [Drive link]
   - Key contacts: [Name + contact]

## Access I Currently Hold
| Tool/System | Access Level | Credentials Location |
|-------------|-------------|---------------------|
| Google Workspace | [role] | Company 1Password |
| GitHub | [role] | Company 1Password |
| [Other] | [role] | [location] |

## Things I Wish I'd Documented Earlier
[Free-form honest notes]

## Recommendations for My Replacement
[Honest advice]
```

### Account Revocation Checklist

```python
# scripts/onboarding_checklist.py handles this in --offboard mode

ACCOUNTS_TO_REVOKE = [
    "google_workspace",     # Suspend account
    "telegram_groups",      # Remove from all BK groups
    "github_org",           # Remove from organization
    "postbridge",           # Delete user
    "lynk_affiliate",       # Deactivate affiliate account
    "notion_workspace",     # Revoke access
    "password_manager",     # Remove from shared vaults
    "cloud_accounts",       # AWS/GCP/etc if applicable
    "api_keys",             # Rotate any shared keys
    "social_accounts"       # Remove admin access
]
```

---

## 11. Scripts Reference

Quick reference for commonly needed information.


### 11A. `scripts/onboarding_checklist.py`

```python
# Usage
python3 scripts/onboarding_checklist.py [OPTIONS]

Options:
  --new-hire        Generate onboarding checklist for new hire
  --offboard        Generate offboarding + account revocation list
  --role TEXT       Role: content_creator|developer|sales|trading_analyst
  --name TEXT       Employee name
  --start-date TEXT Start date (YYYY-MM-DD)
  --send-telegram   Send checklist to HR Telegram group

# Example — new hire
python3 scripts/onboarding_checklist.py \
  --new-hire \
  --role developer \
  --name "Andi Wijaya" \
  --start-date "2026-03-20" \
  --send-telegram

# Example — offboarding
python3 scripts/onboarding_checklist.py \
  --offboard \
  --name "Budi Santoso" \
  --last-date "2026-03-31"

# Output includes:
# - Formatted checklist (Markdown)
# - Telegram notification to HR group
# - Calendar events for key review dates
```

### 11B. `scripts/payroll_calc.py`

```python
# Usage
python3 scripts/payroll_calc.py [OPTIONS]

Options:
  --employee TEXT   Employee name or ID
  --month TEXT      Payroll month (YYYY-MM)
  --list            List all employees + current salaries
  --add-employee    Add new employee to payroll
  --calculate       Calculate net pay for the month
  --pph21           Calculate PPh 21 deduction
  --bpjs            Calculate BPJS Ketenagakerjaan + Kesehatan
  --export          Export payroll summary (CSV)
  --bulk            Run for all employees in batch

# PPh 21 rates (2025, PTKP TK/0 = IDR 54M/year)
PPH21_RATES = {
    (0, 60_000_000): 0.05,
    (60_000_001, 250_000_000): 0.15,
    (250_000_001, 500_000_000): 0.25,
    (500_000_001, float('inf')): 0.30
}

# BPJS contributions
BPJS = {
    "ketenagakerjaan_jht_employee": 0.02,   # 2% dari gaji
    "ketenagakerjaan_jht_employer": 0.037,  # 3.7%
    "ketenagakerjaan_jp_employee": 0.01,    # 1%
    "ketenagakerjaan_jp_employer": 0.02,    # 2%
    "kesehatan_employee": 0.01,             # 1% (max IDR 12M gaji)
    "kesehatan_employer": 0.04              # 4%
}

# Example output
python3 scripts/payroll_calc.py --employee "Andi Wijaya" --month "2026-03"

# Payroll Summary: Andi Wijaya — March 2026
# Gross salary:      IDR 8,000,000
# BPJS Employee:     IDR   320,000
# PPh 21:            IDR   100,000
# Net salary:        IDR 7,580,000
# Bank transfer to:  BCA 1234567890
```

---

## 12. Google Workspace Setup (Per New Hire)

Key aspects of hr-onboarding relevant to this section.


### Account Creation Process

```bash
# Via Google Admin Console (admin.google.com)

1. Add User:
   - First name, Last name
   - Email: [firstname]@berkahkarya.com (or alias)
   - Temp password → force change on first login

2. Assign to Org Unit:
   - /Content-Team | /Dev-Team | /Sales-Team | /Operations

3. Licenses:
   - Google Workspace Business Starter (IDR 85K/user/month)

4. Shared drives to grant access:
   - "BK Company Docs" — Viewer
   - "[Department] Shared" — Editor
   - "HR Private" — Access ONLY for HR team

5. Send welcome email with:
   - Login instructions
   - Link to onboarding checklist
   - First week schedule
```

---

## 13. Quick Reference

```
HIRING SHORTCUTS:
  New hire checklist:   python3 scripts/onboarding_checklist.py --new-hire --role [X] --name "[Name]"
  Offboard:             python3 scripts/onboarding_checklist.py --offboard --name "[Name]"
  Calculate payroll:    python3 scripts/payroll_calc.py --calculate --month 2026-03
  Payroll all:          python3 scripts/payroll_calc.py --bulk --month 2026-03

RATE BENCHMARKS (2025):
  Content Creator: IDR 1.5M–6M/month
  Developer:       IDR 5M–30M/month (level-dependent)
  Sales:           IDR 2M base + 8-12% commission
  Trading Analyst: IDR 3M–10M + profit share

CONTRACT TYPES:
  Freelance:  Project-based, no benefits, higher gross rate
  PKWT:       Fixed term, includes BPJS, standard benefits
  Full-time:  Ongoing, all benefits, probation 3 months

REVIEW SCHEDULE:
  30-day:  Performance vs ramp targets
  60-day:  Autonomy + compensation review
  90-day:  Full scorecard + permanent decision

TELEGRAM GROUPS:
  BK HQ:      All hands announcements
  BK Dev:     Tech team only
  BK Sales:   Sales pipeline
  BK Content: Content team
  BK Trading: Quant division
  BK Alerts:  Bot notifications (read-only)
  BK HR:      Founders only (private)
```

---

*Skill version 1.0 — BerkahKarya HR Engine 🚀*
*Last updated: 2026-03-13*

## When to Use

- Automating employee onboarding workflows
- Managing employee documentation
- Tracking onboarding progress
- Generating onboarding checklists
- Managing employee data and records

## When NOT to Use

- Task requires HR expertise (consult HR professional)
- Task is about recruitment, not onboarding
- You need legal compliance review (use legal tools)
- Task is about payroll processing (use payroll tools)
- You don't have employee data to work with
- Task requires employee relations expertise

## Red Flags

- Handling sensitive employee data improperly
- Not following data privacy regulations
- Missing onboarding steps
- Not tracking onboarding completion
- Ignoring compliance requirements

## Verification

- [ ] Onboarding workflows are complete
- [ ] Employee data is handled securely
- [ ] Compliance requirements are met
- [ ] Onboarding progress is tracked
- [ ] Documentation is properly managed