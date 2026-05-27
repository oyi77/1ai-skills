import sqlite3
import os
import sys
from unittest import mock

# Patch gallery script dependencies
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "content/content-generator/scripts")
    ),
)

TEST_DIR = "/tmp/gallery_test_db"
os.makedirs(TEST_DIR, exist_ok=True)
TEST_DB_PATH = os.path.join(TEST_DIR, "gallery.db")

orig_connect = sqlite3.connect
def my_connect(path, *args, **kwargs):
    if str(path).endswith("gallery.db"):
        return orig_connect(TEST_DB_PATH, *args, **kwargs)
    return orig_connect(path, *args, **kwargs)

with mock.patch("os.makedirs"):
    with mock.patch("sqlite3.connect", side_effect=my_connect):
        import gallery

# Mock DB paths to a local temporary directory
gallery.DB_PATH = TEST_DB_PATH
gallery.GALLERY_DIR = TEST_DIR

# Clean up DB if it exists
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

gallery.init_db()


# Insert dummy data
def insert_dummy_data():
    with gallery._conn() as conn:
        conn.execute(
            """
            INSERT INTO results (chat_id, type, cost_usd, style) VALUES
            ('user_1', 'image', 0.5, 'anime'),
            ('user_1', 'image', 0.5, 'realistic'),
            ('user_1', 'video', 2.0, 'anime'),
            ('user_1', 'video', 1.0, '3d'),
            ('user_1', 'image', 0.5, 'anime'),
            ('user_2', 'image', 1.0, 'realistic')
        """
        )
        conn.commit()


insert_dummy_data()

stats_all = gallery.get_stats()
stats_user_1 = gallery.get_stats("user_1")
stats_user_2 = gallery.get_stats("user_2")

assert stats_all["total"] == 6
assert stats_all["images"] == 4
assert stats_all["videos"] == 2
assert stats_all["total_cost_usd"] == 5.5
assert stats_all["top_style"] == "anime"

assert stats_user_1["total"] == 5
assert stats_user_1["images"] == 3
assert stats_user_1["videos"] == 2
assert stats_user_1["total_cost_usd"] == 4.5
assert stats_user_1["top_style"] == "anime"

assert stats_user_2["total"] == 1
assert stats_user_2["images"] == 1
assert stats_user_2["videos"] == 0
assert stats_user_2["total_cost_usd"] == 1.0
assert stats_user_2["top_style"] == "realistic"

print("All assertions passed!")
