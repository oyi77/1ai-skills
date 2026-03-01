# E2E Task Enforcement Tests
# Tests the full enforcement escalation protocol

import pytest
import sys
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

sys.path.insert(0, "/home/openclaw/.openclaw/workspace")
sys.path.insert(0, "/home/openclaw/.openclaw/workspace/skills/task-manager")

from api import TaskAPI
from enforcement import EnforcementProtocol


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    db_path = tempfile.mktemp(suffix=".db")
    yield db_path
    try:
        os.unlink(db_path)
    except:
        pass


class TestEnforcementEscalation:
    """Test enforcement escalation levels"""

    def test_escalation_warning_levels(self, temp_db):
        """Test warning_level progresses 0->1->2->3->4(maki)"""
        api = TaskAPI(db_path=temp_db)

        # Create overdue task
        task = api.create(title="Test Task", assignee="Veris", deadline="2020-01-01")

        # Initial level should be 0
        assert task["warning_level"] == 0

        # Escalate to warning 1
        result = api.escalate_warning(task["id"])
        assert result["warning_level"] == 1

        # Escalate to warning 2
        result = api.escalate_warning(task["id"])
        assert result["warning_level"] == 2

        # Escalate to warning 3
        result = api.escalate_warning(task["id"])
        assert result["warning_level"] == 3

        # Escalate to maki (level 4)
        result = api.escalate_warning(task["id"])
        assert result["warning_level"] == 4

    def test_deadline_check(self, temp_db):
        """Test overdue task detection"""
        api = TaskAPI(db_path=temp_db)

        # Create overdue task
        api.create(title="Overdue Task", assignee="Nuno", deadline="2020-01-01")

        # Check enforcement - should find overdue tasks
        overdue = api.check_enforcement()
        assert len(overdue) >= 1
        assert any(t["title"] == "Overdue Task" for t in overdue)


class TestEnforcementProtocol:
    """Test EnforcementProtocol class"""

    def test_protocol_initialization(self):
        """Test protocol can be initialized"""
        protocol = EnforcementProtocol()
        assert protocol is not None

    def test_enforcement_levels_defined(self):
        """Test all 4 enforcement levels are defined"""
        db_path = tempfile.mktemp(suffix=".db")
        api = TaskAPI(db_path=db_path)

        # Verify enforcement levels exist
        assert len(api.enforcement_levels) == 4
        assert 1 in api.enforcement_levels
        assert 2 in api.enforcement_levels
        assert 3 in api.enforcement_levels
        assert 4 in api.enforcement_levels
        os.unlink(db_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
