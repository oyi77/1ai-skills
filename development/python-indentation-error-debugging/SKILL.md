---
name: python-indentation-error-debugging
description: Use when Python fails to boot with IndentationError or unexpected indent traceback
domain: development
author: oyi77
license: Apache-2.0
subdomain: debugging
tags:
- python
- debugging
- indentation
- indentationerror
triggers:
- python indentation error
- IndentationError unexpected indent
- fix python indent
- deindent broken block
- python boot crash
version: 1.0.0
category: development
---

## Overview

Python parses indentation, not braces; a single line shifted by four or more spaces below its sibling can flip a clean run into `IndentationError: unexpected indent` and abort every module that imports the file. The error is precise (file, line, expected column) but the fix is rarely "guess and re-indent by hand" — it is a deterministic de-indent of the stray guard until the traceback collapses to a green import.

## When to Use

- Python project refuses to import or boot with `IndentationError` / `TabError`.
- Traceback names `unexpected indent` at a specific `line N` with a shown caret `^`.
- A recent edit touched a loop, `if`, `try`, or guard body and the module now fails to load.
- Eager keyword: "indentation error", "unexpected indent", "deindent", "python boot crash".

## When NOT to Use

- Syntax is fine and the failure is a runtime `ValueError`, `TypeError`, or `AttributeError` — use `development/systematic-debugging`.
- Embedded DSL or mixed tabs/spaces not owned by you — escalate, do not auto-reformat.
- You have not read the offending file; re-read first and compare the caret column.
- Auto-formatting with black/PEP8 is required by project gate; use the formatter, not manual de-indent.

## Process

### Step 1 — Read the traceback literally

Python reports `File "<path>", line <N>` and prints the offending line with `SyntaxError: unexpected indent` and a caret `^` under the first over-indented character. The caret column is the fix target; do not edit neighboring lines.

### Step 2 — Identify the stray block

Locate the guard/loop body immediately above line `N`. Common shape: a `for`, `if`, or `try` whose body gained an extra 4-space (or duplicated `raise`/`return`) line inserted by an editor at the wrong indentation.

### Step 3 — De-indent deterministically

Remove the extra leading spaces from the stray line so it sits at the column Python expected. For duplicated guards inside a `for` loop, collapse the duplicate into one statement at the loop body column (4 spaces, not 8).

### Step 4 — Verify

Run `python -c "import <module>"` and confirm zero output. Then re-run the boot command; expect the service to pass readiness.

## Real-World Case (1ai-hub crash)

File `src/mcp/tool_registry.py`, line 55. A `for tool in self.tools:` loop body contained a duplicated guard:

```python
for tool in self.tools:
    if tool.name == name:
        raise ValueError(f"Duplicate tool name: {name}")
        raise ValueError(f"Duplicate tool name: {name}")  # stray, 8-space indent
```

The second `raise` sits one indentation level deeper than the `if` body, so Python raises `IndentationError: unexpected indent`. Collapse to a single raise at the 4-space column of the `if` body:

```python
for tool in self.tools:
    if tool.name == name:
        raise ValueError(f"Duplicate tool name: {name}")
```

Boot green after the collapse; no behavior change because the first raise already short-circuits.

## Reproduction

```python
# repro_indent.py
def register(self, name):
    for tool in self.tools:
        if tool.name == name:
            raise ValueError(f"Duplicate tool name: {name}")
            raise ValueError(f"Duplicate tool name: {name}")  # bug: 8 spaces
```

```bash
python -c "import repro_indent"
```

Expected error:

```text
IndentationError: unexpected indent (repro_indent.py, line 5)
```

Fix with `deindent` (manual): remove the extra 4-space column from line 5 so both raises collapse into one statement at the `if` body column, delete the duplicate, then re-run.

## Anti-Rationalization Table

| Rationalization | Reality |
| --- | --- |
| "It's just whitespace; ignore and ship" | Python refuses to parse the module; app never boots. |
| "Re-indent the whole block with black" | May mask the duplicate and change scope; de-indent the stray line only. |
| "Add a try/except around the import" | Hides a parse error that must be fixed at source. |
| "Move the file out of the import path" | Breaks features; the real fix is one column adjustment. |

## Verification

After completing this skill, confirm:

- [ ] `python -c "import <module>"` exits 0 with no output.
- [ ] The boot command's readiness probe returns green.
- [ ] Diff is minimal: only the stray indentation column (and duplicate line) changed.
- [ ] No formatter or unrelated whitespace churn introduced.

## Code Example

```python
import ast

def fix_duplicate_raise(source: str) -> str:
    """Collapse an over-indented duplicate raise inside a for-loop guard."""
    lines = source.splitlines()
    out = []
    for line in lines:
        # Strip one level (4 spaces) from any line carrying a duplicate guard
        if line.strip().startswith("raise ValueError(f\"Duplicate"):
            out.append(line.lstrip("    ") if line.startswith("        ") else line)
        else:
            out.append(line)
    return "\n".join(out)
```

## Triggers

- python indentation error
- IndentationError unexpected indent
- fix python indent
- deindent broken block
- python boot crash

## Anti-Rationalization (pivot)

Shortcut: patch the import site instead of the source. Reality: the module still fails to parse wherever it is imported; fix the indentation at the origin.
---
path: development/python-indentation-error-debugging/SKILL.md