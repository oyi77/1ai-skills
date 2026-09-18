## 2024-05-14 - [Optimize Cache Eviction]
**Learning:** Found an N+1 query vulnerability in an SQLite-based cache class where enforcing maximum size during insert caused multiple serial SELECT and DELETE operations in a tight `while` loop. The previous query `ORDER BY created_at ASC LIMIT 1` also lacked an index, causing a full table scan repeatedly.
**Action:** Replaced the loop with a single query of all records ordered by an indexed `created_at` using a server-side cursor iteration, locally aggregated keys to delete, and used `executemany` for batched deletion to improve query counts and memory usage without causing full table loading via `fetchall()`.

## 2025-02-27 - [SQLite Optimization with Python `datetime`]
**Learning:** In the `content-generator` app, aggregation loops involving Python's `datetime.fromtimestamp()` over large SQL result sets proved incredibly slow and memory-intensive.
**Action:** When calculating daily/monthly rollups, push aggregation (COUNT, SUM) to SQLite and use SQLite's native `date(..., 'unixepoch', 'localtime')` instead of processing dates in Python loops.

## 2025-05-16 - [Optimize SQLite Aggregation Queries]
**Learning:** Multiple sequential SQLite aggregation queries (e.g., counting types and summing costs) mapped directly to dictionary keys can severely bottleneck performance due to repeated database round-trips for the exact same filtered rows. Furthermore, f-strings were being used for SQL variables.
**Action:** Always combine multiple aggregation queries into a single query using conditional aggregation (`SUM(CASE WHEN...)`) to reduce database round-trips. Always use parameterized queries (`?`) for variables instead of string interpolation.


## 2025-05-27 - [SQLite Indexes for Frequent Queries]
**Learning:** Found missing database indexes on `chat_id` and `created_at` fields in SQLite tables used for gallery browsing and cost aggregation. As the DB grows, filtering or sorting by these fields without an index causes O(N) full table scans, severely impacting query performance.
**Action:** Consistently ensure fields used heavily in `WHERE` and `ORDER BY` clauses (especially foreign keys like `chat_id` and timestamps like `created_at`) have explicit database indexes created during `init_db()`.
## 2025-06-02 - SQLite N+1 Batched Updates via executemany
**Learning:** In the memory system, looping over database SELECT results to run a single `UPDATE` query per row creates massive N+1 query bottlenecks and slows down `apply_decay` exponentially as the memory table grows.
**Action:** When updating multiple database rows with dynamic variables, collect the parameter tuples in a list (`updates.append(...)`) and process them in a single batch operation using `sqlite3.Connection.executemany()` to minimize I/O overhead and database locking.

## 2025-06-27 - [Optimize YAML Parsing Speed]
**Learning:** Parsing hundreds or thousands of YAML files (e.g., `SKILL.md` frontmatter) using `yaml.safe_load()` in pure Python creates a massive CPU bottleneck during batch operations.
**Action:** When working with PyYAML for large-scale file processing, always switch to the C-extension loader `yaml.load(..., Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))`. This provides a ~5x speedup by seamlessly utilizing the C-based parser when available, while safely falling back to pure Python without complex nested exception handling.

## 2024-05-18 - SequenceMatcher O(N^2) Optimization via Length Pre-check
**Learning:** `difflib.SequenceMatcher.ratio()` calculates similarity as `2.0 * matches / total_length`, meaning the maximum possible ratio is inherently bound by `2.0 * min(len(a), len(b)) / (len(a) + len(b))`. In `scripts/lint-skills.py`, this was being called in a hot N^2 loop over 1300+ strings to find duplicates, taking ~47 seconds.
**Action:** When using `difflib.SequenceMatcher(None, a, b).ratio()` to check against a strict threshold (e.g. 0.99), always implement a fast upper-bound pre-check (`if 2.0 * min(len(a), len(b)) < threshold * (len(a) + len(b)): return 0.0`) to avoid the expensive sequence matching for strings that are mathematically impossible to match. This dropped execution time from 47s to 3s (14x speedup).
## 2025-07-27 - [Optimize YAML Parsing Speed]
**Learning:** Parsing hundreds or thousands of YAML files (e.g., `SKILL.md` frontmatter) using `yaml.safe_load()` in pure Python creates a massive CPU bottleneck during batch operations.
**Action:** When working with PyYAML for large-scale file processing, always switch to the C-extension loader `yaml.load(..., Loader=getattr(yaml, 'CSafeLoader', yaml.SafeLoader))`. This provides a ~5x speedup by seamlessly utilizing the C-based parser when available, while safely falling back to pure Python without complex nested exception handling.
## 2025-02-28 - PyYAML C-extension usage for serialization
**Learning:** Just like `yaml.safe_load()`, using `yaml.safe_dump()` in pure Python creates a massive CPU bottleneck during batch operations (like fixing hundreds of `SKILL.md` frontmatters).
**Action:** When updating or serializing multiple YAML files, use `yaml.dump(..., Dumper=getattr(yaml, 'CSafeDumper', yaml.SafeDumper))` to dramatically improve performance by utilizing the PyYAML C-extension (`libyaml`) when available.
## 2024-05-24 - Pre-compiled Regexes for High-Volume Parsing
**Learning:** In scripts that parse large volumes of Markdown files, repeatedly calling `re.match()` or `re.finditer()` with inline string patterns inside loops creates significant overhead due to regex compilation and cache lookups. For instance, in `scripts/test_quality.py`, optimizing parsing logic by manually finding substrings reduces performance compared to using pre-compiled regex objects at the module-level.
**Action:** When implementing parsing tools that iterate over thousands of files, hoist `re.compile()` calls to the module level instead of using inline `re.match()` inside loops. Avoid manual string manipulation fast-paths (like `split()` or `startswith()`) as they compromise correctness; use `re.compile()` for the optimal balance of speed and robustness.
