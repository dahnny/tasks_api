"""
FastAPI Task Management Application

This module serves as the main entry point for the Task Management API.
It sets up the FastAPI application, creates database tables, and includes
all the necessary routers for authentication, user management, and task operations.
"""

from fastapi import FastAPI
from app.models.base import Base
from app.database import engine
from app.models import user as user_models, task as task_models
from app.routes import user, auth, task

# Initialize FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A RESTful API for managing tasks and user authentication",
    version="1.0.0"
)

@app.get("/")
async def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A simple welcome message
    """
    return {"message": "Hello, World!"}

# Create all database tables
Base.metadata.create_all(bind=engine)

# Include API routers
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(task.router)