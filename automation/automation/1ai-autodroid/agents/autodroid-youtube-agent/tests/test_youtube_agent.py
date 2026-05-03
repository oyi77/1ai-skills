"""Tests for autodroid-youtube-agent — uses mocks, no real device required."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

CONFIG_PATH = Path(__file__).parent.parent / "config" / "youtube_agent_config.json"


class TestYouTubeAgentImport(unittest.TestCase):
    def test_import(self):
        """Agent imports without error (ADB not required)."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import youtube_agent  # noqa: F401

    def test_package_constant(self):
        """PACKAGE constant is set correctly for YouTube."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import youtube_agent
            self.assertEqual(youtube_agent.PACKAGE, "com.google.android.youtube")


class TestAIInterceptOptional(unittest.TestCase):
    def test_ai_intercept_decorator_passthrough(self):
        """_ai_intercept returns function unchanged when interceptor is None."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import youtube_agent
            original_enabled = youtube_agent.AI_INTERCEPT_ENABLED
            original_interceptor = youtube_agent._interceptor
            try:
                youtube_agent.AI_INTERCEPT_ENABLED = False
                youtube_agent._interceptor = None

                @youtube_agent._ai_intercept(skill_type="content_gen")
                def dummy_fn(title):
                    return f"Enhanced: {title}"

                self.assertEqual(dummy_fn("My Video"), "Enhanced: My Video")
            finally:
                youtube_agent.AI_INTERCEPT_ENABLED = original_enabled
                youtube_agent._interceptor = original_interceptor

    def test_ai_intercept_flag_is_bool(self):
        """AI_INTERCEPT_ENABLED is a boolean."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import youtube_agent
            self.assertIsInstance(youtube_agent.AI_INTERCEPT_ENABLED, bool)


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

    def test_config_tap_delay(self):
        """Config tap_delay_ms is a positive integer."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIn("tap_delay_ms", data)
        self.assertGreater(data["tap_delay_ms"], 0)


class TestCmdPlayWrapped(unittest.TestCase):
    def test_cmd_play_is_callable(self):
        """cmd_play remains callable after decorator."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import youtube_agent
            self.assertTrue(callable(youtube_agent.cmd_play))

    def test_cmd_play_returns_error_without_device(self):
        """cmd_play returns ok:false when no device connected."""
        with patch("subprocess.run", return_value=MagicMock(returncode=1, stdout=b"", stderr=b"error")):
            import youtube_agent
            with patch.object(youtube_agent, "get_connected_devices", return_value=[]):
                result = youtube_agent.cmd_play("test query")
                self.assertIn("ok", result)
                self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
