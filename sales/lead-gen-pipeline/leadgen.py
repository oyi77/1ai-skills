#!/usr/bin/env python3
"""
leadgen.py — BerkahKarya Lead Generation Pipeline
================================================
Search → Scrape → Qualify (0-100) → Outreach → Track

Usage:
    python3 leadgen.py --industry fnb --location jakarta --limit 10
    python3 leadgen.py --all-industries --location surabaya --limit 5
    python3 leadgen.py --dry-run --industry retail --location bandung --limit 3
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, date
from typing import Optional

# ─── Constants ───────────────────────────────────────────────────────────────

BRAND = "BerkahKarya Digital Agency"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
LEADS_CSV = os.path.join(OUTPUT_DIR, "leads.csv")

RATE_LIMIT_SEARCH = 2.5   # seconds between search queries
RATE_LIMIT_SCRAPE = 3.0   # seconds between page fetches
RATE_LIMIT_BATCH  = 10.0  # seconds pause after every 10 leads
MAX_RETRIES = 3

CSV_COLUMNS = [
    "timestamp", "name", "industry", "location", "website", "phone",
    "instagram", "facebook", "tiktok", "source_url",
    "score", "tier",
    "size_score", "social_score", "digital_score", "industry_score",
    "notes", "outreach_channel", "outreach_status", "follow_up_date",
    "raw_snippet"
]

# ─── Industry Config ──────────────────────────────────────────────────────────

INDUSTRIES = {
    "fnb": {
        "label": "FnB (Resto/Kafe/Catering)",
        "queries": [
            "{location} restoran kafe populer instagram",
            "{location} catering makanan online pesan",
            "{location} kuliner viral tiktok 2024",
            "{location} coffee shop baru buka",
        ],
        "keywords": ["resto", "restoran", "kafe", "cafe", "catering", "kuliner",
                     "makanan", "minuman", "warung", "kedai", "bakery", "pastry"],
        "pain_signal": ["pesan online", "go-food", "grab-food", "shopee food",
                        "menu digital", "food delivery"],
        "size_signal": ["cabang", "outlet", "franchise", "pusat", "branch"],
    },
    "retail": {
        "label": "Retail (Toko/Oleh-oleh/Minimarket)",
        "queries": [
            "{location} toko oleh-oleh produk lokal online",
            "{location} retail fashion toko online tokopedia",
            "{location} toko sembako minimarket modern",
            "{location} produk UMKM lokal marketplace",
        ],
        "keywords": ["toko", "store", "retail", "oleh-oleh", "minimarket",
                     "supermarket", "warung", "kios", "lapak", "dagang"],
        "pain_signal": ["tokopedia", "shopee", "lazada", "bukalapak", "marketplace",
                        "toko online", "cod", "ongkir"],
        "size_signal": ["cabang", "chain", "waralaba", "distributor", "grosir"],
    },
    "fashion": {
        "label": "Fashion (Butik/Distro/Konveksi)",
        "queries": [
            "{location} butik fashion wanita instagram",
            "{location} distro brand lokal clothing",
            "{location} konveksi seragam baju custom",
            "{location} hijab fashion muslim online",
        ],
        "keywords": ["butik", "boutique", "fashion", "distro", "clothing",
                     "konveksi", "garmen", "hijab", "baju", "pakaian"],
        "pain_signal": ["instagram", "katalog", "lookbook", "pre-order",
                        "limited edition", "drop"],
        "size_signal": ["showroom", "workshop", "pabrik", "produksi", "reseller"],
    },
    "beauty": {
        "label": "Beauty (Salon/Spa/Klinik Kecantikan)",
        "queries": [
            "{location} salon kecantikan booking online",
            "{location} spa wellness treatment terbaik",
            "{location} klinik kecantikan aesthetic",
            "{location} beauty center perawatan wajah",
        ],
        "keywords": ["salon", "spa", "klinik", "kecantikan", "beauty",
                     "aesthetic", "perawatan", "treatment", "skincare", "barbershop"],
        "pain_signal": ["booking", "reservasi", "whatsapp", "appointment",
                        "promo member", "loyalty"],
        "size_signal": ["cabang", "franchise", "pusat kecantikan", "chain", "klinik utama"],
    },
    "education": {
        "label": "Pendidikan (Kursus/Bimbel/Pelatihan)",
        "queries": [
            "{location} kursus pelatihan skill daftar online",
            "{location} bimbel les privat siswa",
            "{location} lembaga training sertifikasi",
            "{location} kursus coding desain digital",
        ],
        "keywords": ["kursus", "bimbel", "les", "pelatihan", "training",
                     "lembaga", "sekolah", "akademi", "workshop", "bootcamp"],
        "pain_signal": ["daftar online", "pendaftaran", "whatsapp", "grup",
                        "modul digital", "e-learning"],
        "size_signal": ["cabang", "pusat", "kampus", "gedung", "angkatan", "batch"],
    },
}

# ─── Scoring Helpers ──────────────────────────────────────────────────────────

def score_company_size(text: str, industry_cfg: dict) -> tuple[int, str]:
    """Score 0-25 based on company size signals."""
    text_lower = text.lower()
    notes = []
    score = 5  # baseline: exists as a business

    for signal in industry_cfg.get("size_signal", []):
        if signal in text_lower:
            score += 8
            notes.append(f"size:{signal}")
            break

    # Employee/scale mentions
    if re.search(r'\b(puluhan|ratusan|ribuan)\s+(karyawan|pegawai|staff)', text_lower):
        score += 10
        notes.append("has_employees_mention")
    if re.search(r'\b\d+\s*(cabang|outlet|toko)\b', text_lower):
        score += 7
        notes.append("multi_location")

    return min(score, 25), ", ".join(notes)


def score_social_presence(text: str) -> tuple[int, str]:
    """Score 0-25 based on social media presence."""
    text_lower = text.lower()
    score = 0
    notes = []

    social_weights = {
        "instagram": 8, "tiktok": 8, "facebook": 5,
        "youtube": 4, "twitter": 3, "linkedin": 3,
        "@": 3, "#": 2,
    }
    for platform, pts in social_weights.items():
        if platform in text_lower:
            score += pts
            notes.append(platform)

    # Followers/engagement hints
    if re.search(r'\b\d+[kK]\s*(follower|pengikut|subscriber)', text_lower):
        score += 5
        notes.append("has_follower_count")

    return min(score, 25), ", ".join(notes)


def score_digital_maturity(text: str) -> tuple[int, str]:
    """Score 0-25 based on digital/online maturity."""
    text_lower = text.lower()
    score = 0
    notes = []

    maturity_signals = {
        "website": 7, ".com": 6, ".id": 6, "www.": 6,
        "online": 5, "digital": 5, "e-commerce": 6,
        "tokopedia": 4, "shopee": 4, "lazada": 4, "gofood": 4, "grabfood": 4,
        "whatsapp": 3, "wa.me": 4, "link.tree": 4, "linktree": 4,
        "google maps": 3, "google bisnis": 3,
    }
    for signal, pts in maturity_signals.items():
        if signal in text_lower:
            score += pts
            notes.append(signal)

    return min(score, 25), ", ".join(notes)


def score_industry_fit(text: str, industry_cfg: dict) -> tuple[int, str]:
    """Score 0-25 based on industry keyword alignment."""
    text_lower = text.lower()
    score = 0
    notes = []

    # Core keyword matches
    keyword_hits = [kw for kw in industry_cfg["keywords"] if kw in text_lower]
    score += min(len(keyword_hits) * 4, 15)
    if keyword_hits:
        notes.append(f"keywords:{','.join(keyword_hits[:3])}")

    # Pain signal matches (higher value — they have the pain we solve)
    pain_hits = [p for p in industry_cfg["pain_signal"] if p in text_lower]
    score += min(len(pain_hits) * 3, 10)
    if pain_hits:
        notes.append(f"pain:{','.join(pain_hits[:2])}")

    return min(score, 25), ", ".join(notes)


def qualify_lead(name: str, snippet: str, industry: str) -> dict:
    """Full lead qualification — returns score dict."""
    cfg = INDUSTRIES[industry]
    combined = f"{name} {snippet}"

    size_score, size_notes = score_company_size(combined, cfg)
    social_score, social_notes = score_social_presence(combined)
    digital_score, digital_notes = score_digital_maturity(combined)
    industry_score, industry_notes = score_industry_fit(combined, cfg)

    total = size_score + social_score + digital_score + industry_score
    tier = (
        "🟢 Hot"   if total >= 75 else
        "🟡 Warm"  if total >= 50 else
        "🟠 Cold"  if total >= 25 else
        "🔴 Skip"
    )

    return {
        "score": total,
        "tier": tier,
        "size_score": size_score,
        "social_score": social_score,
        "digital_score": digital_score,
        "industry_score": industry_score,
        "notes": f"size[{size_notes}] social[{social_notes}] digital[{digital_notes}] industry[{industry_notes}]",
    }


# ─── Extraction Helpers ───────────────────────────────────────────────────────

def extract_phone(text: str) -> str:
    patterns = [
        r'(?:\+62|62|0)[\s-]?8[\d]{8,11}',
        r'08[\d]{8,11}',
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0).strip()
    return ""


def extract_website(text: str) -> str:
    m = re.search(r'https?://[^\s\'"<>]+', text)
    if m:
        url = m.group(0).rstrip('.,)')
        return url
    m = re.search(r'(?:www\.|[a-z0-9-]+\.(?:com|id|co\.id|net|org))[^\s\'"<>]*', text, re.I)
    if m:
        return m.group(0)
    return ""


def extract_instagram(text: str) -> str:
    m = re.search(r'(?:instagram\.com/|@)([a-zA-Z0-9._]{3,30})', text, re.I)
    if m:
        return "@" + m.group(1)
    return ""


def extract_name_from_snippet(snippet: str, query: str) -> str:
    """Best-effort company name extraction."""
    # Try to get the first meaningful phrase (title-like)
    lines = snippet.strip().split('\n')
    if lines:
        first = lines[0].strip()
        if 5 < len(first) < 80:
            return first
    # Fallback: first sentence
    sentences = re.split(r'[.!?]', snippet)
    if sentences:
        return sentences[0].strip()[:70]
    return "Unknown"


# ─── Search & Discovery ───────────────────────────────────────────────────────

def web_search_tool(query: str) -> list[dict]:
    """
    Call web_search via OpenClaw CLI.
    Returns list of {title, url, snippet} dicts.
    """
    try:
        import subprocess
        cmd = [
            "openclaw", "search", "--json", "--count", "8", query
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "results" in data:
                return data["results"]
    except Exception:
        pass

    # Fallback: use Brave Search API directly via urllib if env var set
    api_key = os.environ.get("BRAVE_API_KEY", "")
    if api_key:
        try:
            encoded = urllib.parse.quote(query)
            url = f"https://api.search.brave.com/res/v1/web/search?q={encoded}&count=8&country=id"
            req = urllib.request.Request(url, headers={
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": api_key,
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw = resp.read()
                data = json.loads(raw)
                results = []
                for item in data.get("web", {}).get("results", []):
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("description", ""),
                    })
                return results
        except Exception as e:
            print(f"  [WARN] Brave search error: {e}", file=sys.stderr)

    # Mock fallback for --dry-run / offline testing
    print(f"  [WARN] No search backend available. Using mock data for: {query}", file=sys.stderr)
    return _mock_results(query)


def _mock_results(query: str) -> list[dict]:
    """Mock search results for testing/dry-run mode."""
    location = re.search(r'\b(jakarta|bandung|surabaya|yogyakarta|medan)\b', query, re.I)
    loc = location.group(0).title() if location else "Jakarta"
    return [
        {
            "title": f"Restoran Maju Jaya {loc}",
            "url": f"https://www.restomajujaya.co.id",
            "snippet": (
                f"Restoran Maju Jaya {loc} — Melayani delivery via GoFood & GrabFood. "
                f"Instagram @restomajujaya | 2 cabang di {loc} | WhatsApp 08123456789"
            ),
        },
        {
            "title": f"Kafe Bintang {loc}",
            "url": f"https://maps.google.com/?q=kafebintang{loc.lower()}",
            "snippet": (
                f"Kafe Bintang {loc} — Coffee shop hits di pusat kota. Pesan via website "
                f"atau WhatsApp. Follow kami di Instagram & TikTok @kafebintang"
            ),
        },
        {
            "title": f"Catering Berkah {loc}",
            "url": f"https://cateringberkah.id",
            "snippet": (
                f"Catering Berkah {loc} — Nasi kotak & prasmanan untuk event. "
                f"Tokopedia & Shopee tersedia. Hubungi 081234567890"
            ),
        },
    ]


def search_leads(industry: str, location: str, limit: int, verbose: bool = True) -> list[dict]:
    """Run all queries for an industry and return raw lead candidates."""
    cfg = INDUSTRIES[industry]
    all_results = []
    seen_urls = set()

    queries = [q.format(location=location) for q in cfg["queries"]]

    for i, query in enumerate(queries):
        if len(all_results) >= limit:
            break

        if verbose:
            print(f"  🔍 Searching: {query}")

        results = web_search_tool(query)
        time.sleep(RATE_LIMIT_SEARCH)

        for r in results:
            if len(all_results) >= limit:
                break
            url = r.get("url", "")
            if url in seen_urls:
                continue
            seen_urls.add(url)

            name = r.get("title", "").strip() or extract_name_from_snippet(
                r.get("snippet", ""), query
            )
            snippet = r.get("snippet", "")

            all_results.append({
                "name": name[:100],
                "source_url": url,
                "raw_snippet": (snippet or "")[:500],
                "industry": industry,
                "location": location,
                "website": extract_website(f"{url} {snippet}"),
                "phone": extract_phone(snippet),
                "instagram": extract_instagram(snippet),
                "facebook": "",
                "tiktok": "",
            })

        # Batch pause every 10 results
        if i > 0 and i % 3 == 0:
            time.sleep(RATE_LIMIT_BATCH)

    return all_results


# ─── Outreach Template Loader ─────────────────────────────────────────────────

def load_wa_template(industry: str) -> str:
    """Load WhatsApp template for industry."""
    wa_path = os.path.join(TEMPLATES_DIR, "whatsapp_templates.md")
    if not os.path.exists(wa_path):
        return f"Halo! Kami dari {BRAND}, tertarik kerja sama dengan bisnis Anda."

    with open(wa_path, "r") as f:
        content = f.read()

    # Find the industry section
    pattern = rf'##\s+{re.escape(industry.upper())}.*?(?=##|\Z)'
    m = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if m:
        block = m.group(0)
        # Extract first template (```...```)
        tmpl = re.search(r'```(?:text)?\n(.*?)```', block, re.DOTALL)
        if tmpl:
            return tmpl.group(1).strip()

    return f"Halo! Kami dari {BRAND}, tertarik kerja sama dengan bisnis Anda."


# ─── CSV Management ───────────────────────────────────────────────────────────

def ensure_csv(path: str):
    """Create CSV with headers if it doesn't exist."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            writer.writeheader()
        print(f"  📄 Created: {path}")


def load_existing_leads(path: str) -> set:
    """Return set of existing source_urls to avoid duplicates."""
    seen = set()
    if not os.path.exists(path):
        return seen
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                url = row.get("source_url", "").strip()
                if url:
                    seen.add(url)
    except Exception:
        pass
    return seen


def append_leads(path: str, leads: list[dict]):
    """Append leads to CSV."""
    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        for lead in leads:
            writer.writerow(lead)


# ─── Daily Summary ────────────────────────────────────────────────────────────

def generate_summary(leads: list[dict], date_str: str) -> str:
    """Generate daily markdown summary."""
    if not leads:
        return f"# Lead Gen Summary — {date_str}\n\nNo leads found today.\n"

    tiers = {"🟢 Hot": [], "🟡 Warm": [], "🟠 Cold": [], "🔴 Skip": []}
    industries_count = {}
    for lead in leads:
        tier = lead.get("tier", "🔴 Skip")
        tiers.setdefault(tier, []).append(lead)
        ind = lead.get("industry", "unknown")
        industries_count[ind] = industries_count.get(ind, 0) + 1

    top5 = sorted(leads, key=lambda x: x.get("score", 0), reverse=True)[:5]

    lines = [
        f"# 🎯 Lead Gen Summary — {date_str}",
        f"\n**Brand:** {BRAND}",
        f"**Total Leads Processed:** {len(leads)}",
        f"**Qualified (≥50):** {len(tiers['🟢 Hot']) + len(tiers['🟡 Warm'])}",
        "",
        "## Score Distribution",
        "",
        f"| Tier | Count | % |",
        f"|------|-------|---|",
    ]
    for tier, tleds in tiers.items():
        pct = round(len(tleds) / len(leads) * 100) if leads else 0
        lines.append(f"| {tier} | {len(tleds)} | {pct}% |")

    lines += ["", "## Industry Breakdown", ""]
    for ind, cnt in sorted(industries_count.items()):
        lines.append(f"- **{INDUSTRIES.get(ind, {}).get('label', ind)}:** {cnt} leads")

    lines += ["", "## 🔥 Top 5 Leads", ""]
    for i, lead in enumerate(top5, 1):
        lines.append(f"### {i}. {lead.get('name', 'Unknown')}")
        lines.append(f"- **Score:** {lead.get('score', 0)}/100 — {lead.get('tier', '')}")
        lines.append(f"- **Industry:** {lead.get('industry', '')}")
        lines.append(f"- **Location:** {lead.get('location', '')}")
        if lead.get("phone"):
            lines.append(f"- **Phone:** {lead['phone']}")
        if lead.get("instagram"):
            lines.append(f"- **Instagram:** {lead['instagram']}")
        if lead.get("website"):
            lines.append(f"- **Website:** {lead['website']}")
        lines.append(f"- **Source:** {lead.get('source_url', '')}")
        lines.append("")

    lines += [
        "## Outreach Priority",
        "",
        f"1. 🟢 **Hot leads ({len(tiers['🟢 Hot'])}):** Send WhatsApp TODAY",
        f"2. 🟡 **Warm leads ({len(tiers['🟡 Warm'])}):** Start email nurture sequence",
        f"3. 🟠 **Cold leads ({len(tiers['🟠 Cold'])}):** Schedule follow-up in 14 days",
        "",
        "---",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB by {BRAND}* 🔥",
    ]

    return "\n".join(lines)


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def run_pipeline(
    industry: str,
    location: str,
    limit: int,
    dry_run: bool,
    output_path: str,
    min_score: int,
    verbose: bool = True,
) -> list[dict]:
    """Single-industry pipeline run."""
    cfg = INDUSTRIES[industry]
    print(f"\n{'='*60}")
    print(f"🏭 Industry: {cfg['label']}")
    print(f"📍 Location: {location.title()}")
    print(f"🎯 Limit:    {limit} leads")
    print(f"{'='*60}")

    # Step 1: Search
    print("\n[1/4] 🔍 Searching for leads...")
    raw_leads = search_leads(industry, location, limit, verbose)
    print(f"  Found {len(raw_leads)} raw candidates")

    if not raw_leads:
        print("  ⚠️ No leads found. Check search backend or try different location.")
        return []

    # Step 2: Qualify
    print("\n[2/4] 📊 Qualifying leads...")
    qualified = []
    for lead in raw_leads:
        qual = qualify_lead(lead["name"], lead["raw_snippet"], industry)
        lead.update(qual)
        lead["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lead["outreach_channel"] = "whatsapp" if lead.get("phone") else "email"
        lead["outreach_status"] = "pending"
        lead["follow_up_date"] = ""
        qualified.append(lead)

        tier_icon = lead["tier"].split()[0]
        if verbose:
            print(f"  {tier_icon} [{lead['score']:>3}/100] {lead['name'][:50]}")

    # Filter by min_score
    before = len(qualified)
    qualified = [l for l in qualified if l["score"] >= min_score]
    skipped = before - len(qualified)
    print(f"\n  ✅ Qualified: {len(qualified)} | Skipped (score<{min_score}): {skipped}")

    if not qualified:
        print("  ⚠️ No leads met minimum score threshold.")
        return []

    # Step 3: Generate outreach previews
    print("\n[3/4] ✉️  Generating outreach previews...")
    wa_template = load_wa_template(industry)
    for lead in qualified:
        lead["_wa_template"] = wa_template  # not saved to CSV

    # Step 4: Track
    if dry_run:
        print("\n[4/4] 🔵 DRY RUN — No files written.")
        print("\nSample lead (top scorer):")
        top = max(qualified, key=lambda x: x["score"])
        for k in ["name", "score", "tier", "phone", "instagram", "website", "source_url"]:
            print(f"  {k:20}: {top.get(k, '')}")
        print(f"\n  WA Template preview:\n  {wa_template[:200]}...")
    else:
        print(f"\n[4/4] 💾 Writing to {output_path}...")
        ensure_csv(output_path)
        existing_urls = load_existing_leads(output_path)
        new_leads = [l for l in qualified if l.get("source_url", "") not in existing_urls]
        duplicates = len(qualified) - len(new_leads)
        if duplicates:
            print(f"  ⚠️ Skipped {duplicates} duplicate(s)")
        if new_leads:
            append_leads(output_path, new_leads)
            print(f"  ✅ Saved {len(new_leads)} new leads")
        else:
            print("  ℹ️ All leads already in database")

    return qualified


def print_summary_report(all_leads: list[dict], dry_run: bool):
    """Print + optionally save daily summary."""
    today = date.today().strftime("%Y-%m-%d")
    summary = generate_summary(all_leads, today)

    print("\n" + "="*60)
    print(summary)

    if not dry_run:
        summary_path = os.path.join(OUTPUT_DIR, f"summary_{today}.md")
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"\n📋 Summary saved: {summary_path}")


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description=f"BerkahKarya Lead Generation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 leadgen.py --industry fnb --location jakarta --limit 10
  python3 leadgen.py --all-industries --location surabaya --limit 5
  python3 leadgen.py --dry-run --industry retail --location bandung --limit 3
  python3 leadgen.py --industry beauty --location jakarta --min-score 60 --summary
        """,
    )
    parser.add_argument(
        "--industry",
        choices=list(INDUSTRIES.keys()),
        default="fnb",
        help="Target industry (default: fnb)",
    )
    parser.add_argument(
        "--all-industries",
        action="store_true",
        help="Run all 5 industries sequentially",
    )
    parser.add_argument(
        "--location",
        default="jakarta",
        help="City/region to target (default: jakarta)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max leads per industry run (default: 10)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview only — do not write files",
    )
    parser.add_argument(
        "--output",
        default=LEADS_CSV,
        help=f"CSV output path (default: {LEADS_CSV})",
    )
    parser.add_argument(
        "--min-score",
        type=int,
        default=40,
        help="Minimum score to save lead (default: 40)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print daily markdown summary",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose per-lead output",
    )

    args = parser.parse_args()

    print(f"\n🔥 {BRAND} — Lead Generation Pipeline")
    print(f"   {'[DRY RUN] ' if args.dry_run else ''}Location: {args.location.title()}")
    print(f"   {'All industries' if args.all_industries else args.industry.upper()}")
    print(f"   Limit: {args.limit} | Min Score: {args.min_score}")

    industries_to_run = list(INDUSTRIES.keys()) if args.all_industries else [args.industry]
    all_leads = []

    for ind in industries_to_run:
        try:
            leads = run_pipeline(
                industry=ind,
                location=args.location,
                limit=args.limit,
                dry_run=args.dry_run,
                output_path=args.output,
                min_score=args.min_score,
                verbose=not args.quiet,
            )
            all_leads.extend(leads)
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user.")
            break
        except Exception as e:
            print(f"\n❌ Error running {ind}: {e}", file=sys.stderr)
            continue

        if args.all_industries and ind != industries_to_run[-1]:
            print(f"\n⏳ Pausing {RATE_LIMIT_BATCH}s before next industry...")
            time.sleep(RATE_LIMIT_BATCH)

    if args.summary or args.all_industries:
        print_summary_report(all_leads, args.dry_run)

    print(f"\n✅ Done! Total leads processed: {len(all_leads)}")
    hot = [l for l in all_leads if "Hot" in l.get("tier", "")]
    warm = [l for l in all_leads if "Warm" in l.get("tier", "")]
    print(f"   🟢 Hot: {len(hot)} | 🟡 Warm: {len(warm)}")

    if hot and not args.dry_run:
        print(f"\n🚨 Action required: {len(hot)} hot leads — send WhatsApp TODAY!")


if __name__ == "__main__":
    main()
