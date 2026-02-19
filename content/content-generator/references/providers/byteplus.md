# BytePlusProvider

BytePlus provider for video generation using the Seedance API.

## Overview

```python
from scripts.providers.byteplus import BytePlusProvider

provider = BytePlusProvider(api_key="your_byteplus_key")
```

## Supported Models

| Model ID | Description |
|----------|-------------|
| `seedance-t2v` | Text-to-video generation (default) |
| `seedance-i2v` | Image-to-video generation |

## Cost

**$0.05 per second** of video (image-to-video costs 1.5x more)

## Constructor

```python
def __init__(
    self,
    api_key: Optional[str] = None,
    region: str = "us-east-1",
    **kwargs,
):
```

**Parameters:**
- `api_key` - BytePlus API key for authentication
- `region` - AWS region for API calls (default: `us-east-1`)
- `**kwargs` - Additional provider-specific configuration

## Methods

### generate()

Generate video based on the given prompt.

```python
async def generate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> GenerationResult
```

**Parameters:**
- `prompt` - The prompt/description for video generation
- `model` - Optional model identifier (uses default if not specified)
- `**kwargs`:
  - `image_url` - str, required for image-to-video generation
  - `duration` - int, video duration in seconds (default: 5)
  - `fps` - int, frames per second (default: 24)
  - `resolution` - str, video resolution (default: `"1280x720"`)

**Returns:** GenerationResult containing:
- `data.video_url` - Generated video URL
- `data.task_id` - Task ID for checking status
- `cost` - Estimated cost in USD
- `metadata` - Generation parameters used

**Error Conditions:**
- API key not configured
- `image_url` required for image-to-video but not provided

---

### is_available()

Check if the BytePlus provider is currently available.

```python
async def is_available(self) -> bool
```

Performs a lightweight health check by verifying API connectivity.

**Returns:** True if the provider is available, False otherwise

---

### get_cost_estimate()

Estimate the cost of a video generation operation.

```python
def get_cost_estimate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> float
```

**Parameters:**
- `prompt` - The prompt/description for video generation
- `model` - Optional model identifier
- `**kwargs`:
  - `duration` - int, video duration in seconds (default: 5)

**Returns:** Estimated cost in USD

---

## Usage Example

```python
import asyncio
from scripts.providers.byteplus import BytePlusProvider

async def main():
    provider = BytePlusProvider(api_key="your_api_key")
    
    # Text-to-video
    result = await provider.generate(
        prompt="A bird flying over mountains",
        duration=5,
        fps=24,
        resolution="1280x720"
    )
    
    # Image-to-video
    result = await provider.generate(
        prompt="Animate this image",
        model="seedance-i2v",
        image_url="https://example.com/image.jpg",
        duration=5
    )
    
    if result.success:
        print(f"Generated video: {result.data['video_url']}")
        print(f"Cost: ${result.cost}")
    else:
        print(f"Error: {result.metadata.get('error')}")

asyncio.run(main())
```

---

## API Endpoints

The provider uses these BytePlus API endpoints:
- Text-to-video: `POST /videoextraction/v1/generation/text_to_video`
- Image-to-video: `POST /videoextraction/v1/generation/image_to_video`

Base URL: `https://open.byteplusapi.com`
