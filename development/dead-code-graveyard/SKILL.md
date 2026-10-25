---
name: dead-code-graveyard
description: Auditing, isolating, and safely pruning dead code, unreachable branches, unmounted endpoints, and orphaned assets across large codebases. Use when codebase bloat accumulates, preparing for major refactors, removing deprecated feature flags, or running dead code sweeps.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - dead-code
  - refactoring
  - code-hygiene
  - static-analysis
  - cleanup
  - code-bloat
---

## Overview

Dead code erodes maintainability, wastes compilation cycles, inflates test runtimes, and misleads engineers into preserving obsolete invariants. The Dead Code Graveyard playbook provides a systematic, zero-regression methodology for identifying unreferenced symbols, unreachable branches, abandoned routes, and stale assets—then safely extracting them with verifiable evidence.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "I will just comment it out instead of deleting it." | Commented-out code rots, pollutes searches, and confuses static analysis. Git history preserves all deleted code permanently. | Delete code completely. Never leave `// TODO: remove later` or block-commented dead blocks. |
| "A dynamic string might call this function." | Speculative fear blocks refactoring. Check reflection, `getattr`, `eval`, and event maps explicitly. | Trace call-sites and dynamic dispatch registries. If truly unreferenced, delete. If public API, apply deprecation telemetry. |
| "Let's delete all 50 dead files in one giant commit." | Monolithic cleanups make git bisect useless and hide accidental regressions inside hundreds of diff lines. | Batch deletions by domain or module. Verify the entire test suite and build pipeline after every batch. |
| "Tests pass, so the deletion is 100% safe." | Tests might pass because the deleted module was never asserted or tested in the first place. | Run full-repo symbol grep, verify unmounted routes, and confirm bundle size reduction before claiming completion. |
| "It is only a 30-line helper, leaving it does not hurt." | 30 lines across 40 modules adds 1,200 lines of dead baggage, increasing cognitive load and slowing refactorings. | Enforce zero-tolerance for orphaned internal helpers. YAGNI applies retroactively. |
| "We can delete this public HTTP route immediately." | External consumers or client apps with older cached versions may still call public routes, causing 404 outages. | Follow two-phase retirement: return `410 Gone` with telemetry in phase 1; unmount entirely in phase 2. |

## When to Use

- Repository cleanup passes where obsolete features, deprecated modules, or unused dependencies have accumulated.
- Monolith-to-modular refactoring where unused utility functions and dead abstractions need pruning.
- Post-migration audits after replacing legacy ORM models, API routes, or UI components with newer implementations.
- Feature flag retirement after a feature has reached 100% rollout or permanent deprecation.

## When NOT to Use

- Public library APIs with published SemVer contracts where unreferenced exports belong to the public interface.
- Dynamic plugin architectures where modules are discovered and loaded at runtime via config files or service locators.
- Active exploratory prototyping where experimental implementations are deliberately under current evaluation.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│             Dead Code Graveyard Workflow               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Static Discovery & Candidate Extraction             │
│    - Run AST analyzers (knip, ts-prune, vulture, ast) │
│    - Inventory unused exports, functions, routes       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Dynamic Dispatch & Reflection Cross-Check          │
│    - Audit getattr, string-based event names, DI tags  │
│    - Check router manifests and schema bindings        │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Atomic Pruning & Orphan Sweep                       │
│    - Remove candidate symbols, unused imports, files   │
│    - Delete orphaned unit test fixtures and mock data  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Verification & Regression Gate                      │
│    - Full typecheck (tsc, mypy) + test suite execution │
│    - Verify bundle size delta and zero runtime breaks  │
└────────────────────────────────────────────────────────┘
```

### Step 1: Static Discovery & Candidate Extraction
Run language-appropriate static analysis to detect zero-reference exports and unused functions:
- **TypeScript/JavaScript**: Use `knip` or `ts-prune` to find unused files, exports, and types.
- **Python**: Use `vulture` with confidence thresholds or custom AST visitor scripts.
- **Go**: Use `deadcode ./...` to detect unreachable functions across the call graph.

### Step 2: Dynamic Dispatch & Reflection Cross-Check
Before deleting suspected dead code, verify whether symbols are called indirectly:
- Check string-literal references: `git grep "symbol_name"`.
- Check database column names, serializers, RPC method registries, or event bus topic names.
- Check framework-specific annotations (e.g. FastAPI dependencies, NestJS providers).

### Step 3: Atomic Pruning & Orphan Sweep
Delete dead artifacts in disciplined atomic batches:
- Remove the implementation file or internal function.
- Remove all import statements across sibling files referencing the deleted symbol.
- Remove associated test files or test fixtures that only tested the dead feature.
- Remove stale configuration keys and environment variables associated with the pruned feature.

### Step 4: Verification & Regression Gate
Run the full verification ladder to prove zero collateral damage:
- Run compiler/typecheck: `tsc --noEmit` or `mypy .`.
- Run comprehensive test suite: all existing tests must pass.
- Verify production build finishes cleanly without missing module errors.

## Code Examples

### TypeScript / JavaScript Dead Export Audit (`knip.json`)

```json
{
  "$schema": "https://unpkg.com/knip@5/resources/knip-schema.json",
  "entry": ["src/index.ts!", "src/cli.ts!"],
  "project": ["src/**/*.ts!"],
  "ignore": ["**/*.test.ts", "**/__mocks__/**"],
  "rules": {
    "files": "error",
    "dependencies": "error",
    "unlisted": "error",
    "unresolved": "error",
    "exports": "error",
    "types": "warn",
    "duplicates": "error"
  }
}
```

```bash
# Run Knip in production mode (ignores devDependencies)
npx knip --production

# Filter strictly for unused exports and dead files
npx knip --reporter compact
```

### Python AST-Based Dead Function & Import Scanner (`scripts/deadcode-scanner.py`)

```python
import ast
import os
import sys
from pathlib import Path

def find_defined_and_used_names(root_dir: str):
    defined_functions = set()
    used_names = set()

    for path in Path(root_dir).rglob("*.py"):
        if "venv" in path.parts or ".git" in path.parts or "test" in path.name:
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                defined_functions.add((node.name, str(path), node.lineno))
            elif isinstance(node, ast.Name):
                used_names.add(node.id)
            elif isinstance(node, ast.Attribute):
                used_names.add(node.attr)

    dead_candidates = [
        (name, filepath, line)
        for (name, filepath, line) in defined_functions
        if name not in used_names
    ]

    print(f"Total defined public functions: {len(defined_functions)}")
    print(f"Potential dead functions found: {len(dead_candidates)}")
    for name, filepath, line in sorted(dead_candidates):
        print(f"  [DEAD?] {name} -> {filepath}:{line}")

if __name__ == "__main__":
    scan_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    find_defined_and_used_names(scan_dir)
```

### Safe Deprecation Tombstone Pattern (Two-Phase API Sunset)

```typescript
import { Request, Response, NextFunction } from 'express';

export function deprecatedRouteTombstone(sunsetDate: string, replacementUrl?: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    // Log metric for legacy callers still hitting endpoint
    console.warn(`[DEPRECATION-HIT] ${req.method} ${req.originalUrl} called by ${req.ip}`);

    res.setHeader('Sunset', sunsetDate);
    res.setHeader('Deprecation', 'true');
    if (replacementUrl) {
      res.setHeader('Link', `<${replacementUrl}>; rel="successor-version"`);
    }

    // In Phase 2, change status from continuing execution to 410 Gone
    if (new Date() >= new Date(sunsetDate)) {
      return res.status(410).json({
        error: 'Gone',
        message: 'This endpoint has been permanently retired.',
        successor: replacementUrl ?? null,
      });
    }

    next();
  };
}
```

## Verification Checklist

- [ ] AST analyzer / dead code scanner run across all first-party source directories.
- [ ] Suspected dead symbols cross-referenced against dynamic call-sites (`getattr`, reflection, event buses).
- [ ] Unreferenced functions, dead modules, and unused private variables pruned.
- [ ] Associated stale unit tests, fixtures, and mocks removed alongside implementation.
- [ ] Compiler and typechecker pass with zero missing symbol errors (`tsc --noEmit`, `mypy`).
- [ ] Full automated test suite passes 100%.
- [ ] Application bundle and container image build successfully with verified size reduction.
