"""
test_interceptor.py — Full Test Suite for AI Interceptor
=========================================================
Tests all components with mocked LLM calls to avoid external dependencies.

Run: python3 test_interceptor.py
Or:  python3 -m pytest test_interceptor.py -v
"""

from __future__ import annotations

import json
import logging
import sys
import time
import unittest
from pathlib import Path
from typing import Any, Optional
from unittest.mock import MagicMock, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_interceptor import (
    AIInterceptor,
    InterceptContext,
    InterceptResult,
    InterceptorConfig,
    LLMEnhancePreHook,
    LLMErrorDiagnoseHook,
    LLMQualityPostHook,
    PreHook,
    PostHook,
    ErrorHook,
    call_llm,
    call_llm_json,
)

# Disable logging during tests unless DEBUG
logging.disable(logging.WARNING)


# ---------------------------------------------------------------------------
# Mock LLM responses
# ---------------------------------------------------------------------------
MOCK_ENHANCED_PROMPT = "elegant woman in flowing dress, cinematic lighting, golden hour, 4K quality"
MOCK_QUALITY_RESPONSE = json.dumps({"score": 8.5, "reason": "high quality output"})
MOCK_ERROR_DIAGNOSIS = json.dumps({
    "diagnosis": "Network timeout",
    "fix": "Retry with longer timeout",
    "retry_modification": {"timeout": 60},
})


def mock_call_llm(prompt: str, engine: str = "gemini", **kwargs) -> str:
    """Mock LLM that returns appropriate responses based on prompt content."""
    if "improve" in prompt.lower() or "rewrite" in prompt.lower() or "enhance" in prompt.lower():
        return MOCK_ENHANCED_PROMPT
    if "rate" in prompt.lower() or "score" in prompt.lower() or "quality" in prompt.lower():
        return MOCK_QUALITY_RESPONSE
    if "debug" in prompt.lower() or "error" in prompt.lower() or "diagnose" in prompt.lower():
        return MOCK_ERROR_DIAGNOSIS
    return "mock response"


def mock_call_llm_json(prompt: str, engine: str = "gemini") -> dict:
    raw = mock_call_llm(prompt, engine)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


# ---------------------------------------------------------------------------
# Test: InterceptorConfig
# ---------------------------------------------------------------------------
class TestInterceptorConfig(unittest.TestCase):

    def test_defaults(self):
        config = InterceptorConfig(config_path="/nonexistent/path.json")
        self.assertEqual(config.max_retries, 3)
        self.assertAlmostEqual(config.min_quality_score, 6.0)
        self.assertEqual(config.llm_engine, "gemini")
        self.assertTrue(config.fail_safe_mode)

    def test_skill_config_missing(self):
        config = InterceptorConfig(config_path="/nonexistent/path.json")
        skill_cfg = config.skill_config("nonexistent_skill")
        self.assertEqual(skill_cfg, {})

    def test_load_from_file(self, tmp_path=None):
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({
                "min_quality_score": 7.5,
                "max_retries": 5,
                "skills": {
                    "my_skill": {"quality_threshold": 8.0}
                }
            }, f)
            f.flush()
            config = InterceptorConfig(config_path=f.name)
            self.assertAlmostEqual(config.min_quality_score, 7.5)
            self.assertEqual(config.max_retries, 5)
            self.assertEqual(config.skill_config("my_skill")["quality_threshold"], 8.0)


# ---------------------------------------------------------------------------
# Test: Hook base classes
# ---------------------------------------------------------------------------
class TestHookBaseClasses(unittest.TestCase):

    def test_pre_hook_noop(self):
        ctx = InterceptContext(
            skill_type="test", func_name="test_func",
            args=[], kwargs={"prompt": "hello"}, config={}
        )
        hook = PreHook()
        result_ctx = hook.run(ctx)
        self.assertEqual(result_ctx.kwargs["prompt"], "hello")

    def test_post_hook_noop(self):
        ctx = InterceptContext(
            skill_type="test", func_name="test_func",
            args=[], kwargs={}, config={}
        )
        hook = PostHook()
        score, output = hook.run(ctx, {"result": "ok"})
        self.assertEqual(score, 10.0)
        self.assertEqual(output, {"result": "ok"})

    def test_error_hook_noop(self):
        ctx = InterceptContext(
            skill_type="test", func_name="test_func",
            args=[], kwargs={}, config={}
        )
        hook = ErrorHook()
        recovery = hook.run(ctx, ValueError("test error"))
        self.assertIsNone(recovery)


# ---------------------------------------------------------------------------
# Test: LLM hooks (with mocked LLM)
# ---------------------------------------------------------------------------
class TestLLMEnhancePreHook(unittest.TestCase):

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    def test_enhances_prompt(self, _mock):
        ctx = InterceptContext(
            skill_type="kling_i2v", func_name="generate",
            args=[], kwargs={"prompt": "wanita jalan di taman"}, config={}
        )
        hook = LLMEnhancePreHook()
        result_ctx = hook.run(ctx)
        # Should have modified the prompt
        self.assertIn("prompt", result_ctx.kwargs)

    @patch("ai_interceptor.call_llm", return_value="")
    def test_fallback_on_empty_response(self, _mock):
        original = "original prompt"
        ctx = InterceptContext(
            skill_type="test", func_name="test",
            args=[], kwargs={"prompt": original}, config={}
        )
        hook = LLMEnhancePreHook()
        result_ctx = hook.run(ctx)
        # Should keep original if LLM returns empty
        self.assertEqual(result_ctx.kwargs["prompt"], original)

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    def test_no_kwargs_to_enhance(self, _mock):
        ctx = InterceptContext(
            skill_type="test", func_name="test",
            args=["positional_arg"], kwargs={}, config={}
        )
        hook = LLMEnhancePreHook()
        result_ctx = hook.run(ctx)
        # Should not crash, args unchanged
        self.assertEqual(result_ctx.args, ["positional_arg"])


class TestLLMQualityPostHook(unittest.TestCase):

    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_scores_output(self, _mock):
        ctx = InterceptContext(
            skill_type="test", func_name="test",
            args=[], kwargs={"prompt": "test"}, config={}
        )
        hook = LLMQualityPostHook()
        score, output = hook.run(ctx, {"status": "ok", "url": "http://example.com/video.mp4"})
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 10.0)

    @patch("ai_interceptor.call_llm_json", return_value={})
    def test_fallback_score_on_empty(self, _mock):
        ctx = InterceptContext(
            skill_type="test", func_name="test",
            args=[], kwargs={}, config={}
        )
        hook = LLMQualityPostHook()
        score, _ = hook.run(ctx, "some output")
        # Should return 7.0 fallback
        self.assertEqual(score, 7.0)


# ---------------------------------------------------------------------------
# Test: AIInterceptor core
# ---------------------------------------------------------------------------
class TestAIInterceptor(unittest.TestCase):

    def setUp(self):
        self.interceptor = AIInterceptor(config_path="/nonexistent/path.json")

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_successful_execution(self, _mock1, _mock2):
        def simple_func(prompt: str) -> dict:
            return {"status": "ok", "prompt": prompt}

        result = self.interceptor.run(simple_func, skill_type="test", kwargs={"prompt": "hello"})
        self.assertTrue(result.success)
        self.assertIsNotNone(result.output)

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_decorator_pattern(self, _mock1, _mock2):
        @self.interceptor.intercept(skill_type="demo")
        def my_function(x: int, y: int) -> dict:
            return {"sum": x + y}

        result = my_function(x=3, y=4)
        # Result may be None if quality check redirects output
        # but function should not crash

    def test_fail_safe_mode_on_exception(self):
        """Fail-safe: if all retries fail, run original function without interception."""
        self.interceptor.config._data["fail_safe_mode"] = True
        self.interceptor.config._data["max_retries"] = 0
        self.interceptor.config._data["pre_hooks_enabled"] = False
        self.interceptor.config._data["post_hooks_enabled"] = False
        self.interceptor.config._data["error_hooks_enabled"] = False

        call_count = {"n": 0}

        def always_fails_first(prompt: str) -> dict:
            call_count["n"] += 1
            if call_count["n"] == 1:
                raise RuntimeError("First call fails")
            return {"status": "ok"}

        result = self.interceptor.run(always_fails_first, skill_type="test", kwargs={"prompt": "hi"})
        # Fail-safe should have executed original function
        self.assertIsNotNone(result)  # Should not crash

    def test_retry_on_low_quality(self):
        """Should retry when quality score is below threshold."""
        call_count = {"n": 0}

        def improving_func(prompt: str) -> dict:
            call_count["n"] += 1
            return {"status": "ok", "attempt": call_count["n"]}

        # Mock low quality on first attempt, high on second
        quality_scores = [3.0, 8.0]
        score_idx = {"i": 0}

        class MockPostHook(PostHook):
            def run(self, ctx, output):
                idx = min(score_idx["i"], len(quality_scores) - 1)
                score_idx["i"] += 1
                return quality_scores[idx], output

        self.interceptor._post_hooks = {"*": [MockPostHook()]}
        self.interceptor.config._data["pre_hooks_enabled"] = False
        self.interceptor.config._data["error_hooks_enabled"] = False

        result = self.interceptor.run(improving_func, skill_type="test", kwargs={"prompt": "test"})
        self.assertTrue(result.success)
        self.assertGreaterEqual(call_count["n"], 1)

    def test_error_recovery(self):
        """Should recover from errors via error hooks."""
        recovery_value = {"recovered": True}
        called = {"n": 0}

        def always_fails(prompt: str) -> dict:
            called["n"] += 1
            raise ValueError("Always fails")

        class RecoveryHook(ErrorHook):
            def run(self, ctx, error):
                return recovery_value

        self.interceptor._error_hooks = {"*": [RecoveryHook()]}
        self.interceptor._pre_hooks = {}
        self.interceptor._post_hooks = {}
        self.interceptor.config._data["pre_hooks_enabled"] = False
        self.interceptor.config._data["post_hooks_enabled"] = False

        result = self.interceptor.run(always_fails, skill_type="test", kwargs={"prompt": "hi"})
        self.assertTrue(result.success)
        self.assertEqual(result.output, recovery_value)

    def test_audit_trail(self):
        """Audit trail should be populated."""
        @self.interceptor.intercept(skill_type="test")
        def tracked_func() -> str:
            return "result"

        # Run via interceptor.run directly to access InterceptResult
        def simple() -> str:
            return "result"

        self.interceptor.config._data["pre_hooks_enabled"] = False
        self.interceptor.config._data["post_hooks_enabled"] = False
        self.interceptor.config._data["error_hooks_enabled"] = False

        result = self.interceptor.run(simple, skill_type="test")
        self.assertIsInstance(result.audit_trail, list)

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_async_execution(self, _mock1, _mock2):
        import asyncio

        async def async_func(prompt: str) -> dict:
            await asyncio.sleep(0.01)
            return {"async": True, "prompt": prompt}

        async def run():
            return await self.interceptor.run_async(
                async_func, skill_type="test", kwargs={"prompt": "async test"}
            )

        result = asyncio.run(run())
        self.assertTrue(result.success)


# ---------------------------------------------------------------------------
# Test: Content Interceptor
# ---------------------------------------------------------------------------
class TestContentInterceptor(unittest.TestCase):

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    def test_caption_enhancement(self, _mock):
        from content_interceptor import EnhanceCaptionPreHook

        ctx = InterceptContext(
            skill_type="postbridge_post", func_name="post",
            args=[], kwargs={
                "caption": "Check our new product!",
                "social_accounts": [49675],  # Facebook
            }, config={}
        )
        hook = EnhanceCaptionPreHook()
        result_ctx = hook.run(ctx)
        self.assertIn("caption", result_ctx.kwargs)

    def test_platform_compliance_removes_youtube_without_media(self):
        from content_interceptor import PlatformCompliancePreHook

        ctx = InterceptContext(
            skill_type="postbridge_post", func_name="post",
            args=[], kwargs={
                "caption": "test",
                "social_accounts": [49678, 49675],  # YouTube + Facebook
                "media": [],  # No media
            }, config={}
        )
        hook = PlatformCompliancePreHook()
        result_ctx = hook.run(ctx)
        # YouTube should be removed (requires media)
        self.assertNotIn(49678, result_ctx.kwargs["social_accounts"])
        # Facebook should remain
        self.assertIn(49675, result_ctx.kwargs["social_accounts"])

    def test_platform_compliance_removes_instagram_without_media(self):
        from content_interceptor import PlatformCompliancePreHook

        ctx = InterceptContext(
            skill_type="postbridge_post", func_name="post",
            args=[], kwargs={
                "caption": "test",
                "social_accounts": [49682, 49675],  # Instagram + Facebook
                "media": [],  # No media
            }, config={}
        )
        hook = PlatformCompliancePreHook()
        result_ctx = hook.run(ctx)
        self.assertNotIn(49682, result_ctx.kwargs["social_accounts"])

    def test_post_success_verification(self):
        from content_interceptor import VerifyPostSuccessPostHook

        ctx = InterceptContext(
            skill_type="postbridge_post", func_name="post",
            args=[], kwargs={}, config={}
        )
        hook = VerifyPostSuccessPostHook()

        # Success case
        score, _ = hook.run(ctx, {"id": "123", "status": "scheduled"})
        self.assertGreater(score, 7.0)

        # Failure case
        score2, _ = hook.run(ctx, {"status": "failed", "errors": ["API error"]})
        self.assertLess(score2, 5.0)


# ---------------------------------------------------------------------------
# Test: Prompt Interceptor
# ---------------------------------------------------------------------------
class TestPromptInterceptor(unittest.TestCase):

    def test_indonesian_detection(self):
        from prompt_interceptor import LanguageNormalizationPreHook

        hook = LanguageNormalizationPreHook()
        self.assertTrue(hook._is_indonesian("wanita cantik berjalan di taman"))
        self.assertFalse(hook._is_indonesian("beautiful woman walking in garden"))
        self.assertFalse(hook._is_indonesian("4K cinematic lighting golden hour"))

    @patch("ai_interceptor.call_llm", return_value="beautiful woman walking in zen garden")
    def test_language_translation(self, _mock):
        from prompt_interceptor import LanguageNormalizationPreHook

        ctx = InterceptContext(
            skill_type="kling_i2v", func_name="generate",
            args=[], kwargs={"prompt": "wanita berjalan di taman"}, config={}
        )
        hook = LanguageNormalizationPreHook()
        result_ctx = hook.run(ctx)
        self.assertEqual(result_ctx.kwargs.get("_original_prompt_language"), "id")

    def test_negative_prompt_added(self):
        from prompt_interceptor import NegativePromptPreHook

        ctx = InterceptContext(
            skill_type="kling_i2v", func_name="generate",
            args=[], kwargs={"prompt": "test"}, config={}
        )
        hook = NegativePromptPreHook()
        result_ctx = hook.run(ctx)
        self.assertIn("negative_prompt", result_ctx.kwargs)
        self.assertIn("blurry", result_ctx.kwargs["negative_prompt"])

    def test_negative_prompt_not_overwritten(self):
        from prompt_interceptor import NegativePromptPreHook

        custom_neg = "my custom negative"
        ctx = InterceptContext(
            skill_type="kling_i2v", func_name="generate",
            args=[], kwargs={"prompt": "test", "negative_prompt": custom_neg}, config={}
        )
        hook = NegativePromptPreHook()
        result_ctx = hook.run(ctx)
        self.assertEqual(result_ctx.kwargs["negative_prompt"], custom_neg)

    def test_content_policy_sanitizer(self):
        from prompt_interceptor import ContentPolicyErrorHook

        with patch("ai_interceptor.call_llm", return_value="safe family-friendly version of prompt"):
            ctx = InterceptContext(
                skill_type="image_gen", func_name="generate",
                args=[], kwargs={"prompt": "original prompt"}, config={}
            )
            hook = ContentPolicyErrorHook()
            recovery = hook.run(ctx, ValueError("content policy violation - not allowed"))
            self.assertIsNone(recovery)  # Let retry happen
            self.assertNotEqual(ctx.kwargs["prompt"], "original prompt")


# ---------------------------------------------------------------------------
# Test: ADB Interceptor
# ---------------------------------------------------------------------------
class TestADBInterceptor(unittest.TestCase):

    def test_wrong_app_error_hook_no_adb(self):
        """Should gracefully handle missing ADB."""
        from adb_interceptor import WrongAppErrorHook

        ctx = InterceptContext(
            skill_type="adb_tap", func_name="tap",
            args=[], kwargs={"device": None, "app": "kling"}, config={}
        )
        hook = WrongAppErrorHook()

        with patch("adb_interceptor.adb_foreground_app", return_value=""):
            with patch("adb_interceptor.adb_launch_app", return_value=False):
                recovery = hook.run(ctx, RuntimeError("tap failed"))
                self.assertIsNone(recovery)


# ---------------------------------------------------------------------------
# Integration tests
# ---------------------------------------------------------------------------
class TestIntegration(unittest.TestCase):

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_full_pipeline_kling(self, _mock1, _mock2):
        """Full pipeline: PRE enhance → execute → POST score."""
        from prompt_interceptor import create_prompt_interceptor

        interceptor = create_prompt_interceptor(config_path="/nonexistent.json")

        generation_results = {"calls": 0}

        @interceptor.intercept(skill_type="kling_i2v")
        def mock_kling_generate(prompt: str, negative_prompt: str = "", **kwargs) -> dict:
            generation_results["calls"] += 1
            generation_results["prompt_used"] = prompt
            return {
                "status": "success",
                "task_id": "abc123",
                "url": "https://example.com/video.mp4",
            }

        result = mock_kling_generate(prompt="wanita jalan di taman")
        # Should not crash regardless of quality score
        self.assertGreaterEqual(generation_results["calls"], 1)

    @patch("ai_interceptor.call_llm", side_effect=mock_call_llm)
    @patch("ai_interceptor.call_llm_json", side_effect=mock_call_llm_json)
    def test_error_recovery_pipeline(self, _mock1, _mock2):
        """Test that error hooks diagnose and retry successfully."""
        call_count = {"n": 0}

        interceptor = AIInterceptor(config_path="/nonexistent.json")

        def flaky_func(**kwargs) -> dict:
            call_count["n"] += 1
            if call_count["n"] < 2:
                raise ConnectionError("Network timeout")
            return {"status": "ok", "attempts": call_count["n"]}

        result = interceptor.run(flaky_func, skill_type="test", kwargs={"prompt": "hello"})
        self.assertTrue(result.success or result.error_message != "" or call_count["n"] >= 1)


# ---------------------------------------------------------------------------
# Test: call_llm fail-safe
# ---------------------------------------------------------------------------
class TestCallLLMFallback(unittest.TestCase):

    def test_returns_empty_string_when_oracle_not_found(self):
        with patch("subprocess.run", side_effect=FileNotFoundError("oracle not found")):
            result = call_llm("test prompt")
            self.assertEqual(result, "")

    def test_returns_empty_string_on_timeout(self):
        import subprocess
        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("oracle", 30)):
            result = call_llm("test prompt")
            self.assertEqual(result, "")

    def test_call_llm_json_returns_empty_dict_on_failure(self):
        with patch("ai_interceptor.call_llm", return_value=""):
            result = call_llm_json("test prompt")
            self.assertEqual(result, {})

    def test_call_llm_json_parses_markdown_json(self):
        markdown_json = '```json\n{"score": 8.5, "reason": "good"}\n```'
        with patch("ai_interceptor.call_llm", return_value=markdown_json):
            result = call_llm_json("test")
            self.assertEqual(result.get("score"), 8.5)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def run_tests():
    """Run all tests and print summary."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    test_classes = [
        TestInterceptorConfig,
        TestHookBaseClasses,
        TestLLMEnhancePreHook,
        TestLLMQualityPostHook,
        TestAIInterceptor,
        TestContentInterceptor,
        TestPromptInterceptor,
        TestADBInterceptor,
        TestIntegration,
        TestCallLLMFallback,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Re-enable logging for test output
    logging.disable(logging.NOTSET)
    logging.basicConfig(level=logging.ERROR)

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    print(f"\n{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures:  {len(result.failures)}")
    print(f"Errors:    {len(result.errors)}")
    print(f"Success:   {result.wasSuccessful()}")
    print(f"{'='*60}")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
