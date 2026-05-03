#!/usr/bin/env python3
"""
Tests for autodroid-kling-agent/scripts/kling_agent.py

Run:
    python3 -m pytest tests/test_kling_agent.py -v
    # or
    python3 tests/test_kling_agent.py

Tests:
    - Import and module structure
    - Core utility functions (no device required)
    - Coordinate constants validation
    - Text escaping
    - UI node parsing
    - Credit parsing
    - Screen classification
    - Config file
    - AI Interceptor integration
    - Video Enhancer integration
"""

import json
import os
import sys
import re
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts dir to path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

# ─── Test Cases ───────────────────────────────────────────────────────────────

class TestImport(unittest.TestCase):
    """Test module can be imported without errors."""

    def test_import(self):
        """Module should import cleanly."""
        import kling_agent  # noqa: F401
        self.assertTrue(True, "Import succeeded")

    def test_constants_present(self):
        """All required constants should be defined."""
        import kling_agent as ka
        self.assertEqual(ka.PACKAGE, "kling.ai.video.chat")
        self.assertEqual(ka.DEFAULT_DEVICE, "SGZTONV4OBL74TJZ")
        self.assertEqual(ka.SCREEN_W, 720)
        self.assertEqual(ka.SCREEN_H, 1640)

    def test_ai_interceptor_flag(self):
        """AI_INTERCEPT_ENABLED flag must exist (bool)."""
        import kling_agent as ka
        self.assertIsInstance(ka.AI_INTERCEPT_ENABLED, bool)

    def test_video_enhance_flag(self):
        """VIDEO_ENHANCE_ENABLED flag must exist (bool)."""
        import kling_agent as ka
        self.assertIsInstance(ka.VIDEO_ENHANCE_ENABLED, bool)


class TestCoordinates(unittest.TestCase):
    """Validate navigation coordinates are within screen bounds."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka

    def _check_coord(self, name, x, y):
        """Assert coordinate is within (0, 0, 720, 1640)."""
        self.assertGreaterEqual(x, 0, f"{name}: x must be >= 0")
        self.assertLessEqual(x, 720, f"{name}: x must be <= 720")
        self.assertGreaterEqual(y, 0, f"{name}: y must be >= 0")
        self.assertLessEqual(y, 1640, f"{name}: y must be <= 1640")

    def test_nav_coords(self):
        ka = self.ka
        self._check_coord("NAV_HOME", *ka.NAV_HOME)
        self._check_coord("NAV_CREATE", *ka.NAV_CREATE)
        self._check_coord("NAV_MY_SPACE", *ka.NAV_MY_SPACE)
        self._check_coord("OMNI_SEND", ka.OMNI_SEND_X, ka.OMNI_SEND_Y)

    def test_i2v_coords(self):
        ka = self.ka
        self.assertGreater(ka.I2V_ADD_IMAGE_Y, 0)
        self.assertLess(ka.I2V_ADD_IMAGE_Y, 1640)
        self.assertGreater(ka.I2V_GENERATE_X, 0)
        self.assertGreater(ka.I2V_GENERATE_Y, 0)

    def test_tap_safety_threshold(self):
        """tap() should block taps below y=1530."""
        ka = self.ka
        with patch.object(ka, 'adb') as mock_adb:
            ka.tap(360, 1600)  # below threshold
            mock_adb.assert_not_called()

    def test_tap_allowed(self):
        """tap() should allow taps above threshold."""
        ka = self.ka
        with patch.object(ka, 'adb') as mock_adb:
            with patch('time.sleep'):
                ka.tap(360, 800)  # above threshold
                mock_adb.assert_called()


class TestTextEscaping(unittest.TestCase):
    """Test _escape_adb_text handles special characters."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka

    def test_plain_text(self):
        result = self.ka._escape_adb_text("hello world")
        self.assertEqual(result, "hello world")

    def test_special_chars(self):
        result = self.ka._escape_adb_text("a&b;c|d")
        self.assertNotIn("&b", result)  # & should be escaped

    def test_quotes(self):
        result = self.ka._escape_adb_text('say "hi"')
        self.assertIn('\\"', result)

    def test_dollar(self):
        result = self.ka._escape_adb_text("$price")
        self.assertIn("\\$", result)


class TestBoundsParser(unittest.TestCase):
    """Test bounds_to_center function."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka

    def test_valid_bounds(self):
        center = self.ka.bounds_to_center("[100,200][300,400]")
        self.assertEqual(center, (200, 300))

    def test_zero_bounds(self):
        center = self.ka.bounds_to_center("[0,0][720,100]")
        self.assertEqual(center, (360, 50))

    def test_invalid_bounds(self):
        center = self.ka.bounds_to_center("")
        self.assertIsNone(center)

    def test_partial_bounds(self):
        center = self.ka.bounds_to_center("[100,200]")
        self.assertIsNone(center)


class TestCreditParsing(unittest.TestCase):
    """Test credit parsing from UI nodes."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka

    def test_parse_credits_normal(self):
        nodes = [
            {"text": "🔥 192 Generate", "content-desc": "", "bounds": "[0,0][100,100]", "class": "android.widget.TextView", "resource-id": "", "clickable": "false", "enabled": "true", "focused": "false", "package": "kling.ai.video.chat"}
        ]
        result = self.ka._parse_credits_from_nodes(nodes)
        self.assertEqual(result, 192)

    def test_parse_credits_no_emoji(self):
        nodes = [
            {"text": "48 Generate", "content-desc": "", "bounds": "[0,0][100,100]", "class": "android.widget.TextView", "resource-id": "", "clickable": "false", "enabled": "true", "focused": "false", "package": ""}
        ]
        result = self.ka._parse_credits_from_nodes(nodes)
        self.assertEqual(result, 48)

    def test_parse_credits_not_found(self):
        nodes = [{"text": "Hello", "content-desc": "", "bounds": "", "class": "", "resource-id": "", "clickable": "false", "enabled": "true", "focused": "false", "package": ""}]
        result = self.ka._parse_credits_from_nodes(nodes)
        self.assertEqual(result, -1)

    def test_parse_credits_empty(self):
        result = self.ka._parse_credits_from_nodes([])
        self.assertEqual(result, -1)


class TestScreenClassification(unittest.TestCase):
    """Test UI screen state classification."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka

    def _make_node(self, text="", desc="", pkg="kling.ai.video.chat"):
        return {
            "text": text, "content-desc": desc, "class": "android.widget.TextView",
            "bounds": "[0,0][100,100]", "resource-id": "", "clickable": "false",
            "enabled": "true", "focused": "false", "package": pkg
        }

    def test_home_screen(self):
        nodes = [self._make_node("Omni"), self._make_node("AI Image"), self._make_node("For You")]
        state = self.ka._classify_screen(nodes)
        self.assertEqual(state, "home")

    def test_creator_screen(self):
        nodes = [self._make_node("Generate"), self._make_node("Add Character Image")]
        state = self.ka._classify_screen(nodes)
        self.assertEqual(state, "creator")

    def test_processing_screen(self):
        nodes = [self._make_node("Generating"), self._make_node("25%")]
        state = self.ka._classify_screen(nodes)
        self.assertEqual(state, "processing")

    def test_gallery_screen(self):
        nodes = [self._make_node("Camera roll"), self._make_node("Done")]
        state = self.ka._classify_screen(nodes)
        self.assertEqual(state, "gallery")

    def test_unknown_screen(self):
        nodes = [self._make_node("Random stuff", pkg="com.other.app")]
        state = self.ka._classify_screen(nodes)
        self.assertEqual(state, "unknown")

    def test_empty_nodes(self):
        state = self.ka._classify_screen([])
        self.assertEqual(state, "unknown")


class TestFindNode(unittest.TestCase):
    """Test find_node / find_nodes."""

    def setUp(self):
        import kling_agent as ka
        self.ka = ka
        self.nodes = [
            {"text": "Generate", "content-desc": "", "bounds": "[475,811][672,875]", "class": "android.widget.TextView", "resource-id": "btn_gen", "clickable": "true", "enabled": "true", "focused": "false", "package": "kling.ai.video.chat"},
            {"text": "Add Character Image", "content-desc": "", "bounds": "[0,300][720,400]", "class": "android.widget.FrameLayout", "resource-id": "", "clickable": "true", "enabled": "true", "focused": "false", "package": "kling.ai.video.chat"},
            {"text": "192 Generate", "content-desc": "", "bounds": "[0,0][100,50]", "class": "android.widget.TextView", "resource-id": "", "clickable": "false", "enabled": "true", "focused": "false", "package": "kling.ai.video.chat"},
        ]

    def test_find_by_exact_text(self):
        node = self.ka.find_node(self.nodes, label="Generate", partial=False)
        self.assertIsNotNone(node)
        self.assertEqual(node["text"], "Generate")

    def test_find_by_partial_text(self):
        node = self.ka.find_node(self.nodes, label="Character", partial=True)
        self.assertIsNotNone(node)

    def test_find_by_res_id(self):
        node = self.ka.find_node(self.nodes, res_id="btn_gen")
        self.assertIsNotNone(node)

    def test_not_found(self):
        node = self.ka.find_node(self.nodes, label="NonExistent")
        self.assertIsNone(node)


class TestConfigFile(unittest.TestCase):
    """Test config/kling_agent_config.json."""

    def test_config_exists(self):
        config_path = Path(__file__).parent.parent / "config" / "kling_agent_config.json"
        self.assertTrue(config_path.exists(), "config/kling_agent_config.json should exist")

    def test_config_valid_json(self):
        config_path = Path(__file__).parent.parent / "config" / "kling_agent_config.json"
        with open(config_path) as f:
            config = json.load(f)
        self.assertIn("agent", config)
        self.assertIn("device", config)
        self.assertIn("app", config)

    def test_config_device_serial(self):
        config_path = Path(__file__).parent.parent / "config" / "kling_agent_config.json"
        with open(config_path) as f:
            config = json.load(f)
        self.assertEqual(config["device"]["serial"], "SGZTONV4OBL74TJZ")

    def test_config_interceptor_settings(self):
        config_path = Path(__file__).parent.parent / "config" / "kling_agent_config.json"
        with open(config_path) as f:
            config = json.load(f)
        self.assertIn("ai_interceptor", config)
        self.assertTrue(config["ai_interceptor"]["fail_safe"])


class TestMotionTemplates(unittest.TestCase):
    """Test motion template list."""

    def test_motion_templates_exist(self):
        import kling_agent as ka
        self.assertIsInstance(ka.MOTION_TEMPLATES, list)
        self.assertGreater(len(ka.MOTION_TEMPLATES), 0)

    def test_chinese_trend_in_templates(self):
        import kling_agent as ka
        self.assertIn("Chinese trend", ka.MOTION_TEMPLATES)


class TestRetryDecorator(unittest.TestCase):
    """Test retry() utility."""

    def test_retry_success_first(self):
        import kling_agent as ka
        counter = {"n": 0}
        def fn():
            counter["n"] += 1
            return "ok"
        result = ka.retry(fn, retries=3, base_delay=0)
        self.assertEqual(result, "ok")
        self.assertEqual(counter["n"], 1)

    def test_retry_success_third(self):
        import kling_agent as ka
        counter = {"n": 0}
        def fn():
            counter["n"] += 1
            if counter["n"] < 3:
                raise ValueError("fail")
            return "ok"
        with patch('time.sleep'):
            result = ka.retry(fn, retries=3, base_delay=0.001, label="test")
        self.assertEqual(result, "ok")
        self.assertEqual(counter["n"], 3)

    def test_retry_all_fail(self):
        import kling_agent as ka
        def fn():
            raise ValueError("always fail")
        with patch('time.sleep'):
            with self.assertRaises(ValueError):
                ka.retry(fn, retries=3, base_delay=0.001)


class TestCLIParser(unittest.TestCase):
    """Test argument parser structure."""

    def test_parser_builds(self):
        import kling_agent as ka
        parser = ka.build_parser()
        self.assertIsNotNone(parser)

    def test_t2v_command(self):
        import kling_agent as ka
        parser = ka.build_parser()
        args = parser.parse_args(["t2v", "--prompt", "test video"])
        self.assertEqual(args.command, "t2v")
        self.assertEqual(args.prompt, "test video")

    def test_i2v_command(self):
        import kling_agent as ka
        parser = ka.build_parser()
        args = parser.parse_args(["i2v", "--image", "/tmp/test.jpg"])
        self.assertEqual(args.command, "i2v")
        self.assertEqual(args.image, "/tmp/test.jpg")

    def test_status_command(self):
        import kling_agent as ka
        parser = ka.build_parser()
        args = parser.parse_args(["status"])
        self.assertEqual(args.command, "status")

    def test_device_flag(self):
        import kling_agent as ka
        parser = ka.build_parser()
        args = parser.parse_args(["--device", "ABC123", "status"])
        self.assertEqual(args.device, "ABC123")


# ─── Runner ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Run with basic output
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
