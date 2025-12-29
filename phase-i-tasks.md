# Phase I Implementation Tasks

**Project:** Evolution of Todo
**Phase:** I - Foundation
**Derived From:** phase-i-specification.md, phase-i-plan.md
**Status:** Ready for Implementation

---

## Task Index

| Task ID | Description | Dependencies | Estimated Size |
|---------|-------------|--------------|----------------|
| T-001 | Create project structure and __init__.py files | None | Small |
| T-002 | Define TaskStatus enum | T-001 | Small |
| T-003 | Define Task dataclass | T-002 | Small |
| T-004 | Implement TodoService constructor and storage | T-003 | Small |
| T-005 | Implement TodoService ID generation | T-004 | Small |
| T-006 | Implement TodoService add_task method | T-005 | Small |
| T-007 | Implement TodoService get_all_tasks method | T-006 | Small |
| T-008 | Implement TodoService get_task_by_id method | T-006 | Small |
| T-009 | Implement TodoService update_task method | T-008 | Small |
| T-010 | Implement TodoService delete_task method | T-008 | Small |
| T-011 | Implement TodoService mark_complete method | T-010 | Small |
| T-012 | Implement TodoService mark_incomplete method | T-010 | Small |
| T-013 | Create InputHandler class for validation | T-001 | Small |
| T-014 | Implement InputHandler menu choice validation | T-013 | Small |
| T-015 | Implement InputHandler task ID validation | T-014 | Small |
| T-016 | Implement InputHandler description validation | T-014 | Small |
| T-017 | Create TodoMenu class structure | T-013, T-004 | Small |
| T-018 | Implement TodoMenu display methods | T-017 | Small |
| T-019 | Implement TodoMenu menu loop | T-018 | Small |
| T-020 | Implement TodoMenu add task handler | T-019, T-006 | Small |
| T-021 | Implement TodoMenu view tasks handler | T-019, T-007 | Small |
| T-022 | Implement TodoMenu update task handler | T-019, T-009 | Small |
| T-023 | Implement TodoMenu delete task handler | T-019, T-010 | Small |
| T-024 | Implement TodoMenu mark complete handler | T-019, T-011 | Small |
| T-025 | Implement TodoMenu mark incomplete handler | T-019, T-012 | Small |
| T-026 | Implement TodoMenu exit handler | T-019 | Small |
| T-027 | Create main.py entry point | T-019, T-026 | Small |
| T-028 | Write unit tests for TodoService | T-012 | Medium |
| T-029 | Write unit tests for InputHandler | T-016 | Medium |
| T-030 | Write unit tests for TodoMenu | T-026 | Medium |

---

## Task Details

---

### T-001: Create Project Structure and __init__.py Files

**Description:**
Create the directory structure for the todo_app package and initialize all `__init__.py` files.

**Preconditions:**
- None

**Expected Output:**
- Directory `todo_app/` created
- Directory `todo_app/models/` created
- Directory `todo_app/services/` created
- Directory `todo_app/cli/` created
- Files `todo_app/__init__.py` created
- Files `todo_app/models/__init__.py` created
- Files `todo_app/services/__init__.py` created
- Files `todo_app/cli/__init__.py` created

**Artifacts to Create:**
- `todo_app/__init__.py`
- `todo_app/models/__init__.py`
- `todo_app/services/__init__.py`
- `todo_app/cli/__init__.py`

**References:**
- Plan Section 2.2: File Structure

---

### T-002: Define TaskStatus Enum

**Description:**
Create the TaskStatus enumeration with INCOMPLETE and COMPLETE values.

**Preconditions:**
- T-001 completed
- `todo_app/models/__init__.py` exists

**Expected Output:**
- File `models/task.py` created with TaskStatus enum
- Enum has INCOMPLETE = "Incomplete" and COMPLETE = "Complete"
- Exported from `models/__init__.py`

**Artifacts to Create:**
- `models/task.py` (new file)

**Artifacts to Modify:**
- `models/__init__.py`

**References:**
- Specification Section 3.2: TaskStatus Enum
- Plan Section 3.3: Task Model Implementation

---

### T-003: Define Task Dataclass

**Description:**
Create the Task dataclass with all required fields: id, description, status, created_at.

**Preconditions:**
- T-002 completed
- `models/task.py` exists with TaskStatus

**Expected Output:**
- Task dataclass defined with all four fields
- Dataclass is properly typed
- Imports dataclass, datetime from standard library

**Artifacts to Modify:**
- `models/task.py`

**References:**
- Specification Section 3.1: Task Entity
- Plan Section 3.3: Task Model Implementation

---

### T-004: Implement TodoService Constructor and Storage

**Description:**
Create the TodoService class with constructor that initializes in-memory task storage.

**Preconditions:**
- T-003 completed
- `services/__init__.py` exists

**Expected Output:**
- File `services/todo_service.py` created
- TodoService class defined
- Constructor initializes `_tasks` as empty list
- Constructor initializes `_next_id` as 1

**Artifacts to Create:**
- `services/todo_service.py` (new file)

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 3.4: In-Memory Storage

---

### T-005: Implement TodoService ID Generation

**Description:**
Add the `_generate_id` private method to TodoService for unique ID generation.

**Preconditions:**
- T-004 completed
- `services/todo_service.py` exists with constructor

**Expected Output:**
- Private method `_generate_id()` implemented
- Returns current `_next_id` value
- Increments `_next_id` after each call
- IDs start at 1 and never repeat

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 3.3: Task ID Generation

---

### T-006: Implement TodoService add_task Method

**Description:**
Implement the `add_task` method to create new tasks with validation.

**Preconditions:**
- T-005 completed
- `_generate_id` method exists

**Expected Output:**
- `add_task(description: str)` method implemented
- Strips whitespace from description
- Generates unique ID using `_generate_id`
- Sets status to TaskStatus.INCOMPLETE
- Sets created_at to current datetime
- Appends task to `_tasks` list
- Returns the created Task

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.1: Add Task Acceptance Criteria
- User Story 2.1: Add Task

---

### T-007: Implement TodoService get_all_tasks Method

**Description:**
Implement the `get_all_tasks` method to retrieve all tasks.

**Preconditions:**
- T-006 completed
- `add_task` method exists

**Expected Output:**
- `get_all_tasks()` method implemented
- Returns a copy of `_tasks` list (to prevent external mutation)
- Tasks returned in ID order (insertion order preserved)

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.2: View Tasks Acceptance Criteria
- User Story 2.2: View Task List

---

### T-008: Implement TodoService get_task_by_id Method

**Description:**
Implement the `get_task_by_id` method for single task lookup.

**Preconditions:**
- T-004 completed (constructor exists)

**Expected Output:**
- `get_task_by_id(task_id: int)` method implemented
- Iterates through `_tasks` to find matching ID
- Returns Task if found, None otherwise
- Returns first match only (IDs are unique)

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 6.2: Invalid Task ID

---

### T-009: Implement TodoService update_task Method

**Description:**
Implement the `update_task` method to modify task descriptions.

**Preconditions:**
- T-008 completed
- `get_task_by_id` method exists

**Expected Output:**
- `update_task(task_id: int, new_description: str)` method implemented
- Finds task by ID using `get_task_by_id`
- Returns False if task not found
- Strips whitespace from new_description
- Updates task description
- Returns True on success

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.3: Update Task Acceptance Criteria
- User Story 2.3: Update Task

---

### T-010: Implement TodoService delete_task Method

**Description:**
Implement the `delete_task` method to remove tasks.

**Preconditions:**
- T-008 completed
- `get_task_by_id` method exists

**Expected Output:**
- `delete_task(task_id: int)` method implemented
- Finds task by ID using `get_task_by_id`
- Returns False if task not found
- Removes task from `_tasks` list
- Returns True on success

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.4: Delete Task Acceptance Criteria
- User Story 2.4: Delete Task

---

### T-011: Implement TodoService mark_complete Method

**Description:**
Implement the `mark_complete` method to change task status to complete.

**Preconditions:**
- T-008 completed
- `get_task_by_id` method exists

**Expected Output:**
- `mark_complete(task_id: int)` method implemented
- Finds task by ID using `get_task_by_id`
- Returns False if task not found
- Updates task status to TaskStatus.COMPLETE
- Returns True on success

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.5: Mark Complete/Incomplete Acceptance Criteria
- User Story 2.5: Mark Task Complete

---

### T-012: Implement TodoService mark_incomplete Method

**Description:**
Implement the `mark_incomplete` method to change task status to incomplete.

**Preconditions:**
- T-008 completed
- `get_task_by_id` method exists

**Expected Output:**
- `mark_incomplete(task_id: int)` method implemented
- Finds task by ID using `get_task_by_id`
- Returns False if task not found
- Updates task status to TaskStatus.INCOMPLETE
- Returns True on success

**Artifacts to Modify:**
- `services/todo_service.py`

**References:**
- Plan Section 4.1: TodoService Methods
- Specification Section 5.5: Mark Complete/Incomplete Acceptance Criteria
- User Story 2.6: Mark Task Incomplete

---

### T-013: Create InputHandler Class for Validation

**Description:**
Create the InputHandler class to handle all user input validation.

**Preconditions:**
- T-001 completed
- `cli/__init__.py` exists

**Expected Output:**
- File `cli/input_handler.py` created
- InputHandler class defined
- Constructor (if needed) initializes validation state

**Artifacts to Create:**
- `cli/input_handler.py` (new file)

**References:**
- Plan Section 5.1: Input Handler

---

### T-014: Implement InputHandler Menu Choice Validation

**Description:**
Implement menu choice validation in InputHandler.

**Preconditions:**
- T-013 completed
- InputHandler class exists

**Expected Output:**
- `get_menu_choice()` method implemented
- Prompts user with "Enter your choice (1-7): "
- Returns int if valid (1-7), None otherwise
- Handles ValueError for non-numeric input
- Error message: "Invalid choice. Please enter a number between 1 and 7."

**Artifacts to Modify:**
- `cli/input_handler.py`

**References:**
- Plan Section 5.1: Input Handler
- Specification Section 6.1: Invalid Menu Selection

---

### T-015: Implement InputHandler Task ID Validation

**Description:**
Implement task ID validation in InputHandler.

**Preconditions:**
- T-014 completed
- `get_menu_choice` method exists

**Expected Output:**
- `get_task_id(prompt: str)` method implemented
- Takes prompt string as parameter
- Returns positive int if valid, None otherwise
- Handles ValueError for non-numeric input
- Error message: "Error: Please enter a valid number."
- Negative number message: "Error: Please enter a positive number."

**Artifacts to Modify:**
- `cli/input_handler.py`

**References:**
- Plan Section 5.1: Input Handler
- Specification Section 6.3: Non-Numeric Task ID

---

### T-016: Implement InputHandler Description Validation

**Description:**
Implement task description validation in InputHandler.

**Preconditions:**
- T-014 completed
- `get_menu_choice` method exists

**Expected Output:**
- `get_task_description()` method implemented
- Prompts user with "Enter task description: "
- Returns stripped string if non-empty and <= 500 chars
- Returns None if empty or whitespace
- Returns None if > 500 characters
- Error message: "Error: Description cannot be empty."
- Length error message: "Error: Description must be 500 characters or less."

**Artifacts to Modify:**
- `cli/input_handler.py`

**References:**
- Plan Section 5.1: Input Handler
- Specification Section 6.6: Empty Description

---

### T-017: Create TodoMenu Class Structure

**Description:**
Create the TodoMenu class with service injection.

**Preconditions:**
- T-004 completed (TodoService exists)
- T-013 completed (InputHandler class exists)

**Expected Output:**
- File `cli/menu.py` created
- TodoMenu class defined
- Constructor accepts TodoService instance
- Constructor initializes InputHandler instance
- Class structure ready for handler methods

**Artifacts to Create:**
- `cli/menu.py` (new file)

**References:**
- Plan Section 5.2: Menu Controller

---

### T-018: Implement TodoMenu Display Methods

**Description:**
Implement menu display methods in TodoMenu.

**Preconditions:**
- T-017 completed
- TodoMenu class exists

**Expected Output:**
- `_display_menu()` method implemented
- Prints menu matching Specification Section 4.1
- Menu includes all 7 options with correct numbers

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.1: Main Menu

---

### T-019: Implement TodoMenu Menu Loop

**Description:**
Implement the main application loop in TodoMenu.

**Preconditions:**
- T-018 completed
- `_display_menu` method exists

**Expected Output:**
- `run()` method implemented
- While True loop continues until exit
- Calls `_display_menu()` each iteration
- Calls `_input.get_menu_choice()` to get input
- Routes to `_handle_choice()` for valid choices
- Returns to menu on None from get_menu_choice

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.2-4.8: CLI Flows

---

### T-020: Implement TodoMenu Add Task Handler

**Description:**
Implement the add task handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-006 completed (TodoService.add_task exists)

**Expected Output:**
- `_handle_add()` method implemented
- Calls `_input.get_task_description()`
- If description is None, returns to menu
- Calls `_service.add_task(description)`
- Prints success message: "Task added successfully. ID: {id}"

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.2: Add Task Flow

---

### T-021: Implement TodoMenu View Tasks Handler

**Description:**
Implement the view tasks handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-007 completed (TodoService.get_all_tasks exists)

**Expected Output:**
- `_handle_view()` method implemented
- Calls `_service.get_all_tasks()`
- If no tasks, prints: "No tasks found. Add a task to get started."
- Otherwise, displays each task with:
  - Status indicator ([ ] for incomplete, [X] for complete)
  - Task ID in brackets
  - Status text (Incomplete/Complete)
  - Task description
- Prints summary: "Total: {n} tasks ({complete} complete, {incomplete} incomplete)"

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.3: View Tasks Flow
- Specification Section 5.2: View Tasks Acceptance Criteria

---

### T-022: Implement TodoMenu Update Task Handler

**Description:**
Implement the update task handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-009 completed (TodoService.update_task exists)
- T-008 completed (TodoService.get_task_by_id exists)

**Expected Output:**
- `_handle_update()` method implemented
- Calls `_input.get_task_id()` with "Enter task ID to update: "
- If ID is None, returns to menu
- Calls `_service.get_task_by_id()` to verify exists
- If task not found, prints: "Error: Task with ID {id} not found."
- Calls `_input.get_task_description()`
- If description is None, returns to menu
- Calls `_service.update_task()` and prints success

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.4: Update Task Flow
- Specification Section 5.3: Update Task Acceptance Criteria

---

### T-023: Implement TodoMenu Delete Task Handler

**Description:**
Implement the delete task handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-010 completed (TodoService.delete_task exists)

**Expected Output:**
- `_handle_delete()` method implemented
- Calls `_input.get_task_id()` with "Enter task ID to delete: "
- If ID is None, returns to menu
- Calls `_service.delete_task()`
- On success, prints: "Task {id} deleted successfully."
- On failure, prints: "Error: Task with ID {id} not found."

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.5: Delete Task Flow
- Specification Section 5.4: Delete Task Acceptance Criteria

---

### T-024: Implement TodoMenu Mark Complete Handler

**Description:**
Implement the mark complete handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-011 completed (TodoService.mark_complete exists)
- T-008 completed (TodoService.get_task_by_id exists)

**Expected Output:**
- `_handle_mark_complete()` method implemented
- Calls `_input.get_task_id()` with "Enter task ID to mark complete: "
- If ID is None, returns to menu
- Gets task via `_service.get_task_by_id()`
- If task not found, prints: "Error: Task with ID {id} not found."
- If task already complete, prints: "Task {id} is already complete."
- Otherwise calls `_service.mark_complete()` and prints success

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.6: Mark Complete Flow
- Specification Section 5.5: Mark Complete/Incomplete Acceptance Criteria

---

### T-025: Implement TodoMenu Mark Incomplete Handler

**Description:**
Implement the mark incomplete handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)
- T-012 completed (TodoService.mark_incomplete exists)
- T-008 completed (TodoService.get_task_by_id exists)

**Expected Output:**
- `_handle_mark_incomplete()` method implemented
- Calls `_input.get_task_id()` with "Enter task ID to mark incomplete: "
- If ID is None, returns to menu
- Gets task via `_service.get_task_by_id()`
- If task not found, prints: "Error: Task with ID {id} not found."
- If task already incomplete, prints: "Task {id} is already incomplete."
- Otherwise calls `_service.mark_incomplete()` and prints success

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.7: Mark Incomplete Flow
- Specification Section 5.5: Mark Complete/Incomplete Acceptance Criteria

---

### T-026: Implement TodoMenu Exit Handler

**Description:**
Implement the exit handler in TodoMenu.

**Preconditions:**
- T-019 completed (menu loop exists)

**Expected Output:**
- `_handle_exit()` method implemented
- Prints: "Goodbye!"
- Returns (allowing loop to break in run())

**Artifacts to Modify:**
- `cli/menu.py`

**References:**
- Plan Section 5.2: Menu Controller
- Specification Section 4.8: Exit Flow

---

### T-027: Create main.py Entry Point

**Description:**
Create the application entry point file.

**Preconditions:**
- T-019 completed (TodoMenu.run exists)
- T-026 completed (TodoMenu exit handling exists)

**Expected Output:**
- File `main.py` created
- Imports TodoMenu from cli.menu
- Imports TodoService from services.todo_service
- `main()` function creates service and menu
- `if __name__ == "__main__":` block calls main()

**Artifacts to Create:**
- `main.py` (new file)

**References:**
- Plan Section 6.1: main.py
- Specification Section 7.3: Entry Point

---

### T-028: Write Unit Tests for TodoService

**Description:**
Write comprehensive unit tests for TodoService methods.

**Preconditions:**
- T-012 completed (all TodoService methods exist)

**Expected Output:**
- Test file (e.g., `tests/test_todo_service.py`)
- Tests for add_task: verifies ID generation, status, description
- Tests for get_all_tasks: verifies order, immutability
- Tests for get_task_by_id: verifies found and not-found cases
- Tests for update_task: verifies update, not-found case
- Tests for delete_task: verifies removal, not-found case
- Tests for mark_complete: verifies status change, already-complete case
- Tests for mark_incomplete: verifies status change, already-incomplete case
- Coverage target: 80%+

**Artifacts to Create:**
- `tests/test_todo_service.py`

**References:**
- Plan Section 8.1: Implementation Tasks (T-018)
- Specification Section 5: Acceptance Criteria

---

### T-029: Write Unit Tests for InputHandler

**Description:**
Write comprehensive unit tests for InputHandler validation.

**Preconditions:**
- T-016 completed (all InputHandler methods exist)

**Expected Output:**
- Test file (e.g., `tests/test_input_handler.py`)
- Tests for get_menu_choice: valid and invalid inputs
- Tests for get_task_id: valid, invalid, negative inputs
- Tests for get_task_description: valid, empty, too-long inputs
- Coverage target: 80%+

**Artifacts to Create:**
- `tests/test_input_handler.py`

**References:**
- Plan Section 8.1: Implementation Tasks (T-019)
- Specification Section 6: Error Cases

---

### T-030: Write Unit Tests for TodoMenu

**Description:**
Write comprehensive unit tests for TodoMenu handlers.

**Preconditions:**
- T-026 completed (all TodoMenu handlers exist)

**Expected Output:**
- Test file (e.g., `tests/test_todo_menu.py`)
- Tests for menu display and loop
- Tests for add task handler interaction with service
- Tests for view tasks handler output
- Tests for update task handler interaction
- Tests for delete task handler interaction
- Tests for mark complete handler interaction
- Tests for mark incomplete handler interaction
- Tests for exit handler
- Coverage target: 80%+

**Artifacts to Create:**
- `tests/test_todo_menu.py`

**References:**
- Plan Section 8.1: Implementation Tasks (T-020)
- Specification Section 4: CLI Interface

---

## Task Dependency Graph

```
T-001 ──┬─> T-002 ──> T-003 ──> T-004 ──> T-005 ──> T-006 ──> T-007 ──> ...
        │                              │
        │                              └──> T-008 ──> T-009 ──> ...
        │                              │
        │                              └──> T-010 ──> ...
        │                              │
        │                              └──> T-011 ──> ...
        │                              │
        │                              └──> T-012
        │
        └──> T-013 ──> T-014 ──> T-015 ──> T-016
                      │
                      └──> T-017 ──> T-018 ──> T-019 ──> T-020
                                                   │
                                                   ├──> T-021
                                                   │
                                                   ├──> T-022
                                                   │
                                                   ├──> T-023
                                                   │
                                                   ├──> T-024
                                                   │
                                                   ├──> T-025
                                                   │
                                                   └──> T-026 ──> T-027

        T-012 ──────────────────────────────> T-028 (Testing)
        T-016 ──────────────────────────────> T-029 (Testing)
        T-026 ──────────────────────────────> T-030 (Testing)
```

---

## Sequential Implementation Order

1. T-001: Create project structure
2. T-002: TaskStatus enum
3. T-003: Task dataclass
4. T-004: TodoService constructor
5. T-005: ID generation
6. T-006: add_task
7. T-007: get_all_tasks
8. T-008: get_task_by_id
9. T-009: update_task
10. T-010: delete_task
11. T-011: mark_complete
12. T-012: mark_incomplete
13. T-013: InputHandler class
14. T-014: Menu choice validation
15. T-015: Task ID validation
16. T-016: Description validation
17. T-017: TodoMenu class
18. T-018: Menu display
19. T-019: Menu loop
20. T-020: Add task handler
21. T-021: View tasks handler
22. T-022: Update task handler
23. T-023: Delete task handler
24. T-024: Mark complete handler
25. T-025: Mark incomplete handler
26. T-026: Exit handler
27. T-027: main.py entry point
28. T-028: TodoService tests
29. T-029: InputHandler tests
30. T-030: TodoMenu tests

---

**Task Version:** 1.0
**Total Tasks:** 30
**Status:** Ready for implementation
