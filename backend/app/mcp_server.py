"""
MCP Server for Task Operations
Implements tools: add_task, list_tasks, complete_task, delete_task, update_task
"""
from datetime import datetime
from typing import Optional
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, TextContent
from sqlmodel import Session, select
from .core.database import engine
from .models.models import Task

# Initialize MCP Server using FastMCP (High-level API with .tool() support)
mcp_server = FastMCP("todo-task-server")

@mcp_server.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None) -> dict:
    """
    Create a new task
    
    Args:
        user_id: User identifier (required)
        title: Task title (required)
        description: Task description (optional)
    
    Returns:
        {"task_id": int, "status": "created", "title": str}
    """
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=title,
            description=description,
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title
        }

@mcp_server.tool()
async def list_tasks(user_id: str, status: Optional[str] = "all") -> list[dict]:
    """
    Retrieve tasks from the list
    
    Args:
        user_id: User identifier (required)
        status: Filter by status - "all", "pending", "completed" (optional, default: "all")
    
    Returns:
        Array of task objects
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.user_id == user_id)
        
        if status == "pending":
            statement = statement.where(Task.completed == False)
        elif status == "completed":
            statement = statement.where(Task.completed == True)
        # "all" returns everything
        
        tasks = session.exec(statement).all()
        
        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            for task in tasks
        ]

@mcp_server.tool()
async def complete_task(user_id: str, task_id: int) -> dict:
    """
    Mark a task as complete
    
    Args:
        user_id: User identifier (required)
        task_id: Task ID to complete (required)
    
    Returns:
        {"task_id": int, "status": "completed", "title": str}
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")
        
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "completed",
            "title": task.title
        }

@mcp_server.tool()
async def delete_task(user_id: str, task_id: int) -> dict:
    """
    Remove a task from the list
    
    Args:
        user_id: User identifier (required)
        task_id: Task ID to delete (required)
    
    Returns:
        {"task_id": int, "status": "deleted", "title": str}
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")
        
        title = task.title
        task_id_val = task.id
        session.delete(task)
        session.commit()
        
        return {
            "task_id": task_id_val,
            "status": "deleted",
            "title": title
        }

@mcp_server.tool()
async def update_task(
    user_id: str, 
    task_id: int, 
    title: Optional[str] = None, 
    description: Optional[str] = None
) -> dict:
    """
    Modify task title or description
    
    Args:
        user_id: User identifier (required)
        task_id: Task ID to update (required)
        title: New task title (optional)
        description: New task description (optional)
    
    Returns:
        {"task_id": int, "status": "updated", "title": str}
    """
    with Session(engine) as session:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        
        if not task:
            raise ValueError(f"Task {task_id} not found for user {user_id}")
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        
        return {
            "task_id": task.id,
            "status": "updated",
            "title": task.title
        }
