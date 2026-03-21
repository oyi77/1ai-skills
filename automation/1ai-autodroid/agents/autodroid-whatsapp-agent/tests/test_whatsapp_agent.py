"""Tests for autodroid-whatsapp-agent — uses mocks, no real device required."""
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

CONFIG_PATH = Path(__file__).parent.parent / "config" / "whatsapp_agent_config.json"


class TestWhatsAppAgentImport(unittest.TestCase):
    def test_import(self):
        """Agent imports without error (ADB not required)."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import whatsapp_agent  # noqa: F401

    def test_package_constant(self):
        """PACKAGE constant is set correctly for WhatsApp."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import whatsapp_agent
            self.assertEqual(whatsapp_agent.PACKAGE, "com.whatsapp")


class TestAIInterceptOptional(unittest.TestCase):
    def test_ai_intercept_decorator_passthrough(self):
        """_ai_intercept returns function unchanged when interceptor is None."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import whatsapp_agent
            original_enabled = whatsapp_agent.AI_INTERCEPT_ENABLED
            original_interceptor = whatsapp_agent._interceptor
            try:
                whatsapp_agent.AI_INTERCEPT_ENABLED = False
                whatsapp_agent._interceptor = None

                @whatsapp_agent._ai_intercept(skill_type="generic")
                def dummy_fn(msg):
                    return msg.upper()

                self.assertEqual(dummy_fn("hello"), "HELLO")
            finally:
                whatsapp_agent.AI_INTERCEPT_ENABLED = original_enabled
                whatsapp_agent._interceptor = original_interceptor

    def test_ai_intercept_flag_is_bool(self):
        """AI_INTERCEPT_ENABLED is a boolean."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import whatsapp_agent
            self.assertIsInstance(whatsapp_agent.AI_INTERCEPT_ENABLED, bool)


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

    def test_config_timeout_seconds(self):
        """Config timeout_seconds is positive."""
        with open(CONFIG_PATH) as f:
            data = json.load(f)
        self.assertIn("timeout_seconds", data)
        self.assertGreater(data["timeout_seconds"], 0)


class TestCmdSendWrapped(unittest.TestCase):
    def test_cmd_send_is_callable(self):
        """cmd_send remains callable after decorator."""
        with patch("subprocess.run", return_value=MagicMock(returncode=0, stdout=b"", stderr=b"")):
            import whatsapp_agent
            self.assertTrue(callable(whatsapp_agent.cmd_send))

    def test_cmd_send_returns_error_without_device(self):
        """cmd_send returns ok:false when no device connected."""
        with patch("subprocess.run", return_value=MagicMock(returncode=1, stdout=b"", stderr=b"error")):
            import whatsapp_agent
            with patch.object(whatsapp_agent, "get_connected_devices", return_value=[]):
                result = whatsapp_agent.cmd_send("John", "Hello!")
                self.assertIn("ok", result)
                self.assertFalse(result["ok"])


if __name__ == "__main__":
    unittest.main()
