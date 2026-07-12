---
name: multi-agent
version: 1.0.0
severity: recommended
scope: [research, brainstorming, planning]
pairs-with: [engineering, surpass]
description: Multi-agent collaboration protocol — Advocate, Skeptic, Synthesizer roles for research and brainstorming
---

# §MULTI-AGENT — Collaborative Research & Brainstorming Protocol

**Why:** A single agent rationalizes blind spots. Multiple agents with distinct roles surface contradictions,
challenge assumptions, and produce higher-quality decisions.

---

### Roles

| Role | Instruction to give the agent | Bias |
|------|-------------------------------|------|
| **Advocate** | "Research [topic]. Make the strongest possible case FOR the leading option. Be specific: cite real examples, links, benchmarks." | Optimistic |
| **Skeptic** | "Review the Advocate's findings. Find every weakness, risk, and assumption. What could go wrong? What did they miss? What would a competitor exploit?" | Pessimistic |
| **Synthesizer** | "Read Advocate + Skeptic outputs. Produce a final decision: what to build, what to drop, and why. Resolve disagreements with evidence, not compromise." | Neutral |

For brainstorming (idea generation before a decision), use two additional roles:

| Role | Instruction | Bias |
|------|-------------|------|
| **Explorer** | "Generate 10+ unconventional approaches to [problem]. Ignore feasibility for now. Think first principles." | Wild |
| **Filter** | "Take the Explorer's list. Apply: effort, risk, user impact, and competitive differentiation. Rank top 3. Kill the rest with a reason." | Pragmatic |

---

### Execution modes

**Harness with `task` tool (preferred):**
```
Spawn agents in parallel:
  task(role="Advocate", assignment="Research [topic]. Write findings to local://research-advocate.md")
  task(role="Skeptic",  assignment="Read local://research-advocate.md. Write critique to local://research-skeptic.md")
  task(role="Synthesizer", assignment="Read local://research-advocate.md and local://research-skeptic.md. Write verdict to local://research-verdict.md")
```

Pass shared context via `local://` files. Each agent reads from the previous agent's output.

**Manual (when task tool unavailable):**
1. Run Advocate (yourself): research the topic, write summary.
2. Switch to Skeptic mindset: read summary, list contradictions + risks.
3. Synthesize: combine both into a final decision with evidence.

---

### When to use

- **ONLY for COMPLEX/strategic decisions** — not for bug fixes, simple features, or routine tasks
- Marked by **[MULTI-AGENT]** flag in task descriptions
- **Single-agent fallback** is always acceptable if time pressure doesn't allow multi-agent — but must state why multi-agent was skipped

---

### Output format

Save multi-agent decisions to `docs/decisions/<decision-name>.md`:
```markdown
# Decision: [Title]
**Date:** YYYY-MM-DD
**Advocate:** [summary]
**Skeptic:** [summary]
**Synthesizer:** [verdict with evidence]
```
