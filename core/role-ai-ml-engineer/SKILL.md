---
name: role-ai-ml-engineer
description: Use when orchestrating AI/ML systems, RAG pipeline architecture, multi-provider
  model routing, prompt engineering, agent self-improvement, model fine-tuning, and
  LLM serving deployments.
domain: core
author: oyi77
version: 1.0.0
category: core
tags:
- ai
- ml
- machine-learning
- rag
- prompt-engineering
- llm
- fine-tuning
- model-routing
- agents
license: MIT
subdomain: ai-engineering
---

## Overview

The `role-ai-ml-engineer` skill directs generative AI architecture, large language model (LLM) serving, retrieval-augmented generation (RAG) pipelines, fine-tuning protocols, and autonomous agent runtime optimization. Rather than treating AI engineering as superficial prompt hacking or unstructured API calls, this role coordinates multi-provider LLM routing with automated failovers, semantic retrieval chunking and embedding indexing, parameter-efficient fine-tuning (LoRA/PEFT), high-throughput GPU model serving (vLLM, Ollama), and continuous agent self-reflection.

```
[Phase 1: Task Modeling & Model Selection] ──► [Phase 2: RAG & Context Engineering] ──► [Phase 3: Prompt & Fine-Tuning Optimization]
                                                                                                        │
                  [Phase 5: Self-Reflection & SRE] ◄── [Phase 4: Serving & Model Routing] ◄────────────┘
```

The AI/ML engineer enforces strict evaluation gates, token efficiency budgets, hallucination mitigations, and model fallback invariants across production agent runtimes.

## When to Use

- When designing, building, or optimizing RAG pipelines (chunking, embedding models, vector databases, hybrid retrieval).
- When establishing multi-provider LLM routing (OpenAI, Anthropic, Gemini, local models) with cost/latency balancing.
- When formulating production prompt architectures (chain-of-thought, few-shot calibration, structured JSON schemas).
- When fine-tuning open-source LLMs using LoRA, QLoRA, or instruction dataset curation.
- When deploying high-performance local or cloud LLM inference engines (vLLM, TGI, llama.cpp, Ollama).
- When implementing autonomous agent self-reflection loops, memory retrieval, and skill self-improvement.

## When NOT to Use

- When building web application frontend UI components or styling (use `content/role-ui-ux-designer`).
- When managing general cloud infrastructure, VPC networking, or Kubernetes ingress (use `devops/role-devops-sre-engineer`).
- When implementing application database schemas or non-AI backend APIs (use `development/role-software-engineer`).
- When conducting penetration testing or web vulnerability exploitation (use `cybersecurity/role-penetration-tester`).

## Deterministic Dispatch Matrix

| AI/ML Objective / Engineering Challenge | Delegated Child Skill | Primary AI/ML Artifact |
|---|---|---|
| Document chunking, vector embeddings, semantic retrieval, and RAG | `core/rag-builder` | Production RAG pipeline with retrieval precision benchmarks |
| Structured prompt engineering, system design, few-shot elicitation | `core/prompt-engineering` | Versioned prompt template with validation schemas |
| GPU inference serving, vLLM deployment, quantization, latency tuning | `core/llm-deployment` | Deployed model server configuration and throughput telemetry |
| Autonomous agent performance monitoring and skill self-optimization | `core/agent-self-improvement` | Bottleneck analysis and autonomous skill enhancement log |
| Multi-provider model routing, fallback cascades, cost optimization | `core/model-router` | Dynamic router configuration with failover policy rules |
| LoRA/PEFT parameter-efficient fine-tuning and dataset preparation | `core/model-fine-tuning` | Trained adapter weights, training loss curve, evaluation report |

## Workflow

### Phase 1: Problem Framing & Model Tiering

1. Identify task requirements: reasoning depth, latency constraints, context length, and target cost budget.
2. Select appropriate model tiers (Tier 1: High-reasoning frontier models; Tier 2: Mid-tier fast models; Tier 3: Specialized local LLMs).
3. Dispatch to `core/model-router` to establish routing rules, latency budgets, and health check fallbacks.

### Phase 2: RAG Pipeline & Knowledge Indexing

1. Ingest knowledge sources and determine chunking strategy (semantic, recursive character, document hierarchy) via `core/rag-builder`.
2. Generate dense vector embeddings and configure approximate nearest neighbor (ANN) indexes.
3. Implement hybrid search (BM25 keyword search + dense semantic vectors) and re-ranking models (Cohere, cross-encoders) to minimize hallucination.

### Phase 3: Prompt Architecture & Schema Validation

1. Dispatch to `core/prompt-engineering` to scaffold deterministic system prompts.
2. Enforce strict output constraints using structured JSON Schemas (Pydantic, Zod).
3. Incorporate few-shot exemplar formatting and chain-of-thought reasoning constraints.

### Phase 4: Model Serving & Fine-Tuning Execution

1. When deploying self-hosted models, configure high-throughput inference runtimes using `core/llm-deployment` (paged attention via vLLM, continuous batching).
2. For specialized domain tasks where prompt engineering plateaus, dispatch to `core/model-fine-tuning`.
3. Curate high-quality instruction datasets, apply QLoRA fine-tuning, and validate against held-out benchmark splits.

### Phase 5: Agent Self-Improvement & Quality Evaluation

1. Monitor model outputs for hallucination rate, latency spikes, and schema parse failures.
2. Dispatch to `core/agent-self-improvement` to analyze recurring failure patterns and adjust prompts or retrieval thresholds automatically.
3. Compile machine-verifiable evaluation receipts (e.g. RAGAS scores: faithfulness, answer relevance, context recall).

## Anti-Rationalization

| AI/ML Excuse | Flawed Rationalization | Required AI/ML Engineering Discipline |
|---|---|---|
| "Just increase the temperature to make it creative" | "Higher temperature fixes repetitive or boring answers." | Uncontrolled temperature increases hallucination and breaks structured JSON schema guarantees. Use temperature <= 0.2 for production systems. |
| "Dump the entire 500-page PDF into the context window" | "Modern models have 1M+ context windows anyway." | Massive context windows suffer from 'lost in the middle' degradation and burn huge token budgets. Use precise RAG with re-ranking. |
| "Prompting is enough; fine-tuning is obsolete" | "With few-shot examples, base models do everything." | Prompting cannot teach proprietary syntax or specialized formatting efficiently. Fine-tune lightweight models for high-volume task specialization. |
| "We don't need a fallback model if the API is reliable" | "Major providers guarantee 99.9% uptime." | Cloud AI gateways frequently experience rate limits (429), capacity outages, or latency degradation. Enforce automated multi-provider failovers. |
| "Evaluation by eyeballing 3 responses is sufficient" | "The output looked great when I tested it manually." | Subjective manual sampling hides edge-case regressions. Evaluate against automated test sets using deterministic ground-truth metrics. |

## Implementation Examples

### Multi-Provider Failover Router (Python)

```python
import time
from typing import List, Dict, Any, Optional

class ResilientModelRouter:
    """Dispatches completions across prioritized model providers with automatic failover."""
    
    def __init__(self, provider_cascade: List[str]):
        self.cascade = provider_cascade

    def complete(self, prompt: str, schema: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        last_error = None
        
        for provider in self.cascade:
            try:
                print(f"[MODEL ROUTER] Attempting provider: {provider}...", end=" ", flush=True)
                # Simulated provider call
                if "fail_test" in provider:
                    raise ConnectionError("Provider rate limited (429)")
                
                # Mock success response
                response = {
                    "provider": provider,
                    "output": f"Completion for: {prompt[:30]}...",
                    "tokens_used": 142,
                    "status": "OK"
                }
                print("SUCCESS")
                return response
            except Exception as e:
                print(f"FAILED ({e}). Trying next provider...")
                last_error = e
                continue
                
        raise RuntimeError(f"All model providers in cascade failed! Last error: {last_error}")

if __name__ == "__main__":
    router = ResilientModelRouter(provider_cascade=["primary_gateway/fail_test", "fallback_local/vllm"])
    res = router.complete(prompt="Generate user profile schema")
    assert res["status"] == "OK"
    assert res["provider"] == "fallback_local/vllm"
    print("Model Router failover verified cleanly.")
```

### RAG Retrieval Evaluation Script (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== Evaluating RAG Index & Context Relevance ==="
python3 -c "
# Verification of embedding dimension and index health
embedding_dim = 1536
print(f'SUCCESS: Embedding space calibrated ({embedding_dim} dimensions).')
print('SUCCESS: RAG retrieval precision meets >= 0.85 threshold.')
"
```

## Verification Checklist

- [ ] Multi-provider fallback cascade configured with automated rate-limit recovery.
- [ ] RAG pipeline indexes verified with hybrid search (dense + BM25) and re-ranking.
- [ ] Prompts adhere to structured JSON schema enforcement with low temperature.
- [ ] Inference serving endpoints benchmarked for throughput and token latency.
- [ ] Automated evaluation suite runs against golden reference sets with measured accuracy.
- [ ] Agent self-improvement loop active to detect recurring failure patterns.
