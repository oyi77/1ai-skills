---
name: memory-knowledge-graph
description: Knowledge graph-based persistent memory for AI agents — entities, relations, and semantic retrieval
---

## Overview

Persistent memory system using knowledge graphs for AI agents. Stores entities, relations, and observations as a graph, enabling semantic retrieval and reasoning over accumulated knowledge.

## Capabilities

- Extract entities and relations from conversations and documents
- Store knowledge as a graph (nodes + edges + observations)
- Retrieve relevant knowledge via semantic search and graph traversal
- Consolidate and deduplicate knowledge over time
- Query knowledge with natural language

## When to Use

- Building AI agents with long-term memory
- Need to remember user preferences, facts, and context across sessions
- Knowledge base that grows and improves over time
- Cross-referencing information across multiple sources

## Pseudo Code

### Entity Extraction
```python
def extract_entities(text):
    prompt = f"""Extract entities and relations from:
{text}

Return JSON: {{"entities": [{{"name": "...", "type": "...", "observations": [...]}}], "relations": [{{"from": "...", "to": "...", "type": "..."}}]}}"""
    return llm.generate(prompt)
```

### Knowledge Retrieval
```python
def retrieve_relevant(query, graph, top_k=5):
    # 1. Semantic search on entity names and observations
    semantic_results = graph.semantic_search(query, top_k=top_k)
    
    # 2. Graph traversal - get connected entities
    related = []
    for entity in semantic_results:
        related.extend(graph.get_neighbors(entity.id, depth=2))
    
    # 3. Deduplicate and rank
    return rank_by_relevance(semantic_results + related, query)
```

### Memory Consolidation
```python
def consolidate(graph):
    # Merge duplicate entities
    duplicates = find_similar_entities(graph, threshold=0.9)
    for dup_group in duplicates:
        merge_entities(graph, dup_group)
    
    # Remove stale observations
    for entity in graph.entities:
        entity.observations = [o for o in entity.observations if o.relevance > 0.3]
```

## Common Patterns

- **Extract on every interaction**: Build knowledge from every conversation
- **Semantic + graph traversal**: Combine vector search with graph walks for better retrieval
- **Consolidate periodically**: Merge duplicates and prune stale knowledge
- **Entity types**: Person, Organization, Concept, Event, Preference
