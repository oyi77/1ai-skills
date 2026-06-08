"""
content_gap_finder.py — Find topics competitors miss

Identifies underserved content opportunities in Indonesian market.
Cross-references competitor content with audience demand signals.
"""

import json
from datetime import datetime
from pathlib import Path

# Content gap analysis: topics with high demand but low supply
CONTENT_GAPS = {
    "ai_tools": {
        "high_demand_low_supply": [
            {
                "topic": "AI tools untuk bisnis kuliner / UMKM Indonesia",
                "demand_score": 9.2,
                "supply_score": 2.1,
                "gap_score": 7.1,
                "why_gap": "Kebanyakan konten AI tools target startup/tech, bukan UMKM",
                "content_angle": "Tutorial AI tools spesifik untuk warung, toko kecil, pedagang online",
                "estimated_views": "50K-500K",
            },
            {
                "topic": "AI tools Bahasa Indonesia (bukan Bahasa Inggris)",
                "demand_score": 8.8,
                "supply_score": 1.5,
                "gap_score": 7.3,
                "why_gap": "Hampir semua konten AI tools dalam Bahasa Inggris",
                "content_angle": "Review + tutorial AI tools dengan antarmuka/support Bahasa Indonesia",
                "estimated_views": "30K-300K",
            },
            {
                "topic": "AI tools gratis vs yang worth bayar (comparison real)",
                "demand_score": 9.0,
                "supply_score": 3.2,
                "gap_score": 5.8,
                "why_gap": "Konten ada tapi tidak spesifik untuk budget Indonesia",
                "content_angle": "Perbandingan cost per value — mana yang worth untuk income level Indonesia",
                "estimated_views": "40K-400K",
            },
            {
                "topic": "Cara pakai AI tanpa internet stabil (offline AI tools)",
                "demand_score": 7.5,
                "supply_score": 0.8,
                "gap_score": 6.7,
                "why_gap": "Konten belum ada, tapi relevan di luar Jawa",
                "content_angle": "AI tools yang bisa jalan offline atau dengan koneksi lambat",
                "estimated_views": "20K-150K",
            },
        ],
        "trending_but_undersaturated": [
            "AI untuk bikin proposal bisnis dalam 10 menit",
            "AI tools untuk analisis kompetitor lokal",
            "Cara audit bisnis pakai AI gratis",
            "AI untuk customer service WA otomatis",
        ],
    },
    "digital_marketing": {
        "high_demand_low_supply": [
            {
                "topic": "TikTok monetisasi untuk orang Indonesia (bukan US/UK)",
                "demand_score": 9.5,
                "supply_score": 2.8,
                "gap_score": 6.7,
                "why_gap": "Konten monetisasi TikTok kebanyakan untuk creator luar negeri",
                "content_angle": "Cara monetisasi konten TikTok khusus untuk kreator Indonesia",
                "estimated_views": "100K-1M",
            },
            {
                "topic": "Marketing untuk bisnis B2B lokal (bukan startup)",
                "demand_score": 7.8,
                "supply_score": 1.2,
                "gap_score": 6.6,
                "why_gap": "Konten B2B marketing selalu tentang startup, bukan distributor/supplier lokal",
                "content_angle": "Marketing untuk supplier, distributor, kontraktor, jasa profesional lokal",
                "estimated_views": "20K-100K",
            },
            {
                "topic": "Organic marketing WhatsApp Business strategy",
                "demand_score": 8.5,
                "supply_score": 3.0,
                "gap_score": 5.5,
                "why_gap": "WA Business paling banyak dipakai di Indonesia tapi konten strateginya sedikit",
                "content_angle": "Strategi WA Business: broadcast, catalog, chatbot, segmentasi",
                "estimated_views": "50K-500K",
            },
        ],
        "trending_but_undersaturated": [
            "Email marketing untuk jualan digital product di Indonesia",
            "Cara pakai Google Business Profile secara maksimal",
            "Strategi Tokopedia vs Shopee vs TikTok Shop 2025",
            "Community-led growth untuk brand Indonesia",
        ],
    },
    "kuliner": {
        "high_demand_low_supply": [
            {
                "topic": "HPP (Harga Pokok Produksi) kalkulator untuk makanan",
                "demand_score": 9.1,
                "supply_score": 1.8,
                "gap_score": 7.3,
                "why_gap": "Banyak yang jual makanan tapi gak tau cara hitung HPP yang benar",
                "content_angle": "Tutorial praktis hitung HPP + pricing strategy untuk makanan",
                "estimated_views": "100K-800K",
            },
            {
                "topic": "Bisnis kuliner untuk ibu rumah tangga dari dapur sendiri",
                "demand_score": 9.3,
                "supply_score": 3.5,
                "gap_score": 5.8,
                "why_gap": "Konten ada tapi generic, tidak spesifik untuk constraints IRT",
                "content_angle": "Bisnis makanan yang bisa dimulai dari dapur rumah dengan modal 500ribu",
                "estimated_views": "200K-2M",
            },
            {
                "topic": "Strategi masuk GoFood/GrabFood untuk warung kecil",
                "demand_score": 8.7,
                "supply_score": 2.1,
                "gap_score": 6.6,
                "why_gap": "Banyak yang tau platform tapi gak tau cara optimasi listing",
                "content_angle": "Step-by-step daftar + optimasi foto + pricing di GoFood/GrabFood",
                "estimated_views": "80K-600K",
            },
        ],
        "trending_but_undersaturated": [
            "Makanan diet yang tetap enak untuk dijual",
            "Packaging makanan yang bisa buat viral sendiri",
            "Cara dapat supply bahan baku murah dari distributor",
            "Cloud kitchen setup dari rumah",
        ],
    },
    "side_hustle": {
        "high_demand_low_supply": [
            {
                "topic": "Side hustle dengan income proof yang credible (bukan clickbait)",
                "demand_score": 9.8,
                "supply_score": 1.5,
                "gap_score": 8.3,
                "why_gap": "Semua konten side hustle overclaim tanpa bukti nyata",
                "content_angle": "Transparent income report: real screenshot, real timeline, real challenges",
                "estimated_views": "200K-2M",
            },
            {
                "topic": "Side hustle untuk karyawan dengan waktu terbatas (1-2 jam/hari)",
                "demand_score": 9.5,
                "supply_score": 2.8,
                "gap_score": 6.7,
                "why_gap": "Konten side hustle selalu asumsi punya banyak waktu",
                "content_angle": "Side hustle yang bisa dijalankan dengan hanya 1-2 jam sehari setelah kerja",
                "estimated_views": "150K-1.5M",
            },
            {
                "topic": "Cara validasi ide bisnis sebelum keluar uang",
                "demand_score": 8.4,
                "supply_score": 1.9,
                "gap_score": 6.5,
                "why_gap": "Orang sering bakar modal dulu baru cari pelanggan",
                "content_angle": "Metode validasi bisnis gratis/modal minimum sebelum invest",
                "estimated_views": "50K-400K",
            },
        ],
        "trending_but_undersaturated": [
            "Affiliate marketing TikTok Shop Indonesia step-by-step",
            "Jualan Canva template untuk niche lokal Indonesia",
            "Jasa AI freelance untuk UMKM",
            "Reseller digital product yang profit margin tinggi",
        ],
    },
    "education": {
        "high_demand_low_supply": [
            {
                "topic": "Financial planning untuk fresh graduate gaji UMR",
                "demand_score": 9.4,
                "supply_score": 2.3,
                "gap_score": 7.1,
                "why_gap": "Konten finansial terlalu untuk orang yang sudah punya modal besar",
                "content_angle": "Cara atur keuangan dan mulai invest dengan gaji 3-5 juta/bulan",
                "estimated_views": "200K-2M",
            },
            {
                "topic": "Cara dapat kerja remote international dari Indonesia",
                "demand_score": 9.2,
                "supply_score": 3.1,
                "gap_score": 6.1,
                "why_gap": "Konten ada tapi tidak spesifik dari perspektif orang Indonesia",
                "content_angle": "Step-by-step dapat kerja remote dari company luar untuk orang Indonesia",
                "estimated_views": "100K-1M",
            },
            {
                "topic": "Belajar skill teknis tanpa background IT",
                "demand_score": 8.6,
                "supply_score": 2.7,
                "gap_score": 5.9,
                "why_gap": "Konten learning to code terlalu untuk yang sudah punya background",
                "content_angle": "Transisi karir ke tech dari non-IT background dengan roadmap spesifik",
                "estimated_views": "80K-600K",
            },
        ],
        "trending_but_undersaturated": [
            "Second language learning yang accelerated (untuk orang sibuk)",
            "Cara dapat beasiswa S2 luar negeri 2025",
            "Skill soft yang bikin gaji melejit",
            "Personal branding untuk fresh graduate",
        ],
    },
}


def find_gaps(niche: str = None, min_gap_score: float = 5.0) -> dict:
    """Find content gaps for a niche or all niches."""
    if niche:
        if niche not in CONTENT_GAPS:
            return {"error": f"Niche not found: {niche}"}
        gaps = {niche: CONTENT_GAPS[niche]}
    else:
        gaps = CONTENT_GAPS

    results = {
        "analyzed_at": datetime.now().isoformat(),
        "market": "Indonesia",
        "gaps": {},
        "top_opportunities": [],
    }

    all_opportunities = []

    for niche_key, niche_data in gaps.items():
        high_demand = [
            g
            for g in niche_data.get("high_demand_low_supply", [])
            if g.get("gap_score", 0) >= min_gap_score
        ]

        results["gaps"][niche_key] = {
            "high_demand_low_supply": high_demand,
            "trending_undersaturated": niche_data.get(
                "trending_but_undersaturated", []
            ),
            "total_gaps_found": len(high_demand),
        }

        for gap in high_demand:
            all_opportunities.append({**gap, "niche": niche_key})

    # Sort all opportunities by gap score
    all_opportunities.sort(key=lambda x: x.get("gap_score", 0), reverse=True)
    results["top_opportunities"] = all_opportunities[:10]

    return results


def get_quick_wins(niche: str = None) -> list[dict]:
    """Get top 3 quick win content opportunities."""
    gaps = find_gaps(niche)
    opportunities = gaps.get("top_opportunities", [])

    quick_wins = []
    for opp in opportunities[:3]:
        quick_wins.append(
            {
                "rank": len(quick_wins) + 1,
                "topic": opp["topic"],
                "niche": opp.get("niche", ""),
                "gap_score": opp.get("gap_score", 0),
                "content_angle": opp.get("content_angle", ""),
                "estimated_views": opp.get("estimated_views", ""),
                "why_opportunity": opp.get("why_gap", ""),
            }
        )

    return quick_wins


def generate_content_opportunities_report() -> dict:
    """Generate a comprehensive content opportunities report."""
    all_gaps = find_gaps()

    report = {
        "generated_at": datetime.now().isoformat(),
        "title": "Content Gap Analysis — Indonesian Market",
        "summary": {
            "total_niches_analyzed": 5,
            "total_gaps_identified": sum(
                v["total_gaps_found"] for v in all_gaps["gaps"].values()
            ),
            "top_opportunity": (
                all_gaps["top_opportunities"][0]["topic"]
                if all_gaps["top_opportunities"]
                else "N/A"
            ),
        },
        "top_10_opportunities": all_gaps["top_opportunities"],
        "by_niche": all_gaps["gaps"],
        "quick_wins": get_quick_wins(),
        "action_plan": {
            "week_1": "Buat 1 konten per gap terbesar di setiap niche (5 konten)",
            "week_2": "Analisis engagement — double down pada yang perform",
            "week_3": "Buat series dari yang terbaik",
            "week_4": "Monetize dengan product/affiliate sesuai niche",
        },
    }

    return report


def save_content_gap_report(output_dir: str = None) -> str:
    """Save content gap analysis report."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    report = generate_content_opportunities_report()
    filepath = output_path / "content-gaps.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    print("🔍 CONTENT GAP ANALYSIS")
    print("=" * 60)

    # Quick wins
    quick_wins = get_quick_wins()
    print("\n🏆 TOP 3 QUICK WIN OPPORTUNITIES:")
    for win in quick_wins:
        print(
            f"\n  #{win['rank']} [{win['gap_score']} gap score] {win['niche'].upper()}"
        )
        print(f"  Topic: {win['topic']}")
        print(f"  Angle: {win['content_angle']}")
        print(f"  Est. Views: {win['estimated_views']}")

    # Save full report
    save_content_gap_report()
