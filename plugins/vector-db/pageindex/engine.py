# Vector DB Plugin - PageIndex Engine
# Optimized for long documents with smart indexing

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
import re
from typing import List, Dict, Optional

class PageIndexSearchResult:
    def __init__(self, content: str, score: float, metadata: Dict, source: str = "pageindex"):
        self.content = content
        self.score = score
        self.metadata = metadata
        self.source = source

class PageIndexEngine:
    """
    PageIndex-style Vector Database
    - Optimized for long documents (PDFs, articles)
    - Hierarchical chunking (page → section → paragraph)
    - Reference tracking (page numbers, line numbers)
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.use_google_auth = config.get('useGoogleAuth', False)
        self.model_name = 'paraphrase-multilingual-mpnet-base-v2'
        
        # Initialize ChromaDB
        if CHROMADB_AVAILABLE:
            self.persist_dir = os.path.expanduser("~/.openclaw/vector-cache/pageindex")
            os.makedirs(self.persist_dir, exist_ok=True)
            
            self.client = chromadb.Client(Settings(
                chroma_db_impl="duckdb+parquet",
                persist_directory=self.persist_dir,
                anonymized_telemetry=False
            ))
            
            self.collection = self.client.get_or_create_collection(
                name="pageindex_collection",
                metadata={"hnsw:space": "cosine"}
            )
        
        # Initialize model
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            self.model = SentenceTransformer(self.model_name)
    
    def hierarchical_chunk(self, text: str, max_tokens: int = 500) -> List[Dict]:
        """
        Hierarchical chunking with metadata
        Returns chunks with: page_num, section_title, paragraph_num
        """
        chunks = []
        current_page = 1
        current_section = "Introduction"
        paragraph_num = 0
        
        # Split by page markers (if any)
        pages = re.split(r'\n---PAGE (\d+)---\n', text)
        
        for i, page_content in enumerate(pages):
            if i > 0 and i % 2 == 1:
                # This is a page number
                current_page = int(page_content)
                continue
            
            # Split by sections
            sections = re.split(r'\n(#{1,3} .+?)\n', page_content)
            
            for j, section_content in enumerate(sections):
                if j % 2 == 1:
                    # This is a section header
                    current_section = section_content.strip()
                    continue
                
                # Split into paragraphs
                paragraphs = section_content.strip().split('\n\n')
                
                for para in paragraphs:
                    if not para.strip():
                        continue
                    
                    # Estimate tokens
                    tokens = len(para) / 4
                    
                    if tokens > max_tokens:
                        # Sub-chunk large paragraphs
                        words = para.split()
                        chunks_words = []
                        current_chunk = []
                        current_tokens = 0
                        
                        for word in words:
                            word_tokens = len(word) / 4 + 0.25
                            if current_tokens + word_tokens > max_tokens:
                                if current_chunk:
                                    chunks.append({
                                        'text': ' '.join(current_chunk),
                                        'page': current_page,
                                        'section': current_section,
                                        'paragraph': paragraph_num,
                                        'type': 'partial'
                                    })
                                current_chunk = [word]
                                current_tokens = word_tokens
                                paragraph_num += 1
                            else:
                                current_chunk.append(word)
                                current_tokens += word_tokens
                        
                        if current_chunk:
                            chunks.append({
                                'text': ' '.join(current_chunk),
                                'page': current_page,
                                'section': current_section,
                                'paragraph': paragraph_num,
                                'type': 'partial'
                            })
                    else:
                        chunks.append({
                            'text': para,
                            'page': current_page,
                            'section': current_section,
                            'paragraph': paragraph_num,
                            'type': 'complete'
                        })
                    
                    paragraph_num += 1
        
        return chunks
    
    def search(self, query: str, top_k: int = 5) -> List[PageIndexSearchResult]:
        """Search with document structure awareness"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return []
        
        query_emb = self.model.encode(query).tolist()
        
        results = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k
        )
        
        search_results = []
        for i in range(len(results['documents'][0])):
            metadata = results['metadatas'][0][i] if results['metadatas'][0] else {}
            
            # Build rich metadata
            rich_metadata = {
                'page': metadata.get('page', 'unknown'),
                'section': metadata.get('section', 'unknown'),
                'paragraph': metadata.get('paragraph', 0),
                'type': metadata.get('type', 'text'),
                'doc_id': metadata.get('doc_id', 'unknown')
            }
            
            result = PageIndexSearchResult(
                content=results['documents'][0][i],
                score=results['distances'][0][i],
                metadata=rich_metadata,
                source=f"pageindex (p.{rich_metadata['page']})"
            )
            search_results.append(result)
        
        return search_results
    
    def index_chunks(self, chunks: List[str], doc_id: str, metadata: Optional[Dict] = None):
        """Index with hierarchical chunking"""
        if not CHROMADB_AVAILABLE or not SENTENCE_TRANSFORMERS_AVAILABLE:
            return
        
        metadata = metadata or {}
        
        # Apply hierarchical chunking if text is long
        full_text = '\n'.join(chunks)
        hierarchical = self.hierarchical_chunk(full_text)
        
        if not hierarchical:
            return
        
        # Generate embeddings
        texts = [c['text'] for c in hierarchical]
        embeddings = self.model.encode(texts).tolist()
        
        # Create IDs
        ids = [f"{doc_id}_p{c['page']}_para{c['paragraph']}" for c in hierarchical]
        
        # Prepare metadata
        metadatas = []
        for chunk in hierarchical:
            meta = {
                **metadata,
                'doc_id': doc_id,
                'page': chunk['page'],
                'section': chunk['section'],
                'paragraph': chunk['paragraph'],
                'type': chunk['type']
            }
            metadatas.append(meta)
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            ids=ids,
            metadatas=metadatas
        )
        
        self.client.persist()


# Tool interface
def search(query: str, top_k: int = 5) -> List[Dict]:
    """OpenClaw tool: Search PageIndex"""
    config = {'enabled': True, 'useGoogleAuth': False}
    engine = PageIndexEngine(config)
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

def index_pdf(pdf_path: str, doc_id: Optional[str] = None) -> str:
    """OpenClaw tool: Index PDF to PageIndex"""
    try:
        import PyPDF2
        
        doc_id = doc_id or os.path.basename(pdf_path)
        
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for i, page in enumerate(reader.pages):
                text += f"\n---PAGE {i+1}---\n"
                text += page.extract_text()
        
        config = {'enabled': True, 'useGoogleAuth': False}
        engine = PageIndexEngine(config)
        
        chunks = text.split('\n\n')
        engine.index_chunks(chunks, doc_id, {'source': pdf_path})
        
        return doc_id
    except ImportError:
        return "Error: PyPDF2 not installed"

def index_document(content: str, doc_id: Optional[str] = None, 
                   title: str = "", source_type: str = "text") -> str:
    """OpenClaw tool: Index document to PageIndex"""
    config = {'enabled': True, 'useGoogleAuth': False}
    engine = PageIndexEngine(config)
    
    doc_id = doc_id or f"doc_{hash(content) % 100000}"
    
    # Simulate page markers for long documents
    lines = content.split('\n')
    page_size = 50  # lines per page
    paged_content = ""
    
    for i, line in enumerate(lines):
        if i % page_size == 0:
            paged_content += f"\n---PAGE {(i // page_size) + 1}---\n"
        paged_content += line + "\n"
    
    chunks = [paged_content]
    engine.index_chunks(chunks, doc_id, {
        'title': title,
        'source_type': source_type
    })
    
    return doc_id

if __name__ == "__main__":
    print("🧪 Testing PageIndex Engine...")
    
    config = {'enabled': True, 'useGoogleAuth': False}
    engine = PageIndexEngine(config)
    
    # Test hierarchical chunking
    test_doc = """
    ---PAGE 1---
    # Introduction
    This is the introduction page of the document.
    It contains important context about the topic.
    
    ## Background
    The background section provides historical context.
    
    ---PAGE 2---
    # Main Content
    This is the main content section.
    It has multiple paragraphs
    
    Paragraph two contains more details.
    
    ## Details
    These are the implementation details.
    """
    
    chunks = engine.hierarchical_chunk(test_doc, 500)
    print(f"✅ Hierarchical chunks: {len(chunks)}")
    for c in chunks[:3]:
        print(f"  Page {c['page']}, Para {c['paragraph']}: {c['text'][:50]}...")