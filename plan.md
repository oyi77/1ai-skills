1. **Optimize Near-Duplicate Detection in `scripts/lint-skills.py`**
   - The current `check_duplicates` function contains an $O(N^2)$ nested loop (per category) for comparing strings using `difflib.SequenceMatcher` via the `similarity` function.
   - Refactor `check_duplicates` in `scripts/lint-skills.py` to maintain readability. Create a helper function `_batch_similarity` or perform the internal loop optimization cleanly within `check_duplicates` while keeping it abstracted if possible. Let's do it directly in `check_duplicates` but cleaner.
   - Alternatively, change `similarity` to accept a `matcher` object? No, we can just instantiate `matcher = SequenceMatcher(None, b=lower1)` and reuse it in the inner loop, updating with `.set_seq1()`.
   - Actually, the reviewer is right: inline math logic ruins readability. We can extract it to a helper function within `check_duplicates` or just write it cleanly. Wait, the memory journal says:
   "When using difflib.SequenceMatcher(...).ratio() in nested loops (O(N^2) complexity) with a high similarity threshold, pre-calculate string lengths and transformations (e.g., .lower()) before the loop. Instantiate the matcher ONCE per outer loop. Set the outer loop sequence using .set_seq2() (or constructor) to leverage internal caching, and update the inner loop sequence using .set_seq1(). Furthermore, use a length-based pre-check... AND check matcher.real_quick_ratio() and matcher.quick_ratio()..."
   I will implement this exactly as described, replacing the inner loop in `check_duplicates` with this logic, and add comments to explain it.
2. **Pre-commit Checks**
   - Complete pre-commit steps.
3. **Submit PR**
   - Create PR.
