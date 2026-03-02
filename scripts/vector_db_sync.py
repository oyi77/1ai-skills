#!/usr/bin/env python3
"""
Vector DB Memory Sync - Heartbeat Integration
Automatically syncs new memory files to Vector DB
Run this via HEARTBEAT.md or cron every 30 minutes
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

LOG_FILE = '/home/openclaw/.openclaw/workspace/.vector_db_sync.log'
STATE_FILE = '/home/openclaw/.openclaw/workspace/.vector_db_sync_state.json'

def log(message):
    """Write to log file"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")
    print(message)

def get_indexed_files():
    """Get list of already indexed files"""
    if os.path.exists(STATE_FILE):
        import json
        with open(STATE_FILE, 'r') as f:
            return json.load(f).get('indexed', [])
    return []

def save_indexed_state(files):
    """Save which files have been indexed"""
    import json
    with open(STATE_FILE, 'w') as f:
        json.dump({'indexed': files, 'last_sync': datetime.now().isoformat()}, f)

def main():
    """Main sync function"""
    log("=" * 60)
    log("🔄 Vector DB Memory Sync Started")
    log("=" * 60)
    
    try:
        from vector_db import VectorEngine
        engine = VectorEngine()
        log(f"✅ Engine initialized: {list(engine.engines.keys())}")
    except Exception as e:
        log(f"❌ Failed to initialize engine: {e}")
        return
    
    indexed_files = get_indexed_files()
    new_files = []
    
    # Check memory directory
    memory_dir = '/home/openclaw/.openclaw/workspace/memory'
    if os.path.exists(memory_dir):
        files = [f for f in os.listdir(memory_dir) if f.endswith('.md')]
        log(f"📁 Found {len(files)} memory files")
        
        for filename in files:
            filepath = os.path.join(memory_dir, filename)
            
            # Skip if already indexed
            if filepath in indexed_files:
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if len(content) > 100:
                    doc_id = engine.index_document(
                        content,
                        {'title': f'Memory: {filename}', 'source': filepath}
                    )
                    new_files.append(filepath)
                    log(f"   ✅ Indexed: {filename} ({len(content):,} chars)")
            except Exception as e:
                log(f"   ❌ Failed: {filename} - {e}")
    
    # Check main memory files
    main_files = [
        ('MEMORY.md', 'Strategic Intelligence'),
        ('SOUL.md', 'Soul Configuration'),
        ('USER.md', 'User Profile'),
    ]
    
    for filename, title in main_files:
        filepath = f'/home/openclaw/.openclaw/workspace/{filename}'
        
        if filepath in indexed_files:
            continue
        
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                doc_id = engine.index_document(
                    content,
                    {'title': title, 'source': filename}
                )
                new_files.append(filepath)
                log(f"   ✅ Indexed: {filename}")
        except Exception as e:
            log(f"   ❌ Failed: {filename} - {e}")
    
    # Update state
    indexed_files.extend(new_files)
    save_indexed_state(indexed_files)
    
    log(f"\n📊 Summary: {len(new_files)} new files indexed")
    log(f"📁 Total indexed: {len(indexed_files)} files")
    log("=" * 60)

if __name__ == "__main__":
    main()