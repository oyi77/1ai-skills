---
name: audit
description: Use when audit repo for over-engineering. Ranked list of what to delete, simplify, or replace with stdlib or native features.
domain: mindset
author: mahipal
license: Apache-2.0
subdomain: mindset
tags:
  - audit
  - mindset
  - ponytail
  - simplification
version: 1.0.0
---


# Audit — Repo-Wide Over-Engineering Sweep

## Quick Reference

Find every abstraction, dependency, and pattern that does not pull its weight. Output is a ranked list of what to delete, simplify, or replace with stdlib or native features.

## Overview

Audit mode scans an entire codebase for unnecessary complexity: reinvented stdlib, speculative abstractions, dead code paths, over-engineered patterns (factory/singleton/visitor with one caller), and dependencies that could be replaced by a built-in. It produces a prioritized deletion plan so you can cut 30-50% of LOC in one pass.

Scope: entire repo. Output: ranked list. Best outcome: repo loses 30% of its LOC.

## Quick Start

1. **Run audit**: `ponytail audit --path "src/" --rank-by-impact` — scans and ranks findings
2. **Review top 5 findings**: each finding shows file, line, severity, and the fix (often "delete it")
3. **Delete the #1 finding**: the biggest over-engineering you can remove safely in 15 minutes

## Key Command

```bash
ponytail audit --path "src/" --rank-by-impact --output audit-report.md
```

## Code Example: Over-Engineering Finder

```python
import ast, sys
from pathlib import Path

findings = []
for path in Path("src").rglob("*.py"):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        # Flag single-method classes
        if isinstance(node, ast.ClassDef):
            methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            if len(methods) <= 1:
                findings.append(f"[MEDIUM] {path}:{node.lineno} — class '{node.name}' has ≤1 method, use a function")
        # Flag stdlib wrappers
        if isinstance(node, ast.FunctionDef) and len(node.body) == 1:
            if isinstance(node.body[0], ast.Return) and isinstance(node.body[0].value, ast.Call):
                findings.append(f"[LOW] {path}:{node.lineno} — '{node.name}' is a one-line wrapper, inline it")

for f in sorted(findings):
    print(f)
```

## Audit Checklist

- [ ] All findings ranked by impact (highest LOC savings first)
- [ ] Reinvented stdlib identified (custom JSON, LRU, CSV parsers)
- [ ] Speculative abstractions flagged (unused interfaces, single-use factories)
- [ ] Dead code paths and orphaned exports documented
- [ ] Dependency replacements proposed (stdlib over third-party)

## When to Use

Use when audit repo for over-engineering. Ranked list of what to delete, simplify, or replace with stdlib or native features.

## Workflow

Execute these steps sequentially:

1. **Run audit**: `ponytail audit --path "src/" --rank-by-impact` — scans and ranks findings
2. **Review top 5 findings**: each finding shows file, line, severity, and the fix (often "delete it")
3. **Delete the #1 finding**: the biggest over-engineering you can remove safely in 15 minutes

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "This abstraction will pay off eventually" | 90% of speculative abstractions never pay off. Delete it now; add it back only when you have a real second consumer |
| "I know my codebase, no audit needed" | Familiarity breeds normalization. A fresh pass finds what daily exposure hides |
| "Auditing takes too long for the value" | Each audit saves 30-50% LOC per pass. That is weeks of maintenance you will never pay |
