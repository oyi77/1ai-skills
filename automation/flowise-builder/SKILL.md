---
name: flowise-builder
description: Flowise visual LLM workflow builder — drag-drop chatflows, API endpoints, document loaders, tools
domain: automation
tags:
- api
- automation
- builder
- flowise
- productivity
- workflow
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
**Trigger phrases:**
- "flowise builder"
- "Flowise visual LLM workflow builder — drag-drop chatflows, API endpoints, docume"


- Building LLM apps without writing code
- Prototyping RAG chatbots quickly
- Needing visual workflow design for AI pipelines
- Deploying AI chatbots as APIs or website widgets
- Self-hosting AI infrastructure

## When NOT to Use

- Task requires custom AI model training (use ML tools)
- You need complex AI agent logic (use LangChain directly)
- Task is about data processing, not AI app building
- You don't have Flowise instance running
- Task requires real-time AI inference (use dedicated AI services)
- You need to build a custom AI application (use development tools)

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

- Not testing flows before deployment
- Ignoring error handling in flows
- Missing logging and monitoring
- Not documenting flow logic
- Ignoring rate limits and quotas

## Verification

- [ ] Flows are tested end-to-end
- [ ] Error handling is in place
- [ ] Logging and monitoring are configured
- [ ] Flow logic is documented
- [ ] Rate limits are respected

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "Manual is faster for one-off tasks" | One-off tasks become recurring. Automate early, save time later. |
| "I will add error handling later" | You never do. Handle errors from day one. |
| "Automation is overkill" | If you do it twice, automate it. If you do it daily, it is critical infrastructure. |