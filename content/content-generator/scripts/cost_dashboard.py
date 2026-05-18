"""
Cost Dashboard — Real-time cost tracking per generation
Tracks: NVIDIA images, BytePlus videos, Groq LLM, Edge TTS
"""
import sqlite3, os, json, time
from datetime import datetime, date

DB_PATH = "/home/openclaw/.openclaw/workspace/output/costs.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Real pricing (as of 2026-02-27)
PRICES = {
    "nvidia_flux":    0.0040,  # per image
    "nvidia_sd3":     0.0035,  # per image
    "byteplus_lite":  0.0260,  # per 5s clip
    "byteplus_pro":   0.0500,  # per 5s clip (estimated)
    "groq_llm":       0.0008,  # per request (avg)
    "edge_tts":       0.0000,  # FREE
    "yt_dlp":         0.0000,  # FREE
    "whisper":        0.0000,  # FREE (local)
}

IDR_RATE = 16300  # USD to IDR


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cost_log (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id     TEXT,
                provider    TEXT,
                operation   TEXT,
                units       REAL DEFAULT 1,
                unit_cost   REAL,
                total_cost  REAL,
                project     TEXT DEFAULT '',
                created_at  INTEGER
            )
        """)
        conn.commit()

init_db()


def log_cost(provider: str, operation: str, chat_id: str = "system",
             units: float = 1, project: str = "") -> float:
    """Log a cost event. Returns cost in USD."""
    unit_cost  = PRICES.get(provider, 0)
    total_cost = unit_cost * units
    with _conn() as conn:
        conn.execute("""
            INSERT INTO cost_log (chat_id, provider, operation, units, unit_cost, total_cost, project, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (str(chat_id), provider, operation, units, unit_cost, total_cost, project, int(time.time())))
        conn.commit()
    return total_cost


def get_session_cost(chat_id: str, since_ts: int = None) -> dict:
    """Get cost for a chat session"""
    # Performance Optimization: Replaced fetching all rows and manual aggregation
    # with SQLite GROUP BY queries to reduce memory footprint and database roundtrips.
    base_cond = "WHERE chat_id = ?"
    params = [str(chat_id)]
    if since_ts:
        base_cond += " AND created_at >= ?"
        params.append(since_ts)

    with _conn() as conn:
        # Get total and count
        total_query = f"SELECT SUM(total_cost), COUNT(*) FROM cost_log {base_cond}"
        row = conn.execute(total_query, params).fetchone()

        # Access by index as per project data access patterns
        total = row[0] if row and row[0] is not None else 0.0
        count = row[1] if row and row[1] is not None else 0

        # Get by provider breakdown
        prov_query = f"SELECT provider, SUM(total_cost) FROM cost_log {base_cond} GROUP BY provider"
        prov_rows = conn.execute(prov_query, params).fetchall()

        by_provider = {r[0]: r[1] for r in prov_rows if r[0] is not None}

    return {
        "total_usd": round(total, 4),
        "total_idr": round(total * IDR_RATE),
        "by_provider": {k: round(v, 4) for k, v in by_provider.items()},
        "count": count
    }


def get_monthly_cost(year: int = None, month: int = None) -> dict:
    """Get cost for current/given month"""
    today = date.today()
    year  = year or today.year
    month = month or today.month
    start     = int(datetime(year, month, 1).timestamp())
    next_year = year + 1 if month == 12 else year
    next_mon  = 1 if month == 12 else month + 1
    end       = int(datetime(next_year, next_mon, 1).timestamp())

    # Performance Optimization: Using SQLite aggregations rather than fetching all
    # rows into memory and doing calculations in Python loops.
    with _conn() as conn:
        # Get total and count
        total_query = "SELECT SUM(total_cost), COUNT(*) FROM cost_log WHERE created_at >= ? AND created_at < ?"
        row = conn.execute(total_query, (start, end)).fetchone()
        total = row[0] if row and row[0] is not None else 0.0
        transactions = row[1] if row and row[1] is not None else 0

        # Get by day breakdown
        day_query = """
            SELECT date(created_at, 'unixepoch', 'localtime') as day, SUM(total_cost)
            FROM cost_log
            WHERE created_at >= ? AND created_at < ?
            GROUP BY day
        """
        day_rows = conn.execute(day_query, (start, end)).fetchall()
        by_day = {r[0]: round(r[1], 4) for r in day_rows if r[0] is not None}

        # Get by provider breakdown
        prov_query = """
            SELECT provider, SUM(total_cost)
            FROM cost_log
            WHERE created_at >= ? AND created_at < ?
            GROUP BY provider
        """
        prov_rows = conn.execute(prov_query, (start, end)).fetchall()
        by_provider = {r[0]: round(r[1], 4) for r in prov_rows if r[0] is not None}

    return {
        "period": f"{year}-{month:02d}",
        "total_usd": round(total, 4),
        "total_idr": round(total * IDR_RATE),
        "by_provider": by_provider,
        "by_day": dict(sorted(by_day.items())),
        "transactions": transactions,
        "budget_used_pct": round(total / 100 * 100, 1)  # Assuming $100 budget
    }


def estimate_generation_cost(format_type: str, n_scenes: int = 1,
                              model: str = "pro") -> dict:
    """Estimate cost before generating"""
    vid_key = f"byteplus_{model}"
    img_key = "nvidia_flux"

    costs = {
        "foto":       {"nvidia_flux": 1, vid_key: 0},
        "video_15s":  {"nvidia_flux": 1, vid_key: 3},   # ~3 clips
        "video_30s":  {"nvidia_flux": 1, vid_key: 6},   # ~6 clips
        "tiktok_60s": {"nvidia_flux": n_scenes, vid_key: n_scenes * 2},
    }

    breakdown = costs.get(format_type, {"nvidia_flux": 1, vid_key: 1})
    total = sum(PRICES.get(k, 0) * v for k, v in breakdown.items())
    total += PRICES["groq_llm"] * 2  # Script + analysis

    return {
        "breakdown": breakdown,
        "total_usd": round(total, 4),
        "total_idr": round(total * IDR_RATE),
        "currency_note": f"~Rp {round(total * IDR_RATE):,}"
    }


def build_dashboard_message(chat_id: str = None) -> str:
    """Build cost dashboard text"""
    monthly = get_monthly_cost()
    today_start = int(datetime.now().replace(hour=0, minute=0, second=0).timestamp())

    with _conn() as conn:
        today_rows = conn.execute(
            "SELECT SUM(total_cost) FROM cost_log WHERE created_at >= ?", (today_start,)
        ).fetchone()[0] or 0

    text = (
        f"💰 *Cost Dashboard*\n\n"
        f"📅 Bulan ini ({monthly['period']}):\n"
        f"  Total: *${monthly['total_usd']}* (~Rp {monthly['total_idr']:,})\n"
        f"  Transaksi: {monthly['transactions']}\n"
        f"  Budget: {monthly['budget_used_pct']}% dari $100\n\n"
        f"📆 Hari ini:\n"
        f"  Total: *${today_rows:.4f}* (~Rp {int(today_rows*IDR_RATE):,})\n\n"
        f"📊 Per provider:\n"
    )
    for prov, cost in monthly.get("by_provider", {}).items():
        text += f"  • {prov}: ${cost}\n"

    text += f"\n📋 Harga per operasi:\n"
    for op, price in PRICES.items():
        if price > 0:
            text += f"  • {op}: ${price}\n"
        else:
            text += f"  • {op}: GRATIS\n"

    return text


if __name__ == "__main__":
    # Demo
    print(build_dashboard_message())
    print("\nEstimate video_15s:", estimate_generation_cost("video_15s"))
    print("Estimate tiktok_60s:", estimate_generation_cost("tiktok_60s", n_scenes=6))
