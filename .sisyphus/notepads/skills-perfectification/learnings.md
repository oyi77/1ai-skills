- Added stdlib-only skill harness scripts with shared `rglob('SKILL.md')` discovery and stable sorted output for deterministic checks.
- Lint output format standardized as `path: RULE_ID: message`, keeping rules grep-friendly and CI-friendly.

- Established canonical gate contract in `agent-docs/plan-artifact-standard.md` with required header fields (`Plan ID`, `Status`, `Momus Verdict`, `Evidence Path`) and strict Momus schema (`verdict`, `reasons`, `required_fixes`).
- Updated workflow skills (`using-superpowers`, `writing-plans`, `executing-plans`, `verification-before-completion`) to require `.sisyphus/plans/` artifacts, Momus `OKAY` precondition, planning-phase exception, and explicit plan-drift reapproval flow.

- Pilot Task 3 for `writing-plans` validated that RED evidence should explicitly capture "just do it" rationalizations; this made gate-failure mapping to canonical standard unambiguous.
- WITH-SKILL evidence that maps each scenario to explicit compliance bullets (path, Momus gate, planning exception, drift protocol) is sufficient to justify no-skill-change decisions.


- Created baseline evidence for using-superpowers skill at /Users/paijo/1ai-skills/.sisyphus/evidence/skills/using-superpowers/baseline.md on 2026-02-15. Content describes discovery/application/pressure scenarios and observations.

- Created RED baseline evidence for all 34 skills (2026-02-15):
  - All skills now have baseline.md with discovery/application/pressure scenarios
  - Evidence directories created under .sisyphus/evidence/skills/
  - Task 4 (RED baseline capture) COMPLETE

- Task 5 (GREEN edits) Progress (2026-02-15):
  - Lint violations reduced from 175 to 140 (35 fixed)
  - 9 skills now have only word count warnings (1 violation each)
  - Added required sections to: agent-docs, brainstorming, business-development, clawild-moltbook, finishing-a-development-branch, marketing, receiving-code-review, systematic-debugging, using-git-worktrees, sales, dispatching-parallel-agents
  - Remaining: Skills need ## Common Mistakes, ## When to Use, ## When NOT to Use, ## Quick Reference sections (~15 skills still need work)
