---
name: prompt-engineering
description: Advanced prompt engineering — chain-of-thought, few-shot, tree-of-thought,
  self-consistency, meta-prompting, system design, debugging, and optimization for
  production AI systems.
domain: core
---

# Prompt Engineering

Expert-level prompt design, optimization, and debugging for AI agents and LLM systems. Covers the full lifecycle: writing, testing, debugging, and scaling prompts.

## When to Use

- LLM outputs are inconsistent or low quality
- Complex reasoning tasks that need step-by-step thinking
- Building reusable prompt templates for production systems
- Optimizing prompts for cost (fewer tokens) or accuracy
- Creating system prompts and custom instructions for AI agents
- Debugging prompt performance issues
- Designing multi-turn conversation flows

## Core Techniques

| Technique | Best For | Example |
|-----------|----------|--------|
| Chain-of-thought | Multi-step reasoning | "Let's think step by step" |
| Few-shot examples | Format consistency | 3-5 input/output pairs |
| XML tags | Structured sections | `<context>...</context>` |
| Role prompting | Domain expertise | "You are a senior SRE" |
| Negative constraints | Preventing errors | "Do NOT include" |
| Tree-of-thought | Complex exploration | Generate multiple reasoning paths, pick best |
| Self-consistency | Reliable outputs | Generate N answers, take majority vote |
| Meta-prompting | Prompt optimization | "Critique this prompt and suggest improvements" |

## Chain-of-Thought

```python
def chain_of_thought(question):
    return f"""Think step by step.

Question: {question}

Let me break this down:
1. First, identify the key components...
2. Then, analyze each component...
3. Finally, synthesize the answer...

Answer:"""
```

## Few-Shot Template

```python
def few_shot_prompt(task, examples, input_text):
    header = f"Task: {task}\n\n"
    shots = "\n\n".join([
        f"Input: {ex['input']}\nOutput: {ex['output']}"
        for ex in examples
    ])
    return f"{header}{shots}\n\nInput: {input_text}\nOutput:"
```

## Self-Consistency

```python
def self_consistent_answer(question, n=5):
    answers = [generate(question, temperature=0.7) for _ in range(n)]
    return most_common(answers)
```

## System Prompt Design

Structure system prompts in this order:
1. **Role**: Who the AI is
2. **Context**: What situation it's in
3. **Constraints**: What it must NOT do
4. **Output format**: Exact format expected
5. **Examples**: Few-shot if needed

### XML Tag Patterns

```xml
<system>
You are a senior security engineer. Be concise and evidence-based.
</system>

<context>
{{user_context}}
</context>

<instructions>
Analyze the code for vulnerabilities. List findings with severity.
</instructions>

<output format>
For each finding:
- File:Line
- Severity: Critical/High/Medium/Low
- Description: One sentence
- Fix: Concrete code change
</output>

<constraints>
- Only report real vulnerabilities, not style issues
- Include file path and line number for every finding
- Maximum 5 findings per scan
</constraints>
```

## Prompt Debugging Checklist

When a prompt isn't working:

1. Is the task clearly stated in the first sentence?
2. Are output format requirements explicit?
3. Are edge cases covered with examples?
4. Is the token budget sufficient for the response?
5. Are negative constraints preventing known failure modes?
6. Is the role/context appropriate for the task?
7. Are examples representative of actual inputs?
8. Is the temperature set correctly (0 factual, 0.7 creative, 1.0 diverse)?

## Common Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Vague instructions | Model guesses wrong | Be specific about format, length, tone |
| Missing negative examples | Model does unwanted things | Show what NOT to do |
| Too many constraints | Model ignores some | Prioritize top 3-5 constraints |
| No output format | Inconsistent results | Specify exact format with example |
| Role too generic | Generic output | Give specific expertise level and context |

## Prompt Optimization Process

1. **Baseline**: Test current prompt, measure quality
2. **Diagnose**: Identify failure modes (wrong format, wrong content, hallucination)
3. **Iterate**: Change one variable at a time
4. **A/B Test**: Compare variants on same inputs
5. **Document**: Record what works and why

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems

## Verification

After completing this skill, confirm:

- [ ] Prompt produces consistent, correct output across 5+ test cases
- [ ] Output format matches specification exactly
- [ ] Token usage is optimized (no unnecessary context)
- [ ] Edge cases are handled (empty input, max length, special characters)
- [ ] Prompt is documented with examples and failure modes
