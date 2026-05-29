---
name: prompt-engineering
description: Advanced prompt patterns — chain-of-thought, few-shot, tree-of-thought, self-consistency, and meta-prompting
---

## Overview

Prompt engineering is the foundational skill for all AI work. This covers advanced patterns: chain-of-thought reasoning, few-shot examples, tree-of-thought exploration, self-consistency voting, and meta-prompting for prompt optimization.

## Capabilities

- Design prompts with chain-of-thought and reasoning scaffolds
- Build few-shot example sets for consistent output quality
- Implement tree-of-thought for complex problem exploration
- Use self-consistency for reliable outputs across multiple runs
- Create meta-prompts that optimize other prompts automatically

## When to Use

- LLM outputs are inconsistent or low quality
- Complex reasoning tasks that need step-by-step thinking
- Building reusable prompt templates for production systems
- Optimizing prompts for cost (fewer tokens) or accuracy

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Chain-of-Thought
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

### Few-Shot Template
```python
def few_shot_prompt(task, examples, input_text):
    header = f"Task: {task}\n\n"
    shots = "\n\n".join([
        f"Input: {ex['input']}\nOutput: {ex['output']}"
        for ex in examples
    ])
    return f"{header}{shots}\n\nInput: {input_text}\nOutput:"
```

### Self-Consistency
```python
def self_consistent_answer(question, n=5):
    answers = [generate(question, temperature=0.7) for _ in range(n)]
    return most_common(answers)
```

## Common Patterns

- **System prompt first**: Set role, constraints, and output format in system message
- **XML tags for structure**: Use `<context>`, `<instructions>`, `<output>` tags for clarity
- **Negative examples**: Show what NOT to do, not just what to do
- **Temperature tuning**: 0 for factual, 0.7 for creative, 1.0 for diverse

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
