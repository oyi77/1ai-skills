"""
Pytest configuration and fixtures for 1ai-skills-bundle tests
"""

import pytest
import os
import sys

# Add workspace to path
workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, workspace_root)


@pytest.fixture
def workspace_path():
    """Return the workspace path"""
    return workspace_root


@pytest.fixture
def skills_path(workspace_path):
    """Return the skills directory path"""
    return os.path.join(workspace_path, "skills")


@pytest.fixture
def sample_task_data():
    """Sample task data for testing"""
    return {
        "id": "test-001",
        "title": "Test Task",
        "assignee": "Veris",
        "deadline": "2026-03-01T00:00:00Z",
        "priority": "high",
        "status": "pending",
    }


@pytest.fixture
def mock_telegram_config():
    """Mock Telegram configuration for testing"""
    return {"bot_token": "test_token", "chat_id": "test_chat_id"}


@pytest.fixture
def sample_enforcement_levels():
    """Sample enforcement levels for testing"""
    return {
        "warning_1": {"hours": 24, "message": "Reminder: task due soon"},
        "warning_2": {"hours": 48, "message": "Final reminder: task overdue"},
        "warning_3": {"hours": 72, "message": "URGENT: task severely overdue"},
        "maki": {"hours": 96, "message": "MAKI MODE ACTIVATED"},
    }
