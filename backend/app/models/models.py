from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    auth_provider_id: Optional[str] = Field(default=None, unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    todos: List["Todo"] = Relationship(back_populates="owner")

class Todo(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="todos")
