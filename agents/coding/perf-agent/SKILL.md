---
name: perf-agent
description: Use when measure before optimizing, target actual bottlenecks proven by profiling, verify with benchmarks.
domain: agents
tags:
  - agent
  - ai-agent
  - automation
  - perf
  - coding
version: 1.0.0
---

# Perf Agent

Quick Reference — see parent for full agent ecosystem.

The Perf Agent identifies and fixes performance bottlenecks using systematic profiling, benchmarking, and capacity analysis. Its first principle is measure before optimize — it never guesses at bottlenecks. It profiles CPU, memory, I/O, and network; identifies root causes (N+1 queries, memory leaks, unnecessary allocations, sync I/O); and validates every optimization with before/after benchmarks. The perf agent also projects cost impact so teams prioritize by ROI.

## Key Responsibilities

- **Profile before optimize**: Use profilers (py-spy, cProfile, valgrind, lighthouse, k6) to identify actual bottlenecks, not perceived ones
- **Root cause analysis**: Trace slow endpoints, memory growth, or high CPU to specific code paths, queries, or resource contention
- **Validate with benchmarks**: Every optimization must include a before/after benchmark — no improvement claim without a measurement

## Code Example

```python
"""Minimal perf agent pattern — profile and optimize."""

import json, sys, time, statistics
from pathlib import Path

def profile_endpoint(endpoint: str, samples: int = 100) -> dict:
    """Simple latency profiling for a given operation."""
    import requests  # simulated dependency

    latencies = []
    for _ in range(samples):
        start = time.perf_counter()
        # In practice: call the actual endpoint
        time.sleep(0.01)  # simulated work
        latencies.append((time.perf_counter() - start) * 1000)

    p50 = statistics.median(latencies)
    p95 = sorted(latencies)[int(samples * 0.95)]
    p99 = sorted(latencies)[int(samples * 0.99)]

    return {
        "endpoint": endpoint,
        "samples": samples,
        "p50_ms": round(p50, 1),
        "p95_ms": round(p95, 1),
        "p99_ms": round(p99, 1),
        "assessment": "healthy" if p95 < 200 else "needs_attention" if p95 < 500 else "critical"
    }

def suggest_optimizations(profile: dict) -> list[dict]:
    """Suggest fixes based on profile data."""
    suggestions = []
    if profile["p95_ms"] > 500:
        suggestions.append({
            "type": "N+1 query",
            "confidence": "medium",
            "fix": "Enable eager loading on the relation",
            "impact": "Expected 40-60% p95 reduction"
        })
    if profile["p99_ms"] > 1000:
        suggestions.append({
            "type": "Cache miss",
            "confidence": "low",
            "fix": "Add Redis caching layer with 60s TTL",
            "impact": "Expected 70-90% p99 reduction for cache hits"
        })
    return suggestions

if __name__ == "__main__":
    endpoint = sys.argv[1]
    profile = profile_endpoint(endpoint)
    profile["optimizations"] = suggest_optimizations(profile)
    print(json.dumps(profile, indent=2))
```

## Checklist

- [ ] Profiler confirmed the bottleneck before any optimization code was written
- [ ] Before/after benchmarks recorded with the same methodology (sample size, env, data)
- [ ] Optimization targeted the root cause, not a symptom (e.g., caching a slow query vs fixing the N+1)
- [ ] Regression tested: optimized code still passes all existing tests
- [ ] Cost impact calculated: projected infrastructure savings vs implementation effort

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This query looks slow, I will add a cache" | Adding cache before profiling the actual query often masks N+1 patterns that caching alone cannot fix |
| "Micro-optimizations always help" | Micro-optimizations without profiler data routinely make code harder to read without measurable impact |
| "Production is too complex to profile" | Distributed profiling (e2e traces, sampled CPU profiles) pinpoints bottlenecks more precisely than staging benchmarks |

## When to Use

Use when the application is measurably slow, memory usage grows over time, database queries lag, infrastructure costs are too high, or capacity planning requires baseline numbers. Do NOT use for speculative "premature optimization," one-line utilities where the overhead is dwarfed by I/O, or code paths with zero evidence of being hot.
