---
name: ai-engineering-curriculum
description: Structured AI engineering curriculum — 382 skills + 99 prompts across 20 phases covering ML, deep learning, LLMs, agents, and production systems. Use when learning AI, building AI skills,.
domain: core
tags: 
- [ai
- curriculum
- machine-learning
- deep-learning
- llm
- agents
- education]
---

## When NOT to Use

- Task is outside your authorization scope
- You need to implement controls (use implementing-* skills)
- Task is about analysis, not action (use analyzing-* skills)
- You don't have access to target systems
- Task requires compliance expertise (consult professionals)
- Task is about defense, not offense (use defensive skills)


## Overview

AI Engineering from Scratch: a complete 473-lesson curriculum spanning 20 phases from math foundations to autonomous agent systems. Covers Python, TypeScript, Rust, and Julia. Built for agents and humans who need a structured path through modern AI engineering.

Source: [rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)

Install: `npx skills add rohitg00/ai-engineering-from-scratch`

## Capabilities

- Navigate a structured 20-phase AI engineering curriculum
- Identify skill gaps by mapping current knowledge to phases
- Recommend targeted lessons based on learner level
- Run placement quizzes to find starting phase
- Run per-phase comprehension checks

## When to Use

- User wants to learn AI engineering from scratch
- Need to assess someone's AI skill level
- Looking for structured learning path in ML/DL/LLMs/Agents
- Building AI training programs or onboarding materials
- Searching for specific AI topic coverage

## Phase Map

| Phase | Topic | Focus |
|-------|-------|-------|
| 0 | Setup | Environment, tools, Python/TS/Rust/Julia config |
| 1 | Math | Linear algebra, calculus, probability, statistics |
| 2 | ML Fundamentals | Supervised/unsupervised, evaluation, pipelines |
| 3 | Deep Learning | Neural networks, backprop, CNNs, RNNs |
| 4 | Computer Vision | Image classification, detection, segmentation |
| 5 | NLP | Text processing, embeddings, sequence models |
| 6 | Speech/Audio | ASR, TTS, audio processing |
| 7 | Transformers | Attention, encoder-decoder, positional encoding |
| 8 | Generative AI | GANs, VAEs, diffusion models |
| 9 | Reinforcement Learning | Policy gradient, Q-learning, PPO |
| 10 | LLMs from Scratch | Tokenization, training, scaling laws |
| 11 | LLM Engineering | Fine-tuning, RAG, prompt engineering, evals |
| 12 | Multimodal AI | Vision-language models, cross-modal reasoning |
| 13 | Tools/Protocols | MCP, function calling, tool use patterns |
| 14 | Agent Engineering | ReAct, planning, memory, tool orchestration |
| 15 | Autonomous Systems | Self-improving agents, reflection, verification |
| 16 | Multi-Agent/Swarms | Agent coordination, delegation, consensus |
| 17 | Infrastructure/Production | Serving, monitoring, scaling, cost optimization |
| 18 | Ethics/Safety/Alignment | RLHF, red teaming, guardrails, interpretability |
| 19 | Capstone | End-to-end project combining all phases |

## Built-in Agents
- Primary agent handles core task execution
- Validator agent checks output quality
- Reporter agent formats and delivers results
- Each agent operates with clear input/output contracts


### /find-your-level
Placement quiz that assesses current knowledge across phases and recommends a starting point.

### /check-understanding
Per-phase quiz that tests comprehension after completing each phase.

## Usage

```
User: "Where should I start learning AI?"
Agent: Runs /find-your-level placement quiz, maps results to phase map, recommends starting phase

User: "I know Python and basic ML, what next?"
Agent: Maps to Phase 3-4, recommends deep learning and computer vision modules

User: "Quiz me on transformers"
Agent: Runs /check-understanding for Phase 7
```

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

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |