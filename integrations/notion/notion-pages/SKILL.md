---
name: notion-pages
description: Notion Pages. Use when working with notion pages in integrations domain.
domain: integrations
tags:
- api
- integrations
- notion
- pages
- third-party
---
## When to Use

**Trigger phrases:**
- "notion pages"
- "Help me with notion pages"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

## Notion Pages

Create and edit Notion pages

### Usage

```
/notion-pages <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Retrieve page content as blocks (paragraphs, headings, lists, tables)
2. Append new blocks to pages for structured content
3. Update existing blocks in place
4. Handle rich text formatting with Notion annotation system

## Block Operations

```python
blocks = requests.get(
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    headers=headers
).json()["results"]

requests.patch(
    f"https://api.notion.com/v1/blocks/{page_id}/children",
    headers=headers,
    json={"children": [
        {"object": "block", "type": "heading_2",
         "heading_2": {"rich_text": [{"text": {"content": "Section Title"}}]}},
        {"object": "block", "type": "paragraph",
         "paragraph": {"rich_text": [{"text": {"content": "Body text here."}}]}}
    ]}
)
```

## Common Patterns

- Use heading blocks for document structure
- Bookmark blocks for external links with previews
- Callout blocks for warnings and important notes
- Synced blocks for reusable content across pages

## When NOT to Use

- When the integration requires admin-level permissions on the target platform
- When the data exchange involves regulated information requiring encryption
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Integration does not handle API errors or service unavailability
- Agent does not verify data consistency across connected systems
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] API errors and service outages are handled with appropriate retry logic
- [ ] Data consistency is verified across all connected systems
- [ ] All required outputs generated
- [ ] Success criteria met

## Overview

> Section content — see SKILL.md body for full details.

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
