---
name: contract-manager
version: 1.0.0
description: Contract lifecycle management for BerkahKarya — draft, review, negotiate, sign, track, archive. Covers talent agreements, client deals, vendor contracts, employment. Indonesian law compliant (PKS format). Telegram alerts for renewals and breaches.
author: Vilona / BerkahKarya
tags: [contracts, legal, operations, talent, indonesian-law, lifecycle]
requires: [python3, telegram-bot (optional), docusign/pdf-sign (optional)]
---

# Contract Manager Skill

> End-to-end contract lifecycle for a 1-man company scaling to a team.
> Every deal documented. Every deadline tracked. No surprises.

---

## Overview

This skill covers:
1. **Lifecycle stages** — draft → review → negotiate → sign → active → archive
2. **Contract types** — talent, client, vendor, employment
3. **Template library** — ready-to-use Indonesian-law-compliant templates
4. **Key clauses** — copy-paste clauses for any contract
5. **Tracking** — status, renewal dates, payment milestones, breach alerts
6. **Automation** — Python scripts + Telegram alerts

---

## Directory Structure

```
contracts/
├── active/
│   ├── talent/       # Talent agreements
│   ├── client/       # Client service agreements
│   ├── vendor/       # Vendor/supplier contracts
│   └── employment/   # Full-time/part-time hires
├── archive/
│   ├── 2025/
│   └── 2026/
├── templates/
│   ├── service-agreement.md
│   ├── talent-commission.md
│   ├── nda.md
│   ├── sla.md
│   └── employment-pkwt.md
├── drafts/           # Work-in-progress, unsigned
└── scripts/
    ├── contract_tracker.py
    └── renewal_alert.py
```

### Naming Convention

```
{TYPE}-{PARTY_SHORT}-{YYYYMMDD}-{VERSION}.pdf

Examples:
  TALENT-JENDRALBOT-20260313-v1.pdf
  CLIENT-BERKAHKARYA-ACME-20260101-v2.pdf
  VENDOR-HOSTINGER-20260315-v1.pdf
  EMPLOYMENT-PKWT-SONY-20260301-v1.pdf
  NDA-PARTNER-VERIS-20260101-v1.pdf
```

---

## Lifecycle Stages

```
DRAFT → REVIEW → NEGOTIATE → SIGN → ACTIVE → ARCHIVE
  ↓         ↓          ↓         ↓       ↓         ↓
Created   Internal   Counter-  Both    Running   Expired/
          check      offers   signed  contract  Terminated
```

### Stage Definitions

| Stage | Description | Owner | Duration |
|-------|-------------|-------|----------|
| DRAFT | Initial version created | Vilona/Agent | 1–2 days |
| REVIEW | Internal legal/compliance check | You | 1–3 days |
| NEGOTIATE | Back-and-forth with counterparty | Both | Variable |
| SIGN | Awaiting signatures | You + Party | 1–7 days |
| ACTIVE | Fully executed, obligations running | All parties | Contract term |
| ARCHIVE | Expired, terminated, or superseded | System | Permanent |

---

## Contract Types

Classify contracts by purpose: service agreements, NDAs, SLAs, vendor contracts.


### 1. Talent Agreement (Perjanjian Talent)

Used for: YouTubers, TikTokers, influencers, content creators under BerkahKarya management.

**Key fields:**
- Talent name + NIK (ID number)
- Exclusivity scope (platforms, categories)
- Revenue share % (typical: 70/30 talent/agency)
- Minimum deliverables (posts/month)
- Brand deal split %
- IP ownership of content
- Exit clause (notice period, cooling-off)

**Indonesian compliance:**
- Must reference UU No. 13/2003 (Ketenagakerjaan) if employment-like
- Use PKS format if contractor (not employee)
- Materai Rp 10.000 required for legal enforceability
- Signed witnesses (2 saksi) recommended

---

### 2. Client Service Agreement (Perjanjian Jasa)

Used for: Brands hiring BerkahKarya for influencer marketing, content production, campaigns.

**Key fields:**
- Scope of work (SOW) with deliverables
- Timeline and milestones
- Payment schedule (DP 50%, final 50%)
- Revision policy (max 2 rounds)
- Content approval process
- Termination for convenience clause
- Force majeure

---

### 3. Vendor Contract (Perjanjian Vendor)

Used for: Tools, services, freelancers, suppliers.

**Key fields:**
- Service description + SLA
- Pricing + payment terms (NET-30 standard)
- Data handling / NDA clause
- IP ownership of deliverables
- Liability cap (2x contract value)
- Governing law: Indonesian law

---

### 4. Employment Contract

**PKWT** (Perjanjian Kerja Waktu Tertentu = Fixed Term):
- Max 2 years, extendable once (2 years total = 4 years max)
- Must specify end date
- No severance if contract ends normally
- Regulated: PP No. 35/2021

**PKWTT** (Perjanjian Kerja Waktu Tidak Tertentu = Permanent):
- No end date
- Full severance rights (UPSEG formula)
- Probation max 3 months
- Termination requires BPJS compliance

> 🔴 **Rule:** Freelancers = PKS. Short-term project staff = PKWT. Core team = PKWTT.

---

## Template Library

Reusable contract templates with standard clauses for common scenarios.


### Template 1: Service Agreement (PKS Jasa)

```markdown
PERJANJIAN KERJA SAMA (PKS)
Nomor: PKS-{NUMBER}/{MONTH}/{YEAR}

Pada hari ini, {DAY} tanggal {DATE}, bertempat di Jakarta, telah disepakati
Perjanjian Kerja Sama (PKS) antara:

PIHAK PERTAMA:
Nama/Perusahaan  : {COMPANY_NAME}
NIK/NPWP         : {ID_NUMBER}
Alamat           : {ADDRESS}
Selanjutnya disebut "Pihak Pertama"

PIHAK KEDUA:
Nama/Perusahaan  : {PARTY_2_NAME}
NIK/NPWP         : {PARTY_2_ID}
Alamat           : {PARTY_2_ADDRESS}
Selanjutnya disebut "Pihak Kedua"

Pasal 1 – LINGKUP PEKERJAAN
Pihak Pertama menugaskan Pihak Kedua untuk:
{SCOPE_OF_WORK}

Pasal 2 – JANGKA WAKTU
Perjanjian ini berlaku selama {DURATION} terhitung mulai {START_DATE}
hingga {END_DATE}.

Pasal 3 – IMBALAN JASA
Pihak Pertama membayar kepada Pihak Kedua:
- Total nilai: Rp {AMOUNT}
- Pembayaran: {PAYMENT_SCHEDULE}
- Rekening: {BANK_ACCOUNT}

Pasal 4 – HAK DAN KEWAJIBAN
[Standard obligations clause]

Pasal 5 – KERAHASIAAN
Kedua pihak wajib menjaga kerahasiaan informasi selama {NDA_PERIOD}.

Pasal 6 – PENYELESAIAN SENGKETA
Sengketa diselesaikan secara musyawarah. Jika gagal, melalui BANI atau
Pengadilan Negeri {JURISDICTION}.

Pasal 7 – KETENTUAN LAIN
Force majeure, governing law: Hukum Republik Indonesia.

Demikian PKS ini dibuat dalam 2 (dua) rangkap bermaterai cukup.

PIHAK PERTAMA                    PIHAK KEDUA

___________________              ___________________
{NAME_1}                         {NAME_2}

Saksi 1: _______________   Saksi 2: _______________
```

---

### Template 2: Talent Commission Contract

```markdown
PERJANJIAN MANAJEMEN TALENT
Nomor: TALENT-{NUMBER}/{MONTH}/{YEAR}

PIHAK PERTAMA (Manajemen/Agensi):
BerkahKarya / {LEGAL_ENTITY}

PIHAK KEDUA (Talent):
Nama      : {TALENT_NAME}
NIK       : {TALENT_NIK}
Platform  : {PLATFORMS}  # e.g., TikTok: @handle, IG: @handle

Pasal 1 – EKSKLUSIVITAS
Talent setuju bahwa Manajemen memiliki hak EKSKLUSIF untuk:
- Platform: {PLATFORM_LIST}
- Kategori konten: {CONTENT_CATEGORIES}
- Periode eksklusivitas: {DURATION}

Pasal 2 – PEMBAGIAN PENDAPATAN
| Sumber Pendapatan        | Talent % | Manajemen % |
|--------------------------|----------|-------------|
| Brand Deal / Endorse     | 70%      | 30%         |
| AdSense / Platform Fund  | 85%      | 15%         |
| Merchandise              | 60%      | 40%         |
| Live Gifting             | 80%      | 20%         |

Pasal 3 – KEWAJIBAN TALENT
- Minimum {MIN_POSTS} konten/bulan
- Response time maks {RESPONSE_TIME} jam untuk brief brand
- Tidak bergabung agensi lain selama kontrak

Pasal 4 – KEWAJIBAN MANAJEMEN
- Pembayaran maksimal {PAYMENT_DAY} setiap bulan
- Laporan revenue transparan setiap bulan
- Tidak menanda-tangani deal tanpa persetujuan talent

Pasal 5 – KEPEMILIKAN KONTEN (IP)
Konten yang dibuat talent TETAP milik talent. Agensi hanya memiliki hak
penggunaan (license) selama kontrak aktif.

Pasal 6 – TERMINASI
- Notice period: {NOTICE_PERIOD} hari
- Early termination fee: {EARLY_TERM_FEE}
- Cooling-off: {COOLING_OFF} hari setelah terminasi

Pasal 7 – MATERAI DAN TANDA TANGAN
Ditandatangani dengan materai Rp 10.000 di atas.
```

---

### Template 3: NDA (Non-Disclosure Agreement)

```markdown
PERJANJIAN KERAHASIAAN (NDA)
Nomor: NDA-{NUMBER}/{YEAR}

Antara: {DISCLOSING_PARTY} ("Pihak Pengungkap")
Dan:    {RECEIVING_PARTY} ("Pihak Penerima")

Pasal 1 – DEFINISI
"Informasi Rahasia" mencakup: strategi bisnis, data keuangan, data pengguna,
source code, daftar klien, dan informasi yang ditandai RAHASIA.

Pasal 2 – KEWAJIBAN KERAHASIAAN
Pihak Penerima WAJIB:
a) Tidak mengungkapkan Informasi Rahasia kepada pihak ketiga
b) Menggunakan hanya untuk tujuan {PURPOSE}
c) Melindungi dengan standar keamanan yang wajar

Pasal 3 – PENGECUALIAN
NDA tidak berlaku untuk informasi yang:
- Sudah diketahui publik
- Diperoleh dari sumber independen yang sah
- Diwajibkan oleh hukum/pengadilan

Pasal 4 – JANGKA WAKTU KERAHASIAAN
{NDA_DURATION} tahun sejak penandatanganan, atau selama informasi tetap
bersifat rahasia (whichever is longer).

Pasal 5 – SANKSI
Pelanggaran NDA dikenai denda Rp {PENALTY} dan ganti rugi aktual.

Pasal 6 – GOVERNING LAW
Hukum Republik Indonesia. Sengketa di Pengadilan Negeri {JURISDICTION}.
```

---

### Template 4: SLA (Service Level Agreement)

```markdown
SERVICE LEVEL AGREEMENT (SLA)
Lampiran dari PKS Nomor: {PKS_NUMBER}

1. UPTIME GUARANTEE
   - Minimum uptime: {UPTIME_PERCENTAGE}% per bulan
   - Planned maintenance: max {MAINTENANCE_HOURS} jam/bulan, notifikasi 48 jam sebelumnya

2. RESPONSE TIME
   | Severity | Response | Resolution |
   |----------|----------|------------|
   | Critical | 1 jam    | 4 jam      |
   | High     | 4 jam    | 24 jam     |
   | Medium   | 24 jam   | 72 jam     |
   | Low      | 72 jam   | 1 minggu   |

3. PENALTY CLAUSE
   Jika SLA dilanggar: kredit {PENALTY_PERCENTAGE}% dari tagihan bulan itu
   Max penalty: {MAX_PENALTY_PERCENTAGE}% per bulan

4. EXCLUSIONS
   Force majeure, acts of third-party providers beyond vendor control.

5. REPORTING
   Monthly SLA report dikirim maksimal tanggal {REPORT_DAY} tiap bulan.
```

---

## Key Clauses Library

Essential clauses for liability, termination, IP, and dispute resolution.


### Payment Terms
```
KLAUSUL PEMBAYARAN STANDAR:
- DP: 50% upon signing
- Final: 50% upon delivery/milestone
- Late payment: 2% per month interest
- Payment method: Bank transfer to {ACCOUNT}
- Currency: IDR (or USD if international)
- Invoice: NET-{DAYS} from invoice date
```

### IP Ownership
```
KLAUSUL HAK KEKAYAAN INTELEKTUAL:
OPSI A (Work-for-hire — client owns):
Seluruh hasil pekerjaan yang dibuat dalam ruang lingkup PKS ini secara
otomatis menjadi milik Pihak Pertama (klien) setelah pembayaran lunas.

OPSI B (Licensor keeps IP — agency/vendor owns):
Pihak Kedua tetap memiliki IP atas tools, metodologi, dan karya sebelumnya.
Pihak Pertama mendapat lisensi non-eksklusif, non-transferable untuk
penggunaan yang disepakati.

OPSI C (Joint ownership):
IP dikembangkan bersama dimiliki bersama 50/50. Penggunaan komersial
memerlukan persetujuan bersama.
```

### Non-Compete
```
KLAUSUL NON-COMPETE:
Pihak Kedua setuju bahwa selama kontrak DAN {MONTHS} bulan setelah
terminasi, tidak akan:
a) Bekerja untuk kompetitor langsung: {COMPETITOR_LIST}
b) Menghubungi klien Pihak Pertama secara langsung
c) Mendirikan bisnis yang bersaing di bidang {SCOPE}

Geografis: {GEOGRAPHIC_SCOPE}
Catatan: Non-compete >12 bulan sulit ditegakkan di Indonesia.
```

### Termination Clause
```
KLAUSUL TERMINASI:
TERMINASI DENGAN PEMBERITAHUAN:
Salah satu pihak dapat mengakhiri PKS ini dengan memberikan notice
{NOTICE_DAYS} hari secara tertulis.

TERMINASI SEGERA (Cause):
PKS dapat diakhiri segera tanpa notice jika:
- Material breach yang tidak diperbaiki dalam 14 hari setelah notifikasi
- Kebangkrutan/insolvency
- Pelanggaran hukum yang signifikan
- Force majeure > {FM_DAYS} hari

AKIBAT TERMINASI:
- Pembayaran yang sudah jatuh tempo tetap harus dibayar
- Pengembalian aset/data dalam {RETURN_DAYS} hari
- NDA tetap berlaku {NDA_DURATION} tahun setelah terminasi
```

### Governing Law & Dispute Resolution
```
KLAUSUL PENYELESAIAN SENGKETA:
1. Musyawarah: Para pihak mengutamakan penyelesaian musyawarah
   dalam 30 hari setelah sengketa muncul.

2. Mediasi: Jika musyawarah gagal, mediasi melalui BANI
   (Badan Arbitrase Nasional Indonesia) dalam 60 hari.

3. Arbitrase/Pengadilan: Jika mediasi gagal, penyelesaian melalui:
   OPSI A: BANI (binding arbitration, lebih cepat)
   OPSI B: Pengadilan Negeri {JURISDICTION} (public, slower)

Hukum yang berlaku: Hukum Republik Indonesia.
```

---

## Tracking System

Track contract status, renewal dates, and obligation deadlines.


### Contract Registry (`contracts/registry.csv`)

```csv
id,type,party,start_date,end_date,value_idr,status,renewal_alert,payment_milestone,file_path,notes
TLT-001,TALENT,@jendralbot_handle,2026-01-01,2026-12-31,0,ACTIVE,2026-11-01,monthly,active/talent/TALENT-JENDRALBOT-20260101-v1.pdf,Revenue share deal
CLT-001,CLIENT,Acme Brand,2026-03-01,2026-03-31,15000000,ACTIVE,2026-03-24,on-delivery,active/client/CLIENT-ACME-20260301-v1.pdf,Campaign Feb
VND-001,VENDOR,Hostinger,2026-01-15,2027-01-15,1200000,ACTIVE,2026-12-15,annual,active/vendor/VENDOR-HOSTINGER-20260115-v1.pdf,Hosting renewal
EMP-001,EMPLOYMENT,Sony Ops,2026-03-01,2027-02-28,6000000,ACTIVE,2027-01-01,monthly,active/employment/EMPLOYMENT-PKWT-SONY-20260301-v1.pdf,PKWT 1 tahun
```

### Status Codes

| Status | Meaning |
|--------|---------|
| DRAFT | Being written, not sent |
| REVIEW | Under internal review |
| NEGOTIATE | Sent to counterparty, pending counter |
| PENDING_SIGN | Both agreed, awaiting signatures |
| ACTIVE | Fully signed, running |
| BREACH | Party in breach, remediation active |
| EXPIRED | Past end date, not renewed |
| TERMINATED | Ended early |
| ARCHIVE | Filed away, no action needed |

---

## Scripts

Automation scripts for contract generation, tracking, and alerts.


### `scripts/contract_tracker.py`

```python
#!/usr/bin/env python3
"""
Contract Tracker — reads registry.csv and shows dashboard.
Usage: python3 scripts/contract_tracker.py [--status active] [--type talent]
"""

import csv
import json
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path

REGISTRY = Path(__file__).parent.parent / "contracts" / "registry.csv"
ALERT_DAYS = [30, 7, 1]  # Days before expiry to flag

STATUS_EMOJI = {
    "DRAFT": "📝",
    "REVIEW": "🔍",
    "NEGOTIATE": "🤝",
    "PENDING_SIGN": "✍️",
    "ACTIVE": "✅",
    "BREACH": "🚨",
    "EXPIRED": "⏰",
    "TERMINATED": "❌",
    "ARCHIVE": "📦",
}

def load_contracts(status_filter=None, type_filter=None):
    contracts = []
    if not REGISTRY.exists():
        print(f"[ERROR] Registry not found: {REGISTRY}")
        return []
    with open(REGISTRY) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if status_filter and row["status"].upper() != status_filter.upper():
                continue
            if type_filter and row["type"].upper() != type_filter.upper():
                continue
            contracts.append(row)
    return contracts

def days_until(date_str):
    """Returns days until a date string (YYYY-MM-DD). Negative = overdue."""
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - date.today()).days
    except:
        return None

def get_expiring_soon(contracts, threshold_days=30):
    expiring = []
    for c in contracts:
        if c["status"] != "ACTIVE":
            continue
        days = days_until(c.get("end_date", ""))
        if days is not None and 0 <= days <= threshold_days:
            expiring.append({**c, "_days_left": days})
    return sorted(expiring, key=lambda x: x["_days_left"])

def get_breaches(contracts):
    breaches = []
    for c in contracts:
        if c["status"] == "BREACH":
            breaches.append(c)
        elif c["status"] == "ACTIVE":
            days = days_until(c.get("end_date", ""))
            if days is not None and days < 0:
                breaches.append({**c, "_overdue_days": abs(days), "_auto": True})
    return breaches

def print_dashboard(contracts):
    today = date.today()
    active = [c for c in contracts if c["status"] == "ACTIVE"]
    expiring_30 = get_expiring_soon(contracts, 30)
    expiring_7 = get_expiring_soon(contracts, 7)
    breaches = get_breaches(contracts)

    print("\n" + "="*60)
    print(f"📋 CONTRACT DASHBOARD — {today}")
    print("="*60)
    print(f"\n📊 SUMMARY")
    print(f"  Total contracts: {len(contracts)}")
    for status, emoji in STATUS_EMOJI.items():
        count = sum(1 for c in contracts if c["status"] == status)
        if count > 0:
            print(f"  {emoji} {status}: {count}")

    if breaches:
        print(f"\n🚨 BREACHES / OVERDUE ({len(breaches)})")
        for c in breaches:
            print(f"  [{c['id']}] {c['party']} — {c['type']}")

    if expiring_7:
        print(f"\n⚠️  EXPIRING ≤7 DAYS ({len(expiring_7)})")
        for c in expiring_7:
            print(f"  [{c['id']}] {c['party']} — {c['_days_left']}d left — ends {c['end_date']}")

    if expiring_30:
        print(f"\n📅 EXPIRING ≤30 DAYS ({len(expiring_30)})")
        for c in expiring_30:
            print(f"  [{c['id']}] {c['party']} — {c['_days_left']}d left — ends {c['end_date']}")

    if active:
        print(f"\n✅ ALL ACTIVE CONTRACTS ({len(active)})")
        for c in active:
            days = days_until(c.get("end_date", ""))
            days_str = f"{days}d" if days is not None else "ongoing"
            value = f"Rp {int(c['value_idr']):,}" if c.get('value_idr') else "—"
            print(f"  [{c['id']}] {c['party']} | {c['type']} | {value} | {days_str} left")

    print("\n" + "="*60 + "\n")

def main():
    parser = argparse.ArgumentParser(description="BerkahKarya Contract Tracker")
    parser.add_argument("--status", help="Filter by status (active, draft, etc.)")
    parser.add_argument("--type", help="Filter by type (talent, client, vendor, employment)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--expiring", type=int, default=None, help="Show contracts expiring in N days")
    args = parser.parse_args()

    contracts = load_contracts(args.status, args.type)

    if args.json:
        if args.expiring:
            print(json.dumps(get_expiring_soon(contracts, args.expiring), indent=2))
        else:
            print(json.dumps(contracts, indent=2))
        return

    if args.expiring:
        expiring = get_expiring_soon(contracts, args.expiring)
        for c in expiring:
            print(f"[{c['id']}] {c['party']} — {c['_days_left']} days left")
        return

    print_dashboard(contracts)

if __name__ == "__main__":
    main()
```

---

### `scripts/renewal_alert.py`

```python
#!/usr/bin/env python3
"""
Renewal Alert System — sends Telegram alerts for expiring contracts.
Runs via cron daily at 09:00 WIB.

Cron: 0 9 * * * cd /path/to/contracts && python3 scripts/renewal_alert.py

Setup:
  export TELEGRAM_BOT_TOKEN="your_bot_token"
  export TELEGRAM_CHAT_ID="your_chat_id"  # or @channel_name
"""

import csv
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, date, timedelta
from pathlib import Path

REGISTRY = Path(__file__).parent.parent / "contracts" / "registry.csv"
ALERT_THRESHOLDS = [30, 7, 1]  # Days before expiry

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# State file to avoid duplicate alerts
STATE_FILE = Path(__file__).parent.parent / "contracts" / ".alert_state.json"


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def send_telegram(message: str) -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[TELEGRAM NOT CONFIGURED]\n{message}")
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }).encode()
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        urllib.request.urlopen(req, timeout=10)
        return True
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")
        return False


def days_until(date_str):
    try:
        target = datetime.strptime(date_str, "%Y-%m-%d").date()
        return (target - date.today()).days
    except:
        return None


def check_and_alert():
    today = str(date.today())
    state = load_state()
    alerts_sent = 0

    if not REGISTRY.exists():
        print(f"[ERROR] Registry not found: {REGISTRY}")
        return

    contracts = []
    with open(REGISTRY) as f:
        contracts = list(csv.DictReader(f))

    for c in contracts:
        if c["status"] not in ("ACTIVE", "PENDING_SIGN"):
            continue

        days = days_until(c.get("end_date", ""))
        if days is None:
            continue

        for threshold in ALERT_THRESHOLDS:
            if days == threshold:
                alert_key = f"{c['id']}_{threshold}d_{today}"
                if alert_key in state.get("sent", []):
                    continue  # Already sent today

                urgency = "🚨" if threshold <= 1 else "⚠️" if threshold <= 7 else "📅"
                msg = (
                    f"{urgency} *CONTRACT EXPIRY ALERT*\n\n"
                    f"📋 Contract: `{c['id']}`\n"
                    f"👤 Party: {c['party']}\n"
                    f"🏷️ Type: {c['type']}\n"
                    f"📅 Expires: {c['end_date']} ({days} days)\n"
                    f"💰 Value: Rp {int(c.get('value_idr', 0) or 0):,}\n"
                    f"📁 File: {c.get('file_path', 'N/A')}\n\n"
                    f"{'⚡ ACTION REQUIRED — 1 DAY LEFT!' if threshold <= 1 else '⚡ Renew or close out before deadline.'}"
                )
                sent = send_telegram(msg)
                if sent:
                    state.setdefault("sent", []).append(alert_key)
                    alerts_sent += 1
                    print(f"[ALERT SENT] {c['id']} — {threshold}d warning")

        # Breach detection: active contract past end date
        if days < 0 and c["status"] == "ACTIVE":
            breach_key = f"BREACH_{c['id']}_{today}"
            if breach_key not in state.get("sent", []):
                msg = (
                    f"🚨 *CONTRACT BREACH / OVERDUE*\n\n"
                    f"📋 Contract: `{c['id']}`\n"
                    f"👤 Party: {c['party']}\n"
                    f"📅 Expired: {c['end_date']} ({abs(days)} days ago)\n"
                    f"❗ Status still ACTIVE — update registry!\n\n"
                    f"Action: Renew, terminate, or update status to EXPIRED."
                )
                sent = send_telegram(msg)
                if sent:
                    state.setdefault("sent", []).append(breach_key)
                    alerts_sent += 1

    save_state(state)
    print(f"[DONE] {alerts_sent} alerts sent | {today}")


if __name__ == "__main__":
    check_and_alert()
```

---

## E-Signature Options

Key aspects of contract-manager relevant to this section.


### Free / Low-Cost Options (Recommended for Indonesia)

| Tool | Cost | Legal in ID? | Use Case |
|------|------|--------------|----------|
| **Privy.id** | Freemium | ✅ Yes (BSrE certified) | Best for Indonesian contracts |
| **PeruriSign** | Paid | ✅ Yes (Government) | High-stakes, legal proceedings |
| **DocuSign** | Paid | ✅ Accepted | International contracts |
| **Adobe Sign** | Paid | ✅ Accepted | Enterprise use |
| **SignWell** | Free (5/mo) | ✅ Accepted | Low volume |
| **PDF + WhatsApp** | Free | ⚠️ Debatable | Small informal deals, add materai |

### Materai Digital

- For Indonesian legal enforceability: use **e-Materai** from Peruri
- Cost: Rp 10.000/materai
- URL: https://ematerai.peruri.co.id
- Required for contracts > Rp 5,000,000 or legally sensitive

### Workflow (Privy.id Recommended)

```
1. Draft contract in Google Docs / Word
2. Export to PDF
3. Upload to Privy.id
4. Add e-Materai if needed (Peruri)
5. Send signing link to counterparty
6. Download signed PDF
7. File in contracts/active/{type}/
8. Update registry.csv
```

---

## Indonesian Law Compliance

Key aspects of contract-manager relevant to this section.


### PKS Format Requirements

A valid PKS (Perjanjian Kerja Sama) in Indonesia must have:

- [ ] Nomor PKS (unique reference number)
- [ ] Tanggal dan tempat penandatanganan
- [ ] Identitas para pihak (nama, NIK/NPWP, alamat)
- [ ] Lingkup pekerjaan yang jelas
- [ ] Jangka waktu
- [ ] Nilai dan mekanisme pembayaran
- [ ] Hak dan kewajiban masing-masing pihak
- [ ] Klausul kerahasiaan (jika diperlukan)
- [ ] Penyelesaian sengketa
- [ ] Tanda tangan + materai Rp 10.000
- [ ] 2 orang saksi (strongly recommended)

### References

| Law | Scope |
|-----|-------|
| KUH Perdata Pasal 1320 | Syarat sah perjanjian |
| UU No. 13/2003 | Ketenagakerjaan |
| PP No. 35/2021 | PKWT, alih daya |
| UU No. 11/2008 (ITE) | Kontrak elektronik |
| PP No. 71/2019 | Tanda tangan elektronik |
| UU No. 28/2014 | Hak Cipta |
| UU No. 20/2016 | Merek dan Indikasi Geografis |

---

## Quick Commands

```bash
# Run contract dashboard
python3 scripts/contract_tracker.py

# Show only active contracts
python3 scripts/contract_tracker.py --status active

# Show talent contracts only
python3 scripts/contract_tracker.py --type talent

# Show contracts expiring in 30 days
python3 scripts/contract_tracker.py --expiring 30

# Run renewal alerts manually (also runs via cron)
python3 scripts/renewal_alert.py

# Export registry as JSON
python3 scripts/contract_tracker.py --json

# Setup Telegram alerts (set env vars first)
export TELEGRAM_BOT_TOKEN="bot_token_here"
export TELEGRAM_CHAT_ID="@berkahkarya_ops"
python3 scripts/renewal_alert.py
```

### Cron Setup

```bash
# Add to crontab: crontab -e
# Run daily at 09:00 WIB (UTC+7 = UTC+0 02:00)
0 2 * * * cd /home/openclaw/.openclaw/workspace/contracts && TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=yyy python3 scripts/renewal_alert.py >> logs/renewal_alert.log 2>&1
```

---

## Checklist: New Contract Workflow

Step-by-step workflow for this skill.


### Drafting
- [ ] Choose correct template (service/talent/NDA/SLA/employment)
- [ ] Fill all `{PLACEHOLDERS}`
- [ ] Add correct contract type prefix to filename
- [ ] Set realistic payment terms
- [ ] Include governing law clause
- [ ] Review IP ownership clause

### Before Signing
- [ ] Internal review done
- [ ] Payment terms match what you can fulfill
- [ ] End date + renewal alert date set in registry
- [ ] Materai added (Rp 10.000 physical or e-materai)
- [ ] 2 witnesses identified
- [ ] E-signature platform set up

### After Signing
- [ ] Signed PDF saved to `contracts/active/{type}/`
- [ ] Naming convention followed
- [ ] Registry CSV updated
- [ ] Calendar reminder set for renewal (30d before end)
- [ ] Payment milestones added to finance tracker
- [ ] Send copy to counterparty

---

*🔥 Vilona — BerkahKarya Contract Manager v1.0*
*Every deal documented. Every deadline owned.*

## When to Use

- Managing contract lifecycle (creation, review, signing, renewal)
- Tracking contract deadlines and milestones
- Automating contract document generation
- Managing contract templates and versions
- Tracking contract obligations and compliance

## When NOT to Use

- Task requires creative problem-solving or novel approaches
- You need to understand the contract deeply, not just manage it
- Legal review is required (consult a lawyer)
- Contract is for a one-time, simple agreement
- You don't have the contract template or source document
- Task requires negotiation, not just document management

## Red Flags

- Missing contract deadlines
- Not tracking contract versions
- Ignoring contract obligations
- Not backing up contract documents
- Missing approval workflows

## Verification

- [ ] Contracts are stored securely
- [ ] Deadlines are tracked and alerted
- [ ] Versions are managed properly
- [ ] Approval workflows are in place
- [ ] Compliance is tracked
- [ ] No placeholder content or TODOs remain