---
name: notion-api
description: Full Notion API integration
---
## Notion Api

Full Notion API integration

### Usage

```
/notion-api <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Create an integration at notion.so/my-integrations
2. Share target databases/pages with the integration
3. Use the Notion API to read, create, and update content
4. Handle pagination for large result sets

## API Operations

```python
import requests

NOTION_TOKEN = "secret_..."
headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28"
}

# Query a database
resp = requests.post(
    "https://api.notion.com/v1/databases/{db_id}/query",
    headers=headers,
    json={"filter": {"property": "Status", "select": {"equals": "Active"}}}
)

# Create a page
resp = requests.post(
    "https://api.notion.com/v1/pages",
    headers=headers,
    json={
        "parent": {"database_id": db_id},
        "properties": {"Name": {"title": [{"text": {"content": "New Entry"}}]}}
    }
)
```

## Common Patterns

- Use database properties for structured data (not freeform text)
- Handle rate limits (3 requests per second)
- Use rollup and relation properties for cross-database linking

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

