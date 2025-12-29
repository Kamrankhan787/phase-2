"""Unit tests for TodoMenu."""

import pytest
from unittest.mock import patch, MagicMock
from models.task import Task, TaskStatus
from services.todo_service import TodoService
from cli.menu import TodoMenu


class TestTodoMenuAddTask:
    """Tests for add task handler."""

    @patch('builtins.input', return_value='Test task')
    def test_add_task_success(self, mock_input):
        """Should add task and display success message."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_add()

        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Test task"

    @patch('builtins.input', return_value='')
    def test_add_task_empty_description(self, mock_input):
        """Should handle empty description gracefully."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_add()

        assert len(service.get_all_tasks()) == 0


class TestTodoMenuViewTasks:
    """Tests for view tasks handler."""

    def test_view_empty_list(self, capsys):
        """Should display message when no tasks."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_view()

        captured = capsys.readouterr()
        assert "No tasks found" in captured.out

    def test_view_tasks_with_items(self, capsys):
        """Should display all tasks."""
        service = TodoService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        menu = TodoMenu(service)

        menu._handle_view()

        captured = capsys.readouterr()
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out

    def test_view_shows_incomplete_status(self, capsys):
        """Should show incomplete tasks with [ ] marker."""
        service = TodoService()
        service.add_task("Incomplete task")
        menu = TodoMenu(service)

        menu._handle_view()

        captured = capsys.readouterr()
        assert "[1] Incomplete" in captured.out

    def test_view_shows_complete_status(self, capsys):
        """Should show complete tasks."""
        service = TodoService()
        task = service.add_task("Complete task")
        service.mark_complete(task.id)
        menu = TodoMenu(service)

        menu._handle_view()

        captured = capsys.readouterr()
        assert "[1] Complete" in captured.out

    def test_view_shows_summary(self, capsys):
        """Should display task summary."""
        service = TodoService()
        service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        service.mark_complete(task2.id)
        menu = TodoMenu(service)

        menu._handle_view()

        captured = capsys.readouterr()
        assert "Total: 2 tasks" in captured.out
        assert "1 complete" in captured.out
        assert "1 incomplete" in captured.out


class TestTodoMenuUpdateTask:
    """Tests for update task handler."""

    @patch('builtins.input', side_effect=['1', 'Updated task'])
    def test_update_task_success(self, mock_input):
        """Should update task description."""
        service = TodoService()
        service.add_task("Original")
        menu = TodoMenu(service)

        menu._handle_update()

        task = service.get_task_by_id(1)
        assert task.description == "Updated task"

    @patch('builtins.input', return_value='999')
    def test_update_nonexistent_task(self, mock_input, capsys):
        """Should show error for non-existent task."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_update()

        captured = capsys.readouterr()
        assert "not found" in captured.out

    @patch('builtins.input', side_effect=['1', ''])
    def test_update_empty_description(self, mock_input, capsys):
        """Should handle empty description."""
        service = TodoService()
        service.add_task("Original")
        menu = TodoMenu(service)

        menu._handle_update()

        task = service.get_task_by_id(1)
        assert task.description == "Original"


class TestTodoMenuDeleteTask:
    """Tests for delete task handler."""

    @patch('builtins.input', return_value='1')
    def test_delete_task_success(self, mock_input):
        """Should delete task."""
        service = TodoService()
        service.add_task("Task to delete")
        menu = TodoMenu(service)

        menu._handle_delete()

        assert len(service.get_all_tasks()) == 0

    @patch('builtins.input', return_value='999')
    def test_delete_nonexistent_task(self, mock_input, capsys):
        """Should show error for non-existent task."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_delete()

        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestTodoMenuMarkComplete:
    """Tests for mark complete handler."""

    @patch('builtins.input', return_value='1')
    def test_mark_complete_success(self, mock_input):
        """Should mark task as complete."""
        service = TodoService()
        service.add_task("Task")
        menu = TodoMenu(service)

        menu._handle_mark_complete()

        task = service.get_task_by_id(1)
        assert task.status == TaskStatus.COMPLETE

    @patch('builtins.input', return_value='999')
    def test_mark_complete_nonexistent(self, mock_input, capsys):
        """Should show error for non-existent task."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_mark_complete()

        captured = capsys.readouterr()
        assert "not found" in captured.out

    @patch('builtins.input', return_value='1')
    def test_mark_already_complete(self, mock_input, capsys):
        """Should show message when already complete."""
        service = TodoService()
        service.add_task("Task")
        service.mark_complete(1)
        menu = TodoMenu(service)

        menu._handle_mark_complete()

        captured = capsys.readouterr()
        assert "already complete" in captured.out


class TestTodoMenuMarkIncomplete:
    """Tests for mark incomplete handler."""

    @patch('builtins.input', return_value='1')
    def test_mark_incomplete_success(self, mock_input):
        """Should mark task as incomplete."""
        service = TodoService()
        service.add_task("Task")
        service.mark_complete(1)
        menu = TodoMenu(service)

        menu._handle_mark_incomplete()

        task = service.get_task_by_id(1)
        assert task.status == TaskStatus.INCOMPLETE

    @patch('builtins.input', return_value='999')
    def test_mark_incomplete_nonexistent(self, mock_input, capsys):
        """Should show error for non-existent task."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_mark_incomplete()

        captured = capsys.readouterr()
        assert "not found" in captured.out

    @patch('builtins.input', return_value='1')
    def test_mark_already_incomplete(self, mock_input, capsys):
        """Should show message when already incomplete."""
        service = TodoService()
        service.add_task("Task")
        menu = TodoMenu(service)

        menu._handle_mark_incomplete()

        captured = capsys.readouterr()
        assert "already incomplete" in captured.out


class TestTodoMenuExit:
    """Tests for exit handler."""

    def test_exit_displays_goodbye(self, capsys):
        """Should display goodbye message."""
        service = TodoService()
        menu = TodoMenu(service)

        menu._handle_exit()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out
