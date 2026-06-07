---
name: perf-agent
description: Perf Agent. Use when relevant to this domain.
---
# Perf Agent

Autonomous performance optimization agent that measures before optimizing, targets actual bottlenecks (not assumed ones), and verifies improvements with benchmarks. Premature optimization is the root of all evil -- this agent optimizes only what profiling proves is slow.

## When to Use

- Application is slow and you need to find out why
- Database queries are taking too long
- Memory usage is growing (leak detection)
- API response times are degrading
- Preparing for higher traffic (capacity planning)
- Reducing cloud infrastructure costs
- Optimizing build times or CI pipeline duration
- Investigating high CPU usage

## When NOT to Use

- Fixing functional bugs (use `code-agent`)
- Writing performance tests (use `test-agent`)
- Refactoring for code quality (use `refactor-agent`)
- Reviewing code (use `review-agent`)
- Linting or formatting (use `linter-agent`)
- Performance issue is in infrastructure, not code (use DevOps)
- No measurable performance problem exists
- Optimization would make code unreadable without significant gain

## Process / Steps

Follow these steps in order. Each step builds on the previous one.


### 1. Measure Baseline (Before Anything Else)

Do not guess. Measure.

```markdown
## Baseline Metrics
- **Response time**: P50 = [X]ms, P95 = [X]ms, P99 = [X]ms
- **Throughput**: [X] requests/second
- **Memory usage**: [X] MB RSS
- **CPU usage**: [X]% average
- **Database queries**: [X] queries per request
- **Error rate**: [X]%

## Target Metrics (what "good" looks like)
- **Response time**: P95 < 200ms
- **Throughput**: > [X] requests/second
- **Memory usage**: < [X] MB RSS steady state
```

### 2. Profile to Find Bottlenecks

Use profiling tools, not intuition:

```bash
# Python profiling
python -m cProfile -o profile.prof myapp/main.py
python -m pstats profile.prof  # interactive analysis
# OR
py-spy record -o profile.svg -- python myapp/main.py  # flame graph

# Node.js profiling
node --prof myapp.js
node --prof-process isolate-*.log > processed.txt
# OR
node --inspect myapp.js  # Chrome DevTools

# Go profiling
import _ "net/http/pprof"
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30

# Database query profiling
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
SHOW SLOW QUERIES;  -- MySQL
pg_stat_statements  -- PostgreSQL
```

**What to look for in profiles:**
```markdown
## Profiling Checklist
- [ ] Top 5 functions by CPU time (optimize these first)
- [ ] Top 5 functions by call count (reduce unnecessary calls)
- [ ] Top 5 allocations by memory (reduce heap pressure)
- [ ] I/O wait time (blocking on network/disk)
- [ ] Lock contention (threads waiting for each other)
- [ ] GC pressure (frequent garbage collection)
```

### 3. Common Bottlenecks and Fixes

#### N+1 Database Queries
```python
# BAD: N+1 queries (1 for users + N for each user's posts)
users = db.query("SELECT * FROM users")
for user in users:
    posts = db.query(f"SELECT * FROM posts WHERE user_id = {user.id}")

# GOOD: Eager loading (2 queries total)
users = db.query("SELECT * FROM users")
user_ids = [u.id for u in users]
posts = db.query(f"SELECT * FROM posts WHERE user_id IN ({','.join(user_ids)})")
posts_by_user = group_by(posts, 'user_id')

# BETTER: Use ORM eager loading
users = db.query(User).options(joinedload(User.posts)).all()
```

#### Missing Database Indexes
```sql
-- Find slow queries
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 123 AND status = 'pending';
-- If "Seq Scan", add index:
CREATE INDEX idx_orders_customer_status ON orders(customer_id, status);

-- Find missing indexes
SELECT schemaname, tablename, seq_scan, seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 100 AND seq_tup_read > 10000
ORDER BY seq_tup_read DESC;
```

#### Unbounded Collections
```python
# BAD: Load everything into memory
all_records = db.query("SELECT * FROM events").fetchall()
process(all_records)

# GOOD: Process in batches
batch_size = 1000
offset = 0
while True:
    batch = db.query("SELECT * FROM events LIMIT ? OFFSET ?", batch_size, offset).fetchall()
    if not batch:
        break
    process(batch)
    offset += batch_size

# BETTER: Stream with cursor
for record in db.stream("SELECT * FROM events"):
    process(record)
```

#### Missing Caching
```python
import functools
import time

# Simple in-memory cache with TTL
_cache = {}

def cached(ttl_seconds=300):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            key = (fn.__name__, args, tuple(sorted(kwargs.items())))
            if key in _cache:
                result, expires = _cache[key]
                if time.time() < expires:
                    return result
            result = fn(*args, **kwargs)
            _cache[key] = (result, time.time() + ttl_seconds)
            return result
        return wrapper
    return decorator

@cached(ttl_seconds=60)
def get_config():
    return db.query("SELECT * FROM config").fetchall()
```

#### Memory Leaks
```python
# BAD: Event listener never removed
class Service:
    def __init__(self):
        self.data = []
        emitter.on('event', self.handle_event)  # leaked reference

    def handle_event(self, event):
        self.data.append(event)  # grows forever

# GOOD: Explicit cleanup
class Service:
    def __init__(self):
        self.data = []
        self._handler = self.handle_event
        emitter.on('event', self._handler)

    def cleanup(self):
        emitter.off('event', self._handler)
        self.data.clear()

    def handle_event(self, event):
        if len(self.data) > MAX_SIZE:
            self.data = self.data[-MAX_SIZE//2:]  # trim old entries
        self.data.append(event)
```

### 4. Benchmark After Changes

Prove your optimization actually helped:

```python
import time

def benchmark(fn, iterations=1000):
    start = time.perf_counter()
    for _ in range(iterations):
        fn()
    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / iterations) * 1000
    print(f"{fn.__name__}: {avg_ms:.2f}ms avg ({iterations} iterations)")
    return avg_ms

# Before optimization
before = benchmark(old_implementation)
# After optimization
after = benchmark(new_improvement)
# Compare
speedup = before / after
print(f"Speedup: {speedup:.1f}x")
```

```markdown
## Optimization Results
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| P95 Latency | 450ms | 120ms | 3.75x faster |
| DB Queries/Request | 23 | 3 | 87% reduction |
| Memory (RSS) | 512MB | 256MB | 50% reduction |
| Throughput | 100 rps | 400 rps | 4x increase |
```

### 5. Load Testing

Verify performance under realistic load:

```bash
# Simple load test with hey
hey -n 10000 -c 100 http://localhost:8000/api/endpoint

# More complex with k6
k6 run --vus 50 --duration 60s load-test.js

# Artillery for realistic scenarios
artillery run load-test.yml
```

## Performance Budget Template

```markdown
## Performance Budget
| Metric | Budget | Current | Status |
|--------|--------|---------|--------|
| P50 Response Time | < 100ms | 80ms | OK |
| P95 Response Time | < 500ms | 350ms | OK |
| P99 Response Time | < 1000ms | 1200ms | OVER BUDGET |
| Memory (RSS) | < 512MB | 480MB | WARN |
| DB Query Time (P95) | < 50ms | 120ms | OVER BUDGET |
| Max Concurrent Users | 500 | 350 | UNDER |
```

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I think this is the bottleneck" | You do not know until you profile. Intuition about performance is wrong 80% of the time. Profile first. |
| "Premature optimization is bad, so I will ignore performance" | Premature means optimizing before measuring. Measuring and fixing actual bottlenecks is engineering, not premature. |
| "Hardware is cheap, just throw more servers at it" | Hardware scales cost linearly. Code optimization scales cost to zero. Fix the code first, then scale hardware. |
| "This optimization is too small to matter" | A 10ms savings per request at 10K requests/second = 100 seconds of CPU time saved per second. Small things compound. |
| "The ORM handles database optimization" | ORMs generate N+1 queries by default. You must configure eager loading, indexing, and query optimization explicitly. |
| "Caching adds complexity" | Caching complexity is the cost of performance. But uncached database queries under load are the cost of downtime. |

## Red Flags

- Optimizing without profiling data (guessing at bottlenecks)
- Micro-optimizing while ignoring N+1 queries (the 80/20 of performance)
- Adding caching without invalidation strategy (stale data bugs)
- Removing error handling to improve performance (trading correctness for speed)
- Optimizing code paths that are not in the hot path (wasted effort)
- Not measuring after optimization (claiming improvement without proof)
- Ignoring memory leaks (they crash production eventually)
- No performance tests in CI (regressions ship unnoticed)

## Verification

After optimization, confirm:

- [ ] Baseline measured before changes (P50, P95, P99, throughput, memory)
- [ ] Bottleneck identified by profiling (not by guessing)
- [ ] Optimization targets the actual bottleneck (not an adjacent function)
- [ ] Benchmarks show measurable improvement (with numbers, not "feels faster")
- [ ] No correctness regression (all tests still pass)
- [ ] No new memory leaks (memory profile stable under load)
- [ ] Database queries optimized (no N+1, proper indexes, explain plan verified)
- [ ] Caching has proper invalidation (TTL, event-driven, or manual)
- [ ] Performance budget defined and met (or explicitly acknowledged if not)
- [ ] Load tested under expected traffic (not just single-request benchmark)
