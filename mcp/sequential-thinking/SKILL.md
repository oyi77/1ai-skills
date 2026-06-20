---
name: sequential-thinking
description: Dynamic problem-solving through thought sequences — iterative reasoning, hypothesis testing, and solution refinement
domain: mcp
tags:
- mcp-server
- model-context-protocol
- sequential
- testing
- thinking
- tool-integration
---

## Overview

Sequential thinking is a structured reasoning approach where problems are solved through a chain of thoughts, each building on the previous. Supports backtracking, hypothesis testing, and solution refinement.

## Capabilities

- Break complex problems into sequential thought steps
- Generate and test hypotheses iteratively
- Backtrack and revise when initial approaches fail
- Estimate solution complexity and adjust strategy
- Maintain reasoning context across thought chains

## When to Use

- Complex problems that need multi-step reasoning
- Debugging where the root cause isn't obvious
- Architecture decisions with multiple trade-offs
- Planning tasks with many interdependencies

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


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


### Thought Chain
```python
def sequential_think(problem, max_thoughts=10):
    thoughts = []
    current_thought = generate_initial_thought(problem)
    
    for i in range(max_thoughts):
        thoughts.append(current_thought)
        
        # Evaluate progress
        if is_solution_complete(current_thought, problem):
            return thoughts
        
        # Generate next thought based on all previous
        current_thought = generate_next_thought(problem, thoughts)
        
        # Backtrack if stuck
        if is_stuck(thoughts):
            thoughts = backtrack(thoughts, steps=2)
            current_thought = generate_alternative(problem, thoughts)
    
    return thoughts
```

### Hypothesis Testing
```python
def test_hypothesis(hypothesis, evidence):
    supports = [e for e in evidence if supports(hypothesis, e)]
    contradicts = [e for e in evidence if contradicts(hypothesis, e)]
    
    confidence = len(supports) / (len(supports) + len(contradicts) + 1)
    
    return {
        "hypothesis": hypothesis,
        "confidence": confidence,
        "supports": supports,
        "contradicts": contradicts,
        "verdict": "accept" if confidence > 0.7 else "reject" if confidence < 0.3 else "uncertain"
    }
```

## Common Patterns

- **Number your thoughts**: Explicit numbering helps track reasoning progress
- **State assumptions**: List assumptions at each step for validation
- **Backtrack explicitly**: When a path fails, state why and explore alternatives
- **Complexity estimation**: Estimate difficulty before diving in — adjust strategy if needed

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
