#!/usr/bin/env python3
"""hook_lab.py — offline heuristic check for short-form opening lines.

Not a view predictor. Scores five text-only properties: length, concrete
markers, stakes, front-loading, and explicit audience address. Abstains on
unclassifiable patterns instead of guessing. No network, no uploads.

Usage:
  python3 hook_lab.py hooks.txt                 # one hook per line, ranked
  python3 hook_lab.py --hook "I lost $18,000..."
  python3 hook_lab.py hooks.txt --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[A-Za-z0-9$%'’-]+")
MONEY_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?|\b\d[\d,.]*\s?(?:%|k\b|x\b|hrs?\b|hours?\b|mins?\b|days?\b|weeks?\b|months?\b|years?\b)?")
PROPER_RE = re.compile(r"(?<!^)\b[A-Z][a-z]{2,}\b")
SPOKEN_NUMBERS = {"zero", "two", "three", "four", "five", "six", "seven", "eight",
                  "nine", "ten", "eleven", "twelve", "twenty", "thirty", "fifty",
                  "hundred", "thousand", "million", "billion", "dozen", "half"}
MONEY_WORDS = {"dollars", "grand", "bucks", "euros", "pounds", "rupiah"}
GREETING_RE = re.compile(r"^(hey|hi|hello|good (morning|evening|afternoon))\b", re.I)
PREAMBLE_RE = re.compile(r"^(today|so|in this video|in today's|let's talk|i wanted to)\b", re.I)
ASK_ATTENTION_RE = re.compile(r"^(stop scrolling|wait before you|listen up|pay attention)\b", re.I)
STAKE_RE = re.compile(r"\b(lost|cost|cost me|wasted|saved|made|earned|failed|risk|mistake|wrong|never|regret|before|after)\b", re.I)
AUDIENCE_RE = re.compile(r"\b(you|your|you're|nobody|everybody|most people|we)\b", re.I)


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def concrete(text: str) -> int:
    w = [x.lower() for x in words(text)]
    return len(MONEY_RE.findall(text)) + len(set(PROPER_RE.findall(text))) + sum(
        1 for x in w if x in SPOKEN_NUMBERS or x in MONEY_WORDS
    )


def score(text: str) -> dict:
    """Return five 0-100 checks + overall. Abstain flag when signals conflict."""
    w = words(text)
    if not w:
        return {"length": 0, "concrete": 0, "stakes": 0, "frontload": 0,
                "address": 0, "overall": 0, "verdict": "EMPTY", "abstain": True}
    n = len(w)
    length = max(0.0, min(100.0, 100 - max(0, n - 12) * 8))
    conc = min(100.0, concrete(text) * 45)
    stakes = 100.0 if STAKE_RE.search(text) else 30.0
    # A greeting/preamble or an attention demand is a dealbreaker regardless of
    # other signals: score it WEAK even if it happens to mention a number.
    dealbreaker = bool(GREETING_RE.search(text) or PREAMBLE_RE.search(text) or ASK_ATTENTION_RE.search(text))
    front = 0.0 if dealbreaker else (100.0 if conc or STAKE_RE.search(text) else 55.0)
    address = 100.0 if AUDIENCE_RE.search(text) else 45.0
    checks = {"length": round(length, 1), "concrete": round(conc, 1),
              "stakes": stakes, "frontload": front, "address": address}
    overall = round(sum(checks.values()) / 5, 1)
    # Abstain only suppresses a positive claim. Bad hooks still get labelled WEAK.
    if dealbreaker or overall < 45:
        verdict = "WEAK"
    elif (n > 20 or conc == 0) and overall >= 45:
        verdict = "ABSTAIN"
    else:
        verdict = "STRONG" if overall >= 70 else "OK"
    return {**checks, "overall": overall, "verdict": verdict,
            "abstain": verdict == "ABSTAIN"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", nargs="?", help="file with one hook per line, or '-' for stdin")
    ap.add_argument("--hook", help="score a single hook")
    ap.add_argument("--json", action="store_true", help="JSON output")
    args = ap.parse_args()
    if args.hook:
        hooks = [args.hook]
    elif args.path:
        raw = sys.stdin.read() if args.path == "-" else open(args.path, encoding="utf-8").read()
        hooks = [line.strip() for line in raw.splitlines() if line.strip() and not line.startswith("#")]
    else:
        ap.error("provide a path or --hook")
    results = [{"hook": h, **score(h)} for h in hooks]
    results.sort(key=lambda r: -r["overall"])
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("HOOK LAB (text-only heuristics; not a view predictor)")
        for r in results:
            weakest = min(("length", "concrete", "stakes", "frontload", "address"), key=lambda k: r[k])
            print(f"{r['overall']:5.1f} {r['verdict']:7s} {r['hook'][:58]}")
            print(f"         weakest: {weakest.upper()} ({r[weakest]})")
        if any(r["verdict"] == "ABSTAIN" for r in results):
            print("ABSTAIN: too long or no concrete marker; rewrite or trust real retention data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
