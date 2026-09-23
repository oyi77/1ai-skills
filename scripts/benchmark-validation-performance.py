#!/usr/bin/env python3
"""Reproducible microbenchmarks for validation hot-path optimizations."""

from __future__ import annotations

import argparse
import ast
import difflib
import random
import re
import statistics
import time


THRESHOLD = 0.72
WORDS = (
    "accessibility", "authentication", "authorization", "automation",
    "cryptography", "deployment", "documentation", "observability",
    "performance", "reliability", "responsive", "validation",
)


def baseline_similarity(a: str, b: str, threshold: float = THRESHOLD) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def optimized_similarity(a: str, b: str, threshold: float = THRESHOLD) -> float:
    total_length = len(a) + len(b)
    if total_length and 2.0 * min(len(a), len(b)) < threshold * total_length:
        return 0.0
    matcher = difflib.SequenceMatcher(None, a, b)
    if matcher.quick_ratio() < threshold:
        return 0.0
    return matcher.ratio()


def baseline_syntax(blocks: list[str]) -> int:
    failures = 0
    for block in blocks:
        try:
            ast.parse(block)
        except SyntaxError:
            failures += 1
    return failures


def cached_syntax(blocks: list[str]) -> int:
    cache: dict[str, bool] = {}
    failures = 0
    for block in blocks:
        valid = cache.get(block)
        if valid is None:
            try:
                ast.parse(block)
                valid = True
            except SyntaxError:
                valid = False
            cache[block] = valid
        failures += not valid
    return failures


def baseline_todos(texts: list[str]) -> int:
    checklist = re.compile(r"^\s*-\s*\[")
    return sum(
        1
        for text in texts
        for line in text.splitlines()
        if "[TODO]" in line and not checklist.match(line)
    )


def optimized_todos(texts: list[str]) -> int:
    return sum(
        1
        for text in texts
        if "[TODO]" in text
        for line in text.splitlines()
        if "[TODO]" in line and not line.lstrip().startswith("- [")
    )


def measure(fn, *args, repeats: int) -> tuple[float, object]:
    samples = []
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(*args)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples), result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=7)
    parser.add_argument("--scale", type=int, default=1)
    args = parser.parse_args()

    rng = random.Random(20260922)
    pairs = []
    for _ in range(40_000 * args.scale):
        left = rng.choice(WORDS)
        right = rng.choice(WORDS)
        if rng.random() < 0.2:
            right = left[:-1] + rng.choice("abcdefghijklmnopqrstuvwxyz")
        pairs.append((left, right))

    syntax_templates = [
        "value = 1\nprint(value)",
        "def run(x):\n    return x * 2",
        "def broken(:\n    pass",
        "for item in range(3):\n    print(item)",
    ]
    blocks = [rng.choice(syntax_templates) for _ in range(20_000 * args.scale)]
    clean_text = "\n".join(f"ordinary documentation line {i}" for i in range(80))
    todo_text = clean_text + "\n[TODO] finish this\n- [ ] No [TODO] placeholders"
    texts = [todo_text if i % 25 == 0 else clean_text for i in range(5_000 * args.scale)]

    def all_similarity(fn):
        return [fn(a, b) for a, b in pairs]

    cases = [
        ("SequenceMatcher", lambda: all_similarity(baseline_similarity),
         lambda: all_similarity(optimized_similarity)),
        ("AST parsing", lambda: baseline_syntax(blocks), lambda: cached_syntax(blocks)),
        ("TODO scan", lambda: baseline_todos(texts), lambda: optimized_todos(texts)),
    ]

    print("benchmark,baseline_s,optimized_s,speedup")
    for name, baseline, optimized in cases:
        baseline_time, baseline_result = measure(baseline, repeats=args.repeats)
        optimized_time, optimized_result = measure(optimized, repeats=args.repeats)
        if name == "SequenceMatcher":
            equivalent = all(
                before == after or (before < THRESHOLD and after == 0.0)
                for before, after in zip(baseline_result, optimized_result)
            )
        else:
            equivalent = baseline_result == optimized_result
        if not equivalent:
            raise SystemExit(f"{name}: optimized result changed observable behavior")
        print(f"{name},{baseline_time:.6f},{optimized_time:.6f},{baseline_time / optimized_time:.2f}x")


if __name__ == "__main__":
    main()
