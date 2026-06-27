# Security Checklist for Skills

Use when reviewing skills that handle sensitive operations.

## Credential Handling

- [ ] No hardcoded API keys, tokens, or passwords
- [ ] Credentials stored in environment variables or secret manager
- [ ] Instructions reference env vars, not literal values
- [ ] No credentials in example code or logs

## Command Execution

- [ ] Shell commands are specific, not user-provided
- [ ] No `eval()` or dynamic code execution
- [ ] No file writes outside declared scope
- [ ] No network requests to non-standard endpoints

## Input Validation

- [ ] External inputs validated before processing
- [ ] SQL queries use parameterized statements
- [ ] File paths sanitized (no path traversal)
- [ ] User input escaped for shell context

## Data Handling

- [ ] No PII in logs or outputs
- [ ] Sensitive data redacted in examples
- [ ] Data retention policy mentioned where applicable
- [ ] No exfiltration vectors (unintended network calls)

## Hook Security

- [ ] Hooks don't modify tool inputs without validation
- [ ] Hooks don't execute arbitrary commands
- [ ] Hooks have timeout limits
- [ ] Hooks fail silently (don't break sessions)
