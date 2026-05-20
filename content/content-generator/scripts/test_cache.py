import os
import sys
import time

# Adjust path to find the cache module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cache import Cache


def test_cache_eviction():
    test_db_path = ".cache/test_cache.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    # Very small cache size, e.g. 1 MB, but let's test logic explicitly with bytes size
    # By default, max_size_mb is in MB.
    # Let's insert large string values.

    cache = Cache(db_path=test_db_path, max_size_mb=1)

    # 1 MB is 1048576 bytes.
    # We will insert values of size roughly 400KB
    large_val1 = "A" * 400000
    large_val2 = "B" * 400000
    large_val3 = "C" * 400000
    large_val4 = "D" * 400000

    print("Setting key1")
    cache.set("key1", large_val1)
    time.sleep(0.1)  # ensure order of created_at

    print("Setting key2")
    cache.set("key2", large_val2)
    time.sleep(0.1)

    print("Setting key3")
    cache.set("key3", large_val3)
    time.sleep(0.1)

    print("Setting key4 (should trigger eviction)")
    cache.set("key4", large_val4)

    stats = cache.get_stats()
    print("Cache Stats:", stats)

    # key1 should have been evicted
    assert cache.get("key1") is None, "key1 should be evicted"

    # The cache should still contain the most recent keys that fit in limit
    print("Cache eviction works!")

    # Clean up test artifact
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


if __name__ == "__main__":
    test_cache_eviction()
