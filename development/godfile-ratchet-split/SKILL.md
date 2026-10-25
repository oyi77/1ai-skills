---
name: godfile-ratchet-split
description: Carving monolithic god-files and oversized modules into decoupled domain units behind backward-compatible barrel facades with ratchet size caps. Use when refactoring complex legacy files, breaking 800-line limits, or eliminating circular dependency webs.
domain: development
subdomain: software-development
author: oyi77
license: Apache-2.0
version: 1.0.0
category: development
tags:
  - refactoring
  - god-file
  - architecture
  - clean-code
  - modularization
  - ratchet-test
---

## Overview

Monolithic files (>800–1000 lines) concentrate disproportionate cognitive load, trigger merge collisions during concurrent development, and conceal circular dependencies. The God-File Ratchet Split playbook establishes a zero-regression, seam-driven methodology for dismantling oversized modules into cohesive submodules while preserving the public API through backward-compatible barrel facades and locking file size limits via automated CI ratchet tests.

## Anti-Rationalization Table

| Rationalization | Engineering Reality | Strict Protocol |
|---|---|---|
| "The god-file is already working in production; refactoring it adds risk." | Monolithic files accumulate invisible coupling, resist automated testing, and make bug fixes exponentially riskier over time. | Refactor using safe, bite-sized seams protected by baseline regression tests. Zero logic modifications during the extraction phase. |
| "We should rewrite the entire module from scratch in a new branch." | Full rewrites in long-running branches drift from active production development, create merge nightmares, and are routinely abandoned. | Use iterative extraction in place. Carve one domain slice at a time while keeping the test suite green on every commit. |
| "Moving functions breaks existing imports across the entire codebase." | Broken imports trigger widespread churn across unrelated files and cause build breaks. | Maintain the original file as a barrel facade that re-exports all extracted symbols. External callers experience zero disruption. |
| "Code reviews are sufficient to keep the file from growing again." | Without automated CI enforcement, developers will instinctively append new functions to familiar god-files, regressing the fix. | Install an automated ratchet test that asserts the file size never exceeds the newly reduced line count. |
| "Refactoring is just file reorganization, so tests are not required." | Unintentional changes to closure scopes, variable hoisting, or module initialization order cause subtle runtime regressions. | Run comprehensive regression test suites before and after extraction. Re-export signatures must maintain byte-level behavioral parity. |
| "Circular imports between child submodules are acceptable during transitions." | Inter-module circular dependencies cause runtime `ImportError: cannot access name before initialization` or `undefined` imports. | Structure submodules in a strict hierarchy or extract shared primitives into an independent `types` or `utils` leaf module. |

## When to Use

- Source files exceeding 800 lines of code in TypeScript, JavaScript, Python, or Go.
- High-churn files where concurrent developer branches repeatedly encounter complex git merge conflicts.
- Codebases enforcing strict modularity gates where single files fail automated complexity or size linters.
- Monolithic utility, controller, or service files that mix business logic, database queries, and wire formatting.

## When NOT to Use

- Generated client stubs (e.g. gRPC protobuf outputs, Prisma generated clients, auto-generated OpenAPI schemas).
- Small files (<500 lines) that possess high cohesion and single-responsibility focus.
- Prototype or throwaway experiment scripts that are not part of the core application codebase.

## Workflow

```
┌────────────────────────────────────────────────────────┐
│            God-File Ratchet Split Workflow             │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 1. Seam Analysis & Dependency Graph Mapping            │
│    - Identify symbol clusters and shared state         │
│    - Map inward and outward dependencies               │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 2. Pre-Extraction Test Harness Establishment           │
│    - Run existing tests to verify baseline green state │
│    - Add characterization tests if coverage is sparse  │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 3. Submodule Extraction & Barrel Facade Preservation   │
│    - Move cohesive functions into focused child files  │
│    - Convert original god-file into barrel re-exporter │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 4. Circular Dependency Audit & Seam Verification       │
│    - Verify zero cycles between extracted submodules   │
│    - Test both internal and barrel entry imports       │
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│ 5. Automated CI Ratchet Test Locking                   │
│    - Assert original file length <= new reduced ceiling│
│    - Fail CI if file size expands in future commits    │
└───────────────────────────┘
```

### Step 1: Seam Analysis & Dependency Graph Mapping
Analyze the monolithic file to discover natural architectural seams:
- Group functions and types by their domain concern (e.g., validation, database I/O, serialization, orchestration).
- Identify shared module-level state, global variables, and configuration objects.
- Leaf primitives (types, interfaces, pure utilities) must be extracted first.

### Step 2: Pre-Extraction Test Harness Establishment
Ensure the behavior of the god-file is strictly captured before touching code:
- Execute the full test suite and confirm 100% pass rate.
- If test coverage is low, write integration characterization tests against the public entry points.

### Step 3: Submodule Extraction & Barrel Facade Preservation
Extract functions incrementally without breaking existing call sites:
- Create a directory matching the module name (e.g., `services/user/` for `services/user.ts`).
- Move grouped logic into dedicated files: `validator.ts`, `repository.ts`, `formatter.ts`.
- In the original file (`user.ts`), replace the extracted implementations with re-export statements (`export * from './user/validator'`).

### Step 4: Circular Dependency Audit & Seam Verification
Verify the structural integrity of the extracted modules:
- Check that child modules do not cross-import circularly (`validator` importing `repository` while `repository` imports `validator`).
- Use tools like `madge` (JS/TS) or `pydeps` (Python) to confirm an acyclic dependency graph.

### Step 5: Automated CI Ratchet Test Locking
Prevent regression by installing a ratchet test:
- The ratchet test measures the line count of the carved file.
- If a future PR adds lines to the barrel facade, CI fails, forcing developers to put new code into submodules.

## Code Examples

### Ratchet Test for File Size Enforcement (TypeScript / Vitest)

```typescript
import { describe, it, expect } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';

describe('Architecture Ratchet: services/order-service.ts', () => {
  const TARGET_FILE = path.resolve(__dirname, '../src/services/order-service.ts');
  const MAX_PERMITTED_LINES = 150; // Strict ceiling after splitting the 1,400-line god-file

  it(`must not exceed ${MAX_PERMITTED_LINES} lines (enforcing submodule delegation)`, () => {
    expect(fs.existsSync(TARGET_FILE)).toBe(true);

    const content = fs.readFileSync(TARGET_FILE, 'utf-8');
    const lineCount = content.split('\n').length;

    expect(lineCount).toBeLessThanOrEqual(MAX_PERMITTED_LINES);
  });

  it('must act strictly as a barrel facade (re-exporting submodules)', () => {
    const content = fs.readFileSync(TARGET_FILE, 'utf-8');
    
    // Disallow heavy inline class/function definitions inside the facade
    const inlineFunctionCount = (content.match(/function\s+[a-zA-Z0-9_]+\s*\(/g) || []).length;
    const inlineClassCount = (content.match(/class\s+[a-zA-Z0-9_]+/g) || []).length;

    expect(inlineFunctionCount).toBe(0);
    expect(inlineClassCount).toBe(0);
  });
});
```

### Python Monolith Extraction Pattern (`services/payment.py`)

```python
# BEFORE: 1,200 lines in services/payment.py mixing Stripe, PayPal, DB access, and PDF generation.

# AFTER: services/payment.py becomes a clean backward-compatible facade:
"""
Payment Service Facade.
All implementations have been carved into the services/payment/ package.
This module maintains backward-compatibility for all existing imports.
"""

from services.payment.types import PaymentIntent, PaymentResult, PaymentStatus
from services.payment.stripe_adapter import StripeGateway
from services.payment.paypal_adapter import PayPalGateway
from services.payment.repository import PaymentLedgerRepository
from services.payment.invoicing import generate_tax_invoice
from services.payment.orchestrator import PaymentOrchestrator

# Re-export all symbols for existing callers
__all__ = [
    "PaymentIntent",
    "PaymentResult",
    "PaymentStatus",
    "StripeGateway",
    "PayPalGateway",
    "PaymentLedgerRepository",
    "generate_tax_invoice",
    "PaymentOrchestrator",
]
```

### Python CI Ratchet Enforcement Script (`scripts/check-godfile-ratchet.py`)

```python
import sys
from pathlib import Path

# Registry of monitored files and their mandatory line ceilings
RATCHET_LIMITS = {
    "src/controllers/api_controller.py": 120,
    "src/services/payment.py": 80,
    "src/lib/data_pipeline.py": 200,
}

def audit_ratchet_limits() -> int:
    failures = 0
    for file_path_str, max_lines in RATCHET_LIMITS.items():
        file_path = Path(file_path_str)
        if not file_path.exists():
            print(f"[SKIP] {file_path_str} does not exist.")
            continue

        lines = len(file_path.read_text(encoding="utf-8").splitlines())
        if lines > max_lines:
            print(f"[FAIL] {file_path_str}: {lines} lines exceeds ratchet cap of {max_lines}!")
            failures += 1
        else:
            print(f"[PASS] {file_path_str}: {lines}/{max_lines} lines.")

    return failures

if __name__ == "__main__":
    failed_count = audit_ratchet_limits()
    if failed_count > 0:
        print(f"\nERROR: {failed_count} file(s) violated architectural line ratchet limits.")
        sys.exit(1)
    print("\nSUCCESS: All files within architectural ratchet limits.")
```

## Verification Checklist

- [ ] Baseline test suite passes 100% prior to beginning extraction.
- [ ] Submodules organized into a cohesive directory structure by domain concern.
- [ ] Original file converted into a backward-compatible barrel facade re-exporting all symbols.
- [ ] No circular dependencies introduced between extracted sibling submodules.
- [ ] Automated ratchet test implemented in CI enforcing the reduced line ceiling.
- [ ] Zero changes to business logic or runtime behavior during the split.
