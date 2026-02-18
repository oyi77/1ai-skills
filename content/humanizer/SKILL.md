---
name: humanizer
description: Transform AI-generated content into natural, human-sounding writing with proper tone and style
allowed-tools:
  - MCP(notion:*)
  - MCP(exa:*)
---

# Humanizer

Transform AI-generated content into natural, human-sounding writing.

## Required Tools

```json
{
  "mcpServers": {
    "notion": { "command": "npx", "args": ["-y", "@makenotion/mcp-server"], "env": { "NOTION_API_KEY": "${NOTION_API_KEY}" } },
    "exa": { "command": "npx", "args": ["-y", "@exa/mcp-server"], "env": { "EXA_API_KEY": "${EXA_API_KEY}" } }
  }
}
```

## Pseudo Code

### Rewrite Content

```typescript
// 1. Analyze source content
const content = await loadDraft();

// 2. Identify voice/tone from samples
const samples = await exa.search(author, { numResults: 5 });
const voice = extractVoice(samples);

// 3. Rewrite
const humanized = await rewrite(content, {
  tone: voice,
  preserveMeaning: true
});
```

---
*Skill v2.0 - Humanizer*
