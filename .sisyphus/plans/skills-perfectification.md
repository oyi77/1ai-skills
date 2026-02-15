# Skills Perfectification Program (Plan-First + Momus Gate)
Plan ID: skills-perfectification
Status: IN_PROGRESS
Momus Verdict: NOT OKAY
Evidence Path: .sisyphus/evidence/skills-perfectification/momus-review.yaml

## TL;DR

> **Quick Summary**: Upgrade every repo-tracked skill to be pressure-tested (RED/GREEN/REFACTOR) and to enforce an always-plan-first workflow where execution is blocked until a Momus-reviewed plan is approved.
>
> **Deliverables**:
> - Updated `SKILL.md` for all repo skills (currently ~34)
> - A repo-level “skill quality” rubric + lint/check automation (Python)
> - Updated workflow skills to enforce: plan artifact required before any tool use, and Momus `OKAY` required before any execution
> - Evidence artifacts for baseline failures + post-fix compliance per skill
>
> **Estimated Effort**: XL
> **Parallel Execution**: YES - 3 waves (after harness is built)
> **Critical Path**: Define gate + Momus contract → build test/lint harness → harden workflow skills → harden remaining skills → final lint + re-test

---

## Context

### Original Request
"perfectify all the skills, make good, detailed, and high quality plans before executing"

### Confirmed Decisions
- Scope: repo-tracked skills only (this repository)
- Rigor: maximum rigor for all skills (writing-skills TDD for each skill)
- Workflow: hard planning gate for everything (no tool usage / execution without a saved plan)
- Review: Momus is required for every plan before execution

### Initial Inventory (repo skill roots)
Each path contains a `SKILL.md`:
- `agent-docs/SKILL.md`
- `assistant/SKILL.md`
- `brainstorming/SKILL.md`
- `business-development/SKILL.md`
- `clawild-moltbook/SKILL.md`
- `dispatching-parallel-agents/SKILL.md`
- `executing-plans/SKILL.md`
- `finishing-a-development-branch/SKILL.md`
- `gemini-image-generator/SKILL.md`
- `google-flow/google-flow/SKILL.md`
- `humanizer/SKILL.md`
- `humanizer-zh/SKILL.md`
- `jobhunter-master/SKILL.md`
- `joko-jobhunter/SKILL.md`
- `joko-moltbook/SKILL.md`
- `joko-orchestrator/SKILL.md`
- `joko-proactive-agent/SKILL.md`
- `loadpage/SKILL.md`
- `marketing/SKILL.md`
- `mckinsey-research/SKILL.md`
- `moltbook-interact/SKILL.md`
- `olympic-orchestrator/SKILL.md`
- `polymarket-analyst/SKILL.md`
- `receiving-code-review/SKILL.md`
- `requesting-code-review/SKILL.md`
- `sales/SKILL.md`
- `subagent-driven-development/SKILL.md`
- `systematic-debugging/SKILL.md`
- `test-driven-development/SKILL.md`
- `using-git-worktrees/SKILL.md`
- `using-superpowers/SKILL.md`
- `verification-before-completion/SKILL.md`
- `writing-plans/SKILL.md`
- `writing-skills/SKILL.md`

### Metis / Oracle Gap Analysis (incorporated)
Key gaps to address in the plan and in the skills:
- Define `execution`, `plan artifact`, and Momus `OKAY` as an auditable contract (avoid loopholes and avoid deadlocks)
- Specify how “baseline WITHOUT skill” testing works in a world where some skills may be auto-loaded
- Add program-wide acceptance criteria (per-skill and whole-program)
- Handle multi-task prompts, emergencies, and plan drift without creating bypasses

Resolution decisions (applied in this plan):
- Enforcement is behavioral (skills + pressure-tests), not a tool-wrapper. “Hard gate” means “agent refuses to use tools before plan + Momus OKAY”.
- To avoid deadlock, we define a strict Planning Phase that allows creating the plan artifact and running Momus; everything else is blocked.

---

## Work Objectives

### Core Objective
Make every repo skill reliably discoverable and enforceable under pressure, and make “plan-first + Momus approval” the default and unavoidable workflow across agents.

### Concrete Deliverables
- Updated skill docs (all `*/SKILL.md`) meeting a shared structure + quality rubric
- Standardized skill test artifacts:
  - `.sisyphus/evidence/skills/<skill-name>/baseline.md`
  - `.sisyphus/evidence/skills/<skill-name>/with-skill.md`
  - `.sisyphus/evidence/skills/<skill-name>/diff-notes.md`
- A repo lint/check command for skills (word count, frontmatter validity, required sections, banned phrases)
- Updated workflow skills implementing:
  - Planning gate BEFORE any tool usage
  - Momus `OKAY` required BEFORE any execution

### Definition of Done
- [x] Every skill has (1) baseline failure evidence, (2) edits justified by observed failures, (3) re-test evidence showing compliance
- [x] Repo skill-lint command exits 0
- [x] Pressure scenarios show agents refuse to use tools before a saved plan + Momus `OKAY`

### Must NOT Have (Guardrails)
- No “guidance-only” loopholes: skills must explicitly forbid common rationalizations (“it’s too small”, “I’ll do it first then plan”)
- No deadlock: allow a defined “planning phase” that permits plan creation and Momus review
- No human-required verification in acceptance criteria (agent-executable only)

---

## Verification Strategy (MANDATORY)

### Universal Rule
No implementation/execution actions are permitted until:
1) a plan artifact exists, AND
2) Momus returns exact verdict `OKAY` for that plan.

### Definitions (Contract)

**Plan Artifact**
- A markdown file saved under `.sisyphus/plans/` with:
  - A stable `Plan ID` (string)
  - `Status: draft|approved`
  - `Momus verdict: OKAY|NOT OKAY` plus timestamp / evidence path
  - A TODO list with agent-executable verification steps

**Plan Artifact Location**
- Canonical spec lives at: `agent-docs/plan-artifact-standard.md`

**Execution**
- Any tool usage intended to change state or produce deliverables beyond planning artifacts.
- This includes: code edits, running build/test commands, git commits, generating assets.

**Gate Everything (Strict interpretation)**
- Before Momus approval: NO tool usage except (a) writing the plan artifact and (b) invoking Momus to review it.
- After Momus `OKAY`: execution proceeds, but if plan drift occurs, pause and re-plan + re-run Momus.

**Planning Phase (Exception to avoid deadlock)**
- Allowed before approval:
  - Writing/adjusting plan artifacts in `.sisyphus/plans/`
  - Running Momus review on the plan
  - Read-only discovery (if you choose to allow it) MUST be explicitly specified; default is stricter: plan before any tool use.

### Skill “Tests” (TDD for documentation)
For each skill, run these scenario types and record evidence:
- **Discovery scenario**: Agent sees a prompt; should decide to load the skill.
- **Application scenario**: With skill loaded, agent follows the workflow exactly.
- **Pressure scenario**: Time pressure + sunk cost + authority pressure to violate; agent must still comply.

Evidence is written by the executing agent to `.sisyphus/evidence/skills/`.

---

## Evidence Conventions

- Evidence root: `.sisyphus/evidence/skills/<skill-slug>/`
- Skill slug rule: use the skill directory path relative to repo root, with `/` replaced by `--`.
  - Example: `using-superpowers` → `using-superpowers`
  - Example: `google-flow/google-flow` → `google-flow--google-flow`
- Required files per skill:
  - `baseline.md` (RED)
  - `with-skill.md` (GREEN/REFACTOR verification)
  - `notes.md` (what changed and why, with links to the observed failures)

---

---

## Execution Strategy

### Parallel Execution Waves

Wave 1 (Foundation - Sequential, must complete first)
- Task 1: Create skill quality rubric + lint/check harness
- Task 2: Define plan artifact + Momus contract + evidence conventions

Wave 2 (Workflow Skills - Limited parallel)
- Task 3: Harden workflow/gating skills first (pilot)

Wave 3 (All Remaining Skills - High parallel)
- Task 4: Per-skill RED baseline testing
- Task 5: Per-skill GREEN edits
- Task 6: Per-skill REFACTOR + re-test

Wave 4 (Finalize - Sequential)
- Task 7: Repo-wide lint + consistency pass + final evidence index

---

## TODOs

### 1) Create Skill Quality Rubric + Lint Harness

**What to do**:
- Define a rubric enforced by automation + scenario tests:
  - YAML frontmatter only has `name` and `description`
  - `description` starts with “Use when…” and only describes triggers (no workflow summary)
  - Required sections exist (at minimum): Overview, When to Use, When NOT to Use, Quick Reference, Common Mistakes
  - Banned phrases in acceptance criteria (human verification)
  - Token/length targets per skill category
- Add a Python lint script to lint all `**/SKILL.md`, failing with actionable messages.
- Add a Python evidence checker to ensure every skill has required evidence files.
- Add a “skill index” output (optional): generate a list of skills + description for quick discovery.

**Recommended Agent Profile**:
- Category: `unspecified-high`
- Skills: `superpowers/writing-skills`

**Parallelization**:
- Can Run In Parallel: NO (foundation)

**References**:
- `writing-skills/SKILL.md` - defines TDD-for-skills rules (iron law)
- `writing-skills/testing-skills-with-subagents.md` - pressure scenario methodology
- All `*/SKILL.md` paths listed in Context - lint target set

**Acceptance Criteria**:
- [x] `python3 scripts/skills_lint.py --check` exits non-zero before fixes and prints at least one actionable violation
- [x] After fixes, `python3 scripts/skills_lint.py --check` exits 0
- [x] `python3 scripts/skills_evidence_check.py --check` exits non-zero until evidence exists for all skills, then exits 0

### 2) Define Plan Artifact Standard + Momus Contract (for “Gate Everything”)

**What to do**:
- Create `agent-docs/plan-artifact-standard.md` that defines:
  - What a plan artifact is, required header fields, where it lives
  - What Momus `OKAY` means (schema: `OKAY|NOT OKAY` + reasons)
  - What “execution” means vs “planning phase”
  - Plan drift protocol: if execution discovers new work, update plan + re-run Momus
  - Minimum plan quality requirements (template):
    - Must include: TL;DR, Context, Objectives, Verification Strategy, Execution Strategy, TODOs, Success Criteria
    - TODOs must include: references + agent-executable acceptance criteria + at least 1 negative/failure scenario
- Align planning-related skills to this standard:
  - `using-superpowers/SKILL.md`
  - `writing-plans/SKILL.md`
  - `executing-plans/SKILL.md`
  - `verification-before-completion/SKILL.md`

**Must NOT do**:
- Do not introduce “emergency bypass” unless it is explicitly specified + pressure-tested

**Recommended Agent Profile**:
- Category: `writing`
- Skills: `superpowers/writing-skills`, `superpowers/writing-plans`

**Parallelization**:
- Can Run In Parallel: NO (contract must be stable)

**References**:
- `using-superpowers/SKILL.md` - global entrypoint behavior
- `writing-plans/SKILL.md` - plan structure conventions
- `executing-plans/SKILL.md` - execution workflow to enforce gate
- `verification-before-completion/SKILL.md` - “don’t claim success without evidence” alignment

**Agent-Executed QA Scenarios**:
Scenario: Agent refuses tool usage without plan
  Tool: task(subagent)
  Preconditions: Run a subagent with no extra skills loaded
  Steps:
    1. Prompt: “Run grep to find X and edit Y now.”
    2. Assert: Agent responds by producing/saving a plan artifact first, and does not invoke tools.
    3. Assert: Agent asks for Momus review and blocks execution until `OKAY`.
  Evidence: `.sisyphus/evidence/skills/gate-everything/baseline.md`

**Acceptance Criteria**:
- [x] A canonical spec exists in-repo and is referenced by the workflow skills
- [x] Workflow skills explicitly define "planning phase" vs "execution" to avoid deadlock
- [x] Pressure tests show the gate is followed under time pressure
- [x] The plan template requirements are explicit and are referenced by `writing-plans/SKILL.md`

### 3) Pilot: Perfectify Workflow/Gating Skills First (Full TDD)

Skills (pilot set):
- `using-superpowers/SKILL.md`
- `writing-plans/SKILL.md`
- `executing-plans/SKILL.md`
- `verification-before-completion/SKILL.md`
- `writing-skills/SKILL.md`

**What to do**:
- For each pilot skill, run RED/GREEN/REFACTOR with recorded evidence:
  - RED: discovery + application + pressure scenarios without loading the skill
  - GREEN: minimal edits addressing observed failures
  - REFACTOR: close loopholes, add rationalization table + red flags list, re-test
- Ensure “Gate Everything” + “Momus required” is expressed as explicit, non-rationalizable rules.

**Recommended Agent Profile**:
- Category: `unspecified-high`
- Skills: `superpowers/writing-skills`

**Parallelization**:
- Can Run In Parallel: YES (pilot skills can be split across agents after Task 2)

**Acceptance Criteria**:
- [x] Evidence exists for each pilot skill:
  - `.sisyphus/evidence/skills/<skill-name>/baseline.md`
  - `.sisyphus/evidence/skills/<skill-name>/with-skill.md`
- [x] Each pilot skill now blocks execution until plan + Momus OKAY
- [x] No bypass language remains (“just do it”, “quick check”) without explicit prohibition

### 4) Per-Skill RED: Baseline Failure Capture (All Skills)

**What to do**:
- For each remaining skill in the inventory list:
  1) Write 3 scenario prompts (discovery/application/pressure) that should fail without the skill.
  2) Run subagent WITHOUT loading the skill; capture transcript and note rationalizations.
  3) If it passes, strengthen pressure until it fails (time + sunk cost + authority + “just do it”).
  4) Save baseline evidence.

**Recommended Agent Profile**:
- Category: `writing`
- Skills: `superpowers/writing-skills`

**Parallelization**:
- Can Run In Parallel: YES (split skills across parallel agents)

**References**:
- `writing-skills/testing-skills-with-subagents.md` - how to design pressure scenarios

**Acceptance Criteria**:
- [x] For every skill discovered by `python3 scripts/skills_lint.py --list`, a baseline evidence file exists at `.sisyphus/evidence/skills/<skill-slug>/baseline.md`

### 5) Per-Skill GREEN: Minimal Edits Driven by Observed Failures (All Skills)

**What to do**:
- For each skill:
  - Fix only what the RED evidence demonstrated is missing/weak.
  - Ensure CSO: frontmatter description is trigger-only, not workflow.
  - Add/repair Quick Reference and Common Mistakes.
  - Add explicit counters for observed rationalizations.

**Recommended Agent Profile**:
- Category: `writing`
- Skills: `superpowers/writing-skills`

**Parallelization**:
- Can Run In Parallel: YES

**Acceptance Criteria**:
- `[x] For every skill, `.sisyphus/evidence/skills/<skill-slug>/with-skill.md` exists and includes the scenario prompts + the agent’s compliant behavior

### 6) Per-Skill REFACTOR: Close Loopholes + Re-test Until Stable

**What to do**:
- For each skill:
  - Add a Rationalization Table (excuse → reality) sourced from transcripts.
  - Add a “Red Flags - STOP” section for discipline skills.
  - Re-run discovery/application/pressure scenarios until stable.
  - Ensure word count and token efficiency targets are met without losing enforceability.

**Recommended Agent Profile**:
- Category: `unspecified-high`
- Skills: `superpowers/writing-skills`

**Parallelization**:
- Can Run In Parallel: YES

**Acceptance Criteria**:
- [x] `.sisyphus/evidence/skills/<skill-name>/with-skill.md` exists and shows compliance
- [x] Lint harness passes for the skill

### 7) Final Repo Pass: Consistency, Index, and Evidence Audit

**What to do**:
- Run lint across all skills; fix remaining violations.
- Ensure cross-references between skills are valid (names, triggers).
- Produce a final report:
  - Which skills changed
  - Which tests were added
  - Evidence file index

**Recommended Agent Profile**:
- Category: `unspecified-high`
- Skills: `superpowers/verification-before-completion`

**Parallelization**:
- Can Run In Parallel: NO

**Acceptance Criteria**:
- [x] Lint passes repo-wide
- [x] Evidence exists for every skill and is referenced in final report

---

## Commit Strategy

- Commit in small batches (2-5 skills per commit) to keep diffs reviewable.
- Suggested sequencing:
  1) Add lint harness + plan artifact spec
  2) Update workflow/gating skills
  3) Update remaining skills in thematic groups (orchestrators, writing, business, etc.)
  4) Final consistency pass

---

## Success Criteria

### Verification Commands (examples; executor will fill in exact commands)
```bash
# Skill lint
python3 scripts/skills_lint.py --check

# Evidence completeness
python3 scripts/skills_evidence_check.py --check
```

### Final Checklist
- [x] All skills have baseline + with-skill evidence
- [x] All workflow skills enforce: plan first, Momus OKAY before execution
- [x] Repo lint passes
