# AIProvider Base Classes

Defines the abstract base class and data structures that all AI providers must implement.

## ProviderType Enum

Types of content that a provider can generate.

```python
class ProviderType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    LLM = "llm"
```

**Attributes:**
- `IMAGE` - Static image generation
- `VIDEO` - Video generation
- `LLM` - Large language model (text generation)

---

## GenerationResult Dataclass

Result of a content generation operation.

```python
@dataclass
class GenerationResult:
    success: bool
    data: Any = None
    cost: float = 0.0
    provider: str = ""
    model: str = ""
    metadata: dict = field(default_factory=dict)
```

**Attributes:**
- `success` - Whether the generation succeeded
- `data` - The generated content (URL, file path, text, etc.)
- `cost` - Estimated cost in USD
- `provider` - Name of the provider that generated the content
- `model` - Model identifier used for generation
- `metadata` - Additional provider-specific metadata

**Raises:**
- `ValueError` - If cost is negative

---

## AIProvider Abstract Base Class

Abstract base class for AI content generation providers. All providers must inherit from this class and implement the abstract methods.

```python
class AIProvider(ABC):
    def __init__(
        self,
        provider_type: ProviderType,
        provider_name: str,
        api_key: Optional[str] = None,
        **kwargs,
    ):
```

**Constructor Parameters:**
- `provider_type` - The type of content this provider generates
- `provider_name` - Human-readable name of the provider
- `api_key` - Optional API key for authentication
- `**kwargs` - Additional provider-specific configuration

### Abstract Methods

#### supported_models (property)

```python
@property
def supported_models(self) -> list[str]:
```

Get list of supported model identifiers.

**Returns:** List of model IDs that this provider can use

---

#### generate()

```python
async def generate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> GenerationResult:
```

Generate content based on the given prompt.

**Parameters:**
- `prompt` - The prompt/description for content generation
- `model` - Optional model identifier (uses default if not specified)
- `**kwargs` - Additional provider-specific generation parameters

**Returns:** GenerationResult containing the generated content and metadata

---

#### is_available()

```python
async def is_available(self) -> bool:
```

Check if the provider is currently available and operational. This method should perform a lightweight health check.

**Returns:** True if the provider is available, False otherwise

---

#### get_cost_estimate()

```python
def get_cost_estimate(
    self, prompt: str, model: Optional[str] = None, **kwargs
) -> float:
```

Estimate the cost of a generation operation.

**Parameters:**
- `prompt` - The prompt/description for content generation
- `model` - Optional model identifier
- `**kwargs` - Additional generation parameters

**Returns:** Estimated cost in USD

### Base Implementation Methods

#### validate_api_key()

```python
def validate_api_key(self) -> bool:
```

Validate that the API key is present and properly configured.

**Returns:** True if API key is valid, False otherwise

---

#### get_default_model()

```python
def get_default_model(self) -> str:
```

Get the default model identifier for this provider.

**Returns:** The default model ID

**Raises:** `ValueError` if no supported models defined
