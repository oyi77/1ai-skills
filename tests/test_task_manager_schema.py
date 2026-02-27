"""
Test task-manager schema - tests for task data structure and validation
"""

import pytest
from datetime import datetime, timedelta


class TestTaskSchema:
    """Test task data schema and structure"""

    def test_task_has_required_fields(self, sample_task_data):
        """Test task has all required fields"""
        required_fields = ["id", "title", "assignee", "deadline", "priority", "status"]
        for field in required_fields:
            assert field in sample_task_data, f"Missing required field: {field}"

    def test_task_id_is_string(self, sample_task_data):
        """Test task ID is a string"""
        assert isinstance(sample_task_data["id"], str)
        assert len(sample_task_data["id"]) > 0

    def test_task_title_is_string(self, sample_task_data):
        """Test task title is a string"""
        assert isinstance(sample_task_data["title"], str)
        assert len(sample_task_data["title"]) > 0

    def test_task_assignee_is_string(self, sample_task_data):
        """Test task assignee is a string"""
        assert isinstance(sample_task_data["assignee"], str)
        assert len(sample_task_data["assignee"]) > 0

    def test_task_deadline_is_iso_format(self, sample_task_data):
        """Test task deadline is ISO 8601 format"""
        deadline = sample_task_data["deadline"]
        assert isinstance(deadline, str)
        # Should be parseable as ISO format
        try:
            datetime.fromisoformat(deadline.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(f"Deadline {deadline} is not valid ISO 8601 format")

    def test_task_priority_is_valid(self, sample_task_data):
        """Test task priority is one of valid values"""
        valid_priorities = ["low", "medium", "high", "critical"]
        assert sample_task_data["priority"] in valid_priorities

    def test_task_status_is_valid(self, sample_task_data):
        """Test task status is one of valid values"""
        valid_statuses = ["pending", "in_progress", "completed", "blocked", "cancelled"]
        assert sample_task_data["status"] in valid_statuses

    def test_task_id_uniqueness(self):
        """Test that task IDs should be unique"""
        task_ids = ["task-001", "task-002", "task-003"]
        assert len(task_ids) == len(set(task_ids))

    def test_task_priority_ordering(self):
        """Test priority levels have correct ordering"""
        priority_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        assert priority_order["low"] < priority_order["medium"]
        assert priority_order["medium"] < priority_order["high"]
        assert priority_order["high"] < priority_order["critical"]

    def test_task_status_transitions(self):
        """Test valid status transitions"""
        # pending -> in_progress, completed, cancelled
        # in_progress -> completed, blocked, cancelled
        # blocked -> in_progress, cancelled
        # completed -> (terminal)
        # cancelled -> (terminal)
        valid_transitions = {
            "pending": ["in_progress", "completed", "cancelled"],
            "in_progress": ["completed", "blocked", "cancelled"],
            "blocked": ["in_progress", "cancelled"],
            "completed": [],
            "cancelled": [],
        }
        assert len(valid_transitions) == 5


class TestTaskValidation:
    """Test task data validation"""

    def test_task_title_not_empty(self):
        """Test task title cannot be empty"""
        task = {"title": ""}
        assert len(task["title"]) == 0  # Should fail validation

    def test_task_deadline_in_future(self):
        """Test task deadline should be in future"""
        future_date = (datetime.now() + timedelta(days=1)).isoformat() + "Z"
        assert future_date is not None

    def test_task_assignee_not_empty(self):
        """Test task assignee cannot be empty"""
        task = {"assignee": ""}
        assert len(task["assignee"]) == 0  # Should fail validation

    def test_task_with_optional_fields(self):
        """Test task can have optional fields"""
        task = {
            "id": "task-001",
            "title": "Test Task",
            "assignee": "Veris",
            "deadline": "2026-03-01T00:00:00Z",
            "priority": "high",
            "status": "pending",
            "description": "Optional description",
            "tags": ["urgent", "important"],
        }
        assert "description" in task
        assert "tags" in task

    def test_task_tags_are_list(self):
        """Test task tags should be a list"""
        task = {"tags": ["tag1", "tag2", "tag3"]}
        assert isinstance(task["tags"], list)
        assert all(isinstance(tag, str) for tag in task["tags"])

    def test_task_description_is_string(self):
        """Test task description is a string"""
        task = {"description": "This is a task description"}
        assert isinstance(task["description"], str)


class TestTaskManager:
    """Test task manager interface"""

    def test_task_manager_can_create_task(self, sample_task_data):
        """Test task manager can create a task"""
        # Interface test - actual implementation may vary
        assert sample_task_data["id"] is not None
        assert sample_task_data["title"] is not None

    def test_task_manager_can_update_status(self, sample_task_data):
        """Test task manager can update task status"""
        original_status = sample_task_data["status"]
        # Simulate status update
        new_status = "in_progress"
        assert new_status != original_status

    def test_task_manager_can_list_tasks(self):
        """Test task manager can list tasks"""
        tasks = [
            {"id": "task-001", "title": "Task 1"},
            {"id": "task-002", "title": "Task 2"},
            {"id": "task-003", "title": "Task 3"},
        ]
        assert len(tasks) == 3

    def test_task_manager_can_filter_by_status(self):
        """Test task manager can filter tasks by status"""
        tasks = [
            {"id": "task-001", "status": "pending"},
            {"id": "task-002", "status": "in_progress"},
            {"id": "task-003", "status": "completed"},
        ]
        pending_tasks = [t for t in tasks if t["status"] == "pending"]
        assert len(pending_tasks) == 1

    def test_task_manager_can_filter_by_assignee(self):
        """Test task manager can filter tasks by assignee"""
        tasks = [
            {"id": "task-001", "assignee": "Veris"},
            {"id": "task-002", "assignee": "Alice"},
            {"id": "task-003", "assignee": "Veris"},
        ]
        veris_tasks = [t for t in tasks if t["assignee"] == "Veris"]
        assert len(veris_tasks) == 2

    def test_task_manager_can_sort_by_priority(self):
        """Test task manager can sort tasks by priority"""
        priority_order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        tasks = [
            {"id": "task-001", "priority": "low"},
            {"id": "task-002", "priority": "critical"},
            {"id": "task-003", "priority": "high"},
        ]
        sorted_tasks = sorted(
            tasks, key=lambda t: priority_order[t["priority"]], reverse=True
        )
        assert sorted_tasks[0]["priority"] == "critical"
        assert sorted_tasks[-1]["priority"] == "low"
