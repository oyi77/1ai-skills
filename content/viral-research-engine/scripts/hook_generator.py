"""
hook_generator.py — Generate viral hooks based on trends

Creates ready-to-use hooks for Indonesian market content.
Combines trend data + proven patterns for maximum viral potential.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Optional


# Hook templates with fill slots
HOOK_TEMPLATES = {
    "old_vs_new": {
        "template": "Kamu masih {old_way}? Coba {new_way}...",
        "virality": 8.2,
        "format": "Tutorial",
        "slots": ["old_way", "new_way"],
    },
    "shocking_number": {
        "template": "{number} {thing} yang bisa {outcome} dalam {timeframe}",
        "virality": 9.1,
        "format": "Listicle",
        "slots": ["number", "thing", "outcome", "timeframe"],
    },
    "confession": {
        "template": "Jujur, gue dulu {negative_situation}. Sekarang {positive_outcome}.",
        "virality": 9.4,
        "format": "Storytelling",
        "slots": ["negative_situation", "positive_outcome"],
    },
    "warning_stop": {
        "template": "STOP {bad_action} sebelum kamu tau ini...",
        "virality": 9.7,
        "format": "Controversy",
        "slots": ["bad_action"],
    },
    "before_after": {
        "template": "{before} → {after} dalam {timeframe}",
        "virality": 8.8,
        "format": "Before/After",
        "slots": ["before", "after", "timeframe"],
    },
    "question": {
        "template": "Tau gak kamu bisa {outcome} cuma dengan {simple_method}?",
        "virality": 7.5,
        "format": "Tutorial",
        "slots": ["outcome", "simple_method"],
    },
    "secret": {
        "template": "Rahasia {expert_type} yang gak banyak orang tau di Indonesia",
        "virality": 8.6,
        "format": "Reveal",
        "slots": ["expert_type"],
    },
    "fomo": {
        "template": "Kalau kamu gak {action} sekarang, kamu bakal {negative_consequence}",
        "virality": 9.3,
        "format": "Warning",
        "slots": ["action", "negative_consequence"],
    },
    "proof_first": {
        "template": "Ini hasil {timeframe} setelah gue {method} — gak nyangka",
        "virality": 8.9,
        "format": "Social Proof",
        "slots": ["timeframe", "method"],
    },
    "controversy": {
        "template": "Semua orang salah tentang {topic} — ini faktanya",
        "virality": 9.5,
        "format": "Hot Take",
        "slots": ["topic"],
    },
}

# Niche-specific fill values
NICHE_FILLS = {
    "ai_tools": {
        "old_way": ["edit konten manual berjam-jam", "bayar desainer mahal", "riset kompetitor manual", "buat caption sendiri"],
        "new_way": ["AI tools gratis ini", "Canva AI dalam 5 menit", "tools AI ini cukup 10 menit", "ChatGPT prompt ini"],
        "number": ["5", "7", "3", "10"],
        "thing": ["AI tools gratis", "prompt ChatGPT", "tools produktivitas AI", "cara pakai AI untuk bisnis"],
        "outcome": ["naikkan revenue bisnismu", "hemat 10 jam/minggu", "tingkatkan produktivitas 5x", "gantiin posisi yang butuh gaji"],
        "timeframe": ["sebulan", "seminggu", "2 minggu", "30 hari"],
        "negative_situation": ["gapake AI sama sekali", "bayar mahal untuk tools", "gak tau AI tools apa yang ada"],
        "positive_outcome": ["hemat Rp 5 juta/bulan pakai AI gratis", "jalankan bisnis sendiri tanpa karyawan", "semua otomatis pakai AI"],
        "bad_action": ["bayar mahal untuk tools premium", "abaikan AI tools sekarang", "pakai ChatGPT cara yang salah"],
        "before": ["Kerja 12 jam sehari", "Bayar Rp 3 juta/bulan untuk tools", "Manual semuanya"],
        "after": ["Kerja 4 jam dengan AI", "Pakai tools AI gratis semua", "Otomatis dengan AI"],
        "expert_type": ["AI power user", "startup founder", "freelancer berpenghasilan tinggi"],
        "action": ["pelajari AI tools ini", "mulai pakai AI sekarang", "update cara kerja kamu"],
        "negative_consequence": ["ketinggalan 3 tahun dari kompetitor", "digantikan orang yang bisa AI", "rugi jutaan karena inefficient"],
        "method": ["pakai AI tools gratis", "otomatisasi semua dengan AI", "ganti tools manual dengan AI"],
        "topic": ["ChatGPT", "AI tools berbayar", "prompt engineering"],
        "simple_method": ["1 prompt ChatGPT", "tools gratis ini", "cara ini yang 99% orang belum tau"],
        "outcome": ["otomatisasi seluruh bisnismu", "buat konten 30 hari dalam 2 jam", "hemat 20 jam kerja seminggu"],
    },
    "digital_marketing": {
        "old_way": ["bayar iklan tanpa strategi", "posting tanpa riset hashtag", "buat konten asal-asalan"],
        "new_way": ["formula konten viral ini", "strategi organik yang terbukti", "framework ini yang bikin follower naik"],
        "number": ["5", "7", "3", "10"],
        "thing": ["strategi konten gratis", "trik algoritma TikTok", "teknik copywriting"],
        "outcome": ["bikin konten viral", "dapat 1000 follower baru", "tingkatkan engagement 3x"],
        "timeframe": ["seminggu", "30 hari", "2 minggu"],
        "negative_situation": ["struggle dapat engagement", "konten gak pernah viral", "follower stuck di angka itu-itu"],
        "positive_outcome": ["viral dengan konten pertama", "10K followers dalam sebulan", "brand deal pertama"],
        "bad_action": ["posting tanpa strategi", "abaikan analytics kontenmu", "ikutin trend tanpa angle unik"],
        "before": ["0 engagement per post", "100 views per video", "posting random tiap hari"],
        "after": ["10K views konsisten", "5% engagement rate", "sistem konten yang jalan autopilot"],
        "expert_type": ["content creator 1 juta followers", "digital marketer agency", "brand yang tumbuh organik"],
        "action": ["pelajari algoritma baru ini", "ganti strategi kontenmu", "terapkan formula ini"],
        "negative_consequence": ["shadow banned selamanya", "kalah dari kompetitor yang tau ini", "buang waktu konten yang gak ada hasilnya"],
        "method": ["terapkan formula hook ini", "konsisten dengan format ini", "riset kompetitor secara sistematis"],
        "topic": ["hashtag di 2025", "waktu posting terbaik", "engagement rate yang ideal"],
        "simple_method": ["1 perubahan ini", "formula hook 3 kata", "framework konten ini"],
        "outcome": ["triple engagement ratenya", "dapat brand deal pertama", "viral tanpa iklan"],
    },
    "kuliner": {
        "old_way": ["buka warung tanpa hitung margin", "jual makanan tanpa promosi", "bikin resep coba-coba"],
        "new_way": ["formula pricing bisnis kuliner ini", "strategi marketing makanan viral", "resep yang sudah terbukti laris"],
        "number": ["5", "3", "7"],
        "thing": ["menu yang bikin warung ramai", "strategi bisnis kuliner", "cara promosi makanan gratis"],
        "outcome": ["dobel omzet warungmu", "dapat pelanggan setia", "viral di TikTok food"],
        "timeframe": ["sebulan", "2 minggu", "30 hari"],
        "negative_situation": ["struggle bayar modal warung", "warung sepi terus", "gak tau harga yang tepat"],
        "positive_outcome": ["omzet 30 juta/bulan", "antrian panjang tiap hari", "bisa buka cabang kedua"],
        "bad_action": ["jual makanan tanpa hitung HPP", "abaikan review pelanggan", "ikutin trend makanan tanpa riset"],
        "before": ["Omzet Rp 1 juta/hari", "Warung sepi", "Modal tekor terus"],
        "after": ["Omzet Rp 10 juta/hari", "Antrian sampai luar", "Untung bersih 40%"],
        "expert_type": ["chef yang sukses bisnis", "pemilik warung viral", "food entrepreneur"],
        "action": ["pelajari pricing yang benar", "mulai dokumentasi masakmu", "riset menu yang lagi trending"],
        "negative_consequence": ["bangkrut karena margin salah", "kalah dari kompetitor yang lebih pintar marketing", "kehilangan pelanggan ke cloud kitchen"],
        "method": ["terapkan food cost formula ini", "marketing lewat TikTok food", "buat menu engineering yang benar"],
        "topic": ["harga makanan", "menu yang laris", "cara promosi kuliner"],
        "simple_method": ["1 perubahan menu ini", "strategi foto makanan ini", "caption food yang menarik"],
        "outcome": ["lipat omzet 3x tanpa tambah modal", "jadi warung most reviewed di Google Maps", "viral di TikTok food tanpa bayar influencer"],
    },
    "side_hustle": {
        "old_way": ["kerja 9-5 berharap naik gaji", "coba-coba bisnis tanpa plan", "invest di sesuatu yang gak kamu mengerti"],
        "new_way": ["sistem side hustle ini yang jalan autopilot", "bisnis digital dengan modal nol", "cara ini yang sudah proven works"],
        "number": ["5", "7", "3"],
        "thing": ["side hustle yang bisa dimulai sekarang", "cara cuan dari HP", "bisnis sampingan tanpa modal"],
        "outcome": ["hasilin jutaan tiap bulan", "punya penghasilan tambahan", "akhirnya bisa resign dari kantor"],
        "timeframe": ["sebulan", "30 hari", "3 bulan"],
        "negative_situation": ["gaji habis sebelum tanggal 20", "coba bisnis tapi selalu gagal", "takut investasi karena pernah rugi"],
        "positive_outcome": ["penghasilan tambahan Rp 5 juta/bulan", "resign dari kantor dengan confidence", "aset digital yang menghasilkan tiap bulan"],
        "bad_action": ["coba semua side hustle sekaligus", "ikutin skema yang gak jelas", "mulai bisnis tanpa validasi"],
        "before": ["Gaji Rp 5 juta, habis tanggal 20", "0 penghasilan dari online", "Kerja 10 jam sehari"],
        "after": ["Rp 10 juta/bulan dari side hustle", "Passive income dari konten", "Kerja 4 jam, sisa waktu untuk keluarga"],
        "expert_type": ["affiliate marketer sukses", "seller digital product", "freelancer 8 digit"],
        "action": ["mulai side hustle ini hari ini", "belajar skill yang dibayar tinggi", "validasi ide bisnismu dulu"],
        "negative_consequence": ["stuck di pekerjaan yang gak kamu suka selamanya", "inflasi makan tabunganmu habis", "orang lain yang lebih berani akan sukses duluan"],
        "method": ["jualan digital product", "affiliate marketing yang benar", "freelance dengan rate tinggi"],
        "topic": ["passive income", "dropship di 2025", "cara cepat kaya yang legit"],
        "simple_method": ["platform ini yang bayar dari konten", "cara ini yang belum banyak orang tau", "metode yang gue pakai sendiri"],
        "outcome": ["hasilin Rp 10 juta bulan pertama", "punya asset digital yang menghasilkan tiap hari", "akhirnya financial free"],
    },
    "education": {
        "old_way": ["belajar sistem sekolah konvensional", "bayar kursus mahal tanpa hasil", "baca buku motivasi tanpa action"],
        "new_way": ["sistem belajar yang proven ini", "kursus gratis yang lebih bagus dari yang berbayar", "metode yang bikin skill langsung applicable"],
        "number": ["5", "7", "3", "10"],
        "thing": ["kebiasaan orang sukses", "skill yang wajib dikuasai", "cara belajar yang lebih efektif"],
        "outcome": ["naik level dalam karir", "dapat skill bernilai tinggi", "financial free lebih cepat"],
        "timeframe": ["3 bulan", "6 bulan", "setahun", "30 hari"],
        "negative_situation": ["ngerasa stuck padahal udah kerja keras", "habis jutaan untuk kursus tapi gak ada hasilnya", "tau banyak tapi gak ada yang diimplementasi"],
        "positive_outcome": ["naik gaji 100% dalam 6 bulan", "dapat side income dari skill baru", "punya clarity tentang hidup"],
        "bad_action": ["abaikan financial literacy", "skip belajar skill digital", "nunggu kondisi 'tepat' sebelum mulai"],
        "before": ["Penghasilan minimum", "Skill yang sudah outdated", "Tidak tau harus invest di mana"],
        "after": ["Penghasilan 3x lipat", "Skill yang dicari perusahaan", "Portfolio investasi yang sehat"],
        "expert_type": ["investor sukses", "orang yang sudah financial free di 30an", "top performer perusahaan"],
        "action": ["mulai belajar skill ini sekarang", "perbaiki kebiasaan keuanganmu", "investasi di dirimu sendiri"],
        "negative_consequence": ["tetap stuck di posisi yang sama 5 tahun lagi", "inflasi hancurkan nilai tabunganmu", "AI replace pekerjaanmu sebelum kamu siap"],
        "method": ["sistem belajar 1 jam/hari ini", "portfolio building yang benar", "networking yang efektif"],
        "topic": ["investasi reksa dana", "cara belajar coding", "kebiasaan produktif"],
        "simple_method": ["aplikasi gratis ini", "metode belajar 20 menit/hari", "framework ini"],
        "outcome": ["naik gaji tanpa minta ke atasan", "dapat tawaran kerja sebelum resign", "mulai invest dengan modal 50 ribu"],
    },
}


def generate_hook(
    niche: str,
    hook_type: Optional[str] = None,
    count: int = 5,
    seed_topic: Optional[str] = None,
) -> list[dict]:
    """Generate viral hooks for a niche."""
    if niche not in NICHE_FILLS:
        return [{"error": f"Niche '{niche}' not found"}]

    fills = NICHE_FILLS[niche]

    if hook_type and hook_type not in HOOK_TEMPLATES:
        return [{"error": f"Hook type '{hook_type}' not found. Available: {list(HOOK_TEMPLATES.keys())}"}]

    templates_to_use = (
        {hook_type: HOOK_TEMPLATES[hook_type]}
        if hook_type
        else HOOK_TEMPLATES
    )

    generated = []

    for template_key, template_data in templates_to_use.items():
        template = template_data["template"]
        slots = template_data.get("slots", [])

        # Fill slots with niche-specific values
        filled = template
        for slot in slots:
            options = fills.get(slot, [f"[{slot}]"])
            value = random.choice(options)
            filled = filled.replace(f"{{{slot}}}", value, 1)

        generated.append({
            "hook": filled,
            "type": template_key,
            "format": template_data["format"],
            "virality_score": template_data["virality"],
            "niche": niche,
            "generated_at": datetime.now().isoformat(),
        })

        if len(generated) >= count:
            break

    # Sort by virality
    generated.sort(key=lambda x: x["virality_score"], reverse=True)
    return generated[:count]


def generate_full_content_brief(niche: str, topic: Optional[str] = None) -> dict:
    """Generate a full content brief with hook + structure + CTA."""
    hooks = generate_hook(niche, count=3)
    best_hook = hooks[0] if hooks else {}

    # Build content structure
    structure = {
        "hook": best_hook.get("hook", ""),
        "problem_statement": f"[Masalah yang relate ke audience {niche}]",
        "promise": "[Transformasi yang akan mereka dapat]",
        "body": "[3-5 poin utama konten]",
        "proof": "[Screenshot / angka / testimoni]",
        "cta": "[Ajakan spesifik: follow / comment / share / save]",
    }

    return {
        "niche": niche,
        "generated_at": datetime.now().isoformat(),
        "top_hook": best_hook.get("hook", ""),
        "hook_type": best_hook.get("type", ""),
        "format": best_hook.get("format", "Tutorial"),
        "content_structure": structure,
        "all_hooks_generated": hooks,
        "tips": [
            "Mulai langsung dengan hook — jangan intro",
            "Keep it under 60 detik untuk TikTok",
            "Gunakan text overlay di 3 detik pertama",
            "End dengan clear CTA",
        ],
    }


def batch_generate_hooks(niches: list = None, hooks_per_niche: int = 5) -> dict:
    """Generate hooks for multiple niches at once."""
    if niches is None:
        niches = list(NICHE_FILLS.keys())

    results = {
        "generated_at": datetime.now().isoformat(),
        "total_hooks": 0,
        "niches": {},
    }

    for niche in niches:
        hooks = generate_hook(niche, count=hooks_per_niche)
        results["niches"][niche] = hooks
        results["total_hooks"] += len(hooks)

    return results


def save_generated_hooks(output_dir: str = None) -> str:
    """Generate and save hooks for all niches."""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "data"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    data = batch_generate_hooks(hooks_per_niche=10)
    filepath = output_path / "generated-hooks.json"

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {data['total_hooks']} hooks to: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    print("🎣 HOOK GENERATOR TEST")
    print("=" * 60)

    # Test single niche
    hooks = generate_hook("ai_tools", count=5)
    print("\n🤖 AI Tools — Top 5 Hooks:")
    for h in hooks:
        print(f"\n  [{h['virality_score']}★] {h['type'].upper()}")
        print(f"  \"{h['hook']}\"")

    # Full content brief
    print("\n" + "=" * 60)
    brief = generate_full_content_brief("side_hustle")
    print(f"\n📋 CONTENT BRIEF (Side Hustle):")
    print(f"  Hook: {brief['top_hook']}")
    print(f"  Format: {brief['format']}")
    print(f"  Type: {brief['hook_type']}")

    # Save all
    save_generated_hooks()
