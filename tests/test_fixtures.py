"""
Test fixtures - unit tests for conftest.py fixtures
"""

import pytest
from tests.conftest import (
    workspace_path,
    skills_path,
    sample_task_data,
    mock_telegram_config,
    sample_enforcement_levels,
)


class TestFixtures:
    """Test fixture configurations"""

    def test_workspace_path_exists(self, workspace_path):
        """Test that workspace path is valid"""
        assert workspace_path is not None
        assert len(workspace_path) > 0

    def test_skills_path_is_subdirectory(self, workspace_path, skills_path):
        """Test that skills path is in workspace"""
        assert skills_path.startswith(workspace_path)

    def test_sample_task_data_structure(self, sample_task_data):
        """Test sample task has required fields"""
        required_fields = ["id", "title", "assignee", "deadline", "priority", "status"]
        for field in required_fields:
            assert field in sample_task_data

    def test_sample_task_data_types(self, sample_task_data):
        """Test sample task data types"""
        assert isinstance(sample_task_data["id"], str)
        assert isinstance(sample_task_data["title"], str)
        assert isinstance(sample_task_data["assignee"], str)
        assert isinstance(sample_task_data["priority"], str)
        assert isinstance(sample_task_data["status"], str)

    def test_mock_telegram_config(self, mock_telegram_config):
        """Test Telegram config has required fields"""
        assert "bot_token" in mock_telegram_config
        assert "chat_id" in mock_telegram_config

    def test_enforcement_levels_count(self, sample_enforcement_levels):
        """Test there are 4 enforcement levels"""
        assert len(sample_enforcement_levels) == 4

    def test_enforcement_levels_hours_increasing(self, sample_enforcement_levels):
        """Test enforcement hours are increasing"""
        hours = [level["hours"] for level in sample_enforcement_levels.values()]
        assert hours == sorted(hours)

    def test_enforcement_levels_have_messages(self, sample_enforcement_levels):
        """Test all enforcement levels have messages"""
        for level_name, level_data in sample_enforcement_levels.items():
            assert "message" in level_data, f"Missing message in {level_name}"
            assert len(level_data["message"]) > 0, f"Empty message in {level_name}"
