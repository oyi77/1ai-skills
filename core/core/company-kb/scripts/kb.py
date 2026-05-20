#!/usr/bin/env python3
"""
Company Knowledge Base CLI
Commands: kb search <query>, kb read <path>, kb write <path> <content>
ChromaDB collection: company-knowledge at ~/.openclaw/chroma_db/
Files: ~/workspace/company-knowledge/
"""

import sys
import os
import json
from pathlib import Path

CHROMA_DB_PATH = os.path.expanduser("~/.openclaw/chroma_db")
KB_DIR = os.path.expanduser("~/.openclaw/workspace/company-knowledge")
COLLECTION_NAME = "company-knowledge"

# PARA structure for new files
PARA_DIRS = ["projects", "areas", "resources", "archives"]


def get_chroma_client():
    try:
        import chromadb

        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        return client
    except ImportError:
        print(
            "ERROR: chromadb not installed. Run: pip install chromadb", file=sys.stderr
        )
        sys.exit(1)


def cmd_search(query: str, n_results: int = 5):
    """Semantic search over company-knowledge ChromaDB collection."""
    if not query.strip():
        print("Usage: kb search <query>")
        sys.exit(1)

    client = get_chroma_client()
    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(
            f"ERROR: Could not get collection '{COLLECTION_NAME}': {e}", file=sys.stderr
        )
        sys.exit(1)

    count = collection.count()
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count) if count > 0 else 1,
        include=["documents", "metadatas", "distances"],
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not docs:
        print(f"No results found for: {query}")
        return

    print(f'Search: "{query}" — {len(docs)} result(s) from {count} chunks\n')
    for i, (doc, meta, dist) in enumerate(zip(docs, metas, distances), 1):
        score = round(1 - dist, 4) if dist is not None else "?"
        source = meta.get("source", meta.get("file", meta.get("path", "unknown")))
        print(f"[{i}] Score: {score} | Source: {source}")
        print(f"    {doc[:300].strip()}")
        if len(doc) > 300:
            print(f"    ... ({len(doc)} chars total)")
        print()


def cmd_read(path: str):
    """Read a file from company-knowledge/ directory."""
    if not path.strip():
        # List all files
        kb_path = Path(KB_DIR)
        if not kb_path.exists():
            print(f"company-knowledge/ directory is empty or does not exist: {KB_DIR}")
            return
        files = (
            list(kb_path.rglob("*.md"))
            + list(kb_path.rglob("*.txt"))
            + list(kb_path.rglob("*.json"))
        )
        if not files:
            print(f"No files found in {KB_DIR}")
            return
        print(f"Files in company-knowledge/ ({len(files)} total):")
        for f in sorted(files):
            rel = f.relative_to(kb_path)
            print(f"  {rel}")
        return

    # Resolve path relative to KB_DIR
    kb_path = Path(KB_DIR)
    target = kb_path / path
    # Security: ensure it stays within KB_DIR
    try:
        target.resolve().relative_to(kb_path.resolve())
    except ValueError:
        print(f"ERROR: Path '{path}' is outside company-knowledge/", file=sys.stderr)
        sys.exit(1)

    if not target.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    print(f"=== {path} ===\n")
    print(target.read_text(encoding="utf-8"))


def cmd_list():
    """List all files in company-knowledge/."""
    cmd_read("")


def cmd_write(path: str, content: str):
    """Write/update a knowledge file with proper PARA placement."""
    if not path.strip():
        print("Usage: kb write <path> <content>")
        sys.exit(1)

    kb_path = Path(KB_DIR)
    target = kb_path / path

    # Security: ensure it stays within KB_DIR
    try:
        target.resolve().relative_to(kb_path.resolve())
    except ValueError:
        print(f"ERROR: Path '{path}' is outside company-knowledge/", file=sys.stderr)
        sys.exit(1)

    # Warn if not in PARA structure
    parts = Path(path).parts
    if parts[0] not in PARA_DIRS:
        print(f"NOTE: Consider placing under a PARA folder: {PARA_DIRS}")
        print(f"      e.g. kb write resources/{path} ...")

    # Create parent dirs
    target.parent.mkdir(parents=True, exist_ok=True)

    existing = target.exists()
    target.write_text(content, encoding="utf-8")

    action = "Updated" if existing else "Created"
    print(f"{action}: company-knowledge/{path} ({len(content)} chars)")


def main():
    args = sys.argv[1:]

    if not args:
        print("Usage:")
        print("  kb search <query>         Semantic search (ChromaDB)")
        print("  kb read [path]            Read file or list all files")
        print("  kb list                   List all knowledge files")
        print("  kb write <path> <content> Create/update a knowledge file")
        sys.exit(0)

    cmd = args[0].lower()

    if cmd == "search":
        query = " ".join(args[1:])
        cmd_search(query)
    elif cmd == "read":
        path = args[1] if len(args) > 1 else ""
        cmd_read(path)
    elif cmd == "list":
        cmd_list()
    elif cmd == "write":
        if len(args) < 3:
            print("Usage: kb write <path> <content>")
            sys.exit(1)
        path = args[1]
        content = " ".join(args[2:])
        cmd_write(path, content)
    else:
        print(f"Unknown command: {cmd}")
        print("Commands: search, read, list, write")
        sys.exit(1)


if __name__ == "__main__":
    main()
