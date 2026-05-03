# PaperPod - Isolated Agent Runtime

## What It Does

PaperPod provides isolated, agent-native sandboxes for code execution, browser automation, and AI inference. Run shell commands, Python/JavaScript code, expose preview URLs, generate images, and transcribe audio — all via CLI or HTTP API with per-second billing. No SDK or API keys required.

## Quick Usage Example

```bash
# Install CLI and authenticate
npm install -g @paperpod/cli
ppod login <token>

# Execute Python code
ppod exec "python -c 'print(2+2)'"

# Start server, get public URL
ppod start "python -m http.server 8080 --bind 0.0.0.0"
ppod expose 8080  # → https://8080-{id}-p8080_v1.paperpod.work

# Generate image
ppod ai:image "A cyberpunk city at sunset"

# Take screenshot
ppod browser:screenshot "https://example.com"
```

## Key Features

- **50+ Preinstalled Tools**: ffmpeg, sqlite3, pandoc, imagemagick, git, jq, ripgrep, and more
- **Browser Automation**: Screenshots, PDFs, scraping via Playwright
- **AI Capabilities**: Text generation, embeddings, image generation, audio transcription
- **Persistent Memory**: 10MB R2 storage survives sandbox resets
- **Process Management**: Start, list, and stop background processes
- **Public Preview URLs**: Expose any port as stable HTTPS URLs
- **Multiple Sessions**: Acquire reusable browser sessions, connect to existing ones
- **Per-Second Billing**: $0.0001/sec compute + browser, $0.02/1K neurons AI

## Pricing Models

- Subscription: Fixed cost for unlimited usage during period
- Tiered Usage: Daily/monthly quotas with lower cost
- Pay-Per-Use: Higher cost, no limits

## Documentation

- `ppod help` — CLI command reference
- https://paperpod.dev/docs — Full API documentation
- https://paperpod.dev — Open API schema

**Version:** 2.0.3
**Homepage:** https://paperpod.dev