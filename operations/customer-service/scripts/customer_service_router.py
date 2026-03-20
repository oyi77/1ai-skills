#!/usr/bin/env python3
"""Customer Service Router - auto-respond with BerkahKarya product context via OmniRoute."""
import json, sys, os, re
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"
WORKSPACE = Path(__file__).resolve().parents[3]
LOG_FILE = WORKSPACE / "logs" / "customer_service.log"

SYSTEM_PROMPT = """Kamu adalah customer service BerkahKarya yang ramah dan profesional.

Konteks Produk:
- Brand: BerkahKarya (berkahkarya.com)
- Produk utama: JENDRALBOT — bot trading otomatis
- Harga: IDR 49.000 - 89.000 (tergantung paket)
- Pembayaran: Transfer bank, QRIS, e-wallet
- WhatsApp: +62881080269682
- Support: 24/7 via WhatsApp dan Telegram

Panduan:
- Jawab dalam Bahasa Indonesia yang ramah
- Jika tidak yakin, arahkan ke WhatsApp untuk bantuan lebih lanjut
- Jangan berikan informasi yang tidak akurat
- Selalu tawarkan bantuan lebih lanjut di akhir jawaban
"""

UNCERTAINTY_PHRASES = [
    "saya tidak yakin", "mungkin", "sepertinya", "saya kurang tahu",
    "belum bisa dipastikan", "i'm not sure", "maybe", "perhaps",
    "saya perlu cek", "hubungi langsung",
]


def auto_respond(question):
    """Generate auto-response using OmniRoute LLM with product context."""
    payload = json.dumps({
        "model": OMNIROUTE_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "temperature": 0.5,
        "max_tokens": 512,
    }).encode()

    req = Request(
        f"{OMNIROUTE_BASE}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OMNIROUTE_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Maaf, sistem sedang mengalami gangguan. Silakan hubungi kami di WhatsApp: +62881080269682\n(Error: {e})"


def confidence_score(response):
    """Check if response contains uncertainty phrases. Returns (score, flagged)."""
    response_lower = response.lower()
    matches = [p for p in UNCERTAINTY_PHRASES if p in response_lower]
    if matches:
        score = max(0.0, 1.0 - (len(matches) * 0.2))
        return score, True, matches
    return 1.0, False, []


def log_interaction(question, response, score, flagged):
    """Log the interaction to customer_service.log."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "response_preview": response[:200],
        "confidence": score,
        "flagged": flagged,
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="BerkahKarya Customer Service Router")
    parser.add_argument("question", nargs="?", help="Customer question")
    args = parser.parse_args()

    if not args.question:
        print("Usage: python customer_service_router.py \"berapa harga produknya?\"")
        sys.exit(1)

    print(f"[CS] Processing: {args.question}\n")
    response = auto_respond(args.question)
    score, flagged, matches = confidence_score(response)

    print(response)
    print(f"\n---\n[Confidence: {score:.1f}]", end="")
    if flagged:
        print(f" ⚠ FLAGGED — uncertainty detected: {matches}")
    else:
        print(" ✓ High confidence")

    log_interaction(args.question, response, score, flagged)
