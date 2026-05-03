# GroqProvider

Groq provider for fast LLM inference using high-speed GPU infrastructure.

## Overview

```python
from scripts.providers.groq import GroqProvider

provider = GroqProvider(api_key="gsk_...")
```

## Supported Models

| Model ID | Input Cost | Output Cost |
|----------|------------|-------------|
| `llama-3.3-70b-versatile` | Free | Free |
| `llama-3.1-70b-versatile` | Free | Free |
| `llama-3.1-8b-instant` | Free | Free |
| `llama-3-70b-instruct` | $0.59/M | $0.79/M |
| `llama-3-8b-instruct` | $0.05/M | $0.08/M |
| `mixtral-8x7b-32768` | $0.24/M | $0.24/M |
| `gemma-7b-it` | $0.07/M | $0.07/M |

**Default Model:** `llama-3.3-70b-versatile`

## Constructor

```python
def __init__(
    self,
    api_key: Optional[str] = None,
    base_url: str = "https://api.groq.com/openai/v1",
    **kwargs,
):
```

**Parameters:**
- `api_key` - Groq API key for authentication
- `base_url` - Base URL for the Groq API (defaults to OpenAI-compatible endpoint)
- `**kwargs` - Additional provider-specific configuration

## Methods

### generate()

Generate text content using Groq's chat completions API.

```python
async def generate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> GenerationResult
```

**Parameters:**
- `prompt` - The prompt for text generation
- `model` - Optional model identifier (defaults to `llama-3.3-70b-versatile`)
- `**kwargs`:
  - `temperature` - Sampling temperature (default: 0.7)
  - `max_tokens` - Maximum tokens to generate (default: 1024)
  - `top_p` - Nucleus sampling parameter (default: 1.0)
  - `stop` - Stop sequences (optional)

**Returns:** GenerationResult containing:
- `data` - Generated text content
- `cost` - Actual cost based on API usage
- `metadata.finish_reason` - Why generation stopped
- `metadata.usage` - Token usage from API

---

### is_available()

Check if the Groq API is available.

```python
async def is_available(self) -> bool
```

Performs a lightweight check by attempting to list available models.

**Returns:** True if the provider is available, False otherwise

---

### get_cost_estimate()

Estimate the cost of a generation operation.

```python
def get_cost_estimate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> float
```

Provides a cost estimate based on prompt length and model pricing.

**Parameters:**
- `prompt` - The input prompt
- `model` - Optional model identifier
- `**kwargs`:
  - `max_tokens` - Affects output cost estimate (default: 1024)

**Returns:** Estimated cost in USD

**Note:** Uses rough approximation: 1 token ≈ 4 characters

---

## Internal Methods

### _make_request()

Make an HTTP request to the Groq API.

```python
def _make_request(
    self, endpoint: str, payload: Optional[dict] = None, method: str = "POST"
) -> dict[str, Any]
```

**Parameters:**
- `endpoint` - API endpoint path
- `payload` - Request body (for POST requests)
- `method` - HTTP method (GET or POST)

**Returns:** Parsed JSON response

**Raises:** `urllib.error.HTTPError` - On HTTP errors

---

### _calculate_cost_from_usage()

Calculate actual cost from API usage data.

```python
def _calculate_cost_from_usage(self, usage: dict[str, int], model: str) -> float
```

**Parameters:**
- `usage` - Usage dictionary from API response
- `model` - Model identifier

**Returns:** Actual cost in USD

---

## Usage Example

```python
import asyncio
from scripts.providers.groq import GroqProvider

async def main():
    provider = GroqProvider(api_key="gsk_your_key")
    
    result = await provider.generate(
        prompt="Write a short poem about artificial intelligence",
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=256
    )
    
    if result.success:
        print(f"Generated text:\n{result.data}")
        print(f"Cost: ${result.cost}")
        print(f"Usage: {result.metadata.get('usage')}")
    else:
        print(f"Error: {result.metadata.get('error')}")

asyncio.run(main())
```

---

## API Compatibility

The GroqProvider uses an OpenAI-compatible API format:
- Base URL: `https://api.groq.com/openai/v1`
- Endpoint: `/chat/completions`

This makes it compatible with libraries designed for OpenAI's API.
