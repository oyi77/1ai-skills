## 2024-05-14 - [Optimize Cache Eviction]
**Learning:** Found an N+1 query vulnerability in an SQLite-based cache class where enforcing maximum size during insert caused multiple serial SELECT and DELETE operations in a tight `while` loop. The previous query `ORDER BY created_at ASC LIMIT 1` also lacked an index, causing a full table scan repeatedly.
**Action:** Replaced the loop with a single query of all records ordered by an indexed `created_at` using a server-side cursor iteration, locally aggregated keys to delete, and used `executemany` for batched deletion to improve query counts and memory usage without causing full table loading via `fetchall()`.

## 2025-05-16 - [Optimize SQLite Aggregation Queries]
**Learning:** Multiple sequential SQLite aggregation queries (e.g., counting types and summing costs) mapped directly to dictionary keys can severely bottleneck performance due to repeated database round-trips for the exact same filtered rows. Furthermore, f-strings were being used for SQL variables.
**Action:** Always combine multiple aggregation queries into a single query using conditional aggregation (`SUM(CASE WHEN...)`) to reduce database round-trips. Always use parameterized queries (`?`) for variables instead of string interpolation.
## 2025-02-27 - [SQLite Optimization with Python `datetime`]
**Learning:** In the `content-generator` app, aggregation loops involving Python's `datetime.fromtimestamp()` over large SQL result sets proved incredibly slow and memory-intensive.
**Action:** When calculating daily/monthly rollups, push aggregation (COUNT, SUM) to SQLite and use SQLite's native `date(..., 'unixepoch', 'localtime')` instead of processing dates in Python loops.

## 2025-05-27 - [SQLite Indexes for Frequent Queries]
**Learning:** Found missing database indexes on `chat_id` and `created_at` fields in SQLite tables used for gallery browsing and cost aggregation. As the DB grows, filtering or sorting by these fields without an index causes O(N) full table scans, severely impacting query performance.
**Action:** Consistently ensure fields used heavily in `WHERE` and `ORDER BY` clauses (especially foreign keys like `chat_id` and timestamps like `created_at`) have explicit database indexes created during `init_db()`.

## 2026-06-01 - [Resolve N+1 Queries in Log Ingestion]
**Learning:** Found N+1 query vulnerability when iterating through arrays of records (e.g. log files or network responses) to check existence (`SELECT 1 WHERE id = ?`), insert new records (`INSERT`), and update tracking (`UPDATE`) for each element independently. The constant context switching to SQLite scales poorly on large iterations.
**Action:** Pre-fetch existing record IDs via an `IN (?, ...)` clause, construct insertion/update datasets locally into python lists, and execute them as a single batched `executemany(...)` instead of looping `.execute(...)`.
