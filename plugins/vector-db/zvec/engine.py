# Vector DB Plugin - ZVec Engine
# Using ChromaDB as the vector store backend

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️  ChromaDB not installed. Run: pip install chromadb")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("⚠️  SentenceTransformers not installed. Run: pip install sentence-transformers")

import os
import sys
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ZVecSearchResult:
    def __init__(self, content: str, score: float, metadata: Dict, source: str = "zvec"):
        self.content = content
        self.score = score
        self.metadata = metadata
        self.source = source

class ZVecEngine:
    """
    ZVec-style Vector Database
    - Uses ChromaDB for storage
    - BGE-M3 for embeddings (multilingual)
    - Optimized for similarity search
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.model_name = config.get('model', 'BAAI/bge-m3')
        self.collection_name = "zvec_collection"
        
        # Initialize ChromaDB (v0.4+ compatible)
        if CHROMADB_AVAILABLE:
            self.persist_dir = os.path.expanduser("~/.openclaw/vector-cache/zvec")
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
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize embedding model
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.model = SentenceTransformer(self.model_name)
    
    def search(self, query: str, top_k: int = 5) -> List[ZVecSearchResult]:
        """Semantic search using ZVec"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return []
        
        # Generate query embedding
        query_emb = self.model.encode(query).tolist()
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        
        # Format results
        search_results = []
        for i in range(len(results['documents'][0])):
            result = ZVecSearchResult(
                content=results['documents'][0][i],
                score=results['distances'][0][i],
                metadata=results['metadatas'][0][i] if results['metadatas'][0] else {},
                source="zvec"
            )
            search_results.append(result)
        
        return search_results
    
    def index_chunks(self, chunks: List[str], doc_id: str, metadata: Optional[Dict] = None):
        """Index document chunks"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return
        
        metadata = metadata or {}
        
        # Generate embeddings
        embeddings = self.model.encode(chunks).tolist()
        
        # Create IDs
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=chunks,
            ids=ids,
            metadatas=[{**metadata, 'chunk_index': i} for i in range(len(chunks))]
        )
        
        # Persist
        if hasattr(self.client, 'persist'):
            self.client.persist()
    
    def delete_document(self, doc_id: str):
        """Delete a document and its chunks"""
        if not CHROMADB_AVAILABLE:
            return
        
        # Get all IDs matching doc_id
        results = self.collection.get(
            where={"doc_id": doc_id}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            if hasattr(self.client, 'persist'):
                self.client.persist()


# Tool interface
def search(query: str, top_k: int = 5) -> List[Dict]:
    """OpenClaw tool: Search ZVec"""
    config = {'enabled': True, 'model': 'BAAI/bge-m3'}
    engine = ZVecEngine(config)
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

def index(content: str, doc_id: Optional[str] = None, metadata: Dict = None) -> str:
    """OpenClaw tool: Index content to ZVec"""
    from shared.engine import smart_chunk
    
    config = {'enabled': True, 'model': 'BAAI/bge-m3'}
    engine = ZVecEngine(config)
    
    chunks = smart_chunk(content, 500)
    doc_id = doc_id or f"doc_{hash(content) % 100000}"
    
    engine.index_chunks(chunks, doc_id, metadata)
    return doc_id

if __name__ == "__main__":
    print("🧪 Testing ZVec Engine...")
    
    config = {'enabled': True, 'model': 'BAAI/bge-m3'}
    engine = ZVecEngine(config)
    
    # Test indexing
    test_doc = """
    # Test Document
    This is a test document about OpenClaw plugins.
    The plugin system makes it easy to extend functionality.
    
    ## Features
    - Semantic search
    - Document chunking
    - Multiple engines
    """
    
    from shared.engine import smart_chunk
    chunks = smart_chunk(test_doc, 500)
    engine.index_chunks(chunks, "test_doc_001", {"title": "Test"})
    print(f"✅ Indexed {len(chunks)} chunks")
    
    # Test search
    results = engine.search("OpenClaw plugins", top_k=3)
    print(f"✅ Found {len(results)} results")
    for r in results:
        print(f"  Score: {r.score:.3f} | {r.content[:50]}...")