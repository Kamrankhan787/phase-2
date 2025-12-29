# Evolution of Todo

A Python console application for task management, built following spec-driven development principles.

## Project Overview

This project evolves through 5 phases:
- **Phase I**: Foundation - In-memory console todo app
- **Phase II**: Agent Integration - AI-powered task management
- **Phase III**: Multi-Agent Coordination - Collaborative task handling
- **Phase IV**: Advanced Orchestration - Workflow management
- **Phase V**: Production Scale - Cloud-native distributed system

## Phase I Features

- Add, view, update, and delete tasks
- Mark tasks as complete/incomplete
- In-memory data storage (no persistence beyond runtime)
- Menu-driven CLI interface
- Input validation and error handling

## Quick Start

```bash
cd todo_app
python main.py
```

## Project Structure

```
todo_app/
├── main.py                    # Application entry point
├── models/
│   └── task.py                # Task and TaskStatus definitions
├── services/
│   └── todo_service.py        # Business logic
├── cli/
│   ├── input_handler.py       # Input validation
│   └── menu.py                # CLI interface
└── tests/                     # Unit tests
```

## Running Tests

```bash
cd todo_app
python -m pytest tests/ -v
```

## Tech Stack (Phase I)

- Python 3.9+
- Standard library only (no external dependencies)
- Clean architecture principles

## Constitution

This project follows the [Constitution](sp.constitution) which mandates:
- Spec-Driven Development (Constitution → Specs → Plan → Tasks → Implement)
- No feature invention outside specifications
- Phase isolation (no future-phase features)
