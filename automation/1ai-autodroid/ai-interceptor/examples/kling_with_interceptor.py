"""
kling_with_interceptor.py — Integration Example: Kling + AI Interceptor
========================================================================
Shows how to wrap the existing kling_agent.py with the AI Interceptor
middleware for automatic prompt enhancement, quality scoring, and retry.

Usage:
    python3 kling_with_interceptor.py --prompt "wanita jalan di taman" --image photo.jpg
    python3 kling_with_interceptor.py --prompt "sunset beach" --mode t2v
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Setup path so we can import from scripts/
# ---------------------------------------------------------------------------
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from ai_interceptor import AIInterceptor, InterceptResult
from prompt_interceptor import create_prompt_interceptor
from adb_interceptor import create_adb_interceptor

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("kling_example")


# ---------------------------------------------------------------------------
# Mock Kling agent (replace with actual kling_agent.py import)
# ---------------------------------------------------------------------------
def _mock_kling_api_call(
    prompt: str,
    input_image: Optional[str] = None,
    negative_prompt: str = "",
    mode: str = "i2v",
    aspect_ratio: str = "16:9",
    duration: int = 5,
    **kwargs,
) -> dict:
    """
    Mock Kling API call. Replace this with actual kling_agent.py integration:

        from kling_agent import KlingAgent
        agent = KlingAgent()
        return agent.generate(prompt=prompt, input_image=input_image, ...)
    """
    logger.info("🎬 Calling Kling API: mode=%s prompt=%s", mode, prompt[:60])
    # Simulate API call delay
    time.sleep(0.1)

    # Simulate occasional failures for demo
    import random
    if random.random() < 0.2:  # 20% chance of failure
        raise ConnectionError("Kling API connection timeout")

    return {
        "status": "success",
        "task_id": f"kling_{int(time.time())}",
        "url": f"https://cdn.kling.ai/videos/demo_{int(time.time())}.mp4",
        "prompt": prompt,
        "mode": mode,
        "duration": duration,
        "created_at": time.time(),
    }


# ---------------------------------------------------------------------------
# Option 1: Simple decorator pattern
# ---------------------------------------------------------------------------
def demo_decorator_pattern(prompt: str, input_image: Optional[str] = None):
    """Demonstrate using @interceptor.intercept decorator."""
    print("\n" + "="*60)
    print("Option 1: Decorator Pattern")
    print("="*60)

    # Create interceptor with prompt-specific hooks
    interceptor = create_prompt_interceptor()

    @interceptor.intercept(skill_type="kling_i2v")
    def generate_video(
        prompt: str,
        input_image: Optional[str] = None,
        negative_prompt: str = "",
        mode: str = "i2v",
    ) -> dict:
        """Generate video using Kling AI."""
        return _mock_kling_api_call(
            prompt=prompt,
            input_image=input_image,
            negative_prompt=negative_prompt,
            mode=mode,
        )

    print(f"Input prompt: {prompt}")
    print(f"Input image: {input_image}")
    print("\n🚀 Running with AI Interceptor...")

    result = generate_video(
        prompt=prompt,
        input_image=input_image,
        mode="i2v" if input_image else "t2v",
    )

    print(f"\n✅ Result: {json.dumps(result, indent=2, default=str)}" if result else "❌ Generation failed")
    return result


# ---------------------------------------------------------------------------
# Option 2: interceptor.run() pattern (access full InterceptResult)
# ---------------------------------------------------------------------------
def demo_run_pattern(prompt: str, input_image: Optional[str] = None):
    """Demonstrate using interceptor.run() for access to InterceptResult."""
    print("\n" + "="*60)
    print("Option 2: interceptor.run() with Full Result")
    print("="*60)

    interceptor = create_prompt_interceptor()

    print(f"Input prompt: {prompt}")
    print(f"Input image: {input_image}")
    print("\n🚀 Running with AI Interceptor...")

    result: InterceptResult = interceptor.run(
        func=_mock_kling_api_call,
        skill_type="kling_i2v",
        kwargs={
            "prompt": prompt,
            "input_image": input_image,
            "mode": "i2v" if input_image else "t2v",
        },
    )

    print(f"\n📊 Intercept Summary:")
    print(f"  Success:        {result.success}")
    print(f"  Quality Score:  {result.quality_score:.1f}/10")
    print(f"  Retries:        {result.retries}")
    print(f"  Pre-Enhanced:   {result.pre_enhanced}")
    print(f"  Post-Validated: {result.post_validated}")
    print(f"  Error Diagnosed:{result.error_diagnosed}")
    if result.error_message:
        print(f"  Error:          {result.error_message}")
    print(f"\n  Audit Trail ({len(result.audit_trail)} events):")
    for event in result.audit_trail[:5]:  # Show first 5
        print(f"    [{event['event']}] attempt={event['attempt']}")

    if result.output:
        print(f"\n✅ Output: {json.dumps(result.output, indent=2, default=str)}")
    else:
        print("\n❌ No output generated")

    return result


# ---------------------------------------------------------------------------
# Option 3: ADB interceptor pattern (for Android automation)
# ---------------------------------------------------------------------------
def demo_adb_pattern(prompt: str, app: str = "kling"):
    """Demonstrate ADB interceptor for Android automation."""
    print("\n" + "="*60)
    print("Option 3: ADB Interceptor (Android Automation)")
    print("="*60)

    interceptor = create_adb_interceptor()

    def adb_input_prompt_and_generate(
        prompt: str,
        app: str = "kling",
        device: Optional[str] = None,
        element_description: str = "text input field",
        expected_screen: str = "video generation result",
    ) -> dict:
        """Simulate ADB interaction with Kling app."""
        logger.info("📱 ADB: Typing prompt into %s app", app)
        # In real usage, this would use ADB commands to:
        # 1. Find and tap the text input field
        # 2. Type the prompt
        # 3. Tap the Generate button
        # 4. Wait for result
        return {
            "status": "submitted",
            "app": app,
            "prompt": prompt,
            "device": device,
        }

    print(f"App: {app}")
    print(f"Prompt: {prompt}")
    print("\n📱 Running ADB automation with AI Interceptor...")

    result: InterceptResult = interceptor.run(
        func=adb_input_prompt_and_generate,
        skill_type="kling_i2v",
        kwargs={
            "prompt": prompt,
            "app": app,
            "element_description": "prompt text input",
            "expected_screen": "generation in progress",
        },
    )

    print(f"\n📊 ADB Result: success={result.success}, retries={result.retries}")
    return result


# ---------------------------------------------------------------------------
# Option 4: Wrapping existing kling_agent.py
# ---------------------------------------------------------------------------
def demo_wrap_existing_agent(prompt: str, input_image: Optional[str] = None):
    """
    Example of how to wrap an existing kling_agent.py without modifying it.

    Replace the import below with your actual kling_agent.py path:
        sys.path.insert(0, '/path/to/kling_agent_dir')
        from kling_agent import KlingAgent

    Then wrap it as shown.
    """
    print("\n" + "="*60)
    print("Option 4: Wrapping Existing kling_agent.py")
    print("="*60)

    # Simulated existing agent class
    class ExistingKlingAgent:
        """Simulated existing Kling agent (replace with real import)."""

        def generate_i2v(self, prompt: str, image_path: str, **kwargs) -> dict:
            return _mock_kling_api_call(prompt=prompt, input_image=image_path, mode="i2v", **kwargs)

        def generate_t2v(self, prompt: str, **kwargs) -> dict:
            return _mock_kling_api_call(prompt=prompt, mode="t2v", **kwargs)

    # Create interceptor and wrap the existing agent
    interceptor = create_prompt_interceptor()
    agent = ExistingKlingAgent()

    # Wrap the method without modifying ExistingKlingAgent
    def wrapped_generate_i2v(prompt: str, image_path: str = "", **kwargs) -> dict:
        return agent.generate_i2v(prompt=prompt, image_path=image_path, **kwargs)

    result = interceptor.run(
        func=wrapped_generate_i2v,
        skill_type="kling_i2v",
        kwargs={
            "prompt": prompt,
            "image_path": input_image or "",
        },
    )

    print(f"Wrapped agent result: success={result.success}, quality={result.quality_score:.1f}")
    return result


# ---------------------------------------------------------------------------
# Main CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Kling AI with Interceptor Demo")
    parser.add_argument("--prompt", default="wanita cantik berjalan di taman bunga", help="Generation prompt")
    parser.add_argument("--image", default=None, help="Input image path (for i2v mode)")
    parser.add_argument("--mode", choices=["i2v", "t2v"], default="i2v", help="Generation mode")
    parser.add_argument("--demo", choices=["1", "2", "3", "4", "all"], default="2", help="Demo to run")
    args = parser.parse_args()

    print("🎬 Kling AI with AI Interceptor Middleware")
    print(f"Prompt: {args.prompt}")
    print(f"Mode: {args.mode}")

    if args.demo in ("1", "all"):
        demo_decorator_pattern(args.prompt, args.image)

    if args.demo in ("2", "all"):
        demo_run_pattern(args.prompt, args.image)

    if args.demo in ("3", "all"):
        demo_adb_pattern(args.prompt)

    if args.demo in ("4", "all"):
        demo_wrap_existing_agent(args.prompt, args.image)

    print("\n✅ Demo complete! Check /tmp/ai_interceptor.log for full audit trail.")


if __name__ == "__main__":
    main()
