"""
faq_responder.py — Common question → instant answer mapper
Pre-built FAQ responses for most frequent Indonesian comment patterns
"""

import re
from typing import Optional

# ─── FAQ DATABASE ──────────────────────────────────────────────────────────────
# Format: (trigger_patterns, response)

FAQ_DATABASE = [
    # PRICE questions
    (
        [r"harga", r"berapa", r"price", r"bayar berapa", r"biaya", r"cost"],
        "Harganya cuma IDR 75.000 kak! Murah banget buat tools AI sekelas ini 🔥 Cek link di bio ya, lagi ada promo!"
    ),
    (
        [r"gratis", r"free", r"bayar ga", r"berbayar ga"],
        "Ada yang gratis ada yang berbayar kak! Yang gratis langsung cek di bio. Yang berbayar cuma 75rb — worth it banget! 🎁"
    ),

    # HOW TO BUY
    (
        [r"cara beli", r"gimana beli", r"order", r"pesan", r"purchase", r"beli dimana", r"beli nya"],
        "Gampang kak! Klik link di bio → pilih produk → checkout. Proses 2 menit, langsung bisa dipake! 🔥"
    ),
    (
        [r"cara daftar", r"register", r"sign up", r"gabung", r"join"],
        "Kak tinggal klik link di bio → daftar → langsung aktif! Gampang banget, ga pake ribet 😊"
    ),

    # PAYMENT METHOD
    (
        [r"transfer", r"bayar", r"payment", r"metode bayar", r"gopay", r"ovo", r"dana", r"bca", r"mandiri"],
        "Bisa bayar via transfer bank, GoPay, OVO, Dana, dan kartu kredit kak! Semua ada di checkout 💳"
    ),

    # PRODUCT SPECIFIC — JobMagnet
    (
        [r"jobmagnet", r"job magnet", r"cari kerja", r"dapet kerja", r"loker", r"lamaran", r"cv ai"],
        "JobMagnet AI kak! Bantu kamu dapet kerja lebih cepet pakai AI — dari nulis CV, cover letter, sampai prep interview 🔥 IDR 75rb di link bio!"
    ),

    # PRODUCT SPECIFIC — Affiliate TikTok
    (
        [r"affiliate tiktok", r"kelas tiktok", r"belajar tiktok", r"tiktok shop affiliate"],
        "Kelas Affiliate TikTok kak! Belajar hasilin uang dari TikTok Shop affiliate. Lengkap dari nol sampai cuan! 💰 1 juta aja. Cek link di bio"
    ),

    # PRODUCT SPECIFIC — Food/Kuliner
    (
        [r"kuliner", r"makanan", r"restoran", r"menu", r"fnb", r"food"],
        "Ada 2 produk kuliner kak! Food Menu AI Studio (desain menu AI) dan Mesin Cetak Bisnis Kuliner (scale bisnis FnB). Keduanya cuma 75rb! 🍜 Link di bio"
    ),

    # WHAT IS THIS / GENERAL
    (
        [r"apa ini", r"apaan ini", r"ini apa", r"produk apa", r"jualan apa"],
        "Ini tools AI kak! Buat bantu bisnis, kerja, konten, dan banyak lagi. Semua harganya cuma 75rb — cek link di bio! 🤖🔥"
    ),

    # LEGIT / TRUST
    (
        [r"aman ga", r"terpercaya", r"legit", r"trusted", r"penipuan ga", r"scam ga", r"bisa dipercaya"],
        "Aman kak! Pembelian via LYNK.id yang terjamin keamanannya. Ribuan pembeli udah coba dan puas 🙏 Cek review di profil ya!"
    ),

    # REFUND
    (
        [r"refund", r"kembalikan", r"garansi", r"warranty", r"jaminan"],
        "Ada garansi kepuasan kak! Kalau gak puas, hubungi kami langsung. Tapi rata-rata pelanggan senang banget sama hasilnya 😊"
    ),

    # HOW TO USE / TUTORIAL
    (
        [r"cara pakai", r"tutorial", r"cara penggunaan", r"panduan", r"guide", r"gimana cara"],
        "Gampang banget kak! Setelah beli, langsung dapat panduan lengkap + video tutorial. No skill required! 🎓 Cek link di bio"
    ),

    # DISCOUNT
    (
        [r"diskon", r"promo", r"voucher", r"kode promo", r"coupon", r"potongan harga"],
        "Lagi ada promo spesial kak! Harga udah diskon di link bio. Jangan sampai kehabisan ya — terbatas! 🎁🔥"
    ),

    # RESELLER / AFFILIATE
    (
        [r"reseller", r"jual lagi", r"affiliate", r"komisi", r"referral"],
        "Bisa jadi affiliate kak dan dapet komisi! DM aku buat info program affiliatenya 😊🔥"
    ),

    # CONTACT
    (
        [r"contact", r"hubungi", r"wa", r"whatsapp", r"telegram", r"dm"],
        "DM aku langsung kak! Atau cek link di bio buat kontak lengkapnya. Respon cepat! 😊"
    ),

    # ALREADY HAVE / ALREADY BOUGHT
    (
        [r"udah beli", r"udah punya", r"udah coba", r"sudah beli"],
        "Mantap kak udah punya! Semoga bermanfaat ya 🔥 Kalo ada pertanyaan teknis, DM aku langsung"
    ),
]


def find_faq_response(comment_text: str) -> Optional[str]:
    """
    Check if comment matches any FAQ pattern.
    Returns pre-built response string or None if no match.
    """
    text = comment_text.lower().strip()

    for patterns, response in FAQ_DATABASE:
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return response

    return None


def get_all_faqs() -> list:
    """Return all FAQ entries as list of dicts (for documentation)."""
    result = []
    for patterns, response in FAQ_DATABASE:
        result.append({
            "triggers": patterns,
            "response": response,
        })
    return result


if __name__ == "__main__":
    test_comments = [
        "Kak harganya berapa?",
        "Bisa refund ga?",
        "Cara belinya gimana?",
        "Ini scam ga?",
        "Ada promo ga kak?",
        "Saya mau jadi reseller bisa?",
        "Produk ini untuk apa ya?",
        "Udah beli nih, mantap!",
        "Random comment yang ga ada di FAQ",
    ]

    print("=== FAQ Responder Test ===\n")
    for comment in test_comments:
        response = find_faq_response(comment)
        status = "✅ MATCH" if response else "❌ no match"
        print(f"{status} | '{comment}'")
        if response:
            print(f"         → {response[:80]}...")
        print()
