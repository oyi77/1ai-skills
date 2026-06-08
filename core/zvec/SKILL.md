---
name: zvec
description: ZVec Skill. Use when relevant to this domain.
persona:
  name: Mikolov et al.
  title: The Word2Vec Pioneers - Masters of Vector Embeddings
  expertise:
  - Word Embeddings
  - Vector Representations
  - Neural Networks
  - NLP
  philosophy: Words that appear in similar contexts have similar meanings.
  credentials:
  - Created Word2Vec at Google
  - Published landmark embedding papers
  - Enabled modern NLP
  principles:
  - Embed meaning
  - Capture semantic relationships
  - Train on large corpora
  - Visualize in 2D/3D
domain: core
---
# ZVec Skill

> Alibaba's lightweight in-process vector database - "The SQLite of Vector Databases"

## Overview

ZVec is an open-source, in-process vector database from Alibaba's Tongyi Lab. It's lightweight, blazing fast, and embeds directly into your application - no server needed. Built on Proxima (Alibaba's battle-tested vector search engine used in production across Taobao, Ele.me, and more).

## When to Use

Use this skill when you need:
- **Lightweight vector storage** with minimal setup
- **Fast local RAG** without external services
- **Edge AI** with on-device embeddings
- **Simple API** that "just works"
- **Production-grade** performance in a tiny package

## Key Features
- Automated workflow execution with error recovery
- Configurable parameters for different use cases
- Integration with existing tooling and pipelines
- Detailed logging and status reporting


### 🚀 Blazing Fast
- Searches billions of vectors in milliseconds
- Built on Alibaba's Proxima engine
- Optimized for low latency

### 📦 Simple, Just Works
- `pip install zvec` and start searching
- No servers, no config, no daemon
- Runs wherever your code runs

### 🌍 Runs Anywhere
- macOS (ARM64)
- Linux (x86_64, ARM64)
- Python 3.10-3.12
- Node.js support

### 🔍 Rich Query Support
- Dense and sparse vectors
- Hybrid search with filters
- Multiple index types (Flat, HNSW, IVF)

## Installation

```bash
# Python
pip install zvec

# Node.js
npm install @zvec/zvec
```

## Usage Patterns
- Invoke the skill when the matching domain keywords appear
- Combine with related skills for end-to-end workflows
- Use verification steps to confirm successful execution
- Review output quality before finalizing results


### Python Example
```python
import zvec

# Define collection schema
schema = zvec.CollectionSchema(
    name="example",
    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, 384)
)

# Create collection
collection = zvec.create("my_vectors", schema)

# Add vectors
collection.add(
    ids=["doc1", "doc2"],
    vectors=[[0.1] * 384, [0.2] * 384],
    payloads=[{"text": "AI is great"}, {"text": "Vectors are useful"}]
)

# Search
results = collection.search(
    query_vector=[0.1] * 384,
    top_k=10,
    filter={"text": {"$contains": "AI"}}
)
```

### Node.js Example
```javascript
const zvec = require('@zvec/zvec');

const collection = await zvec.create('documents', { dimension: 384 });
await collection.add({ id: '1', vector: embedding, payload: { text: 'Hello' } });
const results = await collection.search({ vector: queryEmbedding, topK: 5 });
```

## Index Types

| Type | Use Case | Latency | Accuracy |
|------|----------|---------|----------|
| Flat | Small datasets, exact results | Low | 100% |
| HNSW | Balanced speed/accuracy | Medium | ~95% |
| IVF | Large datasets | Fast | ~90% |

## Integration with 1ai-skills

ZVec integrates perfectly with:
- `faceless-youtube` - Video content embedding
- `ai-research-agent` - Document similarity search
- `content-generator` - Content deduplication

## When to Choose ZVec vs RuVector

| Feature | ZVec | RuVector |
|---------|------|----------|
| **Speed** | ⚡⚡⚡⚡⚡ | ⚡⚡⚡ |
| **Self-Learning** | ❌ | ✅ GNN |
| **Local LLM** | ❌ | ✅ |
| **Graph Queries** | ❌ | ✅ Cypher |
| **Complexity** | Simple | Advanced |
| **Size** | Tiny | Full-featured |

**Choose ZVec** for: Simple, fast, lightweight vector storage
**Choose RuVector** for: Self-learning memory, graph queries, local LLMs

## Files in This Skill

- `SKILL.md` - This file

## See Also

- [ZVec GitHub](https://github.com/alibaba/zvec)
- [ZVec Documentation](https://zvec.org/en/docs)
- [Benchmarks](https://zvec.org/en/docs/benchmarks)

## When NOT to Use

- When the task requires domain expertise the agent has not been configured with
- When human review is mandated by compliance or regulatory requirements
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Agent output is not validated against expected quality standards
- Prerequisites are not verified before task execution
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] All required outputs generated
- [ ] Success criteria met

