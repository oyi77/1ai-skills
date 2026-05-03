# Agent Docs

Create documentation optimized for AI agent consumption.

## What It Does

Write documentation that AI agents can efficiently consume. Based on Vercel benchmarks and industry standards (AGENTS.md, llms.txt).

## Quick Usage Example

```markdown
# AGENTS.md: Inline critical context (2K-4K tokens)

> Context: Next.js 16 | Tailwind | Supabase

## 🚨 CRITICAL
- NO SECRETS in output
- Use `app/` directory ONLY

## 📚 DOCS INDEX
- Auth: `docs/auth/llms.txt`
- DB: `docs/db/schema.md`

# llms.txt: Machine-readable index

## Authentication
- [Setup](docs/auth/setup.md): Environment vars and init
- [Server](docs/auth/server.md): Cookie handling

## Database
- [Schema](docs/db/schema.md): Full Prisma schema
```

## Key Features

- 📊 Three-layer architecture (always-in-context, fetch-on-demand, gated)
- 🎯 Token efficiency (100% vs 53% pass rate vs tool-based retrieval)
- 📝 RAG-optimized chunking at headers
- 🧠 U-shaped attention awareness (critical info at top)
- 🔒 Security-conscious design
- ⚡ File path and function signature indexing

## Category

**Documentation / Framework / AI Optimization**

## Keywords

agent documentation, RAG optimization, token efficiency