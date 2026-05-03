"""
ai_visual_validator.py — Vision-Based UI & Content Validation
=============================================================
Uses oracle CLI (with vision model) to analyze screenshots and score outputs.

Functions:
  validate_screen(screenshot_path, expected_state) -> dict
  find_element_coords(screenshot_path, description) -> tuple
  score_generated_content(screenshot_path, content_type) -> float
  compare_screens(before_path, after_path, action_desc) -> dict
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("ai_visual_validator")

# ---------------------------------------------------------------------------
# Oracle CLI vision helpers
# ---------------------------------------------------------------------------
def call_vision_llm(prompt: str, image_path: Optional[str] = None, engine: str = "gemini") -> str:
    """Call oracle CLI with optional image for vision analysis."""
    cmd = ["oracle", "--prompt", prompt, "--engine", engine]
    if image_path and Path(image_path).exists():
        cmd += ["--file", image_path]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        logger.warning("oracle vision call failed (rc=%d): %s", result.returncode, result.stderr[:200])
    except FileNotFoundError:
        logger.warning("oracle CLI not found — using fallback text analysis")
        # Fallback: run without image
        if image_path:
            cmd_no_img = ["oracle", "--prompt", f"[Image: {image_path}] {prompt}", "--engine", engine]
            try:
                result = subprocess.run(cmd_no_img, capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    return result.stdout.strip()
            except Exception:  # pylint: disable=broad-except
                pass
    except subprocess.TimeoutExpired:
        logger.warning("oracle vision call timed out")
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("oracle vision error: %s", exc)
    return ""


def parse_json_from_response(text: str) -> Dict[str, Any]:
    """Extract and parse JSON from LLM response."""
    if not text:
        return {}
    # Try markdown code blocks first
    for pattern in [r"```json\s*(.*?)\s*```", r"```\s*(.*?)\s*```", r"(\{.*?\})"]:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                continue
    # Try raw JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def validate_screen(
    screenshot_path: str,
    expected_state: str,
    engine: str = "gemini",
) -> Dict[str, Any]:
    """
    Validate that a screenshot matches the expected UI state.

    Args:
        screenshot_path: Path to the screenshot file
        expected_state: Description of what the screen should show (e.g., "Kling app home screen")
        engine: LLM engine to use for analysis

    Returns:
        dict with keys:
            - valid (bool): Whether the screen matches expected state
            - confidence (float): 0-10 confidence score
            - actual_state (str): What the screen actually shows
            - issues (list[str]): Any problems found
            - recommendations (list[str]): Suggested actions
    """
    if not Path(screenshot_path).exists():
        logger.error("Screenshot not found: %s", screenshot_path)
        return {
            "valid": False,
            "confidence": 0.0,
            "actual_state": "screenshot_not_found",
            "issues": [f"File not found: {screenshot_path}"],
            "recommendations": ["Take a new screenshot before validation"],
        }

    prompt = (
        f"Analyze this mobile app screenshot and validate if it shows: '{expected_state}'\n"
        f"Return JSON with these fields:\n"
        f"  - valid: true/false (does screen match expected state?)\n"
        f"  - confidence: 0-10 (how confident are you?)\n"
        f"  - actual_state: brief description of what screen actually shows\n"
        f"  - issues: array of problems found (empty if none)\n"
        f"  - recommendations: array of suggested actions\n"
        f"Be specific and accurate."
    )

    raw = call_vision_llm(prompt, screenshot_path, engine)
    data = parse_json_from_response(raw)

    if not data:
        logger.warning("Could not parse validation response: %s", raw[:200])
        # Return conservative fallback
        return {
            "valid": False,
            "confidence": 3.0,
            "actual_state": raw[:200] if raw else "unknown",
            "issues": ["Could not parse validation response"],
            "recommendations": ["Manual verification required"],
        }

    # Ensure required fields
    result = {
        "valid": bool(data.get("valid", False)),
        "confidence": float(data.get("confidence", 5.0)),
        "actual_state": str(data.get("actual_state", "unknown")),
        "issues": list(data.get("issues", [])),
        "recommendations": list(data.get("recommendations", [])),
    }

    logger.info(
        "Screen validation: valid=%s confidence=%.1f state='%s'",
        result["valid"], result["confidence"], result["actual_state"][:60],
    )
    return result


def find_element_coords(
    screenshot_path: str,
    description: str,
    screen_width: int = 1080,
    screen_height: int = 1920,
    engine: str = "gemini",
) -> Tuple[Optional[int], Optional[int]]:
    """
    Find the screen coordinates of a UI element in a screenshot.

    Args:
        screenshot_path: Path to the screenshot
        description: Description of the element to find (e.g., "Generate Video button")
        screen_width: Device screen width in pixels (default 1080)
        screen_height: Device screen height in pixels (default 1920)
        engine: LLM engine for analysis

    Returns:
        (x, y) tuple of estimated coordinates, or (None, None) if not found
    """
    if not Path(screenshot_path).exists():
        logger.error("Screenshot not found: %s", screenshot_path)
        return None, None

    prompt = (
        f"Find the UI element: '{description}' in this mobile app screenshot.\n"
        f"Screen dimensions: {screen_width}x{screen_height} pixels.\n"
        f"If found, return JSON: {{\"found\": true, \"x\": <pixel_x>, \"y\": <pixel_y>, "
        f"\"confidence\": <0-10>, \"description\": \"what you found\"}}\n"
        f"If NOT found, return JSON: {{\"found\": false, \"reason\": \"why not found\"}}\n"
        f"Estimate pixel coordinates carefully based on element position."
    )

    raw = call_vision_llm(prompt, screenshot_path, engine)
    data = parse_json_from_response(raw)

    if not data:
        logger.warning("Could not parse element search response for '%s'", description)
        return None, None

    if not data.get("found", False):
        reason = data.get("reason", "not visible")
        logger.warning("Element '%s' not found: %s", description, reason)
        return None, None

    x = data.get("x")
    y = data.get("y")
    confidence = float(data.get("confidence", 5.0))

    if x is None or y is None:
        logger.warning("Element '%s' found but coordinates missing", description)
        return None, None

    # Validate coordinates are within screen bounds
    x = max(0, min(int(x), screen_width))
    y = max(0, min(int(y), screen_height))

    logger.info(
        "Element '%s' found at (%d, %d) confidence=%.1f",
        description, x, y, confidence,
    )
    return x, y


def score_generated_content(
    screenshot_path: str,
    content_type: str,
    original_prompt: Optional[str] = None,
    engine: str = "gemini",
) -> float:
    """
    Score the quality of generated content visible in a screenshot.

    Args:
        screenshot_path: Path to screenshot of generated content
        content_type: Type of content (e.g., "video_thumbnail", "generated_image", "social_post")
        original_prompt: Original generation prompt for accuracy scoring
        engine: LLM engine for analysis

    Returns:
        Quality score from 0.0 to 10.0
    """
    if not Path(screenshot_path).exists():
        logger.error("Screenshot not found: %s", screenshot_path)
        return 0.0

    prompt_context = f"\nOriginal prompt was: '{original_prompt}'" if original_prompt else ""
    prompt = (
        f"Evaluate the quality of this {content_type} content.{prompt_context}\n"
        f"Score on these dimensions (1-10 each):\n"
        f"  - visual_quality: sharpness, clarity, resolution appearance\n"
        f"  - composition: framing, balance, visual hierarchy\n"
        f"  - relevance: matches the intended content type\n"
        f"  - professionalism: looks polished and high-quality\n"
        f"Return JSON: {{\"overall\": <0-10>, \"visual_quality\": <0-10>, "
        f"\"composition\": <0-10>, \"relevance\": <0-10>, "
        f"\"professionalism\": <0-10>, \"summary\": \"brief assessment\"}}"
    )

    raw = call_vision_llm(prompt, screenshot_path, engine)
    data = parse_json_from_response(raw)

    if not data:
        logger.warning("Could not score content from screenshot: %s", raw[:100])
        return 5.0  # Neutral score on failure

    overall = float(data.get("overall", 5.0))
    summary = data.get("summary", "")
    logger.info(
        "Content quality score: %.1f/10 — %s",
        overall, summary[:80],
    )
    return overall


def compare_screens(
    before_path: str,
    after_path: str,
    action_description: str,
    engine: str = "gemini",
) -> Dict[str, Any]:
    """
    Compare two screenshots to verify an action had the expected effect.

    Args:
        before_path: Screenshot before the action
        after_path: Screenshot after the action
        action_description: What action was performed (e.g., "tapped Generate button")
        engine: LLM engine for analysis

    Returns:
        dict with:
            - success (bool): Did the action succeed?
            - change_detected (bool): Was any change detected?
            - confidence (float): 0-10 confidence
            - description (str): What changed
            - issues (list[str]): Problems found
    """
    before_exists = Path(before_path).exists()
    after_exists = Path(after_path).exists()

    if not after_exists:
        return {
            "success": False,
            "change_detected": False,
            "confidence": 0.0,
            "description": "After screenshot not found",
            "issues": ["Cannot compare without after screenshot"],
        }

    # If we only have the after screenshot, just analyze it
    if not before_exists:
        prompt = (
            f"Analyze this screenshot taken AFTER the action: '{action_description}'\n"
            f"Did the action appear to succeed based on the current state?\n"
            f"Return JSON: {{\"success\": true/false, \"confidence\": <0-10>, "
            f"\"description\": \"current state\", \"issues\": []}}"
        )
        raw = call_vision_llm(prompt, after_path, engine)
        data = parse_json_from_response(raw)
        return {
            "success": bool(data.get("success", False)),
            "change_detected": True,
            "confidence": float(data.get("confidence", 5.0)),
            "description": data.get("description", ""),
            "issues": data.get("issues", []),
        }

    # Compare both screenshots
    # Note: oracle may not support multi-image input natively
    # We analyze each and compare descriptions
    before_prompt = (
        f"Describe the UI state in this screenshot in 2-3 sentences. Be specific about "
        f"visible elements, text, and current app state."
    )
    after_prompt = (
        f"After performing '{action_description}', describe what changed in this screenshot. "
        f"Was the action successful? Return JSON: {{\"success\": true/false, "
        f"\"change_detected\": true/false, \"confidence\": <0-10>, "
        f"\"description\": \"what changed\", \"issues\": []}}"
    )

    before_desc = call_vision_llm(before_prompt, before_path, engine)
    after_raw = call_vision_llm(
        f"Before state: '{before_desc[:200]}'\n{after_prompt}",
        after_path,
        engine,
    )

    data = parse_json_from_response(after_raw)
    if not data:
        return {
            "success": False,
            "change_detected": False,
            "confidence": 3.0,
            "description": after_raw[:200] if after_raw else "unknown",
            "issues": ["Could not parse comparison response"],
        }

    result = {
        "success": bool(data.get("success", False)),
        "change_detected": bool(data.get("change_detected", False)),
        "confidence": float(data.get("confidence", 5.0)),
        "description": str(data.get("description", "")),
        "issues": list(data.get("issues", [])),
    }
    logger.info(
        "Screen comparison: success=%s change=%s confidence=%.1f",
        result["success"], result["change_detected"], result["confidence"],
    )
    return result


def detect_app_in_foreground(
    screenshot_path: str,
    expected_app: str,
    engine: str = "gemini",
) -> Tuple[bool, str]:
    """
    Detect if the expected app is currently in the foreground.

    Args:
        screenshot_path: Current screenshot
        expected_app: App name to look for (e.g., "Kling", "CapCut")

    Returns:
        (is_expected_app, actual_app_name)
    """
    if not Path(screenshot_path).exists():
        return False, "unknown"

    prompt = (
        f"What Android app is currently in the foreground in this screenshot? "
        f"Is it '{expected_app}'? "
        f"Return JSON: {{\"app_name\": \"<detected app>\", \"is_expected\": true/false, "
        f"\"confidence\": <0-10>}}"
    )

    raw = call_vision_llm(prompt, screenshot_path, engine)
    data = parse_json_from_response(raw)

    if not data:
        return False, "parse_error"

    is_expected = bool(data.get("is_expected", False))
    actual_app = str(data.get("app_name", "unknown"))
    confidence = float(data.get("confidence", 5.0))

    logger.info(
        "Foreground app detection: expected=%s actual=%s match=%s confidence=%.1f",
        expected_app, actual_app, is_expected, confidence,
    )
    return is_expected, actual_app


# ---------------------------------------------------------------------------
# Batch validation helper
# ---------------------------------------------------------------------------
def validate_automation_sequence(
    screenshots: List[str],
    expected_states: List[str],
    engine: str = "gemini",
) -> Dict[str, Any]:
    """
    Validate a sequence of screenshots against expected states.

    Returns:
        dict with overall success, per-step results, and failure points
    """
    assert len(screenshots) == len(expected_states), "screenshots and expected_states must match in length"

    results = []
    overall_success = True
    failure_point = None

    for i, (screenshot, expected) in enumerate(zip(screenshots, expected_states)):
        validation = validate_screen(screenshot, expected, engine)
        results.append({
            "step": i + 1,
            "screenshot": screenshot,
            "expected": expected,
            **validation,
        })
        if not validation["valid"] and overall_success:
            overall_success = False
            failure_point = i + 1

    return {
        "overall_success": overall_success,
        "steps_validated": len(results),
        "failure_point": failure_point,
        "results": results,
    }


if __name__ == "__main__":
    # Quick test with a dummy path
    result = validate_screen("/tmp/test_screen.png", "Kling app home screen")
    print("Validation result:", result)

    coords = find_element_coords("/tmp/test_screen.png", "Generate Video button")
    print("Element coords:", coords)
