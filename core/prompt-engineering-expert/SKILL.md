---
name: prompt-engineering-expert
description: Advanced expert in prompt engineering, custom instructions design, and
  prompt optimization for AI agents
domain: core
---

# Prompt Engineering Expert Skill

This skill equips Claude with deep expertise in prompt engineering, custom instructions design, and prompt optimization. It provides comprehensive guidance on crafting effective AI prompts, designing agent instructions, and iteratively improving prompt performance.

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Capabilities

- **Prompt Writing Best Practices**: Expert guidance on clear, direct prompts with proper structure and formatting
- **Custom Instructions Design**: Creating effective system prompts and custom instructions for AI agents
- **Prompt Optimization**: Analyzing, refining, and improving existing prompts for better performance
- **Advanced Techniques**: Chain-of-thought prompting, few-shot examples, XML tags, role-based prompting
- **Evaluation & Testing**: Developing test cases and success criteria for prompt evaluation
- **Anti-patterns Recognition**: Identifying and correcting common prompt engineering mistakes
- **Context Management**: Optimizing token usage and context window management
- **Multimodal Prompting**: Guidance on vision, embeddings, and file-based prompts

## Use Cases

- Refining vague or ineffective prompts
- Creating specialized system prompts for specific domains
- Designing custom instructions for AI agents and skills
- Optimizing prompts for consistency and reliability
- Teaching prompt engineering best practices
- Debugging prompt performance issues
- Creating prompt templates for reusable workflows

## When to Use

- When the task falls within this skill's domain expertise
- When automated execution saves time over manual work
- When the skill's tools and integrations are available

## How to Use

1. Invoke the skill when relevant domain keywords appear in the request
2. Provide required inputs as specified in the skill definition
3. Review the output for correctness before delivering to the user
4. Combine with related skills for complex multi-step workflows

## How to Use

1. Describe the prompt engineering task clearly (system prompt, few-shot, chain-of-thought)
2. Provide the current prompt or target application context
3. Specify the LLM model and constraints (token limits, output format)
4. Review the optimized prompt and iterate based on test results

## Core Techniques

| Technique | Best For | Example |
|-----------|----------|--------|
| Chain-of-thought | Multi-step reasoning | "Let's think step by step" |
| Few-shot examples | Format consistency | 3-5 input/output pairs |
| XML tags | Structured sections | `<context>...</context>` |
| Role prompting | Domain expertise | "You are a senior SRE" |
| Negative constraints | Preventing errors | "Do NOT include" |

## Prompt Debugging Checklist

- Is the task clearly stated in the first sentence?
- Are output format requirements explicit?
- Are edge cases covered with examples?
- Is the token budget sufficient for the response?
- Are negative constraints preventing known failure modes?

## Verification

After completing this skill, confirm:

- [ ] Output meets the defined quality and completeness requirements
- [ ] All prerequisites are verified and documented
- [ ] Error handling covers edge cases
- [ ] Results are accurate and actionable
