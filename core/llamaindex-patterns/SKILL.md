---
name: llamaindex-patterns
description: LlamaIndex data framework — ingestion, indexing, query engines, chat engines, agents
domain: core
tags:
- ai-agent
- infrastructure
- llamaindex
- memory
- patterns
- self-improvement
---

## Overview

LlamaIndex is a data framework for connecting LLMs with external data. It provides document loaders, vector stores, query engines, and chat engines for building RAG applications and knowledge-augmented agents.

## Capabilities

- Load documents from 160+ sources (PDF, Notion, Slack, databases)
- Build vector indices for semantic search
- Create query engines with retrieval and synthesis
- Build conversational chat engines with memory
- Use agents with tool use and multi-step reasoning
- Implement advanced RAG patterns (routing, fusion, recursive)

## When to Use

- Building RAG applications over custom data sources
- Needing structured document ingestion pipelines
- Wanting query engines with citations and source tracking
- Building chatbots over knowledge bases
- Implementing agentic RAG with tool use

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Document Ingestion

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Build index
index = VectorStoreIndex.from_documents(documents)
```

### Query Engine

```python
from llama_index.core import VectorStoreIndex
from llama_index.llms.openai import OpenAI

llm = OpenAI(model="gpt-4o", temperature=0)

index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(
    llm=llm,
    similarity_top_k=5,
    response_mode="compact",  # or "tree_summarize", "refine"
)

response = query_engine.query("What are the company's revenue streams?")
print(response.response)
print(response.source_nodes)  # Citations
```

### Chat Engine

```python
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",  # or "context", "condense", "simple"
    llm=llm,
    similarity_top_k=3,
)

# Multi-turn conversation
response1 = chat_engine.chat("What is the return policy?")
response2 = chat_engine.chat("What about international orders?")  # Has context
```

### Custom Document Loaders

```python
from llama_index.core import Document

# From database
import pandas as pd
df = pd.read_sql("SELECT * FROM articles", con=engine)
documents = [
    Document(text=row['content'], metadata={"id": row['id'], "title": row['title']})
    for _, row in df.iterrows()
]

index = VectorStoreIndex.from_documents(documents)
```

### Vector Store Integrations

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext

# Pinecone
vector_store = PineconeVectorStore(
    index_name="my-index",
    environment="us-east1-gcp",
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Qdrant
from llama_index.vector_stores.qdrant import QdrantVectorStore
import qdrant_client

client = qdrant_client.QdrantClient(host="localhost", port=6333)
vector_store = QdrantVectorStore(client=client, collection_name="docs")
```

### Agent with Tools

```python
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import QueryEngineTool, FunctionTool

# Tool from query engine
query_tool = QueryEngineTool.from_defaults(
    query_engine=query_engine,
    name="document_search",
    description="Search company documents for information",
)

# Custom tool
def multiply(a: float, b: float) -> float:
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

# Agent
agent = ReActAgent.from_tools(
    tools=[query_tool, multiply_tool],
    llm=llm,
    verbose=True,
)

response = agent.chat("Find the Q3 revenue and multiply by 1.1 for Q4 projection")
```

### Advanced RAG: Router Query Engine

```python
from llama_index.core.query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

# Multiple query engines
vector_engine = index.as_query_engine()
summary_engine = index.as_query_engine(response_mode="tree_summarize")

router = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engines=[vector_engine, summary_engine],
    select_multi=False,
)

response = router.query("Summarize all quarterly reports")
```

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| `SimpleDirectoryReader` | Load files from disk |
| `VectorStoreIndex` | Build searchable index |
| `as_query_engine()` | Single question + answer |
| `as_chat_engine()` | Multi-turn conversation |
| `ReActAgent` | Agent with tool reasoning |
| `RouterQueryEngine` | Route to best engine automatically |
| `response_mode="compact"` | Concise answers |
| `response_mode="tree_summarize"` | Summarize across many documents |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `IndexEmpty` | No documents loaded | Check directory path and file types |
| `Response incomplete` | Too few source nodes | Increase `similarity_top_k` |
| Embedding dimension mismatch | Wrong model | Use consistent embedding model |
| Token limit during synthesis | Too many nodes retrieved | Reduce `similarity_top_k` or use `compact` mode |

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
