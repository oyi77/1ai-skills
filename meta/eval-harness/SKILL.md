---
name: eval-harness
description: Use when setting up eval-driven development (EDD) for AI-assisted workflows, defining pass/fail criteria for agent task completion, measuring reliability with pass@k metrics, creating regression suites for prompt or agent changes, or benchmarking performance across model versions.
domain: meta
subdomain: self-improvement
category: meta
version: 1.0.0
author: oyi77
license: Apache-2.0
tags:
- evaluation
- edd
- benchmarking
- regression-testing
- pass-at-k
- prompt-engineering
triggers:
- eval harness
- evaluate agent
- benchmark skill
- pass at k
- edd
- eval driven development
argument-hint: "[eval name or feature]"
---

# Eval Harness

## Overview

Formal evaluation framework implementing eval-driven development (EDD). Evals are the unit tests of AI development: define expected behavior BEFORE implementation, run continuously during development, track regressions with each change, measure reliability with pass@k metrics.

## When to Use

**Trigger phrases:**
- "eval harness", "evaluate agent", "benchmark skill"
- "pass@k", "eval driven development", "regression eval"

Use directly when:
- Setting up EDD for a new agent workflow or skill.
- Defining pass/fail criteria before shipping a prompt or agent change.
- Measuring reliability across model versions or harnesses.
- Creating regression suites for skill modifications.
- Comparing candidate vs baseline skill output (blind eval).

## When NOT to Use

- Ordinary code test suites → use `test-driven-development` or language-native runners.
- One-off manual checks with no repeatability requirement.
- Production monitoring → use `observability` skills.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll eyeball the output, no need for formal evals." | Eyeballing doesn't survive model updates. A saved eval catches regressions automatically next week. |
| "Evals take too long to set up." | A 5-case eval takes 10 minutes and pays back on every subsequent change. Unmeasured changes ship blind. |
| "One passing run proves it works." | LLMs are stochastic. Run pass@k (typically k=5) to measure reliability, not luck. |
| "Grading by another LLM is cheating." | LLM-as-judge is standard practice for subjective outputs. Pin the judge model version and use rubrics for consistency. |

## Workflow

### 1. Define Success Criteria (Before Implementation)

```markdown
[EVAL: feature-name]
Task: Description of what the agent should accomplish
Inputs: Fixture files, prompts, or API mocks
Success Criteria:
  - [ ] Criterion 1 (binary: met / not met)
  - [ ] Criterion 2
  - [ ] Criterion 3
Expected Output Shape: Schema or example
```

Every criterion must be mechanically checkable or rubric-scored—never "looks good".

### 2. Choose Grader Type

| Grader | Use For | Method |
|---|---|---|
| **Code-based** | Deterministic outputs (files, JSON, build artifacts) | Bash/python assertion scripts |
| **Exact-match** | Fixed strings, IDs, enum values | String equality |
| **LLM-as-judge** | Subjective quality (writing, design rationale) | Rubric + pinned judge model |
| **Human review** | Gold-standard calibration only | Sample 10% of runs monthly |

Prefer code-based graders. Reserve LLM judges for genuinely subjective dimensions.

### 3. Build the Eval Runner

Minimal Python harness pattern:

```python
import json, subprocess, sys
from pathlib import Path

CASES = sorted(Path("evals/cases").glob("*.json"))
passed = 0
for case_path in CASES:
    case = json.loads(case_path.read_text())
    # run agent/command under test
    result = subprocess.run(
        [sys.executable, "run_task.py", "--input", str(case_path)],
        capture_output=True, text=True, timeout=120,
    )
    ok = all(check(result.stdout, c) for c in case["criteria"])
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {case_path.name}")
print(f"\npass@1: {passed}/{len(CASES)}")
```

Store cases as JSON fixtures under `evals/cases/`; one file per scenario.

### 4. Measure Reliability (pass@k)

Run each case k times (default k=5):
- **pass@1**: single-run success rate
- **pass@k**: probability at least one of k runs succeeds
- **cons@k**: all k runs succeed (stability metric)

Track deltas between baseline and candidate:

```text
Baseline (main):   pass@1 = 80%, cons@5 = 60%
Candidate (feat):  pass@1 = 90%, cons@5 = 75%
Verdict:           SHIP — both reliability and stability improved
```

### 5. Regression Eval After Changes

```markdown
[REGRESSION EVAL: feature-name]
Baseline: git SHA or checkpoint tag
Cases: N total
Result: X/N passed (previously Y/N)
New failures: [list]
Flaky failures: [list — passed on rerun]
```

Any new hard failure blocks the merge until fixed or the eval is proven wrong.

## Eval Types

| Type | Purpose | Frequency |
|---|---|---|
| **Capability eval** | Prove the agent CAN do something new | Before shipping a feature |
| **Regression eval** | Prove nothing broke | Every PR touching prompts/skills |
| **Benchmark eval** | Compare models/harnesses/skills | Weekly or on model version bump |
| **Blind A/B eval** | Candidate vs baseline without knowing which is which | Skill style/rule changes |

## Skill Quality Gates (3-Tier)

When the thing being evaluated is a **skill** (not a prompt or task), run gates in this order. Pattern adapted from [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator); in 1ai-skills the tiers map to tools that already exist in `scripts/`.

### Tier 1 — Validation (safety, well-formedness, harness compatibility)

A skill must parse, follow the standard, and not carry unsafe declarations before anything else matters:

```bash
python3 scripts/validate-skill-schema.py     # frontmatter schema conformance
python3 scripts/lint-skills.py               # required sections, description quality
python3 scripts/test-skills.py               # structure + cross-references
```

Gate: **0 errors** required. `--write` (lint) syncs SKILLS.json. Anything failing Tier 1 does not proceed to Tier 2 — measuring a malformed skill wastes eval budget.

### Tier 2 — Deduplication (semantic overlap detection)

Before creating a skill, detect near-duplicates among the existing set; before merging, detect overlap a candidate introduces:

1. Search by intent, not name: `grep -ril "<domain phrase>" */SKILL.md` plus tag intersection against `SKILLS.json`.
2. Compare **triggers** (`When to Use` phrases) — overlap in trigger phrases is stronger evidence of duplication than shared tags.
3. Verdict: **duplicate** (same workflow + same triggers → extend existing instead), **adjacent** (complementary triggers → cross-link via Related Skills), or **distinct**.

Gate: a new skill must name the skills it overlaps with and state why it isn't a duplicate of each.

### Tier 3 — Live Evaluation (agent impact in a sandbox)

Does the skill measurably change agent outcomes? This is an eval-harness run where the treatment is "skill loaded" vs "skill not loaded":

1. Pick N representative tasks with code-based graders (see Grader Type above).
2. Run baseline (agent without skill) and candidate (agent with skill), blind to which is which where possible.
3. Score with `pass@k` (k≥5); compare tiers.

Gate: ship only if candidate ≥ baseline on pass@1 without regressing cons@k. Record the numbers in the skill's PR — a skill that changes nothing measurable is documentation, not capability.

### CI flow

Wire Tier 1 into pre-commit/CI (fast, deterministic); run Tier 2 on skill-additions only; run Tier 3 on demand or weekly (`doctor`-style single entry point recommended: one command that runs Tiers 1–2 locally and reports what's skipped).

## Verification

- [ ] Success criteria defined BEFORE implementation
- [ ] All criteria mechanically checkable or rubric-scored
- [ ] Code-based grader preferred over LLM judge where possible
- [ ] pass@k measured with k >= 5 for stochastic tasks
- [ ] Baseline recorded before candidate runs
- [ ] Regression suite updated with any newly discovered failure mode
- [ ] Eval fixtures committed to repo (`evals/cases/`)
- [ ] Skill quality gates run in order (Tier 1 → 2 → 3) when evaluating a skill
- [ ] Tier 1 gate passed with 0 errors before spending eval budget on Tiers 2–3
- [ ] Tier 2 overlap verdict recorded for any new or merged skill
- [ ] Tier 3 candidate-vs-baseline numbers recorded; no cons@k regression