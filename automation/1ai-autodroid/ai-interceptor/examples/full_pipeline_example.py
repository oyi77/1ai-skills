"""
full_pipeline_example.py — End-to-End Kling Pipeline Demo

Demonstrates the complete Kling video generation pipeline:
  1. Account selection
  2. Prompt enhancement
  3. Video generation
  4. Watermark removal
  5. AI quality enhancement
  6. Quality scoring

Usage:
    python full_pipeline_example.py

Environment variables:
    KLING_COOKIE      — Kling session cookie (alternative to accounts.json)
    KLING_API_KEY     — Kling API key
"""

import logging
import os
import sys
from pathlib import Path

# Add scripts/ to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("full_pipeline_example")


def run_text_to_video_example():
    """Run a text-to-video generation example."""
    from kling_pipeline import KlingPipeline

    pipeline = KlingPipeline(
        config={
            "output_dir": "/tmp/kling_pipeline_demo",
            "min_credits": 60,
            "poll_interval": 10,
            "max_wait": 300,
        }
    )

    print("\n" + "=" * 60)
    print("  KLING PIPELINE — Text to Video")
    print("=" * 60)

    result = pipeline.text_to_video(
        prompt="A serene mountain lake at sunset, golden reflections on still water, cinematic quality",
        remove_watermark=True,
        enhance_quality=False,  # Skip if weights not downloaded
        duration="5",
        mode="std",
        aspect_ratio="16:9",
    )

    print(f"\nSuccess:         {result['success']}")
    print(f"Video:           {result['video_path']}")
    print(f"Original:        {result['original_path']}")
    print(f"Prompt original: {result['prompt_original']}")
    print(f"Prompt enhanced: {result['prompt_enhanced']}")
    print(f"Credits used:    {result['credits_used']}")
    print(f"Account:         {result['account_used']}")
    print(f"Quality score:   {result['quality_score']:.2f}")
    print(f"Processing time: {result['processing_time_s']:.1f}s")
    if result.get("error"):
        print(f"Error:           {result['error']}")

    return result


def run_image_to_video_example(image_path: str):
    """Run an image-to-video generation example."""
    from kling_pipeline import KlingPipeline

    pipeline = KlingPipeline(
        config={
            "output_dir": "/tmp/kling_pipeline_demo",
            "min_credits": 144,  # image2video costs more
        }
    )

    print("\n" + "=" * 60)
    print("  KLING PIPELINE — Image to Video")
    print("=" * 60)

    result = pipeline.image_to_video(
        prompt="Gentle camera pan across the scene, natural movement, cinematic",
        image_path=image_path,
        remove_watermark=True,
        enhance_quality=True,
        duration="5",
    )

    print(f"\nSuccess:    {result['success']}")
    print(f"Video:      {result['video_path']}")
    print(f"Error:      {result.get('error', 'None')}")
    return result


def run_provider_registry_example():
    """Demonstrate the provider registry."""
    from providers import get_registry

    registry = get_registry()
    print("\n" + "=" * 60)
    print("  PROVIDER REGISTRY")
    print("=" * 60)

    providers = registry.list_providers()
    print(f"\nRegistered providers: {providers}")

    print("\nHealth report:")
    for h in registry.health_report():
        status = "✅" if h["available"] else "❌"
        print(f"  {status} {h['provider']:15s} | credits={h['credits']:.0f} | caps={h['capabilities']}")

    # Find best provider for text2video
    best = registry.best_for("text2video", min_credits=60)
    if best:
        print(f"\nBest for text2video: {best.name}")
    else:
        print("\nNo available provider for text2video (configure API keys first)")


if __name__ == "__main__":
    # Check for required credentials
    has_cookie = bool(os.getenv("KLING_COOKIE"))
    has_api_key = bool(os.getenv("KLING_API_KEY"))

    print("Kling Pipeline — Full Pipeline Example")
    print(f"  KLING_COOKIE:  {'✅ Set' if has_cookie else '❌ Not set'}")
    print(f"  KLING_API_KEY: {'✅ Set' if has_api_key else '❌ Not set'}")

    if not has_cookie and not has_api_key:
        print("\n⚠️  No credentials set. Running provider registry demo only.")
        print("   Set KLING_COOKIE or KLING_API_KEY to run generation examples.")
        run_provider_registry_example()
    else:
        run_provider_registry_example()
        run_text_to_video_example()
