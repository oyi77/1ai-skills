# Cost Observability / Tracking
> Version: 1.0.0 | Status: Active

## Purpose
Track model API costs per session, per agent, and per task. Enable cost-aware decision-making.

## Cost Log Format

Cost events use the session trace format (see SESSION_TRACING.md) with the `cost` event type:

```json
{"t":"2026-07-13T12:00:00Z","event":"cost","agent":"task","model":"sonnet-4.6","tokens_in":500,"tokens_out":120,"cost_usd":0.015,"task":"auth"}
```

The session trace file (`~/.1ai/traces/{session-id}.jsonl`) unifies cost events with other trace events.

## Cost Categories

| Category | Example | Typical cost/1K tokens |
|----------|---------|----------------------|
| Reasoning (sonnet/opus) | Code generation, analysis | $0.015/$0.060 in, $0.075/$0.240 out |
| Fast (haiku) | Simple lookups, formatting | $0.003 in, $0.015 out |
| Embedding | Vector generation | $0.0001/1K tokens |
| Image generation | UI mockups, assets | $0.04-0.12 per image |
| External API | Search, browser | Variable |

## Daily Log

Each cost event is also aggregated into `~/.1ai/costs/{YYYY-MM-DD}.csv`:

```
t,agent,model,tokens_in,tokens_out,cost_usd,task
2026-07-13T12:00:00Z,task,sonnet-4.6,500,120,0.015,auth
```

## Tracking Script

### `bin/cost-track.sh`

Handles cost log operations:

```bash
# Log a cost event
cost-track.sh log --agent task --model sonnet-4.6 --tokens-in 500 --tokens-out 120 --cost 0.015 --task auth

# Show daily summary
cost-track.sh today

# Show weekly summary  
cost-track.sh week

# Show monthly summary
cost-track.sh month

# Show per-agent breakdown
cost-track.sh by-agent

# Export to CSV
cost-track.sh export
```

## Cost Alerts

If cost exceeds threshold in a single session, the script prints a warning:

```
COST ALERT: Session cost $0.50 exceeded threshold ($0.10)
```

Thresholds:
- Per-call alert: $0.10
- Per-session alert: $0.50
- Daily limit: $10.00 (stops on exceed)
- Monthly budget: $300.00 (prints warning at 80% = $240)

## Integration with SESSION_TRACING

Both protocols write to the same trace file (`~/.1ai/traces/{session-id}.jsonl`):
- `session_start`, `session_end`, `tool_call`, `decision` → SESSION_TRACING
- `cost` → COST_TRACKING

This enables queries like:
```bash
# Total cost of last session
grep '"event":"cost"' "$(ls -t ~/.1ai/traces/*.jsonl | head -1)" | grep -o '"cost_usd":[0-9.]+' | cut -d: -f2 | paste -sd+ | bc

# Cost by agent across all sessions
grep -rh '"event":"cost"' ~/.1ai/traces/ | grep -o '"agent":"[^"]*","cost_usd":[0-9.]+' | ...
```

## Acceptance Criteria
- `cost-track.sh` logs cost events
- `cost-track.sh today` shows numeric summary (≥ $0)
- Cost events appear in session trace file
- Alert fires when threshold exceeded
