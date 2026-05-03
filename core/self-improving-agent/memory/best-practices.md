# Best Practices

## Prompt Engineering
- Use "Chain of Thought" for complex logic.
- Explicitly state output format (JSON/Markdown).
- Provide 1-2 examples (Few-Shot) for new tasks.

## Error Handling
- Always catch network errors and retry with backoff.
- Validate JSON output before parsing.
