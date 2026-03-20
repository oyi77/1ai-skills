---
name: deep-research-pro
version: 1.1.0
description: "Exhaustive multi-source research agent with academic rigor. Mandated 2-cycle research per theme, APA 7th citations, evidence hierarchy, and 3 user checkpoints. Uses DuckDuckGo search — no API keys required."
homepage: https://github.com/paragshah/deep-research-pro
metadata: {"clawdbot":{"emoji":"🔬","category":"research"}}
---

# Deep Research Pro 🔬

A powerful, self-contained deep research skill that produces thorough, cited reports from multiple web sources. Combines practical multi-source search with academic-grade methodology — evidence hierarchy, APA citations, mandated research cycles, and structured checkpoints.

**No paid APIs required** — uses DuckDuckGo search.

## When to Use This Skill

Use `/research` or trigger this skill when:
- User asks for "deep research" or "exhaustive analysis"
- Complex topics requiring multi-source investigation
- Literature reviews, competitive analysis, or trend reports
- "Tell me everything about X"
- Claims need verification from multiple sources

## Tool Configuration

| Tool | Purpose | Configuration |
|------|---------|---------------|
| `web_search` | Broad context gathering | `count=20` for comprehensive coverage |
| `web_fetch` | Deep extraction from specific sources | Use for detailed page analysis |
| `sessions_spawn` | Parallel research tracks | For investigating multiple themes simultaneously |
| DDG search script | Free web + news search | `--max 8` per query |

## Core Workflow (Three Checkpoints)

### Phase 1: Initial Engagement [CHECKPOINT — WAIT FOR USER]

Before any research begins:

1. **Ask 1-3 clarifying questions:**
   - What is the primary question or problem you're trying to solve?
   - What depth of analysis do you need? (overview vs. exhaustive)
   - Any specific time constraints, geographic focuses, or source preferences?

2. **Reflect understanding back** — summarize what you understand their need to be.

3. **Wait for response before proceeding.**

If the user says "just research it" — skip ahead with reasonable defaults.

---

### Phase 2: Research Planning [CHECKPOINT — WAIT FOR APPROVAL]

Present the complete research plan:

#### 1. Major Themes Identified
List 3-5 major themes for investigation. For each:
- **Theme name**
- **Key questions to investigate**
- **Expected research approach**

#### 2. Research Execution Plan
| Step | Action | Tool | Expected Output |
|------|--------|------|-----------------|
| 1 | [Action] | web_search/ddg | [What you'll capture] |
| 2 | ... | ... | ... |

#### 3. Expected Deliverables
- Report format, citation style, estimated depth

**Wait for explicit user approval before proceeding.**

---

### Phase 3: Mandated Research Cycles [EXECUTE FULLY]

**MINIMUM REQUIREMENTS:**
- Two full research cycles per theme
- Evidence trail for each conclusion
- Multiple sources per claim
- Documentation of contradictions
- Analysis of limitations

#### For Each Theme — Cycle 1: Landscape Analysis

**Step 1: Broad Search**
```bash
# Web search with comprehensive coverage
web_search count=20 "theme keywords"
# Or DDG fallback
/home/clawdbot/clawd/skills/ddg-search/scripts/ddg "<keywords>" --max 8
```

**Step 2: Synthesize**
- Extract key patterns and trends
- Map knowledge structure
- Form initial hypotheses
- Note contradictions

**Step 3: Gap Identification**
- What key concepts were found?
- What knowledge gaps remain?
- What contradictions appeared?

#### For Each Theme — Cycle 2: Deep Investigation

**Step 1: Targeted Deep Search & Fetch**
- `web_search` targeting identified gaps
- `web_fetch` on primary sources for deep extraction
- Use `freshness` parameter for recent developments

**Step 2: Comprehensive Analysis**
- Test hypotheses against new evidence
- Challenge assumptions from Cycle 1
- Find contradictions between sources
- Build connections to previous findings

**Step 3: Knowledge Synthesis**
- New evidence found in Cycle 2
- Connections to Cycle 1 findings
- Remaining uncertainties

#### Required Analysis Between Tool Uses

After EACH tool call, show your work:
1. **Connect** new findings to previous results
2. **Show evolution** of understanding
3. **Highlight** pattern changes
4. **Address** contradictions with sources
5. **Build** coherent narrative

#### Knowledge Integration (Cross-Theme)

After completing all theme cycles:
1. Identify shared conclusions across themes
2. Note when themes reinforce or challenge each other
3. Map relationships between discoveries
4. Form unified understanding

---

## Evidence Hierarchy

1. **Systematic reviews & meta-analyses** — Highest confidence
2. **Randomized controlled trials** — High confidence
3. **Cohort / longitudinal studies** — Medium-high confidence
4. **Expert consensus / guidelines** — Medium confidence
5. **Cross-sectional / observational** — Medium confidence
6. **Expert opinion / editorials** — Lower confidence
7. **Media reports / blogs** — Lowest confidence, verify against primary sources

### Confidence Annotations
- **[HIGH]** — Multiple high-quality sources agree
- **[MEDIUM]** — Limited or mixed evidence
- **[LOW]** — Single source, preliminary, or needs verification
- **[SPECULATIVE]** — Hypothesis or emerging area

---

## Quality Rules

1. **Every claim needs a source.** No unsourced assertions.
2. **Cross-reference.** If only one source says it, flag as unverified.
3. **Recency matters.** Prefer sources from the last 12 months.
4. **Acknowledge gaps.** If you couldn't find good info, say so.
5. **No hallucination.** If you don't know, say "insufficient data found."
6. **All contradictions must be addressed** — document and analyze conflicts.

---

## Citation Standards (APA 7th Edition)

### In-Text Citations
```
Recent research has demonstrated significant effects (Johnson et al., 2023).
Multiple meta-analyses have confirmed this finding (Smith, 2020; Williams & Thompson, 2021).
```

### Reference Format
```
Garcia, J., Martinez, A., & Lee, S. (2022). Title of article. Journal Name,
    15(3), 245-267. https://doi.org/10.xxxx/example
```

**Rules:**
- ~1-2 citations per paragraph
- Use "et al." for 3+ authors in-text
- Full author list in references
- Alphabetize by first author's surname
- If source lacks formal citation data: (Source Name, n.d.) with URL

---

## Writing Style

### Final Report Requirements
- **Flowing narrative style** — prose, not lists
- **Academic but accessible** — rigorous but readable
- **Evidence integrated naturally** into sentences
- **Progressive logical development** — each paragraph builds on previous
- Data and statistics woven into narrative sentences

### Paragraph Structure
- **Topic sentence:** Core claim
- **Evidence:** Supporting sources with citations
- **Analysis:** Interpretation and implications
- **Transition:** Link to next idea

### Prohibited in Final Report
- Bullet points or numbered lists (convert to prose)
- Data tables (describe in prose)
- Isolated data points without narrative context

---

## Final Report Structure [CHECKPOINT THREE — PRESENT TO USER]

```markdown
# Research Report: [Topic]

## Executive Summary
Two to three paragraphs: core question, primary findings, significance.

## Knowledge Development
How understanding evolved through the research process.

## Comprehensive Analysis

### Primary Findings and Implications
### Patterns and Trends Across Research Phases
### Contradictions and Competing Evidence
### Strength of Evidence for Major Conclusions
### Limitations and Gaps

## Practical Implications
### Immediate Applications
### Long-Term Implications
### Risk Factors and Mitigation
### Future Research Directions

## References
[Full APA-formatted reference list]

## Appendices (if needed)
### Search Strategy
### Source Reliability Assessment
```

---

## Error Handling

### Empty or Insufficient Results
1. Broaden query terms, use synonyms
2. Try related concepts
3. Document the gap
4. Mark as [LOW] or [SPECULATIVE]

### Contradictory Sources
1. Present both claims with full context
2. Analyze why they differ
3. Assess evidence quality on each side
4. Document as unresolved if necessary

### Technical Failures
- `web_fetch` fails → document URL, note as inaccessible
- Rate limiting → slow down, retry with backoff

---

## Parallel Research Strategy

For independent themes, use `sessions_spawn`:

```
Theme A:
→ sessions_spawn(
    task="Research [topic]. Complete 2 cycles:
    Cycle 1: web_search count=20 on [aspect]. Analyze, identify gaps.
    Cycle 2: web_fetch top sources, deep dive contradictions.
    Return: Key findings, confidence levels, gaps, source list."
  )
```

**Important:** Sub-agents run in isolation — pass any cross-cutting context in task descriptions.

---

## Save & Deliver

```bash
mkdir -p ~/clawd/research/[slug]
# Write report to ~/clawd/research/[slug]/report.md
```

- **Short topics**: Post full report in chat
- **Long reports**: Post executive summary + key takeaways, offer full report as file

## Requirements

- `web_search` / `web_fetch` (native OpenClaw tools)
- DDG search script (fallback): `/home/clawdbot/clawd/skills/ddg-search/scripts/ddg`
- No API keys needed!
