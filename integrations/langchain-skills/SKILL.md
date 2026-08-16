---
name: langchain-skills
description: Use when building agents with LangChain, LangGraph, or Deep Agents. 21 skills covering ecosystem primer, quickstarts, Deep Agents (memory, orchestration, managed), LangChain (fundamentals, middleware, RAG), LangGraph (fundamentals, persistence, CLI, human-in-the-loop), evaluation (Harbor), and utilities (swarm).
category: integrations
domain: integrations
tags:
  - langchain
  - langgraph
  - deep-agents
  - agent-engineering
  - harbor-evaluation
  - rag
  - multi-agent
version: 1.0.0
---

# LangChain Skills: Agent Engineering with LangChain, LangGraph & Deep Agents

Official agent skills from LangChain for building production-grade LLM applications. 21 skills covering the full stack from fundamentals to managed deployment.

---

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "I'll just use raw LLM calls" | Raw calls lack observability, memory, streaming, and eval infrastructure | Use LangGraph for stateful agents, LangSmith for tracing |
| "LangChain is too heavy" | Core is modular; use only what you need (create_agent, StateGraph, checkpointers) | Import specific modules, not the whole framework |
| "I don't need evals" | Evals catch regressions before production; Harbor makes it systematic | Run eval-engineering skill to set up Harbor evals |
| "Deep Agents are overkill" | Deep Agents add planning, subagents, filesystem - essential for complex tasks | Use Deep Agents when task needs multi-step planning + tools |
| "I'll write my own RAG" | RAG has 50+ failure modes; langchain-rag skill covers loaders, embeddings, vector stores | Use the skill; customize only the retrieval strategy |

---

## When to Use

**Use when you need to:**

- **Start a new agent project** → `ecosystem-primer` (framework selection: LangChain vs LangGraph vs Deep Agents)
- **Quick prototype** → Quickstart skills (weather bot, math agent, research agent)
- **Build Deep Agents** → `deep-agents-core`, `deep-agents-memory`, `deep-agents-orchestration`, `managed-deep-agents`
- **Build LangChain agents** → `langchain-fundamentals`, `langchain-middleware`, `langchain-rag`
- **Build LangGraph workflows** → `langgraph-fundamentals`, `langgraph-persistence`, `langgraph-cli`, `langgraph-human-in-the-loop`
- **Evaluate agents** → `eval-engineering` (Harbor evals with user approval)
- **Parallelize independent work** → `swarm` (dispatch + aggregate)

---

## Workflow

1. **Select Framework** — Run `ecosystem-primer` to choose LangChain / LangGraph / Deep Agents
2. **Verify Setup** — Run appropriate quickstart (weather, math, or research agent)
3. **Configure API Keys** — Set `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY`
4. **Load Framework Skill** — Load skill matching your framework choice
5. **Build & Test** — Develop agent with framework-specific patterns
6. **Evaluate (Production)** — Use `eval-engineering` to set up Harbor evals
7. **Deploy** — Use `managed-deep-agents` or `langgraph-cli` for deployment

---

## Quick Start

### Install All Skills (via npx)
```bash
# Local (current project)
npx skills add langchain-ai/langchain-skills --skill '*' --yes

# Global (all projects)
npx skills add langchain-ai/langchain-skills --skill '*' --yes --global

# Link to specific agent (e.g., Claude Code)
npx skills add langchain-ai/langchain-skills --agent claude-code --skill '*' --yes --global
```

### Install via Script (Claude Code & Deep Agents CLI)
```bash
# Clone and install
git clone https://github.com/langchain-ai/langchain-skills
cd langchain-skills

# Install for Claude Code in current directory
./install.sh

# Install for specific project
./install.sh ~/my-project

# Install globally
./install.sh --global

# Install for Deep Agents CLI
./install.sh --deepagents ~/my-project

# Install globally for Deep Agents (includes agent persona)
./install.sh --deepagents --global
```

### Required API Keys
```bash
export OPENAI_API_KEY=<your-key>      # For OpenAI models
export ANTHROPIC_API_KEY=<your-key>   # For Anthropic models
```

---

## Available Skills (21)

### Getting Started
| Skill | Description |
|-------|-------------|
| `ecosystem-primer` | **Start here.** Framework selection (LangChain vs LangGraph vs Deep Agents), env setup, which skill to load next |
| `langchain-dependencies` | Full package version and dependency management reference (Python + TypeScript) |

### Quickstarts (Local)
| Skill | Description |
|-------|-------------|
| `langchain-python-quickstart` | Python weather agent (default: anthropic:claude-sonnet-5) |
| `langchain-typescript-quickstart` | TypeScript weather agent |
| `langgraph-python-quickstart` | Python math agent |
| `langgraph-typescript-quickstart` | TypeScript math agent |
| `deepagents-python-quickstart` | Python research agent (web search) |
| `deepagents-typescript-quickstart` | TypeScript research agent |

### Deep Agents
| Skill | Description |
|-------|-------------|
| `deep-agents-core` | Agent architecture, harness setup, SKILL.md format |
| `deep-agents-memory` | Memory, persistence, filesystem middleware |
| `deep-agents-orchestration` | Subagents, task planning, human-in-the-loop |
| `managed-deep-agents` | Deploy with CLI, use SDKs, stream runs, connect MCP tools, build React useStream UIs |

### LangChain
| Skill | Description |
|-------|-------------|
| `langchain-fundamentals` | Agents with create_agent, tools, structured output, middleware basics |
| `langchain-middleware` | Human-in-the-loop approval, custom middleware, Command resume patterns |
| `langchain-rag` | RAG pipeline: document loaders, embeddings, vector stores |

### LangGraph
| Skill | Description |
|-------|-------------|
| `langgraph-fundamentals` | StateGraph, nodes, edges, state reducers |
| `langgraph-persistence` | Checkpointers, thread_id, cross-thread memory |
| `langgraph-cli` | CLI lifecycle: scaffold, dev, build, deploy, langgraph.json config |
| `langgraph-human-in-the-loop` | Interrupts, human review, approval workflows |

### Evaluation
| Skill | Description |
|-------|-------------|
| `eval-engineering` | Build, run, and audit Harbor evals for existing agent with user approval |

### Utilities
| Skill | Description |
|-------|-------------|
| `swarm` | Dispatch independent work items in parallel and aggregate results |

---

## Framework Selection Guide

| Use Case | Recommended Framework | Start With Skill |
|----------|----------------------|------------------|
| Simple tool-calling agent | LangChain | `langchain-fundamentals` |
| Stateful multi-turn conversation | LangGraph | `langgraph-fundamentals` |
| Complex planning + subagents + filesystem | Deep Agents | `deep-agents-core` |
| Need eval/monitoring in prod | LangSmith + Harbor | `eval-engineering` |
| Quick prototype (weather, math, research) | Any | Quickstart skills |

---

## Verification Checklist

- [ ] Choose framework via `ecosystem-primer`
- [ ] Run appropriate quickstart to verify setup
- [ ] Install API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY)
- [ ] Load framework-specific skill for your use case
- [ ] For production: set up `eval-engineering` with Harbor
- [ ] For complex tasks: use `deep-agents-orchestration` for subagents
- [ ] For stateful workflows: use `langgraph-persistence` with checkpointers

---

## References

- **GitHub Repository**: https://github.com/langchain-ai/langchain-skills
- **Documentation**: https://langchain-ai.github.io/langgraph/
- **LangSmith Platform**: https://smith.langchain.com/
- **Harbor Evaluation**: https://github.com/langchain-ai/harbor
- **Deep Agents**: https://github.com/langchain-ai/deepagents
- **LangChain Academy**: https://academy.langchain.com/
- **License**: MIT

---

## Related 1ai-skills

- `langchain-patterns` — LangChain/LangGraph patterns: chains, agents, tools, memory, retrieval, graph workflows
- `langgraph-fundamentals` — LangGraph state machines, nodes, edges, reducers (if available)
- `rag-builder` — RAG pipeline design: chunking, embedding, retrieval, answer generation
- `agent-harness-optimizer` — Agent harness optimization for token efficiency, memory persistence
- `model-router` — Route AI model requests to optimal provider