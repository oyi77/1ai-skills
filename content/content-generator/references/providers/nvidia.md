# NVIDIAProvider

NVIDIA NIM provider for image generation using Flux and Stable Diffusion models.

## Overview

```python
from scripts.providers.nvidia import NVIDIAProvider

provider = NVIDIAProvider(api_key="nvapi-...")
```

## Supported Models

| Model ID | Description |
|----------|-------------|
| `nvidia/flux-1.1-pro` | Flux 1.1 Pro (default) |
| `nvidia/flux-1.1-dev` | Flux 1.1 Developer |
| `nvidia/flux-1-schnell` | Flux 1.1 Schnell (fast) |
| `nvidia/stable-diffusion-xl-1024-v1-0` | SDXL 1024 v1.0 |
| `nvidia/stable-diffusion-3-medium` | Stable Diffusion 3 Medium |

## Cost Estimates

| Model | Cost per Image |
|-------|----------------|
| `nvidia/flux-1.1-pro` | $0.003 |
| `nvidia/flux-1.1-dev` | $0.004 |
| `nvidia/flux-1-schnell` | $0.001 |
| `nvidia/stable-diffusion-xl-1024-v1-0` | $0.002 |
| `nvidia/stable-diffusion-3-medium` | $0.0025 |

## Constructor

```python
def __init__(
    self,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs,
):
```

**Parameters:**
- `api_key` - NVIDIA API key (can also be set via `NVIDIA_API_KEY` env var)
- `base_url` - Custom API base URL (defaults to `https://integrate.api.nvidia.com`)
- `**kwargs` - Additional configuration options

## Methods

### generate()

Generate an image based on the given prompt.

```python
async def generate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> GenerationResult
```

**Parameters:**
- `prompt` - The text description for image generation
- `model` - Optional model identifier (defaults to `flux-1.1-pro`)
- `**kwargs`:
  - `width` - Image width (default 1024)
  - `height` - Image height (default 1024)
  - `num_images` - Number of images to generate (default 1)
  - `seed` - Random seed for reproducibility
  - `steps` - Number of inference steps

**Returns:** GenerationResult containing:
- `data.url` - Generated image URL
- `data.base64` - Base64 encoded image data
- `data.images` - List of generated images
- `cost` - Estimated cost in USD
- `metadata` - Generation parameters used

---

### is_available()

Check if the NVIDIA NIM provider is available.

```python
async def is_available(self) -> bool
```

Performs a lightweight health check by verifying API key and attempting connectivity test.

**Returns:** True if the provider is available, False otherwise

---

### get_cost_estimate()

Estimate the cost of an image generation operation.

```python
def get_cost_estimate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> float
```

**Parameters:**
- `prompt` - The text description for image generation
- `model` - Optional model identifier
- `**kwargs`:
  - `num_images` - Number of images to generate (default 1)

**Returns:** Estimated cost in USD

---

## Usage Example

```python
import asyncio
from scripts.providers.nvidia import NVIDIAProvider

async def main():
    provider = NVIDIAProvider()
    
    result = await provider.generate(
        prompt="A futuristic cityscape at sunset",
        model="nvidia/flux-1.1-pro",
        width=1024,
        height=1024,
        num_images=1
    )
    
    if result.success:
        print(f"Generated image: {result.data['url']}")
        print(f"Cost: ${result.cost}")
    else:
        print(f"Error: {result.metadata.get('error')}")

asyncio.run(main())
```
