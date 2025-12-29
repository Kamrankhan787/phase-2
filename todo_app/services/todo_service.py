"""Todo service for managing in-memory task storage and operations."""

from datetime import datetime
from typing import List, Optional
from models.task import Task, TaskStatus


class TodoService:
    """Handles in-memory task storage and CRUD operations.

    This service manages a collection of tasks stored in memory.
    Data persists only for the duration of the application session.
    """

    def __init__(self):
        """Initialize the todo service with empty storage."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generate the next unique task ID.

        Returns:
            The next available integer ID (starts at 1, never reused).
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add_task(self, description: str) -> Task:
        """Create a new task with the given description.

        Args:
            description: The task description text.

        Returns:
            The newly created Task with unique ID and INCOMPLETE status.
        """
        description = description.strip()
        task_id = self._generate_id()
        task = Task(
            id=task_id,
            description=description,
            status=TaskStatus.INCOMPLETE,
            created_at=datetime.now()
        )
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in ID order.

        Returns:
            A copy of the task list to prevent external mutation.
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> bool:
        """Update a task's description.

        Args:
            task_id: The ID of the task to update.
            new_description: The new description text.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.description = new_description.strip()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was found and deleted, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def mark_complete(self, task_id: int) -> bool:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.status = TaskStatus.COMPLETE
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete.

        Returns:
            True if the task was found and updated, False otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.status = TaskStatus.INCOMPLETE
        return True
