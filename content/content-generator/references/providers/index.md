# Providers Module

This module contains AI provider implementations for generating content. All providers follow a common interface defined in the base module.

## Available Providers

| Provider | Type | Description |
|----------|------|-------------|
| [NVIDIAProvider](./nvidia.md) | Image | NVIDIA NIM for image generation using Flux and Stable Diffusion |
| [BytePlusProvider](./byteplus.md) | Video | BytePlus Seedance for native video generation |
| [GroqProvider](./groq.md) | LLM | Groq for fast LLM inference |
| OllamaProvider | Both | Local LLM using Ollama |
| XAIProvider | Video | XAI for video editing |
| ReplicateProvider | Image | Replicate for image generation |
| HuggingFaceProvider | Image | HuggingFace for image generation |

## Common Interface

All providers inherit from `AIProvider` and implement these key methods:

- `generate()` - Generate content from a prompt
- `is_available()` - Check provider availability
- `get_cost_estimate()` - Estimate generation cost
- `supported_models` - Property listing supported models

See [base.md](./base.md) for the full interface definition.
