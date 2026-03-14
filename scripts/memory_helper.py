#!/usr/bin/env python3
"""
Memory System Helper - Search, Index, and Maintain Memory Files

Usage:
  python3 memory_helper.py search <keyword>
  python3 memory_helper.py index
  python3 memory_helper.py check
  python3 memory_helper.py consolidate
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = BASE_DIR / "memory"
NOTES_DIR = BASE_DIR / "notes"
SKILLS_DIR = BASE_DIR / "skills"

def search_keyword(keyword):
    """Search all memory files for keyword"""
    keyword_lower = keyword.lower()

    print(f"🔍 Searching for: '{keyword}'")
    print("=" * 70)

    results = []

    # Search in memory/
    for file in MEMORY_DIR.glob("**/*.md"):
        try:
            with open(file) as f:
                content = f.read()
                if keyword_lower in content.lower():
                    results.append({
                        'file': str(file.relative_to(BASE_DIR)),
                        'matches': content.lower().count(keyword_lower)
                    })
        except Exception as e:
            print(f"⚠️  Error reading {file}: {e}")

    # Search in notes/
    for file in NOTES_DIR.glob("**/*.md"):
        try:
            with open(file) as f:
                content = f.read()
                if keyword_lower in content.lower():
                    results.append({
                        'file': str(file.relative_to(BASE_DIR)),
                        'matches': content.lower().count(keyword_lower)
                    })
        except Exception as e:
            print(f"⚠️  Error reading {file}: {e}")

    # Display results
    if results:
        results.sort(key=lambda x: x['matches'], reverse=True)

        for result in results[:10]:  # Top 10 results
            print(f"\n📄 {result['file']}")
            print(f"   Matches: {result['matches']}")
            print(f"   Path: {BASE_DIR / result['file']}")
    else:
        print(f"\n❌ No results found for '{keyword}'")
        print(f"\n💡 Suggest creating a new memory entry or checking INDEX.md")

    print("\n" + "=" * 70)

def update_index():
    """Update INDEX.md with current file list"""
    print("📝 Updating INDEX.md...")
    print("=" * 70)

    index_file = MEMORY_DIR / "INDEX.md"

    # Collect all memory files
    memory_files = list(MEMORY_DIR.glob("*.md"))
    notes_files = list(NOTES_DIR.glob("*.md"))

    print(f"\n📁 Memory files: {len(memory_files)}")
    print(f"📁 Notes files: {len(notes_files)}")

    print("\n✅ Review INDEX.md for current lessons")
    print(f"   Location: {index_file}")
    print("\n💡 To add new entries:")
    print("   1. Read INDEX.md")
    print("   2. Find relevant section")
    print("   3. Add lesson")
    print("   4. Save file")

    print("\n" + "=" * 70)

def check_status():
    """Check memory system status"""
    print("📊 Memory System Status Check")
    print("=" * 70)

    # Check INDEX.md
    index_file = MEMORY_DIR / "INDEX.md"
    if index_file.exists():
        print(f"✅ INDEX.md exists ({index_file.stat().st_size:,} bytes)")
    else:
        print("❌ INDEX.md NOT FOUND - Create it!")

    # Check critical notes
    critical_notes = [
        "open-loops.md",
        "browser-tool-critical-gotchas.md"
    ]

    print("\n🔍 Critical Notes:")
    for note in critical_notes:
        note_file = NOTES_DIR / note
        if note_file.exists():
            age_days = (datetime.now() - datetime.fromtimestamp(note_file.stat().st_mtime)).days
            print(f"   ✅ {note} ({age_days} days old)")
        else:
            print(f"   ❌ {note} NOT FOUND")

    # Check today's memory
    today = datetime.now().strftime("%Y-%m-%d")
    today_memory = MEMORY_DIR / f"{today}.md"

    print(f"\n📅 Today's Memory ({today}):")
    if today_memory.exists():
        print(f"   ✅ Exists")
        size = today_memory.stat().st_size
        lines = len(today_memory.read_text().splitlines())
        print(f"   Size: {size:,} bytes, {lines} lines")
    else:
        print(f"   ❌ NOT FOUND - Create for today's work")

    print("\n" + "=" * 70)

def list_lessons():
    """List all critical lessons from notes/"""
    print("📚 Critical Lessons Index")
    print("=" * 70)

    if NOTES_DIR.exists():
        for file in sorted(NOTES_DIR.glob("*.md")):
            print(f"\n📄 {file.name}")
            print(f"   Path: {file}")

            # Try to get first paragraph (summary)
            try:
                content = file.read_text()
                lines = content.split('\n')

                # Find first non-header line
                for line in lines:
                    if line and not line.startswith('#'):
                        print(f"   Summary: {line[:80]}...")
                        break
            except Exception as e:
                print(f"   Error: {e}")

    else:
        print("❌ notes/ directory not found")

    print("\n" + "=" * 70)

def main():
    """Main CLI"""
    if len(sys.argv) < 2:
        print("🔧 Memory System Helper")
        print("\nUsage:")
        print("  search <keyword>     Search all memory files")
        print("  index               Check index status")
        print("  check               Check system status")
        print("  lessons             List all critical lessons")
        print("\nExamples:")
        print("  python3 memory_helper.py search browser")
        print("  python3 memory_helper.py lessons")
        return

    command = sys.argv[1].lower()

    if command == "search":
        if len(sys.argv) < 3:
            print("❌ Please provide a search keyword")
            return
        search_keyword(sys.argv[2])

    elif command == "index":
        update_index()

    elif command == "check":
        check_status()

    elif command == "lessons":
        list_lessons()

    else:
        print(f"❌ Unknown command: {command}")
        print("Use: search, index, check, or lessons")

if __name__ == "__main__":
    main()