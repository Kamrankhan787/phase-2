"""Unit tests for TodoService."""

import pytest
from datetime import datetime
from models.task import Task, TaskStatus
from services.todo_service import TodoService


class TestTodoServiceInitialization:
    """Tests for TodoService initialization."""

    def test_initial_state_is_empty(self):
        """Service should start with empty task list."""
        service = TodoService()
        tasks = service.get_all_tasks()
        assert tasks == []

    def test_first_id_starts_at_one(self):
        """First generated ID should be 1."""
        service = TodoService()
        task = service.add_task("Test task")
        assert task.id == 1

    def test_ids_increment_sequence(self):
        """Task IDs should increment sequentially."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_ids_not_reused_after_delete(self):
        """Deleted task IDs should not be reused."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        service.delete_task(1)

        task3 = service.add_task("Task 3")
        assert task3.id == 3  # Not 1


class TestAddTask:
    """Tests for add_task method."""

    def test_add_task_creates_with_incomplete_status(self):
        """New tasks should have INCOMPLETE status."""
        service = TodoService()
        task = service.add_task("Test task")

        assert task.status == TaskStatus.INCOMPLETE

    def test_add_task_strips_whitespace(self):
        """Task description should be stripped of whitespace."""
        service = TodoService()
        task = service.add_task("  Test task  ")

        assert task.description == "Test task"

    def test_add_task_has_timestamp(self):
        """New task should have a created_at timestamp."""
        service = TodoService()
        before = datetime.now()
        task = service.add_task("Test task")
        after = datetime.now()

        assert before <= task.created_at <= after

    def test_add_task_returns_task_object(self):
        """add_task should return the created Task."""
        service = TodoService()
        task = service.add_task("Test task")

        assert isinstance(task, Task)
        assert task.id == 1
        assert task.description == "Test task"
        assert task.status == TaskStatus.INCOMPLETE


class TestGetAllTasks:
    """Tests for get_all_tasks method."""

    def test_returns_empty_list_when_no_tasks(self):
        """Should return empty list when no tasks exist."""
        service = TodoService()
        tasks = service.get_all_tasks()

        assert tasks == []

    def test_returns_tasks_in_id_order(self):
        """Tasks should be returned in ID order."""
        service = TodoService()
        service.add_task("Third")
        service.add_task("First")
        service.add_task("Second")

        tasks = service.get_all_tasks()
        assert len(tasks) == 3
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_returns_copy_not_original(self):
        """Should return a copy to prevent external mutation."""
        service = TodoService()
        service.add_task("Test")
        tasks = service.get_all_tasks()

        # Modifying the returned list should not affect the service
        tasks.clear()
        original_tasks = service.get_all_tasks()
        assert len(original_tasks) == 1


class TestGetTaskById:
    """Tests for get_task_by_id method."""

    def test_returns_none_for_nonexistent_id(self):
        """Should return None for non-existent task ID."""
        service = TodoService()
        result = service.get_task_by_id(999)

        assert result is None

    def test_returns_task_when_found(self):
        """Should return the task when found."""
        service = TodoService()
        created = service.add_task("Test task")
        found = service.get_task_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.description == "Test task"

    def test_returns_first_match_only(self):
        """Should return first match (IDs are unique anyway)."""
        service = TodoService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        found = service.get_task_by_id(1)
        assert found.id == 1


class TestUpdateTask:
    """Tests for update_task method."""

    def test_returns_false_for_nonexistent_task(self):
        """Should return False when task not found."""
        service = TodoService()
        result = service.update_task(999, "New description")

        assert result is False

    def test_updates_description(self):
        """Should update the task description."""
        service = TodoService()
        service.add_task("Original")
        result = service.update_task(1, "Updated description")

        assert result is True
        task = service.get_task_by_id(1)
        assert task.description == "Updated description"

    def test_strips_whitespace_from_description(self):
        """Should strip whitespace from new description."""
        service = TodoService()
        service.add_task("Original")
        service.update_task(1, "  Updated  ")

        task = service.get_task_by_id(1)
        assert task.description == "Updated"

    def test_does_not_change_status(self):
        """Update should not change task status."""
        service = TodoService()
        service.add_task("Task")
        service.mark_complete(1)
        service.update_task(1, "New description")

        task = service.get_task_by_id(1)
        assert task.status == TaskStatus.COMPLETE


class TestDeleteTask:
    """Tests for delete_task method."""

    def test_returns_false_for_nonexistent_task(self):
        """Should return False when task not found."""
        service = TodoService()
        result = service.delete_task(999)

        assert result is False

    def test_removes_task_from_list(self):
        """Should remove task from the list."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")

        result = service.delete_task(1)

        assert result is True
        assert service.get_task_by_id(1) is None
        assert len(service.get_all_tasks()) == 1

    def test_does_not_affect_other_tasks(self):
        """Deleting one task should not affect others."""
        service = TodoService()
        service.add_task("Task 1")
        task2 = service.add_task("Task 2")

        service.delete_task(1)

        remaining = service.get_all_tasks()
        assert len(remaining) == 1
        assert remaining[0].id == task2.id


class TestMarkComplete:
    """Tests for mark_complete method."""

    def test_returns_false_for_nonexistent_task(self):
        """Should return False when task not found."""
        service = TodoService()
        result = service.mark_complete(999)

        assert result is False

    def test_changes_status_to_complete(self):
        """Should change task status to COMPLETE."""
        service = TodoService()
        service.add_task("Task")
        result = service.mark_complete(1)

        assert result is True
        task = service.get_task_by_id(1)
        assert task.status == TaskStatus.COMPLETE


class TestMarkIncomplete:
    """Tests for mark_incomplete method."""

    def test_returns_false_for_nonexistent_task(self):
        """Should return False when task not found."""
        service = TodoService()
        result = service.mark_incomplete(999)

        assert result is False

    def test_changes_status_to_incomplete(self):
        """Should change task status to INCOMPLETE."""
        service = TodoService()
        service.add_task("Task")
        service.mark_complete(1)
        result = service.mark_incomplete(1)

        assert result is True
        task = service.get_task_by_id(1)
        assert task.status == TaskStatus.INCOMPLETE
