from typing import Optional

class InputHandler:
    """
    Handles raw user input and basic validation.
    Satisfies Phase I Plan §5, §6.
    """
    @staticmethod
    def get_int(prompt: str) -> Optional[int]:
        """Safely gets an integer from the user."""
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Please enter a valid numerical ID.")
            return None

    @staticmethod
    def get_string(prompt: str) -> str:
        """Gets a string from the user."""
        return input(prompt).strip()

    @staticmethod
    def get_menu_choice(prompt: str) -> Optional[int]:
        """Safely gets a menu choice."""
        try:
            return int(input(prompt))
        except ValueError:
            return None
