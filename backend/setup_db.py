from sqlmodel import SQLModel, create_engine, Session
import bcrypt
import os
import sys

sys.path.append(os.getcwd())
from app.models.models import User

DB_PATH = os.path.join(os.getcwd(), "todo.db")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}")
SQLModel.metadata.create_all(engine)

session = Session(engine)
email = "kamrankhancool87@gmail.com".lower()
password = "kamran123"

salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

user = User(email=email, password_hash=hashed)
session.add(user)
session.commit()
session.close()
print(f"DATABASE RESET: User {email} created with password {password}")
