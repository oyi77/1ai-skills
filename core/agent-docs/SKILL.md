---
name: agent-docs
description: Use when writing documentation optimized for AI agent consumption - SKILL.md files, README files, API docs, or any documentation that will be read by LLMs in context windows.
---
persona:
  name: "Don Knuth"
  title: "The Documentation Master - Literate Programming Pioneer"
  expertise: ['Technical Writing', 'Documentation Systems', 'Literate Programming', 'Knowledge Management']
  philosophy: "Code should be written for humans to read, and only incidentally for machines to execute."
  credentials: ["Author of 'The Art of Computer Programming'", 'Created TeX typesetting system', 'Turing Award winner']
  principles: ['Document as you code', 'Write for your future self', 'Examples over abstractions', 'Maintainability first']



# Agent Docs

## Overview

Write documentation that AI agents can efficiently consume. Based on Vercel benchmarks and industry standards (AGENTS.md, llms.txt, CLAUDE.md).

## When to Use

- Writing SKILL.md files that will be loaded by agents
- Creating README files for agent consumption
- Building API documentation
- Any documentation that will be read by LLMs in context windows

## When NOT to Use

- Writing human-only documentation without agent context
- Creating content that won't be read by AI agents

## The Hybrid Context Hierarchy

Three-layer architecture for optimal agent performance:

### Layer 1: Constitution (Inline)
**Always in context.** 2,000–4,000 tokens max.

```markdown
# AGENTS.md
> Context: Next.js 16 | Tailwind | Supabase

## 🚨 CRITICAL
- NO SECRETS in output
- Use `app/` directory ONLY

## 📚 DOCS INDEX (use read_file)
- Auth: `docs/auth/llms.txt`
- DB: `docs/db/schema.md`
```

**Include:**

## Quick Reference

- Use markdown formatting for RAG retrieval
- Keep token count low for context efficiency
- Structure content in layers: Constitution → Reference → Detail
- Include code examples inline

## Common Mistakes

- Putting too much detail in context (exceeds token limits)
- Not structuring content for RAG retrieval
- Missing critical information in first 2000 tokens
- Using prose instead of scannable lists
- Security rules, architecture constraints
- Build/test/lint commands (top for primacy bias)
- Documentation map (where to find more)

### Layer 2: Reference Library (Local Retrieval)
**Fetched on demand.** 1K–5K token chunks.

- Framework-specific guides
- Detailed style guides
- API schemas

### Layer 3: Research Assistant (External)
**Gated by allow-lists.** Edge cases only.

- Latest library updates
- Stack Overflow for obscure errors
- Third-party llms.txt

## Why This Works

**Vercel Benchmark (2026):**
| Approach | Pass Rate |
|----------|-----------|
| Tool-based retrieval | 53% |
| Retrieval + prompting | 79% |
| **Inline AGENTS.md** | **100%** |

**Root cause:** Meta-cognitive failure. Agents don't know what they don't know—they assume training data is sufficient. Inline docs bypass this entirely.

## Core Principles

### 1. Compressed Index > Full Docs

An 8KB compressed index outperforms a 40KB full dump.

**Compress to:**
- File paths (where code lives)
- Function signatures (names + types only)
- Negative constraints ("Do NOT use X")

### 2. Structure for Chunking

RAG systems split at headers. Each section must be self-contained:

```markdown
## Database Setup          ← Chunk boundary

Prerequisites: PostgreSQL 14+

1. Create database...
```

**Rules:**
- Front-load key info (chunkers truncate)
- Descriptive headers (agents search by header text)

### 3. Inline Over Links

Agents can't autonomously browse. Each link = tool call + latency + potential failure.

| Approach | Token Load | Agent Success |
|----------|------------|---------------|
| Full inline | ~12K | ✅ High |
| Links only | ~2K | ❌ Requires fetching |
| Hybrid | ~4K base | ✅ Best of both |

### 4. The "Lost in the Middle" Problem

LLMs have U-shaped attention:
- **Strong:** Start of context (primacy)
- **Strong:** End of context (recency)
- **Weak:** Middle of context

**Solution:** Put critical rules at TOP of AGENTS.md. Governance first, details later.

### 5. Signal-to-Noise Ratio

Strip everything that isn't essential:
- No "Welcome to..." preambles
- No marketing text
- No changelogs in core docs

Formats like llms.txt and AGENTS.md mechanically increase SNR.

## llms.txt Standard

Machine-readable doc index for agents:

```markdown
# Project Name

> One-line project description.

## Authentication

- [Setup](docs/auth/setup.md): Environment vars and init
- [Server](docs/auth/server.md): Cookie handling

## Database

- [Schema](docs/db/schema.md): Full Prisma schema
```

**Location:** `/llms.txt` at domain root
**Companion:** `/llms-full.txt` — full concatenated docs, HTML stripped

## Security Considerations

### Inline = Trusted
AGENTS.md is part of your codebase. Controlled, version-pinned.

### External = Attack Surface
- Indirect prompt injection via hidden text
- SSRF risks if agents can browse freely
- Dependency on external uptime

**Mitigation:** Domain allow-lists, human-in-the-loop for external retrieval.

## Anti-Patterns

1. **Pasting 50 pages** — triggers "Lost in the Middle"
2. **"See external docs"** — agents can't browse autonomously
3. **Generic advice** — "Write clean code" (use specific constraints)
4. **TOC-only docs** — indexes without content
5. **Trusting retrieval alone** — 53% vs 100% pass rate

## Advanced Patterns

For detailed guidance on RAG optimization, multi-framework docs, and API templates, see [references/advanced-patterns.md](references/advanced-patterns.md).

## Validation Checklist

- [ ] Critical governance at TOP of doc
- [ ] Total inline context under 4K tokens
- [ ] Each H2 section self-contained
- [ ] No external links without inline summary
- [ ] Negative constraints explicit ("Do NOT...")
- [ ] File paths and signatures, not full code
