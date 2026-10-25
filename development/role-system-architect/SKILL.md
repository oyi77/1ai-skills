---
name: role-system-architect
description: Use when orchestrating system architecture, modular decomposition, domain
  boundary enforcement, AST layer guards, and long-term evolutionary design decisions.
domain: development
author: oyi77
version: 1.0.0
category: development
tags:
- architecture
- system-design
- ast-guard
- modularity
- refactoring
- domain-modeling
license: MIT
subdomain: system-architecture
---

## Overview

The `role-system-architect` skill directs the structural integrity, boundaries, and long-term maintainability of production software systems. Instead of allowing architectural decisions to degenerate into vague prose or unmonitored conventions, this role enforces strict domain boundaries, prevents circular and layer-violating dependencies via AST validation, drives god-file decomposition behind backward-compatible facades, and establishes deterministic event-driven integration patterns.

```
[Phase 1: Domain & Layer Topology] ──► [Phase 2: Invariant Scaffolding] ──► [Phase 3: Modular Carve]
                                                                                     │
         [Phase 5: Gate Enforcement] ◄── [Phase 4: Contract Parity] ◄───────────────┘
```

The system architect ensures that software evolvability is protected by automated tests rather than documentation alone, adhering to first-principles thinking and formal decision frameworks.

## When to Use

- When decomposing oversized monolithic god-files or tangled modules into domain submodules.
- When establishing or auditing layer boundaries (e.g. Domain -> Application -> Infrastructure -> Presentation).
- When detecting and eliminating circular import dependencies in Python, TypeScript, or Go codebases.
- When designing distributed or decoupled event-driven architectures (pub/sub, event brokers, CQRS).
- When making high-stakes technical decisions requiring structured trade-off analysis and rollback criteria.
- When standardizing public REST, GraphQL, or RPC API contracts across services.

## When NOT to Use

- When implementing specific isolated bug fixes or localized unit tests (use `development/role-software-engineer`).
- When writing E2E browser automation scripts or load test harnesses (use `development/role-qa-automation-engineer`).
- When managing CI/CD deployment pipelines, container runtimes, or Kubernetes manifests (use `devops/role-devops-sre-engineer`).
- When auditing codebases for external security exploits or vulnerabilities (use `cybersecurity/role-security-engineer`).

## Deterministic Dispatch Matrix

| Architectural Challenge / Objective | Delegated Child Skill | Primary Architectural Output |
|---|---|---|
| Enforcing strict layer boundaries and preventing circular imports | `development/ast-architectural-guard` | AST import graph validator and CI boundary gate |
| Breaking down oversized monolithic god-files (>800 lines) | `development/godfile-ratchet-split` | Domain submodules behind barrel facade with line-cap ratchet |
| Standardizing REST/RPC resource modeling and pagination | `development/api-design` | OpenAPI spec, uniform envelope, and idempotent endpoints |
| Evaluating complex technical options under uncertainty | `mindset/decision-frameworks` | Weighted decision matrix with explicit rollback trigger |
| Designing asynchronous, decoupled pub/sub event systems | `development/event-driven` | Message schema definitions, dead-letter queues, idempotent consumers |
| Deconstructing novel problems down to fundamental truths | `mindset/first-principles-thinking` | Core constraint decomposition and assumption audit |

## Workflow

### Phase 1: Domain Mapping & Boundary Definition

1. Identify core entities, bounded contexts, and trust boundaries.
2. Formulate explicit layer hierarchy (Presentation -> Application Service -> Domain Model -> Infrastructure).
3. If tackling novel architectural constraints, dispatch to `mindset/first-principles-thinking`.

### Phase 2: Invariant Specification & Decision Framing

1. Quantify architectural constraints (max module line count, prohibited cross-domain imports, latency budgets).
2. For architectural trade-offs (e.g. monolithic vs microservices, SQL vs NoSQL, sync vs async), dispatch to `mindset/decision-frameworks` to document non-negotiable tradeoffs and rollback criteria.
3. Design API contracts and resource models using `development/api-design`.

### Phase 3: Modular Decomposition & Refactoring

1. When decomposing monoliths, dispatch to `development/godfile-ratchet-split`.
2. Extract domain logic into focused leaf modules while preserving all existing exports through a backward-compatible barrel facade.
3. Lock module line count using a ratchet test that fails if lines increase in subsequent commits.

### Phase 4: AST Guard & Dependency Verification

1. Dispatch to `development/ast-architectural-guard` to build automated import rule checkers.
2. Assert zero circular dependencies and verify that lower layers never import from upper layers.
3. If async decoupling is required, structure event emitters and consumers via `development/event-driven`.

### Phase 5: Architectural Gate Enforcement & Handoff

1. Integrate architectural lint checks into the CI test pipeline.
2. Verify that 100% of existing call-sites remain intact without deprecation friction.
3. Deliver comprehensive architectural specification with machine-verifiable gates.

## Anti-Rationalization

| Architecture Excuse | Flawed Rationalization | Required Architectural Discipline |
|---|---|---|
| "Circular imports are fine if deferred" | "Python lets us import inside the function body." | Deferred imports mask structural design rot. Refactor shared types into leaf contracts. |
| "A 3,000-line file is easier to navigate" | "Everything is in one place, just use Cmd+F." | Monoliths hide tight coupling and cause merge contention. Split into submodules with ratchet caps. |
| "We will document the architecture in Confluence" | "Engineers just need to read the wiki." | Architectural rules in wikis are ignored. Enforce boundaries with automated AST checks in CI. |
| "Microservices will solve our spaghetti code" | "Separating into repositories forces modularity." | A distributed monolith is strictly worse. Achieve clean bounded contexts in code first. |
| "We don't need an event schema registry" | "Just send JSON payloads; consumer can unpack it." | Schema-less events cause runtime drift. Define strict versioned event contracts. |

## Implementation Examples

### AST Layer Boundary Checker (Python)

```python
import ast
import os
import sys
from typing import Dict, List, Set

class LayerBoundaryValidator(ast.NodeVisitor):
    """Enforces that domain models never import infrastructure or presentation modules."""
    
    FORBIDDEN_IMPORTS: Dict[str, Set[str]] = {
        "domain": {"infrastructure", "presentation", "api", "controllers"},
        "application": {"presentation", "controllers"},
    }
    
    def __init__(self, current_layer: str):
        self.current_layer = current_layer
        self.violations: List[str] = []
        
    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self._check(alias.name, node.lineno)
        self.generic_visit(node)
        
    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            self._check(node.module, node.lineno)
        self.generic_visit(node)
        
    def _check(self, module_name: str, lineno: int):
        forbidden = self.FORBIDDEN_IMPORTS.get(self.current_layer, set())
        root_pkg = module_name.split(".")[0]
        if root_pkg in forbidden:
            self.violations.append(
                f"Line {lineno}: Layer '{self.current_layer}' cannot import '{module_name}'"
            )

def validate_layer(file_path: str, layer: str) -> List[str]:
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=file_path)
    validator = LayerBoundaryValidator(layer)
    validator.visit(tree)
    return validator.violations

if __name__ == "__main__":
    sample_code = "from infrastructure.database import db_conn\nclass User: pass"
    tree = ast.parse(sample_code)
    v = LayerBoundaryValidator("domain")
    v.visit(tree)
    assert len(v.violations) == 1
    print("Layer boundary validation successful:", v.violations[0])
```

### Ratchet Line-Ceiling Test (Bash)

```bash
#!/usr/bin/env bash
set -euo pipefail

TARGET_MODULE="src/services/order_service.py"
MAX_ALLOWED_LINES=350

ACTUAL_LINES=$(wc -l < "$TARGET_MODULE")

echo "Checking ratchet line ceiling for $TARGET_MODULE..."
echo "Current: $ACTUAL_LINES lines | Max Allowed: $MAX_ALLOWED_LINES lines"

if [ "$ACTUAL_LINES" -gt "$MAX_ALLOWED_LINES" ]; then
    echo "ERROR: Ratchet ceiling breached! $ACTUAL_LINES > $MAX_ALLOWED_LINES."
    echo "Decompose functions into submodules before committing."
    exit 1
else
    echo "SUCCESS: Module complies with architectural ratchet limits."
fi
```

## Verification Checklist

- [ ] Domain boundaries and layer hierarchies formally identified.
- [ ] No circular imports exist between modules or packages.
- [ ] Monolithic god-files disassembled into focused leaf modules behind barrel facades.
- [ ] Automated AST lint rules integrated into CI to prevent boundary regression.
- [ ] Architectural decisions documented with explicit trade-offs and rollback criteria.
- [ ] Backward compatibility verified for all existing import paths and public interfaces.
