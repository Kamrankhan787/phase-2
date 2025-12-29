"""Entry point for the Todo application."""

from cli.menu import TodoMenu
from services.todo_service import TodoService


def main():
    """Application entry point."""
    service = TodoService()
    menu = TodoMenu(service)
    menu.run()


if __name__ == "__main__":
    main()
