#!/usr/bin/env python3
"""Self-check: CachedSimilarityMatcher vs original similarity() — exact equivalence.

Run: uv run --with pyyaml==6.0.2 python3 tests/test_cached_similarity.py
"""
import importlib.util
import random
import sys as _sys
_sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent.parent / "scripts"))
import sys
from difflib import SequenceMatcher
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "lint", Path(__file__).resolve().parent.parent / "scripts" / "lint-skills.py")
ls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ls)


def reference(a: str, b: str, t: float) -> float:
    """Original similarity() semantics (pre-optimization)."""
    la, lb = len(a), len(b)
    if t > 0.0 and (la + lb) > 0 and 2.0 * min(la, lb) < t * (la + lb):
        return 0.0
    m = SequenceMatcher(None, a.lower(), b.lower())
    if t > 0.0 and m.quick_ratio() < t:
        return 0.0
    return m.ratio()


def main() -> int:
    # edge cases, including empty strings and length-asymmetry
    cases = ["", "a", "A", "abc", "acb", "aaaa", "aaab", "x" * 210, "x" * 199 + "y"]
    for a in cases:
        m = ls.CachedSimilarityMatcher(a)
        for b in cases:
            for t in (0.0, 0.5, 0.99, 1.0):
                assert m.similarity(b, threshold=t) == reference(a, b, t), (a, b, t)

    # randomized, including matcher reuse across bases (mirrors the N^2 loop)
    rng = random.Random(2024)
    alpha = "abcdefghijklmnopqrstuvwxyz-0123456789"
    for _ in range(60000):
        a = "".join(rng.choice(alpha) for _ in range(rng.randrange(0, 30)))
        b = "".join(rng.choice(alpha) for _ in range(rng.randrange(0, 30)))
        t = rng.choice((0.0, 0.5, 0.75, 0.99))
        m = ls.CachedSimilarityMatcher(b)
        for _ in range(2):  # reuse same cached target
            assert m.similarity(a, threshold=t) == reference(a, b, t), (a, b, t)

    print("OK: CachedSimilarityMatcher == similarity() on all cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
