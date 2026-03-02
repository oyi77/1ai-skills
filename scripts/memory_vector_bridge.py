#!/usr/bin/env python3
"""
Memory Vector DB Bridge
Integrates OpenClaw's memory_search with Vector DB Plugin
This acts as an enhancement layer on top of qmd
"""

import sys
import os

sys.path.insert(0, '/home/openclaw/.openclaw/plugins')
sys.path.insert(0, '/home/openclaw/.openclaw/workspace')

# Import Vector DB
try:
    from vector_db import VectorEngine
    VECTOR_DB_AVAILABLE = True
except ImportError:
    VECTOR_DB_AVAILABLE = False
    print("⚠️ Vector DB not available")

class MemoryVectorBridge:
    """Bridge between OpenClaw memory and Vector DB"""
    
    def __init__(self):
        self.engine = None
        self.qmd_fallback = True
        
        if VECTOR_DB_AVAILABLE:
            try:
                self.engine = VectorEngine()
                print(f"✅ Vector DB Bridge initialized: {list(self.engine.engines.keys())}")
            except Exception as e:
                print(f"⚠️ Vector DB init failed: {e}")
    
    def search(self, query, max_results=10, min_score=0.7):
        """
        Enhanced memory search using Vector DB + qmd fallback
        """
        results = []
        
        # Try Vector DB first
        if self.engine and self.engine.engines:
            try:
                # Detect language
                is_id = any(w in query.lower() for w in ['cara', 'yang', 'dan', 'ini', 'dari', 'untuk'])
                
                # Choose engine
                if is_id and 'ruvector' in self.engine.engines:
                    eng_name = 'ruvector'
                else:
                    eng_name = list(self.engine.engines.keys())[0]
                
                # Search
                vector_results = self.engine.engines[eng_name].search(query, top_k=max_results)
                
                # Convert to OpenClaw format
                for r in vector_results:
                    if r.score >= min_score:
                        results.append({
                            'content': r.content,
                            'score': r.score,
                            'source': r.metadata.get('source', 'vector-db'),
                            'path': r.metadata.get('source', 'unknown'),
                            'citation': f"vector-db:{eng_name}"
                        })
                
                if results:
                    print(f"✅ Vector DB found {len(results)} results")
                    return results
                    
            except Exception as e:
                print(f"⚠️ Vector DB search failed: {e}")
        
        # Fallback to qmd (OpenClaw's built-in)
        if self.qmd_fallback:
            print("📄 Falling back to qmd...")
            # Return empty - actual qmd call will be made by OpenClaw
            return []
        
        return results

# Global instance
_bridge = None

def get_bridge():
    """Get or create bridge instance"""
    global _bridge
    if _bridge is None:
        _bridge = MemoryVectorBridge()
    return _bridge

def enhanced_memory_search(query, max_results=10, min_score=0.7):
    """
    Drop-in replacement for memory_search
    Usage: from memory_vector_bridge import enhanced_memory_search
    """
    bridge = get_bridge()
    return bridge.search(query, max_results, min_score)

# Hook for OpenClaw
def memory_search_hook(query, max_results=10, min_score=0.7):
    """Hook to be called by OpenClaw"""
    return enhanced_memory_search(query, max_results, min_score)

if __name__ == "__main__":
    # Test
    print("=" * 60)
    print("Memory Vector DB Bridge - Test")
    print("=" * 60)
    
    results = enhanced_memory_search("cara optimasi iklan", max_results=3, min_score=0.5)
    
    print(f"\nResults: {len(results)}")
    for r in results[:3]:
        print(f"\nScore: {r['score']:.3f}")
        print(f"Content: {r['content'][:100]}...")