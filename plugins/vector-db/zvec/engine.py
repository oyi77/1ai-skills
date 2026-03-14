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

# OpenAI embeddings fallback
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

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
    ZVec-style Vector Database with fallback embeddings
    - Uses ChromaDB for storage
    - Multiple embedding models with automatic fallback
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
            
            try:
                self.client = chromadb.PersistentClient(
                    path=self.persist_dir,
                    settings=Settings(anonymized_telemetry=False)
                )
            except AttributeError:
                self.client = chromadb.Client(Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=self.persist_dir,
                    anonymized_telemetry=False
                ))
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize embedding model with fallback
        self.model = self._init_embedding_model()
    
    def _init_embedding_model(self):
        """Initialize embedding model with fallback chain"""
        models = []
        
        # Priority 1: BGE-M3 (multilingual, high quality)
        try:
            from sentence_transformers import SentenceTransformer
            models.append(('BAAI/bge-m3', SentenceTransformer('BAAI/bge-m3')))
            print("✅ Using BGE-M3 embedding model")
        except Exception as e:
            print(f"⚠️  BGE-M3 unavailable: {e}")
        
        # Priority 2: MiniLM (faster, single language)
        try:
            from sentence_transformers import SentenceTransformer
            models.append(('all-MiniLM-L6-v2', SentenceTransformer('all-MiniLM-L6-v2')))
            print("✅ Using MiniLM fallback model")
        except Exception as e:
            print(f"⚠️  MiniLM unavailable: {e}")
        
        # Priority 3: OpenAI embeddings (as fallback)
        if OPENAI_AVAILABLE:
            try:
                api_key = os.getenv("OPENAI_API_KEY", "")
                if api_key:
                    openai.api_key = api_key
                    models.append(('openai/text-embedding-3-small', None))  # Will use OpenAI directly
                    print("✅ OpenAI embeddings available as fallback")
                else:
                    print("⚠️  OPENAI_API_KEY not set")
            except Exception as e:
                print(f"⚠️  OpenAI init failed: {e}")
        
        if not models:
            print("❌ No embedding models available!")
            return None
        
        # Use best available model
        return models[0][1] if models[0][1] else models[0][0]
    
    def _get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings with automatic fallback
        """
        if self.model is None:
            raise Exception("No embedding model available")
        
        # If using OpenAI as model (not instantiated)
        if isinstance(self.model, str) and self.model.startswith('openai'):
            try:
                import openai
                embeddings = []
                for text in texts:
                    response = openai.Embedding.create(
                        input=text,
                        model="text-embedding-3-small"
                    )
                    embeddings.append(response['data'][0]['embedding'])
                return embeddings
            except Exception as e:
                print(f"⚠️  OpenAI failed, trying fallback...")
                # Fall back to local models
        
        # Use local models
        return self.model.encode(texts).tolist()
    
    def search(self, query: str, top_k: int = 5) -> List[ZVecSearchResult]:
        """Semantic search using ZVec with fallback"""
        if not CHROMADB_AVAILABLE:
            return []
        
        # Generate query embedding with fallback
        try:
            query_emb = self._get_embeddings([query])[0]
        except Exception as e:
            print(f"⚠️  Embedding generation failed: {e}")
            return []
        
        # Search
        try:
            results = self.collection.query(
                query_embeddings=[query_emb],
                n_results=top_k
            )
        except Exception as e:
            print(f"⚠️  Collection query failed: {e}")
            return []
        
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
        if not CHROMADB_AVAILABLE:
            return
        
        metadata = metadata or {}
        
        # Generate embeddings with fallback
        try:
            embeddings = self._get_embeddings(chunks)
        except Exception as e:
            print(f"⚠️  Embedding generation failed: {e}")
            return
        
        # Create IDs
        ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
        
        # Add to collection
        try:
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                ids=ids,
                metadatas=[{**metadata, 'chunk_index': i} for i in range(len(chunks))]
            )
            
            # Persist
            if hasattr(self.client, 'persist'):
                self.client.persist()
        except Exception as e:
            print(f"⚠️  Collection add failed: {e}")
    
    def delete_document(self, doc_id: str):
        """Delete a document and its chunks"""
        if not CHROMADB_AVAILABLE:
            return
        
        try:
            results = self.collection.get(
                where={"doc_id": doc_id}
            )
            
            if results['ids']:
                self.collection.delete(ids=results['ids'])
                if hasattr(self.client, 'persist'):
                    self.client.persist()
        except Exception as e:
            print(f"⚠️  Delete failed: {e}")


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

if __name__ == "__main__":
    # Test
    print("=" * 60)
    print("ZVec Engine - Fallback Test")
    print("=" * 60)
    
    engine = ZVecEngine({})
    
    # Test search
    results = engine.search("trading strategy", top_k=3)
    
    print(f"\nResults: {len(results)}")
    for r in results:
        print(f"Score: {r.score:.3f}")
        print(f"Content: {r.content[:100]}...")
