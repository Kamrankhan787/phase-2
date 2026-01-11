import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Evolution of Todo API"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
    secret_key: str = os.getenv("SECRET_KEY", "supersecretkey")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    better_auth_secret: str = os.getenv("BETTER_AUTH_SECRET", "secret")
    better_auth_url: str = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"

settings = Settings()
