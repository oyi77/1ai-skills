---
name: calendar-management
description: Advanced calendar management, scheduling, and meeting automation with Google Calendar MCP
allowed-tools:
  - Bash(calendar:*)
  - MCP(google-calendar:*)
  - MCP(tldv:*)
---

# Calendar Management

Advanced calendar management with intelligent scheduling, meeting automation, and cross-platform synchronization.

## Required Tools

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

## Related Skills

- `productivity/google-workspace` - Calendar integration
- `productivity/email-automation` - Meeting invites

---
*Skill v2.0 - Calendar Management with MCP*
