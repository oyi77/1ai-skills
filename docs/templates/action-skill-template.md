---
name: {{SKILL_NAME}}
description: {{ONE_LINE_DESCRIPTION}}
allowed-tools:
  - Bash({{TOOL_NAME}}:*)
  - MCP({{MCP_SERVER_NAME}}:*)
---

# {{SKILL_NAME}}

{{EXTENDED_DESCRIPTION}}

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "{{MCP_SERVER_NAME}}": {
      "command": "npx",
      "args": ["-y", "{{NPM_PACKAGE}}"],
      "env": {
        {{ENV_VARS}}
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash({{TOOL_NAME}}:*)` | Execute {{TOOL_NAME}} commands |
| `MCP({{MCP_SERVER_NAME}}:*)` | Access {{MCP_SERVER_NAME}} functions |

## Authentication

### Setup Steps

1. **Get Credentials**
   ```
   {{AUTH_STEPS}}
   ```

2. **Configure Environment**
   ```bash
   export {{VAR_NAME}}="{{VALUE}}"
   ```

3. **Verify Connection**
   ```bash
   {{VERIFY_COMMAND}}
   ```

## Pseudo Code

### Example 1: {{EXAMPLE_1_NAME}}

```typescript
// 1. Initialize connection
const client = await connect({{CREDENTIALS}});

// 2. Perform action
const result = await client.{{ACTION_1}}({
  {{PARAMS_1}}
});

// 3. Handle response
if (result.success) {
  console.log(result.data);
} else {
  console.error(result.error);
}

// 4. Cleanup
await client.disconnect();
```

### Example 2: {{EXAMPLE_2_NAME}}

```typescript
// 1. Authenticate
const auth = await login({
  email: "{{EMAIL}}",
  password: "{{PASSWORD}}"
});

// 2. Create resource
const item = await create("{{RESOURCE_TYPE}}", {
  name: "{{NAME}}",
  data: {{DATA}}
});

// 3. Update state
await update(item.id, {
  status: "{{STATUS}}"
});
```

### Example 3: {{EXAMPLE_3_NAME}}

```typescript
// 1. List resources
const items = await list("{{RESOURCE_TYPE}}", {
  filter: "{{FILTER}}",
  limit: {{LIMIT}}
});

// 2. Process each
for (const item of items) {
  await process(item);
}

// 3. Report results
console.log(`Processed ${items.length} items`);
```

## Error Handling

| Error Code | Meaning | Recovery |
|------------|---------|----------|
| `AUTH_001` | Invalid credentials | Re-authenticate |
| `AUTH_002` | Token expired | Refresh token |
| `API_001` | Rate limited | Wait and retry |
| `API_002` | Not found | Check resource ID |
| `API_003` | Permission denied | Check permissions |

## Common Patterns

### Pattern 1: Batch Processing

```typescript
async function processBatch(items: Item[]): Promise<Results> {
  const results = [];
  
  for (const item of items) {
    try {
      const result = await process(item);
      results.push({ item, success: true, data: result });
    } catch (error) {
      results.push({ item, success: false, error: error.message });
    }
    
    // Respect rate limits
    await delay({{DELAY_MS}});
  }
  
  return results;
}
```

### Pattern 2: Retry Logic

```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await delay({{RETRY_DELAY_MS}});
    }
  }
}
```

## Testing

### Unit Test

```typescript
describe("{{SKILL_NAME}}", () => {
  it("should {{EXPECTED_BEHAVIOR}}", async () => {
    const result = await action({{PARAMS}});
    expect(result.success).toBe(true);
  });
});
```

### Integration Test

```typescript
it("should complete full workflow", async () => {
  // Setup
  await setup({{TEST_DATA}});
  
  // Execute
  const result = await workflow();
  
  // Verify
  expect(result.status).toBe("complete");
  
  // Cleanup
  await cleanup();
});
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `{{CLI_CMD_1}}` | {{CLI_DESC_1}} |
| `{{CLI_CMD_2}}` | {{CLI_DESC_2}} |
| `{{CLI_CMD_3}}` | {{CLI_DESC_3}} |

## Related Skills

- `{{RELATED_SKILL_1}}` - {{RELATED_DESC_1}}
- `{{RELATED_SKILL_2}}` - {{RELATED_DESC_2}}

---
*Template v1.0 - Action Skill Template*
