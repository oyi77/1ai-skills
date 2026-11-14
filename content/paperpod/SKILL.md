---
name: paperpod
description: Use when running code, checking live previews, automating browsers, using 50+ tools (ffmpeg, sqlite, pandoc, imagemagick), and calling LLMs inside isolated Paperpod sandboxes via CLI or HTTP without SDK or API keys.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- sandbox
- cli
- preview
- browser-automation
- ffmpeg
- sqlite
- tools
version: 1.0.0
category: content
---

# Paperpod — Isolated Agent Sandboxes

> ⚠️ **Scope honesty.** This skill could not corroborate a public "Paperpod" product or its API surface during authoring. The **HTTP endpoints, CLI subcommands, and image names below are illustrative placeholders**, not verified contracts. Before relying on any of it, confirm the real Paperpod docs/CLI for your environment. What survives regardless: the *pattern* — run untrusted/heavy work in an ephemeral isolated sandbox, expose a port via a tunnel URL, fetch artifacts, then destroy to stop billing.

Run code, preview apps live, automate browsers, and use 50+ built-in tools (ffmpeg, sqlite, pandoc, imagemagick) inside an isolated Paperpod sandbox via CLI or HTTP. No SDK or API keys required.

## When to Use

**Trigger phrases:**
- "spin up a sandbox" · "run in paperpod" · "live preview URL"
- "browser automation sandbox" · "run ffmpeg / imagemagick in cloud sandbox"
- "isolated code execution"

**Use cases:**
- Executing untrusted code safely
- Getting a public live preview URL for a local web app
- Running heavy CLI tools (ffmpeg, pandoc) without local dependencies
- Browser automation (Puppeteer/Playwright) in a clean container

## When NOT to Use

- Local development where you already have all tools installed and running
- Long-running production servers (Paperpod sandboxes have compute limits)
- High-throughput database operations requiring persistent disk backing

## Core Capabilities

- **50+ CLI tools pre-installed:** `ffmpeg`, `ffprobe`, `sqlite3`, `pandoc`, `imagemagick`, `curl`, `git`, `node`, `python3`, `jq`, `ripgrep`, etc.
- **Live Preview URLs:** Instant public HTTPS tunnels to any port running inside the sandbox.
- **Browser Automation:** Headless Chromium pre-configured with Playwright / Puppeteer.
- **Persistent Memory:** Scratchpad folders and key-value state stored across sandbox sessions.

## Setup & CLI Usage

```bash
# Install paperpod CLI (or use via the paperpod skill / MCP if connected)
npm install -g paperpod-cli

# 1. Spin up an interactive sandbox
paperpod run --image node:20

# 2. Run a script with live preview on port 3000
paperpod up --port 3000 -- npx vite

# 3. Execute a one-off command in a fresh sandbox
paperpod exec -- ffmpeg -i input.mp4 -vf scale=1080:1920 out.mp4
```

## Workflow

### 1. Spin up sandbox with required tools

```python
# Create sandbox via HTTP API
import requests, os

API = "https://api.paperpod.dev/v1"
HEADERS = {"Authorization": f"Bearer {os.environ.get('PAPERPOD_API_KEY', 'local')}"}

def create_sandbox(image: str = "ubuntu:22.04") -> dict:
    r = requests.post(f"{API}/sandboxes", headers=HEADERS, json={"image": image})
    r.raise_for_status()
    return r.json() # {"id": "sb_123", "preview_url": "..."}
```

### 2. Execute commands and stream output

```python
def exec_cmd(sandbox_id: str, cmd: str) -> dict:
    r = requests.post(
        f"{API}/sandboxes/{sandbox_id}/exec",
        headers=HEADERS,
        json={"command": cmd},
        timeout=300,
    )
    r.raise_for_status()
    return r.json() # {"stdout": "...", "stderr": "...", "exit_code": 0}
```

### 3. Fetch files or preview URLs

```python
# Download rendered video or image from sandbox
def get_file(sandbox_id: str, remote_path: str, local_path: str):
    r = requests.get(
        f"{API}/sandboxes/{sandbox_id}/files",
        headers=HEADERS,
        params={"path": remote_path},
        stream=True,
    )
    r.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in r.iter_content(8192):
            f.write(chunk)
```

### 4. Cleanup

```python
def destroy_sandbox(sandbox_id: str):
    requests.delete(f"{API}/sandboxes/{sandbox_id}", headers=HEADERS)
```

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll run untrusted code locally" | Never run unvetted scripts on your host machine. Use the sandbox. |
| "I don't need to destroy sandboxes" | Sandboxes bill per second of compute. Always clean up in a `try...finally` block. |
| "Previews work without ports" | You must map the port explicitly (`--port 3000`) for the tunnel URL to route traffic. |

## Verification

- [ ] Sandbox initializes and responds to `/health` or `exec` in <10s
- [ ] Required CLI tools (`ffmpeg`, `node`, etc.) present in path
- [ ] Live preview URL returns 200 OK for running web app
- [ ] Files correctly transferred in/out of sandbox
- [ ] Sandbox destroyed immediately after task completion to stop billing
