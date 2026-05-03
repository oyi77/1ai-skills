#!/usr/bin/env python3
"""TikTok Viral Predictor — scores caption/topic viral potential (0-100)."""

import argparse
import json
import re
import sys

from duckduckgo_search import DDGS
from openai import OpenAI

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOOK_PATTERNS = [
    r"^stop\b",
    r"^wait\b",
    r"^did you know\b",
    r"^you won't believe\b",
    r"^nobody talks about\b",
    r"^here'?s why\b",
    r"^this is why\b",
    r"^don'?t\b",
    r"^warning\b",
    r"^breaking\b",
    r"^unpopular opinion\b",
    r"^the truth about\b",
    r"^secret\b",
    r"^imagine\b",
    r"^what if\b",
    r"^pov\b",
]

EMOTIONAL_TRIGGERS = [
    "amazing", "shocking", "insane", "unbelievable", "mind-blowing",
    "secret", "hack", "mistake", "never", "always", "worst", "best",
    "free", "easy", "fast", "truth", "exposed", "finally", "obsessed",
    "game-changer", "life-changing", "crazy", "no way", "literally",
]

CTA_PATTERNS = [
    r"follow for",
    r"save this",
    r"share with",
    r"comment\b",
    r"tag someone",
    r"link in bio",
    r"check (it )?out",
    r"let me know",
    r"drop a",
    r"try (this|it)",
]

TRENDING_HASHTAGS = ["#fyp", "#foryou", "#viral", "#trending", "#foryoupage"]

# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------


def analyze_hook_strength(text: str) -> tuple[int, list[str]]:
    """Return a score (0-30) and list of reasons based on the first few words."""
    if not text:
        return 0, []

    lower = text.lower().strip()
    score = 0
    reasons: list[str] = []

    for pattern in HOOK_PATTERNS:
        if re.search(pattern, lower):
            score += 15
            reasons.append("Strong hook pattern detected")
            break

    # Exclamation in first sentence boosts urgency
    first_sentence = text.split(".")[0]
    if "!" in first_sentence:
        score += 5
        reasons.append("Urgency/excitement in opening")

    # Short punchy opener (first 3 words <= 12 chars total) reads well on-screen
    first_words = text.split()[:3]
    if len(" ".join(first_words)) <= 12:
        score += 5
        reasons.append("Short punchy hook")

    # Emojis in hook area
    if any(ord(c) > 0x1F000 for c in first_sentence):
        score += 5
        reasons.append("Emoji in hook grabs attention")

    return min(score, 30), reasons


def analyze_engagement_patterns(text: str) -> tuple[int, list[str]]:
    """Return a score (0-25) and reasons for engagement signals."""
    if not text:
        return 0, []

    lower = text.lower()
    score = 0
    reasons: list[str] = []

    # Question marks invite comments
    if "?" in text:
        score += 8
        reasons.append("Question encourages comments")

    # CTAs
    for pattern in CTA_PATTERNS:
        if re.search(pattern, lower):
            score += 7
            reasons.append("Call-to-action detected")
            break

    # Emotional triggers
    triggers_found = [t for t in EMOTIONAL_TRIGGERS if t in lower]
    if triggers_found:
        bonus = min(len(triggers_found) * 3, 10)
        score += bonus
        reasons.append(f"Emotional triggers: {', '.join(triggers_found[:3])}")

    return min(score, 25), reasons


def check_hashtag_relevance(topic: str) -> tuple[int, list[str], list[str]]:
    """Use DuckDuckGo to gauge topic trendiness. Returns (score, reasons, hashtags)."""
    score = 0
    reasons: list[str] = []
    recommended: list[str] = list(TRENDING_HASHTAGS)

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"TikTok trending {topic}", max_results=5))

        if results:
            score += 10
            reasons.append("Topic appears in recent search results")

            # Mine hashtag ideas from result snippets
            for r in results:
                body = (r.get("body") or "") + " " + (r.get("title") or "")
                tags = re.findall(r"#\w+", body)
                for tag in tags:
                    if tag.lower() not in [h.lower() for h in recommended]:
                        recommended.append(tag)

            if len(results) >= 4:
                score += 5
                reasons.append("High search volume for topic")
        else:
            reasons.append("Low search volume — niche topic")

    except Exception as exc:
        reasons.append(f"Hashtag search unavailable: {exc}")

    # Build topic-derived hashtags
    words = re.findall(r"\w+", topic.lower())
    for w in words:
        if len(w) > 3:
            candidate = f"#{w}"
            if candidate not in [h.lower() for h in recommended]:
                recommended.append(candidate)

    return min(score, 15), reasons, recommended[:8]


def llm_score(topic: str, caption: str) -> tuple[int, list[str], list[str]]:
    """Ask OmniRoute LLM to evaluate viral potential. Returns (score, reasons, hooks)."""
    prompt = (
        "You are a TikTok viral content analyst. "
        "Given the following topic and caption, respond ONLY with valid JSON "
        "(no markdown fences) containing:\n"
        '  "score": <int 0-30>,\n'
        '  "reasons": [<str>, ...],\n'
        '  "suggested_hooks": [<str>, ...]\n\n'
        f"Topic: {topic}\n"
        f"Caption: {caption}\n"
    )

    try:
        client = OpenAI(base_url="http://localhost:20128/v1", api_key="omniroute")
        resp = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=512,
        )
        raw = resp.choices[0].message.content.strip()
        # Strip markdown fences if present
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
        data = json.loads(raw)
        return (
            min(int(data.get("score", 15)), 30),
            data.get("reasons", []),
            data.get("suggested_hooks", []),
        )
    except Exception as exc:
        return 15, [f"LLM scoring unavailable ({exc}), using default"], [
            "Did you know...",
            "Stop scrolling if...",
            "Nobody talks about this...",
        ]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def predict(topic: str, caption: str) -> dict:
    """Run all analyses and return the final prediction dict."""
    combined_text = f"{caption} {topic}".strip()

    hook_score, hook_reasons = analyze_hook_strength(caption or topic)
    engage_score, engage_reasons = analyze_engagement_patterns(combined_text)
    hashtag_score, hashtag_reasons, hashtags = check_hashtag_relevance(topic)
    lm_score, lm_reasons, suggested_hooks = llm_score(topic, caption)

    total = hook_score + engage_score + hashtag_score + lm_score
    total = max(0, min(total, 100))

    all_reasons = hook_reasons + engage_reasons + hashtag_reasons + lm_reasons
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_reasons: list[str] = []
    for r in all_reasons:
        if r not in seen:
            seen.add(r)
            unique_reasons.append(r)

    if not suggested_hooks:
        suggested_hooks = [
            "Did you know...",
            "Stop scrolling if...",
            "Nobody talks about this...",
        ]

    return {
        "score": total,
        "reasons": unique_reasons,
        "suggested_hooks": suggested_hooks[:5],
        "recommended_hashtags": hashtags,
        "posting_time": "6-9 PM local time",
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Predict TikTok viral potential for a topic/caption."
    )
    parser.add_argument("--topic", required=True, help="Content topic or niche")
    parser.add_argument("--caption", default="", help="Draft caption text")
    args = parser.parse_args()

    result = predict(args.topic, args.caption)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
