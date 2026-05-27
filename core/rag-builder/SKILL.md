---
name: rag-builder
description: RAG pipeline design — document chunking, embedding strategies, retrieval optimization, and answer generation
---

## Overview

Retrieval-Augmented Generation (RAG) is the standard pattern for grounding LLMs in your data. This skill covers the full pipeline: document loading, chunking strategies, embedding, vector storage, retrieval, and answer synthesis.

## Capabilities

- Design document chunking strategies (fixed, semantic, recursive)
- Select and configure embedding models for your use case
- Implement hybrid search (vector + keyword) for better retrieval
- Build answer synthesis with source attribution
- Evaluate RAG quality with RAGAS metrics

## When to Use

- Building a chatbot over your documentation or knowledge base
- Need LLM answers grounded in factual, up-to-date data
- Document Q&A where hallucination is unacceptable
- Customer support automation over product docs

## Pseudo Code

### Chunking Strategy
```python
def chunk_document(doc, strategy="recursive", chunk_size=512, overlap=50):
    if strategy == "fixed":
        return split_by_chars(doc, chunk_size, overlap)
    elif strategy == "recursive":
        return recursive_split(doc, separators=["\n\n", "\n", ". ", " "], chunk_size=chunk_size)
    elif strategy == "semantic":
        return semantic_split(doc, similarity_threshold=0.8)
```

### RAG Pipeline
```python
def rag_query(question, vector_store, llm):
    # 1. Retrieve relevant chunks
    chunks = vector_store.similarity_search(question, k=5)
    
    # 2. Re-rank by relevance
    ranked = rerank(chunks, question, top_k=3)
    
    # 3. Synthesize answer with sources
    context = "\n\n".join([c.text for c in ranked])
    prompt = f"""Answer based on context. Cite sources.

Context:
{context}

Question: {question}

Answer with citations:"""
    
    return llm.generate(prompt)
```

## Common Patterns

- **Recursive chunking**: Best default — splits by paragraphs, then sentences, then words
- **Overlap matters**: 10-20% overlap between chunks prevents context loss at boundaries
- **Hybrid search**: Combine vector similarity with BM25 keyword search for best results
- **Source attribution**: Always return which chunks informed the answer
