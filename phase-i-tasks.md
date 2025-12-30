# Atomic Implementation Tasks: Phase I

This document provides a sequential, atomic task list for implementing Phase I of the "Evolution of Todo" project. All tasks are derived from `phase-i-specification.md` and `phase-i-plan.md`.

## Task List

### T.1 - Data Model Implementation
- **Description:** Implement the `Task` data class.
- **Preconditions:** Project folder created.
- **Expected Output:** A working `Task` model.
- **Artifacts:** `todo_app/models/task.py`
- **References:** Spec §3, Plan §1

### T.2 - In-Memory Service Shell
- **Description:** Create the `TodoService` class with a list for storage and a next_id counter.
- **Preconditions:** T.1 complete.
- **Expected Output:** `TodoService` class skeleton.
- **Artifacts:** `todo_app/services/todo_service.py`
- **References:** Plan §1, §2, §3

### T.3 - Task Creation Persistence (In-Memory)
- **Description:** Implement `add_task(description)` in `TodoService`.
- **Preconditions:** T.2 complete.
- **Expected Output:** Method increases `_next_id` and appends to `self.tasks`.
- **Artifacts:** `todo_app/services/todo_service.py`
- **References:** Spec §5.1, Plan §3

### T.4 - Task Retrieval Logic
- **Description:** Implement `get_all_tasks()` in `TodoService`.
- **Preconditions:** T.3 complete.
- **Expected Output:** Returns the list of tasks.
- **Artifacts:** `todo_app/services/todo_service.py`
- **References:** Spec §5.2

### T.5 - Task ID Search and Error Exceptions
- **Description:** Define `TaskNotFoundError` exception and a private helper `_get_task_by_id(task_id)` in `TodoService`.
- **Preconditions:** T.4 complete.
- **Expected Output:** Throws exception if ID is missing.
- **Artifacts:** `todo_app/services/todo_service.py`
- **References:** Spec §6, Plan §6

### T.6 - Task Update, Delete, and Toggle Logic
- **Description:** Implement `update_task()`, `delete_task()`, and `toggle_task_status()` in `TodoService`.
- **Preconditions:** T.5 complete.
- **Expected Output:** Service methods modify or remove tasks using the ID search helper.
- **Artifacts:** `todo_app/services/todo_service.py`
- **References:** Spec §5.3, §5.4, §5.5

### T.7 - Input Sanitization Utility
- **Description:** Create `InputHandler` to handle `input()` and convert string integers to `int` safely.
- **Preconditions:** None.
- **Expected Output:** Validates numeric choice inputs and non-empty description inputs.
- **Artifacts:** `todo_app/cli/input_handler.py`
- **References:** Plan §5, §6

### T.8 - CLI Menu Display and Loop
- **Description:** Implement the main menu loop and the visual display of the task list.
- **Preconditions:** T.7 complete.
- **Expected Output:** Menu appears and accepts options 1-6.
- **Artifacts:** `todo_app/cli/menu.py`
- **References:** Spec §4, Plan §4

### T.9 - Application Integration
- **Description:** Create `main.py` to instantiate `TodoService` and `Menu`, then start the program.
- **Preconditions:** T.6, T.8 complete.
- **Expected Output:** End-to-end working console application.
- **Artifacts:** `main.py`
- **References:** Plan §1

### T.10 - Error Handling and Boundary Testing
- **Description:** Apply global exception handling in `main.py` or the menu loop to catch `TaskNotFoundError` and display pretty messages.
- **Preconditions:** T.9 complete.
- **Expected Output:** App does not crash on invalid IDs or empty lists.
- **Artifacts:** `todo_app/cli/menu.py`
- **References:** Spec §6
