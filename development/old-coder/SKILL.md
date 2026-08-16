---
name: old-coder
description: Use when implementing high-assurance code with evidence-first development
  — executable spec + gauntlet of constraints (tests, types, coverage, mutation) so
  line-by-line review becomes optional. Triggers on "prove it works", "I won't read
  the code", or high-stakes domains (money, auth, data loss, concurrency, public API).
category: development
domain: development
version: 1.0.0
tags:
- tdd
- evidence-first
- mutation-testing
- quality-assurance
- high-assurance
- test-driven-development
---


# Old Coder: Evidence-First Development

An old coder's strategy for the agent era: don't read the code — make it run the gauntlet. This skill makes coding agents prove their work through executable specifications and evidence reports rather than relying on human code review.

## When to Use

- User explicitly asks for high-assurance or evidence-first work ("reliable", "TDD", "prove it works", "I won't read the code")
- Changes touching high-stakes domains: money, auth, data loss, concurrency, public API
- When you need to produce an executable spec (SPEC) and evidence report (EVIDENCE) instead of relying on code review
- For routine changes where the user just wants normal tests, write good tests directly instead of invoking this loop

---

## Anti-Rationalization Table

| Excuse | Reality | Rule |
|--------|---------|------|
| "The tests pass, isn't that enough?" | Passing tests can be vacuous, mocked, or testing the wrong thing | Mutation testing is mandatory — tests must catch planted bugs |
| "I'll add tests after the implementation" | Post-hoc tests rarely exercise the actual logic paths | RED phase is non-negotiable — watch every test fail first |
| "Coverage is 100%, we're good" | Global coverage % is vanity; changed-line coverage is the constraint | Gate on changed-line coverage with `--cov-fail-under` |
| "This is a trivial change, skip the gauntlet" | Trivial changes in high-stakes domains cause the worst bugs | Scale to blast radius (Tier 1/2/3), never skip silently |
| "The mutation tool is slow/unavailable" | No tool? Manual mutation with a persisted runner script is required | Document every skipped layer and why in EVIDENCE |
| "The spec is good enough, let's code" | An unapproved spec breaks the author-correlation breaker | Human must explicitly approve SPEC before any implementation |
| "I fixed it, the gauntlet passes now" | If you weakened a test or check to make it pass, you destroyed trust | Never weaken tests, never report unrun layers, failing gauntlet blocks done |

---

## Workflow: The Evidence-First Loop

```
SPEC → (human approves spec, not code) → RED → GREEN → REFACTOR → GAUNTLET → EVIDENCE
                                          ↑_____________________|
                                              repeat per behavior
```

### Phase 1: SPEC — The Only Thing the Human Reads Before Code

**Goal**: Turn the request into executable acceptance criteria before touching implementation.

**Steps**:
1. Write behaviors as Gherkin-style scenarios or a named test list — concrete inputs, concrete expected outputs, edge cases, and error cases.
2. Include what the change must NOT do (invariants: existing tests, public API signatures, performance budgets).
3. Include the **setup plan**: tools to install, git usage, files the gauntlet will add, and **every new dependency with a one-line justification**.
4. Write the spec to a file at an **absolute path** (so it's clickable in terminal).
5. Show the spec to the human in plain language and get explicit approval **before writing implementation**.
6. In autonomous mode: state the spec and proceed, but EVIDENCE must record `spec approval: not obtained (autonomous run)` with lower confidence.

**Anti-gaming**: An answer to a question is not an approval. Questions and approval are two exchanges — fold answers in, show revised spec, ask again.

### Phase 2: RED — Prove Each Test Can Fail

**Goal**: Write the test for one behavior, run it, and **watch it fail** before writing implementation.

**Steps**:
1. If module doesn't exist, create a stub that raises (e.g., `NotImplementedError`) so test fails on behavior, not import.
2. Run the new test individually and observe failure.
3. If a new test passes immediately: it's either vacuous or behavior already exists. Prove it — break implementation with a throwaway mutant, watch test fail, restore.
4. Record pre-existing behavior kept as regression armor.

### Phase 3: GREEN — Minimal Implementation

**Goal**: Write the least code that makes the failing test pass.

**Steps**:
1. Implement minimal code for the current behavior.
2. Run the **full suite**, not just the new test.
3. All tests must pass.

### Phase 4: REFACTOR — Clean Up Under Green

**Goal**: Improve names, extract duplication, simplify structure while suite is green.

**Rules**:
- Implementation refactors touch no test files.
- Test-structure refactors (helpers, fixtures) allowed as separate step: assertions unchanged, suite green before and after, then rerun mutation to confirm tests still kill.
- Anything requiring editing an assertion is a behavior change — goes back to SPEC.
- Run suite after each refactor.

### Phase 5: GAUNTLET — The Constraint Stack

**Goal**: Run every applicable layer after all spec behaviors are green. Scale to task (Tier 1/2/3), never skip silently.

| Layer | What It Catches | Tool (Python) | Must Exit Non-Zero |
|-------|----------------|---------------|-------------------|
| Full test suite | Regressions | `pytest -q` | Yes |
| Static types | Whole classes of bugs | `mypy <pkg>` / `pyright` | Yes |
| Lint + format | Latent bugs, drift | `ruff check . && ruff format --check .` | Yes |
| Changed-line coverage | Untested code paths | `pytest --cov=<pkg> --cov-branch --cov-fail-under=100` | **Yes** (critical) |
| Mutation testing | Tests that assert nothing | `mutmut run` (configure in pyproject.toml) | Yes |
| Property-based tests | Edge cases you didn't imagine | `hypothesis` strategies | Yes |
| Complexity budget | Unmaintainable output | Manual review / tools | No (subjective) |
| Real execution | "Passes tests, doesn't run" | Run app/CLI/endpoint on realistic input | Yes |
| Supply chain & secrets | Vulnerable deps, leaked creds | `pip-audit`, `gitleaks` | Yes |
| Suite health | Flaky/order-dependent tests | `pytest-randomly`, repeat suspected flakes | Yes |

**Calibration**:
- **Tier 1 (trivial)**: Full suite + lint. No new tests required, state why.
- **Tier 2 (normal)**: Full loop. Bug fixes MUST start with RED test reproducing the bug.
- **Tier 3 (high stakes — money, auth, data loss, concurrency, public API)**: Full loop + property-based tests + mutation testing (tool-based) + **adversarial pass** — explicitly try to break your own implementation with hostile inputs before declaring done. Write a short **failure model** listing ways this change can hurt, and for each mode add a layer that catches it.

### Phase 6: EVIDENCE — The Only Thing the Human Reads After Code

**Goal**: End with a report the human can trust without opening a single source file.

**Required Sections**:
1. **Spec approval status**: Obtained from user / not obtained (autonomous) with confidence downgrade
2. **Source state**: Commit SHA or sha256 tree hash (persist computation as script)
3. **Toolchain**: Pinned versions file (e.g., `requirements-dev.txt`)
4. **Entry point**: Single command that reruns every layer (e.g., `tools/gauntlet.sh`)
5. **Independent verification**: not performed / passed / failed / blocked (Tier 3 protocol in `verifier.md`)

**Spec → Test Mapping Table**:
| Scenario | Test | Status |
|---|---|---|
| Scenario name | `test_file::test_name` | pass / fail / unverified / n-a |

**Gauntlet Results Table** (all from ONE final fresh run):
| Layer | Command | Result |
|---|---|---|
| Tests | `<cmd>` | N passed, 0 failed |
| Types | `<cmd>` | 0 errors |
| Lint | `<cmd>` | 0 warnings |
| Changed-line coverage | `<cmd>` | covered/total changed lines |
| Mutation | `<tool or manual>` | killed/total killed |
| Property-based | `<cmd>` | N properties, examples each |
| Real execution | `<cmd>` | Observed output |
| Supply chain | `<cmd>` | 0 known vulns; new deps listed with SPEC justification |
| Suite health | `<cmd>` | Randomized order (seed N), all passed |

**Skipped layers**: List each with reason (or "none").

**Honest notes**: Failures hit during task and how resolved, spec revisions, anything reducing confidence.

---

## Code Examples

### Python Project Setup (pyproject.toml)

```toml
[project]
name = "my-project"
version = "0.1.0"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "pytest-randomly>=3.15",
    "hypothesis>=6.100",
    "mutmut>=3.0",
    "mypy>=1.10",
    "ruff>=0.6",
    "pip-audit>=2.7",
    "gitleaks>=8.0",
]

[tool.pytest.ini_options]
addopts = "-q --randomly-seed=last"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]

[tool.mutmut]
source_paths = ["src/"]
tests_dir = "tests/"
runner = "python -m pytest"

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
fail_under = 100
show_missing = true

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.ruff]
target-version = "py311"
line-length = 100
select = ["E", "F", "I", "UP", "B", "C4", "PTH", "T20", "ARG", "SIM", "RUF", "PERF"]
ignore = []
```

### Gauntlet Entry Point Script (tools/gauntlet.sh)

```bash
#!/usr/bin/env bash
set -euo pipefail

# Freshness by mechanism: delete stale artifacts from previous runs
rm -rf .coverage coverage.xml .mutmut-cache htmlcov .pytest_cache

echo "=== GAUNTLET START ==="
echo "Source state: $(git rev-parse HEAD 2>/dev/null || sha256sum $(find . -type f -name '*.py' | sort) | sha256sum | cut -d' ' -f1)"

# 1. Full test suite
echo "--- Tests ---"
python -m pytest -q

# 2. Static types
echo "--- Types ---"
python -m mypy src/

# 3. Lint + format
echo "--- Lint ---"
python -m ruff check .
python -m ruff format --check .

# 4. Changed-line coverage (requires baseline)
echo "--- Changed-line Coverage ---"
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-fail-under=100

# 5. Mutation testing
echo "--- Mutation ---"
python -m mutmut run --paths-to-mutate=src/

# 6. Property-based tests (included in pytest run above)
echo "--- Properties ---"
python -m pytest -q -k "property"

# 7. Real execution
echo "--- Real Execution ---"
python -m src.cli --help  # or run actual CLI/app on realistic input

# 8. Supply chain & secrets
echo "--- Supply Chain ---"
python -m pip_audit
gitleaks detect --source . --verbose --redact

# 9. Suite health
echo "--- Suite Health ---"
python -m pytest -q --randomly-seed=last --randomly-dont-reorganize

echo "=== GAUNTLET COMPLETE ==="
```

### SPEC Template (spec.md)

```markdown
# SPEC: <Task Name>

**Tier**: 1 | 2 | 3
**Approval**: [ ] Obtained from user / [ ] Not obtained (autonomous)

## Behaviors (Gherkin-style)

### Feature: <Capability in user language>

#### Scenario: <One concrete behavior>
**Given** <concrete starting state>
**When** <concrete action with concrete input>
**Then** <concrete observable outcome, exact values>

#### Scenario: <Error case>
**Given** <starting state>
**When** <invalid/hostile input>
**Then** <exact error type/message/status, and what state must NOT change>

## Negative Constraints (Must NOT)

| Invariant | Verification Method |
|-----------|---------------------|
| Existing tests still pass | Full suite baseline |
| Public API signatures unchanged | API compatibility check (griffe) |
| No new network/filesystem/env usage | Capability diff |

## Setup Plan

- Tools to install: (from `requirements-dev.txt`)
- Git: init / checkpoint commit cadence
- Files gauntlet will add: `tests/`, `tools/gauntlet.sh`, `tools/mutants.py`
- New dependencies: (each with one-line justification)

## Failure Model (Tier 3 only)

| Failure Mode | Layer That Catches It |
|--------------|----------------------|
| Race condition | `go test -race` / threading stress + rerun |
| Parser edge case | Property-based tests (hypothesis) |
| Silent production failure | Observability assertions in tests |
| Rollback failure | Migration rehearsal test |
```

### EVIDENCE Template (evidence.md)

```markdown
## Evidence Report — <Task Name> (Tier <1|2|3>)

- Spec approval: <obtained | not obtained (autonomous)>
- Source state: <commit SHA | tree hash>
- Toolchain: <requirements-dev.txt>
- Entry point: `./tools/gauntlet.sh`
- Independent verification: <not performed | passed | failed | blocked>

### Spec → Test Mapping

| Scenario | Test | Status |
|---|---|---|
| Happy path: divide(10, 2) = 5 | `test_math.py::test_divide_happy` | pass |
| Error: divide(1, 0) raises ZeroDivisionError | `test_math.py::test_divide_by_zero` | pass |
| Must NOT: change existing API | `griffe` diff | pass |

### Gauntlet (Final Fresh Run)

| Layer | Command | Result |
|---|---|---|
| Tests | `pytest -q` | 47 passed, 0 failed |
| Types | `mypy src` | 0 errors |
| Lint | `ruff check . && ruff format --check .` | 0 warnings |
| Changed-line coverage | `pytest --cov=src --cov-fail-under=100` | 31/31 lines, 20/20 branches |
| Mutation | `mutmut run` | 22/22 killed |
| Property-based | `pytest -k property` | 5 properties, 200 examples each |
| Real execution | `python -m src.cli 10 2` | `5.0` |
| Supply chain | `pip-audit && gitleaks detect` | 0 vulns; 0 new deps |
| Suite health | `pytest --randomly-seed=last` | seed 42, all passed |

### Skipped Layers
- none

### Honest Notes
- Mutation runner initially had cache bug (fixed in tools/mutants.py with mtime pinning)
- Spec revised once: added negative constraint for env var access
```

### Manual Mutation Runner (tools/mutants.py)

```python
#!/usr/bin/env python3
"""
Manual mutation runner for ecosystems without a mature mutation tool.
Persisted in repo so EVIDENCE is reproducible.
Proves it executed each mutant via mtime pinning + cache check.
"""
import subprocess
import sys
import os
import hashlib
from pathlib import Path

MUTANTS = [
    # (file, original_snippet, mutated_snippet, description)
    ("src/rate_limiter.py", "if current >= limit:", "if current > limit:", "off-by-one: >= -> >"),
    ("src/rate_limiter.py", "return tokens >= cost", "return tokens > cost", "off-by-one: >= -> >"),
    ("src/rate_limiter.py", "self.tokens = min(self.tokens + rate, capacity)", "self.tokens = min(self.tokens + rate, capacity - 1)", "capacity off-by-one"),
    ("src/rate_limiter.py", "async def acquire", "async def acquire_not_called", "delete method"),
    ("src/rate_limiter.py", "return True", "return False", "flip boolean return"),
]

def file_hash(path: Path) -> str:
    return hashlib.md5(path.read_bytes()).hexdigest()

def run_tests() -> bool:
    result = subprocess.run([sys.executable, "-m", "pytest", "-q"], capture_output=True)
    return result.returncode == 0

def main():
    src_files = [Path(m[0]) for m in MUTANTS]
    original_hashes = {f: file_hash(f) for f in src_files}

    killed = 0
    total = len(MUTANTS)

    for file_path, original, mutated, desc in MUTANTS:
        path = Path(file_path)
        content = path.read_text()

        if original not in content:
            print(f"FAIL: mutant pattern not found: {desc}")
            sys.exit(1)

        # Apply mutant
        mutated_content = content.replace(original, mutated, 1)
        path.write_text(mutated_content)

        # Prove execution: mtime must change, no bytecode cache reuse
        new_hash = file_hash(path)
        if new_hash == original_hashes[path]:
            print(f"FAIL: mutant did not change file hash: {desc}")
            sys.exit(1)

        print(f"Testing mutant: {desc}")
        if not run_tests():
            print(f"  KILLED")
            killed += 1
        else:
            print(f"  SURVIVED - missing test!")
            # Restore and fail
            path.write_text(content)
            print(f"Manual mutation: {killed}/{total} killed")
            sys.exit(1)

        # Restore
        path.write_text(content)
        restored_hash = file_hash(path)
        if restored_hash != original_hashes[path]:
            print(f"FAIL: restore mismatch for {desc}")
            sys.exit(1)

    print(f"Manual mutation: {killed}/{total} killed")
    # Final verification
    if not run_tests():
        print("FAIL: suite not green after restore")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## Verification Checklist

Run this checklist before claiming the task is complete:

- [ ] **SPEC written to absolute path** and contains: behaviors (Gherkin/named tests), negative constraints, setup plan with justified dependencies, failure model (Tier 3)
- [ ] **Human explicitly approved SPEC** before any implementation (or autonomous mode noted in EVIDENCE)
- [ ] **RED phase**: Every new test observed failing individually before implementation
- [ ] **GREEN phase**: Minimal implementation, full suite passes
- [ ] **REFACTOR phase**: Only under green, assertions frozen, mutation rerun after test-structure changes
- [ ] **GAUNTLET**: Every applicable layer run, all exit non-zero on failure, no silent skips
- [ ] **Changed-line coverage**: Gates at 100% with `--cov-fail-under` (not just reports %)
- [ ] **Mutation testing**: Tool-based preferred; manual with persisted runner that proves execution
- [ ] **EVIDENCE report**: Single final fresh run, reproducible entry point, spec→test mapping, all layers with commands+results, skipped layers with reasons, honest notes
- [ ] **Anti-gaming**: No weakened tests, no simultaneous test+impl edits, no mocking unit under test, no coverage chasing, no unrun layers reported
- [ ] **Tier 3**: Failure model written, adversarial pass performed, independent verification protocol acknowledged
- [ ] **Independent verification** (Tier 3): `verifier.md` protocol executed or explicitly marked not performed with confidence downgrade

---

## References

- Original repo: https://github.com/AmazingAng/old-coder
- Gauntlet tooling by ecosystem: `references/gauntlet.md`
- Verifier protocol (Tier 3): `references/verifier.md`
- Verifier case study: `references/verifier-case-study.md`
- Demo project: `demo-rate-limiter/` (shows 41 tests, 100% coverage, 22/22 mutants killed)