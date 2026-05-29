---
name: calendar-management
description: Advanced calendar management, scheduling, and meeting automation with Google Calendar MCP
allowed-tools:
  - Bash(calendar:*)
  - MCP(google-calendar:*)
  - MCP(tldv:*)
---
persona:
  name: "Domain Expert"
  title: "Master of Calendar Management"
  expertise: ['Specialized Knowledge', 'Best Practices', 'Industry Standards']
  philosophy: "Excellence through expertise."
  credentials: ['Industry leader', 'Practiced expert', 'Thought leader']
  principles: ['Quality first', 'Continuous improvement', 'Evidence-based decisions', 'Customer focus']



# Calendar Management

Advanced calendar management with intelligent scheduling, meeting automation, and cross-platform synchronization.

## World-Class Expert Personas

This skill channels the expertise of:

### **Cal Newport** - Deep Work & Time Management Expert
- **Credentials**: MIT PhD, Georgetown CS professor; bestselling author (Deep Work, A World Without Email, Time-Block Planner)
- **Expertise**: Time blocking, attention management, deep work scheduling, shallow work batching, calendar-based productivity
- **Philosophy**: "Clarity about what matters provides clarity about what does not."
- **Principles**: Time-block every minute, protect deep work blocks, batch shallow work, fixed-schedule productivity, shutdown rituals

### **Tim Ferriss** - 4-Hour Workweek Author & Productivity Hacker
- **Credentials**: 5x NYT bestselling author; angel investor (Uber, Facebook, Shopify); pioneered lifestyle design movement
- **Expertise**: 80/20 analysis, batching, elimination, automation, meeting minimization, calendar audits
- **Philosophy**: "Focus on being productive instead of busy."
- **Principles**: Pareto principle (80/20), batch similar tasks, eliminate before optimizing, automate recurring decisions, protect maker time

### **Laura Vanderkam** - Time Management Researcher
- **Credentials**: Time management expert; author of "168 Hours" and "Off the Clock"; studied 1000+ time diaries
- **Expertise**: Time tracking, calendar audits, energy management, meeting optimization, work-life integration
- **Philosophy**: "Time is highly elastic. We cannot make more time, but time will stretch to accommodate what we choose to put into it."
- **Principles**: Track before optimizing, schedule priorities first, protect peak energy hours, batch meetings, build in buffer time

## Required Tools
| Tool | Purpose | Required |
|------|---------|----------|
| CLI | Primary execution | Yes |
| API client | External service calls | Conditional |
| Validator | Output checking | Recommended |


### MCP Servers

#### Google Calendar MCP

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-calendar"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

#### Tldv MCP (Meeting Notes)

```json
{
  "mcpServers": {
    "tldv": {
      "command": "npx",
      "args": ["-y", "@tldv/mcp-server"],
      "env": {
        "TLDV_API_KEY": "${TLDV_API_KEY}"
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(calendar:*)` | Execute calendar CLI |
| `MCP(google-calendar:*)` | Create, read, update events |
| `MCP(tldv:*)` | Meeting transcription, summaries |

## Authentication
1. Obtain API credentials from the service provider
2. Set environment variables: `export API_KEY=<your-key>`
3. Test authentication: invoke the skill with a read-only operation
4. Store credentials securely; never commit to version control


### Setup Steps

1. **Enable Google Calendar API**
   ```bash
   gcloud services enable calendar.googleapis.com
   ```

2. **Get OAuth Credentials**
   - Google Cloud Console → APIs → Credentials
   - Create OAuth 2.0 Client ID (Desktop app)
   - Download credentials.json

3. **Configure**
   ```bash
   export GOOGLE_CLIENT_ID="your-client-id"
   export GOOGLE_CLIENT_SECRET="your-client-secret"
   export TLDV_API_KEY="your-tldv-key"
   ```

4. **Verify**
   ```bash
   calendar list
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


### Example 1: Schedule Meeting with Availability Check

```typescript
// 1. Get attendees' calendars
const attendees = ["alice@company.com", "bob@company.com"];

// 2. Find available time slots
const freeSlots = await calendar.findFreeBusy({
  timeMin: "2024-03-15T09:00:00",
  timeMax: "2024-03-15T17:00:00",
  items: attendees.map(email => ({ id: email }))
});

// 3. Filter to find 1-hour slots
const suitableTimes = freeSlots
  .filter(slot => slot.start - slot.end >= 3600000)
  .filter(slot => !slot.busy);

// 4. Create event at best time
const event = await calendar.createEvent({
  summary: "Team Sync",
  description: "Weekly team synchronization",
  start: { dateTime: suitableTimes[0].start },
  end: { dateTime: addHours(suitableTimes[0].start, 1) },
  attendees: attendees.map(email => ({ email })),
  conferenceData: {
    createRequest: { requestId: "team-sync" }
  }
});
```

### Example 2: Cross-Timezone Scheduling

```typescript
// 1. Define timezones
const locations = [
  { name: "San Francisco", timezone: "America/Los_Angeles" },
  { name: "London", timezone: "Europe/London" },
  { name: "Tokyo", timezone: "Asia/Tokyo" }
];

// 2. Find overlapping business hours (9am-6pm)
const businessHours = { start: 9, end: 18 };

// 3. Try each hour and convert
for (let hour = 0; hour < 24; hour++) {
  const times = locations.map(loc => {
    const time = getTimeInZone(hour, loc.timezone);
    return { location: loc.name, hour: time.hour };
  });
  
  // Check if all in business hours
  if (times.every(t => t.hour >= 9 && t.hour < 18)) {
    console.log(`Found: ${hour} UTC works for all`);
    break;
  }
}

// 4. Create meeting
await calendar.createEvent({
  summary: "Global Team Meeting",
  start: { dateTime: `${date}T${hour}:00:00Z`, timeZone: "UTC" },
  end: { dateTime: `${date}T${hour + 1}:00:00Z`, timeZone: "UTC" }
});
```

### Example 3: Recurring Meeting Setup

```typescript
// 1. Create recurring event
const event = await calendar.createEvent({
  summary: "Weekly 1:1",
  description: "Weekly sync with manager",
  start: { 
    dateTime: "2024-03-15T10:00:00", 
    timeZone: "America/New_York" 
  },
  end: { 
    dateTime: "2024-03-15T10:30:00", 
    timeZone: "America/New_York" 
  },
  recurrence: [
    "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=12"
  ],
  reminders: {
    useDefault: false,
    overrides: [
      { method: "email", minutes: 1440 },  // 1 day
      { method: "popup", minutes: 15 }     // 15 min
    ]
  }
});
```

### Example 4: Meeting Analytics

```typescript
// 1. Get all events for last month
const events = await calendar.listEvents({
  timeMin: "2024-02-01T00:00:00Z",
  timeMax: "2024-02-29T23:59:59Z",
  singleEvents: true,
  orderBy: "startTime"
});

// 2. Analyze
const stats = {
  totalMeetings: 0,
  totalHours: 0,
  byType: {},
  byAttendee: {}
};

for (const event of events) {
  if (event.summary?.includes("[1:1]")) {
    stats.byType["1:1"] = (stats.byType["1:1"] || 0) + 1;
  }
  
  const hours = (event.end - event.start) / 3600000;
  stats.totalMeetings++;
  stats.totalHours += hours;
  
  for (const attendee of event.attendees || []) {
    stats.byAttendee[attendee.email] = 
      (stats.byAttendee[attendee.email] || 0) + 1;
  }
}

console.log(`Total: ${stats.totalMeetings} meetings, ${stats.totalHours} hours`);
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `calendar list` | List upcoming events |
| `calendar create --title "Meeting" --time "2024-03-15T10:00"` | Create event |
| `calendar find --emails a@b.com,c@d.com --duration 60` | Find free time |
| `calendar delete <event-id>` | Delete event |
| `calendar update <event-id> --title "New Title"` | Update event |

## Error Handling

| Error | Meaning | Fix |
|-------|---------|-----|
| `AUTH_001` | Not authenticated | Run `calendar auth` |
| `CONFLICT_001` | Time slot taken | Pick different time |
| `PERM_001` | No access to calendar | Request access |

## Common Patterns
- Use structured input/output schemas for reliable automation
- Add retry logic with exponential backoff for external calls
- Validate inputs before processing to fail fast
- Log execution steps for debugging and auditing


### Find Next Available Slot

```typescript
async function findNextSlot(duration: number, preferred: string[]) {
  const now = new Date();
  const endOfDay = new Date(now);
  endOfDay.setHours(18, 0, 0, 0);
  
  let checkTime = new Date(now);
  while (checkTime < endOfDay) {
    const free = await calendar.freeBusy({
      timeMin: checkTime.toISOString(),
      timeMax: addMinutes(checkTime, duration).toISOString()
    });
    
    if (free.length === 0) {
      return checkTime;
    }
    
    checkTime = addMinutes(checkTime, 30);
  }
}
```

### Batch Send Invites

```typescript
async function sendInvites(emails: string[], event: Event) {
  const results = [];
  for (const email of emails) {
    await calendar.invite(event.id, email);
    results.push({ email, status: "invited" });
  }
  return results;
}
```

## Best Practices

1. **Time Zones**: Always specify explicitly
2. **Buffer Time**: Add 5-15 min between meetings
3. **Reminders**: Set both email and popup
4. **Recurrence**: Use RRULE for recurring meetings


## When NOT to Use

- When calendar automation involves executive scheduling requiring human discretion
- When the calendar data contains meeting details subject to NDA
- When the task is too trivial to warrant this skill
- When a more appropriate skill exists

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Calendar automation double-books time slots
- Agent does not account for time zones when scheduling across regions
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] No double-bookings exist in the scheduled time slots
- [ ] Time zones are correctly handled for cross-region scheduling
- [ ] All required outputs generated
- [ ] Success criteria met

## Related Skills

- `productivity/google-workspace` - Calendar integration
- `productivity/email-automation` - Meeting invites

---
*Skill v2.0 - Calendar Management with MCP*
