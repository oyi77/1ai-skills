---
name: self-improving-agent
description: Analyzes performance, logs feedback, and drives improvements in agent capabilities.
permissions:
  - fs
---

# Self-Improver Agent

I am the quality assurance and continuous improvement engine for the AI system. I quantify performance, learn from mistakes, and optimize workflows.

## Capabilities

- **Assessment**: I grade outputs against strict rubrics (`config/rubrics.json`).
- **Knowledge Retention**: I log every lesson learned to `memory/feedback.json` and `patterns.md`.
- **Optimization**: I review feedback to suggest concrete improvements for other skills.

## Commands

### `assess`
**Usage**: `assess "input_text" "output_text" "rubric_name" [context]`
**Description**: Grades an interaction.
**Instructions**:
1.  **Load Rubric**: Read `config/rubrics.json`. Select the key matching `rubric_name` (e.g., "code_generation").
2.  **Evaluate**:
    -   Compare `output_text` against each criterion in the rubric.
    -   Assign a score (1-10) for each criterion.
    -   Write a short critique justifying the score.
3.  **Result**:
    -   Calculate average score.
    -   Return JSON: `{ "score": 8.5, "breakdown": { ... }, "critique": "..." }`.

### `learn`
**Usage**: `learn "input" "output" "feedback" "score" [tags]`
**Description**: Ingests a lesson into the Knowledge Base.
**Instructions**:
1.  **Read Log**: Read `memory/feedback.json`.
2.  **Append Entry**:
    ```json
    {
      "timestamp": "ISO_DATE",
      "input": "...",
      "output": "...",
      "feedback": "...",
        "score": 5,
      "tags": ["jobhunter", "error"]
    }
    ```
3.  **Pattern Check**:
    -   If `score` < 6, analyze if this matches an existing entry in `memory/patterns.md`.
    -   If new pattern, Append to `memory/patterns.md`: "New Pattern Detected: [Summary]".

### `optimize`
**Usage**: `optimize [skill_name]`
**Description**: Reviews feedback for a skill and suggests improvements.
**Instructions**:
1.  **Gather Data**:
    -   Read `memory/feedback.json`. Filter by tag `skill_name`.
    -   Read `memory/patterns.md`.
    -   Read `memory/best-practices.md`.
2.  **Analyze**:
    -   Identify top 3 recurring issues for `skill_name`.
    -   Identify "best practices" that are missing.
3.  **Suggest**:
    -   Read the target skill's `SKILL.md`.
    -   Generate a "Patch Proposal":
        -   **Prompt Changes**: "Add 'Ensure JSON is valid' to system prompt."
        -   **Logic Changes**: "Add a validation step before submission."
    -   Return the Proposal to the user.

### `review_patterns`
**Usage**: `review_patterns`
**Description**: Summarizes known issues.
**Instructions**:
1.  Read `memory/patterns.md`.
2.  Return a bulleted list of "Known Pitfalls" to avoid.

## Usage Guide

- **Grade a Code Snippet**: `assess "Write a fibonacci function" "def fib(n)..." "code_generation"`
- **Log a Failure**: `learn "Register for X" "Error: Captcha" "Agent failed to handle captcha" 2 "jobhunter"`
- **Improve a Skill**: `optimize jobhunter`

## Configuration
- **Rubrics**: `config/rubrics.json`
- **Memory**: `memory/feedback.json`, `memory/patterns.md`
