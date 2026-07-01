---
name: model-router
description: Route AI model requests to the optimal provider based on task, cost, latency, and capability requirements. Manage multi-provider LLM deployments. Use when working with model router.
domain: core
tags:
- ai
- llm
- routing
- multi-provider
- cost-optimization
- model-selection
---

# Model Router

## When to Use

**Trigger phrases:**
- "model router"
- "When managing multiple LLM providers (OpenAI, Anthropic, Google, etc"
- "When optimizing for cost vs quality tradeoffs"
- "When implementing fallback chains for reliability"


- When managing multiple LLM providers (OpenAI, Anthropic, Google, etc.)
- When optimizing for cost vs quality tradeoffs
- When implementing fallback chains for reliability
- When routing by task type (code to Claude, vision to Gemini, etc.)

## When NOT to Use

- For single-provider setups (just use that provider SDK)
- For local-only inference (use Ollama skills)

## Overview

Intelligent model routing that selects the best LLM for each task based on capability, cost, latency, and availability. Supports fallback chains, load balancing, and cost tracking.

## Workflow

1. **Define routes** — Task type to model mapping
2. **Configure providers** — API keys, endpoints, rate limits
3. **Set fallbacks** — Primary, secondary, tertiary model chain
4. **Track metrics** — Cost per request, latency, success rate
5. **Optimize** — A/B test models, adjust routing rules

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "One model is enough" | Different models excel at different tasks — routing optimizes quality |
| "I will use the cheapest model" | Cheap models fail on complex tasks — cost of failure exceeds savings |
| "Routing is over-engineering" | A 3-line fallback chain prevents 90% of LLM outages |

## Code Example (TypeScript)

```typescript
const routes: Record<string, string[]> = {
  code: ['claude-sonnet-4-20250514', 'gpt-4o', 'gemini-2.5-pro'],
  vision: ['gemini-2.5-pro', 'gpt-4o', 'claude-sonnet-4-20250514'],
  fast: ['gemini-2.5-flash', 'gpt-4o-mini', 'claude-haiku'],
  creative: ['gpt-4o', 'claude-opus-4-20250514', 'gemini-2.5-pro'],
};

async function routeRequest(task: string, prompt: string) {
  const models = routes[task] || routes.fast;
  for (const model of models) {
    try {
      return await callModel(model, prompt);
    } catch (e) {
      console.warn(`${model} failed, trying next...`);
    }
  }
  throw new Error('All models failed');
}
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run model router workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] Routes correctly by task type
- [ ] Fallback triggers on primary failure
- [ ] Cost tracking accurate per request
- [ ] Latency within acceptable bounds
- [ ] No single point of failure

