# self-improving-agent Skill

## What It Does

Continuous AI learning from feedback - receives feedback, analyzes root cause, generates improvements, and commits learnings to knowledge base.

## When to Use

- Improve output quality after receiving feedback
- Learn from mistakes and avoid repetition
- Optimize prompts and workflows
- Build institutional knowledge
- Self-grade before completing tasks

## Self-Improving Loop

```
1. RECEIVE output + feedback
2. GRADE against rubric (self-assessment)
3. ANALYZE errors (root cause)
4. GENERATE corrections (new approach)
5. UPDATE parameters (prompts, workflows)
6. TEST with improved approach
7. COMMIT to knowledge base
```

## How It Works

### Step 1: Capture Feedback

- Store: original output, feedback, context
- Format: structured record in feedback.log

### Step 2: Self-Grade

- Compare: output against quality rubric
- Score: each criterion (1-10)
- Identify: specific failures

### Step 3: Analyze Root Cause

- Categorize: failure type (prompt, workflow, context, knowledge)
- Trace: where in pipeline it failed
- Determine: fix type (quick fix vs systemic)

### Step 4: Generate Corrections

- Prompt refinement: better instructions, more context
- Workflow adjustment: different approach, additional steps
- Context enrichment: include relevant background

### Step 5: Update Parameters

- Modify skill prompts
- Adjust quality thresholds
- Update workflow steps
- Add to knowledge base

### Step 6: Test

- Generate new output
- Compare to previous
- Verify improvement
- If not improved, iterate again (max 3 times)

### Step 7: Commit

- Document: what changed and why
- Version: knowledge base
- Share: with related skills

## Quality Rubric Template

| Criterion | Weight | 1 (Poor) | 5 (OK) | 10 (Excellent) |
|-----------|--------|----------|--------|-----------------|
| Relevance | 30% | Off-topic | Partial | Perfect match |
| Accuracy | 30% | Wrong | Partial | Completely correct |
| Completeness | 20% | Missing parts | Mostly complete | Fully complete |
| Format | 20% | Wrong format | Acceptable | Perfect format |

## Usage Examples

### Improve Content After Feedback
```
User: "The LinkedIn post you wrote was too formal. Make it more conversational."
Skill: Receives feedback → self-grades → identifies tone issue → rewrites → tests → commits
```

### Optimize Research Output
```
User: "Your competitor analysis missed key pricing information."
Skill: Analyzes gap → adds pricing extraction → re-runs research → validates → updates
```

### Refine Support Responses
```
User: "The support response didn't address the customer's emotional concern."
Skill: Reviews feedback → adds empathy check → regenerates → commits improvement
```

## Skills It Coordinates

- `systematic-debugging` - Root cause analysis
- `writing-skills` - Prompt refinement
- `verification-before-completion` - Quality checks

## Files Created

- `feedback.log` - All feedback received
- `improvements/` - Generated improvements
- `knowledge-base/` - Learned patterns and solutions
- `version-history/` - Change logs

## Self-Grade Checklist

Before completing any task, run through:

- [ ] Does output meet original requirements?
- [ ] Is quality rubric satisfied (≥7/10)?
- [ ] Are there obvious improvements?
- [ ] Would I be satisfied as the customer?
- [ ] Is this my best work?

If any check fails → trigger self-improvement loop.
