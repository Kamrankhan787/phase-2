"""Menu controller for the Todo application CLI."""

from cli.input_handler import InputHandler
from models.task import TaskStatus
from services.todo_service import TodoService


class TodoMenu:
    """Handles menu display and user interaction for the todo application."""

    def __init__(self, service: TodoService):
        """Initialize the menu with a todo service.

        Args:
            service: The TodoService instance for task operations.
        """
        self._service = service
        self._input = InputHandler()

    def run(self):
        """Run the main application loop."""
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
        """Route to the appropriate handler based on menu choice.

        Args:
            choice: The menu choice number.
        """
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
        """Handle adding a new task."""
        description = self._input.get_task_description()
        if description is None:
            return
        task = self._service.add_task(description)
        print(f"Task added successfully. ID: {task.id}")

    def _handle_view(self):
        """Handle viewing all tasks."""
        tasks = self._service.get_all_tasks()
        if not tasks:
            print("\nNo tasks found. Add a task to get started.")
            return

        print("\n=== Your Tasks ===\n")
        complete_count = 0
        for task in tasks:
            status_text = "Incomplete" if task.status == TaskStatus.INCOMPLETE else "Complete"
            print(f"[{task.id}] {status_text}: {task.description}")
            if task.status == TaskStatus.COMPLETE:
                complete_count += 1

        incomplete_count = len(tasks) - complete_count
        print(f"\nTotal: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")

    def _handle_update(self):
        """Handle updating a task."""
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
        """Handle deleting a task."""
        task_id = self._input.get_task_id("Enter task ID to delete: ")
        if task_id is None:
            return

        if self._service.delete_task(task_id):
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")

    def _handle_mark_complete(self):
        """Handle marking a task as complete."""
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
        """Handle marking a task as incomplete."""
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
        """Handle exiting the application."""
        print("Goodbye!")
