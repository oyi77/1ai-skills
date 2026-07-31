---
name: linter-agent
description: Use when detect and fix code style violations, enforce project conventions, ensure consistent formatting.
domain: agents
author: oyi77
license: Apache-2.0
subdomain: ai-agents
tags:
  - agent
  - ai-agent
  - automation
  - linter
  - coding
version: 1.0.0
---

# Linter Agent

Quick Reference — see parent for full agent ecosystem.

The Linter Agent enforces code style, convention rules, and formatting standards across the codebase at scale. It goes beyond running a tool — it interprets project-specific conventions that static linters cannot express, fixes violations in bulk, migrates rules when upgrading linters, and surfaces only the warnings that matter. Its job is to make the codebase look like one person wrote it, even when fifty people contributed.



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

- **Apply project conventions**: Enforce naming, import ordering, error-handling patterns, and file structure rules that go beyond automated linter config
- **Bulk fix and migrate**: Run across entire directories with auto-fix, handle rule migrations (e.g., eslint flat config), and clean up after dependency updates
- **Surface actionable results**: Suppress noise from rules the team has consciously decided to ignore; report only violations that need human attention

## Code Example

```python
"""Minimal linter agent pattern — scan and fix."""

import json, subprocess, sys
from pathlib import Path

def lint(paths: list[str], config: str | None = None, auto_fix: bool = True) -> dict:
    results = {"files_scanned": 0, "errors": 0, "warnings": 0, "auto_fixed": 0}

    for p in paths:
        target = Path(p)
        if not target.exists():
            continue

        # Run the linter (simplified — real agent integrates tool output)
        cmd = ["ruff", "check", str(target)]
        if auto_fix:
            cmd.append("--fix")
        if config:
            cmd.extend(["--config", config])

        result = subprocess.run(cmd, capture_output=True, text=True)

        # Parse output (simplified — real agent parses JSON/SARIF)
        results["files_scanned"] += 1
        if result.returncode != 0:
            results["errors"] += 1

    # Apply project-specific conventions the linter cannot enforce
    for p in paths:
        for file in Path(p).rglob("*.py"):
            content = file.read_text()
            # Detect and fix common patterns (example: ensure newline at EOF)
            if content and not content.endswith("\n"):
                file.write_text(content + "\n")
                results["auto_fixed"] += 1

    return results

if __name__ == "__main__":
    result = lint(sys.argv[1:])
    print(json.dumps(result, indent=2))
```

## Checklist

- [ ] Zero lint errors after auto-fix (warnings may remain if intentionally accepted)
- [ ] Project-specific conventions verified: naming, imports, error handling, comments
- [ ] No new warnings introduced compared to baseline
- [ ] Linter config committed and consistent across CI and local environments
- [ ] False positives documented with justification (for rule suppression)

## Workflow

1. **Identify** the task or trigger.
2. **Prepare** inputs and configure parameters.
3. **Execute** the core routine.
4. **Verify** the output against expected results.
5. **Iterate** based on feedback or new data.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will fix formatting in the next PR" | Postponing lint debt compounds — every new file copies the bad patterns, making the eventual cleanup harder |
| "My editor already highlights these" | Highlighted warnings you habitually ignore become permanent noise. The linter agent treats them as blockers |
| "We have too many false positives to run lint strictly" | Each false positive deserves a rule suppression with a reason, not a habit of ignoring all warnings |

## When to Use

Use before every PR commit, after merge conflicts, when adopting new lint rules or migrating configs, after bulk code generation, and when on-boarding new team members to enforce standards. Do NOT use on generated code (protobuf, OpenAPI stubs) or vendored dependencies where upstream formatting is outside your control.
