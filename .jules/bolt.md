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
## 2025-06-02 - SQLite N+1 Batched Updates via executemany
**Learning:** In the memory system, looping over database SELECT results to run a single  query per row creates massive N+1 query bottlenecks and slows down  exponentially as the memory table grows.
**Action:** When updating multiple database rows with dynamic variables, collect the parameter tuples in a list () and process them in a single batch operation using  to minimize I/O overhead and database locking.
## 2025-06-02 - SQLite N+1 Batched Updates via executemany
**Learning:** In the memory system, looping over database SELECT results to run a single `UPDATE` query per row creates massive N+1 query bottlenecks and slows down `apply_decay` exponentially as the memory table grows.
**Action:** When updating multiple database rows with dynamic variables, collect the parameter tuples in a list (`updates.append(...)`) and process them in a single batch operation using `sqlite3.Connection.executemany()` to minimize I/O overhead and database locking.

## 2025-06-08 - [Avoid N+1 Queries during Existence Checks]
**Learning:** Checking for row existence (e.g. `SELECT 1 FROM table WHERE id = ?`) inside a loop before insertion introduces severe N+1 query bottlenecks and slows down database writes.
**Action:** Extract all identifiers from the loop, perform a batched `SELECT id FROM table WHERE id IN (?, ...)` query to filter out existing elements, and execute bulk inserts using `.executemany()`.
