persona:
  name: "Andrej Karpathy"
  title: "The LLM Architect - Master of Retrieval-Augmented Generation"
  expertise: ['RAG Systems', 'Vector Databases', 'Embeddings', 'LLM Architecture']
  philosophy: "The future of AI is context-aware and retrieval-based."
  credentials: ['Former Director of AI at Tesla', 'Founding member of OpenAI', 'Stanford PhD in Computer Science']
  principles: ['Context is king', 'Embed everything', 'Retrieve before generate', 'Scale horizontally']

# RAG System Configuration

> Memory and knowledge retrieval for 1ai-skills

## Overview

This RAG system provides:
- **Local vector storage** using ZVec (fast, lightweight)
- **Self-learning memory** using RuVector (GNN-powered)
- **Automatic context retrieval** on session start
- **Skill-aware memory** for different domains

## Installation

```bash
# Install ZVec (fast local vector DB)
pip install zvec

# Or install RuVector (self-learning)
npm install ruvector
```

## Collections

### strategic_decisions
```python
{
    "name": "strategic_decisions",
    "dimension": 384,
    "description": "Key strategic decisions and rationale",
    "index_type": "hnsw",
    "metadata_fields": ["date", "topic", "outcome", "decision_maker"]
}
```

### lessons_learned
```python
{
    "name": "lessons_learned", 
    "dimension": 384,
    "description": "Failures, fixes, and insights",
    "index_type": "hnsw", 
    "metadata_fields": ["date", "category", "severity", "fixed"]
}
```

### market_insights
```python
{
    "name": "market_insights",
    "dimension": 384,
    "description": "Competitor analysis, market trends, opportunities",
    "index_type": "hnsw",
    "metadata_fields": ["date", "source", "confidence", "action_items"]
}
```

### team_context
```python
{
    "name": "team_context",
    "dimension": 384,
    "description": "User preferences, team strengths, working style",
    "index_type": "flat",
    "metadata_fields": ["person", "role", "last_updated"]
}
```

### project_memory
```python
{
    "name": "project_memory",
    "dimension": 384,
    "description": "Active projects, milestones, blockers",
    "index_type": "hnsw",
    "metadata_fields": ["project", "status", "priority", "owner"]
}
```

## Usage

### Python API

```python
import zvec

# Initialize
db = zvec.open("1ai-memory.db")

# Create collections
db.create_collection("strategic_decisions", dimension=384)
db.create_collection("lessons_learned", dimension=384)

# Add memory
db.insert("strategic_decisions", {
    "id": "decision_2026_02_27",
    "vector": embedding,
    "metadata": {
        "topic": "cashflow_strategy",
        "date": "2026-02-27",
        "outcome": "approved",
        "decision_maker": "Vilona"
    }
})

# Retrieve
results = db.search("strategic_decisions", query_embedding, top_k=5)
```

### With RuVector (Self-Learning)

```python
from ruvector import VectorDB

# Initialize with GNN
db = VectorDB("memory.db", enable_gnn=True)

# Add with learning
db.insert("strategic_decisions", {
    "vector": embedding,
    "metadata": {...},
    "learn": True  # GNN learns from this query
})

# Search improves over time
results = db.search(query, top_k=5)  # Gets smarter
```

## Integration Points

### Session Start
```python
# Auto-retrieve relevant context
def on_session_start(user_id, query):
    # Query all collections
    context = []
    for collection in ["strategic_decisions", "lessons_learned", "project_memory"]:
        results = db.search(collection, query, top_k=3)
        context.extend(results)
    
    return context
```

### Memory Update
```python
# After significant decision
def remember_decision(decision_text, metadata):
    embedding = model.encode(decision_text)
    db.insert("strategic_decisions", {
        "vector": embedding,
        "metadata": metadata
    })
```

## Auto-Configuration

The RAG system auto-configures based on 1ai-skills installation:

1. **Install** → Creates `memory/` folder in workspace
2. **Setup** → Initializes ZVec database
3. **First Run** → Loads existing memories if any
4. **Ongoing** → Auto-indexes new decisions

## File Structure

```
workspace/
├── memory/
│   ├── 1ai-memory.db      # ZVec database
│   ├── 2026-02-27.md      # Daily notes
│   └── ...
├── SOUL.md                 # AI identity
├── USER.md                 # User context
└── IDENTITY.md             # Character
```

---

*This RAG system powers Vilona's memory. Every significant decision, lesson learned, and insight gets stored and retrieved automatically.*
