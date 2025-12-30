# Evolution of Todo: Phase I Specification
## Project: In-Memory Python Console Application

### 1. Scope and Vision
Phase I focuses on the absolute foundation of the "Evolution of Todo" project. It delivers a simple, single-user, in-memory CLI application for managing a task list. No persistence, networking, or databases are permitted.

### 2. User Stories
| ID | User Story |
|----|------------|
| US.1 | As a user, I want to add a task with a description so I can remember what I need to do. |
| US.2 | As a user, I want to view all my tasks in a list so I can see what is on my plate. |
| US.3 | As a user, I want to update a task's description if my requirements change. |
| US.4 | As a user, I want to delete a task if it's no longer relevant. |
| US.5 | As a user, I want to mark a task as complete or incomplete to track my progress. |

### 3. Task Data Model
The application will manage `Task` objects with the following fields:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| `id` | Integer | Unique identifier for the task | Positive, auto-incrementing |
| `description` | String | What needs to be done | Non-empty, max 200 chars |
| `is_completed` | Boolean | Status of the task | Default: False |

### 4. CLI Interaction Flow
The application will operate via a loop-based menu system:
1. **Main Menu:**
   - [1] View Tasks
   - [2] Add Task
   - [3] Update Task
   - [4] Delete Task
   - [5] Toggle Completion status
   - [6] Exit
2. **Input Handling:**
   - Numerical selection for menu options.
   - String input for descriptions.
   - Numerical input for selecting Task IDs.

### 5. Feature Specifications

#### 5.1 Add Task
- **Input:** Description (String).
- **Processing:** Assign next available ID, set `is_completed` to False.
- **Success:** Confirmation message with the assigned ID.
- **Fail:** Error message if description is empty or whitespace.

#### 5.2 View Task List
- **Input:** None.
- **Processing:** Retrieve all tasks from in-memory storage.
- **Output:** A formatted list (or table) showing ID, Status ([ ] or [X]), and Description.
- **Empty State:** Inform the user "No tasks found."

#### 5.3 Update Task
- **Input:** Task ID (Integer), New Description (String).
- **Processing:** Find task by ID. Update description field.
- **Success:** Confirmation message.
- **Fail:** Error if ID doesn't exist; Error if new description is empty.

#### 5.4 Delete Task
- **Input:** Task ID (Integer).
- **Processing:** Find and remove task from memory.
- **Success:** Confirmation message.
- **Fail:** Error if ID doesn't exist.

#### 5.5 Toggle Completion status
- **Input:** Task ID (Integer).
- **Processing:** Switch `is_completed` (True -> False or False -> True).
- **Success:** Message showing new status.
- **Fail:** Error if ID doesn't exist.

### 6. Error Cases and Validation
- **Invalid Menu Choice:** "Invalid option. Please choose 1-6."
- **Empty Description:** "Task description cannot be empty."
- **Task Not Found:** "Error: Task with ID [ID] not found."
- **Invalid ID Format:** "Error: Please enter a valid numerical ID."

### 7. Technical Constraints (Phase I ONLY)
- Language: Python 3.x
- Storage: In-memory (List or Dictionary)
- Dependencies: None (Standard library ONLY)
- Architecture: Simple modular structure (e.g., `main.py`, `models.py`, `service.py`)

### 8. Acceptance Criteria
1. The application starts without errors.
2. User can perform all 5 CRUD operations successfully.
3. State is maintained throughout the session but cleared on exit.
4. Input validation prevents empty descriptions and invalid IDs from crashing the app.
5. List view displays tasks clearly with their current completion status.
