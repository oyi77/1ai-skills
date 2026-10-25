---
name: ast-architectural-guard
description: Enforcing architectural layer boundaries, import hierarchies, and circular dependency prevention using AST analysis and dependency graph linting. Use when modularizing monoliths, enforcing hexagonal or clean architecture rules, preventing cross-domain leaking, or checking boundary violations.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - architecture
  - ast
  - static-analysis
  - clean-architecture
  - circular-dependencies
  - dependency-graph
---

## Overview

Software architecture degrades when internal layer boundaries erode through convenient cross-boundary imports and circular references. The AST Architectural Guard playbook establishes automated, machine-enforced boundaries across domains, ensuring higher-level layers depend on lower-level abstractions without illegal upward or sideways coupling.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "A quick relative import across domain boundaries is harmless." | Cross-domain imports create spaghetti coupling, circular dependency traps, and prevent extracting standalone packages. | Enforce clean architectural boundaries. Domains must communicate only through explicit public interfaces, events, or shared kernel contracts. |
| "Circular dependencies are fine if the runtime boots without crashing." | Circular imports cause intermittent `undefined` exports, Temporal Dead Zone (TDZ) crashes during startup, and break tree-shaking. | Zero tolerance for circular dependencies. Treat cyclic import warnings as hard errors in CI. |
| "Developer discipline is enough without automated AST tooling." | Discipline degrades under deadline pressure and team expansion. What is not automated will eventually be violated. | Integrate AST linters or dependency graph checkers directly into Git pre-commit hooks and CI gates. |
| "Core domain models can import a utility from an adapter layer." | The Inward Dependency Rule is absolute: core entities must never know about transport layers, web frameworks, or DB drivers. | Keep core zero-dependency. Invert dependencies using ports and interfaces when core needs external capabilities. |
| "TypeScript compiles cleanly, so the architecture must be sound." | Compilers verify type signatures and type compatibility, not architectural topology, module cohesion, or layer encapsulation. | Run architectural boundary linters (Dependency Cruiser, Import Linter, custom AST scripts) alongside `tsc`. |
| "Dynamic import inside functions is a good way to solve circular imports." | Inline dynamic `import()` or runtime `require()` masks cyclic rot instead of fixing the inverted graph relationship. | Extract the shared concept into a lower-tier foundation module or pass dependencies via constructor injection. |

## When to Use

- Monolithic codebases undergoing modularization or domain-driven design (DDD) partitioning.
- Projects implementing Clean Architecture, Hexagonal (Ports & Adapters), or Onion Architecture.
- Preventing and eliminating circular import cycles in growing TypeScript, JavaScript, or Python projects.
- Enforcing monorepo package boundaries (e.g. apps must import packages, but packages must never import apps).

## When NOT to Use

- Early-stage proof-of-concept (PoC) scripts with fewer than 3 files where velocity outweighs architecture.
- Single-module flat utility libraries that do not have distinct domain layers.
- Auto-generated schema stubs or protocol buffer bindings that generate interdependent code by design.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│             AST Architectural Guard Workflow           │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Layer Topology & Boundary Definition                │
│    - Define core, application, adapters, and infra     │
│    - Establish inward dependency direction rules       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Static Import Graph Extraction                      │
│    - Parse AST trees across all source modules         │
│    - Map all internal and external import statements   │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Boundary & Cycle Detection                          │
│    - Evaluate imports against boundary matrix          │
│    - Detect strongly connected components (cycles)     │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Cycle Breaking & Dependency Inversion               │
│    - Extract shared leaf contracts to foundation layer │
│    - Inject dependencies via interfaces/ports          │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. CI Gate Integration & Ratchet Enforcement           │
│    - Wire linter into pre-commit and CI workflows      │
│    - Fail on new boundary violations or circular edges │
└───────────────────────────┘
```

### Step 1: Layer Topology & Boundary Definition
Formulate explicit rules mapping source directories to architectural tiers:
- **Core / Domain** (`src/domain/`): Entities, value objects, business invariants. Zero outer dependencies.
- **Application / Use Cases** (`src/app/`): Orchestration, ports, DTOs. Depends only on Core.
- **Adapters / Transport** (`src/adapters/`): HTTP controllers, GraphQL resolvers, message consumers. Depends on Application.
- **Infrastructure** (`src/infra/`): Database repositories, external API clients, file storage. Implements Application ports.

### Step 2: Static Import Graph Extraction
Extract the full directed import graph using AST parsing or specialized tools:
- **TypeScript**: `npx depcruise --validate .dependency-cruiser.js src`
- **Python**: `import-linter` or custom `ast.parse` scanner.

### Step 3: Boundary & Cycle Detection
Identify and catalog all rule violations:
- Illegal outward dependencies (e.g. `domain` importing from `infra`).
- Cross-domain leakage (e.g. `billing` domain directly querying `inventory` internal tables instead of using public facade).
- Circular loops (A imports B, B imports C, C imports A).

### Step 4: Cycle Breaking & Dependency Inversion
Refactor detected cycles using proven architectural patterns:
- **Extract Shared Kernel**: If A and B depend on each other for types, extract common types into a shared `types` leaf.
- **Dependency Inversion**: If service A calls infrastructure B, define an interface in A's layer and have B implement it.
- **Event-Driven Decoupling**: Replace direct synchronous calls with domain events or observer patterns.

### Step 5: CI Gate Integration & Ratchet Enforcement
Enforce rules automatically on every PR:
- Add checking command to CI pipeline (e.g. `npm run check:arch` or `pytest tests/test_architecture.py`).
- Prevent any new circular dependencies or boundary crossings from being merged.

## Code Examples

### TypeScript Dependency Cruiser Configuration (`.dependency-cruiser.js`)

```javascript
/** @type {import('dependency-cruiser').IConfiguration} */
module.exports = {
  forbidden: [
    {
      name: 'no-circular',
      severity: 'error',
      comment: 'Circular dependencies cause runtime TDZ errors and bundle bloat.',
      from: {},
      to: { circular: true }
    },
    {
      name: 'domain-must-not-depend-on-infra',
      severity: 'error',
      comment: 'Domain core must remain pure and free of infrastructure dependencies.',
      from: { path: '^src/domain' },
      to: { path: '^src/(infra|adapters|api)' }
    },
    {
      name: 'usecases-must-not-depend-on-adapters',
      severity: 'error',
      comment: 'Application use cases should only depend on domain and ports, not controllers.',
      from: { path: '^src/application' },
      to: { path: '^src/(adapters|api)' }
    }
  ],
  options: {
    doNotFollow: { path: 'node_modules' },
    tsPreCompilationDeps: true,
    tsConfig: { fileName: 'tsconfig.json' }
  }
};
```

### Python AST Import Hierarchy Linter (`scripts/lint-architecture.py`)

```python
import ast
from pathlib import Path
import sys

# Allowed dependencies: Layer -> Allowed Target Layers
LAYER_RULES = {
    "domain": set(),  # Pure, no outer dependencies
    "application": {"domain"},
    "adapters": {"domain", "application"},
    "infrastructure": {"domain", "application"},
}

def get_layer(path: Path) -> str | None:
    for part in path.parts:
        if part in LAYER_RULES:
            return part
    return None

def check_architecture(root_dir: str) -> int:
    violations = 0
    src_path = Path(root_dir)

    for py_file in src_path.rglob("*.py"):
        from_layer = get_layer(py_file)
        if not from_layer:
            continue

        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            imported_module = None
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_module = alias.name
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_module = node.module

            if imported_module:
                to_layer = None
                for layer in LAYER_RULES:
                    if f".{layer}" in imported_module or imported_module.startswith(layer):
                        to_layer = layer
                        break

                if to_layer and to_layer != from_layer:
                    allowed = LAYER_RULES[from_layer]
                    if to_layer not in allowed:
                        print(f"[ARCH-VIOLATION] {py_file}:{getattr(node, 'lineno', 1)}")
                        print(f"  Layer '{from_layer}' is forbidden from importing '{to_layer}' ({imported_module})")
                        violations += 1

    return violations

if __name__ == "__main__":
    count = check_architecture("src")
    if count > 0:
        print(f"\nFailed: {count} architectural violation(s) found.")
        sys.exit(1)
    print("Architecture clean: all layer boundaries respected.")
```

### Graphlib Cycle Detection for Monorepo Packages (`scripts/check-cycles.py`)

```python
from graphlib import TopologicalSorter, CycleError
import json
from pathlib import Path
import sys

def check_package_cycles(monorepo_root: str):
    packages_dir = Path(monorepo_root) / "packages"
    graph = {}

    for pkg_json in packages_dir.glob("*/package.json"):
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
        name = data.get("name")
        deps = set()
        for dep_type in ("dependencies", "devDependencies", "peerDependencies"):
            deps.update(data.get(dep_type, {}).keys())
        graph[name] = deps

    # Filter graph to only internal packages
    internal = set(graph.keys())
    clean_graph = {pkg: deps.intersection(internal) for pkg, deps in graph.items()}

    ts = TopologicalSorter(clean_graph)
    try:
        ts.prepare()
        print(f"Verified {len(internal)} packages: zero cyclic package dependencies.")
        return 0
    except CycleError as err:
        print(f"[CYCLE ERROR] Cyclic package dependency detected: {err.args[1]}")
        return 1

if __name__ == "__main__":
    sys.exit(check_package_cycles("."))
```

## Verification Checklist

- [ ] Clear layer boundaries (domain, application, adapters, infra) documented in project guidelines.
- [ ] Static dependency analyzer (Dependency Cruiser, Import Linter, AST script) configured.
- [ ] Circular dependency check passes with zero cycles reported.
- [ ] Inward dependency rule verified: domain layer has zero imports from outer layers.
- [ ] Pre-commit hook or CI pipeline step executes architectural linter on changed files.
- [ ] Monorepo package dependencies form a directed acyclic graph (DAG).
