---
name: email-automation
description: Automate email workflows, templates, and campaigns with Gmail MCP integration
allowed-tools:
  - Bash(gmail:*)
  - MCP(gmail-mcp:*)
  - MCP(nineteen-blocks:*)
---
persona:
  name: "Domain Expert"
  title: "Master of Email Automation"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Email Automation

Automate email workflows, create templates, and manage campaigns using Gmail and MCP integrations.

## Required Tools
| Tool | Purpose | Required |
|------|---------|----------|
| CLI | Primary execution | Yes |
| API client | External service calls | Conditional |
| Validator | Output checking | Recommended |


### MCP Servers

#### Gmail MCP Server

```json
{
  "mcpServers": {
    "gmail-mcp": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}",
        "GOOGLE_REDIRECT_URI": "http://localhost:3000/oauth/callback"
      }
    }
  }
}
```

#### Nineteen Blocks (Sales Automation)

```json
{
  "mcpServers": {
    "nineteen-blocks": {
      "command": "npx",
      "args": ["-y", "@nineteen-blocks/mcp-server"],
      "env": {
        "NINETEEN_BLOCKS_API_KEY": "${NINETEEN_BLOCKS_API_KEY}"
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(gmail:*)` | Execute Gmail CLI commands |
| `MCP(gmail-mcp:*)` | Gmail API: send, read, label, draft |
| `MCP(nineteen-blocks:*)` | Streak CRM, Sheets, Drive integration |

## Authentication
1. Obtain API credentials from the service provider
2. Set environment variables: `export API_KEY=<your-key>`
3. Test authentication: invoke the skill with a read-only operation
4. Store credentials securely; never commit to version control


### Setup Steps

1. **Create Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create new project
   - Enable Gmail API

2. **Get OAuth Credentials**
   - Go to "Credentials" → "Create Credentials" → "OAuth Client ID"
   - Desktop app (not web)
   - Download `credentials.json`

3. **Configure Environment**
   ```bash
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   export NINETEEN_BLOCKS_API_KEY="your-api-key"
   ```

4. **First Run (OAuth)**
   ```bash
   gmail auth
   ```

5. **Verify Connection**
   ```bash
   gmail me
   ```

## Pseudo Code
```python
# Example workflow for this skill
def execute(input_data):
    # Step 1: Validate input
    if not input_data:
        raise ValueError("Input data is required")

    # Step 2: Process core logic
    result = process(input_data)

    # Step 3: Validate output
    validate_output(result)

    return result
```


### Example 1: Send Personalized Email

```typescript
// 1. Load recipient data from sheet
const leads = await sheet.load("Q1_Prospects", "A:D");

// 2. For each lead, send personalized email
for (const lead of leads) {
  const email = {
    to: lead.email,
    subject: `Exclusive Offer for ${lead.company_name}`,
    body: `Hi ${lead.first_name}, ...`
  };
  
  await gmail.send(email);
  
  // Respect rate limits (100 emails/day)
  await delay(60000);
}
```

### Example 2: Auto-Responder for Support

```typescript
// Watch inbox for new emails
gmail.watch({
  labelIds: ["INBOX"],
  callback: async (email) => {
    if (email.subject.toLowerCase().includes("urgent")) {
      await gmail.send({
        to: email.from,
        subject: `Re: ${email.subject}`,
        body: "Thank you for reaching out..."
      });
    }
  }
});
```

### Example 3: Email Campaign with Tracking

```typescript
const recipients = await sheet.load("Campaign_Q1", "A:C");
const results = [];

for (const recipient of recipients) {
  const result = await gmail.send({
    to: recipient.email,
    subject: `Hi ${recipient.name}`,
    body: "..."
  });
  results.push({ email: recipient.email, status: result.success });
  await delay(1000);
}
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `gmail auth` | Start OAuth authentication |
| `gmail send --to user@email.com --subject "Subject" --body "Body"` | Send email |
| `gmail list --label INBOX --max 10` | List recent emails |
| `gmail read <message-id>` | Read specific email |
| `gmail draft --to user@email.com --subject "Subject"` | Create draft |
| `gmail label create "Label Name"` | Create new label |

## Error Handling

| Error Code | Meaning | Recovery |
|------------|---------|----------|
| `AUTH_001` | Invalid credentials | Run `gmail auth` |
| `AUTH_002` | Token expired | Re-authenticate |
| `RATE_001` | Daily limit (100/day) | Wait 24 hours |
| `SEND_001` | Invalid recipient | Check email format |

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Batch Send with Rate Limiting

```typescript
async function sendBatch(emails: Email[], delayMs = 60000) {
  const results = [];
  for (const email of emails) {
    try {
      const result = await gmail.send(email);
      results.push({ ...email, success: true, id: result.messageId });
    } catch (error) {
      results.push({ ...email, success: false, error: error.message });
    }
    await delay(delayMs);
  }
  return results;
}
```

## Best Practices

1. **Rate Limits**: Free Gmail = 100/day
2. **Warm Up**: Start with 10-20 emails/day
3. **Personalization**: Replace {{PLACEHOLDERS}}
4. **Unsubscribe**: Always include link
5. **Compliance**: Follow CAN-SPAM

## Testing

```bash
# Dry run
gmail send --to test@example.com --subject "Test" --body "Test" --dry-run
```


## When NOT to Use

- When the productivity tool handles legally privileged communications
- When the automation affects compliance-archived records or legal holds
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Automation creates duplicate entries across connected platforms
- Agent does not handle timezone differences correctly
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] No duplicate entries are created across connected platforms
- [ ] Timezone handling is correct for all scheduling operations
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `productivity/google-workspace` - Google Drive, Sheets integration
- `sales/sales-strategy` - Sales email sequences

---
*Skill v2.0 - Email Automation with MCP*
