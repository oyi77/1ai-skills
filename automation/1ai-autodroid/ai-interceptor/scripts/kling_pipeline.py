"""
kling_pipeline.py — End-to-End Kling Video Generation Pipeline

Orchestrates the full pipeline:
  1. Select best Kling account (KlingAccountManager)
  2. Enhance prompt (AIInterceptor PRE hooks)
  3. Generate video (KlingProvider)
  4. Remove watermark (VideoEnhancer)
  5. AI-enhance quality (VideoEnhancer)
  6. Score output (AIInterceptor POST hooks)
  7. Return polished result
"""

from __future__ import annotations

import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Ensure parent scripts/ directory is on path for sibling imports
_SCRIPTS_DIR = Path(__file__).parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

_LOG_DIR = Path(os.path.expanduser("~/.openclaw/workspace/logs"))
_LOG_DIR.mkdir(parents=True, exist_ok=True)


class KlingPipeline:
    """
    Full Kling AI video generation pipeline.

    Combines:
        - KlingAccountManager  — multi-account credit pool & rotation
        - AIInterceptor        — PRE/POST hook middleware
        - KlingProvider        — Kling API client
        - VideoEnhancer        — watermark removal + upscaling

    Each stage is fail-safe: if it errors, the pipeline continues
    with the result of the previous stage.

    Args:
        config: Optional configuration dict with keys:
            accounts_file   (str)  — path to kling_accounts.json
            output_dir      (str)  — directory for generated videos
            min_credits     (float)— minimum credits required (default 60)
            poll_interval   (int)  — seconds between API polls (default 10)
            max_wait        (int)  — max wait for generation in seconds (default 600)
            repo_path       (str)  — path to KLing-Video-WatermarkRemover-Enhancer
            weights_dir     (str)  — path to model weights directory
            interceptor_config (str) — path to ai_interceptor_config.json
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._output_dir = Path(self._config.get("output_dir", "/tmp/kling_pipeline_output"))
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._min_credits = float(self._config.get("min_credits", 60.0))

        # Lazy-loaded components
        self._account_manager: Optional[Any] = None
        self._provider: Optional[Any] = None
        self._enhancer: Optional[Any] = None
        self._interceptor: Optional[Any] = None

    # ------------------------------------------------------------------
    # Component initialisation (lazy, fail-safe)
    # ------------------------------------------------------------------

    def _get_account_manager(self) -> Optional[Any]:
        if self._account_manager is not None:
            return self._account_manager
        try:
            from kling_account_manager import KlingAccountManager
            accts_file = self._config.get("accounts_file")
            self._account_manager = KlingAccountManager(accounts_file=accts_file)
            return self._account_manager
        except Exception as exc:  # noqa: BLE001
            logger.warning("KlingAccountManager unavailable: %s", exc)
            return None

    def _get_provider(self, account: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        try:
            from providers.kling_provider import KlingProvider
            cfg: Dict[str, Any] = {
                "poll_interval": self._config.get("poll_interval", 10),
                "max_wait": self._config.get("max_wait", 600),
                "output_dir": str(self._output_dir),
            }
            if account:
                if account.get("cookie"):
                    cfg["cookie"] = account["cookie"]
                elif account.get("api_key"):
                    cfg["api_key"] = account["api_key"]
            self._provider = KlingProvider(config=cfg)
            return self._provider
        except Exception as exc:  # noqa: BLE001
            logger.warning("KlingProvider unavailable: %s", exc)
            return None

    def _get_enhancer(self) -> Optional[Any]:
        if self._enhancer is not None:
            return self._enhancer
        try:
            from video_enhancer import VideoEnhancer
            self._enhancer = VideoEnhancer(
                repo_path=self._config.get("repo_path"),
                weights_dir=self._config.get("weights_dir"),
            )
            return self._enhancer
        except Exception as exc:  # noqa: BLE001
            logger.warning("VideoEnhancer unavailable: %s", exc)
            return None

    def _get_interceptor(self) -> Optional[Any]:
        if self._interceptor is not None:
            return self._interceptor
        try:
            from ai_interceptor import AIInterceptor
            interceptor_config = self._config.get(
                "interceptor_config",
                str(Path(__file__).parent.parent / "config" / "ai_interceptor_config.json"),
            )
            self._interceptor = AIInterceptor(config_path=interceptor_config)
            return self._interceptor
        except Exception as exc:  # noqa: BLE001
            logger.debug("AIInterceptor unavailable: %s", exc)
            return None

    # ------------------------------------------------------------------
    # Main pipeline
    # ------------------------------------------------------------------

    def generate(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        remove_watermark: bool = True,
        enhance_quality: bool = True,
        duration: str = "5",
        mode: str = "std",
        aspect_ratio: str = "16:9",
    ) -> Dict[str, Any]:
        """
        Run the full Kling generation pipeline.

        Args:
            prompt:           Text prompt for video generation.
            image_path:       Path to input image for image-to-video (optional).
            remove_watermark: Whether to remove Kling watermark (default True).
            enhance_quality:  Whether to AI-enhance the output (default True).
            duration:         Video duration "5" or "10" seconds.
            mode:             "std" or "pro".
            aspect_ratio:     e.g. "16:9", "9:16", "1:1".

        Returns:
            dict with keys:
                success          (bool)
                video_path       (str)   — final processed video path
                original_path    (str)   — raw Kling output
                prompt_original  (str)
                prompt_enhanced  (str)
                credits_used     (int)
                account_used     (str)
                quality_score    (float)
                processing_time_s (float)
                error            (str|None)
        """
        start_time = time.time()
        result: Dict[str, Any] = {
            "success": False,
            "video_path": None,
            "original_path": None,
            "prompt_original": prompt,
            "prompt_enhanced": prompt,
            "credits_used": 0,
            "account_used": "",
            "quality_score": 0.0,
            "processing_time_s": 0.0,
            "error": None,
        }

        try:
            # ── Step 1: Select best account ─────────────────────────────
            account = None
            mgr = self._get_account_manager()
            if mgr:
                account = mgr.get_best_account(min_credits=self._min_credits)
                if account:
                    result["account_used"] = account.get("email", "unknown")
                    logger.info("[Pipeline] Using account: %s (%.1f credits)", account.get("email"), account.get("credits", 0))
                else:
                    logger.warning("[Pipeline] No account with sufficient credits — trying anyway.")

            # ── Step 2: Enhance prompt via AIInterceptor ────────────────
            enhanced_prompt = prompt
            interceptor = self._get_interceptor()
            if interceptor:
                try:
                    pre_result = interceptor.pre_process(
                        {"prompt": prompt, "task_type": "text2video" if not image_path else "image2video"}
                    )
                    enhanced_prompt = pre_result.get("prompt", prompt) if isinstance(pre_result, dict) else prompt
                    logger.info("[Pipeline] Prompt enhanced by interceptor.")
                except Exception as exc:  # noqa: BLE001
                    logger.warning("[Pipeline] Interceptor PRE hook failed: %s — using original prompt.", exc)
            result["prompt_enhanced"] = enhanced_prompt

            # ── Step 3: Generate video ──────────────────────────────────
            provider = self._get_provider(account)
            if not provider:
                result["error"] = "KlingProvider could not be initialised."
                return self._finalise(result, start_time)

            task_type = "text2video" if not image_path else "image2video"
            gen_kwargs: Dict[str, Any] = {
                "prompt": enhanced_prompt,
                "duration": duration,
                "mode": mode,
                "aspect_ratio": aspect_ratio,
            }
            if image_path:
                gen_kwargs["image_path"] = image_path

            logger.info("[Pipeline] Generating %s...", task_type)
            gen_result = provider.generate(task_type, **gen_kwargs)

            if not gen_result.get("success"):
                result["error"] = gen_result.get("error", "Generation failed.")
                return self._finalise(result, start_time)

            raw_video = gen_result.get("output", "")
            result["original_path"] = raw_video
            result["credits_used"] = gen_result.get("cost", 0)
            current_video = raw_video
            logger.info("[Pipeline] Raw video: %s", raw_video)

            # ── Step 4 & 5: Video enhancement ──────────────────────────
            if remove_watermark or enhance_quality:
                enhancer = self._get_enhancer()
                if enhancer:
                    logger.info("[Pipeline] Running VideoEnhancer (wm=%s enhance=%s)...", remove_watermark, enhance_quality)
                    final_path = str(self._output_dir / f"final_{int(time.time())}.mp4")
                    current_video = enhancer.process(
                        current_video,
                        output_path=final_path,
                        remove_wm=remove_watermark,
                        enhance=enhance_quality,
                    )
                else:
                    logger.warning("[Pipeline] VideoEnhancer unavailable — skipping enhancement.")

            result["video_path"] = current_video

            # ── Step 6: Score output via AIInterceptor ──────────────────
            quality_score = 0.0
            if interceptor:
                try:
                    post_result = interceptor.post_process(
                        {"output_path": current_video, "prompt": enhanced_prompt}
                    )
                    quality_score = float(post_result.get("quality_score", 0.0)) if isinstance(post_result, dict) else 0.0
                    logger.info("[Pipeline] Quality score: %.2f", quality_score)
                except Exception as exc:  # noqa: BLE001
                    logger.debug("[Pipeline] Interceptor POST hook failed: %s", exc)
            result["quality_score"] = quality_score

            # ── Update account credits ──────────────────────────────────
            if mgr and account:
                new_credits = account.get("credits", 0) - result["credits_used"]
                mgr.rotate_if_low(new_credits, threshold=self._min_credits)

            result["success"] = True

        except Exception as exc:  # noqa: BLE001
            logger.exception("[Pipeline] Unexpected error: %s", exc)
            result["error"] = str(exc)

        return self._finalise(result, start_time)

    def _finalise(self, result: Dict[str, Any], start_time: float) -> Dict[str, Any]:
        """Stamp processing time and log the result."""
        result["processing_time_s"] = round(time.time() - start_time, 2)
        self._log_result(result)
        status = "✅ SUCCESS" if result["success"] else f"❌ FAILED ({result.get('error', '')})"
        logger.info("[Pipeline] Done in %.1fs — %s", result["processing_time_s"], status)
        return result

    def _log_result(self, result: Dict[str, Any]) -> None:
        """Append result to pipeline log."""
        log_file = _LOG_DIR / "kling_pipeline.log"
        try:
            with open(log_file, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    **result,
                }) + "\n")
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def text_to_video(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """Shorthand for text-to-video generation."""
        return self.generate(prompt=prompt, image_path=None, **kwargs)

    def image_to_video(self, prompt: str, image_path: str, **kwargs: Any) -> Dict[str, Any]:
        """Shorthand for image-to-video generation."""
        return self.generate(prompt=prompt, image_path=image_path, **kwargs)

    def __repr__(self) -> str:
        return f"<KlingPipeline output_dir={self._output_dir!r} min_credits={self._min_credits}>"
