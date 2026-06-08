---
name: rag-system
description: 'Skill: rag-system. See SKILL.md body for details. Use when this domain
  is relevant.'
domain: core
---
*This RAG system powers Vilona's memory. Every significant decision, lesson learned, and insight gets stored and retrieved automatically.*

## Architecture

The RAG pipeline follows a retrieve-then-read pattern:

1. **Embed** incoming queries using a sentence transformer
2. **Retrieve** top-k chunks from the vector store (Chroma, Pinecone, or pgvector)
3. **Rerank** results by relevance score using a cross-encoder
4. **Read** the reranked context and generate the answer with the LLM

## Key Configuration

| Parameter | Default | Notes |
|-----------|---------|-------|
| `chunk_size` | 512 tokens | Overlap by 50 tokens for context continuity |
| `top_k` | 5 | Retrieve more for complex queries |
| `rerank_threshold` | 0.7 | Below this, return no relevant context |
| `embedding_model` | `text-embedding-3-small` | Swap for domain-specific models |

## How to Use

1. Ingest documents into the vector store with appropriate chunking strategy
2. Configure retrieval parameters for your use case (top_k, threshold)
3. Test with representative queries to validate retrieval quality
4. Monitor retrieval accuracy and adjust embedding model if needed

## Red Flags

- Retrieval returns irrelevant chunks (low precision)
- Answers hallucinate despite available context
- Chunk boundaries split important information
- Embedding model mismatch between ingest and query time
- Stale vector store not updated after document changes
- No fallback when retrieval confidence is below threshold

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

