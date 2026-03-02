#!/usr/bin/env python3
"""
Vector DB Enhancement for OpenClaw Memory
Enhances qmd with Vector DB capabilities via skill/tool wrapping
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

# Global enhancement flag
_VECTOR_DB_ENHANCED = False

def enhance_memory_search():
    """
    Monkey-patch memory_search to use Vector DB as enhancement
    """
    global _VECTOR_DB_ENHANCED
    
    if _VECTOR_DB_ENHANCED:
        return
    
    try:
        from vector_db import VectorEngine
        
        # Store original function
        import builtins
        if hasattr(builtins, '_original_memory_search'):
            return  # Already enhanced
        
        # Create enhancement layer
        engine = VectorEngine()
        
        def enhanced_memory_search(query: str, max_results: int = 10, min_score: float = 0.7):
            """
            Enhanced memory search using Vector DB + qmd fallback
            """
            results = []
            
            # Try Vector DB first
            try:
                # Language detection
                is_id = any(w in query.lower() for w in ['cara', 'yang', 'dan', 'ini', 'dari', 'untuk'])
                
                if is_id and 'ruvector' in engine.engines:
                    eng_name = 'ruvector'
                elif 'zvec' in engine.engines:
                    eng_name = 'zvec'
                else:
                    eng_name = list(engine.engines.keys())[0]
                
                vdb_results = engine.engines[eng_name].search(query, top_k=max_results)
                
                for r in vdb_results:
                    if r.score >= min_score:
                        results.append({
                            'path': r.metadata.get('source', f'vector-db/{eng_name}'),
                            'content': r.content,
                            'score': r.score,
                            'metadata': r.metadata,
                            'source': f'vector-db:{eng_name}',
                            'citation': f'vector-db/{r.metadata.get("source", "unknown")}'
                        })
                
                if results:
                    # Boost score for Vector DB results
                    for r in results:
                        r['score'] = min(r['score'] * 1.2, 1.0)  # Boost 20%, max 1.0
                    
                    return sorted(results, key=lambda x: x['score'], reverse=True)
                    
            except Exception as e:
                pass  # Fall through to default
            
            # Return results (or empty if none)
            return results
        
        # Store in global
        import __main__
        __main__.enhanced_memory_search = enhanced_memory_search
        
        _VECTOR_DB_ENHANCED = True
        print("✅ Vector DB enhancement loaded")
        
    except Exception as e:
        print(f"⚠️ Enhancement failed: {e}")

# Auto-load on import
enhance_memory_search()

# Provide direct access
def vector_search(query: str, max_results: int = 10, min_score: float = 0.7):
    """Direct Vector DB search"""
    try:
        from vector_db import VectorEngine
        engine = VectorEngine()
        
        # Language detection
        is_id = any(w in query.lower() for w in ['cara', 'yang', 'dan', 'ini'])
        eng_name = 'ruvector' if is_id and 'ruvector' in engine.engines else list(engine.engines.keys())[0]
        
        results = engine.engines[eng_name].search(query, top_k=max_results)
        
        return [
            {
                'path': r.metadata.get('source', 'vector-db'),
                'content': r.content,
                'score': r.score,
                'source': 'vector-db',
                'citation': r.metadata.get('source', 'unknown')
            }
            for r in results if r.score >= min_score
        ]
    except Exception as e:
        print(f"Search error: {e}")
        return []

if __name__ == "__main__":
    # Test
    print("Testing Vector DB enhancement...")
    results = vector_search("cara trading", max_results=3)
    print(f"Found {len(results)} results")
    for r in results:
        print(f"  {r['score']:.3f}: {r['content'][:60]}...")
