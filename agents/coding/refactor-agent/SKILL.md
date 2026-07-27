---
name: refactor-agent
description: Use when restructure code to improve readability, maintainability, extensibility without changing external behavior.
domain: agents
author: mahipal
license: Apache-2.0
subdomain: ai-agents
tags:
  - agent
  - ai-agent
  - automation
  - refactor
  - coding
version: 1.0.0
---

# Refactor Agent

Quick Reference — see parent for full agent ecosystem.

The Refactor Agent restructures code to improve readability, maintainability, and extensibility without changing external behavior. It systematically identifies high-complexity functions, duplicated logic, dead code, and tightly coupled modules; then applies targeted refactorings (extract method, split module, introduce interface, remove duplication) with verification that all existing tests still pass. Its mantra: make the change easy, then make the easy change.



## When Not to Use

- **Simple or one-off tasks** — if the task is straightforward, direct execution is faster than structured methodology.
- **Already established workflows** — follow existing team conventions rather than introducing new frameworks.
- **When automation overhead exceeds benefit** — for very small scopes, the setup cost may not be justified.


## Dependencies

- Python 3.8+ or Node.js 18+
- Access to relevant APIs/services for your specific use case
- Basic understanding of the domain concepts


## Commands

```bash
# Refer to the skill's usage section for specific commands
# Adapt these to your workflow
```
## Key Responsibilities

- **Measure complexity**: Calculate cyclomatic complexity, cognitive complexity, and coupling metrics to identify the files that need refactoring most
- **Apply pattern-driven refactors**: Extract methods, split monoliths, introduce abstractions, remove dead code — each with a defined before/after signature
- **Preserve behavior**: Run the full test suite before and after every refactoring step to confirm zero behavioral changes

## Code Example

```python
"""Minimal refactor agent pattern — analyze and restructure."""

import json, sys
from pathlib import Path

def analyze_complexity(file_path: str) -> dict:
    """Analyze a file for refactoring candidates."""
    content = Path(file_path).read_text()
    lines = content.split("\n")

    functions = []
    current_fn = None
    fn_lines = 0
    branch_count = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("def ") or stripped.startswith("async def "):
            if current_fn:
                functions.append({
                    "name": current_fn, "lines": fn_lines,
                    "branches": branch_count, "line": i - fn_lines + 1
                })
            current_fn = stripped.split("(")[0].replace("def ", "").replace("async ", "")
            fn_lines = 1
            branch_count = 0
        elif current_fn:
            fn_lines += 1
            if any(kw in stripped for kw in ["if ", "elif ", "for ", "while ", "and ", "or "]):
                branch_count += 1

    if current_fn:
        functions.append({
            "name": current_fn, "lines": fn_lines,
            "branches": branch_count, "line": len(lines) - fn_lines + 1
        })

    candidates = [f for f in functions if f["branches"] > 10 or f["lines"] > 50]

    return {
        "file": file_path, "total_lines": len(lines),
        "functions": functions,
        "candidates": candidates,
        "recommendations": [
            f"Extract method: {c['name']} ({c['branches']} branches, {c['lines']} lines)"
            for c in candidates
        ]
    }

if __name__ == "__main__":
    result = analyze_complexity(sys.argv[1])
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] Full test suite passes before and after refactoring (same pass/fail count)
- [ ] Cyclomatic complexity reduced below team threshold (<12 per function recommended)
- [ ] Dead code removed: unused functions, parameters, imports, and variables
- [ ] Public API unchanged (consumers should not notice the refactor)
- [ ] Each refactoring step committed separately for clean review

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "It works, do not touch it" | Working-but-complex code has the highest bug rate per line. Refactoring now prevents production incidents later |
| "I will refactor while adding the feature" | Mixing refactoring with feature work creates unreviewable diffs and hides regressions in the noise |
| "The tests are fragile, I cannot refactor" | Fragile tests are the exact reason to refactor first — make the code testable before making the easy change |

## When to Use

Use before adding features to complex code, when cyclomatic complexity exceeds team thresholds, when duplicate code spans multiple files, when dead code clutters navigation, and when migrating from old patterns to modern alternatives. Do NOT use for auto-generated code, vendored dependencies, or code scheduled for complete replacement.
