import sys
from todo_app.services.todo_service import TodoService
from todo_app.cli.menu import Menu

def main():
    """
    Application entry point.
    Satisfies Phase I Plan §1.
    """
    try:
        service = TodoService()
        app = Menu(service)
        app.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
