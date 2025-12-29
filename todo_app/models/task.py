"""Task data model for the Todo application."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TaskStatus(Enum):
    """Enumeration of possible task statuses."""

    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"


@dataclass
class Task:
    """Represents a single task in the todo list.

    Attributes:
        id: Unique identifier, auto-assigned when task is created.
        description: The task description text (non-empty, max 500 chars).
        status: The current status of the task.
        created_at: Timestamp when the task was created.
    """

    id: int
    description: str
    status: TaskStatus
    created_at: datetime
