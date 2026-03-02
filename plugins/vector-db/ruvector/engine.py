# Vector DB Plugin - Ruvector Engine
# Multilingual embeddings for Indonesian and other languages

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

import os
import sys
import numpy as np
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RuvectorSearchResult:
    def __init__(self, content: str, score: float, metadata: Dict, source: str = "ruvector"):
        self.content = content
        self.score = score
        self.metadata = metadata
        self.source = source

class RuvectorEngine:
    """
    Ruvector-style Vector Database
    - Multilingual embeddings (Indonesian, English, etc.)
    - Sentence-transformers base
    - Optimized for mixed-language content
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model_name = config.get('model', 'paraphrase-multilingual-mpnet-base-v2')
        # Alternative: 'sentence-transformers/paraphrase-xlm-r-multilingual-v1'
        
        # Initialize ChromaDB (v0.4+ compatible)
        if CHROMADB_AVAILABLE:
            self.persist_dir = os.path.expanduser("~/.openclaw/vector-cache/ruvector")
            os.makedirs(self.persist_dir, exist_ok=True)
            
            # Use PersistentClient for v0.4+
            try:
                self.client = chromadb.PersistentClient(
                    path=self.persist_dir,
                    settings=Settings(anonymized_telemetry=False)
                )
            except AttributeError:
                # Fallback for older versions
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=self.persist_dir,
                    anonymized_telemetry=False
                ))
            
            self.collection = self.client.get_or_create_collection(
                name="ruvector_collection",
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize multilingual model
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.model = SentenceTransformer(self.model_name)
    
    def detect_language(self, text: str) -> str:
        """Simple language detection based on character patterns"""
        indo_patterns = ['yang', 'dan', 'di', 'untuk', 'dengan', 'ini', 'itu', 'adalah']
        text_lower = text.lower()
        
        indo_count = sum(1 for word in indo_patterns if word in text_lower)
        
        if indo_count >= 2:
            return 'id'
        
        # Check for non-ASCII (might be Indonesian or other)
        non_ascii = sum(1 for c in text if ord(c) > 127)
        if non_ascii / len(text) > 0.3:
            return 'mixed'
        
        return 'en'
    
    def encode_multilingual(self, texts: List[str]) -> np.ndarray:
        """
        Encode with language-aware processing
        """
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return np.array([])
        
        # The paraphrase-multilingual model handles multiple languages natively
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
    
    def search(self, query: str, top_k: int = 5) -> List[RuvectorSearchResult]:
        """Multilingual semantic search"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return []
        
        query_lang = self.detect_language(query)
        query_emb = self.encode_multilingual([query])[0].tolist()
        
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        
        search_results = []
        for i in range(len(results['documents'][0])):
            metadata = results['metadatas'][0][i] if results['metadatas'][0] else {}
            content = results['documents'][0][i]
            
            # Detect result language
            result_lang = self.detect_language(content)
            
            result = RuvectorSearchResult(
                content=content,
                score=results['distances'][0][i],
                metadata={
                    **metadata,
                    'query_language': query_lang,
                    'result_language': result_lang
                },
                source=f"ruvector ({result_lang})"
            )
            search_results.append(result)
        
        return search_results
    
    def index_chunks(self, chunks: List[str], doc_id: str, metadata: Optional[Dict] = None):
        """Index with language detection"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return
        
        metadata = metadata or {}
        
        # Detect languages
        languages = [self.detect_language(chunk) for chunk in chunks]
        
        # Generate embeddings
        embeddings = self.encode_multilingual(chunks).tolist()
        
        # Create IDs
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Prepare metadata with language info
        metadatas = []
        for i, chunk in enumerate(chunks):
            meta = {
                **metadata,
                'doc_id': doc_id,
                'chunk_index': i,
                'language': languages[i],
                'length': len(chunk)
            }
            metadatas.append(meta)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        
        self.client.persist()
    
    def search_by_language(self, query: str, language: str, top_k: int = 5) -> List[RuvectorSearchResult]:
        """Search filtering by language"""
        all_results = self.search(query, top_k=top_k * 2)  # Get more, filter after
        
        # Filter by language
        filtered = [r for r in all_results if r.metadata.get('language') == language]
        
        return filtered[:top_k]
    
    def get_stats(self) -> Dict:
        """Get statistics about indexed content"""
        if not CHROMADB_AVAILABLE:
            return {}
        
        count = self.collection.count()
        
        # Get all metadata
        results = self.collection.get()
        
        languages = {}
        if results['metadatas']:
            for meta in results['metadatas']:
                lang = meta.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
        
        return {
            'total_documents': count,
            'languages': languages
        }


# Tool interface
def search(query: str, top_k: int = 5) -> List[Dict]:
    """OpenClaw tool: Search Ruvector (multilingual)"""
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    results = engine.search(query, top_k)
    return [
        {
            'content': r.content,
            'score': r.score,
            'metadata': r.metadata,
            'source': r.source
        }
        for r in results
    ]

def search_indonesian(query: str, top_k: int = 5) -> List[Dict]:
    """OpenClaw tool: Search specifically for Indonesian content"""
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    results = engine.search_by_language(query, 'id', top_k)
    return [
        {
            'content': r.content,
            'score': r.score,
            'metadata': r.metadata,
            'source': r.source
        }
        for r in results
    ]

def index(content: str, doc_id: Optional[str] = None, metadata: Dict = None) -> str:
    """OpenClaw tool: Index content to Ruvector with language detection"""
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    
    from shared.engine import smart_chunk
    chunks = smart_chunk(content, 500)
    doc_id = doc_id or f"doc_{hash(content) % 100000}"
    
    engine.index_chunks(chunks, doc_id, metadata)
    return doc_id

def get_stats() -> Dict:
    """OpenClaw tool: Get Ruvector statistics"""
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    return engine.get_stats()

if __name__ == "__main__":
    print("🧪 Testing Ruvector Engine...")
    
    config = {'enabled': True, 'model': 'paraphrase-multilingual-mpnet-base-v2'}
    engine = RuvectorEngine(config)
    
    # Test language detection
    test_texts = [
        "This is English text",
        "Ini adalah teks dalam bahasa Indonesia",
        "Ce texte est en français"
    ]
    
    print("✅ Language detection:")
    for text in test_texts:
        lang = engine.detect_language(text)
        print(f"  '{text[:30]}...' -> {lang}")
    
    if CHROMADB_AVAILABLE and SENTENCE_TRANSFORMERS_AVAILABLE:
        try:
            # Try importing smart_chunk
            try:
                import sys
                sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from shared.engine import smart_chunk
            except ImportError:
                def smart_chunk(text, max_tokens=500):
                    return [text[:1000]]
            
            mixed_doc = """
            # Dokumen Campuran
            
            Bagian pertama dalam bahasa Indonesia.
            Ini berisi informasi penting.
            
            ## English Section
            This is content in English.
            
            ## Kesimpulan
            Dokumen ini mencakup dua bahasa.
            """
            
            chunks = smart_chunk(mixed_doc, 500)
            engine.index_chunks(chunks, "mixed_doc_001", {"title": "Mixed Test"})
            print(f"\n✅ Indexed {len(chunks)} chunks")
        except Exception as e:
            print(f"⚠️  Test error: {e}")
    else:
        print("⚠️  Dependencies missing - install: pip install chromadb sentence-transformers")