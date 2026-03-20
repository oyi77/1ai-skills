#!/usr/bin/env python3
"""
NotebookLM Automation Helper
CLI tool to interact with Google NotebookLM via notebooklm-py.

Auth: Uses Playwright storage state at ~/.notebooklm_playwright.json
      (auto-converted from browser extension export at ~/.notebooklm_cookies.json)

Usage:
    python notebooklm_helper.py --action list
    python notebooklm_helper.py --action create --title "My Notebook"
    python notebooklm_helper.py --action import --notebook-id X --source-url https://...
    python notebooklm_helper.py --action generate --notebook-id X --output-type audio
    python notebooklm_helper.py --action download --notebook-id X --output-type audio
"""

import argparse, json, os, sys, asyncio
from pathlib import Path
from datetime import datetime

try:
    import notebooklm
    from notebooklm import _notebooks, _sources, _artifacts
except ImportError:
    print("ERROR: notebooklm-py not installed.\nRun: pip install notebooklm-py --break-system-packages")
    sys.exit(1)

OUTPUT_DIR = Path(__file__).parent.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

COOKIES_FILE = Path("~/.notebooklm_cookies.json").expanduser()
PW_STATE_FILE = Path("~/.notebooklm_playwright.json").expanduser()

def convert_cookies_to_playwright():
    """Convert browser extension cookie format to Playwright storage state."""
    if not COOKIES_FILE.exists():
        return False
    cookies_raw = json.loads(COOKIES_FILE.read_text())
    storage_state = {"cookies": [], "origins": []}
    for c in cookies_raw:
        samesite = c.get("sameSite") or "None"
        if samesite == "no_restriction": samesite = "None"
        elif samesite == "lax": samesite = "Lax"
        elif samesite == "strict": samesite = "Strict"
        storage_state["cookies"].append({
            "name": c["name"], "value": c["value"],
            "domain": c["domain"], "path": c.get("path", "/"),
            "expires": int(c.get("expirationDate", -1)),
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", False),
            "sameSite": samesite
        })
    PW_STATE_FILE.write_text(json.dumps(storage_state, indent=2))
    return True

async def get_client():
    """Get authenticated NotebookLM client."""
    if not PW_STATE_FILE.exists():
        if not convert_cookies_to_playwright():
            print("ERROR: No cookies found.\nSet NOTEBOOKLM_COOKIES_FILE env var or export cookies to ~/.notebooklm_cookies.json")
            sys.exit(1)
    return await notebooklm.NotebookLMClient.from_storage(PW_STATE_FILE)

async def cmd_list():
    client = await get_client()
    async with client:
        api = _notebooks.NotebooksAPI(client._core)
        notebooks = await api.list()
        if not notebooks:
            print("No notebooks found.")
            return
        print(f"Found {len(notebooks)} notebooks:")
        for nb in notebooks:
            print(f"  [{nb.id[:8]}...] {nb.title}")

async def cmd_create(title):
    client = await get_client()
    async with client:
        api = _notebooks.NotebooksAPI(client._core)
        nb = await api.create(title)
        print(json.dumps({"id": nb.id, "title": nb.title, "created": True}))

async def cmd_import(notebook_id, source_url=None, source_text=None):
    client = await get_client()
    async with client:
        api = _sources.SourcesAPI(client._core)
        if source_url:
            src = await api.add_url(notebook_id, source_url)
            print(f"Added URL source: {src.id} (status: {src.status})")
            # Wait for processing
            print("Waiting for source to be processed...")
            await api.wait_for_sources(notebook_id, [src.id])
            src = await api.get(notebook_id, src.id)
            print(json.dumps({"source_id": src.id, "title": src.title, "status": str(src.status), "ready": src.is_ready}))
        elif source_text:
            src = await api.add_text(notebook_id, source_text[:100]+"...", source_text)
            print(json.dumps({"source_id": src.id, "title": src.title}))

async def cmd_generate(notebook_id, output_type):
    client = await get_client()
    async with client:
        artifacts_api = _artifacts.ArtifactsAPI(client._core)
        print(f"Generating {output_type} for notebook {notebook_id}...")
        if output_type == "audio":
            artifact = await artifacts_api.generate_audio_overview(notebook_id)
        elif output_type == "report":
            artifact = await artifacts_api.generate_briefing_doc(notebook_id)
        elif output_type == "quiz":
            artifact = await artifacts_api.generate_quiz(notebook_id)
        elif output_type == "mindmap":
            artifact = await artifacts_api.generate_mind_map(notebook_id)
        elif output_type == "slides":
            artifact = await artifacts_api.generate_slide_deck(notebook_id)
        else:
            print(f"Unknown output type: {output_type}")
            return
        print(json.dumps({"artifact_id": artifact.id, "type": str(artifact.artifact_type), "status": str(artifact.status)}))

async def cmd_download(notebook_id, output_type):
    client = await get_client()
    async with client:
        artifacts_api = _artifacts.ArtifactsAPI(client._core)
        artifacts = await artifacts_api.list(notebook_id)
        target = None
        for a in artifacts:
            if output_type in str(a.artifact_type).lower():
                target = a
                break
        if not target:
            print(f"No {output_type} artifact found. Generate it first.")
            return
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = {"audio": "mp3", "video": "mp4", "slides": "pdf", "quiz": "json"}.get(output_type, "bin")
        outfile = OUTPUT_DIR / f"{notebook_id[:8]}_{output_type}_{ts}.{ext}"
        await artifacts_api.download(notebook_id, target.id, outfile)
        print(f"Downloaded to: {outfile}")

def main():
    parser = argparse.ArgumentParser(description="NotebookLM Automation Helper")
    parser.add_argument("--action", required=True, choices=["list","create","import","generate","download"])
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--source-url", help="Source URL")
    parser.add_argument("--source-text", help="Source text")
    parser.add_argument("--output-type", choices=["audio","video","slides","quiz","report","mindmap"])
    parser.add_argument("--title", help="Notebook title")
    args = parser.parse_args()

    if args.action == "list":
        asyncio.run(cmd_list())
    elif args.action == "create":
        if not args.title: parser.error("--title required")
        asyncio.run(cmd_create(args.title))
    elif args.action == "import":
        if not args.notebook_id: parser.error("--notebook-id required")
        asyncio.run(cmd_import(args.notebook_id, args.source_url, args.source_text))
    elif args.action == "generate":
        if not args.notebook_id: parser.error("--notebook-id required")
        if not args.output_type: parser.error("--output-type required")
        asyncio.run(cmd_generate(args.notebook_id, args.output_type))
    elif args.action == "download":
        if not args.notebook_id: parser.error("--notebook-id required")
        if not args.output_type: parser.error("--output-type required")
        asyncio.run(cmd_download(args.notebook_id, args.output_type))

if __name__ == "__main__":
    main()
