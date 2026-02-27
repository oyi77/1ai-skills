"""
Result Gallery — Store & manage all generated content
SQLite-based, with thumbnail support and tagging
"""
import sqlite3, os, json, time, shutil
from datetime import datetime

DB_PATH     = "/home/openclaw/.openclaw/workspace/output/gallery.db"
GALLERY_DIR = "/home/openclaw/.openclaw/workspace/output/gallery"
os.makedirs(GALLERY_DIR, exist_ok=True)


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     TEXT,
                type        TEXT,       -- 'image' | 'video' | 'clone'
                category    TEXT,
                style       TEXT,
                format      TEXT,
                file_path   TEXT,
                thumb_path  TEXT,
                prompt      TEXT,
                cost_usd    REAL DEFAULT 0,
                rating      INTEGER DEFAULT 0,
                tags        TEXT DEFAULT '[]',
                posted_to   TEXT DEFAULT '[]',
                created_at  INTEGER,
                project     TEXT DEFAULT ''
            )
        """)
        conn.commit()

init_db()


def save_result(chat_id: str, file_path: str, meta: dict) -> int:
    """Save a generated result to gallery"""
    # Copy file to gallery dir
    ext = os.path.splitext(file_path)[1]
    ts  = int(time.time())
    gallery_path = os.path.join(GALLERY_DIR, f"{ts}_{meta.get('type','content')}{ext}")
    shutil.copy2(file_path, gallery_path)

    with _conn() as conn:
        cursor = conn.execute("""
            INSERT INTO results 
            (chat_id, type, category, style, format, file_path, prompt, cost_usd, tags, created_at, project)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(chat_id),
            meta.get("type", "image"),
            meta.get("category", ""),
            meta.get("style", ""),
            meta.get("format", ""),
            gallery_path,
            meta.get("prompt", "")[:500],
            meta.get("cost_usd", 0),
            json.dumps(meta.get("tags", [])),
            ts,
            meta.get("project", "")
        ))
        conn.commit()
        return cursor.lastrowid


def get_results(chat_id: str = None, limit: int = 20, offset: int = 0,
                category: str = None, content_type: str = None) -> list:
    """Get gallery results with optional filters"""
    query = "SELECT * FROM results WHERE 1=1"
    params = []
    if chat_id:
        query += " AND chat_id = ?"; params.append(str(chat_id))
    if category:
        query += " AND category = ?"; params.append(category)
    if content_type:
        query += " AND type = ?"; params.append(content_type)
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    with _conn() as conn:
        rows = conn.execute(query, params).fetchall()
    return [dict(r) for r in rows]


def get_result(result_id: int) -> dict:
    with _conn() as conn:
        row = conn.execute("SELECT * FROM results WHERE id = ?", (result_id,)).fetchone()
    return dict(row) if row else {}


def delete_result(result_id: int):
    result = get_result(result_id)
    if result and os.path.exists(result.get("file_path", "")):
        os.remove(result["file_path"])
    with _conn() as conn:
        conn.execute("DELETE FROM results WHERE id = ?", (result_id,))
        conn.commit()


def rate_result(result_id: int, rating: int):
    """Rate result 1-5 stars"""
    with _conn() as conn:
        conn.execute("UPDATE results SET rating = ? WHERE id = ?", (rating, result_id))
        conn.commit()


def mark_posted(result_id: int, platform: str):
    """Mark result as posted to a platform"""
    result = get_result(result_id)
    posted = json.loads(result.get("posted_to", "[]"))
    if platform not in posted:
        posted.append(platform)
    with _conn() as conn:
        conn.execute("UPDATE results SET posted_to = ? WHERE id = ?",
                     (json.dumps(posted), result_id))
        conn.commit()


def get_stats(chat_id: str = None) -> dict:
    """Get gallery statistics"""
    where = f"WHERE chat_id = '{chat_id}'" if chat_id else ""
    with _conn() as conn:
        total     = conn.execute(f"SELECT COUNT(*) FROM results {where}").fetchone()[0]
        images    = conn.execute(f"SELECT COUNT(*) FROM results {where} {'AND' if where else 'WHERE'} type='image'").fetchone()[0] if total else 0
        videos    = conn.execute(f"SELECT COUNT(*) FROM results {where} {'AND' if where else 'WHERE'} type='video'").fetchone()[0] if total else 0
        total_cost = conn.execute(f"SELECT SUM(cost_usd) FROM results {where}").fetchone()[0] or 0
        top_style = conn.execute(f"SELECT style, COUNT(*) as c FROM results {where} GROUP BY style ORDER BY c DESC LIMIT 1").fetchone()
    return {
        "total": total,
        "images": images,
        "videos": videos,
        "total_cost_usd": round(total_cost, 4),
        "total_cost_idr": round(total_cost * 16300, 0),
        "top_style": top_style[0] if top_style else "N/A"
    }


def build_gallery_message(chat_id: str) -> tuple[str, list]:
    """Build gallery browser message with buttons"""
    stats = get_stats(chat_id)
    results = get_results(chat_id, limit=5)

    text = (
        f"🗂️ *Galeri Kamu*\n\n"
        f"📊 Total: {stats['total']} konten "
        f"({stats['images']} foto, {stats['videos']} video)\n"
        f"💰 Total cost: ${stats['total_cost_usd']:.3f} "
        f"(~Rp {int(stats['total_cost_idr']):,})\n"
        f"🎨 Style favorit: {stats['top_style']}\n\n"
    )

    if results:
        text += "📋 *5 Terbaru:*\n"
        for r in results:
            dt = datetime.fromtimestamp(r['created_at']).strftime("%d/%m %H:%M")
            emoji = "🖼️" if r['type'] == 'image' else "🎬"
            text += f"{emoji} [{dt}] {r['category']} × {r['style']}\n"

    buttons = [
        [{"text": "📋 Lihat Semua", "callback_data": "gallery:list:0"},
         {"text": "🗑️ Bersihkan", "callback_data": "gallery:clean"}],
        [{"text": "📊 Cost Report", "callback_data": "gallery:costs"},
         {"text": "✖️ Tutup", "callback_data": "gallery:close"}],
    ]
    return text, buttons


if __name__ == "__main__":
    print("Gallery DB initialized at:", DB_PATH)
    stats = get_stats()
    print("Stats:", stats)
