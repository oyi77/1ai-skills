---
name: codebase-memory-mcp
description: Index codebases into a persistent knowledge graph for structural code queries, call-chain tracing, and semantic
  search. Use when navigating unfamiliar repos, understanding architecture, or exploring large codebases.
domain: mcp
tags:
- codebase
- mcp
- mcp-server
- memory
- model-context-protocol
- tool-integration
---

# Codebase Memory MCP

High-performance code intelligence MCP server by DeusData. Indexes codebases into a persistent knowledge graph — functions, classes, call chains, HTTP routes, cross-service links. Queries in sub-ms, 120× fewer tokens than reading files.

## When to Use

- Navigating an unfamiliar codebase (first time exploring)
- Understanding architecture: "What are the main modules and how do they connect?"
- Tracing call chains: "What calls `handlePayment()` and what does it call?"
- Finding code by semantics: "Find all auth-related functions" (natural language)
- Cross-file impact analysis: "What breaks if I change this function?"
- **When NOT to use**: Single-file tasks (just read it), trivial codebases (<10 files), or when you already have full context

## Install

**Single static binary — zero dependencies.**

```bash
# macOS (Apple Silicon)
curl -L -o cbm https://github.com/DeusData/codebase-memory-mcp/releases/latest/download/cbm-darwin-arm64
chmod +x cbm
sudo mv cbm /usr/local/bin/cbm

# macOS (Intel)
curl -L -o cbm https://github.com/DeusData/codebase-memory-mcp/releases/latest/download/cbm-darwin-amd64
chmod +x cbm
sudo mv cbm /usr/local/bin/cbm

# Linux (x64)
curl -L -o cbm https://github.com/DeusData/codebase-memory-mcp/releases/latest/download/cbm-linux-amd64
chmod +x cbm
sudo mv cbm /usr/local/bin/cbm

# Linux (ARM64)
curl -L -o cbm https://github.com/DeusData/codebase-memory-mcp/releases/latest/download/cbm-linux-arm64
chmod +x cbm
sudo mv cbm /usr/local/bin/cbm
```

**Verify**: `cbm --version` (should print version)

## MCP Client Configuration

Add to your MCP client config (e.g., `~/.config/claude/settings.json`, `~/.cursor/mcp.json`, or `~/.config/opencode/config.json`):

```json
{
  "mcpServers": {
    "codebase-memory": {
      "command": "cbm",
      "args": ["serve", "--stdio", "--graph", "/tmp/codebase-graph.db"]
    }
  }
}
```

**Or with project-specific graph:**

```json
{
  "mcpServers": {
    "codebase-memory": {
      "command": "cbm",
      "args": ["serve", "--stdio", "--graph", "./.codebase-graph.db"]
    }
  }
}
```

## First-Time Indexing

```bash
# Index current project
cbm index .

# Index with verbose output
cbm index . --verbose

# Index specific directory
cbm index /path/to/project
```

**Performance**: Average repo in milliseconds. Linux kernel (28M LOC, 75K files) in 3 minutes.

## Available MCP Tools (14)

| Tool | Description |
|------|-------------|
| `search_graph` | Natural-language semantic search across code (uses built-in embeddings) |
| `query_graph` | Cypher query against the knowledge graph |
| `trace_path` | Trace call chains: who calls X, what does X call |
| `detect_changes` | Find what changed since last index (diff-aware) |
| `get_architecture` | High-level architecture summary with module boundaries |
| `get_code_snippet` | Get exact source code by node ID or path:line |
| `manage_adr` | Create/read/update Architecture Decision Records |
| `get_file_dependencies` | List all imports/exports for a file |
| `get_symbol_references` | Find all references to a function/class/variable |
| `get_callers` | Find all callers of a function |
| `get_callees` | Find all functions called by a function |
| `get_module_boundary` | Get the public API surface of a module |
| `get_type_hierarchy` | Get class inheritance tree |
| `list_symbols` | List all symbols in a file or directory |

## Common Workflows

### Explore unfamiliar codebase

```
1. Index: cbm index .
2. Architecture: Use get_architecture → understand module boundaries
3. Entry points: Use search_graph "main entry point" or list_symbols on main file
4. Deep dive: Use trace_path or get_callers/get_callees
```

### Impact analysis before changing a function

```
1. get_callers("handlePayment") → find who depends on it
2. get_callees("handlePayment") → find what it depends on
3. trace_path("handlePayment", "processOrder") → find the call chain
4. Make change, then detect_changes → verify impact
```

### Find code by intent (semantic search)

```
search_graph("authentication middleware") → finds auth-related code even if not named "auth"
search_graph("database connection pooling") → finds pool management code
search_graph("retry logic with backoff") → finds retry implementations
```

### Cross-service dependency mapping

```
1. Index both services
2. get_file_dependencies("src/api/users.ts") → see what external modules it imports
3. search_graph("external API calls") → find all HTTP/gRPC calls
4. trace_path → map the full request flow
```

## Supported Languages (158)

Python, TypeScript, JavaScript, Java, Go, Rust, C, C++, C#, PHP, Ruby, Swift, Kotlin, Scala, Haskell, Lua, R, Julia, Zig, Nim, Dart, Elixir, Erlang, OCaml, F#, Clojure, Bash, SQL, YAML, TOML, JSON, Markdown, and 130+ more via vendored tree-sitter grammars.

**Hybrid LSP type resolution** for: Python, TypeScript/JavaScript/JSX/TSX, PHP, C#, Go, C/C++, Java, Kotlin, Rust.

## Graph Schema

**Node types**: FUNCTION, CLASS, METHOD, VARIABLE, MODULE, FILE, INTERFACE, ENUM, STRUCT, NAMESPACE, PACKAGE, HTTP_ROUTE, EXTERNAL_SERVICE

**Edge types**: CALLS, IMPORTS, EXPORTS, EXTENDS, IMPLEMENTS, CONTAINS, DEPENDS_ON, SEMANTICALLY_RELATED (vocabulary mismatch), SIMILAR_TO (near-clone detection)

## Example Cypher Queries

```cypher
-- Find all functions with >10 callers (hot paths)
MATCH (f:FUNCTION)<-[:CALLS]-() 
WITH f, count(*) as callers 
WHERE callers > 10 
RETURN f.name, f.file, callers ORDER BY callers DESC

-- Find dead code (no callers)
MATCH (f:FUNCTION) 
WHERE NOT (f)<-[:CALLS]-() 
RETURN f.name, f.file

-- Find circular dependencies
MATCH (a:MODULE)-[:DEPENDS_ON]->(b:MODULE)-[:DEPENDS_ON]->(a)
RETURN a.name, b.name
```

## Performance

| Operation | Time |
|-----------|------|
| Index average repo | Milliseconds |
| Index Linux kernel (28M LOC) | ~3 min |
| Sub-ms queries | <1ms |
| Token savings | 120× fewer (3,400 vs 412,000 tokens) |

## When NOT to Use

- Single-file tasks (just read the file)
- Codebase <10 files (overkill)
- You already have full context and know where everything is
- Task is purely writing new code with no exploration needed

## Red Flags

- You're indexing a monorepo with multiple languages — use `--include` flag to scope
- Graph is stale (re-index after major changes: `cbm index .`)
- Binary/asset files polluting the graph (use `.cbmignore` to exclude)
- You're querying without indexing first (graph will be empty)

## Verification

- [ ] `cbm --version` works
- [ ] MCP server configured in client settings
- [ ] `cbm index .` completed successfully
- [ ] `get_architecture` returns module boundaries
- [ ] `search_graph` finds code by natural language query
- [ ] `trace_path` traces a call chain correctly

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
