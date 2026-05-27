---
name: rag-knowledge-base
description: RAG Knowledge Base Builder. Use when relevant to this domain.
---
persona:
  name: "Domain Expert"
  title: "Master of Rag Knowledge Base"
  expertise: ['Research Excellence', 'Best Practices', 'Professional Standards']
  philosophy: "Excellence is not a skill, it's an attitude."
  credentials: ['Industry leader', 'Practiced professional', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based', 'Customer focused']



# RAG Knowledge Base Builder

## Overview

Build enterprise AI assistants that answer questions from your own documents — no hallucinations, source-cited, always accurate to your data.

**Use cases**:
- Internal HR / policy bot (employees ask company policies)
- Customer support bot (answers from product docs)
- Legal document analysis (contracts, regulations)
- Sales enablement (pricing, case studies, objection handling)
- Medical / clinical knowledge assistant

**Revenue**: $3,000–30,000 per build + $1,000–5,000/month SLA

---

## When to Use

- Business has 50+ documents that employees struggle to navigate
- Customer support handling repetitive questions about products
- Legal/compliance team drowning in regulations
- Sales team needing instant access to case studies/pricing
- Any "ask my data" use case

---

## Tech Stack Options

### Option A: LlamaIndex (Recommended for custom builds)
```python
# pip install llama-index llama-index-embeddings-openai
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
docs = SimpleDirectoryReader("./documents").load_data()

# Build index
index = VectorStoreIndex.from_documents(docs)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is our refund policy?")
print(response)
```

### Option B: LangChain + ChromaDB
```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load and split docs
loader = DirectoryLoader("./documents", glob="**/*.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# Build vector store
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
vectorstore.persist()

print(f"Indexed {len(chunks)} chunks from {len(docs)} documents")
```

### Option C: Local/Free (No API costs)
```python
# pip install sentence-transformers chromadb
from sentence_transformers import SentenceTransformer
import chromadb

# Local embeddings — free, private
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
client = chromadb.PersistentClient(path="./vectordb")
collection = client.get_or_create_collection("knowledge_base")

def add_document(text: str, doc_id: str, metadata: dict = {}):
    """Index a document chunk"""
    embedding = model.encode(text).tolist()
    collection.add(
        embeddings=[embedding],
        documents=[text],
        metadatas=[metadata],
        ids=[doc_id]
    )

def search(query: str, n_results: int = 5) -> list:
    """Semantic search"""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results["documents"][0]
```

---

## Full Pipeline Script

```python
#!/usr/bin/env python3
# scripts/build_knowledge_base.py
"""
Build a RAG knowledge base from a folder of documents.
Supports: PDF, Word, TXT, Markdown, CSV
"""

import os
import sys
import argparse
from pathlib import Path

def extract_text_from_pdf(filepath: str) -> str:
    """Extract text from PDF"""
    try:
        import pdfplumber
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        import subprocess
        result = subprocess.run(["pdftotext", filepath, "-"], capture_output=True, text=True)
        return result.stdout

def extract_text_from_docx(filepath: str) -> str:
    """Extract text from Word document"""
    try:
        import docx
        doc = docx.Document(filepath)
        return "\n".join(para.text for para in doc.paragraphs)
    except ImportError:
        return ""

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    """Split text into overlapping chunks"""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

def load_documents(docs_dir: str) -> list:
    """Load all documents from directory"""
    docs = []
    supported = {".pdf", ".txt", ".md", ".docx", ".csv"}
    
    for filepath in Path(docs_dir).rglob("*"):
        if filepath.suffix.lower() not in supported:
            continue
        
        print(f"Loading: {filepath.name}")
        
        if filepath.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(str(filepath))
        elif filepath.suffix.lower() == ".docx":
            text = extract_text_from_docx(str(filepath))
        else:
            text = filepath.read_text(errors="ignore")
        
        if text.strip():
            docs.append({
                "source": filepath.name,
                "text": text,
                "path": str(filepath)
            })
    
    return docs

def build_index(docs_dir: str, output_dir: str = "./knowledge_base"):
    """Build knowledge base from documents"""
    import chromadb
    from sentence_transformers import SentenceTransformer
    
    print(f"\n🔧 Building knowledge base from: {docs_dir}")
    
    # Load model
    print("Loading embedding model...")
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    
    # Setup vector store
    os.makedirs(output_dir, exist_ok=True)
    client = chromadb.PersistentClient(path=output_dir)
    collection = client.get_or_create_collection(
        name="documents",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Load and index documents
    documents = load_documents(docs_dir)
    print(f"Loaded {len(documents)} documents")
    
    total_chunks = 0
    for doc in documents:
        chunks = chunk_text(doc["text"])
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc['source']}__chunk{i}"
            embedding = model.encode(chunk).tolist()
            
            collection.add(
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{"source": doc["source"], "chunk": i}],
                ids=[chunk_id]
            )
            total_chunks += 1
    
    print(f"✅ Indexed {total_chunks} chunks from {len(documents)} documents")
    print(f"📁 Saved to: {output_dir}")
    return output_dir

def query_knowledge_base(query: str, kb_dir: str = "./knowledge_base", n: int = 3) -> str:
    """Query the knowledge base"""
    import chromadb
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    client = chromadb.PersistentClient(path=kb_dir)
    collection = client.get_collection("documents")
    
    query_embedding = model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=n)
    
    context = "\n\n---\n\n".join(results["documents"][0])
    sources = [m.get("source") for m in results["metadatas"][0]]
    
    return {"context": context, "sources": sources}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAG Knowledge Base Builder")
    parser.add_argument("--build", help="Directory of documents to index")
    parser.add_argument("--query", help="Query the knowledge base")
    parser.add_argument("--kb", default="./knowledge_base", help="KB directory")
    args = parser.parse_args()
    
    if args.build:
        build_index(args.build, args.kb)
    elif args.query:
        result = query_knowledge_base(args.query, args.kb)
        print(f"Query: {args.query}\n")
        print(f"Context:\n{result['context']}\n")
        print(f"Sources: {result['sources']}")
```

---

## Chat Interface

```python
#!/usr/bin/env python3
# scripts/rag_chat.py
"""Interactive chat with knowledge base"""

import os
from scripts.build_knowledge_base import query_knowledge_base

def chat_with_kb(kb_dir: str = "./knowledge_base"):
    """Interactive Q&A with knowledge base"""
    # Requires OpenAI or local LLM
    import openai
    client = openai.OpenAI()
    
    print("Knowledge Base Assistant (type 'exit' to quit)\n")
    history = []
    
    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break
        
        # Get relevant context
        result = query_knowledge_base(query, kb_dir)
        context = result["context"]
        sources = result["sources"]
        
        # Generate answer
        messages = [
            {"role": "system", "content": f"""You are a helpful assistant. 
Answer questions based ONLY on the provided context. 
If the answer isn't in the context, say "I don't have that information."
Always cite your sources.

Context:
{context}"""},
            *history,
            {"role": "user", "content": query}
        ]
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        answer = response.choices[0].message.content
        print(f"\nAssistant: {answer}")
        print(f"Sources: {', '.join(set(sources))}\n")
        
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": answer})
        
        if len(history) > 20:
            history = history[-20:]

if __name__ == "__main__":
    chat_with_kb()
```

---

## Deployment Options

### Option 1: WhatsApp Bot (via wa-business-automation)
```python
# Add to wa_chatbot.py:
from skills.rag_knowledge_base.scripts.build_knowledge_base import query_knowledge_base

def handle_wa_query(message: str) -> str:
    result = query_knowledge_base(message)
    context = result["context"]
    # Use AI to generate answer from context
    return generate_answer(message, context)
```

### Option 2: Web Chat Widget
```
Stack: FastAPI backend + React frontend
Embed on client website
Branded as "[Company] AI Assistant"
```

### Option 3: Telegram Bot
```python
# pip install python-telegram-bot
from telegram.ext import Application, MessageHandler, filters
```

### Option 4: Slack Bot
```
Slack app with message listener
Deploy to Railway/Render ($5/month)
```

---

## Client Delivery Package

### What to deliver:
1. ✅ Indexed knowledge base (all their docs)
2. ✅ Chat interface (web/WA/Telegram)
3. ✅ Admin panel (add/remove docs)
4. ✅ Analytics (top questions, unanswered)
5. ✅ Monthly doc refresh automation

### Pricing:
| Scope | One-time | Monthly |
|-------|----------|---------|
| Internal Bot (<50 docs) | IDR 5M | IDR 1M/mo |
| Customer Support Bot | IDR 15M | IDR 3M/mo |
| Enterprise (100+ docs) | IDR 30M+ | IDR 5M+/mo |

---

## Installation

```bash
pip install chromadb sentence-transformers pdfplumber python-docx openai

# Build index
python3 skills/rag-knowledge-base/scripts/build_knowledge_base.py \
  --build ./client_documents \
  --kb ./client_kb

# Query
python3 skills/rag-knowledge-base/scripts/build_knowledge_base.py \
  --query "What is your return policy?" \
  --kb ./client_kb
```

## When NOT to Use

- [TODO: Add specific exclusion cases for this skill]
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- [TODO: Add behavioral signs the skill is being violated]
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] [TODO: Add specific evidence-based checklist items]
- [ ] All required outputs generated
- [ ] Success criteria met

