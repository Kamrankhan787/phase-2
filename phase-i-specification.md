# Phase I Specification: Foundation

**Project:** Evolution of Todo
**Phase:** I - Foundation
**Status:** Approved for Implementation
**Scope:** In-Memory Console Application

---

## 1. Overview

This specification defines Phase I of the Evolution of Todo project: a basic in-memory console application for task management. Phase I establishes the foundational codebase and patterns that subsequent phases will build upon.

### 1.1 Phase I Objectives

1. Create a working todo application with core CRUD operations
2. Establish development patterns and code organization
3. Validate the spec-driven development process
4. Provide baseline for Phase II agent integration

### 1.2 Scope Boundaries

Phase I includes ONLY the features and behaviors defined in this specification. The following are explicitly OUT OF SCOPE:

- Any database integration (Phase V scope)
- File-based persistence (Phase V scope)
- User authentication (future phase scope)
- Web API or HTTP server (future phase scope)
- AI or agent features (Phase II scope)
- Multi-user functionality (future phase scope)
- Any advanced features not listed below

---

## 2. User Stories

### 2.1 Add Task

**As a** user,
**I want to** create a new task with a description,
**So that** I can track things I need to do.

**Scenario:** Adding a valid task
- Given the application is running
- When I choose to add a task
- And I provide a non-empty description
- Then the task is created with status "incomplete"
- And the task is assigned a unique ID
- And the task is added to my task list

### 2.2 View Task List

**As a** user,
**I want to** see all my current tasks,
**So that** I can review what I need to do.

**Scenario:** Viewing tasks when list is empty
- Given I have no tasks
- When I choose to view tasks
- Then I see a message indicating no tasks exist

**Scenario:** Viewing tasks with items
- Given I have one or more tasks
- When I choose to view tasks
- Then I see each task with its ID, description, and status
- And incomplete tasks are clearly distinguished from complete tasks

### 2.3 Update Task

**As a** user,
**I want to** change a task's description,
**So that** I can correct or refine my tasks.

**Scenario:** Updating an existing task
- Given a task with ID 1 exists
- When I choose to update task 1
- And I provide a new non-empty description
- Then the task's description is changed
- And the task's status remains unchanged

### 2.4 Delete Task

**As a** user,
**I want to** remove a task from my list,
**So that** I can get rid of tasks I no longer need.

**Scenario:** Deleting an existing task
- Given a task with ID 1 exists
- When I choose to delete task 1
- Then the task is removed from the list
- And the task ID is not reused

### 2.5 Mark Task Complete

**As a** user,
**I want to** mark a task as completed,
**So that** I can track my progress.

**Scenario:** Marking a task complete
- Given a task with ID 1 exists with status "incomplete"
- When I choose to mark task 1 as complete
- Then the task's status changes to "complete"

### 2.6 Mark Task Incomplete

**As a** user,
**I want to** mark a completed task as incomplete,
**So that** I can reopen a task if needed.

**Scenario:** Marking a task incomplete
- Given a task with ID 1 exists with status "complete"
- When I choose to mark task 1 as incomplete
- Then the task's status changes to "incomplete"

---

## 3. Data Model

### 3.1 Task Entity

```python
@dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int                    # Unique identifier, auto-assigned
    description: str           # Task description text
    status: TaskStatus         # Current status
    created_at: datetime       # When task was created (runtime clock)
```

### 3.2 TaskStatus Enum

```python
from enum import Enum

class TaskStatus(Enum):
    """Enumeration of possible task statuses."""
    INCOMPLETE = "Incomplete"
    COMPLETE = "Complete"
```

### 3.3 Field Constraints

| Field | Type | Constraint | Validation |
|-------|------|------------|------------|
| id | int | Unique, auto-incrementing starting at 1 | System-assigned |
| description | str | Non-empty, max 500 characters | Required, strip whitespace |
| status | TaskStatus | Must be a valid TaskStatus value | System-enforced |
| created_at | datetime | Auto-set on creation | System-assigned |

### 3.4 In-Memory Storage

- Tasks are stored in a Python list: `tasks: List[Task]`
- Task counter stored as: `next_task_id: int = 1`
- Data persists only for the duration of the application session
- No file or database persistence in Phase I

---

## 4. CLI Interface

### 4.1 Main Menu

The application displays a menu with the following options:

```
=== Todo Application ===

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Task Complete
6. Mark Task Incomplete
7. Exit

Enter your choice (1-7):
```

### 4.2 Add Task Flow

```
1. User selects "Add Task"
2. Application prompts: "Enter task description:"
3. User enters description
4. If description is empty/whitespace:
   - Display: "Error: Description cannot be empty."
   - Return to main menu
5. Otherwise:
   - Create task with description
   - Display: "Task added successfully. ID: {id}"
   - Return to main menu
```

### 4.3 View Tasks Flow

```
1. User selects "View Tasks"
2. If no tasks exist:
   - Display: "No tasks found. Add a task to get started."
3. Otherwise, display tasks in ID order:
   ```
   === Your Tasks ===

   [1] Incomplete: Buy groceries
   [2] Complete:   Finish report
   [3] Incomplete: Call dentist

   Total: 3 tasks (1 complete, 2 incomplete)
   ```
4. Return to main menu
```

### 4.4 Update Task Flow

```
1. User selects "Update Task"
2. Application prompts: "Enter task ID to update:"
3. User enters ID
4. If ID is invalid (non-numeric or not found):
   - Display: "Error: Task with ID {id} not found."
   - Return to main menu
5. Application prompts: "Enter new description:"
6. User enters description
7. If description is empty/whitespace:
   - Display: "Error: Description cannot be empty."
   - Return to main menu
8. Otherwise:
   - Update task description
   - Display: "Task {id} updated successfully."
   - Return to main menu
```

### 4.5 Delete Task Flow

```
1. User selects "Delete Task"
2. Application prompts: "Enter task ID to delete:"
3. User enters ID
4. If ID is invalid:
   - Display: "Error: Task with ID {id} not found."
   - Return to main menu
5. Otherwise:
   - Remove task from list
   - Display: "Task {id} deleted successfully."
   - Return to main menu
```

### 4.6 Mark Complete Flow

```
1. User selects "Mark Task Complete"
2. Application prompts: "Enter task ID to mark complete:"
3. User enters ID
4. If ID is invalid:
   - Display: "Error: Task with ID {id} not found."
   - Return to main menu
5. If task is already complete:
   - Display: "Task {id} is already complete."
   - Return to main menu
6. Otherwise:
   - Change status to COMPLETE
   - Display: "Task {id} marked as complete."
   - Return to main menu
```

### 4.7 Mark Incomplete Flow

```
1. User selects "Mark Task Incomplete"
2. Application prompts: "Enter task ID to mark incomplete:"
3. User enters ID
4. If ID is invalid:
   - Display: "Error: Task with ID {id} not found."
   - Return to main menu
5. If task is already incomplete:
   - Display: "Task {id} is already incomplete."
   - Return to main menu
6. Otherwise:
   - Change status to INCOMPLETE
   - Display: "Task {id} marked as incomplete."
   - Return to main menu
```

### 4.8 Exit Flow

```
1. User selects "Exit"
2. Display: "Goodbye!"
3. Application terminates
```

---

## 5. Acceptance Criteria

### 5.1 Add Task Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| Task is created with unique ID | Run add task twice, verify IDs are 1 and 2 |
| New task has "Incomplete" status | Add task, view tasks, verify status |
| Empty description rejected | Add task with empty input, verify error message |
| Whitespace-only description rejected | Add task with "   ", verify error message |
| Description is trimmed of whitespace | Add task with "  buy milk  ", view shows "buy milk" |
| Description max 500 characters | Add task with 501 chars, verify rejection |

### 5.2 View Tasks Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| Empty list shows helpful message | Run with no tasks, verify message |
| Tasks shown in ID order | Add tasks 1, 2, 3, view shows 1, 2, 3 |
| Complete tasks marked clearly | Mark task complete, view shows "Complete" |
| Incomplete tasks marked clearly | Add task, view shows "Incomplete" |
| Summary count displayed | With 3 tasks (1 complete), shows "Total: 3 (1 complete, 2 incomplete)" |

### 5.3 Update Task Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| Invalid ID shows error | Update task 999, verify error message |
| Empty description rejected | Update with empty input, verify error message |
| Status unchanged after update | Mark complete, update, verify still complete |
| Description actually changed | Update task, view shows new description |

### 5.4 Delete Task Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| Invalid ID shows error | Delete task 999, verify error message |
| Task removed from list | Delete task 1, view no longer shows task 1 |
| Other tasks unaffected | Delete task 1, verify task 2 still exists |
| Deleted ID not reused | Delete task 1, add task, verify new ID is 2 |

### 5.5 Mark Complete/Incomplete Acceptance Criteria

| Criterion | Verification |
|-----------|--------------|
| Invalid ID shows error | Mark complete task 999, verify error |
| Already complete shows message | Mark complete, then mark complete again |
| Status actually changes | Mark complete, view shows "Complete" |
| Can toggle back and forth | Complete, then incomplete, then complete |

---

## 6. Error Cases

### 6.1 Invalid Menu Selection

```
Input: "abc" or "0" or "8"
Response: "Invalid choice. Please enter a number between 1 and 7."
Re-prompt for input
```

### 6.2 Invalid Task ID (Numeric Input)

```
Input: Non-existent ID (e.g., 999)
Response: "Error: Task with ID 999 not found."
Return to main menu
```

### 6.3 Non-Numeric Task ID

```
Input: "abc" when prompted for task ID
Response: "Error: Please enter a valid number."
Re-prompt for input (up to 3 attempts, then abort to menu)
```

### 6.4 Empty Task List Operations

```
Attempt: View, Update, Delete, Mark Complete, Mark Incomplete
Response: Same error handling as invalid ID
Message: "Error: Task with ID {id} not found."
```

### 6.5 Already Complete/Incomplete

```
Attempt: Mark complete an already complete task
Response: "Task {id} is already complete."

Attempt: Mark incomplete an already incomplete task
Response: "Task {id} is already incomplete."
```

### 6.6 Empty Description

```
Input: "" or "   " when adding/updating description
Response: "Error: Description cannot be empty."
```

---

## 7. Technical Requirements

### 7.1 Implementation Constraints

- Python 3.9+ (standard library only, no external dependencies)
- No database connections
- No file I/O
- No HTTP server or web framework
- No authentication code
- No API layer
- No AI/ML integrations

### 7.2 Code Organization

```
todo_app/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── task.py          # Task and TaskStatus classes
├── services/
│   ├── __init__.py
│   └── todo_service.py  # Business logic for task operations
├── cli/
│   ├── __init__.py
│   └── menu.py          # Menu display and input handling
└── main.py              # Application entry point
```

### 7.3 Entry Point

The application starts from `main.py`:

```python
from cli.menu import TodoMenu
from services.todo_service import TodoService

def main():
    service = TodoService()
    menu = TodoMenu(service)
    menu.run()

if __name__ == "__main__":
    main()
```

### 7.4 Testing Requirements

- Unit tests for TodoService
- Unit tests for CLI input handling
- No integration tests required in Phase I
- Test coverage target: 80%+

---

## 8. Out of Scope Features

The following are explicitly NOT part of Phase I and must not be implemented:

### 8.1 Data Persistence
- No database storage (SQL, NoSQL)
- No file-based persistence (JSON, CSV, text files)
- No export/import functionality

### 8.2 User Management
- No user accounts
- No login/logout
- No user preferences
- No multiple user support

### 8.3 Advanced Task Features
- No due dates
- No priorities
- No categories or tags
- No subtasks
- No task dependencies
- No recurring tasks
- No reminders or notifications

### 8.4 AI/Agent Features
- No task suggestions
- No auto-categorization
- No natural language processing
- No agent integration (Phase II scope)

### 8.5 API/Web Features
- No REST API
- No HTTP server
- No web frontend
- No webhooks
- No GraphQL

### 8.6 Collaboration Features
- No shared task lists
- No comments on tasks
- No assignments to other users
- No real-time sync

---

## 9. Definition of Done

Phase I is complete when:

- [ ] All acceptance criteria verified
- [ ] Code passes all tests (80%+ coverage)
- [ ] Code reviewed and approved
- [ ] Application runs without errors
- [ ] All out-of-scope features confirmed absent
- [ ] Phase baseline established for Phase II

---

## 10. Traceability

| Feature | User Story | Tasks |
|---------|------------|-------|
| Add Task | Section 2.1 | T-001 through T-003 |
| View Tasks | Section 2.2 | T-004 through T-006 |
| Update Task | Section 2.3 | T-007 through T-009 |
| Delete Task | Section 2.4 | T-010 through T-012 |
| Mark Complete | Section 2.5 | T-013 through T-015 |
| Mark Incomplete | Section 2.6 | T-016 through T-018 |

---

**Specification Version:** 1.0
**Approved:** Yes
**Phase:** I - Foundation
**Next Review:** Phase I completion
