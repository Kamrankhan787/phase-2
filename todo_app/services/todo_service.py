from typing import List, Optional
from todo_app.models.task import Task

class TaskNotFoundError(Exception):
    """Raised when a task with a given ID is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Error: Task with ID {task_id} not found.")

class InvalidTaskError(Exception):
    """Raised when task data is invalid (e.g. empty description)."""
    pass

class TodoService:
    """
    Manages in-memory storage and business logic for tasks.
    Satisfies Phase I Plan §1, §2, §3 and Spec §5.
    """
    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Adds a new task to the in-memory list."""
        if not description or not description.strip():
            raise InvalidTaskError("Task description cannot be empty.")

        task = Task(id=self._next_id, description=description.strip())
        self.tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Returns all tasks."""
        return self.tasks

    def _get_task_by_id(self, task_id: int) -> Task:
        """Private helper to find a task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise TaskNotFoundError(task_id)

    def update_task(self, task_id: int, new_description: str) -> Task:
        """Updates an existing task's description."""
        if not new_description or not new_description.strip():
            raise InvalidTaskError("Task description cannot be empty.")

        task = self._get_task_by_id(task_id)
        task.description = new_description.strip()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Removes a task from the list."""
        task = self._get_task_by_id(task_id)
        self.tasks.remove(task)
        return True

    def toggle_task_status(self, task_id: int) -> Task:
        """Toggles the completion status of a task."""
        task = self._get_task_by_id(task_id)
        task.is_completed = not task.is_completed
        return task
