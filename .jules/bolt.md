## 2024-05-14 - [Optimize Cache Eviction]
**Learning:** Found an N+1 query vulnerability in an SQLite-based cache class where enforcing maximum size during insert caused multiple serial SELECT and DELETE operations in a tight `while` loop. The previous query `ORDER BY created_at ASC LIMIT 1` also lacked an index, causing a full table scan repeatedly.
**Action:** Replaced the loop with a single query of all records ordered by an indexed `created_at` using a server-side cursor iteration, locally aggregated keys to delete, and used `executemany` for batched deletion to improve query counts and memory usage without causing full table loading via `fetchall()`.

## 2025-05-16 - [Optimize SQLite Aggregation Queries]
**Learning:** Multiple sequential SQLite aggregation queries (e.g., counting types and summing costs) mapped directly to dictionary keys can severely bottleneck performance due to repeated database round-trips for the exact same filtered rows. Furthermore, f-strings were being used for SQL variables.
**Action:** Always combine multiple aggregation queries into a single query using conditional aggregation (`SUM(CASE WHEN...)`) to reduce database round-trips. Always use parameterized queries (`?`) for variables instead of string interpolation.
