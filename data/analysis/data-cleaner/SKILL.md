---
name: data-cleaner
description: Data Cleaner skill for automated data workflows. Provides tools and templates for clean, cleaner, data operations, integration with AI pipelines, and performance optimization.
---


## Data Cleaner

Clean messy datasets

### Usage

```
/data-cleaner <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## When NOT to Use

- When the data contains regulated PII that must be handled under specific retention policies
- When the cleaning process would destroy audit trails required for compliance
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Data cleaning silently drops records without logging what was removed
- Agent does not validate data types after cleaning
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Removed records are logged with reason for removal
- [ ] Data types are validated after all cleaning operations
- [ ] All required outputs generated
- [ ] Success criteria met
## Notes

- This skill integrates with the broader 1ai-skills ecosystem for data workflows
- Combine with related skills for maximum impact across your pipeline
- Monitor output quality and iterate on configuration based on results
- Keep dependencies up to date for security and performance
- Document custom workflows and configurations for team knowledge sharing
## Additional Resources

- Review the 1ai-skills repository for related data skills
- Check the references/ directory for checklists and templates
- Join the community for best practices and support
- Contribute improvements via pull requests
## Notes

- This skill integrates with the broader 1ai-skills ecosystem for data workflows
- Combine with related skills for maximum impact across your pipeline
- Monitor output quality and iterate on configuration based on results
- Keep dependencies up to date for security and performance
- Document custom workflows and configurations for team knowledge sharing
