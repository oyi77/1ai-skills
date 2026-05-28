"""
sentiment_analyzer.py — Detect comment intent/sentiment
Categories: positive, negative, question, interest, price_ask, spam, neutral
"""

import re
from dataclasses import dataclass
from typing import Optional

@dataclass
class SentimentResult:
    category: str           # positive | negative | question | interest | price_ask | spam | neutral
    confidence: float       # 0.0 – 1.0
    is_dm_trigger: bool     # Should we DM this person?
    reason: str             # Human-readable reason
    keywords_matched: list  # Which keywords fired

# ─── KEYWORD LISTS ─────────────────────────────────────────────────────────────

POSITIVE_KEYWORDS = [
    "bagus", "keren", "mantap", "mantul", "josss", "jos", "top", "oke", "ok", "sip",
    "nice", "good", "great", "amazing", "wow", "waw", "luar biasa", "kece",
    "makasih infonya", "thanks", "terima kasih", "helpful", "berguna", "bermanfaat",
    "love", "suka", "sukak", "sukaaaak", "❤️", "🔥", "👍", "💪", "😍",
]

NEGATIVE_KEYWORDS = [
    "jelek", "buruk", "gagal", "gak berguna", "tidak berguna", "sampah", "scam",
    "penipuan", "tipu", "bohong", "palsu", "fake", "rugi", "kecewa", "zonk",
    "gak worth", "tidak worth", "mahal banget", "kemahalan", "gak mutu",
    "gak jelas", "tidak jelas", "buang uang",
]

QUESTION_KEYWORDS = [
    "apa itu", "apaan", "gimana", "bagaimana", "cara", "tutorial", "bisa",
    "fungsi", "fitur", "keunggulan", "kelebihan", "buat apa", "untuk apa",
    "bedanya apa", "perbedaan", "cocok buat", "untuk siapa", "gimana caranya",
    "bagaimana cara", "apa manfaat", "apa kegunaannya", "?",
]

INTEREST_KEYWORDS = [
    "tertarik", "mau", "mau dong", "mau beli", "mau coba", "pengen", "pengin",
    "ingin", "minat", "mau info", "info dong", "info lebih", "detail",
    "daftar gimana", "cara daftar", "cara beli", "order gimana", "beli dimana",
    "link dong", "linknya", "dimana beli", "ada di mana", "jual dimana",
    "mau pesan", "pesan gimana",
]

PRICE_KEYWORDS = [
    "harga", "berapa", "berapa harga", "price", "cost", "bayar berapa",
    "harganya", "mahal gak", "murah gak", "worth it gak", "worth ga",
    "bayarnya", "biayanya", "gratis gak", "free gak", "berbayar",
]

SPAM_PATTERNS = [
    r"follow\s*(back|me|aku)",
    r"f4f",
    r"l4l",
    r"check\s*my\s*(profile|bio)",
    r"cek\s*(profil|bio)\s*(aku|saya|gw)",
    r"(kunjungi|visit)\s*(web|toko|shop)\s*(kami|saya|aku)",
    r"(promo|diskon)\s*\d+%",  # competitor spam
    r"wa\s*:\s*\d{10,}",
    r"http[s]?://(?!lynk\.id)",  # external links (not lynk)
]

NEUTRAL_GREETINGS = [
    "halo", "hai", "hi", "hello", "hei", "permisi", "selamat",
    "pagi", "siang", "malam", "sore",
]


def normalize(text: str) -> str:
    return text.lower().strip()


def count_matches(text: str, keywords: list) -> list:
    matched = []
    for kw in keywords:
        if kw in text:
            matched.append(kw)
    return matched


def is_spam(text: str) -> bool:
    for pattern in SPAM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def analyze_sentiment(comment_text: str) -> SentimentResult:
    """
    Analyze comment text and return structured sentiment result.
    Priority: spam > price_ask > interest > question > positive > negative > neutral
    """
    text = normalize(comment_text)

    # 1. Spam check
    if is_spam(text):
        return SentimentResult(
            category="spam",
            confidence=0.9,
            is_dm_trigger=False,
            reason="Spam patterns detected",
            keywords_matched=[],
        )

    # 2. Price question (high-intent — buyer signal!)
    price_matches = count_matches(text, PRICE_KEYWORDS)
    if price_matches:
        return SentimentResult(
            category="price_ask",
            confidence=min(0.6 + 0.1 * len(price_matches), 0.95),
            is_dm_trigger=True,
            reason="Asking about price — buyer signal",
            keywords_matched=price_matches,
        )

    # 3. Interest / purchase intent (highest DM priority)
    interest_matches = count_matches(text, INTEREST_KEYWORDS)
    if interest_matches:
        return SentimentResult(
            category="interest",
            confidence=min(0.6 + 0.1 * len(interest_matches), 0.95),
            is_dm_trigger=True,
            reason="Showing purchase interest",
            keywords_matched=interest_matches,
        )

    # 4. Question
    question_matches = count_matches(text, QUESTION_KEYWORDS)
    if question_matches:
        return SentimentResult(
            category="question",
            confidence=min(0.5 + 0.1 * len(question_matches), 0.90),
            is_dm_trigger=len(question_matches) >= 2,
            reason="Asking a question about product",
            keywords_matched=question_matches,
        )

    # 5. Positive
    positive_matches = count_matches(text, POSITIVE_KEYWORDS)
    if positive_matches:
        return SentimentResult(
            category="positive",
            confidence=min(0.5 + 0.08 * len(positive_matches), 0.90),
            is_dm_trigger=False,
            reason="Positive sentiment",
            keywords_matched=positive_matches,
        )

    # 6. Negative
    negative_matches = count_matches(text, NEGATIVE_KEYWORDS)
    if negative_matches:
        return SentimentResult(
            category="negative",
            confidence=min(0.5 + 0.1 * len(negative_matches), 0.90),
            is_dm_trigger=False,
            reason="Negative sentiment",
            keywords_matched=negative_matches,
        )

    # 7. Neutral
    return SentimentResult(
        category="neutral",
        confidence=0.5,
        is_dm_trigger=False,
        reason="No strong signals detected",
        keywords_matched=[],
    )


if __name__ == "__main__":
    tests = [
        "Kak harganya berapa?",
        "Mau dong, gimana cara belinya?",
        "Bagus banget kontennya!",
        "Produk sampah, scam!",
        "Ini bisa buat apa ya?",
        "Halo kak",
        "Follow back dong hehe",
        "Pengen coba, ada diskon ga?",
    ]
    for t in tests:
        result = analyze_sentiment(t)
        print(f"[{result.category:12s}] {result.confidence:.2f} dm={result.is_dm_trigger} | '{t}'")
