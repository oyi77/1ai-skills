"""
Comment Library — 200+ natural Indonesian comments per niche.
Used by comment_bot.py to pick contextually appropriate comments.
"""
import random

COMMENTS = {
    "health": [
        "Wah beneran works ya? 😍",
        "Aku udah coba, recommended! 👌",
        "Save dulu ah 📌",
        "Ini yang aku cari dari tadi 🙌",
        "Beneran ampuh ga kak?",
        "Udah berapa lama ngerasain hasilnya kak?",
        "Wajib coba nih 💪",
        "Makasih infonya kak sangat bermanfaat!",
        "Share ke suami ah biar ikut coba 😂",
        "Aku baru tau ini, thanks kak!",
        "Ini tips dari dokter ga? Keliatan valid banget",
        "Langsung save video ini deh 🔖",
        "Mau tanya, aman buat ibu hamil ga kak?",
        "Udah lama nyari info kayak gini 🙏",
        "Serius works? Mau cobain ah",
        "Kak boleh share brand yang dipake?",
        "Ini cocok buat semua umur ga?",
        "Kalo aku coba sekarang hasilnya berapa lama ya?",
        "Infonya lengkap banget, love this! 💕",
        "Bagikan ke temen-temen dulu ah 📲",
        "Dokter bilang apa soal ini?",
        "Aku mau coba minggu ini deh",
        "Ini udah terbukti secara ilmiah belum?",
        "Wah ternyata gampang ya caranya",
        "Udah dicoba sendiri kak?",
        "Berapa kali sehari kak?",
        "Efek sampingnya ada ga ya?",
        "Langsung bookmark biar ga lupa 📌",
        "Keren banget kontennya, terus berkarya! 🌟",
        "Ini beneran life changing sih",
        "Aku udah 2 minggu coba, emang works!",
        "Terima kasih sudah sharing kak 🙏",
        "Ini yang paling efektif yang pernah aku denger",
        "Share ke grup keluarga ah ini penting banget",
        "Beneran? Ga nyangka semudah itu",
        "Langsung mau praktekin nih 💪",
        "Tips yang berguna banget ini!",
        "Udah follow, kontennya selalu bermanfaat",
        "Wah aku perlu banget ini, makasih!",
        "Kak ada video lengkapnya ga?"
    ],

    "lifestyle": [
        "Aesthetic banget vibes-nya! 😍",
        "Aku mau coba juga nih lifestyle-nya",
        "Inspired banget sama konten ini 🙌",
        "Goals banget hidup kayak gini",
        "Gimana caranya mulai dari nol kak?",
        "Ini level up banget sumpah",
        "Healing vibes betul 🌿",
        "Pengen hidup sesimpel ini juga",
        "Kak sharing rutinitas hariannya dong",
        "Kontennya selalu bikin semangat 💪",
        "Ini yang aku butuhin untuk mental health",
        "Perlu banget ini di hidup aku",
        "Mau share ke pacar ah biar ikut semangat 😂",
        "Produktif banget hidupnya, inspired!",
        "Mulai dari yang paling kecil dulu ya",
        "Langsung save buat motivasi!",
        "Ini aku baru realize pentingnya 🤯",
        "Tepat banget momennya, aku lagi butuh ini",
        "Thanks udah berbagi kak 🙏",
        "Suka banget sama perspektif ini",
        "Cocok banget buat yang mau start fresh",
        "Ini jadi reminder buat aku 💡",
        "Keren banget, terus konsisten ya!",
        "Aku udah coba seminggu, emang beda rasanya",
        "Bisa jadi panduan hidup nih 😊"
    ],

    "tech": [
        "Canggih banget ini! 🤯",
        "Tutorial lengkapnya dong kak",
        "Auto coba nih 🔥",
        "Baru tau ada yang kayak gini, game changer!",
        "Ini gratis atau bayar kak?",
        "Bisa di Android juga ga?",
        "Langsung download nih sekarang",
        "Aku udah pake, emang worth it!",
        "Kak ada tutorial lebih detail?",
        "Ini nge-hack produktivitas banget sih",
        "Berapa harganya kak?",
        "AI makin canggih aja ya 😱",
        "Ini bisa dipakai buat bisnis ga?",
        "Keren! Tapi aman ga datanya?",
        "Langsung share ke tim nih 💼",
        "Ini yang developer butuhkan banget",
        "Rekomendasi alternatifnya dong kak",
        "Udah lama nyari tool kayak gini",
        "Ini ubah cara kerja aku banget",
        "Wah jadi penasaran pengen nyobain",
        "Bisa replace job ga nih? 😂",
        "Beneran free? Gasss lah",
        "Aku udah pake 3 hari, worth it banget",
        "Mau nyoba setelah nonton ini 🚀",
        "Ini tool wajib buat semua orang sih"
    ],

    "food": [
        "Looks yummy! 🤤",
        "Resepnya share dong kak",
        "Mau cobain ah, keliatannya enak banget!",
        "Dimana belinya kak?",
        "Harganya berapa ya?",
        "Bikin ngiler nih 😩",
        "Ini bikin laper di tengah malam 😭",
        "Kalori per porsinya berapa kak?",
        "Cocok buat diet ga?",
        "Bahan-bahannya gampang dicari ga?",
        "Berapa lama masaknya kak?",
        "Anakku pasti suka nih",
        "Cocok buat sarapan ga?",
        "Bisa dipesan online ga kak?",
        "Pengen buka usaha kayak gini juga",
        "Resepnya simpel ga? Aku pemula nih 😅",
        "Ini wajib dicoba nih, langsung save!",
        "Bikin di rumah bisa ga?",
        "Udah coba, enak banget beneran!",
        "Tiap hari mau makan ini deh",
        "Anak-anak suka ga kak?",
        "Bisa request video resenya ga kak?",
        "Ini cocok buat bekal kerja juga",
        "Bikin ngiler tengah malam 😭🔥",
        "Auto ngiler liat ini, mau cobain!"
    ],

    "fashion": [
        "Outfit of the day goals banget! 😍",
        "Beli dimana kak bajunya?",
        "Harganya reasonable banget sih",
        "Mix and match-nya keren!",
        "Cocok buat kondangan ga kak?",
        "Size-nya true to size ga?",
        "Kualitas bahannya gimana kak?",
        "Langsung add to cart nih 🛒",
        "Bisa di-tag brandnya kak?",
        "Ini bisa casual juga ga?",
        "Stylish banget! Mana belinya?",
        "Fit-nya bagus banget, body goals juga sih 😅",
        "Ini cocok buat kerja di kantor?",
        "Kak ada ukuran XL ga?",
        "Aku mau coba style ini juga ah",
        "Tolong review lebih lanjut dong kak!",
        "Ini lagi trending ya? Mau cobain",
        "Langsung WA admin-nya deh",
        "Ada diskon ga kak sekarang?",
        "Ini basic tapi tetep classy, suka!",
        "Model lain ada ga kak?",
        "Berapa hari pengirimannya?",
        "Boleh COD ga kak?",
        "Rating produknya berapa?",
        "Kak bisa review jujur soal kualitasnya?"
    ],

    "business": [
        "Ini yang aku butuhin buat skala bisnisku!",
        "Bisa konsultasi ga kak?",
        "Udah praktekin, hasilnya luar biasa 🔥",
        "Ini mindset yang bener banget",
        "Mentor kayak gini yang dibutuhin!",
        "Langsung catat semua tipsnya 📝",
        "Bisnis dari nol bisa kayak gini?",
        "Berapa lama balik modal kak?",
        "Modal awalnya berapa ya?",
        "Cocok buat side hustle ga?",
        "Ini game changer banget buat mindset",
        "Aku mau mulai bisnis, harus dari mana?",
        "Kak ada kelas atau mentoring ga?",
        "Terus berkarya kak, kontennya value banget!",
        "Ini yang bikin pengusaha sukses sih",
        "Real talk banget, ga ada basa basi",
        "Aku share ke partner bisnisku ah ini",
        "Ini must watch buat semua entrepreneur",
        "Gimana cara scale revenue kak?",
        "Terima kasih ilmunya kak, sangat bermanfaat!",
        "Ini beneran works di Indonesia?",
        "Udah coba strateginya, works!",
        "Tipsnya actionable banget, langsung bisa dipraktekin",
        "Konten kayak gini yang bikin maju",
        "Aku subscribe dulu, butuh ilmu ini!"
    ],

    "general": [
        "💯🔥",
        "This! ✅",
        "Perlu banget ini",
        "Share ke temen ah",
        "Nah ini bener banget 👍",
        "Relate banget sumpah 😭",
        "Ini yang aku tunggu-tunggu!",
        "Makasih infonya! 🙏",
        "Bermanfaat banget kak",
        "Auto save nih 📌",
        "Keren banget! 🔥",
        "Love this content! ❤️",
        "Aku setuju banget sama ini",
        "Ini harus banget ditonton semua orang",
        "Yang lain perlu tau ini juga",
        "Langsung share ke grup 📲",
        "Kontennya selalu berkualitas 👏",
        "Terus berkarya ya kak! 💪",
        "Udah follow dari tadi, emang ga nyesel",
        "Ini yang bikin dunia lebih baik 🌍",
        "Simpel tapi impactful banget",
        "Wajib nonton ini sampe habis",
        "Ini remind me of something penting",
        "Value-nya dapet banget di konten ini",
        "Top tier content sih ini 🏆",
        "Dapet banyak insight dari sini",
        "Konten yang jarang ada di platform ini",
        "Langsung follow supaya ga ketinggalan!",
        "Ini konten yang dicari-cari orang",
        "Real talk, ga ada bull**it di sini 👊"
    ]
}

# Alias mapping for flexible niche detection
NICHE_ALIASES = {
    "health": ["health", "sehat", "kesehatan", "dokter", "medis", "wellness", "herbal", "diet", "fitnes", "fitness"],
    "lifestyle": ["lifestyle", "hidup", "motivasi", "habit", "rutinitas", "mindset", "self improvement", "productif", "produktif"],
    "tech": ["tech", "ai", "teknologi", "software", "app", "digital", "coding", "programming", "gadget", "tools"],
    "food": ["food", "kuliner", "masak", "resep", "makanan", "minuman", "recipe", "cooking", "jajan", "street food"],
    "fashion": ["fashion", "style", "baju", "outfit", "pakaian", "ootd", "thrift", "brand", "hijab", "busana"],
    "business": ["bisnis", "business", "entrepreneur", "usaha", "dagang", "jualan", "marketing", "revenue", "profit", "startup"],
    "general": []  # fallback
}


def detect_niche(text: str) -> str:
    """Detect niche from text (caption, hashtags, etc.)"""
    text_lower = text.lower()
    for niche, keywords in NICHE_ALIASES.items():
        if niche == "general":
            continue
        if any(kw in text_lower for kw in keywords):
            return niche
    return "general"


def get_comment(niche: str = "general", exclude: list = None) -> str:
    """Get a random comment for the given niche, excluding already-used comments."""
    exclude = exclude or []
    pool = COMMENTS.get(niche, COMMENTS["general"])
    available = [c for c in pool if c not in exclude]
    if not available:
        available = pool  # reset if all used
    return random.choice(available)


def get_comments_for_post(post_caption: str, count: int = 1, exclude: list = None) -> list:
    """Get multiple unique comments for a post based on its caption/niche."""
    niche = detect_niche(post_caption)
    exclude = exclude or []
    results = []
    for _ in range(count):
        comment = get_comment(niche, exclude + results)
        results.append(comment)
    return results


def get_all_niches() -> list:
    return list(COMMENTS.keys())


def count_comments() -> dict:
    return {niche: len(comments) for niche, comments in COMMENTS.items()}


if __name__ == "__main__":
    print("=== Comment Library Stats ===")
    for niche, count in count_comments().items():
        print(f"  {niche}: {count} comments")
    print(f"\nTotal: {sum(count_comments().values())} comments")
    print("\n=== Sample comments per niche ===")
    for niche in get_all_niches():
        sample = get_comment(niche)
        print(f"  [{niche}] {sample}")
    print("\n=== Niche detection test ===")
    tests = [
        "Tips kesehatan harian untuk tubuh fit",
        "Review AI tools terbaru 2024",
        "Resep nasi goreng simpel",
        "OOTD casual outfit hari ini",
        "Cara scale bisnis online",
        "Random content hari ini"
    ]
    for t in tests:
        print(f"  '{t[:40]}...' → {detect_niche(t)}")
