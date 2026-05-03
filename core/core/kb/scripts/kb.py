#!/usr/bin/env python3
"""
kb.py — BerkahKarya Knowledge Base CLI
Provides semantic search, file read, and file write access to company-knowledge/.

Usage:
  kb search <query> [--limit N]
  kb read <path>
  kb write <path> <content>
  kb list [subpath]
"""

import sys
import os
import json
import argparse
from pathlib import Path

CHROMA_DB_PATH = os.path.expanduser("~/.openclaw/chroma_db")
COLLECTION_NAME = "company-knowledge"
KNOWLEDGE_DIR = Path(__file__).parent.parent.parent.parent.parent / "company-knowledge"
# Fallback: use absolute path
KNOWLEDGE_DIR_ABS = Path(os.path.expanduser("~/.openclaw/workspace/company-knowledge"))


def get_knowledge_dir() -> Path:
    """Return the company-knowledge directory."""
    if KNOWLEDGE_DIR.exists():
        return KNOWLEDGE_DIR
    return KNOWLEDGE_DIR_ABS


def cmd_search(query: str, limit: int = 5) -> None:
    """Semantic search via ChromaDB company-knowledge collection."""
    try:
        import chromadb
    except ImportError:
        print("ERROR: chromadb not installed. Run: pip install chromadb", file=sys.stderr)
        sys.exit(1)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    try:
        coll = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"ERROR: Could not open collection '{COLLECTION_NAME}': {e}", file=sys.stderr)
        sys.exit(1)

    results = coll.query(
        query_texts=[query],
        n_results=min(limit, coll.count()),
        include=["documents", "metadatas", "distances"],
    )

    ids = results["ids"][0]
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    if not ids:
        print("No results found.")
        return

    print(f"Search results for: \"{query}\"\n")
    for i, (doc_id, doc, meta, dist) in enumerate(zip(ids, docs, metas, dists), 1):
        score = round(1 - dist, 4)  # convert distance to similarity
        file_path = meta.get("file_path", "unknown")
        section = meta.get("section", "")
        print(f"[{i}] {file_path}" + (f" — {section}" if section else ""))
        print(f"     Score: {score}")
        # Print snippet (first 300 chars)
        snippet = doc[:300].replace("\n", " ").strip()
        if len(doc) > 300:
            snippet += "..."
        print(f"     {snippet}")
        print()


def cmd_read(path: str) -> None:
    """Read a file from company-knowledge/."""
    kb_dir = get_knowledge_dir()
    # Normalise path — strip leading slashes
    clean_path = path.lstrip("/")
    full_path = kb_dir / clean_path

    if not full_path.exists():
        # Try to read from ChromaDB as fallback
        print(f"File not found on disk: {full_path}", file=sys.stderr)
        print("Falling back to ChromaDB chunks...\n")
        _read_from_chroma(clean_path)
        return

    if full_path.is_dir():
        print(f"Error: '{path}' is a directory. Use 'kb list {path}' instead.", file=sys.stderr)
        sys.exit(1)

    content = full_path.read_text(encoding="utf-8")
    print(content)


def _read_from_chroma(file_path: str) -> None:
    """Read all chunks for a file_path from ChromaDB."""
    try:
        import chromadb
    except ImportError:
        print("ERROR: chromadb not installed.", file=sys.stderr)
        sys.exit(1)

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    try:
        coll = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        print(f"ERROR: Could not open collection '{COLLECTION_NAME}': {e}", file=sys.stderr)
        sys.exit(1)

    results = coll.get(
        where={"file_path": file_path},
        include=["documents", "metadatas"],
    )

    if not results["ids"]:
        print(f"No content found for path: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Sort chunks by chunk_index
    chunks = sorted(
        zip(results["metadatas"], results["documents"]),
        key=lambda x: x[0].get("chunk_index", 0),
    )

    print(f"# {file_path} (from ChromaDB index)\n")
    for meta, doc in chunks:
        print(doc)


def cmd_write(path: str, content: str) -> None:
    """Write/update a file in company-knowledge/ with PARA structure enforcement."""
    kb_dir = get_knowledge_dir()
    kb_dir.mkdir(parents=True, exist_ok=True)

    clean_path = path.lstrip("/")

    # Validate PARA placement (warn if not under a known PARA category)
    para_roots = {"projects", "areas", "resources", "archives"}
    top_level = clean_path.split("/")[0]
    if top_level not in para_roots and clean_path != "README.md":
        print(f"WARNING: Path '{clean_path}' is not under a PARA category (projects/areas/resources/archives).")
        print("Consider placing files under: areas/<topic>/, resources/<topic>/, projects/<name>/")
        print()

    full_path = kb_dir / clean_path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    existed = full_path.exists()
    full_path.write_text(content, encoding="utf-8")

    action = "Updated" if existed else "Created"
    print(f"{action}: {full_path}")
    print(f"Size: {len(content)} bytes")
    print()
    print("Note: Re-run the ChromaDB indexer (BER-50) to make this file searchable.")


def cmd_list(subpath: str = "") -> None:
    """List files in company-knowledge/ or a subpath."""
    kb_dir = get_knowledge_dir()
    target = kb_dir / subpath.lstrip("/") if subpath else kb_dir

    if not target.exists():
        # Fall back to listing paths from ChromaDB
        print(f"Directory not found on disk: {target}")
        print("Showing indexed paths from ChromaDB:\n")
        _list_from_chroma(subpath)
        return

    print(f"Contents of company-knowledge/{subpath}:\n")
    for item in sorted(target.rglob("*")):
        if item.is_file():
            rel = item.relative_to(kb_dir)
            size = item.stat().st_size
            print(f"  {rel}  ({size} bytes)")

    if not any(target.rglob("*")):
        print("  (empty)")
        print("\nShowing indexed paths from ChromaDB:\n")
        _list_from_chroma(subpath)


def _list_from_chroma(prefix: str = "") -> None:
    """List unique file paths from ChromaDB."""
    try:
        import chromadb
    except ImportError:
        print("ERROR: chromadb not installed.", file=sys.stderr)
        return

    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    try:
        coll = client.get_collection(COLLECTION_NAME)
    except Exception:
        return

    results = coll.get(include=["metadatas"])
    paths = set()
    for m in results["metadatas"]:
        fp = m.get("file_path", "")
        if fp and (not prefix or fp.startswith(prefix.lstrip("/"))):
            paths.add(fp)

    for p in sorted(paths):
        print(f"  {p}")
    print(f"\nTotal: {len(paths)} files indexed in ChromaDB")


def main():
    parser = argparse.ArgumentParser(
        prog="kb",
        description="BerkahKarya Knowledge Base — read, search, write company-knowledge/",
    )
    subparsers = parser.add_subparsers(dest="command")

    # kb search
    p_search = subparsers.add_parser("search", help="Semantic search via ChromaDB")
    p_search.add_argument("query", nargs="+", help="Search query")
    p_search.add_argument("--limit", "-n", type=int, default=5, help="Max results (default: 5)")

    # kb read
    p_read = subparsers.add_parser("read", help="Read a file from company-knowledge/")
    p_read.add_argument("path", help="Relative path within company-knowledge/")

    # kb write
    p_write = subparsers.add_parser("write", help="Write/update a file in company-knowledge/")
    p_write.add_argument("path", help="Relative path within company-knowledge/")
    p_write.add_argument("content", help="File content (use '-' to read from stdin)")

    # kb list
    p_list = subparsers.add_parser("list", help="List files in company-knowledge/")
    p_list.add_argument("subpath", nargs="?", default="", help="Optional subdirectory")

    args = parser.parse_args()

    if args.command == "search":
        query = " ".join(args.query)
        cmd_search(query, limit=args.limit)

    elif args.command == "read":
        cmd_read(args.path)

    elif args.command == "write":
        if args.content == "-":
            content = sys.stdin.read()
        else:
            content = args.content
        cmd_write(args.path, content)

    elif args.command == "list":
        cmd_list(args.subpath)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
