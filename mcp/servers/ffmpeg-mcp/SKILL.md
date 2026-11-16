---
name: ffmpeg-mcp
description: Use when exposing FFmpeg/FFprobe operations as MCP tools so a coding agent can inspect, cut, join, transcode, extract audio, thumbnail, and normalize media without ad hoc shell commands. Local only — no API keys, no cloud.
domain: mcp
author: oyi77
license: Apache-2.0
subdomain: mcp
tags:
- mcp
- mcp-server
- model-context-protocol
- ffmpeg
- ffprobe
- video
- audio
- media-processing
- tool-integration
version: 1.0.0
category: mcp
risk_level: low
human_approval: false
tool_requirements:
- tool: ffmpeg
  purpose: Encode/transcode/cut/concat media
  required: true
- tool: ffprobe
  purpose: Read media metadata
  required: true
---

# FFmpeg MCP Server

The first **runnable** MCP server in this repo — every other `mcp/servers/*` entry is docs-only. This one ships working Python (`server.py`) that registers 12 FFmpeg tools via `FastMCP`, validated end-to-end against real media.

## When to Use

**Trigger phrases:**
- "process video with an agent" · "expose ffmpeg as a tool"
- "cut / join / transcode media from MCP" · "ffprobe metadata via MCP"
- "normalize loudness" · "make a gif" · "extract frames / audio"

**Use cases:**
- Give an agent a safe, typed surface over FFmpeg instead of raw shell strings
- Batch media prep (thumbnails, proxies, frame extraction) inside a tool loop
- Loudness normalization before publishing

## When NOT to Use

- Real-time streaming or live capture (this renders to files)
- Heavy GPU encoding pipelines better served by dedicated render farms
- Operations needing frame-level scripting — use `content/video/remotion` instead

## Overview

Wraps FFmpeg/FFprobe behind a machine-readable tool contract. No network, no credentials. Each tool builds an argv list and runs it in the foreground with a hard timeout; on failure it raises `FFmpegError` carrying stderr so the agent sees why.

### The 12 tools

| Group | Tool | What it does |
|---|---|---|
| analysis | `probe` | Media metadata (codec, w/h, fps, duration, streams) as JSON |
| editing | `cut` | Segment [start, end/duration]; stream-copy or frame-accurate reencode |
| editing | `concat` | Join ≥2 same-codec files via concat demuxer |
| picture | `transcode` | Re-encode with codec/CRF/preset + optional scale |
| picture | `compress` | Smaller file; quality low/medium/high → CRF 28/23/18 |
| picture | `thumbnail` | Single still at a timestamp |
| picture | `extract_frames` | PNGs at N fps into a directory |
| picture | `make_gif` | Palette-optimized GIF from a short segment |
| audio | `extract_audio` | Pull audio stream to m4a/mp3/flac |
| audio | `normalize_audio` | loudnorm to target integrated LUFS |
| delivery | `add_subtitles` | Burn SRT/ASS/VTT onto video |
| delivery | `strip_metadata` | Drop metadata + chapters before publishing |

## Setup

```bash
pip install mcp            # FastMCP lives in mcp.server.fastmcp
ffmpeg -version && ffprobe -version   # must be on PATH
python3 server.py          # stdio transport, ready for any MCP client
```

Register in a client config (Claude Code example):

```json
{
  "mcpServers": {
    "ffmpeg": {
      "command": "python3",
      "args": ["/abs/path/to/mcp/servers/ffmpeg-mcp/server.py"],
      "env": {"FFMPEG_MCP_WORKDIR": "/abs/output/dir", "FFMPEG_MCP_TIMEOUT": "300"}
    }
  }
}
```

### Env vars

| Var | Default | Meaning |
|---|---|---|
| `FFMPEG_MCP_WORKDIR` | cwd | Base dir; bare filenames resolve here |
| `FFMPEG_MCP_TIMEOUT` | 300 | Hard per-command seconds; overrun → FFmpegError |

## Workflow

1. **Probe first.** Call `probe(path)` before any edit — confirm codecs/fps so `concat` inputs match and `cut` timings are sane.
2. **Paths.** Inputs accept absolute paths or bare names resolved against `FFMPEG_MCP_WORKDIR`. Outputs default to a suffixed sibling of the source; pass `output=` to override.
3. **Cut precision.** Default `cut` is stream-copy (fast, snaps to keyframes). Set `reencode=true` for frame-accurate boundaries at the cost of speed.
4. **Concat constraint.** `concat` uses stream copy, so all inputs MUST share codec/container. Probe each first; mismatched inputs need `transcode` to a common format beforehand.
5. **Normalize last.** Run `normalize_audio` after all edits — loudnorm re-encodes audio, so do it once at the end.
6. **Verify output.** Every tool returns the written path. `probe` the result if correctness matters.

### Error handling

All failures raise `FFmpegError` with the offending command and tail of stderr:
- missing input → `input not found: …`
- binary absent → `binary not found on PATH: ffmpeg`
- timeout → `timed out after Ns: …`
- non-zero exit → `exit N … stderr: …`

Never backgrounds a process and never invokes a shell — argv is passed directly, so there's no injection surface from quoted filenames.

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Just let the agent run `ffmpeg` in bash" | Typed tools prevent malformed flags and give structured errors; raw shell invites quoting bugs and runaway commands. |
| "Stream-copy is always fine" | It snaps cuts to keyframes — off by up to a GOP. Use `reencode=true` when the boundary must be exact. |
| "Concat anything" | Stream-copy concat needs identical codecs. Probe first or transcode to a common format. |
| "Set concurrency high like Remotion" | FFmpeg already threads internally; the MCP layer serializes. Don't fan out blindly — respect the timeout budget. |
| "Timeouts don't matter locally" | A bad filtergraph can hang forever. The hard timeout is the safety net. |

## Verification

- [ ] `python3 -c "import server"` loads with no import error
- [ ] Exactly 12 tools registered (`probe, transcode, cut, extract_audio, thumbnail, make_gif, concat, normalize_audio, compress, extract_frames, add_subtitles, strip_metadata`)
- [ ] `probe` on a known file returns valid JSON with width/height/duration
- [ ] `cut`, `transcode`, `concat`, `thumbnail`, `extract_audio` produce readable output files (verified against a generated `testsrc2` clip)
- [ ] Missing-input call raises `FFmpegError`, not a traceback crash
- [ ] `FFMPEG_MCP_TIMEOUT` enforced on a long-running encode
