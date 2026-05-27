---
name: llm-deployment
description: LLM deployment and serving — vLLM, Ollama, TGI, llama.cpp. Model quantization, GPU optimization, API serving
---

## Overview

Running LLMs in production — local inference with Ollama/llama.cpp to high-throughput serving with vLLM/TGI. Quantization, GPU optimization, OpenAI-compatible APIs.

## Capabilities

- Local deployment (Ollama, llama.cpp, LM Studio)
- High-throughput serving (vLLM, TGI)
- Quantization (GGUF, GPTQ, AWQ)
- GPU memory optimization (FlashAttention, PagedAttention)
- OpenAI-compatible API endpoints

## When to Use

- Self-hosted LLM for privacy/cost
- High-throughput API serving
- Running on consumer GPUs (24GB or less)

## Pseudo Code

### Ollama
```bash
ollama pull llama3.1:8b && ollama serve
curl http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","prompt":"Hello!","stream":false}'
```

### vLLM
```bash
python -m vllm.entrypoints.openai.api_server --model meta-llama/Llama-3.1-8B-Instruct --tensor-parallel-size 2
# Use: OpenAI(base_url="http://localhost:8000/v1", api_key="dummy")
```

### llama.cpp
```bash
cmake -B build -DGGML_METAL=ON && cmake --build build -j
./build/bin/llama-server -m model.gguf --host 0.0.0.0 --port 8080 -ngl 99
```

### Quantize
```python
# GPTQ
from transformers import AutoModelForCausalLM, GPTQConfig
model = AutoModelForCausalLM.from_pretrained("model", quantization_config=GPTQConfig(bits=4))
```

## Common Patterns

- Benchmark: measure tokens/sec, latency p50/p99
- Multi-GPU: tensor-parallel-size = GPU count
- Memory: gpu-memory-utilization=0.9, max-model-len for context
