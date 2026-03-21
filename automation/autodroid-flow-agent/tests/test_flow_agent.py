"""Tests for autodroid-flow-agent — mock tests, no device required."""
import unittest
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestAgent(unittest.TestCase):

    def test_script_syntax(self):
        """Script imports without syntax error."""
        import ast
        script = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'flow_agent.py')
        if os.path.exists(script):
            with open(script) as f:
                ast.parse(f.read())

    def test_config_exists(self):
        config_dir = os.path.join(os.path.dirname(__file__), '..', 'config')
        configs = [f for f in os.listdir(config_dir) if f.endswith('.json')] if os.path.isdir(config_dir) else []
        self.assertTrue(len(configs) > 0)

    def test_skill_md_exists(self):
        skill_md = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        self.assertTrue(os.path.isfile(skill_md))


if __name__ == '__main__':
    unittest.main(verbosity=2)
