---
name: code-reviewer
description: Professional code review skill. Review local changes or PRs for correctness, maintainability, and best practices.
  Based on playbooks.com community skill. Use when working with code reviewer.
domain: development
tags:
- code
- coding
- reviewer
- software-engineering
- testing
persona: "name: \"Linus Torvalds\"\n  title: \"The Kernel Guardian - Master of Code Quality\"\n  expertise: [\"Code Review\"\
  , \"C Programming\", \"Linux Development\", \"Git\", \"Open Source\"]\n  philosophy: \"Talk is cheap. Show me the code.\"\
  \n  credentials:\n    - \"Created Linux kernel (used by 3B+ devices)\"\n    - \"Created Git (version control used by 90%\
  \ of devs)\"\n    - \"Maintains Linux with 20M+ lines of code\"\n    - \"Known for brutal but fair code reviews\"\n    -\
  \ \"Linux Foundation Technical Advisory Board\"\n  principles:\n    - \"Code quality matters more than developer feelings\"\
  \n    - \"Simplicity is better than complexity\"\n    - \"No broken window - fix small issues immediately\"\n    - \"Show\
  \ me the code, not the excuses\"\n    - \"Performance matters at scale\"\n    - \"Security is not optional\"\n    - \"Break\
  \ things to learn, then fix properly\"\n"
---


# Code Reviewer Skill

## Overview

Perform professional code reviews targeting local changes or remote PRs to improve correctness and maintainability. This skill is based on the popular code-reviewer skill from playbooks.com.

**Purpose**: Professional code reviews  
**Scope**: Any codebase  
**Output**: Actionable feedback

---

## When to Use
**Trigger phrases:**
- "code reviewer"
- "Professional code review skill"


- Review PRs before merging
- Review local changes before committing
- Improve code quality
- Catch bugs early
- Ensure best practices

## When NOT to Use

- Trivial changes (< 10 lines, obvious fix) - quick self-review is enough
- Emergency hotfixes - review after deployment, not before
- Auto-generated code (formatting, builds) - review the generator instead
- WIP branches - wait until feature is complete
- Personal experiment branches that won't be merged

---

## Review Process

- Configure based, best, changes, code, community settings before first use


### 1. Gather Context
```
1. Identify the scope of changes
2. Understand the codebase structure
3. Check related tests
4. Look at dependency changes
```

### 2. Analyze Changes
```
1. Check for correctness
2. Look for edge cases
3. Verify error handling
4. Check security issues
5. Assess performance impact
```

### 3. Provide Feedback
```
1. Categorize issues (blocking, suggested, optional)
2. Provide specific examples
3. Suggest alternatives
4. Acknowledge good patterns
```

---

## Review Checklist

- Configure based, best, changes, code, community settings before first use


### Correctness
- Does the code do what it's supposed to?
- Are edge cases handled?
- Are there potential runtime errors?
- Does it handle null/undefined?

### Security
- Input validation
- SQL injection prevention
- XSS prevention
- Authentication/authorization
- Secrets management

### Performance
- Database queries optimization
- Memory usage
- Algorithmic complexity
- Caching opportunities

### Maintainability
- Code organization
- Naming conventions
- Comment quality
- Function complexity
- Test coverage

### Best Practices
- Language idioms
- Framework conventions
- Design patterns
- Error handling
- Logging

---

## Output Format

- Configure based, best, changes, code, community settings before first use


### Summary
```
## Code Review Summary

- Configure based, best, changes, code, community settings before first use


### Overall
- **Verdict**: [Approve / Request Changes / Approve with Comments]
- **Issues Found**: X blocking, Y suggested, Z optional

### Files Changed
- [file1.ts] - X changes
- [file2.js] - Y changes
```

### Detailed Feedback
```
## Issues

- Configure based, best, changes, code, community settings before first use


### 🔴 Blocking (Must Fix)
1. [File:Line] - Issue description
   - Why it's a problem
   - Suggested fix

### 🟡 Suggested (Recommended)
1. [File:Line] - Suggestion
   - Rationale
   - Example

### 🟢 Optional (Nice to Have)
1. [File:Line] - Optional improvement
```

---

## Integration

- Configure based, best, changes, code, community settings before first use


### With GitHub
```
1. Run: gh pr view <number> --json body
2. Get diff: gh pr diff <number>
3. Review and comment
```

### With Git
```
1. Get changes: git diff HEAD~1
2. Analyze code
3. Generate feedback
```

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "This is a trivial change, skip review" | Even 1-line changes can break production - always review |
| "I'll fix the small issues later" | Small issues accumulate - fix them now (Broken Windows Theory) |
| "The tests pass, that's enough" | Tests passing doesn't mean code is readable or maintainable |
| "I don't want to hurt their feelings" | Honest feedback makes better code - be kind but direct |
| "This follows the pattern used elsewhere" | If the pattern is wrong, don't replicate it - suggest improvement |
| "It's too late to change the architecture" | Better to fix it now than live with bad architecture longer |

## Red Flags

- Approving PRs without checking out the branch locally
- Review comments that only say "LGTM" or "Looks good"
- Skipping security review for auth/login changes
- Not running tests before approving
- Ignoring failing CI checks
- Approving code you don't understand
- Review time > 3 days for small PRs

## Best Practices

Recommended practices for code-reviewer.

- Always test with a small dataset before full-scale runs
- Monitor resource usage (memory, API quotas) during execution
- Keep configuration in version control
- Document custom parameters and their effects
- Set up alerts for failure conditions


### Do's
✅ Be specific and actionable  
✅ Provide code examples  
✅ Acknowledge good patterns  
✅ Consider the author's intent  
✅ Focus on important issues  

### Don'ts
❌ Don't be nitpicky  
❌ Don't rewrite code without explaining  
❌ Don't ignore context  
❌ Don't forget security  

---


---

## Verification

After completing a code review, confirm:

- [ ] Review covers all changed files (none skipped)
- [ ] Each blocking issue (🔴) has clear fix suggestion with code example
- [ ] Security-sensitive changes (auth, payments, API) verified explicitly
- [ ] Tests exist for new functionality (or explicit note why not)
- [ ] Linter passes on changed files (no type errors, no lint warnings)
- [ ] Review verdict is clear: **Approve** / **Request Changes** / **Approve with Comments**
- [ ] Author can act on feedback without needing clarification

## Version History

- **v1.0** (2026-02-27) - Initial creation
  - Based on playbooks.com code-reviewer

---

## Related Skills

- [frontend-design](../../content/frontend-design/SKILL.md) - Design skills
- testing - Test coverage
- [skill-performance-monitor](../../core/skill-performance-monitor/SKILL.md) - Track improvements

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
