#!/usr/bin/env python3
"""
Vector DB - Simple Query Tool
Usage: query_vector.py "your query here"
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')

from vector_db import VectorEngine

def search(query: str):
    """Fast vector search"""
    engine = VectorEngine()
    
    # Detect Indonesian
    is_indonesian = any(w in query.lower() for w in ['cara', 'yang', 'dan', 'ini', 'dari', 'untuk', 'dengan', 'apa', 'bagaimana'])
    
    available = list(engine.engines.keys())
    if not available:
        print("❌ No engines available")
        return []
    
    # Choose best engine
    if is_indonesian and 'ruvector' in available:
        eng_name = 'ruvector'
    else:
        eng_name = available[0]
    
    # Search
    try:
        results = engine.engines[eng_name].search(query, top_k=5)
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: query_vector.py 'your search query'")
        sys.exit(1)
    
    query = sys.argv[1]
    print(f"Searching: '{query}'")
    print("-" * 50)
    
    results = search(query)
    
    if results:
        for i, r in enumerate(results, 1):
            print(f"\n{i}. Score: {r.score:.3f}")
            print(f"   {r.content[:120]}...")
    else:
        print("No results found")
        print("(Vector DB may be empty - run AUTO_INDEX.py first)")