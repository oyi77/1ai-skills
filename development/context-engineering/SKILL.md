---
name: context-engineering
description: Use when design and manage the context window for AI coding agents. Structure
  prompts, manage file loading, and optimize token usage for maximum agent effectiveness.
  Use when designing and manage the context window for ai coding agents.
domain: development
author: oyi77
license: Apache-2.0
subdomain: software-development
tags:
- engineering
- context
- prompts
- ai-agents
- token-optimization
version: 1.0.0
category: development
---


# Context Engineering

## When to Use
**Trigger phrases:**
- "context engineering"
- "Design and manage the context window for AI coding agents"


- When setting up AI agent instructions for a project
- When optimizing agent performance on large codebases
- When managing context window limits for complex tasks
- When designing multi-agent systems with shared context

## When NOT to Use

- For simple one-off prompts
- When the codebase fits entirely in context

## Overview

Context Engineering is the practice of designing what information an AI agent sees and in what order. The right context produces correct output; the wrong context produces hallucinations.

## Workflow

1. **Map information needs** - What does the agent need to know?
2. **Prioritize** - Critical context first, nice-to-have last
3. **Structure** - AGENTS.md, .cursor/rules/, system prompts
4. **Manage loading** - Progressive disclosure, lazy loading
5. **Optimize tokens** - Compress, deduplicate, summarize
6. **Test** - Does the agent produce correct output with this context?

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "More context is always better" | Context window has limits. Noise degrades signal. Prioritize ruthlessly. |
| "The agent will figure it out" | Without explicit context, agents hallucinate patterns and APIs |
| "README is enough" | Agents need different context than humans - code structure, conventions, gotchas |

## Context Architecture

```markdown
# AGENTS.md (loaded first, always)
- Project overview (2-3 sentences)
- Key commands (test, build, lint)
- File structure map
- Coding conventions
- Known gotchas

# System prompt (agent-specific)
- Role definition
- Quality gates
- Anti-rationalization rules
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run context engineering workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] AGENTS.md is under 500 lines
- [ ] Key commands are copy-pasteable
- [ ] File structure map is accurate
- [ ] No redundant information across context files
- [ ] Agent produces correct output with this context

## Code Examples

### Python — Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4") -> int:
    """Count tokens for a given text and model."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))


def truncate_to_limit(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """Truncate text to fit within token limit, preserving complete tokens."""
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return encoding.decode(tokens[:max_tokens])


# Usage
prompt = "You are a senior engineer. Follow these rules..."
print(count_tokens(prompt))  # ~11 tokens
truncated = truncate_to_limit(prompt * 50, 200)
```

### Python — Context Window Manager with Priority Eviction

```python
class ContextManager:
    """Manages context window with priority-based eviction.
    
    Highest-priority content survives when the total exceeds max_tokens.
    """
    
    def __init__(self, max_tokens: int = 8000, model: str = "gpt-4"):
        self.max_tokens = max_tokens
        self.sections: list[dict] = []
        self._encoding = tiktoken.get_encoding("cl100k_base")
    
    def add(self, content: str, priority: int = 5):
        tokens = len(self._encoding.encode(content))
        self.sections.append({
            "content": content,
            "priority": priority,
            "tokens": tokens,
        })
        self._evict()
    
    def _evict(self):
        total = sum(s["tokens"] for s in self.sections)
        if total <= self.max_tokens:
            return
        self.sections.sort(key=lambda s: s["priority"])
        while total > self.max_tokens and self.sections:
            removed = self.sections.pop(0)
            total -= removed["tokens"]
    
    def build(self) -> str:
        """Assemble context string, highest priority first."""
        ordered = sorted(self.sections, key=lambda s: (-s["priority"], s["tokens"]))
        return "\n\n---\n\n".join(s["content"] for s in ordered)


# Usage
ctx = ContextManager(max_tokens=4000)
ctx.add("Project overview and architecture decisions", priority=10)
ctx.add("Full API reference with all endpoints", priority=5)
ctx.add("Historical changelog and edge cases", priority=1)
agent_prompt = ctx.build()
```

### Node.js — Token Counting

```javascript
import { encoding_for_model } from "tiktoken";

function countTokens(text, model = "gpt-4") {
  const enc = encoding_for_model(model);
  const count = enc.encode(text).length;
  enc.free(); // tiktoken requires explicit free
  return count;
}

function truncateToLimit(text, maxTokens, model = "gpt-4") {
  const enc = encoding_for_model(model);
  const tokens = enc.encode(text);
  if (tokens.length <= maxTokens) {
    enc.free();
    return text;
  }
  const result = enc.decode(tokens.slice(0, maxTokens));
  enc.free();
  return result;
}
```

### Node.js — Progressive Context Loader

```javascript
import { readFileSync } from "fs";
import { encoding_for_model } from "tiktoken";

class ProgressiveContext {
  constructor(maxTokens = 8000, model = "gpt-4") {
    this.maxTokens = maxTokens;
    this.enc = encoding_for_model(model);
    this.sections = [];
  }

  add(name, content, priority = 5) {
    const tokens = this.enc.encode(content).length;
    this.sections.push({ name, content, priority, tokens });
    this.sections.sort((a, b) => b.priority - a.priority);
  }

  /** Build prompt fitting within maxTokens, highest priority first */
  compile(separator = "\n\n---\n\n") {
    let result = "";
    for (const s of this.sections) {
      const candidate = result ? result + separator + s.content : s.content;
      if (this.enc.encode(candidate).length > this.maxTokens) break;
      result = candidate;
    }
    return result;
  }

  cleanup() {
    this.enc.free();
  }
}

// Usage
const ctx = new ProgressiveContext(6000);
ctx.add("rules", readFileSync("AGENTS.md", "utf-8"), 10);
ctx.add("types", readFileSync("types.d.ts", "utf-8"), 7);
ctx.add("docs", readFileSync("README.md", "utf-8"), 3);
const prompt = ctx.compile();
ctx.cleanup();
```

## Setup & Configuration

```bash
# Python — install tokenizer
pip install tiktoken

# Node.js — install tokenizer
npm install tiktoken
# lighter alternative with no WASM dependency
npm install gpt-tokenizer

# Verify installation works
python -c "import tiktoken; print(tiktoken.get_encoding('cl100k_base').encode('hello'))"
```

## Common Issues & Troubleshooting

| Problem | Solution |
|---|---|
| Context window exceeded mid-task | Break task into subtasks; use progressive disclosure; summarize intermediate results before continuing |
| Agent ignores instructions at end of prompt | Place critical instructions first (primacy effect); use AGENTS.md loaded at session start |
| Token count differs between environments | Use the same tokenizer library (tiktoken) everywhere; always specify the exact model name |
| File loading order affects output quality | Load critical-path files first; use dependency ordering, not alphabetical |
| Multi-turn context drift over long sessions | Re-inject core instructions every N turns (summary + system prompt re-insertion pattern) |
| Agent hallucinates file paths or APIs | Include an explicit file tree map and API surface summary in the context block |

## Monetization

- **Context audit consulting** — Charge $500-2000 per engagement to audit and optimize context setups for teams using AI coding agents. Identify wasted tokens, structural gaps, and priority misalignments across their AGENTS.md, rules files, and system prompts.
- **Template marketplace** — Sell project-specific context templates ($20-100 each) for popular stacks (Next.js, Django, FastAPI, Rails, Spring Boot) with pre-optimized token budgets, priority ordering, and file structure maps.
- **Training workshops** — Run 2-day remote workshops ($3000-8000) covering token economics, progressive disclosure design, multi-agent context sharing, CI-based context validation, and debugging session drift.
- **CI context validation SaaS** — Build a service that checks PRs for context health: token budgets, stale references, duplicate sections, priority inversions, and missing critical paths. $10-50/month per repo.
- **Internal tooling development** — Build custom context management tooling for enterprise teams: token budget dashboards, auto-summarization pipelines that compress verbose docs into agent-optimal chunks, and collaborative context editors with diff/review workflows.

