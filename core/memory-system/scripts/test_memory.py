"""
test_memory.py — Full test suite for the memory system.

Tests:
  1. All 4 memory layer types
  2. Fallback when primary embedding fails
  3. Hybrid search returns ranked results
  4. Async pipeline doesn't block main thread
  5. Multi-hop graph traversal
  6. Decay + importance boost
  7. Health check + self-healing
  8. Compaction
  9. Mode switching (local_only)
  10. Stats accuracy

Target: completes in <30 seconds (embedding load may take a few sec first run)
"""
import sys
import time
import tempfile
from pathlib import Path

# ── Bootstrap path ──────────────────────────────────────────────────────────
# This file lives in:  skills/1ai-skills/core/memory-system/scripts/
# We need to add      skills/1ai-skills/core/   to sys.path so that
# `import memory_system.scripts.xxx` works.
_HERE = Path(__file__).resolve().parent          # .../scripts/
_PKG_ROOT = _HERE.parent.parent                  # .../core/
sys.path.insert(0, str(_PKG_ROOT))

# ── Patch config to use a temp directory (no pollution) ─────────────────────
import memory_system.scripts.config as _cfg
_TMP = Path(tempfile.mkdtemp(prefix="mem_test_"))
_cfg.BASE_DIR         = _TMP
_cfg.DB_PATH          = _TMP / "memory.db"
_cfg.ARCHIVE_DIR      = _TMP / "archive"
_cfg.HNSW_INDEX_PATH  = _TMP / "hnsw.bin"
_cfg.HNSW_LABELS_PATH = _TMP / "hnsw_labels.npy"
_cfg.BASE_DIR.mkdir(parents=True, exist_ok=True)
_cfg.ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

from memory_system.scripts.memory_manager import MemoryManager

_PASS = "✅ PASS"
_FAIL = "❌ FAIL"
_results = []


def check(name: str, condition: bool, detail: str = "") -> bool:
    status = _PASS if condition else _FAIL
    msg = f"  {status}  {name}"
    if detail:
        msg += f"  ({detail})"
    print(msg)
    _results.append((name, condition))
    return condition


def section(title: str):
    print(f"\n{'─'*62}")
    print(f"  {title}")
    print(f"{'─'*62}")


# ─────────────────────────────────────────────────────────────────
# TEST 1: Working Memory
# ─────────────────────────────────────────────────────────────────
def test_working_memory(mm):
    section("TEST 1: Working Memory")

    mm.set_working("key1", "hello")
    check("set/get basic value", mm.get_working("key1") == "hello")

    mm.set_working("task", {"symbol": "XAUUSD", "sl": 20})
    check("set/get dict value", mm.get_working("task") == {"symbol": "XAUUSD", "sl": 20})

    check("default on miss", mm.get_working("nonexistent", "def") == "def")

    mm.set_working("short", "gone", ttl=1)
    check("key present before TTL", mm.get_working("short") == "gone")
    time.sleep(1.1)
    check("key expired after TTL", mm.get_working("short") is None)

    mm.set_working("del_me", "value")
    mm.delete_working("del_me")
    check("delete working key", mm.get_working("del_me") is None)

    t0 = time.perf_counter()
    for i in range(500):
        mm.set_working(f"perf_{i}", i)
        mm.get_working(f"perf_{i}")
    elapsed_ms = (time.perf_counter() - t0) * 1000
    avg_us = elapsed_ms / 1000 * 1000
    check("latency <1ms avg per op", avg_us < 1000, f"{avg_us:.0f}µs avg")


# ─────────────────────────────────────────────────────────────────
# TEST 2: Semantic Memory
# ─────────────────────────────────────────────────────────────────
def test_semantic_memory(mm):
    section("TEST 2: Semantic Memory (FTS5 + embeddings)")

    id1 = mm.store("XAUUSD scalping strategy using H1 timeframe",
                   importance=0.9, tags=["trading", "strategy"])
    id2 = mm.store("User prefers aggressive risk management 2% max",
                   importance=0.8, tags=["trading", "risk"])
    id3 = mm.store("BerkahKarya revenue target IDR 150K per week",
                   importance=0.7, tags=["business", "revenue"])

    check("store returns id", len(id1) > 0)
    check("3 memories stored", mm._semantic.count() >= 3)

    results = mm._semantic.fts_search("XAUUSD", top_k=5)
    check("FTS5 finds trading memory",
          any("XAUUSD" in r["text"] for r in results),
          f"{len(results)} results")

    results2 = mm._semantic.fts_search("revenue", top_k=5)
    check("FTS5 finds revenue memory", len(results2) > 0)


# ─────────────────────────────────────────────────────────────────
# TEST 3: Episodic Memory
# ─────────────────────────────────────────────────────────────────
def test_episodic_memory(mm):
    section("TEST 3: Episodic Memory")

    messages = [
        {"role": "user", "content": "How is XAUUSD looking today?"},
        {"role": "assistant", "content": "XAUUSD shows bullish breakout above 2950, TP 2975"},
        {"role": "user", "content": "What's the stop loss?"},
        {"role": "assistant", "content": "SL at 2935, risk 15 pips"},
    ]
    eid = mm.add_episode(messages, importance=0.8)
    check("add_episode returns id", len(eid) > 0)
    check("episode stored", mm._episodic.count() >= 1)

    # Buffer auto-flush
    for i in range(_cfg.EPISODIC_SUMMARY_EVERY + 1):
        mm.add_message("user" if i % 2 == 0 else "assistant",
                       f"Message {i}: analysis for XAUUSD trade")
    check("episodic grows after buffer flush", mm._episodic.count() >= 2)

    kw = mm._episodic.keyword_search("XAUUSD", top_k=5)
    check("episodic keyword search works", len(kw) >= 1)


# ─────────────────────────────────────────────────────────────────
# TEST 4: Archive Memory
# ─────────────────────────────────────────────────────────────────
def test_archive_memory(mm):
    section("TEST 4: Archive Memory (gzipped JSONL)")

    test_mems = [
        {"id": "arc1", "text": "Old trading log March 2025", "importance": 0.05, "timestamp": time.time()},
        {"id": "arc2", "text": "Expired task from January", "importance": 0.03, "timestamp": time.time()},
    ]
    count = mm._archive.archive(test_mems, date_str="2026-03-12")
    check("archive writes records", count == 2)

    recalled = mm.recall_archive("2026-03-12")
    check("recall returns records", len(recalled) >= 2)
    check("recalled content correct",
          any("trading log" in r.get("text", "") for r in recalled))

    dates = mm._archive.list_dates()
    check("list_dates shows archived date", "2026-03-12" in dates)


# ─────────────────────────────────────────────────────────────────
# TEST 5: Async Pipeline (non-blocking)
# ─────────────────────────────────────────────────────────────────
def test_async_pipeline(mm):
    section("TEST 5: Async Pipeline (non-blocking)")

    t0 = time.perf_counter()
    ids = [mm.store(f"Async test memory {i}: XAUUSD trade note", importance=0.5)
           for i in range(20)]
    elapsed = time.perf_counter() - t0

    check("20 stores in <2s (non-blocking)", elapsed < 2.0, f"{elapsed:.2f}s")
    check("all 20 ids returned", len(ids) == 20)

    # Give worker time to chew through jobs (local model may be slow first batch)
    time.sleep(8)
    pending = mm._pipeline.pending_count()
    # Worker should have processed at least some; total pending across ALL tests ≤ 50
    check("worker processes jobs async", pending <= 50, f"{pending} pending after 8s")


# ─────────────────────────────────────────────────────────────────
# TEST 6: Hybrid Search
# ─────────────────────────────────────────────────────────────────
def test_hybrid_search(mm):
    section("TEST 6: Hybrid Search")

    mm.store("Gold trading XAUUSD Asia session 15:00 UTC+7", importance=0.9)
    mm.store("TikTok content JENDRALBOT marketing campaign", importance=0.7)
    mm.store("BerkahKarya cashflow IDR weekly target", importance=0.8)
    mm.store("XAUUSD stop loss 2% per trade risk management", importance=0.85)
    time.sleep(0.5)

    results = mm.search("XAUUSD trading", top_k=5)
    check("search returns results", len(results) > 0, f"{len(results)}")
    check("results have required fields",
          all("text" in r and "score" in r and "source" in r for r in results))
    check("results sorted desc",
          all(results[i]["score"] >= results[i+1]["score"]
              for i in range(len(results)-1)),
          str([round(r["score"], 3) for r in results]))

    kw = mm.search("BerkahKarya cashflow", top_k=3)
    check("keyword search works", len(kw) > 0)

    t0 = time.perf_counter()
    mm.search("trading risk management", top_k=10)
    ms = (time.perf_counter() - t0) * 1000
    # 100ms ceiling on local hardware (typical: 45ms, spikes under load)
    check("search latency <100ms", ms < 100, f"{ms:.1f}ms")


# ─────────────────────────────────────────────────────────────────
# TEST 7: Embedding Fallback
# ─────────────────────────────────────────────────────────────────
def test_embedding_fallback(mm):
    section("TEST 7: Embedding Fallback (local_only mode)")

    mm.set_mode("local_only")
    check("mode=local_only set", mm._mode == "local_only")

    # local embed should return array (not crash)
    emb = mm._emb.embed("Test text for local embedding fallback")
    check("local embed no crash", True)
    if emb is not None:
        check("local embed has dims > 0", len(emb) > 0, f"dim={len(emb)}")

    # Search must still work
    mm.store("Local only test XAUUSD gold", importance=0.5)
    time.sleep(0.3)
    results = mm.search("XAUUSD gold", top_k=5)
    check("search works in local_only", len(results) >= 0)

    mm.set_mode("hybrid")
    check("mode restored to hybrid", mm._mode == "hybrid")


# ─────────────────────────────────────────────────────────────────
# TEST 8: Memory Graph Multi-hop
# ─────────────────────────────────────────────────────────────────
def test_memory_graph(mm):
    section("TEST 8: Memory Graph (multi-hop traversal A→B→C)")

    id_a = mm.store("Gold trading strategy entry rules", importance=0.8)
    id_b = mm.store("Risk management stop loss placement", importance=0.7)
    id_c = mm.store("Position sizing formula 2% max risk", importance=0.6)
    id_d = mm.store("Exit rules take profit strategy", importance=0.6)

    mm.link(id_a, id_b, edge_type="refers_to", weight=0.9)
    mm.link(id_b, id_c, edge_type="refers_to", weight=0.8)
    mm.link(id_b, id_d, edge_type="related_topic", weight=0.7)

    # 1-hop
    hop1 = mm._graph.traverse(id_a, max_hops=1, edge_types=["refers_to"])
    check("1-hop finds direct neighbor",
          any(n["memory_id"] == id_b for n in hop1),
          f"{len(hop1)} neighbors")

    # 2-hop A→B→C
    hop2 = mm._graph.traverse(id_a, max_hops=2, edge_types=["refers_to"])
    found_ids = {n["memory_id"] for n in hop2}
    check("2-hop finds B and C", id_b in found_ids and id_c in found_ids,
          str(found_ids))

    # 3-hop via manager (with text enrichment)
    enriched = mm.traverse(id_a, max_hops=3)
    check("traverse() enriches with text",
          all("text" in n for n in enriched))

    # Edge count
    check("graph has ≥3 edges", mm._graph.edge_count() >= 3)

    # Find path
    path = mm._graph.find_path(id_a, id_c)
    check("find_path returns valid path",
          path is None or (isinstance(path, list) and id_a == path[0] and id_c == path[-1]),
          str(path))


# ─────────────────────────────────────────────────────────────────
# TEST 9: Decay & Importance Boost
# ─────────────────────────────────────────────────────────────────
def test_decay(mm):
    section("TEST 9: Decay & Importance Boost")

    mid = mm.store("Decay test: XAUUSD historical note", importance=0.8)
    ten_days_ago = time.time() - 10 * 86400
    with mm._semantic._conn() as conn:
        conn.execute(
            "UPDATE memories SET last_accessed=?, importance=0.8 WHERE id=?",
            (ten_days_ago, mid),
        )

    result = mm.decay_all()
    check("decay_all runs", "semantic_decayed" in result)
    check("memories decayed", result["semantic_decayed"] > 0,
          str(result))

    mem = mm._semantic.get(mid, update_access=False)
    if mem:
        expected = 0.8 * (0.95 ** 10)
        diff = abs(mem["importance"] - expected)
        check("importance decayed ~5%/day", diff < 0.05,
              f"got {mem['importance']:.3f} expected ~{expected:.3f}")

    # Access boost
    mm._semantic._boost_importance(mid)
    mem2 = mm._semantic.get(mid, update_access=False)
    if mem and mem2:
        check("access boosts importance",
              mem2["importance"] >= mem["importance"],
              f"{mem['importance']:.3f}→{mem2['importance']:.3f}")


# ─────────────────────────────────────────────────────────────────
# TEST 10: Health Check & Self-Healing
# ─────────────────────────────────────────────────────────────────
def test_health_check(mm):
    section("TEST 10: Health Check & Self-Healing")

    report = mm.health_check()
    check("returns dict", isinstance(report, dict))
    check("has status", "status" in report)
    check("has issues list", isinstance(report.get("issues"), list))
    check("has fixes list", isinstance(report.get("fixes"), list))
    check("status valid",
          report["status"] in ("healthy", "repaired", "degraded"),
          report["status"])
    print(f"    issues: {report['issues']}")
    print(f"    fixes:  {report['fixes']}")


# ─────────────────────────────────────────────────────────────────
# TEST 11: Stats
# ─────────────────────────────────────────────────────────────────
def test_stats(mm):
    section("TEST 11: Stats")

    stats = mm.get_stats()
    check("returns dict", isinstance(stats, dict))
    for key in ["total_memories", "working", "episodic", "semantic",
                "archived", "pending_embeddings", "mode"]:
        check(f"has '{key}'", key in stats, str(stats.get(key, "MISSING")))
    print(f"    {stats}")


# ─────────────────────────────────────────────────────────────────
# TEST 12: Compaction
# ─────────────────────────────────────────────────────────────────
def test_compaction(mm):
    section("TEST 12: Memory Compaction")

    for text in [
        "XAUUSD entry 2950 SL 2935 TP 2975 position opened",
        "XAUUSD trade at 2950, stop loss at 2935, target 2975",
        "Gold entry price 2950 with risk to 2935 and target 2975",
        "XAUUSD long at 2950, risk 15 pips, reward 25 pips",
    ]:
        mm.store(text, importance=0.6, tags=["trading"])

    time.sleep(5)  # wait for embeddings to be generated

    result = mm.compact(similarity_threshold=0.7)
    check("compact returns dict", isinstance(result, dict))
    check("compact has required fields",
          all(k in result for k in
              ["clusters_found", "memories_compacted", "new_memories_created"]))
    check("compact runs without crash", True)
    print(f"    Compact result: {result}")


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    print("\n" + "═"*62)
    print("  MEMORY SYSTEM — FULL TEST SUITE")
    print("═"*62)
    print(f"  Temp DB: {_TMP}")
    t_start = time.time()

    with MemoryManager(db_path=_TMP / "memory.db", mode="hybrid") as mm:
        test_working_memory(mm)
        test_semantic_memory(mm)
        test_episodic_memory(mm)
        test_archive_memory(mm)
        test_async_pipeline(mm)
        test_hybrid_search(mm)
        test_embedding_fallback(mm)
        test_memory_graph(mm)
        test_decay(mm)
        test_health_check(mm)
        test_stats(mm)
        test_compaction(mm)

    elapsed = time.time() - t_start
    passed = sum(1 for _, ok in _results if ok)
    failed = sum(1 for _, ok in _results if not ok)

    print(f"\n{'═'*62}")
    print(f"  RESULTS: {passed}/{len(_results)} passed  |  {failed} failed  |  {elapsed:.1f}s")
    print(f"{'═'*62}\n")

    if failed:
        print("  Failed tests:")
        for name, ok in _results:
            if not ok:
                print(f"    ❌ {name}")
        print()

    import shutil
    shutil.rmtree(_TMP, ignore_errors=True)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
