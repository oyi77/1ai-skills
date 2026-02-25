#!/usr/bin/env python3
"""
OPENCLOW CHROMADB RAG - Retrieval-Augmented Generation
Memberikan context relevan ke LLM dari knowledge base
"""

import sys
import json
from pathlib import Path

# Chroma import
try:
    import chromadb
    from chromadb.config import Settings
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False
    print("❌ ChromaDB not installed")

# Embedding
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDING_AVAILABLE = True
except ImportError:
    EMBEDDING_AVAILABLE = False

class OpenClawRAG:
    """RAG system untuk OpenClaw."""

    def __init__(self, db_path="/home/openclaw/.openclaw/chroma_db"):
        if not CHROMA_AVAILABLE:
            raise ImportError("ChromaDB not installed")

        # Initialize client
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True)
        )

        # Get collections
        self.skills_col = self.client.get_collection("skills")
        self.tools_col = self.client.get_collection("tools")
        self.memory_col = self.client.get_collection("memory")
        self.commands_col = self.client.get_collection("commands")
        self.context_col = self.client.get_collection("context")

        # Embedding model
        if EMBEDDING_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = None

        print("✅ OpenClaw RAG initialized")

    def _embed(self, text):
        """Convert text to vector."""
        if self.embedding_model is not None:
            return self.embedding_model.encode(text).tolist()
        else:
            # Dummy hash-based embedding
            import hashlib
            import numpy as np
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            np.random.seed(int(hash_hex[:8], 16))
            return np.random.rand(384).astype(np.float32).tolist()

    def retrieve_for_task(self, task, n_results=3):
        """Retrieve relevant context untuk task."""
        context = {}

        # Search skills
        skills_results = self.skills_col.query(
            query_embeddings=[self._embed(task)],
            n_results=n_results
        )

        if skills_results['ids'] and skills_results['ids'][0]:
            context['skills'] = []

            for i, (doc_id, doc, metadata) in enumerate(zip(
                skills_results['ids'][0],
                skills_results['documents'][0],
                skills_results['metadatas'][0]
            )):
                context['skills'].append({
                    'id': doc_id,
                    'name': metadata.get('name', doc_id),
                    'description': metadata.get('description', ''),
                    'path': metadata.get('path', ''),
                    'score': skills_results['distances'][0][i] if 'distances' in skills_results else None
                })

        # Search memory
        memory_results = self.memory_col.query(
            query_embeddings=[self._embed(task)],
            n_results=n_results
        )

        if memory_results['ids'] and memory_results['ids'][0]:
            context['memory'] = []

            for i, (doc_id, doc, metadata) in enumerate(zip(
                memory_results['ids'][0],
                memory_results['documents'][0],
                memory_results['metadatas'][0]
            )):
                context['memory'].append({
                    'id': doc_id,
                    'file': metadata.get('file', ''),
                    'type': metadata.get('type', ''),
                    'snippet': doc[:500],
                    'score': memory_results['distances'][0][i] if 'distances' in memory_results else None
                })

        # Search context
        context_results = self.context_col.query(
            query_embeddings=[self._embed(task)],
            n_results=n_results
        )

        if context_results['ids'] and context_results['ids'][0]:
            context['context'] = []

            for i, (doc_id, doc, metadata) in enumerate(zip(
                context_results['ids'][0],
                context_results['documents'][0],
                context_results['metadatas'][0]
            )):
                context['context'].append({
                    'id': doc_id,
                    'file': metadata.get('file', ''),
                    'snippet': doc[:500],
                    'score': context_results['distances'][0][i] if 'distances' in context_results else None
                })

        return context

    def format_context_for_llm(self, context):
        """Format context untuk input ke LLM."""
        formatted = []

        if 'skills' in context and context['skills']:
            formatted.append("## Relevant Skills\n")
            for skill in context['skills']:
                formatted.append(f"- {skill['name']}: {skill['description']}")

        if 'memory' in context and context['memory']:
            formatted.append("\n## Relevant Memory\n")
            for mem in context['memory']:
                formatted.append(f"- {mem['file']}: {mem['snippet']}")

        if 'context' in context and context['context']:
            formatted.append("\n## Relevant Context\n")
            for ctx in context['context']:
                formatted.append(f"- {ctx['file']}: {ctx['snippet']}")

        return '\n'.join(formatted)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='OpenClaw RAG System')
    parser.add_argument('task', help='Task to retrieve context for')
    parser.add_argument('--n-results', type=int, default=3, help='Number of results per collection')
    parser.add_argument('--format', choices=['json', 'text', 'llm'], default='text', help='Output format')
    parser.add_argument('--db-path', default='/home/openclaw/.openclaw/chroma_db', help='Database path')

    args = parser.parse_args()

    # Initialize RAG
    try:
        rag = OpenClawRAG(args.db_path)
    except ImportError as e:
        print(f"❌ {e}")
        sys.exit(1)

    # Retrieve context
    context = rag.retrieve_for_task(args.task, n_results=args.n_results)

    # Format output
    if args.format == 'json':
        print(json.dumps(context, indent=2))
    elif args.format == 'llm':
        formatted = rag.format_context_for_llm(context)
        print(formatted)
    else:  # text
        print("="*80)
        print(f"RETRIEVED CONTEXT FOR: '{args.task}'")
        print("="*80)
        print()

        if 'skills' in context and context['skills']:
            print("🎯 Skills:")
            for skill in context['skills']:
                print(f"  - {skill['name']}: {skill['description']}")
            print()

        if 'memory' in context and context['memory']:
            print("📝 Memory:")
            for mem in context['memory']:
                print(f"  - {mem['file']}: {mem['snippet']}")
            print()

        if 'context' in context and context['context']:
            print("📁 Context:")
            for ctx in context['context']:
                print(f"  - {ctx['file']}: {ctx['snippet']}")
            print()

if __name__ == "__main__":
    main()
