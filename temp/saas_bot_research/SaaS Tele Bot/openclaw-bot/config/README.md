# Configuration

This directory contains all configuration files for the OpenClaw Bot.

## 📁 Files

| File | Description |
|------|-------------|
| `database.yml` | Database connection settings |
| `payment.yml` | Payment gateway configuration |
| `ai.yml` | AI provider settings |
| `features.yml` | Feature flags |

## 🔧 Usage

Configuration files are loaded at runtime and can be overridden by environment variables.

### Priority Order

1. Environment variables (highest priority)
2. Configuration files
3. Default values (lowest priority)

### Example

```yaml
# config/ai.yml
providers:
  geminigen:
    enabled: true
    timeout: 60000
```

```bash
# Override with environment variable
GEMINIGEN_TIMEOUT=120000
```

## 📝 Feature Flags

Feature flags are defined in `features.yml`. They can be enabled/disabled:

- Globally
- Per user tier
- Per region
- By percentage rollout

---

*See [../.env.example](../.env.example) for environment variable reference*
