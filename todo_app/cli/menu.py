from todo_app.services.todo_service import TodoService, TaskNotFoundError, InvalidTaskError
from todo_app.cli.input_handler import InputHandler

class Menu:
    """
    Handles the presentation logic and main loop.
    Satisfies Phase I Spec §4 and Plan §4.
    """
    def __init__(self, service: TodoService):
        self.service = service
        self.input_handler = InputHandler()

    def display_menu(self):
        print("\n" + "="*30)
        print("   Evolution of Todo (Phase I)  ")
        print("="*30)
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Completion Status")
        print("6. Exit")
        print("="*30)

    def run(self):
        while True:
            self.display_menu()
            choice = self.input_handler.get_menu_choice("Choose an option: ")

            if choice == 1:
                self._view_tasks()
            elif choice == 2:
                self._add_task()
            elif choice == 3:
                self._update_task()
            elif choice == 4:
                self._delete_task()
            elif choice == 5:
                self._toggle_task()
            elif choice == 6:
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-6.")

    def _view_tasks(self):
        tasks = self.service.get_all_tasks()
        if not tasks:
            print("\nNo tasks found.")
            return

        print("\nYour Tasks:")
        print("-" * 30)
        print(f"{'ID':<4} | {'Status':<8} | {'Description'}")
        print("-" * 30)
        for task in tasks:
            status = "[Done]" if task.is_completed else "[Pending]"
            print(f"{task.id:<4} | {status:<8} | {task.description}")
        print("-" * 30)

    def _add_task(self):
        description = self.input_handler.get_string("Enter task description: ")
        try:
            task = self.service.add_task(description)
            print(f"Success: Task added with ID {task.id}.")
        except InvalidTaskError as e:
            print(f"Error: {e}")

    def _update_task(self):
        task_id = self.input_handler.get_int("Enter Task ID to update: ")
        if task_id is None:
            return

        new_description = self.input_handler.get_string("Enter new description: ")
        try:
            self.service.update_task(task_id, new_description)
            print("Success: Task updated.")
        except (TaskNotFoundError, InvalidTaskError) as e:
            print(f"Error: {e}")

    def _delete_task(self):
        task_id = self.input_handler.get_int("Enter Task ID to delete: ")
        if task_id is None:
            return

        try:
            self.service.delete_task(task_id)
            print("Success: Task deleted.")
        except TaskNotFoundError as e:
            print(f"Error: {e}")

    def _toggle_task(self):
        task_id = self.input_handler.get_int("Enter Task ID to toggle: ")
        if task_id is None:
            return

        try:
            task = self.service.toggle_task_status(task_id)
            status = "completed" if task.is_completed else "incomplete"
            print(f"Success: Task {task_id} is now {status}.")
        except TaskNotFoundError as e:
            print(f"Error: {e}")
