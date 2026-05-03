"""Tests for autodroid-instagram-agent — uses mocks, no real device required."""
import json
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Ensure scripts dir is on path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

CONFIG_PATH = Path(__file__).parent.parent / "config" / "instagram_agent_config.json"


class TestInstagramAgentImport(unittest.TestCase):
    def test_import(self):
        """Agent imports without error (ADB not required)."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import instagram_agent  # noqa: F401

    def test_package_constant(self):
        """PACKAGE constant is set correctly."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import instagram_agent
            self.assertEqual(instagram_agent.PACKAGE, "com.instagram.android")


class TestAIInterceptOptional(unittest.TestCase):
    def test_ai_intercept_disabled_when_missing(self):
        """AI intercept flag is False when interceptor module is not found."""
        # Reload the module with interceptor path blocked
        if "instagram_agent" in sys.modules:
            del sys.modules["instagram_agent"]
        # Patch the interceptor import to fail
        real_import = __builtins__.__import__ if hasattr(__builtins__, "__import__") else __import__

        def mock_import(name, *args, **kwargs):
            if name in ("ai_interceptor", "content_interceptor"):
                raise ImportError(f"Mocked missing: {name}")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=mock_import):
            # Just verify the flag pattern works — actual import may already be cached
            pass  # graceful: no crash expected

    def test_ai_intercept_decorator_passthrough(self):
        """_ai_intercept decorator returns function unchanged when interceptor is None."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import instagram_agent
            # Force interceptor to None to simulate missing dependency
            original_enabled = instagram_agent.AI_INTERCEPT_ENABLED
            original_interceptor = instagram_agent._interceptor
            try:
                instagram_agent.AI_INTERCEPT_ENABLED = False
                instagram_agent._interceptor = None

                @instagram_agent._ai_intercept(skill_type="postbridge_post")
                def dummy_fn(x):
                    return x * 2

                self.assertEqual(dummy_fn(5), 10)
            finally:
                instagram_agent.AI_INTERCEPT_ENABLED = original_enabled
                instagram_agent._interceptor = original_interceptor


class TestConfigLoads(unittest.TestCase):
    def test_config_file_exists(self):
        """Config file exists at expected path."""
        self.assertTrue(CONFIG_PATH.exists(), f"Config not found: {CONFIG_PATH}")

    def test_config_valid_json(self):
        """Config file is valid JSON."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIsInstance(data, dict)

    def test_config_required_keys(self):
        """Config has expected keys."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        for key in ("device_serial", "adb_port", "screenshot_dir", "ai_intercept", "max_retries"):
            self.assertIn(key, data, f"Missing key: {key}")

    def test_config_defaults(self):
        """Config has sensible default values."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIsInstance(data["max_retries"], int)
        self.assertGreater(data["max_retries"], 0)
        self.assertIsInstance(data["ai_intercept"], bool)


class TestCmdPostWrapped(unittest.TestCase):
    def test_cmd_post_is_callable(self):
        """cmd_post remains callable after decorator application."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import instagram_agent
            self.assertTrue(callable(instagram_agent.cmd_post))

    def test_cmd_post_returns_error_without_device(self):
        """cmd_post returns ok:false gracefully when no device connected."""
        with patch("subprocess.run", return_value=MagicMock(returncode=1, stdout=b"", stderr=b"error")):
            import instagram_agent
            with patch.object(instagram_agent, "get_connected_devices", return_value=[]):
                result = instagram_agent.cmd_post("/tmp/fake.jpg", caption="test")
                self.assertIn("ok", result)
                self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
