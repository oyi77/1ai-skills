"""Tests for autodroid-tiktok-agent — uses mocks, no real device required."""
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

CONFIG_PATH = Path(__file__).parent.parent / "config" / "tiktok_agent_config.json"


class TestTikTokAgentImport(unittest.TestCase):
    def test_import(self):
        """Agent imports without error (ADB not required)."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import tiktok_agent  # noqa: F401

    def test_package_constant(self):
        """PACKAGE constant is set correctly for TikTok."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import tiktok_agent
            self.assertEqual(tiktok_agent.PACKAGE, "com.ss.android.ugc.trill")


class TestAIInterceptOptional(unittest.TestCase):
    def test_ai_intercept_decorator_passthrough(self):
        """_ai_intercept returns function unchanged when interceptor is None."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import tiktok_agent
            original_enabled = tiktok_agent.AI_INTERCEPT_ENABLED
            original_interceptor = tiktok_agent._interceptor
            try:
                tiktok_agent.AI_INTERCEPT_ENABLED = False
                tiktok_agent._interceptor = None

                @tiktok_agent._ai_intercept(skill_type="postbridge_post")
                def dummy_fn(x):
                    return x + 100

                self.assertEqual(dummy_fn(5), 105)
            finally:
                tiktok_agent.AI_INTERCEPT_ENABLED = original_enabled
                tiktok_agent._interceptor = original_interceptor

    def test_ai_intercept_flag_is_bool(self):
        """AI_INTERCEPT_ENABLED is a boolean."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import tiktok_agent
            self.assertIsInstance(tiktok_agent.AI_INTERCEPT_ENABLED, bool)


class TestConfigLoads(unittest.TestCase):
    def test_config_file_exists(self):
        """Config file exists."""
        self.assertTrue(CONFIG_PATH.exists(), f"Config not found: {CONFIG_PATH}")

    def test_config_valid_json(self):
        """Config is valid JSON."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_config_required_keys(self):
        """Config has all required keys."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        for key in ("device_serial", "adb_port", "screenshot_dir", "ai_intercept", "max_retries"):
            self.assertIn(key, data, f"Missing key: {key}")

    def test_config_ai_enhance_keys(self):
        """Config has AI enhancement keys."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIn("ai_enhance_captions", data)
        self.assertIn("ai_enhance_hashtags", data)


class TestCmdUploadWrapped(unittest.TestCase):
    def test_cmd_upload_is_callable(self):
        """cmd_upload remains callable after decorator."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import tiktok_agent
            self.assertTrue(callable(tiktok_agent.cmd_upload))

    def test_cmd_upload_returns_error_without_device(self):
        """cmd_upload returns ok:false when no device connected."""
        with patch("subprocess.run", return_value=MagicMock(returncode=1, stdout=b"", stderr=b"error")):
            import tiktok_agent
            with patch.object(tiktok_agent, "get_connected_devices", return_value=[]):
                result = tiktok_agent.cmd_upload("/tmp/fake.mp4", caption="#test")
                self.assertIn("ok", result)
                self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
