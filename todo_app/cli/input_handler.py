"""Input handler for user input validation and parsing."""


class InputHandler:
    """Handles all user input validation and parsing.

    This class provides methods to validate and parse user input
    for the todo application CLI.
    """

    def get_menu_choice(self) -> Optional[int]:
        """Get and validate a menu selection.

        Returns:
            An integer between 1 and 7 if valid, None otherwise.
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

    def get_task_id(self, prompt: str) -> Optional[int]:
        """Get and validate a task ID from user input.

        Args:
            prompt: The prompt message to display.

        Returns:
            A positive integer if valid, None otherwise.
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

    def get_task_description(self) -> Optional[str]:
        """Get and validate a task description.

        Returns:
            The trimmed description string if valid (non-empty, <= 500 chars),
            None otherwise.
        """
        description = input("Enter task description: ").strip()
        if not description:
            print("Error: Description cannot be empty.")
            return None
        if len(description) > 500:
            print("Error: Description must be 500 characters or less.")
            return None
        return description
