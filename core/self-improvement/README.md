# Self-Improvement

Captures learnings, errors, and corrections to enable continuous improvement for AI agents.

## What It Does

This skill provides a systematic way to log learnings, errors, and feature requests that can be processed later by coding agents. Key capabilities:
- Log corrections when users provide feedback
- Track errors and failures with context
- Capture feature requests from user needs
- Promote recurring learnings to project memory (AGENTS.md, TOOLS.md, etc.)
- Convert valuable learnings into reusable skills
- Multi-agent inter-session memory sharing

## Quick Usage Example

```bash
# User corrects you: "No, that's wrong. You should use pnpm, not npm."

# Log to LEARNINGS.md with correction category
cat >> .learnings/LEARNINGS.md << 'EOF'
## [LRN-20250310-001] correction

**Logged**: 2025-03-10T10:00:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
Project uses pnpm, not npm for package management

### Details
Attempted `npm install` but it failed. User corrected that this project requires `pnpm install` because the lock file is `pnpm-lock.yaml`.

### Suggested Action
Always use `pnpm install` for this project, never `npm install`

### Metadata
- Source: user_feedback
- Related Files: package.json, pnpm-lock.yaml
- Tags: package-manager, pnpm, npm

EOF

# Promote to project memory if broadly applicable
# Add to CLAUDE.md or .github/copilot-instructions.md
```

## Key Features

- ✅ Structured logging format for learnings, errors, feature requests
- ✅ Automatic ID generation (TYPE-YYYYMMDD-XXX)
- ✅ Priority levels and area tags for filtering
- ✅ Link related entries with "See Also" for recurrence detection
- ✅ Promote learnings to project memory files
- ✅ Extract skills from verified learnings
- ✅ Multi-agent support (Claude Code, Codex, OpenClaw, Copilot)
- ✅ Optional hooks for automatic reminders
- ✅ Review workflows for periodic cleanup

## Requirements

- `.learnings/` directory in project root
- Three log files: LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md
- Optional: Agent-specific configuration (Claude, Codex, etc.)

## When to Use

Use this skill when:
1. User corrects you ("No, that's wrong...")
2. Command or operation fails unexpectedly
3. User requests a capability that doesn't exist
4. External API or tool fails
5. You realize knowledge is outdated or incorrect
6. You discover a better approach for a recurring task
7. Before starting major tasks (review existing learnings)