---
name: gemini-api-dev
description: Build applications using Google Gemini API. Handle chat completions, multimodal inputs, function calling, streaming, and grounding with Google Search. Use when building applications using google gemini api. handle chat completions, multimodal.
domain: core
tags:
- ai
- gemini
- google
- llm
- multimodal
- api
---

# Gemini Api Dev

## When to Use

**Trigger phrases:**
- "gemini api dev"
- "When building apps powered by Google Gemini models"
- "When processing multimodal inputs (text + images + audio + video)"
- "When implementing function calling or tool use with Gemini"


- When building apps powered by Google Gemini models
- When processing multimodal inputs (text + images + audio + video)
- When implementing function calling or tool use with Gemini
- When using Gemini for grounding with Google Search

## When NOT to Use

- For OpenAI-compatible APIs (use OpenAI skills)
- For local model inference (use Ollama skills)
- For fine-tuning (use Vertex AI training skills)

## Overview

Integrate Google Gemini API for chat, multimodal analysis, function calling, and streaming. Supports Gemini 2.5 Pro, Flash, and Nano models via the Google AI SDK.

## Workflow

1. **Set up SDK** — Install `@google/genai` or `google-genai` package
2. **Configure auth** — API key or service account
3. **Build prompts** — System instructions, few-shot examples
4. **Handle responses** — Streaming, function calls, safety settings
5. **Error handling** — Rate limits, retries, fallback models

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will just use curl" | SDK handles retries, streaming, auth, and type safety |
| "Gemini is just for text" | Gemini 2.5 processes images, audio, video, and PDFs natively |
| "One prompt fits all" | System instructions and grounding dramatically improve accuracy |

## Code Example (TypeScript)

```typescript
import { GoogleGenAI } from '@google/genai';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

const response = await ai.models.generateContentStream({
  model: 'gemini-2.5-pro',
  contents: [{ role: 'user', parts: [{ text: 'Analyze this chart' }] }],
  config: {
    systemInstruction: 'You are a data analyst. Be precise and cite numbers.',
    temperature: 0.3,
  }
});

for await (const chunk of response) {
  process.stdout.write(chunk.text);
}
```


## Process

1. **Design** — Define interface, identify patterns, plan implementation
1. **Implement** — Write code following existing conventions, add tests
1. **Verify** — Run tests, check integration, validate behavior

## Verification

- [ ] API key authenticated successfully
- [ ] Chat completions return valid responses
- [ ] Streaming works without buffering issues
- [ ] Function calling triggers correctly
- [ ] Safety settings block harmful content

