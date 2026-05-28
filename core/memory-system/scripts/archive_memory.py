"""
archive_memory.py — Compressed JSONL archival storage.

One gzipped JSONL file per day: archive/YYYY-MM-DD.jsonl.gz
NOT used in normal retrieval. Only accessed on explicit request.
"""
import gzip
import json
import logging
import os
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from . import config

logger = logging.getLogger(__name__)


def _today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def _date_to_path(archive_dir: Path, date_str: str) -> Path:
    return archive_dir / f"{date_str}.jsonl.gz"


class ArchiveMemory:
    def __init__(self, archive_dir: Path = config.ARCHIVE_DIR):
        self._dir = archive_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    # ── Write ────────────────────────────────────────────────────────────────

    def archive(self, memories: List[Dict], date_str: Optional[str] = None) -> int:
        """
        Append memories to today's (or specified date's) archive file.
        Embeddings are stripped to save space (not useful in cold storage).
        Returns count written.
        """
        if not memories:
            return 0
        date_str = date_str or _today_str()
        path = _date_to_path(self._dir, date_str)
        serialised = []
        for m in memories:
            d = {k: v for k, v in m.items() if k != "embedding"}
            d["archived_at"] = time.time()
            serialised.append(d)

        with self._lock:
            with gzip.open(str(path), "ab") as f:
                for record in serialised:
                    line = json.dumps(record, default=str) + "\n"
                    f.write(line.encode("utf-8"))

        logger.info("ArchiveMemory: archived %d records to %s", len(serialised), path.name)
        return len(serialised)

    def archive_one(self, memory: Dict, date_str: Optional[str] = None) -> None:
        self.archive([memory], date_str)

    # ── Read ─────────────────────────────────────────────────────────────────

    def recall(self, date_str: str) -> List[Dict]:
        """Load all records from a specific date's archive."""
        path = _date_to_path(self._dir, date_str)
        if not path.exists():
            logger.info("ArchiveMemory: no archive for %s", date_str)
            return []
        records = []
        with self._lock:
            with gzip.open(str(path), "rb") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            records.append(json.loads(line.decode("utf-8")))
                        except json.JSONDecodeError:
                            pass
        logger.info("ArchiveMemory: loaded %d records from %s", len(records), path.name)
        return records

    def list_dates(self) -> List[str]:
        """Return sorted list of archive dates available."""
        dates = []
        for p in sorted(self._dir.glob("*.jsonl.gz")):
            # p.stem would give "2026-03-12.jsonl" for double-extension files
            dates.append(p.name.replace(".jsonl.gz", ""))
        return dates

    def search(self, query: str, date_str: Optional[str] = None) -> List[Dict]:
        """
        Simple keyword search across archive(s).
        date_str=None → search all dates (slow for large archives).
        """
        query_lower = query.lower()
        dates = [date_str] if date_str else self.list_dates()
        results = []
        for d in dates:
            for record in self.recall(d):
                text = record.get("text", record.get("summary", ""))
                if query_lower in text.lower():
                    results.append(record)
        return results

    def size_bytes(self) -> int:
        total = 0
        for p in self._dir.glob("*.jsonl.gz"):
            total += p.stat().st_size
        return total

    def stats(self) -> Dict:
        dates = self.list_dates()
        return {
            "dates": len(dates),
            "oldest": dates[0] if dates else None,
            "newest": dates[-1] if dates else None,
            "size_bytes": self.size_bytes(),
        }
