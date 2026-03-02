#!/usr/bin/env python3
"""
Vector DB Tools - Auto-registered for OpenClaw
These tools are automatically available in all sessions
"""

import sys
sys.path.insert(0, '/home/openclaw/.openclaw/plugins')

# Initialize on import
_VECTOR_ENGINE = None

def _get_engine():
    """Lazy initialization of Vector Engine"""
    global _VECTOR_ENGINE
    if _VECTOR_ENGINE is None:
        try:
            from vector_db import VectorEngine
            _VECTOR_ENGINE = VectorEngine()
        except Exception as e:
            print(f"⚠️ Vector DB not available: {e}")
            return None
    return _VECTOR_ENGINE

# Tool 1: Semantic Search
def vector_search(query: str, top_k: int = 5) -> list:
    """
    Search documents using Vector DB semantic similarity.
    
    Args:
        query: Search query text
        top_k: Number of results to return (default: 5)
    
    Returns:
        List of search results with relevance scores
    """
    engine = _get_engine()
    if not engine:
        return []
    
    try:
        # Detect Indonesian
        is_id = any(w in query.lower() for w in ['cara', 'yang', 'dan', 'ini', 'dari', 'untuk', 'apa', 'bagaimana', 'mengapa'])
        
        # Choose engine
        if is_id and 'ruvector' in engine.engines:
            eng_name = 'ruvector'
        elif 'zvec' in engine.engines:
            eng_name = 'zvec'
        else:
            eng_name = list(engine.engines.keys())[0]
        
        results = engine.engines[eng_name].search(query, top_k=top_k)
        
        return [
            {
                'content': r.content,
                'score': r.score,
                'source': r.metadata.get('source', 'unknown'),
                'engine': eng_name
            }
            for r in results
        ]
    except Exception as e:
        return []

# Tool 2: Index Document
def vector_index(content: str, title: str = "", source: str = "") -> str:
    """
    Index a document to Vector DB for future search.
    
    Args:
        content: Document content to index
        title: Document title
        source: Source identifier (filename, etc.)
    
    Returns:
        Document ID string
    """
    engine = _get_engine()
    if not engine:
        return ""
    
    try:
        doc_id = engine.index_document(content, {'title': title, 'source': source})
        return doc_id
    except Exception as e:
        return ""

# Tool 3: Smart Chunk
def vector_chunk(text: str, max_tokens: int = 500) -> list:
    """
    Split text into semantic chunks.
    
    Args:
        text: Input text to chunk
        max_tokens: Maximum tokens per chunk (default: 500)
    
    Returns:
        List of text chunks
    """
    engine = _get_engine()
    if not engine:
        return [text]
    
    try:
        from vector_db.shared.engine import smart_chunk
        return smart_chunk(text, max_tokens)
    except:
        return [text]

# Tool 4: Detect Language
def vector_detect_language(text: str) -> str:
    """
    Detect language of text (id/en/mixed).
    
    Args:
        text: Input text
    
    Returns:
        Language code: 'id', 'en', or 'mixed'
    """
    engine = _get_engine()
    if not engine or 'ruvector' not in engine.engines:
        # Simple detection
        indo_words = ['yang', 'dan', 'di', 'untuk', 'dengan', 'ini', 'adalah', 'saya', 'kamu']
        text_lower = text.lower()
        indo_count = sum(1 for w in indo_words if w in text_lower)
        return 'id' if indo_count >= 2 else 'en'
    
    try:
        return engine.engines['ruvector'].detect_language(text)
    except:
        return 'unknown'

# Tool 5: Get Status
def vector_status() -> dict:
    """
    Get Vector DB status.
    
    Returns:
        Dict with engine status and document counts
    """
    engine = _get_engine()
    if not engine:
        return {'error': 'Vector DB not available'}
    
    return {
        'engines': list(engine.engines.keys()),
        'active': engine.active_engine,
        'status': 'ready'
    }

# Make tools available globally
__all__ = [
    'vector_search',
    'vector_index', 
    'vector_chunk',
    'vector_detect_language',
    'vector_status'
]

# Auto-execute on import if run directly
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print("Testing Vector DB Tools...")
        results = vector_search("cara optimasi", top_k=2)
        print(f"Found {len(results)} results")
        for r in results:
            print(f"  {r['score']:.3f}: {r['content'][:60]}...")
