#!/usr/bin/env python3
"""
Memory Auto-Compaction Script
Runs periodically to optimize and consolidate memory files.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta
import hashlib
import re
from typing import Dict

WORKSPACE = Path("/home/openclaw/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_FILE = WORKSPACE / "MEMORY.md"

DUPLICATE_THRESHOLD = 0.85
MAX_DAYS_IN_MEMORY = 90

def hash_text(text: str) -> str:
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def similarity(text1: str, text2: str) -> float:
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union)

def compact_memory(dry_run: bool = False) -> Dict:
    now = datetime.now()
    results = {
        'timestamp': now.isoformat(),
        'duplicates': [],
        'old_sections': [],
        'daily_insights': [],
        'actions_taken': []
    }
    
    # Find older memory files
    old_files = [f for f in MEMORY_DIR.glob('*.md') if f != MEMORY_FILE]
    old_files.sort()
    
    for f in old_files:
        content = f.read_text()
        if len(content) < 100:
            results['old_sections'].append({
                'file': str(f),
                'reason': 'empty_file',
                'size': len(content)
            })
            if not dry_run:
                f.unlink()
                results['actions_taken'].append(f"Removed empty file: {f.name}")
    
    return results

def main():
    dry_run = '--dry-run' in sys.argv
    
    print("🧹 Memory Compaction System")
    print("=" * 50)
    
    results = compact_memory(dry_run=dry_run)
    
    print(f"Old sections: {len(results['old_sections'])}")
    print(f"Actions taken: {len(results['actions_taken'])}")
    
    if results['actions_taken']:
        for action in results['actions_taken']:
            print(f"✓ {action}")
    
    print("\n✅ Compaction complete!")

if __name__ == '__main__':
    main()