# Session Observability / Tracing
> Version: 1.0.0 | Status: Active | Applies to: All agents

## Purpose
Every session produces a trace log capturing key decisions, tool calls, costs, and outcomes. This enables:
- Debugging failed sessions
- Auditing agent decisions
- Measuring framework effectiveness
- Cost attribution per task

## Trace Log Format

Each session creates a trace file at `~/.1ai/traces/{session-id}.jsonl`:

```json
{"t": "2026-07-13T12:00:00Z", "event": "session_start", "agent": "task", "task": "Implement auth", "model": "sonnet-4.6"}
{"t": "2026-07-13T12:00:05Z", "event": "tool_call", "tool": "edit", "file": "src/auth.ts", "lines": "12-15", "status": "ok"}
{"t": "2026-07-13T12:00:10Z", "event": "decision", "action": "gate_check", "gate": "0", "result": "pass"}
{"t": "2026-07-13T12:01:00Z", "event": "cost", "tokens_in": 500, "tokens_out": 120, "cost_usd": 0.015}
{"t": "2026-07-13T12:05:00Z", "event": "session_end", "duration_s": 300, "tools_called": 12, "files_changed": 3, "total_cost_usd": 0.042}
```

## Event Types

| Event | When | Fields |
|-------|------|--------|
| `session_start` | Session begins | agent, task, model, session_id |
| `session_end` | Session ends | duration_s, tools_called, files_changed, total_cost_usd |
| `tool_call` | Each tool invocation | tool, file (if applicable), status (ok/error) |
| `decision` | Gate check or choice | action, gate (if gate), result (pass/fail/block) |
| `cost` | Periodic cost snapshot | tokens_in, tokens_out, cost_usd |
| `milestone` | Major phase boundary | phase, item, status |

## Session ID

Format: `YYYYMMDD-HHMMSS-{agent}-{random4}`

Generated at session start. Written to `~/.1ai/current-session.txt` for cross-tool reference.

## Trace Directory

`~/.1ai/traces/`
- One `.jsonl` file per session
- Rotated: keep last 30 days, auto-archive older
- Each file name: `{session-id}.jsonl`

## Integration

### BOOTSTRAP.md
When a TASK session starts, the SessionStart hook SHOULD:
1. Generate session ID
2. Write `session_start` event to new trace file
3. Write session ID to `~/.1ai/current-session.txt`
4. On session end, write `session_end` event

### Tool hooks
Post-tool hooks SHOULD:
1. Read session ID from `~/.1ai/current-session.txt`
2. Append `tool_call` event to trace file

### Cost tracking
Cost tracking (`COST_TRACKING.md`) writes `cost` events to the same trace file for unified audit trail.

## Diagnostic Commands

```bash
# View current session trace
cat ~/.1ai/traces/$(cat ~/.1ai/current-session.txt 2>/dev/null).jsonl 2>/dev/null

# List recent sessions
ls -lt ~/.1ai/traces/ | head -10

# Count tool calls in last session
grep -c '"event":"tool_call"' ~/.1ai/traces/latest.jsonl

# Find sessions where a specific file was edited
grep -rl '"file":"src/auth.ts"' ~/.1ai/traces/
```

## Acceptance Criteria
- SessionStart hook writes `session_start` event
- Tool calls are recorded to trace file
- Session end is recorded on completion
- `grep` commands above produce meaningful output
