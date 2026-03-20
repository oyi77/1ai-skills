#!/usr/bin/env python3
"""
Podcast Production Pipeline for NotebookLM

Automates the full podcast workflow: topic/URL → NotebookLM import →
Audio Overview generation → MP3 download.

Uses notebooklm_helper.py (same directory) for NotebookLM operations.

Usage:
    python podcast_pipeline.py --topic "AI trading strategies 2026"
    python podcast_pipeline.py --url "https://example.com/article"
    python podcast_pipeline.py --topic "crypto market analysis" --title "Crypto Weekly"
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent scripts dir to path for notebooklm_helper
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

OUTPUT_DIR = SCRIPT_DIR.parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OMNIROUTE_BASE = "http://localhost:20128/v1"
OMNIROUTE_KEY = "omniroute"
OMNIROUTE_MODEL = "auto/pro-chat"


def get_llm_client():
    """Get OpenAI-compatible client via OmniRoute."""
    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai not installed. Run: pip install openai")
        sys.exit(1)
    return OpenAI(base_url=OMNIROUTE_BASE, api_key=OMNIROUTE_KEY)


def llm_chat(client, system_prompt, user_prompt):
    """Send chat completion via OmniRoute."""
    try:
        resp = client.chat.completions.create(
            model=OMNIROUTE_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"[LLM Error: {e}]"


def generate_source_text(topic):
    """Generate source material from a topic using LLM for NotebookLM import."""
    print(f"  Generating source material for topic: {topic}")
    client = get_llm_client()

    system = """You are a research writer. Write a comprehensive article (800-1500 words)
on the given topic. Include facts, analysis, and multiple perspectives.
Write in a style suitable for conversion to a podcast discussion.
Include section headings and key takeaways."""

    raw = llm_chat(client, system, f"Write a comprehensive article about: {topic}")
    return raw


async def run_pipeline(topic=None, url=None, title=None):
    """Run the full podcast production pipeline.

    Steps:
    1. Create NotebookLM notebook
    2. Import source (URL or generated text from topic)
    3. Generate Audio Overview
    4. Download MP3
    """
    try:
        import notebooklm_helper
    except ImportError:
        print("ERROR: notebooklm_helper.py not found in same directory.")
        print(f"Expected at: {SCRIPT_DIR / 'notebooklm_helper.py'}")
        sys.exit(1)

    notebook_title = title or f"Podcast: {topic or 'URL Import'}"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("=" * 60)
    print("PODCAST PRODUCTION PIPELINE")
    print(f"  Title: {notebook_title}")
    print(f"  Source: {'URL: ' + url if url else 'Topic: ' + (topic or 'N/A')}")
    print("=" * 60)

    # Step 1: Create notebook
    print("\n[1/4] Creating NotebookLM notebook...")
    client = await notebooklm_helper.get_client()
    async with client:
        from notebooklm import _notebooks, _sources, _artifacts

        notebooks_api = _notebooks.NotebooksAPI(client._core)
        nb = await notebooks_api.create(notebook_title)
        notebook_id = nb.id
        print(f"  Created: {notebook_id[:8]}... ({nb.title})")

        # Step 2: Import source
        print("\n[2/4] Importing source material...")
        sources_api = _sources.SourcesAPI(client._core)

        if url:
            src = await sources_api.add_url(notebook_id, url)
            print(f"  Added URL source: {src.id}")
            print("  Waiting for processing...")
            await sources_api.wait_for_sources(notebook_id, [src.id])
            src = await sources_api.get(notebook_id, src.id)
            print(f"  Source ready: {src.title} (status: {src.status})")
        elif topic:
            source_text = generate_source_text(topic)
            src = await sources_api.add_text(
                notebook_id,
                f"Research: {topic}",
                source_text,
            )
            print(f"  Added text source: {src.id}")
        else:
            print("ERROR: Provide either --topic or --url")
            return None

        # Step 3: Generate Audio Overview
        print("\n[3/4] Generating Audio Overview (podcast)...")
        print("  This may take 2-5 minutes...")
        artifacts_api = _artifacts.ArtifactsAPI(client._core)
        artifact = await artifacts_api.generate_audio_overview(notebook_id)
        print(f"  Audio generated: {artifact.id} (status: {artifact.status})")

        # Step 4: Download MP3
        print("\n[4/4] Downloading MP3...")
        outfile = OUTPUT_DIR / f"podcast_{ts}.mp3"
        await artifacts_api.download(notebook_id, artifact.id, outfile)
        print(f"  Saved to: {outfile}")

    result = {
        "status": "success",
        "notebook_id": notebook_id,
        "title": notebook_title,
        "source": url or topic,
        "source_type": "url" if url else "topic",
        "artifact_id": artifact.id,
        "output_file": str(outfile),
        "generated_at": datetime.now().isoformat(),
    }

    print("\n" + "=" * 60)
    print(f"DONE: Podcast saved to {outfile}")
    print(f"Notebook ID: {notebook_id}")
    print("=" * 60)

    return result


def main():
    parser = argparse.ArgumentParser(description="Podcast Production Pipeline")
    parser.add_argument("--topic", "-t", help="Topic to generate podcast about")
    parser.add_argument("--url", "-u", help="URL to import as source")
    parser.add_argument("--title", help="Custom podcast/notebook title")
    parser.add_argument("--output", "-o", help="Output JSON metadata file")

    args = parser.parse_args()

    if not args.topic and not args.url:
        parser.error("Provide either --topic or --url")

    result = asyncio.run(run_pipeline(args.topic, args.url, args.title))

    if result and args.output:
        with open(args.output, "w") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\nMetadata saved to: {args.output}")


if __name__ == "__main__":
    main()
