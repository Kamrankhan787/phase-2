from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .api import todos, auth, chat
from .core.database import init_db

# Load environment variables
load_dotenv()



app = FastAPI(title="Evolution of Todo API")

# Configure CORS - Explicit origins required when allow_credentials=True
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://[::1]:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(todos.router)
app.include_router(auth.router)
app.include_router(chat.router)  # Phase III: Chat endpoint

@app.get("/")
def read_root():
    return {"message": "Welcome to the Evolution of Todo API (Phase II)"}
