#!/usr/bin/env python3
"""
OPENCLOW CHROMADB INTEGRATION - Global Vector Database
System-wide knowledge base untuk OpenClaw: skills, tools, memory, commands
"""

import sys
import os
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path
import re

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

class OpenClawChromaDB:
    """ChromaDB untuk OpenClaw system."""

    def __init__(self, db_path="/home/openclaw/.openclaw/chroma_db"):
        if not CHROMA_AVAILABLE:
            raise ImportError("ChromaDB not installed")

        # Initialize persistent client
        self.client = chromadb.PersistentClient(
            path=db_path,
            settings=Settings(anonymized_telemetry=False, allow_reset=True)
        )

        # Collections
        self.skills_col = self.client.get_or_create_collection(
            name="skills",
            metadata={"hnsw:space": "l2"}
        )

        self.tools_col = self.client.get_or_create_collection(
            name="tools",
            metadata={"hnsw:space": "l2"}
        )

        self.memory_col = self.client.get_or_create_collection(
            name="memory",
            metadata={"hnsw:space": "l2"}
        )

        self.commands_col = self.client.get_or_create_collection(
            name="commands",
            metadata={"hnsw:space": "l2"}
        )

        self.context_col = self.client.get_or_create_collection(
            name="context",
            metadata={"hnsw:space": "l2"}
        )

        # Embedding model
        if EMBEDDING_AVAILABLE:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        else:
            self.embedding_model = None
            print("⚠️  Using dummy embeddings")

        print(f"✅ OpenClaw ChromaDB initialized at {db_path}")

    def _embed(self, text):
        """Convert text to vector."""
        if self.embedding_model is not None:
            return self.embedding_model.encode(text).tolist()
        else:
            # Dummy hash-based embedding
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            import numpy as np
            np.random.seed(int(hash_hex[:8], 16))
            return np.random.rand(384).astype(np.float32).tolist()

    # ==================== SKILLS ====================

    def index_skills(self, skills_dir="/home/openclaw/.openclaw/workspace/skills"):
        """Index semua skills."""
        print(f"🔍 Indexing skills from {skills_dir}...")

        skills = []
        for skill_dir in Path(skills_dir).iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                if skill_md.exists():
                    with open(skill_md, 'r') as f:
                        content = f.read()

                    skills.append({
                        "id": skill_dir.name,
                        "name": skill_dir.name,
                        "path": str(skill_dir),
                        "content": content
                    })

        print(f"Found {len(skills)} skills")

        for skill in skills:
            # Extract description (lines until first empty line)
            lines = skill['content'].split('\n')
            description_lines = []
            for line in lines[1:]:
                if line.strip() == '' or line.startswith('#'):
                    break
                description_lines.append(line)
            description = ' '.join(description_lines).strip()

            # Create text for embedding
            text = f"""
            Skill: {skill['name']}
            Description: {description}
            Content: {skill['content'][:500]}
            """

            embedding = self._embed(text)

            self.skills_col.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "name": skill['name'],
                    "path": skill['path'],
                    "description": description,
                    "indexed_at": datetime.now().isoformat()
                }],
                ids=[f"skill_{skill['name']}"]
            )

            print(f"  ✅ Indexed: {skill['name']}")

    def search_skills(self, query, category=None, n_results=10):
        """Cari skills."""
        query_embedding = self._embed(query)

        if category:
            results = self.skills_col.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where={"category": category}
            )
        else:
            results = self.skills_col.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

        return results

    # ==================== TOOLS ====================

    def index_tools(self, tools_spec=None):
        """Index tools dari OpenClaw TOOLS.md."""
        tools_path = "/home/openclaw/.openclaw/workspace/TOOLS.md"

        if not os.path.exists(tools_path):
            print(f"⚠️  TOOLS.md not found at {tools_path}")
            return

        with open(tools_path, 'r') as f:
            content = f.read()

        # Parse tools
        tools = []
        sections = re.split(r'\n###\s+', content)

        for section in sections[1:]:  # Skip header
            if section.strip():
                lines = section.strip().split('\n')
                tool_name = lines[0].strip()
                tool_info = '\n'.join(lines[1:])

                tools.append({
                    "name": tool_name,
                    "info": tool_info
                })

        print(f"Found {len(tools)} tools")

        for tool in tools:
            text = f"Tool: {tool['name']}\nInfo: {tool['info']}"
            embedding = self._embed(text)

            self.tools_col.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "name": tool['name'],
                    "indexed_at": datetime.now().isoformat()
                }],
                ids=[f"tool_{tool['name']}"]
            )

            print(f"  ✅ Indexed: {tool['name']}")

    def search_tools(self, query, n_results=10):
        """Cari tools."""
        query_embedding = self._embed(query)

        results = self.tools_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    # ==================== MEMORY ====================

    def index_memory(self, memory_dir="/home/openclaw/.openclaw/workspace/memory"):
        """Index semua memory files."""
        print(f"🔍 Indexing memory from {memory_dir}...")

        # Check MEMORY.md
        memory_main = Path(memory_dir).parent / "MEMORY.md"
        if memory_main.exists():
            with open(memory_main, 'r') as f:
                content = f.read()

            text = f"MEMORY.md\n{content}"
            embedding = self._embed(text)

            self.memory_col.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "file": "MEMORY.md",
                    "type": "main_memory",
                    "indexed_at": datetime.now().isoformat()
                }],
                ids=["memory_main"]
            )

            print("  ✅ Indexed: MEMORY.md")

        # Index daily memory files
        if os.path.exists(memory_dir):
            for mem_file in Path(memory_dir).glob("*.md"):
                with open(mem_file, 'r') as f:
                    content = f.read()

                text = f"{mem_file.name}\n{content}"
                embedding = self._embed(text)

                self.memory_col.add(
                    documents=[text],
                    embeddings=[embedding],
                    metadatas=[{
                        "file": mem_file.name,
                        "type": "daily_memory",
                        "date": mem_file.stem,
                        "indexed_at": datetime.now().isoformat()
                    }],
                    ids=[f"memory_{mem_file.stem}"]
                )

                print(f"  ✅ Indexed: {mem_file.name}")

    def search_memory(self, query, n_results=10):
        """Cari memory."""
        query_embedding = self._embed(query)

        results = self.memory_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    # ==================== COMMANDS ====================

    def index_commands(self):
        """Index commands dari history/docs."""
        # Common OpenClaw commands
        commands = [
            {
                "name": "openclaw status",
                "description": "Check OpenClaw system status",
                "usage": "openclaw status"
            },
            {
                "name": "openclaw help",
                "description": "Show OpenClaw help and available commands",
                "usage": "openclaw help"
            },
            {
                "name": "openclaw gateway start",
                "description": "Start OpenClaw gateway daemon",
                "usage": "openclaw gateway start"
            },
            {
                "name": "openclaw gateway stop",
                "description": "Stop OpenClaw gateway daemon",
                "usage": "openclaw gateway stop"
            },
            {
                "name": "openclaw gateway status",
                "description": "Check gateway daemon status",
                "usage": "openclaw gateway status"
            },
            {
                "name": "python3 -m venv",
                "description": "Create Python virtual environment",
                "usage": "python3 -m venv /path/to/venv"
            },
            {
                "name": "pip install",
                "description": "Install Python packages",
                "usage": "pip install package-name"
            },
            {
                "name": "source activate",
                "description": "Activate Python virtual environment",
                "usage": "source /path/to/venv/bin/activate"
            }
        ]

        print(f"Found {len(commands)} commands")

        for cmd in commands:
            text = f"Command: {cmd['name']}\nDescription: {cmd['description']}\nUsage: {cmd['usage']}"
            embedding = self._embed(text)

            self.commands_col.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[{
                    "name": cmd['name'],
                    "description": cmd['description'],
                    "usage": cmd['usage'],
                    "indexed_at": datetime.now().isoformat()
                }],
                ids=[f"cmd_{cmd['name'].replace(' ', '_')}"]
            )

            print(f"  ✅ Indexed: {cmd['name']}")

    def search_commands(self, query, n_results=10):
        """Cari commands."""
        query_embedding = self._embed(query)

        results = self.commands_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    # ==================== CONTEXT ====================

    def index_context(self, context_dir="/home/openclaw/.openclaw/workspace"):
        """Index context files (SOUL.md, USER.md, etc.)."""
        print(f"🔍 Indexing context from {context_dir}...")

        context_files = [
            "SOUL.md",
            "USER.md",
            "IDENTITY.md",
            "AGENTS.md",
            "TOOLS.md"
        ]

        for ctx_file in context_files:
            ctx_path = Path(context_dir) / ctx_file

            if ctx_path.exists():
                with open(ctx_path, 'r') as f:
                    content = f.read()

                text = f"{ctx_file}\n{content}"
                embedding = self._embed(text)

                self.context_col.add(
                    documents=[text],
                    embeddings=[embedding],
                    metadatas=[{
                        "file": ctx_file,
                        "indexed_at": datetime.now().isoformat()
                    }],
                    ids=[f"ctx_{ctx_file}"]
                )

                print(f"  ✅ Indexed: {ctx_file}")

    def search_context(self, query, n_results=10):
        """Cari context."""
        query_embedding = self._embed(query)

        results = self.context_col.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results

    # ==================== GLOBAL SEARCH ====================

    def global_search(self, query, collections=None, n_results=10):
        """Search across all collections."""
        query_embedding = self._embed(query)

        if collections is None:
            collections = {
                "skills": self.skills_col,
                "tools": self.tools_col,
                "memory": self.memory_col,
                "commands": self.commands_col,
                "context": self.context_col
            }

        all_results = {}

        for col_name, col in collections.items():
            results = col.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )

            all_results[col_name] = results

        return all_results

    def clear_all(self):
        """Clear all collections."""
        self.client.delete_collection("skills")
        self.client.delete_collection("tools")
        self.client.delete_collection("memory")
        self.client.delete_collection("commands")
        self.client.delete_collection("context")
        print("✅ All collections cleared")

def main():
    parser = argparse.ArgumentParser(description='OpenClaw ChromaDB Global Integration')
    parser.add_argument('action', choices=[
        'index-all', 'index-skills', 'index-tools', 'index-memory',
        'index-commands', 'index-context',
        'search-skills', 'search-tools', 'search-memory',
        'search-commands', 'search-context', 'search-all',
        'clear-all'
    ], help='Action')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--n-results', type=int, default=10, help='Number of results')
    parser.add_argument('--db-path', default='/home/openclaw/.openclaw/chroma_db', help='Database path')

    args = parser.parse_args()

    # Initialize DB
    try:
        db = OpenClawChromaDB(args.db_path)
    except ImportError as e:
        print(f"❌ {e}")
        sys.exit(1)

    print("="*80)
    print("OPENCLOW CHROMADB GLOBAL INTEGRATION")
    print("="*80)
    print(f"Action: {args.action}")
    print(f"DB Path: {args.db_path}")
    print("="*80)
    print()

    # Execute action
    if args.action == 'index-all':
        # Index everything
        print("\n[1/5] Indexing Skills...")
        db.index_skills()

        print("\n[2/5] Indexing Tools...")
        db.index_tools()

        print("\n[3/5] Indexing Memory...")
        db.index_memory()

        print("\n[4/5] Indexing Commands...")
        db.index_commands()

        print("\n[5/5] Indexing Context...")
        db.index_context()

        print("\n" + "="*80)
        print("✅ ALL INDEXED SUCCESSFULLY!")
        print("="*80)

    elif args.action == 'search-all':
        # Global search
        if not args.query:
            print("❌ --query is required for search")
            sys.exit(1)

        results = db.global_search(args.query, n_results=args.n_results)

        print(f"\n🔍 GLOBAL SEARCH: '{args.query}'")
        print("="*80)

        for col_name, col_results in results.items():
            if col_results['ids'] and col_results['ids'][0]:
                print(f"\n📁 {col_name.upper()}:")
                print("-"*80)

                for i, (doc_id, doc, metadata) in enumerate(zip(
                    col_results['ids'][0],
                    col_results['documents'][0],
                    col_results['metadatas'][0]
                )):
                    print(f"{i+1}. {doc_id}")
                    print(f"   {doc[:200]}...")

    elif args.action == 'search-skills':
        results = db.search_skills(args.query, n_results=args.n_results)

        print(f"\n🔍 SEARCH SKILLS: '{args.query}'")
        print("="*80)

        for i, (doc_id, doc, metadata) in enumerate(zip(
            results['ids'][0],
            results['documents'][0],
            results['metadatas'][0]
        )):
            print(f"{i+1}. {doc_id}")
            print(f"   {doc[:200]}...")

    elif args.action == 'clear-all':
        db.clear_all()

    else:
        print(f"❌ Unknown action: {args.action}")

    print()
    print("="*80)
    print("COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
