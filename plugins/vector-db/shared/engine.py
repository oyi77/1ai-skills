#!/usr/bin/env python3
"""
Vector DB Plugin - Shared Engine for OpenClaw
Unified interface for ZVec, PageIndex, and Ruvector
"""

import os
import sys
import json
import hashlib
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import re

@dataclass
class SearchResult:
    content: str
    score: float
    metadata: Dict
    source: str

class VectorEngine:
    """Unified vector database engine"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.active_engine = self.config.get('defaultEngine', 'zvec')
        self.cache_dir = os.path.expanduser('~/.openclaw/vector-cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Initialize engines
        self.engines = {}
        self._init_engines()
    
    def _load_config(self, path: Optional[str]) -> Dict:
        """Load plugin configuration"""
        if path and os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        
        # Default config
        return {
            'defaultEngine': 'zvec',
            'chunkSize': 500,
            'maxTokens': 8192,
            'cacheEnabled': True,
            'zvec': {'enabled': True, 'model': 'BAAI/bge-m3'},
            'pageindex': {'enabled': True, 'useGoogleAuth': False},
            'ruvector': {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
        }
    
    def _init_engines(self):
        """Initialize available engines"""
        # Get plugin directory for imports
        plugin_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if plugin_dir not in sys.path:
            sys.path.insert(0, plugin_dir)
        
        # ZVec-style engine (using ChromaDB)
        if self.config.get('zvec', {}).get('enabled', True):
            try:
                from plugins.vector_db.zvec.engine import ZVecEngine
                self.engines['zvec'] = ZVecEngine(self.config['zvec'])
            except ImportError as e:
                try:
                    from zvec.engine import ZVecEngine
                    self.engines['zvec'] = ZVecEngine(self.config['zvec'])
                except ImportError as e2:
                    print(f"⚠️  ZVec not available: {e}, {e2}")
        
        # PageIndex-style engine
        if self.config.get('pageindex', {}).get('enabled', True):
            try:
                from plugins.vector_db.pageindex.engine import PageIndexEngine
                self.engines['pageindex'] = PageIndexEngine(self.config['pageindex'])
            except ImportError as e:
                try:
                    from pageindex.engine import PageIndexEngine
                    self.engines['pageindex'] = PageIndexEngine(self.config['pageindex'])
                except ImportError as e2:
                    print(f"⚠️  PageIndex not available: {e}, {e2}")
        
        # Ruvector-style engine
        if self.config.get('ruvector', {}).get('enabled', True):
            try:
                from plugins.vector_db.ruvector.engine import RuvectorEngine
                self.engines['ruvector'] = RuvectorEngine(self.config['ruvector'])
            except ImportError as e:
                try:
                    from ruvector.engine import RuvectorEngine
                    self.engines['ruvector'] = RuvectorEngine(self.config['ruvector'])
                except ImportError as e2:
                    print(f"⚠️  Ruvector not available: {e}, {e2}")
    
    def search(self, query: str, top_k: int = 5, 
               engine: Optional[str] = None) -> List[SearchResult]:
        """
        Semantic search across vector databases
        """
        engine = engine or self.active_engine
        
        if engine not in self.engines:
            # Fallback to available engine
            engine = list(self.engines.keys())[0] if self.engines else None
            if not engine:
                return []
        
        return self.engines[engine].search(query, top_k)
    
    def index_document(self, content: str, metadata: Dict = None,
                       doc_id: Optional[str] = None) -> str:
        """
        Index a document for semantic search
        """
        # Smart chunking first
        chunks = smart_chunk(content, self.config.get('chunkSize', 500))
        
        # Index in all available engines
        doc_id = doc_id or hashlib.md5(content.encode()).hexdigest()
        
        for name, engine in self.engines.items():
            try:
                engine.index_chunks(chunks, doc_id, metadata)
            except Exception as e:
                print(f"⚠️  Failed to index in {name}: {e}")
        
        return doc_id
    
    def enhance_memory_search(self, query: str, max_results: int = 10,
                              min_score: float = 0.7) -> List[Dict]:
        """
        Hook for memory_search enhancement
        """
        results = self.search(query, top_k=max_results)
        
        # Filter by score
        filtered = [r for r in results if r.score >= min_score]
        
        # Convert to memory format
        return [
            {
                'content': r.content,
                'score': r.score,
                'source': r.source,
                'metadata': r.metadata
            }
            for r in filtered
        ]


def smart_chunk(text: str, max_tokens: int = 500) -> List[str]:
    """
    Intelligent text chunking
    Splits by logical sections first, then by token count
    """
    # Preserve code blocks
    code_blocks = {}
    code_pattern = r'```[\s\S]*?```'
    
    def replace_code(match):
        slot = f"CODE_SLOT_{len(code_blocks)}"
        code_blocks[slot] = match.group(0)
        return slot
    
    text_with_slots = re.sub(code_pattern, replace_code, text)
    
    # Split by logical sections (headers)
    sections = re.split(r'\n#{1,3} ', text_with_slots)
    
    chunks = []
    current_chunk = ""
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Estimate tokens (rough: 1 token ≈ 4 chars)
        estimated_tokens = len(current_chunk + section) / 4
        
        if estimated_tokens < max_tokens:
            current_chunk += "\n# " + section if current_chunk else section
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = section
    
    if current_chunk:
        chunks.append(current_chunk)
    
    # Restore code blocks
    restored_chunks = []
    for chunk in chunks:
        for slot, code in code_blocks.items():
            chunk = chunk.replace(slot, code)
        restored_chunks.append(chunk)
    
    return restored_chunks if restored_chunks else [text]


# OpenClaw Tool Interface
def memory_search(query: str, max_results: int = 10, 
                  min_score: float = 0.7) -> List[Dict]:
    """Tool: Enhanced semantic memory search"""
    engine = VectorEngine()
    return engine.enhance_memory_search(query, max_results, min_score)

def index_document(content: str, title: str = "", source: str = "") -> str:
    """Tool: Index document for semantic search"""
    engine = VectorEngine()
    metadata = {'title': title, 'source': source}
    return engine.index_document(content, metadata)

def semantic_similarity(text1: str, text2: str) -> float:
    """Tool: Compare semantic similarity between texts"""
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    embeddings = model.encode([text1, text2])
    
    # Cosine similarity
    import numpy as np
    similarity = np.dot(embeddings[0], embeddings[1]) / (
        np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
    )
    return float(similarity)


if __name__ == "__main__":
    # Test
    print("🧪 Testing Vector Engine...")
    engine = VectorEngine()
    print(f"✅ Available engines: {list(engine.engines.keys())}")
    
    # Test chunking
    test_text = """
    # Section 1
    This is some test content that should be chunked properly.
    
    ## Subsection
    More content here.
    
    ```python
    code block preserved
    ```
    
    # Section 2
    Another section with different content.
    """
    
    chunks = smart_chunk(test_text, max_tokens=100)
    print(f"✅ Chunked into {len(chunks)} parts")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: {len(chunk)} chars")