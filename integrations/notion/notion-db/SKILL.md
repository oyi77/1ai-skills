---
name: notion-db
description: Manage Notion databases
domain: integrations
---
## Notion Db

Manage Notion databases

### Usage

```
/notion-db <task>
```

### Features

- Automated execution
- Error handling
- Result validation

## How to Use

1. Identify the target database by its ID (from the Notion URL)
2. Query with filters, sorts, and page size parameters
3. Map database properties to your data model
4. Create and update pages programmatically

## Database Query Patterns

```python
query = {
    "filter": {
        "and": [
            {"property": "Status", "select": {"equals": "Active"}},
            {"property": "Priority", "number": {"greater_than": 3}}
        ]
    },
    "sorts": [{"property": "Created", "direction": "descending"}],
    "page_size": 100
}

all_results = []
while True:
    resp = requests.post(url, headers=headers, json=query)
    data = resp.json()
    all_results.extend(data["results"])
    if not data["has_more"]:
        break
    query["start_cursor"] = data["next_cursor"]
```

## Common Patterns

- Use rollups for computed values across relations
- Create database templates for consistent page structure
- Use status properties with predefined options for kanban views

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

