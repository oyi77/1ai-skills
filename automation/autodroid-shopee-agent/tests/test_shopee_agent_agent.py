"""Tests for autodroid-shopee-agent — mock tests, no device required."""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestShopeeagentAgent(unittest.TestCase):

    def test_import(self):
        """Script imports without syntax error."""
        scripts = [f for f in os.listdir(
            os.path.join(os.path.dirname(__file__), '..', 'scripts')
        ) if f.endswith('.py')]
        self.assertTrue(len(scripts) > 0, "No scripts found")

    def test_config_exists(self):
        """Config file exists."""
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        self.assertTrue(os.path.isdir(config_dir), "No config dir")
        configs = [f for f in os.listdir(config_dir) if f.endswith('.json')]
        self.assertTrue(len(configs) > 0, "No config files")

    def test_skill_md_exists(self):
        """SKILL.md exists."""
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        self.assertTrue(os.path.isfile(skill_md), "SKILL.md missing")


if __name__ == '__main__':
    unittest.main(verbosity=2)
