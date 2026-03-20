#!/usr/bin/env python3
"""
NotebookLM Automation Helper
CLI tool to interact with Google NotebookLM via notebooklm-py.

Usage:
    python notebooklm_helper.py --action create --title "My Notebook"
    python notebooklm_helper.py --action import --notebook-id X --source-url Y
    python notebooklm_helper.py --action generate --notebook-id X --output-type audio
    python notebooklm_helper.py --action download --notebook-id X
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "output"


def get_client():
    """Initialize NotebookLM client with auth."""
    try:
        from notebooklm import NotebookLM
    except ImportError:
        print("ERROR: notebooklm-py not installed.")
        print("Run: pip install notebooklm-py")
        sys.exit(1)

    cookies = os.environ.get("NOTEBOOKLM_COOKIES")
    cookies_file = os.environ.get("NOTEBOOKLM_COOKIES_FILE")

    if cookies_file and Path(cookies_file).exists():
        with open(cookies_file) as f:
            cookies = f.read()

    if not cookies:
        print("ERROR: NotebookLM authentication not configured.")
        print()
        print("Setup instructions:")
        print("1. Log into notebooklm.google.com in your browser")
        print("2. Export cookies using a browser extension")
        print("3. Set environment variable:")
        print('   export NOTEBOOKLM_COOKIES=\'<cookies_json>\'')
        print("   OR")
        print('   export NOTEBOOKLM_COOKIES_FILE=~/.notebooklm_cookies.json')
        sys.exit(1)

    try:
        client = NotebookLM(cookies=cookies)
        return client
    except Exception as e:
        print(f"ERROR: Failed to initialize NotebookLM client: {e}")
        print()
        print("Your cookies may be expired. Re-export from browser and try again.")
        sys.exit(1)


def action_create(args):
    """Create a new notebook."""
    client = get_client()
    title = args.title or f"Notebook {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    try:
        notebook = client.create_notebook(title=title)
        nb_id = getattr(notebook, "id", str(notebook))
        print(f"Created notebook: {title}")
        print(f"Notebook ID: {nb_id}")
        return nb_id
    except Exception as e:
        print(f"ERROR creating notebook: {e}")
        sys.exit(1)


def action_import(args):
    """Import a source into a notebook."""
    if not args.notebook_id:
        print("ERROR: --notebook-id required for import action")
        sys.exit(1)
    if not args.source_url:
        print("ERROR: --source-url required for import action")
        sys.exit(1)

    client = get_client()
    try:
        notebook = client.get_notebook(args.notebook_id)
        url = args.source_url

        if "youtube.com" in url or "youtu.be" in url:
            source = notebook.add_youtube_source(url)
        elif url.endswith(".pdf"):
            source = notebook.add_pdf_source(url)
        elif url.startswith("http"):
            source = notebook.add_website_source(url)
        else:
            source = notebook.add_text_source(url)

        print(f"Imported source: {url}")
        print(f"Source ID: {getattr(source, 'id', str(source))}")
    except Exception as e:
        print(f"ERROR importing source: {e}")
        sys.exit(1)


def action_generate(args):
    """Generate an artifact from a notebook."""
    if not args.notebook_id:
        print("ERROR: --notebook-id required for generate action")
        sys.exit(1)

    output_type = args.output_type or "audio"
    client = get_client()

    try:
        notebook = client.get_notebook(args.notebook_id)

        type_map = {
            "audio": "audio_overview",
            "video": "video_overview",
            "slides": "slides",
            "quiz": "quiz",
            "report": "report",
            "mindmap": "mind_map",
        }

        gen_type = type_map.get(output_type, output_type)
        result = notebook.generate(gen_type)

        out_dir = OUTPUT_DIR / args.notebook_id
        out_dir.mkdir(parents=True, exist_ok=True)

        ext_map = {
            "audio": ".mp3",
            "video": ".mp4",
            "slides": ".pptx",
            "quiz": ".json",
            "report": ".md",
            "mindmap": ".json",
        }
        ext = ext_map.get(output_type, ".bin")
        out_file = out_dir / f"{output_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"

        if hasattr(result, "content"):
            content = result.content
        elif hasattr(result, "data"):
            content = result.data
        else:
            content = result

        if isinstance(content, (str, dict)):
            with open(out_file, "w") as f:
                if isinstance(content, dict):
                    json.dump(content, f, indent=2)
                else:
                    f.write(content)
        else:
            with open(out_file, "wb") as f:
                f.write(content)

        print(f"Generated {output_type}: {out_file}")
    except Exception as e:
        print(f"ERROR generating {output_type}: {e}")
        sys.exit(1)


def action_download(args):
    """Download all artifacts from a notebook."""
    if not args.notebook_id:
        print("ERROR: --notebook-id required for download action")
        sys.exit(1)

    client = get_client()
    try:
        notebook = client.get_notebook(args.notebook_id)
        out_dir = OUTPUT_DIR / args.notebook_id
        out_dir.mkdir(parents=True, exist_ok=True)

        artifacts = notebook.get_artifacts() if hasattr(notebook, "get_artifacts") else []
        if not artifacts:
            print("No artifacts found. Generate some first with --action generate.")
            return

        for artifact in artifacts:
            name = getattr(artifact, "name", f"artifact_{id(artifact)}")
            data = artifact.download() if hasattr(artifact, "download") else artifact
            out_file = out_dir / name
            if isinstance(data, (str, dict)):
                with open(out_file, "w") as f:
                    f.write(json.dumps(data) if isinstance(data, dict) else data)
            else:
                with open(out_file, "wb") as f:
                    f.write(data)
            print(f"Downloaded: {out_file}")

        print(f"All artifacts saved to: {out_dir}")
    except Exception as e:
        print(f"ERROR downloading artifacts: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="NotebookLM Automation Helper")
    parser.add_argument("--action", required=True, choices=["create", "import", "generate", "download"])
    parser.add_argument("--notebook-id", help="Notebook ID")
    parser.add_argument("--source-url", help="Source URL (web, YouTube, PDF)")
    parser.add_argument("--output-type", choices=["audio", "video", "slides", "quiz", "report", "mindmap"],
                        default="audio", help="Output type for generate action")
    parser.add_argument("--title", help="Notebook title for create action")

    args = parser.parse_args()

    actions = {
        "create": action_create,
        "import": action_import,
        "generate": action_generate,
        "download": action_download,
    }

    actions[args.action](args)


if __name__ == "__main__":
    main()
