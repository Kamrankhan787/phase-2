from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid
from ..models.models import Todo, User
from ..core.database import get_session
# Placeholder for current_user dependency which will integrate with Better Auth
from ..dependencies.auth import get_current_user

router = APIRouter(prefix="/api/todos", tags=["todos"])

@router.post("/", response_model=Todo)
def create_todo(
    todo: Todo,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    todo.user_id = current_user.id
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.get("/", response_model=List[Todo])
def read_todos(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # CRITICAL: User level data isolation
    statement = select(Todo).where(Todo.user_id == current_user.id)
    return session.exec(statement).all()

@router.patch("/{todo_id}/toggle", response_model=Todo)
def toggle_todo(
    todo_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    db_todo = session.exec(statement).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_todo.completed = not db_todo.completed
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: uuid.UUID,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    db_todo = session.exec(statement).first()
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    session.delete(db_todo)
    session.commit()
    return {"ok": True}
