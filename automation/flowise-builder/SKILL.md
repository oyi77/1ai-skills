---
name: flowise-builder
description: Flowise visual LLM workflow builder — drag-drop chatflows, API endpoints, document loaders, tools
---

## Overview

Flowise is an open-source visual tool for building LLM workflows. It provides a drag-drop interface to connect LLMs, document loaders, vector stores, tools, and chains — then deploy as API endpoints.

## Capabilities

- Build chatflows visually with drag-drop nodes
- Connect to OpenAI, Anthropic, Ollama, and local models
- Add document loaders (PDF, web, CSV, Notion)
- Integrate vector stores (Pinecone, FAISS, Chroma, Qdrant)
- Add tools (web search, calculator, API calls)
- Deploy as REST API with streaming support
- Embed chatbot widget in websites

## When to Use

- Building LLM apps without writing code
- Prototyping RAG chatbots quickly
- Needing visual workflow design for AI pipelines
- Deploying AI chatbots as APIs or website widgets
- Self-hosting AI infrastructure

## Pseudo Code

Implementation patterns for common use cases with this skill.


### Installation

```bash
# npm
npm install -g flowise
npx flowise start

# Docker
docker run -d -p 3000:3000 flowiseai/flowise

# Access at http://localhost:3000
```

### Chatflow Architecture

```
Document Loader → Text Splitter → Embedding → Vector Store
                                                    ↓
User Question → Embedding → Vector Store Retriever → LLM Chain → Response
```

### API Usage

```bash
# Prediction
curl -X POST http://localhost:3000/api/v1/prediction/{chatflow-id} \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the return policy?", "overrideConfig": {}}'

# Streaming
curl -X POST http://localhost:3000/api/v1/prediction/{chatflow-id} \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello", "streaming": true}'
```

### Embed Widget

```html
<script type="module">
  import Chatbot from "https://cdn.jsdelivr.net/npm/flowise-embed/dist/web.js"
  Chatbot.init({
    chatflowid: "your-chatflow-id",
    apiHost: "http://localhost:3000",
  })
</script>
```

### Node Configuration

| Node | Config |
|------|--------|
| ChatOpenAI | model, temperature, maxTokens, apiKey |
| OpenAIEmbeddings | modelName, apiKey |
| VectorStoreRetriever | topK, filter |
| TextSplitter | chunkSize, chunkOverlap |
| Calculator | — |
| RequestsGet | url, headers |
| CustomJS | code |

## Common Patterns

| Pattern | When to Use |
|---------|------------|
| Document Loader → Vector Store | Index knowledge base |
| Retriever → LLM Chain | RAG chatbot |
| Agent + Tools | Autonomous assistant |
| Conditional Branches | Different paths based on input |
| Memory | Multi-turn conversations |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| API key not set | Missing env var | Set OPENAI_API_KEY in .env |
| Vector store empty | Documents not indexed | Re-upload and process documents |
| Node connection error | Invalid node config | Check node settings in UI |
| Streaming not working | Missing streaming flag | Add `streaming: true` in API call |

## Red Flags

- Claiming completion without running verification
- Skipping the analysis phase and jumping to implementation
- Ignoring existing codebase patterns and conventions

## Verification

- [ ] Output matches the original requirements
- [ ] All code or content runs without errors
- [ ] Edge cases have been considered and handled
- [ ] No placeholder content or TODOs remain