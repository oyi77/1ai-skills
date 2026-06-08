"""
Module 3: QualityGate — content text quality checks before posting.
Single Responsibility: text analysis only. No caption gen, no scheduling.
Open/Closed: add rules via config["quality_gates"] — no code changes needed.

NOTE: content/content-generator/scripts/quality_gate.py is an IMAGE approval
gate for Telegram bot flows (different domain). This module checks post TEXT.

Platform limits sourced from config["platforms"] — zero hardcoded char limits.
Brand safety terms configurable via config["quality_gates"]["blocked_terms"].
"""

import sys

sys.path.insert(0, "/home/openclaw/.openclaw/workspace")

import re
from dataclasses import dataclass, field

try:
    from .base import BaseModule
except ImportError:
    from base import BaseModule  # standalone


@dataclass
class QualityReport:
    approved: bool
    score: float  # 0–100 engagement potential
    reasons: list[str] = field(default_factory=list)  # blocking failures
    warnings: list[str] = field(default_factory=list)  # non-blocking notices
    checks: dict = field(default_factory=dict)


_DEFAULT_BLOCKED: list[str] = [
    # Politically sensitive (Indonesian context)
    "PKI",
    "komunis",
    "radikal",
    "jihad",
    # Adult / offensive
    "porn",
    "bokep",
    "sex",
    "ngentot",
    "kontol",
    "memek",
    # Scam signals
    "MLM",
    "money game",
    "skema ponzi",
]

_SCORE_WEIGHTS: dict[str, int] = {
    "hook_strength": 25,
    "emoji_presence": 15,
    "question": 15,
    "cta_clarity": 20,
    "urgency": 15,
    "social_proof": 10,
}

_HOOK_WORDS = [
    "GRATIS",
    "FREE",
    "RAHASIA",
    "TERBUKTI",
    "VIRAL",
    "STOP",
    "JANGAN",
    "FAKTA",
    "PENTING",
    "BOCORAN",
]

_URGENCY_TERMS = [
    "sekarang",
    "hari ini",
    "terbatas",
    "habis",
    "last",
    "deadline",
    "segera",
    "jangan sampai",
    "buruan",
]

_CTA_PATTERNS = [
    r"link (di bio|bio)",
    r"klik (link|di bio|sekarang)",
    r"(daftar|beli|coba|download|grab|ambil) (sekarang|gratis|disini|di sini)",
    r"👉",
    r"🔗",
    r"lynk\.id",
    r"bit\.ly",
    r"https?://",
]


class QualityGate(BaseModule):
    """Check content text before it enters the posting queue."""

    def __init__(self, config: dict):
        super().__init__(config)
        gate_cfg = config.get("quality_gates", {})
        # min_engagement stored as 0–10 in config; we work 0–100 internally
        self._min_score: float = (
            gate_cfg.get("min_engagement_prediction_score", 6.0) * 10
        )
        self._require_cta: bool = gate_cfg.get("required_call_to_action", True)
        self._require_hashtags: bool = gate_cfg.get("required_hashtags", True)
        self._min_len: int = gate_cfg.get("min_caption_length", 50)
        self._blocked: list[str] = gate_cfg.get("blocked_terms", _DEFAULT_BLOCKED)

    # ── Main entry point ──────────────────────────────────────────────────

    def check_content(self, text: str, platform: str = "tiktok") -> QualityReport:
        """Run all checks. Returns QualityReport with approve/reject verdict."""
        reasons: list[str] = []
        warnings: list[str] = []
        checks: dict = {}

        # Hard block: brand safety (instant reject, no score)
        safe, hits = self.check_brand_safety(text)
        checks["brand_safety"] = {"pass": safe, "hits": hits}
        if not safe:
            return QualityReport(
                approved=False,
                score=0.0,
                reasons=[f"Brand safety violation: {', '.join(hits)}"],
                checks=checks,
            )

        # Length
        length_ok, length_msg = self.check_length(text, platform)
        checks["length"] = {"pass": length_ok, "detail": length_msg}
        if not length_ok:
            reasons.append(length_msg)

        # Hashtags
        ht_ok, ht_msg = self.check_hashtags(text, platform)
        checks["hashtags"] = {"pass": ht_ok, "detail": ht_msg}
        if not ht_ok:
            (reasons if self._require_hashtags else warnings).append(ht_msg)

        # CTA
        cta_ok, cta_msg = self.check_cta(text)
        checks["cta"] = {"pass": cta_ok, "detail": cta_msg}
        if not cta_ok:
            (reasons if self._require_cta else warnings).append(cta_msg)

        # Link
        link_ok, link_msg = self.check_link(text)
        checks["link"] = {"pass": link_ok, "detail": link_msg}
        if not link_ok:
            warnings.append(link_msg)

        # Engagement score
        score = self.score_engagement_potential(text)
        checks["engagement_score"] = score
        if score < self._min_score:
            reasons.append(
                f"Engagement score {score:.0f}/100 below threshold ({self._min_score:.0f})"
            )

        return QualityReport(
            approved=len(reasons) == 0,
            score=score,
            reasons=reasons,
            warnings=warnings,
            checks=checks,
        )

    # ── Individual checks (also callable standalone) ──────────────────────

    def check_brand_safety(self, text: str) -> tuple[bool, list[str]]:
        """Flag blocked terms. Returns (is_safe, matched_terms)."""
        hits = [t for t in self._blocked if t.lower() in text.lower()]
        return len(hits) == 0, hits

    def check_length(self, text: str, platform: str) -> tuple[bool, str]:
        """Verify caption within platform limits."""
        cfg = self.platform_cfg(platform)
        limit = cfg.get("caption_max_chars", 2200)
        n = len(text)
        if n < self._min_len:
            return False, f"Too short: {n} chars (min {self._min_len})"
        if n > limit:
            return False, f"Too long: {n}/{limit} chars for {platform}"
        return True, f"{n}/{limit} chars ✓"

    def check_hashtags(self, text: str, platform: str) -> tuple[bool, str]:
        """Verify hashtag count within platform-optimal range."""
        cfg = self.platform_cfg(platform)
        optimal = cfg.get("optimal_hashtag_count", 5)
        min_ht, max_ht = max(1, optimal - 2), optimal + 3
        count = len(re.findall(r"#\w+", text))
        if count == 0:
            return False, "No hashtags found"
        if count < min_ht:
            return False, f"Too few hashtags: {count} (want {min_ht}–{max_ht})"
        if count > max_ht:
            return False, f"Too many hashtags: {count} (want {min_ht}–{max_ht})"
        return True, f"{count} hashtags ✓"

    def check_cta(self, text: str) -> tuple[bool, str]:
        """Check for a clear call-to-action."""
        for pat in _CTA_PATTERNS:
            if re.search(pat, text, re.I):
                return True, "CTA found ✓"
        return False, "No clear call-to-action found"

    def check_link(self, text: str) -> tuple[bool, str]:
        """Check for a trackable LYNK or URL."""
        if re.search(r"lynk\.id/\w+", text):
            return True, "LYNK link ✓"
        if re.search(r"https?://\S+", text):
            return True, "URL ✓"
        return False, "No trackable link"

    def score_engagement_potential(self, text: str) -> float:
        """Score 0–100. Weights defined in _SCORE_WEIGHTS."""
        total = 0.0
        first = text.split("\n")[0].strip()

        # Hook: power word or emoji in first line
        has_hook_word = any(w.upper() in first.upper() for w in _HOOK_WORDS)
        has_hook_emoji = bool(re.search(r"[^\w\s,.]", first))
        total += (
            min(1.0, (has_hook_word + 0.5 * has_hook_emoji))
            * _SCORE_WEIGHTS["hook_strength"]
        )

        # Emoji density
        total += (
            min(1.0, len(re.findall(r"[^\w\s,.]", text)) / 5)
            * _SCORE_WEIGHTS["emoji_presence"]
        )

        # Question
        total += _SCORE_WEIGHTS["question"] if "?" in text else 0

        # CTA
        total += _SCORE_WEIGHTS["cta_clarity"] if self.check_cta(text)[0] else 0

        # Urgency
        total += (
            _SCORE_WEIGHTS["urgency"]
            if any(t in text.lower() for t in _URGENCY_TERMS)
            else 0
        )

        # Social proof: number + unit
        total += (
            _SCORE_WEIGHTS["social_proof"]
            if re.search(r"\d+(K|rb|juta|%|\+)", text, re.I)
            else 0
        )

        return round(total, 1)

    def approve_or_reject(self, text: str, platform: str) -> tuple[bool, list[str]]:
        """Convenience: returns (approved, reasons)."""
        r = self.check_content(text, platform)
        return r.approved, r.reasons


# ── Self-test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    from base import load_config  # noqa (standalone)

    cfg = load_config()
    gate = QualityGate(cfg)

    GOOD = (
        "🔥 RAHASIA viral konten yang jarang orang tahu!\n\n"
        "Udah 500+ kreator pakai cara ini — hasilnya gila banget.\n\n"
        "Buruan ambil sebelum habis 👉 https://lynk.id/jendralbot/test\n\n"
        "#AI #Konten #Indonesia #TipsDigital #Bisnis"
    )
    BAD_SAFE = "Ini terbukti scam MLM terbaik! #AI #Bisnis"
    BAD_SHORT = "tes"
    BAD_NOCTA = (
        "Konten bagus nih semoga viral ya guys #AI #Indonesia #Bisnis #Tips #UMKM"
    )

    tests = [
        ("GOOD caption", GOOD, "tiktok"),
        ("BAD: brand safety", BAD_SAFE, "tiktok"),
        ("BAD: too short", BAD_SHORT, "tiktok"),
        ("BAD: no CTA", BAD_NOCTA, "instagram"),
    ]

    for label, text, platform in tests:
        r = gate.check_content(text, platform)
        status = "✅ APPROVED" if r.approved else "❌ REJECTED"
        print(f"\n[{label}] {status}  score={r.score}")
        if r.reasons:
            for reason in r.reasons:
                print(f"  ✗ {reason}")
        if r.warnings:
            for w in r.warnings:
                print(f"  ⚠ {w}")

    # Assertions
    assert gate.check_brand_safety("normal text")[0] is True
    assert gate.check_brand_safety("ini MLM")[0] is False
    assert gate.check_link("https://lynk.id/j/abc")[0] is True
    assert gate.check_link("no link")[0] is False
    ok, _ = gate.approve_or_reject(GOOD, "tiktok")
    assert ok is True

    print("\n✅ quality_gate self-test passed")
