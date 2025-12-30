from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a task in the todo application.
    Satisfies Phase I Spec §3: Task Data Model.
    """
    id: int
    description: str
    is_completed: bool = False
