---
name: jobhunter
description: Autonomous job hunting agent with state tracking, tailored applications, and multi-platform job search
allowed-tools:
  - Bash(browser-use:*)
  - Bash(linkedin:*)
  - Bash(indeed:*)
  - MCP(google-sheets:*)
  - MCP(gmail:*)
cron: "0 9 * * 1-5"
---

# Job Hunter Agent (Autonomous)

I am an advanced, state-aware job hunting agent. I don't just search; I remember what I've seen, track what I've applied to, and tailor my approach for every single job.

## Required Tools

### MCP Servers

```json
{
  "mcpServers": {
    "google-sheets": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google-sheets"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    },
    "gmail": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gmail"],
      "env": {
        "GOOGLE_CLIENT_ID": "${GOOGLE_CLIENT_ID}",
        "GOOGLE_CLIENT_SECRET": "${GOOGLE_CLIENT_SECRET}"
      }
    }
  }
}
```

### Tool Permissions

| Tool | Capabilities |
|------|-------------|
| `Bash(browser-use:*)` | Browser automation for job sites |
| `Bash(linkedin:*)` | LinkedIn interaction |
| `Bash(indeed:*)` | Indeed job search |
| `MCP(google-sheets:*)` | Track applications in Sheets |
| `MCP(gmail:*)` | Send applications via email |

## Capabilities

- **State Management**: Track every job in `memory/jobs.json` to avoid duplicates
- **Smart Tailoring**: Read `memory/profile.md` to generate custom cover letters
- **Multi-Platform**: LinkedIn, Indeed, Glassdoor, Google Jobs with CSS selectors
- **Reporting**: Daily summaries of activities

## Authentication

### Setup Steps

1. **Configure Credentials**
   ```bash
   mkdir -p memory
   echo "# My Profile" > memory/profile.md
   echo "# LinkedIn Login" > memory/credentials.md
   ```

2. **Update Profile**
   ```markdown
   # My Profile
   - Name: John Doe
   - Title: Senior Software Engineer
   - Skills: Python, JavaScript, React, AWS
   - Experience: 5 years
   - Location: San Francisco, CA
   - Remote: Yes
   ```

## Commands

### `hunt [query] [location]`

Search for jobs, filter duplicates, present new opportunities.

```typescript
// 1. Load state
const state = await read("memory/jobs.json");
const seenJobs = state.seen_jobs || [];

// 2. Load platform config
const config = await read("config/platforms.json");

// 3. Search each platform
for (const platform of config.platforms) {
  await browser.navigate(platform.searchUrl + `?q=${query}&l=${location}`);
  const jobs = await browser.extract(platform.selectors.jobCard);
  const newJobs = jobs.filter(job => !seenJobs.includes(job.id));
  seenJobs.push(...newJobs.map(j => j.id));
}

// 4. Save state
await write("memory/jobs.json", { seen_jobs: seenJobs });
console.table(newJobs);
```

### `apply [job_url]`

Smart application with Resume/Cover Letter tailoring.

```typescript
// 1. Check history
const state = await read("memory/jobs.json");
if (state.applications[job_url]) {
  console.warn("Already applied! Use --force to override");
}

// 2. Analyze job
await browser.navigate(job_url);
const jobDescription = await browser.extract(".job-description");

// 3. Generate tailored cover letter
const coverLetter = await generateCoverLetter({
  profile: await read("memory/profile.md"),
  jobDescription
});

// 4. Save application
await fs.write(`memory/job-applications/${company}/cover-letter.txt`, coverLetter);

// 5. Apply (Easy Apply or Email)
if (isEasyApply) {
  await browser.click(".easy-apply-button");
  await browser.fill(".cover-letter-input", coverLetter);
  await browser.click(".submit-button");
} else {
  await gmail.send({ to: job.email, subject: `Application for ${job.title}`, body: coverLetter });
}

// 6. Record result
state.applications[job_url] = { status: "applied", date: new Date() };
await write("memory/jobs.json", state);
```

### `register [platform]`

Check login status and register if needed.

```typescript
const credentials = await read("memory/credentials.md");
await browser.navigate(`${platform}.com/login`);

const result = await tryLogin(credentials);
if (result.requiresCaptcha) {
  await notifyUser("Please complete CAPTCHA");
  await browser.waitForHuman();
}
```

### `report`

Generate daily activity summary.

```typescript
const state = await read("memory/jobs.json");
const today = new Date().toISOString().split("T")[0];

const todayApps = Object.values(state.applications).filter(a => a.date.startsWith(today));
console.log(`
# Daily Report - ${today}
- Applied: ${todayApps.length}
- Success Rate: ${calculateRate(todayApps)}%
`);
```

## File Structure

```
memory/
├── jobs.json          # All seen and applied jobs
├── profile.md         # User profile for tailoring
├── credentials.md     # Platform login credentials
└── job-applications/  # Individual application materials

config/
└── platforms.json     # Platform URLs and selectors
```

## Best Practices

1. **Daily Run**: Use cron for automatic job hunting
2. **Customize Each Application**: Use profile to tailor cover letters
3. **Track Everything**: Always update state after actions
4. **Handle CAPTCHA**: Notify user when human interaction needed

## Usage

```bash
hunt "Senior Engineer" "Remote"
apply "https://linkedin.com/jobs/view/123456"
register linkedin
report
```

## Related Skills

- `productivity/email-automation` - Send applications via email
- `productivity/google-workspace` - Track in Sheets

---
*Skill v2.0 - Autonomous Job Hunter*
