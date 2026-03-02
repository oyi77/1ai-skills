# Vector DB Auto-Loader for OpenClaw Sessions
# Add to HEARTBEAT.md or startup

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace/tools')

try:
    from vector_db_tools import (
        vector_search,
        vector_index, 
        vector_chunk,
        vector_detect_language,
        vector_status
    )
    
    # Make available globally
    import builtins
    builtins.vector_search = vector_search
    builtins.vector_index = vector_index
    builtins.vector_chunk = vector_chunk
    builtins.vector_detect_language = vector_detect_language
    builtins.vector_status = vector_status
    
    print("✅ Vector DB tools auto-loaded:")
    print("   vector_search(query, top_k=5)")
    print("   vector_index(content, title, source)")
    print("   vector_chunk(text, max_tokens=500)")
    
except Exception as e:
    print(f"⚠️ Could not auto-load Vector DB tools: {e}")
