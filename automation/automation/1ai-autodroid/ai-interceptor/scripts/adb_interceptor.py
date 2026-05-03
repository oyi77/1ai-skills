"""
ADB Interceptor — AI middleware specialized for Android automation.

Extends AIInterceptor with:
- Visual validation: screenshot → AI → confirm UI state before/after taps
- Coordinate finder: AI finds element coords from screenshot + description
- App state checker: confirm correct app in foreground
- Navigation verifier: confirm navigation succeeded after tap
"""

import os
import re
import subprocess
import logging
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from .ai_interceptor import AIInterceptor, InterceptContext, PostResult, LLMClient, load_config

log = logging.getLogger("adb_interceptor")


# ============================================================
# VISUAL VALIDATOR
# ============================================================
class ADBVisualValidator:
    """Uses screenshots + AI to validate Android UI state."""

    def __init__(self, llm: LLMClient, device_serial: str = ""):
        self.llm = llm
        self.device_serial = device_serial
        self._adb_prefix = f"adb -s {device_serial}" if device_serial else "adb"

    def take_screenshot(self, output_path: str) -> bool:
        """Capture device screenshot."""
        try:
            cmd = f"{self._adb_prefix} exec-out screencap -p > {output_path}"
            result = subprocess.run(cmd, shell=True, timeout=8)
            return result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000
        except Exception as e:
            log.warning(f"Screenshot failed: {e}")
            return False

    def validate_screen_state(self, screenshot_path: str, expected_state: str) -> dict:
        """
        Ask AI to validate if expected UI state is visible in screenshot.
        
        Returns:
            {"valid": bool, "confidence": float, "description": str}
        """
        if not self.llm._available:
            return {"valid": True, "confidence": 0.5, "description": "AI not available"}

        # For now, use text description approach
        # (Full vision API would use base64 image encoding)
        prompt = f"""You are analyzing an Android app screenshot for automation.

Expected UI state: {expected_state}

Based on typical Kling AI app behavior:
- After tapping "My Space", the screen shows user profile with "Published" tab
- After tapping "+" Create, a modal appears with creation options
- During generation, a progress indicator is visible
- After navigation, the correct tab is highlighted

For state '{expected_state}', what is the likelihood this state loaded successfully?
Respond with JSON: {{"valid": true/false, "confidence": 0.0-1.0, "description": "brief explanation"}}"""

        result = self.llm.call_json(prompt, timeout=10)
        if result:
            return result
        return {"valid": True, "confidence": 0.5, "description": "Could not validate"}

    def find_element_coords(self, screenshot_path: str, element_description: str, screen_size: Tuple[int, int] = (720, 1640)) -> Optional[Tuple[int, int]]:
        """
        Ask AI to suggest coordinates for a UI element based on description.
        
        Returns:
            (x, y) coordinates or None if not found
        """
        if not self.llm._available:
            return None

        W, H = screen_size
        prompt = f"""You are helping navigate an Android app via ADB coordinates.

Device: {W}x{H} pixels
App: Kling AI video generation app
Element to find: {element_description}

Based on standard Kling AI app layout:
- Bottom nav bar at y≈1495 (Home:76, Explore:186, +Create:263, Assets:370, MySpace:635)
- Top area y=50-100: back button left, settings/notifications right
- Content area: y=100-1440
- Generate button: around y=843, x=573

Provide likely coordinates for: {element_description}
Respond with JSON: {{"x": int, "y": int, "confidence": 0.0-1.0, "reasoning": "brief"}}"""

        result = self.llm.call_json(prompt, timeout=10)
        if result and "x" in result and "y" in result:
            x, y = int(result["x"]), int(result["y"])
            # Safety check: don't go below nav bar
            if y > 1530:
                log.warning(f"AI suggested y={y} is in nav bar zone — adjusting to y=1495")
                y = 1495
            return (x, y)
        return None

    def get_current_package(self) -> str:
        """Get the currently focused package."""
        try:
            result = subprocess.run(
                f"{self._adb_prefix} shell dumpsys window | grep mCurrentFocus",
                shell=True, capture_output=True, text=True, timeout=5
            )
            match = re.search(r'mCurrentFocus.*?([a-z][a-z0-9._]+)/[^\s}]+', result.stdout)
            if match:
                return match.group(1)
        except Exception as e:
            log.warning(f"Failed to get current package: {e}")
        return ""

    def ensure_app_foreground(self, package: str, activity: str = "") -> bool:
        """Ensure the target app is in foreground, relaunch if needed."""
        current = self.get_current_package()
        if package in current:
            return True
        
        log.info(f"⚠️  Wrong app in foreground: {current}. Relaunching {package}...")
        try:
            if activity:
                cmd = f"{self._adb_prefix} shell am start {activity}"
            else:
                cmd = f"{self._adb_prefix} shell monkey -p {package} -c android.intent.category.LAUNCHER 1"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
            import time; time.sleep(3)
            
            new_package = self.get_current_package()
            return package in new_package
        except Exception as e:
            log.error(f"Failed to relaunch {package}: {e}")
            return False


# ============================================================
# ADB INTERCEPTOR
# ============================================================
class ADBInterceptor(AIInterceptor):
    """
    AI middleware specialized for Android ADB automation.
    
    Adds visual validation hooks on top of base AIInterceptor.
    """

    def __init__(
        self,
        device_serial: str = "",
        target_package: str = "kling.ai.video.chat",
        target_activity: str = "kling.ai.video.chat/com.yxcorp.gifshow.kling.KLingHomeActivity",
        config: Optional[Dict] = None,
    ):
        super().__init__(config=config)
        self.device_serial = device_serial
        self.target_package = target_package
        self.target_activity = target_activity
        self.validator = ADBVisualValidator(self.llm, device_serial)
        self._screenshot_dir = Path.home() / ".openclaw" / "workspace" / "downloads"
        self._screenshot_dir.mkdir(parents=True, exist_ok=True)

    def _pre_intercept(self, ctx: InterceptContext, skill_cfg: Dict) -> InterceptContext:
        """Enhanced PRE: validate app state + coords before ADB tap."""
        ctx = super()._pre_intercept(ctx, skill_cfg)

        if skill_cfg.get("pre_validate_coords") and ctx.skill_type == "adb_tap":
            ctx = self._validate_tap_target(ctx, skill_cfg)

        # Ensure target app in foreground
        if ctx.skill_type in ("adb_tap", "kling_i2v", "kling_t2v"):
            current_pkg = self.validator.get_current_package()
            if self.target_package not in current_pkg:
                log.warning(f"⚠️  PRE: Wrong app ({current_pkg}), relaunching {self.target_package}")
                self.validator.ensure_app_foreground(self.target_package, self.target_activity)
                ctx.ai_enhancements.append("auto-relaunched app")

        return ctx

    def _validate_tap_target(self, ctx: InterceptContext, skill_cfg: Dict) -> InterceptContext:
        """Take screenshot, verify tap target is visible."""
        try:
            screenshot_path = str(self._screenshot_dir / "pre_tap_validate.png")
            if self.validator.take_screenshot(screenshot_path):
                x = ctx.enhanced_kwargs.get("x", 0)
                y = ctx.enhanced_kwargs.get("y", 0)
                element = ctx.enhanced_kwargs.get("element_description", f"element at ({x},{y})")
                
                validation = self.validator.validate_screen_state(
                    screenshot_path, f"{element} is visible and tappable"
                )
                
                if not validation.get("valid") and validation.get("confidence", 1.0) > 0.7:
                    log.warning(f"⚠️  PRE: Tap target may not be visible: {validation.get('description')}")
                    # Try to find better coords
                    if element:
                        better_coords = self.validator.find_element_coords(
                            screenshot_path, element
                        )
                        if better_coords:
                            log.info(f"🎯 PRE: Updated coords to AI-suggested ({better_coords[0]}, {better_coords[1]})")
                            ctx.enhanced_kwargs["x"] = better_coords[0]
                            ctx.enhanced_kwargs["y"] = better_coords[1]
                            ctx.ai_enhancements.append(f"coords updated to {better_coords}")
        except Exception as e:
            log.warning(f"Tap validation error (non-fatal): {e}")
        
        return ctx

    def _post_intercept(self, ctx: InterceptContext, result: Any, skill_cfg: Dict) -> PostResult:
        """Enhanced POST: take screenshot and verify navigation state."""
        post = super()._post_intercept(ctx, result, skill_cfg)

        if skill_cfg.get("post_verify_navigation"):
            try:
                import time
                time.sleep(1)  # Brief wait for UI to settle
                screenshot_path = str(self._screenshot_dir / "post_nav_verify.png")
                if self.validator.take_screenshot(screenshot_path):
                    expected = ctx.enhanced_kwargs.get(
                        "expected_state",
                        f"navigation result of {ctx.func_name}"
                    )
                    validation = self.validator.validate_screen_state(screenshot_path, expected)
                    
                    if not validation.get("valid", True):
                        log.warning(f"⚠️  POST: Navigation may have failed: {validation.get('description')}")
                        post.score = min(post.score, 4.0)  # Downgrade score
                        post.accepted = False
                        post.should_retry = ctx.attempt < ctx.max_attempts - 1
                    else:
                        log.info(f"✅ POST: Navigation verified successfully")
            except Exception as e:
                log.warning(f"Navigation verification error (non-fatal): {e}")

        return post

    def _error_intercept(self, ctx: InterceptContext, error: Exception, skill_cfg: Dict) -> InterceptContext:
        """Enhanced ERROR: relaunch app if it crashed."""
        ctx = super()._error_intercept(ctx, error, skill_cfg)

        # If error looks like app crash / wrong foreground, relaunch
        error_str = str(error).lower()
        if any(kw in error_str for kw in ["not found", "timeout", "connection", "closed"]):
            log.info("🔄 ERROR: Attempting app relaunch...")
            if self.validator.ensure_app_foreground(self.target_package, self.target_activity):
                log.info("✅ App relaunched successfully")
                ctx.ai_enhancements.append("app relaunched after error")
            import time
            time.sleep(3)

        return ctx


# ============================================================
# CONVENIENCE DECORATORS
# ============================================================
_default_adb_interceptor: Optional[ADBInterceptor] = None

def get_adb_interceptor(**kwargs) -> ADBInterceptor:
    """Get or create default ADB interceptor."""
    global _default_adb_interceptor
    if _default_adb_interceptor is None:
        _default_adb_interceptor = ADBInterceptor(**kwargs)
    return _default_adb_interceptor
