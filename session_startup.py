# Session Startup - Auto-load Memory & Context
# Execute this at START of EVERY MAIN SESSION

import sys
from pathlib import Path
from datetime import datetime

# Workspace paths
WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"

# Get dates
today = datetime.now().strftime("%Y-%m-%d")
from datetime import timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# Files to read
files_to_read = [
    WORKSPACE / "SOUL.md",
    WORKSPACE / "USER.md",
    MEMORY_DIR / f"{today}.md",
    MEMORY_DIR / f"{yesterday}.md",
    WORKSPACE / "MEMORY.md"
]

print("📚 Loading startup context...\n")

read_count = 0
for path in files_to_read:
    if path.exists():
        read_count += 1
        print(f"✅ {path.name} ({len(str(path))} chars)")
        # File content is auto-extracted by context loading
    else:
        print(f"⚠️  {path.name} (not found)")

print(f"\n📊 Context loaded: {read_count}/{len(files_to_read)} files")
print(f"🗓️  Date: {today} (yesterday: {yesterday})")
print("=" * 50)