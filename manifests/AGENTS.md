<!-- Parent: ../AGENTS.md -->

# manifests/

## Purpose
Marketplace submission manifests. **Not skill content.** Used by `scripts/submit_*` helpers.

## Files

| File | Marketplace |
|---|---|
| `claude-app-store.json` | Anthropic Claude App Store |
| `openai-gpt-store.json` | OpenAI GPT Store |
| `langchain-hub-submission.md` | LangChain Hub (markdown spec) |
| `langchain-hub.yaml` | LangChain Hub (YAML manifest) |
| `huggingface-space.md` | Hugging Face Spaces card |

## Maintenance
When `SKILLS.json` totals change, update skill counts in each manifest. CI does not currently validate this (manifests are external metadata).

## For AI Agents
- Read-only for normal sessions.
- Edit only when submitting a new release to a marketplace.
