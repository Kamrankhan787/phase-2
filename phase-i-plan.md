# Phase I Technical Plan: Foundation

**Project:** Evolution of Todo
**Phase:** I - Foundation
**Derived From:** phase-i-specification.md, sp.constitution
**Status:** Technical Implementation Plan
**Scope:** In-Memory Console Application

---

## 1. Plan Overview

This technical plan describes HOW to implement the approved Phase I specification. It derives directly from the specification and follows constitutional principles of clean architecture and separation of concerns.

### 1.1 Planning Principles

Per Constitution Article I, this plan:
- Derives from approved specifications
- Breaks work into atomic, traceable tasks
- Specifies technology choices explicitly
- Includes acceptance criteria for each task

### 1.2 Scope Boundaries

This plan implements ONLY Phase I specification requirements. No features from future phases are included. No "nice-to-have" additions. Strict adherence to specification.

---

## 2. Application Architecture

### 2.1 High-Level Structure

The application follows a simple layered architecture:

```
┌─────────────────────────────────┐
│          main.py                │  Entry point
├─────────────────────────────────┤
│           CLI Layer             │  User interaction
│      (cli/menu.py, cli/io.py)   │
├─────────────────────────────────┤
│        Service Layer            │  Business logic
│     (services/todo_service.py)  │
├─────────────────────────────────┤
│         Model Layer             │  Data structures
│      (models/task.py)           │
└─────────────────────────────────┘
```

### 2.2 File Structure

```
todo_app/
├── __init__.py
├── main.py                       # Application entry point
├── models/
│   ├── __init__.py
│   └── task.py                   # Task, TaskStatus classes
├── services/
│   ├── __init__.py
│   └── todo_service.py           # Business logic (CRUD operations)
└── cli/
    ├── __init__.py
    ├── menu.py                   # Menu display and navigation
    └── input_handler.py          # User input validation
```

### 2.3 Layer Responsibilities

| Layer | Responsibility | Examples |
|-------|----------------|----------|
| `main.py` | Application bootstrap | Create service, run menu |
| `cli/menu.py` | User interaction | Display menu, route choices |
| `cli/input_handler.py` | Input validation | Validate IDs, sanitize text |
| `services/todo_service.py` | Business logic | CRUD operations, ID generation |
| `models/task.py` | Data structures | Task class, TaskStatus enum |

---

## 3. Data Layer Implementation

### 3.1 In-Memory Storage

Per Specification Section 3.4, tasks are stored in-memory:

**File:** `services/todo_service.py`

```python
from typing import List
from models.task import Task, TaskStatus

class TodoService:
    """Handles in-memory task storage and operations."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1
```

**Rationale:** The specification requires no persistence beyond runtime. A simple list with a counter satisfies all requirements.

### 3.2 Task ID Generation

Per Specification Section 3.3, IDs are auto-assigned:

```python
def _generate_id(self) -> int:
    """Generate the next available task ID."""
    current_id = self._next_id
    self._next_id += 1
    return current_id
```

**ID Strategy:**
- Starts at 1 (Specification: "auto-incrementing starting at 1")
- Never reused (Specification: "The task ID is not reused")
- Assigned at task creation time
- Incremented regardless of deletions

### 3.3 Task Model Implementation

**File:** `models/task.py`

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"

@dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    description: str
    status: TaskStatus
    created_at: datetime
```

**Validation Notes:**
- `id`: System-assigned, no validation needed
- `description`: Validated at CLI input level, not in model
- `status`: Enum enforces valid values
- `created_at`: Generated at construction time

---

## 4. Service Layer Implementation

### 4.1 TodoService Methods

The service layer contains all business logic:

```python
class TodoService:
    """Service for managing todo tasks."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Create a new task with given description."""
        # Strip whitespace from description
        description = description.strip()
        # Generate ID
        task_id = self._generate_id()
        # Create task with INCOMPLETE status and current timestamp
        task = Task(
            id=task_id,
            description=description,
            status=TaskStatus.INCOMPLETE,
            created_at=datetime.now()
        )
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks ordered by ID."""
        return self._tasks.copy()  # Return copy to prevent external mutation

    def get_task_by_id(self, task_id: int) -> Task | None:
        """Return task with given ID, or None if not found."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> bool:
        """Update task description. Returns True if successful."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.description = new_description.strip()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID. Returns True if successful."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        self._tasks.remove(task)
        return True

    def mark_complete(self, task_id: int) -> bool:
        """Mark task as complete. Returns True if successful."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.status = TaskStatus.COMPLETE
        return True

    def mark_incomplete(self, task_id: int) -> bool:
        """Mark task as incomplete. Returns True if successful."""
        task = self.get_task_by_id(task_id)
        if task is None:
            return False
        task.status = TaskStatus.INCOMPLETE
        return True
```

### 4.2 Service Method Contracts

| Method | Parameters | Returns | Side Effects |
|--------|------------|---------|--------------|
| `add_task` | `description: str` | `Task` | Appends to `_tasks` |
| `get_all_tasks` | None | `List[Task]` | None (returns copy) |
| `get_task_by_id` | `task_id: int` | `Task \| None` | None |
| `update_task` | `task_id: int`, `new_description: str` | `bool` | Modifies task |
| `delete_task` | `task_id: int` | `bool` | Removes from `_tasks` |
| `mark_complete` | `task_id: int` | `bool` | Modifies status |
| `mark_incomplete` | `task_id: int` | `bool` | Modifies status |

---

## 5. CLI Layer Implementation

### 5.1 Input Handler

**File:** `cli/input_handler.py`

```python
class InputHandler:
    """Handles user input validation and parsing."""

    def get_menu_choice(self) -> int | None:
        """
        Get and validate menu selection.
        Returns None on invalid input after 3 attempts.
        """
        try:
            choice = int(input("Enter your choice (1-7): ").strip())
            if 1 <= choice <= 7:
                return choice
            print("Invalid choice. Please enter a number between 1 and 7.")
            return None
        except ValueError:
            print("Invalid choice. Please enter a number between 1 and 7.")
            return None

    def get_task_id(self, prompt: str) -> int | None:
        """
        Get and validate a task ID.
        Returns None on invalid input.
        """
        try:
            task_id = int(input(prompt).strip())
            if task_id > 0:
                return task_id
            print("Error: Please enter a positive number.")
            return None
        except ValueError:
            print("Error: Please enter a valid number.")
            return None

    def get_task_description(self) -> str | None:
        """
        Get and validate task description.
        Returns None if description is empty or whitespace.
        """
        description = input("Enter task description: ").strip()
        if not description:
            print("Error: Description cannot be empty.")
            return None
        if len(description) > 500:
            print("Error: Description must be 500 characters or less.")
            return None
        return description
```

### 5.2 Menu Controller

**File:** `cli/menu.py`

```python
from cli.input_handler import InputHandler
from services.todo_service import TodoService

class TodoMenu:
    """Handles menu display and user interaction."""

    def __init__(self, service: TodoService):
        self._service = service
        self._input = InputHandler()

    def run(self):
        """Main application loop."""
        while True:
            self._display_menu()
            choice = self._input.get_menu_choice()
            if choice is None:
                continue
            if choice == 7:
                self._handle_exit()
                break
            self._handle_choice(choice)

    def _display_menu(self):
        """Display the main menu."""
        print("\n=== Todo Application ===\n")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete")
        print("6. Mark Task Incomplete")
        print("7. Exit\n")

    def _handle_choice(self, choice: int):
        """Route to appropriate handler."""
        handlers = {
            1: self._handle_add,
            2: self._handle_view,
            3: self._handle_update,
            4: self._handle_delete,
            5: self._handle_mark_complete,
            6: self._handle_mark_incomplete,
        }
        handler = handlers.get(choice)
        if handler:
            handler()

    def _handle_add(self):
        """Handle add task flow per spec 4.2."""
        description = self._input.get_task_description()
        if description is None:
            return
        task = self._service.add_task(description)
        print(f"Task added successfully. ID: {task.id}")

    def _handle_view(self):
        """Handle view tasks flow per spec 4.3."""
        tasks = self._service.get_all_tasks()
        if not tasks:
            print("\nNo tasks found. Add a task to get started.")
            return

        print("\n=== Your Tasks ===\n")
        complete_count = 0
        for task in tasks:
            status_mark = "[ ]" if task.status == TaskStatus.INCOMPLETE else "[X]"
            status_text = "Incomplete" if task.status == TaskStatus.INCOMPLETE else "Complete"
            print(f"{status_mark} [{task.id}] {status_text}: {task.description}")
            if task.status == TaskStatus.COMPLETE:
                complete_count += 1

        incomplete_count = len(tasks) - complete_count
        print(f"\nTotal: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")

    def _handle_update(self):
        """Handle update task flow per spec 4.4."""
        task_id = self._input.get_task_id("Enter task ID to update: ")
        if task_id is None:
            return

        task = self._service.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        description = self._input.get_task_description()
        if description is None:
            return

        if self._service.update_task(task_id, description):
            print(f"Task {task_id} updated successfully.")

    def _handle_delete(self):
        """Handle delete task flow per spec 4.5."""
        task_id = self._input.get_task_id("Enter task ID to delete: ")
        if task_id is None:
            return

        if self._service.delete_task(task_id):
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _handle_mark_complete(self):
        """Handle mark complete flow per spec 4.6."""
        task_id = self._input.get_task_id("Enter task ID to mark complete: ")
        if task_id is None:
            return

        task = self._service.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        if task.status == TaskStatus.COMPLETE:
            print(f"Task {task_id} is already complete.")
            return

        if self._service.mark_complete(task_id):
            print(f"Task {task_id} marked as complete.")

    def _handle_mark_incomplete(self):
        """Handle mark incomplete flow per spec 4.7."""
        task_id = self._input.get_task_id("Enter task ID to mark incomplete: ")
        if task_id is None:
            return

        task = self._service.get_task_by_id(task_id)
        if task is None:
            print(f"Error: Task with ID {task_id} not found.")
            return

        if task.status == TaskStatus.INCOMPLETE:
            print(f"Task {task_id} is already incomplete.")
            return

        if self._service.mark_incomplete(task_id):
            print(f"Task {task_id} marked as incomplete.")

    def _handle_exit(self):
        """Handle exit flow per spec 4.8."""
        print("Goodbye!")
```

---

## 6. Entry Point

### 6.1 main.py

**File:** `main.py`

```python
from cli.menu import TodoMenu
from services.todo_service import TodoService

def main():
    """Application entry point."""
    service = TodoService()
    menu = TodoMenu(service)
    menu.run()

if __name__ == "__main__":
    main()
```

---

## 7. Error Handling Strategy

### 7.1 Error Handling Layers

```
┌─────────────────────────────────────────────────────────┐
│ Input Validation (cli/input_handler.py)                │
│ - Invalid menu choices                                 │
│ - Non-numeric task IDs                                 │
│ - Empty descriptions                                   │
│ - Descriptions > 500 chars                             │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ Service Validation (services/todo_service.py)          │
│ - Task not found (by ID)                               │
│ - Task already complete/incomplete                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ CLI Presentation (cli/menu.py)                         │
│ - Convert None returns to user-friendly messages       │
│ - Display appropriate error/success messages           │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Error Response Matrix

| Input Condition | Error Message | Returns To |
|-----------------|---------------|------------|
| Non-numeric menu choice | "Invalid choice. Please enter a number between 1 and 7." | Menu |
| Out-of-range menu choice | "Invalid choice. Please enter a number between 1 and 7." | Menu |
| Non-numeric task ID | "Error: Please enter a valid number." | Menu |
| Negative task ID | "Error: Please enter a positive number." | Menu |
| Empty description | "Error: Description cannot be empty." | Menu |
| Description > 500 chars | "Error: Description must be 500 characters or less." | Menu |
| Task not found | "Error: Task with ID {id} not found." | Menu |
| Already complete | "Task {id} is already complete." | Menu |
| Already incomplete | "Task {id} is already incomplete." | Menu |

### 7.3 Exception Handling

Per Constitution clean architecture principles, this implementation:
- Uses return values (`bool`, `Task | None`) for error conditions
- Does not raise exceptions for expected error cases
- Only raises exceptions for truly unexpected conditions
- Keeps error handling at the appropriate layer

---

## 8. Task Breakdown

### 8.1 Implementation Tasks

| Task ID | Component | Description | Acceptance Criteria |
|---------|-----------|-------------|---------------------|
| T-001 | models/task.py | Define TaskStatus enum | Enum has INCOMPLETE, COMPLETE values |
| T-002 | models/task.py | Define Task dataclass | Dataclass has id, description, status, created_at |
| T-003 | services/todo_service.py | Implement TodoService constructor | Initializes empty list, next_id = 1 |
| T-004 | services/todo_service.py | Implement add_task() | Returns Task with unique ID, INCOMPLETE status |
| T-005 | services/todo_service.py | Implement get_all_tasks() | Returns ordered list copy |
| T-006 | services/todo_service.py | Implement get_task_by_id() | Returns Task or None |
| T-007 | services/todo_service.py | Implement update_task() | Updates description, returns bool |
| T-008 | services/todo_service.py | Implement delete_task() | Removes task, returns bool |
| T-009 | services/todo_service.py | Implement mark_complete() | Updates status, returns bool |
| T-010 | services/todo_service.py | Implement mark_incomplete() | Updates status, returns bool |
| T-011 | cli/input_handler.py | Implement get_menu_choice() | Validates 1-7, returns int or None |
| T-012 | cli/input_handler.py | Implement get_task_id() | Validates positive int, returns int or None |
| T-013 | cli/input_handler.py | Implement get_task_description() | Validates non-empty, max 500 |
| T-014 | cli/menu.py | Implement TodoMenu class | Displays menu, routes choices |
| T-015 | cli/menu.py | Implement menu handlers | Each handler calls appropriate service method |
| T-016 | main.py | Implement entry point | Creates service, runs menu |
| T-017 | All | Create __init__.py files | Package structure complete |

### 8.2 Testing Tasks

| Task ID | Description | Target |
|---------|-------------|--------|
| T-018 | Unit tests for TodoService | 80%+ coverage |
| T-019 | Unit tests for InputHandler | 80%+ coverage |
| T-020 | Unit tests for TodoMenu | 80%+ coverage |

---

## 9. Dependencies

### 9.1 Python Standard Library Only

Per Specification Section 7.1, only standard library:

```python
# Used modules
from dataclasses import dataclass      # Task definition
from datetime import datetime          # Timestamps
from enum import Enum                  # TaskStatus
from typing import List, Optional      # Type hints
```

### 9.2 No External Dependencies

- No `pip install` required
- No third-party packages
- No database drivers
- No web frameworks
- No AI/ML libraries

---

## 10. Verification Checklist

### 10.1 Implementation Verification

- [ ] All T-001 through T-017 tasks complete
- [ ] Code passes all tests (T-018 through T-020)
- [ ] Application runs without errors
- [ ] All specification acceptance criteria met
- [ ] No out-of-scope features present

### 10.2 Architecture Verification

- [ ] Clean architecture principles followed
- [ ] Separation of concerns maintained
- [ ] No layer violations (CLI calls service, service manages data)
- [ ] Stateless services (no in-memory state beyond session)

---

## 11. Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Input validation bypass | Low | InputHandler validates all user input |
| Task ID collision | None | Counter-based ID generation, never reuses |
| Race conditions | None | Single-user, single-threaded |
| Memory exhaustion | Very Low | Simple list, user can delete tasks |

---

**Plan Version:** 1.0
**Derived From:** phase-i-specification.md, sp.constitution
**Next Phase:** Task generation upon approval
