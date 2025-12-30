# Phase I Technical Plan: Foundation

This technical plan describes the implementation strategy for Phase I of the "Evolution of Todo" project. It is strictly derived from `phase-i-specification.md` and adheres to the `sp.constitution`.

## 1. High-Level Architecture
The application will follow a simplified Clean Architecture pattern to ensure a clean separation of concerns, even within a minimal CLI application.

- **Models (`todo_app/models/task.py`):** Defines the `Task` data structure.
- **Service Layer (`todo_app/services/todo_service.py`):** Manages the in-memory task list and business logic (CRUD, validation).
- **CLI Layer (`todo_app/cli/`):** Handles user input/output and the menu loop.
- **Entry Point (`main.py`):** Initializes the service and starts the CLI loop.

## 2. In-Memory Data Structures
- **Storage:** The `TodoService` will maintain tasks in a Python **List** (`self.tasks = []`).
- **Reasoning:** A list is sufficient for Phase I as it maintains order and is easy to iterate over for display and ID searches.

## 3. Task Identification Strategy
- **Mechanism:** A private counter variable (`self._next_id`) within the `TodoService` class.
- **Initial Value:** 1.
- **Increment:** Each time a new task is added, the current value of `_next_id` is assigned to the task, and then the counter is incremented by 1.
- **Stability:** Once assigned, a task ID never changes. If a task is deleted, its ID is not reused during the current session.

## 4. CLI Control Flow
The application will use a `while True` loop to keep the program running until the "Exit" option is chosen.

- **Menu Loop:**
  1. Display the main menu.
  2. Prompt for user input (choice).
  3. Validate choice is a number between 1 and 6.
  4. Dispatch to the appropriate service method or nested input prompts.
  5. Handle exceptions (e.g., TaskNotFound, ValueError).
  6. Repeat.

## 5. Separation of Responsibilities
| Component | Responsibility |
|-----------|----------------|
| `main.py` | Infrastructure setup and start. |
| `Task` (Model) | Pure data container. |
| `TodoService` | Storage and logic. Only performs operations on data. Does NOT interact with the terminal. |
| `Menu` (CLI) | Presentation logic. Displays data to the user. |
| `InputHandler` | sanitizes and validates raw user input from `input()`. |

## 6. Error Handling Strategy
- **Internal Errors:** `TodoService` will raise custom exceptions (e.g., `TaskNotFoundError`, `InvalidTaskError`) when logic rules are violated.
- **Input Errors:** The `InputHandler` will use `try-except` blocks around `int()` conversions to catch `ValueError`, prompting the user to re-enter valid data.
- **Graceful Failure:** The main loop will wrap service calls in `try-except` blocks to display user-friendly error messages instead of stack traces.

## 7. Compliance Checklist
- [x] No Databases? Yes (Memory only).
- [x] No Files? Yes (No persistence).
- [x] No Web? Yes (CLI only).
- [x] SDD Flow? Yes (Plan derived from Spec).
- [x] Single User? Yes.
